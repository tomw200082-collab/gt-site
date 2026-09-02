# Publishing the site

The theme is built, uploaded and unpublished. This is the whole procedure for
making it live, and the whole procedure for putting it back.

**Nothing here runs without Tom's written word.** A session executing this file
must be able to quote the instruction it is acting on.

| | |
|---|---|
| New theme | `162206646513` · `GT Site v5 — Hebrew (do not publish)` · **UNPUBLISHED** |
| Live theme | `131669328113` · `HE-RU Vodoma 2024` · **MAIN** |
| Preview | `https://gteveryday.com/?preview_theme_id=162206646513` |
| Rollback | publish `131669328113` again — see §4 |

---

## 1. Blockers — the site must not go live while any of these stands

Tom answered four of these on 2026-08-31. His answers are recorded in
`docs/2026-08-31_decisions.md` with an authority grade, per truth rule 1.

| # | Blocker | State |
|---|---|---|
| B1 | `20–30% פחות אלכוהול מאשר לפני עשור` | **Cleared.** The concern was raised — no source exists in any repo — and Tom's decision was to leave the sentence exactly as written. It is now `user_confirmed` rather than unsourced, which is a grade the constitution recognises. Do not re-open it as a finding |
| B2 | Tom has not opened the preview in a real browser. No Claude session can render the live store | **Open — Tom** |
| B3 | The wholesale price list is public: the `#pricing` section, 27 of the page's 105 prices | **Scope settled, flip deferred.** Tom 2026-09-02: the switch covers *the price list only* — the recommended per-cup prices and margins stay. He asked that it not be turned off yet, so the default stays on. `show_pricing` in the theme editor does it in one click, both ways, without touching a figure. `U-003` stays open until he flips it |
| B4 | The About section has no photographs | **Open — Tom** |
| B5 | `Don't Drink Boring.` in the footer | **Settled.** Deliberate; stays in English |

None of the remaining three is a correctness failure. B2 and B4 are Tom's to
supply; B3 is a commercial posture whose mechanism is built, scoped and
proven in both states — it is now a click Tom makes when he wants it.

---

## 2. Pre-flight — run these and read the output

```sh
cd gt-site
./tools/build.sh              # rebuilds and validates; fails loudly on a moved anchor
python3 tools/verify_figures.py   # every figure against the record — must say 0 disagreements
python3 tools/sync_figures.py --check
python3 tools/build_theme.py
git status --porcelain        # must be empty: the committed build is the build
```

Then confirm on the store, not in a browser — a preview cookie makes a browser
lie about which theme is live:

```
theme 162206646513 -> role must still be UNPUBLISHED
theme 131669328113 -> role must still be MAIN
```

If either has changed since this file was written, **stop** and find out who
changed it.

---

## 3. Publishing

1. Quote Tom's instruction in the session, in writing.
2. Re-run §2. Green, or stop.
3. Publish `162206646513` (Shopify Admin → Online Store → Themes → Publish, or
   `themePublish` on the Admin API).
4. Confirm `131669328113` has become `UNPUBLISHED` and `162206646513` is `MAIN`.
5. Tell Tom it is live, with the time.

Do not delete `131669328113`. It is the rollback.

---

## 4. Rollback

Publishing the old theme back is the undo, and it is complete: the old theme was
never modified.

```
publish 131669328113   ->  HE-RU Vodoma 2024 becomes MAIN again
```

Nothing else needs undoing. The new theme keeps its files and returns to
UNPUBLISHED. No customer data, no product, no price and no inventory is touched
by publishing or un-publishing either theme.

The one thing that does **not** roll back: `website_lead_intake` keeps
accepting enquiries, because it is an Edge Function and not part of the theme.
That is correct — a lead already submitted should not be lost by a rollback.

---

## 5. The first ten minutes

In this order, because the later ones matter less if an earlier one fails.

1. **The homepage renders**, on a phone and on a desktop, in a browser with no
   preview cookie. Use a private window — an ordinary one may still hold the
   cookie from previewing and will show you the new site either way.
2. **The enquiry form lands a lead.** Submit a real one and check it appears:
   ```sql
   select id, contact_name, phone_e164, created_at
     from sales_core.lead
    where source = 'website_form'
    order by created_at desc limit 5;
   ```
   Then confirm the alert email arrived. If the row is there and the email is
   not, the lead is safe — `routeIngest` stores before it alerts, and the poll's
   sweep retries an alert that failed.
3. **The store's own routes still work**: a product page, the cart, the account
   page. They render from the Vodoma layer underneath, so if one is wrong it was
   wrong before — but check, because customers use them.
4. **Prices on the page match the record.** Spot-check three: מאצ'ה קוקוס תות
   ₪44, אייס מאצ'ה מנגו ₪39, דירטי צ'אי ₪32.
5. **Shopify analytics is recording sessions.** The layout carries
   `content_for_header`, so the store's own analytics and any app pixels are
   live automatically.

---

## 6. Who to tell

- **Tom** — first, with the time it went live.
- **Avi and Alex** — they take leads, and the form now creates them. They should
  know enquiries will start arriving from a new source (`source = 'website_form'`
  in the queue) before the first one lands.
- **Nobody external.** There is no announcement in scope here.

---

## 7. What is deliberately not automated

Publishing is a single irreversible-feeling action with a one-step undo, and it
is the one thing on this project that is Tom's alone. There is no script in
`tools/` that publishes, and there should not be one.
