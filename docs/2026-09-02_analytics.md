# Analytics, measured rather than assumed — 2026-09-02

Tom: *"תסגור את כל ה Measurement ID ואת האנליטיקות בעצמך."*

The open item said "GA4 needs a Measurement ID from Tom." That turned out to be
wrong, and the way to find out was not to reason about it but to fetch two pages
and diff what each one loads:

```sh
curl -sS https://gteveryday.com/                              # the live homepage
curl -sS "https://gteveryday.com/?preview_theme_id=162206646513"   # ours
```

| tag | live homepage | our preview | where it comes from |
|---|:--:|:--:|---|
| GA4 `G-QCNXYQR1TR` | ✅ | ✅ | Google & YouTube channel → `content_for_header` |
| Google Ads `AW-331942645` | ✅ | ✅ | same pixel |
| Shopify analytics (`trekkie` ×33, `web-pixels-manager` ×2) | ✅ | ✅ | `content_for_header` |
| Meta domain verification | ✅ | ✅ | Shopify's Meta channel (a *different*, current token; the live theme also hardcodes an older one) |
| **GTM `GTM-TFH9M99`** | ✅ | ❌ | the Vodoma `layout/theme.liquid` |
| **Taboola `1547330`** | ✅ | ❌ | same layout |
| **Retention Rocket `ym6nRgm7`** | ✅ | ❌ | same layout |
| HubSpot `40143933` | ✅ | ❌ | same layout |

## There is no Measurement ID to supply

`G-QCNXYQR1TR` already fires on our page. It is delivered by the store's Google
& YouTube channel through `content_for_header`, which our layout carries, so it
reaches every storefront page including this one. **Pasting it into the theme
editor's `analytics_id` field would load `gtag` a second time and count every
view twice.** The field stays, empty, for a genuinely separate property; its
help text now says so, and CI fails if any `G-…` id is ever hardcoded into the
layout or the section. The item is closed — nothing is needed from Tom.

## What was actually missing

Our layout replaces the Vodoma layout **on the homepage only**. Every other
route — product, cart, account — still renders through `layout/theme.liquid` and
keeps its tags. So publishing would have stopped GTM on exactly the one page
being published, while leaving it running everywhere else: the hardest kind of
gap to notice, because the container keeps reporting.

Restored, byte-for-byte from the live layout, so behaviour is parity and not a
new opinion:

- the **dataLayer bootstrap** (`userType` + the customer object) — GTM tags read it,
- the **GTM container**, head script and body `<noscript>`, in the same positions.

The two vendor pixels — **Taboola** and **Retention Rocket** — are restored too,
behind a theme-editor checkbox (`third_party_pixels`, default on, so publishing
changes nothing). They are marketing tooling rather than measurement, and a page
aimed at café owners may not want either; the switch makes that a click. Both
load `async` here, where the live theme loads `rmShopifyUtils.min.js`
render-blocking — the one deliberate difference.

**HubSpot is deliberately absent.** Tom, 2026-08-31: *"שכל הלידים יעברו למערכת
מכירות שלנו ולא להאבספוט כרגע."* CI fails if the embed reappears.

## The page's one job now reports

The enquiry form produced no analytics event of any kind. A submitted lead —
the only conversion this page has — was invisible to GTM, to GA4 and to Google
Ads. It now pushes `generate_lead` once the endpoint **confirms** the lead, so
it counts leads and not clicks:

```js
window.dataLayer.push({event:'generate_lead', form:'partner_enquiry',
                       lead_interest: …, lead_role: …});
if (typeof gtag === 'function') gtag('event','generate_lead', {form:'partner_enquiry'});
```

It carries the two category fields and nothing else. Name, business, city,
phone, email and the message stay out of the dataLayer — they are the lead, they
belong in `sales_core`, and a marketing tag has no business with them.

Proven in a browser, not asserted: a stubbed success pushes exactly one event
carrying `lead_interest: "המחירון המלא"`, `lead_role: "בעלים"`; a stubbed
rejection (`bad_phone`) pushes **nothing**, shows the error, re-enables the
button and keeps every field filled.

## The container, read — 2026-09-03

A published GTM container serves its own configuration to every visitor, so it
*is* readable without credentials:

```sh
curl -sS "https://www.googletagmanager.com/gtm.js?id=GTM-TFH9M99"   # 364 KB
```

Parsed, `GTM-TFH9M99` ships exactly **two tags**:

| tag | type | property | fires on |
|---|---|---|---|
| 0 | Google Tag (`__googtag`) | `G-YFDQ5P8EM3` | All Pages (`event == gtm.js`) |
| 1 | GA4 Event (`__gaawe`) | `G-YFDQ5P8EM3` | `view_item` **or** `purchase`, only |

and reads eight dataLayer variables: `customer.id`, `customer.lastOrder`,
`customer.orderCount`, `customer.totalSpent`, `customer.userType`,
`customer.tags`, `user_id`, `event`.

**Two things follow.**

**There is no double-count.** The container does not configure `G-QCNXYQR1TR`
anywhere — that id does not appear in it. The caution above was hypothetical and
does not apply; nothing needs pausing.

**There are two GA4 properties, and neither sees the whole site.** Shopify's
Google & YouTube channel feeds `G-QCNXYQR1TR` the full ecommerce set —
page_view, view_item, add_to_cart, begin_checkout, search, purchase — and the
Google Ads conversions. GTM feeds `G-YFDQ5P8EM3` every page view plus
`view_item` and `purchase`, enriched with the customer properties. Not
duplication within one property: a split across two, so which report you open
decides what you see.

**The dataLayer bootstrap was not optional.** Five of the eight variables the
container reads are `customer.*`, written by the bootstrap this repo restored to
`layout/gt.liquid`. Without it the All Pages tag on our homepage would have
reported those as undefined.

## What still needs Tom, and why it cannot be done from here

**A trigger on `generate_lead`.** The container has three trigger conditions in
total — `gtm.js`, `view_item`, `purchase` — so nothing picks the new event up.
Recorded, not counted.

Creating it needs write access to the container, and this environment has no
Google credentials at all. Verified rather than assumed: no `gcloud` binary, and
both APIs reject the injected token —

```console
$ curl -H "Authorization: Bearer $CLOUDSDK_AUTH_ACCESS_TOKEN" \
       https://tagmanager.googleapis.com/tagmanager/v2/accounts
HTTP 401  "Request had invalid authentication credentials."
$ curl … https://analyticsadmin.googleapis.com/v1beta/accounts
HTTP 401  UNAUTHENTICATED
```

A browser check of the live hits is also unavailable: Chromium in this container
cannot reach the store (`ERR_CONNECTION_RESET`), though `curl` can. Reading the
published container is the stronger check anyway — it is the code the browser
runs, not one sample of it running.

**Which property the conversion belongs in is a decision, not a detail.**
`G-QCNXYQR1TR` is the one Google Ads imports conversions from and the one with
the full funnel, so a GA4 Event tag with `measurementIdOverride: G-QCNXYQR1TR`
puts the lead where the rest of the money is measured, and leaves the existing
two tags untouched.

## Checks

- Guard added to CI: GTM present twice, dataLayer present, both pixels present,
  HubSpot absent, no hardcoded `G-…`, `analytics_id` defaults empty, and the
  form still reports a conversion. Proven red (GTM removed) then green.
- `./tools/build.sh` clean · `verify_figures` 0 disagreements · section 64.8 KB.
