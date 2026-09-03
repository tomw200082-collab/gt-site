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
// ── WHAT /ingest KEEPS, AND WHAT IT DROPS ──────────────────────────────────
//
// Checked against the deployed normaliser (`_lib/ingest_body.ts`) and
// `sales_core.ingest_lead`, not assumed. On the flat shape this form uses, the
// meta that reaches the `created` event is exactly:
//
//     campaign_name campaign_id ad_name ad_id form_id form_name platform
//     is_organic
//
// `city` is mapped onto the lead object and then never passed to `ingest_lead`,
// which has no city parameter and never writes `org.city`. `role`, `interest`
// and the visitor's own message have no field in that contract at all.
//
// So everything the visitor typed beyond name / business / phone / email is
// this function's responsibility to store, and it stores it as a note event on
// the lead — human-readable text for whoever works the queue, plus the same
// answers as structured JSON beside it so nothing has to be parsed back out of
// a sentence.
//
// The note is written over a direct connection: PostgREST is not an option,
// because `sales_core` is deliberately off its exposed-schema list — those
// tables have RLS disabled, and exposing the schema would make every lead
// readable with the public anon key.
//
// Two things about that write, both learned the hard way:
//
//   * It uses `DATABASE_URL_POOLED` and `npm:pg`, which is what the poll
//     function itself uses and what this project actually sets. An earlier
//     version reached for `SUPABASE_DB_URL` and `deno.land/x/postgres`; that
//     path has never once produced a note.
//   * It inserts the `lead_event` row itself instead of calling
//     `sales_core.add_lead_note`, because that function also calls
//     `touch_first`, which sets `first_touch_at`. A lead born already "first
//     touched" — by nobody — is a lead that looks handled before anyone has
//     seen it.
//
// GET ?health=db opens that connection and runs `select 1`, so the note path
// can be proven without putting a test lead into the sales queue.
import pg from "npm:pg@8.11.3";

const { Pool } = pg;

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

const dbUrl = () =>
  Deno.env.get("DATABASE_URL_POOLED") ?? Deno.env.get("SUPABASE_DB_URL") ?? "";

// The pg default export is a CommonJS namespace object, so its client type is
// not reachable as `pg.PoolClient` here; the shape used below is one method.
// deno-lint-ignore no-explicit-any
async function withDb<T>(fn: (c: any) => Promise<T>): Promise<T> {
  const pool = new Pool({ connectionString: dbUrl(), max: 1 });
  try {
    const c = await pool.connect();
    try {
      return await fn(c);
    } finally {
      c.release();
    }
  } finally {
    await pool.end().catch(() => {});
  }
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });

  // Proves the note path without creating a lead. Says whether this function
  // can reach the database and nothing else — no schema, no data, no secret.
  if (req.method === "GET" && new URL(req.url).searchParams.get("health") === "db") {
    if (!dbUrl()) return json({ db: "unconfigured" }, 200, origin);
    try {
      await withDb((c) => c.query("select 1"));
      return json({ db: "ok" }, 200, origin);
    } catch (e) {
      console.error("health db", String(e));
      return json({ db: "error" }, 200, origin);
    }
  }

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
  const role = s("role");
  const interest = s("interest");
  const message = s("message");
  const phone = s("phone");
  const email = s("email");
  const page = typeof b.page === "string" ? b.page.slice(0, 300) : "";
  const referrer = typeof b.referrer === "string" ? b.referrer.slice(0, 300) : "";

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

  // Everything /ingest has no field for. Written as a note event: readable text
  // for whoever works the queue, and the same answers as JSON beside it.
  //
  // Best-effort by design — the lead is already stored and alerted, and a
  // missing note must never turn a captured enquiry into an error the visitor
  // sees. One retry, because a cold pooled connection failing once is common
  // and losing what the visitor wrote is not acceptable.
  let noteOk: boolean | null = null;
  if (out?.was_new && out?.lead_id) {
    const lines = [
      "טופס האתר",
      `עיר: ${city}`,
      role && `תפקיד: ${role}`,
      interest && `מתעניין ב: ${interest}`,
      message && `הודעה: ${message}`,
      page && `עמוד: ${page}`,
      referrer && `הגיע מ: ${referrer}`,
    ].filter(Boolean).join("\n");

    const payload = {
      note: lines,
      form: {
        form_name: "partner_enquiry",
        city, role: role || null, interest: interest || null,
        message: message || null, page: page || null, referrer: referrer || null,
      },
    };

    for (let attempt = 1; attempt <= 2 && noteOk !== true; attempt++) {
      try {
        await withDb((c) =>
          c.query(
            `insert into sales_core.lead_event (lead_id, event_type, payload, actor)
             values ($1, 'note', $2::jsonb, 'system:website_form')`,
            [out.lead_id, JSON.stringify(payload)],
          )
        );
        noteOk = true;
      } catch (e) {
        noteOk = false;
        // Loud on purpose: this is the line that says a visitor's message did
        // not reach the people who answer it.
        console.error("WEBSITE_LEAD_NOTE_FAILED", {
          attempt, lead_id: out.lead_id, error: String(e).slice(0, 300),
        });
      }
    }
  }

  console.log("lead ingested", {
    external_id, lead_id: out?.lead_id, was_new: out?.was_new,
    alerted: out?.alerted, note: noteOk,
  });
  return json({ ok: true, was_new: out?.was_new ?? null }, 200, origin);
});
