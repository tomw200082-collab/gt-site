# What actually reaches the sales system when someone fills the form — 2026-09-03

Tom asked whether a website enquiry arrives in the sales system, is recognisable
as coming from the site, and shows the visitor's note and every field they
filled, in order. Checked against the deployed code and the live database rather
than against intent. The answer was **partly**, and the gap was mine.

## What the pipeline does with each field

`website_lead_intake` → `sales-leads-poll` `/ingest` → `sales_core.ingest_lead`.
Reading the deployed `_lib/ingest_body.ts` and the SQL function:

| the visitor types | where it ends up |
|---|---|
| name | `lead.contact_name` |
| business | `org.display_name` |
| phone | `lead.phone_raw` + `lead.phone_e164` (normalised) |
| email | `lead.email`, and `org.email` when the org is new |
| — | `lead.source = 'website_form'`, `platform = 'website'`, `form_name = 'partner_enquiry'`, `is_organic = true` |
| **city** | **nowhere.** The normaliser maps it onto the lead object; `routeIngest` never passes it to `ingest_lead`, which has no city parameter and never writes `org.city` |
| **role, interest, message** | **no field in the contract at all** |

On the flat shape this form uses, the meta that reaches the `created` event is
exactly `campaign_name campaign_id ad_name ad_id form_id form_name platform
is_organic`. Confirmed against every lead of the last fortnight: Facebook leads
carry those keys plus `unmapped_fields`, and nothing else.

So identification: **yes, and unambiguously.** Everything past name / business /
phone / email: **this function's job**, and it was not doing it.

## Why the one website lead in the database looks fine — and is not evidence

`804570a6` carries `city`, `role`, `interest`, `message`, `page` and `referrer`
in its `created` event. It was written on 2026-08-31 at 12:31, by the **second**
version of this function — the one that reimplemented ingestion and was then
thrown away for exactly that reason. The proxy version that replaced it went out
at 12:35 and **has never run**. That lead proves the discarded code worked, not
the deployed code.

## Two defects, both in code this repo owns

**1. The note write could not have worked.** Free text was attached with
`deno.land/x/postgres` over `SUPABASE_DB_URL`. The poll function — the one that
demonstrably talks to this database from the same runtime every five minutes —
uses `npm:pg@8.11.3` over **`DATABASE_URL_POOLED`**. There is not one
`lead_event` note from `system:website_form`; all fourteen notes in the table
are Avi's. Now on the same driver and the same variable, and provable:

```console
$ curl "…/website_lead_intake?health=db"
{"db":"ok"}
```

`GET ?health=db` opens the connection and runs `select 1`. It exists so this can
be checked without putting a test lead into the sales queue, and it reports
reachability and nothing else — no schema, no data, no secret.

**2. The note would have marked the lead as already handled.**
`sales_core.add_lead_note` calls `touch_first`, which sets `first_touch_at`. An
automated note a second after the lead is born would have stamped it as touched
before any person had seen it. The function now inserts the `lead_event` row
itself, so `first_touch_at` stays null until someone really makes contact.

## What a real enquiry produces now

A `note` event on the lead, actor `system:website_form`, carrying both a
readable Hebrew note and the same answers as structured JSON:

```
טופס האתר
עיר: תל אביב
תפקיד: בעלים
מתעניין ב: תמציות תה
הודעה: …what the visitor wrote…
עמוד: https://gteveryday.com/
```

```json
{"note": "…the text above…",
 "form": {"form_name":"partner_enquiry","city":"תל אביב","role":"בעלים",
          "interest":"תמציות תה","message":"…","page":"…","referrer":null}}
```

Written twice if the first attempt fails, and logged as
`WEBSITE_LEAD_NOTE_FAILED` if both do — a line that says a visitor's message did
not reach the people who answer it. The lead itself is never at risk: it is
already stored and alerted before the note is attempted.

## Two things still true, and not this repo's to change

- **The alert email does not carry the message.** `buildLeadAlert` takes
  `contact_name, display_name, phone_e164, email, campaign_name, ad_name,
  form_name, platform, created_at, is_known_customer, org_snapshot, unmapped` —
  no free text. Whoever opens the lead sees the note; whoever only reads the
  email sees that an enquiry arrived, not what it said. Fixing it means adding a
  field to `sales-leads-poll`, which belongs to the sales module.
- **`org.city` is still never written**, for any source. `ingest_lead` is shared
  by every intake path, so adding a city parameter is a sales-module decision,
  not a website one. Until then the city lives in the note.

## Verified

- `{"db":"ok"}` twice from the deployed function (v5).
- `sales_core.lead_event` accepts `event_type = 'note'` — fourteen existing rows
  prove the shape; `lead_alert_fanout` fires only on `alert_sent`, so a note
  triggers nothing.
- Not verified end to end: a real submission, because it puts a lead in the
  queue and emails three people. Everything up to the insert is proven.
