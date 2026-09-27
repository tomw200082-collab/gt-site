# Site gate brief — the GT brand site (read first, every UX agent)

This brief re-aims an agent definition written for the operations portal at the brand site. Where
the brief and your definition disagree, the brief wins. It is permanent: the 2026-09-25 gate wrote
most of it by hand for one run (`gt-factory-os/docs/superpowers/plans/2026-09-25-customer-portal-ux-gate/BRIEF.md`,
and its `prompts/IPAD-S.md` for this site); this file is that work kept, so the next gate starts here
instead of from nothing. `/site-gate` in the brain drives it.

## 1. What is under audit

The Shopify storefront at `gteveryday.com` (store `greenteaeveryday.myshopify.com`): Hebrew, RTL,
generated from this repo and uploaded as a theme. `PUBLISH.md` names the live theme and the staged
copy; a gate against the staged copy runs the harness with `SITE_URL=https://gteveryday.com/?preview_theme_id=<id>`.

| Surface | Where a visitor finds it | What is there |
|---|---|---|
| Home `/` | the whole page | nav (`.nav-links`, the products dropdown `.nav-dd`, the burger `.nav-burger` on narrow widths, the business entry `.portal-pill`), hero carousel `#hs` (10 collection slides), logo ticker, `#products` with the product modal `#pmodal` and the flavour cards `.fcard` → `#fmodal`, `#drinks` collection cards `.ccard` → the recipe card `#cmodal` (48 drinks, 10 collections, prev/next, drink chips, deep links `#recipe-<c>-<d>`), the "one bottle, many cups" matrix `#mxtog` → `#mxbox`, `#partners`, `#pricing` (only when prices are on), `#about`, `#faq` (`<details>`), `#contact` with the enquiry form `#pform`, footer |
| Category landing pages | `?view=chai`, `?view=matcha`, `?view=iced-tea`, `?view=ube` | one category each: hero, drink menu `.g-lp .g-drink` with "איך מכינים" `<details>`; reached from Instagram and ads; their `/pages/<slug>` records are unpublished |
| The business entry | nav + burger menu + phone header icon | `כניסה לעסקים` (`כניסת לקוחות` on the theme live before #25) → the customer ordering portal. Behind the theme switch `show_portal_entry` |
| The enquiry form | `#contact` | `#pform` → Edge Function `website_lead_intake` → `sales_core.lead` (`source='website_form'`) → alert email to the lead queue; a confirmed send pushes `generate_lead` to `dataLayer` |
| Store-native routes | product, collection, cart, account | rendered by the Vodoma theme layer underneath ours. Out of scope, except "still works" (`PUBLISH.md` §5.3) |

**Source, and the only vocabulary a fix may use.** The site is generated (`README.md`):

- `src/index.en.html` — the delivered English design, never edited.
- `src/index.html` — the committed Hebrew build = `./tools/build.sh`: extract → catalogue → apply
  the Hebrew (`i18n/parts/*.py`, `i18n/strings.he.json`) → the passes `patch_hebrew_build`,
  `patch_rtl_shell`, `patch_figures`, `patch_claims`, `patch_form`, `patch_a11y`, `patch_ux`,
  `patch_launch`, `patch_ipad` → `validate.js`. Every pass asserts its anchors; a moved anchor fails
  the build.
- `theme/` — `python3 tools/build_theme.py` writes `sections/gt-home.liquid`, `assets/gt-site.css`,
  `assets/gt-site.js`, `templates/index.json`; it strips every price when `data/site_flags.json`
  `show_prices` is false (`tools/strip_prices.py`). `theme/layout/gt.liquid` is hand-maintained.
- Landing pages — `tools/landing-pages/gen.py` writes `out/gt-lp-<slug>.liquid`; `out/gt-lp.css`
  and `out/gt-lp.js` are hand-written.
- Figures of record — `data/drinks_final_figures.json` (+ `.provenance.json`);
  `tools/verify_figures.py` must report 0 disagreements.

A proposed fix therefore names one of: a `sub()` in an existing `tools/patch_*.py` or a new pass
wired into `build.sh`; a change in `build_theme.py`; `gt-lp.css` / `gt-lp.js` / `gen.py`;
`theme/layout/gt.liquid`; Hebrew copy in `i18n/parts/` (`copy: needs Tom`). Never "edit
`src/index.html`" or "edit `theme/...`": CI (`.github/workflows/build.yml`) rejects a hand edit to
either. CI also guards: every figure against the record; no price on a served page while prices
are off; no placeholder copy; the Liquid section under 256 KB; no remote image host in the theme;
nothing hidden by a large negative offset (RTL widens the page instead); `og:image` + JSON-LD
(exactly one `Organization`, an `FAQPage`); GTM twice, no hard-coded GA4, `generate_lead` present,
no HubSpot; the landing-page card colour reset. A finding CI already blocks is not a finding.

## 2. Who reads the page, and the bar

From `docs/2026-09-03_benchmark.md` (twenty sites read; the ICP cards in Sales-Machine `knowledge/`):

| | The decider — owner / manager | The influencer — bar manager / barista |
|---|---|---|
| Cares about | profit, risk, headache | taste, prep time, variety |
| Does not care about | tea varieties, leaf origin, brand story | — |
| What closes | ₪ per cup vs. ₪ on the menu · no machine · no fridge space · no big stock | recipes · variety · ten-second prep · training |
| Can they say yes? | signs | cannot sign, can kill it |

Four venues, four entry products: café — one tea concentrate; restaurant — the caffeine-free four;
bar — chai; specialty coffee — matcha (never lead with the tin price). Hotels, catering and offices
are named targets with no script: the page must not pretend to know them.

- **The job of the page** is an enquiry or a first order, not a meeting. The real objection is
  inertia, not price. Tom, 2026-09-03: *the hero has to make a stranger understand what GT does in
  one moment*, and *"we are more than a supplier — we help the customer sell it"*.
- **How they arrive:** a phone, often from Instagram, WhatsApp or an ad, between tasks; an office
  desktop for the chain buyer; an iPad on the bar for the recipes. Hebrew, RTL, one-handed, weak
  connections, the cheapest Android in the kitchen.
- **The bar:** the best B2B beverage brand sites, and the best consumer brand sites in feel — hero
  clarity, one conversion path, craft on phone first. Refine within the brand that exists (warm
  paper, ink, GT green, Heebo, the flavour colours and the bottle photography, `GT Latin` for the
  English drink names) unless a finding shows it fails a visitor. Propose system rules, not one-off
  decoration.

## 3. Rules from your definition that do NOT apply here

Say so in one line in your report, then move on.

- `gt-factory-os-portal/docs/portal_ux_standard.md` and `portal_language_direction_audit.md` govern
  the operations portal. Not this site.
- "English-first", "Hebrew copy is P0", "RTL is forbidden" are reversed. The site is Hebrew RTL by
  design (`<html lang="he" dir="rtl">`; README, 2026-08-31). English is data: drink names, "Don't
  Drink Boring." (settled, §5), partner logos.
- The Operational Precision tokens, shadcn/Tailwind conventions, `RUNTIME_READY`, the ops harness
  `tests/e2e/ux-shot.spec.ts` with dev-shim auth, the ops status lexicon and button lexicon, the
  YAML handoff packet. The design system here is the CSS custom properties at the top of
  `theme/assets/gt-site.css`; the evidence is §6; the output is §9.
- `DECISION_GRADE` / `FLOW_COMPLETION` / `POLISH_ACCELERATION` map onto P0 / P1 / P2 (§8).
- The persona is not a factory operator. "Operator" reads as **visitor**: the decider, the
  influencer, the chain buyer, the barista. `operator-task-simulation` reads as the visitor tasks in §7.

## 4. Constraints on proposals

- **Generator terms only** (§1). Every fix names the file that generates the output and how to
  verify it: which shot or fact changes.
- **Money truth.** Every figure on the page comes from the record. A finding may say two figures
  disagree, or a figure is missing where the argument needs it; the fix is "which one the record
  says", never a new number. While `show_prices` is false, any ₪ figure on a served page is a P0.
  Margin percentages are allowed either way (Tom, 2026-09-24).
- **Copy.** Customer-visible Hebrew changes need Tom's approval: quote the current string, give the
  exact new one, mark `copy: needs Tom`. The English source and `i18n/strings.en.json` never change.
- **Switches are Tom's:** `show_prices` (`data/site_flags.json`), `show_pricing` and
  `show_portal_entry` (theme editor). Report their state; do not propose flipping them.
- **The theme is the whole storefront** (brain skill `shopify-theme`). Never propose removing or
  overriding Vodoma-layer files, and never propose uploading or publishing: `PUBLISH.md` §7,
  publishing is Tom's alone. Liquid limits: a section under 256 KB, 25 sections per JSON template.
- **Analytics and the lead pipeline are load-bearing:** GTM twice, no second GA4, the Taboola and
  Retention Rocket pixels, `generate_lead` on a confirmed send. A change that touches the layout head
  or the form must say what happens to each.
- **No new dependency and no new build step** without a strong reason; the page is one section plus
  one stylesheet and one script on purpose.
- **`ARCH_REQUIRED`** = needs a Shopify app, a backend or Edge Function change, or a Shopify
  behaviour we do not control (checkout, the account pages). Name the endpoint or data it needs;
  it never blocks the verdict on its own.

## 5. Settled — do not re-open

Tom's decisions and design calls already made. Re-raise one only if new evidence changes the
picture, marked `(settled — Tom)` and outside the ranked table.

| Item | State |
|---|---|
| `20–30% פחות אלכוהול מאשר לפני עשור` | stays as written — `user_confirmed` (B1, 2026-08-31) |
| `Don't Drink Boring.` in English in the footer | deliberate (B5) |
| The wholesale price list and every ₪ figure hidden on served pages | `show_prices=false` since 2026-09-24; margins stay |
| No photographs in About | Tom's to supply (B4); report only if the empty space breaks the layout |
| Four names for one destination (`רוצים להתחיל`, `רוצה מחירון`, `בקשת שיתוף פעולה`, `בואו נדבר`) | brand voice, Tom's call (2026-09-03). A CRO finding may quantify the cost once; it is not a P0 |
| The hero is a collection carousel; the H1 is screen-reader only | a design decision (2026-09-03). §7 T1 still asks whether the first screen explains GT |
| Placeholders are the only labels on the form | left (2026-09-03); an A11Y row may state the risk once, effort M |
| Footer social links | real URLs in place since 2026-09; not text any more |
| Hebrew RTL everywhere customer-facing | Tom-approved (2026-08-31; 2026-09-25 for the ordering portal) |
| The iPad recipe-card work (IPAD-S-01…21) | shipped in #21/#22; verify it holds, do not re-derive it |

## 6. Evidence

Regenerated every run, never stored in a repo. Both scripts are read-only against the site and
create no lead: the harness intercepts the form's POST to `website_lead_intake` and answers it
itself, so the "error" and "sent" shots cost nothing.

```
UX_OUT=<scratchpad> node gt-site/tools/site_shots.mjs                       # phone + desktop, this file
UX_OUT=<scratchpad> node gt-factory-os/api/scripts/site_ipad_shots.mjs      # iPad, five widths
```

`$UX_OUT/site/shots/<vp>-<nn>-<state>.png` — `<vp>` is `p360` (360×780) and `p390` (390×844), a
cheap Android with touch, @2x; `d1366` (1366×768) a laptop; `d1920` (1920×1080) an office screen.
iPad shots are under `$UX_OUT/site-ipad/` (`i744`, `i820`, `i1024`, `li1180`, `li1366`).

| # | Home |
|---|---|
| 01 | first screen |
| 02 | full page |
| 03 | nav open (burger) on phones; products dropdown hovered on desktops |
| 04 | `#drinks` |
| 05 / 06 | recipe card open; after "הבא" |
| 07 | the matrix open |
| 08 | `#pricing` — only when the price list is on |
| 09 | FAQ, first answer open |
| 10 / 11 / 12 | the form; after a rejected send (`bad_phone`); after a confirmed send |
| 13 | footer |
| 20 | keyboard focus after ten Tabs from the top |
| `lp-<slug>-01/02/03` | landing page top; first recipe open; full page (p390 and d1366) |

`$UX_OUT/site/facts.json`, per viewport: `first` (the H1 and whether it is visible, the text
actually visible on the first screen, how the nav presents and where the business entry points),
`probe` (horizontal overflow, elements sticking out), `smallTargets` (phones: interactive elements
under 44 px), `sections` (p390: the visible text of every section, for copy), `media` (images,
images without width/height, lazy, broken, fonts and their status), `axe.home / recipe / form`
(p390, d1366: axe-core WCAG 2.2 AA + best-practice violations), `navOpen` / `ddMenuVisible`,
`recipe` + `recipeAfterNext` + `recipeEscapeCloses` (card geometry: does it fit, is the header in
view, is the page locked behind it), `matrixProbe`, `pricing` and `shekelOnPage`, `formEmptySubmit`
/ `formError` / `formSent` (with `generateLead`), `tabOrder` (`NO-RING` marks a stop without a
visible focus ring), `reducedMotion` (p390: did the hero advance, is the ticker animating),
`lp-<slug>` (first screen, overflow, cards still hidden after scrolling, other cards resized by
opening one, small targets), `errors` (page errors, including the store's installed apps).
`perf` (p390, cold cache, slow 4G, CPU ×4, against the real CDN): FCP, LCP and its element, CLS
with sources, KB by type, the eight biggest resources, fonts loaded; `perfBudget` against the
"good" thresholds (LCP ≤ 2500 ms, CLS ≤ 0.1). The iPad facts are `site-ipad/site_ipad_facts.json`.

Rules: a **visual or layout** finding cites a shot path. A **structural, copy, semantic or
performance** finding cites the generator `file:line` (or the fact) and the rendered string. Open
the images — Read renders PNG. Chromium only: Safari-only behaviour (toolbar `vh`, `backdrop-filter`
cost, scroll chaining) is reasoned from the CSS and marked *inferred*; Linux has no Apple fonts, so
rasterisation is never a finding.

## 7. Visitor tasks — the spine of every review

| Task | The visitor and what they do |
|---|---|
| T1 | A stranger on a phone, five seconds: from the first screen alone, understands what GT sells, for whom, and that GT helps them sell it. Decider lens. |
| T2 | A café owner on a phone: from any screen reaches the enquiry form, fills it one-handed, sends, knows it arrived and what happens next. The CTA is never more than one tap away. |
| T3 | A barista on an iPad or phone: finds one drink's recipe, reads it whole, moves to the next drink, closes the card, shares one drink (deep link). |
| T4 | A chain buyer: finds `כניסה לעסקים` on a phone and on a desktop; the hand-off to the ordering portal is clear. |
| T5 | From an Instagram ad to `?view=matcha`: understands the category offer, sees the drinks, reaches the form or WhatsApp. |
| T6 | The decider checks the money: the margin argument is consistent across hero, recipe cards and matrix; nothing contradicts the record; no ₪ figure appears while prices are off. |
| T7 | A weak network on the cheapest Android: the first screen paints fast, nothing jumps, the hero image is the LCP, fonts do not flash, the page is still readable before the scripts arrive. |
| T8 | A screen-reader or keyboard user in Hebrew: the nav, the recipe card, the FAQ and the form, end to end. |
| T9 | Desktop 1366 and 1920: the page holds at wide widths (measure, line length, hover craft, the dropdown), and the burger appears only where it should. |

## 8. Severity and effort

| Severity | Meaning on a brand site |
|---|---|
| **P0** | A figure or claim wrong or contradicting the record; a ₪ figure on a served page while prices are off; the enquiry form fails to produce a lead, loses the lead silently or claims success falsely; a primary surface unreadable or broken at a common width (360, 390, iPad, 1366); a tracking regression (GTM or `generate_lead` missing, GA4 doubled); a keyboard or screen-reader blocker on T2 or T3. |
| **P1** | Significant friction, confusion or a trust gap on a primary path (hero, form, recipes, the business entry, a landing page), or clearly below the bar in §2 on a primary surface. |
| **P2** | Polish, delight, refinement. |

| Effort | Meaning |
|---|---|
| **S** | Under an hour: CSS, one `sub()`, copy. |
| **M** | A few hours, or a new patch pass. |
| **L** | A day or more, a design decision, or `ARCH_REQUIRED`. |

Markers: `(settled — Tom)` per §5 · `(parked)` outside this gate's scope · `copy: needs Tom` ·
`ARCH_REQUIRED` with what it needs. Owner of a shared cause: the dimension that owns the rule
(accessibility → A11Y, structure → FLOW/INTER, pixels → VIS, words → COPY/BRAND, conversion and
speed → CRO); mention the secondary effect in the finding, report it once.

## 9. Output, in this exact shape (markdown, returned as your final message)

```
## <agent or dimension> — GT brand site

### Not applicable from my definition
<one line>

### Findings
| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator terms: file, anchor, CSS/JS, or the Hebrew with the current string) | Evidence |
|---|---|---|---|---|---|---|
| <DIM>-01 | P0 | S | ... | ... | ... | shot:`...png` or `tools/patch_ux.py:NNN` or fact:`p390.formSent` |

### World-class upgrades (beyond defects — what would make this the best site in its category)
1. ...

### Visitor task results
| Task | Result (PASS / FRICTION / FAIL) | Where it breaks |
|---|---|---|

### Settled items seen (not ranked)
<none, or the §5 line and the new evidence>

### Scorecard
| P0 | P1 | P2 | Status (GREEN ≤2 P1, no P0 / AMBER / RED any P0) |
```

Dimensions and prefixes: FLOW (ux-flow-architect) · INTER (interaction-design-specialist) · VIS
(visual-system-designer) · COPY (ux-content-state-designer) · A11Y (accessibility-usability-auditor)
· CRO (conversion and performance: skills `page-cro`, `landing-page`; `facts.perf` is yours) ·
BRAND (voice, promise, persuasion: skills `ogilvy`, `copywriting`; Hebrew is `copy: needs Tom`).

Be exhaustive and specific: name the pixel, the line and the string. One precise finding beats a
vague theme. Do not pad: if something is excellent, say so in one line and move on. Do not edit
any file. This is read-only; your report is the deliverable.

---
Written 2026-09-27 from the 2026-09-25 gate brief, `docs/2026-09-03_benchmark.md`,
`docs/2026-09-03_ux-review.md`, `PUBLISH.md` and the brain skill `shopify-theme`. When a Tom
decision changes a row in §5, change the row here in the same PR.
