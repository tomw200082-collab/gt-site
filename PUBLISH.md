# Publishing the site

**One path, for every change:** stage the whole GT file set, push all of it, and check the theme
against it file by file. `tools/theme_ship.py` does all three. The live theme is updated in place
with the Shopify CLI. It is never swapped for a copy.

**Nothing reaches the live theme without Tom's written word.** A session pushing to it must be
able to quote the instruction it is acting on.

| | |
|---|---|
| Live theme | `166730072305` · `GT 2026 Site — כניסת לקוחות` · **MAIN**. Carries `main` at `73c302e` (#30), pushed 2026-09-29 with `drift: 0` on Tom's word of 2026-09-28 night (quoted in #30's gate record) |
| Preview | `186698334449` · `GT site — preview 2026-09-27` · unpublished. Duplicated from MAIN on 2026-09-27 and reused: each round re-pushes the whole set |
| Preview link | `https://gteveryday.com/?preview_theme_id=186698334449` |
| Superseded | `186686636273` (`כניסה לעסקים`): its two changes, #23 and #25, went live with `73c302e` on 2026-09-29. It is not to be published. `166741213425` and `166708576497` are older copies of MAIN. None of the three holds anything that `main` or MAIN lacks (compared file by file, 2026-09-27), so all three are safe to delete |
| Rollback | push the previous set: check out the commit that was live, then run `python3 tools/theme_ship.py push 166730072305 --allow-live`. Before 2026-09-29 the live set was `8a19041` (#24) |

---

## 1. Why there is one path

On 2026-09-27 three merged site PRs (#22, #23, #25) had never reached the live theme. The landing
pages on it were two PRs behind, and the favicon existed only inside it. There were four causes:

- each upload sent only the files its own PR changed;
- previews were duplicated from whichever theme looked newest;
- the landing-page outputs (`tools/landing-pages/out/`) were never part of an upload check;
- publishing swaps the whole theme, so anything set in MAIN after a copy was taken is lost when
  the copy is published.

So a change never ships as a subset, and code never ships by publishing a theme.

## 2. What the tool guarantees

- **The whole set, every time.** `layout/gt.liquid`, `sections/gt-home.liquid`,
  `assets/gt-site.{css,js}`, `templates/index.json`, every file in `tools/landing-pages/out/`, and
  the images in `theme/assets.manifest.json`. The set is defined once, in `gt_set()`.
- **Nothing else.** Staging fails if its folder holds any other file, and the push always runs
  with `--nodelete`, so no other file in the theme is touched.
- **Admin settings survive.** `config/settings_data.json` holds the favicon and is never in the
  set. Each template's `sections.main.settings` (on the home page: `show_portal_entry`,
  `third_party_pixels`, `analytics_id`) is copied from the target theme when the set is staged.
- **Proof after every push.** It pulls the theme again and compares it with the staged set. Liquid,
  CSS and JS are compared by md5 (the Admin API's `checksumMd5`). Templates are compared as parsed
  JSON, because Shopify writes its own header above them. Images are content-addressed and are
  compared by presence. Anything that differs is printed, and the exit code is 1.

It needs `SHOPIFY_CLI_THEME_TOKEN` (a Theme Access password, set in the environment on
2026-09-27).

## 3. Shipping a change

```sh
cd gt-site                          # on the merged main
./tools/build.sh                    # rebuilds and validates; fails loudly on a moved anchor
python3 tools/verify_figures.py     # must say 0 disagreements
python3 tools/sync_figures.py --check
python3 tools/build_theme.py
git status --porcelain              # must be empty: the committed build is the build

python3 tools/theme_ship.py push 186698334449                  # preview: must end "drift: 0"
# look at the preview; get Tom's word, and quote it
python3 tools/theme_ship.py push 166730072305 --allow-live     # live: must end "drift: 0"
```

`python3 tools/theme_ship.py check <theme_id>` is the same comparison without the push, and it
writes nothing. Run it before a push to see what will change.

**A new preview is needed only if the old one is gone.** Duplicate MAIN, never another theme, and
do it at the moment you need it:
`npx -y @shopify/cli@4.8.2 theme duplicate --store greenteaeveryday.myshopify.com --theme <MAIN id> --name '<name>' --force`.
The tool waits for the copy to finish before it pushes. A push that lands while the copy is still
running is overwritten by the copy job; that happened on 2026-09-27. The store holds at most 20
themes. Deleting one is Tom's call.

## 4. Rollback

Check out the commit that was live before the push, and push its set:

```sh
git checkout <previous main>
python3 tools/theme_ship.py push 166730072305 --allow-live
```

Images are never deleted, so every older page still finds its images. The one thing that does not
roll back is `website_lead_intake`: it is an Edge Function, not part of the theme, and a lead that
has already been submitted should stay submitted.

## 5. The first ten minutes after a live push

In this order, because the later checks matter less if an earlier one fails.

1. **The homepage renders**, on a phone and on a desktop, in a browser without a preview cookie.
   Use a private window. An ordinary window may still hold the cookie and will show the preview
   either way.
2. **The enquiry form lands a lead.** Submit one and check it:
   ```sql
   select id, form_name, created_at from sales_core.lead
    where source = 'website_form' order by created_at desc limit 5;
   ```
   Then confirm the staff alert arrived. If the row is there and the alert is not, the lead is safe:
   `routeIngest` stores the lead before it alerts, and the poll's sweep retries a failed alert.
3. **The store's own routes still work:** a product page, the cart, the account page. They render
   from the theme underneath, so a fault there predates this change, but check anyway, because
   customers use them.
4. **No price on the served page**, while `data/site_flags.json` says `show_prices: false`.
   The visible text must carry no ₪: in the browser, `document.body.innerText` has none. A raw
   `curl | grep '₪'` finds 2, both money-format templates of installed apps (`{{amount}} ₪`, the
   request-a-quote app and the `xo` app), not prices; the count was the same before and after
   the 2026-09-29 push.
5. **Measurement is reporting.** The inventory and the reasoning behind it are in
   `docs/2026-09-02_analytics.md`.

   ```sh
   curl -sS https://gteveryday.com/ | grep -oE 'G-[A-Z0-9]+|GTM-[A-Z0-9]+|gtag/js' | sort | uniq -c
   ```

   - `G-QCNXYQR1TR` comes through the Google & YouTube channel in `content_for_header`, inside the
     web pixel's configuration JSON, where it appears once per configured event (12 times on
     2026-09-29, the same before and after that push). A `gtag/js` loader in the page means
     someone filled in the `analytics_id` field, and every view is being counted twice: there
     must be none.
   - `GTM-TFH9M99` **twice**: the head script and the body `<noscript>`.
   - A confirmed lead pushes one `generate_lead` to `window.dataLayer`. A rejected one pushes
     nothing.

## 6. Open from the first publish

- The About section still has no photographs. That is Tom's to supply (B4 in the first-publish
  record: `git show 4c45338:PUBLISH.md`).

## 7. What is not automated

Choosing to go live is Tom's. The tool pushes only when it is told to, and the CLI refuses the
live theme unless it is given `--allow-live`.
