// Public intake for the brand site's enquiry form.
//
// The form used to build a `mailto:` and set its own "sent" class whether or not
// a mail client existed, so on most phones an enquiry vanished silently. This is
// what replaces it.
//
// It does NOT ingest the lead itself. `sales-leads-poll` already owns a POST
// /ingest route, and its own normaliser names "a future website form" as an
// intended caller. That route ingests, matches the enquirer against Shopify,
// emails the staff allowlist through Resend, writes the `alert_sent` event that
// the `lead_alert_fanout` trigger watches, and files anything it cannot map into
// `sales_core.lead_reject` rather than dropping it. Reimplementing any of that
// here would have produced a lead nobody was told about.
//
// So this function is the thin public edge that route cannot be: it terminates
// CORS, rejects junk, and holds the two secrets a browser must never see — the
// service-role JWT that satisfies verify_jwt, and LEAD_INGEST_TOKEN.
//
// Deployed with verify_jwt = false, because a website visitor has no token.
// Every other defence is below.
//
// The one thing /ingest's contract has no field for is free text. The visitor's
// message, role and interest are attached afterwards as a lead note, which is
// where free text belongs, over a direct connection — PostgREST is not an
// option here: `sales_core` is deliberately off its exposed-schema list, since
// those tables have RLS disabled and exposing the schema would make every lead
// readable with the public anon key.
import { Pool } from "https://deno.land/x/postgres@v0.17.0/mod.ts";

const ALLOWED_ORIGINS = [
  "https://gteveryday.com",
  "https://www.gteveryday.com",
  "https://greenteaeveryday.myshopify.com",
];

const MAX_BODY = 8 * 1024; // an enquiry is a few hundred bytes
const LIMITS: Record<string, number> = {
  contact_name: 120, venue: 160, city: 80, role: 80,
  phone: 40, email: 160, interest: 120, message: 2000,
};

function cors(origin: string | null) {
  const allow = origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}

const json = (body: unknown, status: number, origin: string | null) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...cors(origin) },
  });

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405, origin);

  const raw = await req.text();
  if (raw.length > MAX_BODY) return json({ error: "too_large" }, 413, origin);

  let b: Record<string, unknown>;
  try {
    b = JSON.parse(raw);
  } catch {
    return json({ error: "bad_json" }, 400, origin);
  }

  const s = (k: string) =>
    typeof b[k] === "string" ? (b[k] as string).trim().slice(0, LIMITS[k] ?? 200) : "";

  // Honeypot: a field positioned off-screen and never shown to a person. Bots
  // fill every input they find. Answer 200 so the bot learns nothing.
  if (s("company_website") !== "") return json({ ok: true }, 200, origin);

  // A person cannot read nine fields and submit in under three seconds.
  const elapsed = Number(b.elapsed_ms);
  if (Number.isFinite(elapsed) && elapsed < 3000) return json({ ok: true }, 200, origin);

  const contact_name = s("contact_name");
  const venue = s("venue");
  const city = s("city");
  const phone = s("phone");
  const email = s("email");
  const missing = [
    ["contact_name", contact_name], ["venue", venue], ["city", city], ["phone", phone],
  ].filter(([, v]) => !v).map(([k]) => k);
  if (missing.length) return json({ error: "missing_fields", missing }, 400, origin);
  if (!/\d/.test(phone) || phone.replace(/\D/g, "").length < 9) {
    return json({ error: "bad_phone" }, 400, origin);
  }
  if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ error: "bad_email" }, 400, origin);
  }

  const token = Deno.env.get("LEAD_INGEST_TOKEN");
  const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  const baseUrl = Deno.env.get("SUPABASE_URL");
  if (!token || !serviceKey || !baseUrl) {
    console.error("intake not configured", {
      LEAD_INGEST_TOKEN: !!token, SUPABASE_SERVICE_ROLE_KEY: !!serviceKey, SUPABASE_URL: !!baseUrl,
    });
    return json({ error: "not_configured" }, 503, origin);
  }

  // One lead per number per day. /ingest is idempotent on (source, external_id),
  // so a double-tapped submit button is one lead, and a single submitter cannot
  // flood the queue.
  const digits = phone.replace(/\D/g, "");
  const day = new Date().toISOString().slice(0, 10);
  const external_id = `web-${day}-${digits.slice(-9)}`;

  let res: Response;
  try {
    res = await fetch(`${baseUrl}/functions/v1/sales-leads-poll/ingest`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "authorization": `Bearer ${serviceKey}`,
        "x-lead-ingest-token": token,
      },
      body: JSON.stringify({
        route: "ingest",
        source: "website_form",
        external_id,
        contact_name,
        phone,
        email: email || null,
        display_name: venue,
        city,
        created_at: new Date().toISOString(),
        form_name: "partner_enquiry",
        platform: "website",
        is_organic: true,
        // campaign_name is deliberately absent. The source_id taxonomy is still
        // an open draft (production-brain PR #188 §Q3) and the registry has not
        // issued a value for this path; inventing one would stamp a fabricated
        // campaign string on every website lead. Everything needed to backfill
        // it later is on the lead already.
      }),
    });
  } catch (e) {
    console.error("ingest unreachable", String(e));
    return json({ error: "ingest_unreachable" }, 502, origin);
  }

  const out = await res.json().catch(() => ({}));
  if (!res.ok || out?.ok === false) {
    console.error("ingest rejected", { status: res.status, body: out });
    return json({ error: "ingest_failed" }, 502, origin);
  }

  // Free text has no field in /ingest's contract, so it becomes a note on the
  // lead. Best-effort by design: the lead is already stored and alerted, and a
  // missing note must never turn a captured enquiry into an error the visitor
  // sees.
  const extras = [
    s("role") && `תפקיד: ${s("role")}`,
    s("interest") && `מתעניין ב: ${s("interest")}`,
    s("message") && `הודעה: ${s("message")}`,
    typeof b.page === "string" && b.page ? `עמוד: ${String(b.page).slice(0, 300)}` : "",
    typeof b.referrer === "string" && b.referrer
      ? `מקור: ${String(b.referrer).slice(0, 300)}` : "",
  ].filter(Boolean).join("\n");

  if (extras && out?.was_new && out?.lead_id) {
    const pool = new Pool(Deno.env.get("SUPABASE_DB_URL")!, 1, true);
    try {
      const conn = await pool.connect();
      try {
        await conn.queryObject`
          select sales_core.add_lead_note(
            ${out.lead_id}::uuid,
            ${`טופס האתר\n${extras}`}::text,
            ${"system:website_form"}::text)`;
      } finally {
        conn.release();
      }
    } catch (e) {
      console.error("note failed (lead is stored)", { lead_id: out.lead_id, error: String(e) });
    } finally {
      await pool.end().catch(() => {});
    }
  }

  console.log("lead ingested", {
    external_id, lead_id: out?.lead_id, was_new: out?.was_new, alerted: out?.alerted,
  });
  return json({ ok: true, was_new: out?.was_new ?? null }, 200, origin);
});
