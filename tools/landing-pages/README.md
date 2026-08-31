# Category landing pages

Four Hebrew landing pages for the GT Shopify theme
`GT Site v5 — Hebrew (do not publish)` (id `162206646513`):
`צ'אי` · `מאצ'ה` (+ הוג'יצ'ה) · `תה קר` · `אובה`.

They ride `layout/gt.liquid` — the chrome-free layout the theme already had —
so each page is one JSON template plus one section. No theme fork, no nav, no footer.

## Regenerate

```bash
python3 gen.py          # -> out/gt-lp-<slug>.liquid + out/page.<slug>.json
```

`out/gt-lp.css` and `out/gt-lp.js` are hand-written and not generated.

**Do not hand-edit `out/gt-lp-*.liquid`.** Four pages from one template is the point:
if the fourth needs an edit the first three did not, the template is wrong.

## Where the figures come from

`catalog.py` is the 48 drinks transcribed from Canva design `DAHTYkRvEnM`
(`קטלוג משקאות סופי 26`), read live 2026-08-31. It is proven equal to
`gt-factory-os-production-brain/.claude/skills/drinks-pricelist/drinks_final_figures.json`
(2026-08-27): 48/48 names matched, 0 figure deviations, and margin independently
re-derived from `price/1.18 − cost` with 0/48 mismatches.

`drinks.py` adds the preparation steps and assigns each drink to exactly one page
(16 / 11 / 16 / 5 = 48), asserting row-by-row against `catalog.py` so the two
cannot drift apart silently.

Never type a figure into a section by hand. Change the catalog, re-verify, regenerate.

## Lead capture

Each page's form posts JSON to the Make webhook set in the section's
`lead_webhook` setting. Make holds `LEAD_INGEST_TOKEN` and calls the `ingest`
route on the `sales-leads-poll` Edge Function; the browser never sees the secret.
The per-page discriminator is `source` (`site-chai`, `site-matcha`,
`site-iced-tea`, `site-ube`) — `sales_core.lead.source`, unique with `external_id`.

With no webhook set the form falls back to WhatsApp with the details prefilled,
so a submission is never silently lost.
