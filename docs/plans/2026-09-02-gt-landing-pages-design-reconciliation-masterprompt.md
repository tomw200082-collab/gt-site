# MASTERPROMPT — the four GT category landing pages stop being a parallel design system and become the site

**STATUS: LIVE — not yet executed**

> **Usage:** paste this entire file as the first message of a fresh session with the
> `tomw200082-collab/gt-site` repo and the Shopify MCP attached. It takes the four
> Hebrew B2B landing pages from *deployed, correct, and visibly not-quite-the-site* to
> *indistinguishable from the rest of `gt-site.css`, down to the radius on a button*.
> It halts for you only where a human must genuinely act — §6 is that complete list.
>
> **Provenance:** written 2026-09-02, from measurements made that day against the
> Shopify Admin API (`themes`, `theme.files` including bodies, `pages`) and against the
> repo at commit `577117f`. Every byte count and hex value below was read, not recalled.
> Authority, in order: `gt-acquisition-os/CLAUDE.md` ·
> `gt-site/tools/landing-pages/README.md` — cited below, never copied.
>
> **Shelf life:** §2 is presumed wrong if pasted after 2026-09-16. Run §2.5 first.
> If reality no longer matches §2, **halt and surface** — do not adapt silently.

## 0. How to work

- **Who you are here:** one agent session. You hold the `gt-site` repo (write), the
  Shopify Admin API through MCP (theme read + write), and no Canva dependency. You may
  decide anything inside `tools/landing-pages/`. You may **not** publish a page,
  publish a theme, or change a price.
- **Read first, in order:**
  1. `tools/landing-pages/README.md` — the `g-` prefix policy and why it exists
  2. `tools/landing-pages/gen.py` — one generator, four sections
  3. `tools/landing-pages/out/gt-lp.css` — the current landing-page stylesheet
  4. `assets/gt-site.css` — the design system you are matching. **It is not in the
     repo.** Fetch it with the query in §2.5b and keep it on disk for the whole job.
- **Authority:** `gt-acquisition-os/CLAUDE.md` §Absolute non-negotiables and
  §Page quality rule. Where this document and that file disagree, that file wins and
  this document is wrong.
- **Halt conditions, evidence standard, git discipline:** inherited from
  `gt-acquisition-os/CLAUDE.md` §Required workflow and §Completion standard.
  Deltas specific to this work are in §8 only.
- **The standard.** The requester's words: *"in the site's design style with all the
  small details so it is beautiful"* and *"so they are perfect"*. Translated into three
  checkable prohibitions:
  - **No colour on these pages may be a near-miss of a `gt-site.css` token.** Either it
    is the token, or it is a deliberate value with a comment saying why.
  - **No component may re-implement one `gt-site.css` already ships.** Reuse the values;
    do not parallel-build.
  - **No page may regress** — not the drawn glass, not the verified figures, not the
    WhatsApp fallback, not the `g-` collision audit, and not text contrast.
- **Language:** this document is in English because that is the register you reason best
  in. Data literals stay in their own script, in backticks, and are never translated —
  every Hebrew string here is copy that ships to a customer.
  **Output language: concise English.** Short sentences. No preamble, no restating the
  question, no summary of what you are about to do. Customer-facing copy stays Hebrew.

## 1. Mission and definition of done

**One testable sentence:** the four landing-page sections render using `gt-site.css`'s
own tokens, radii, button and card behaviour, so that a reviewer shown a landing page
and a site page side by side cannot name a systematic difference.

Run each command below. **A hit means NOT done** unless the row says otherwise.

```bash
cd tools/landing-pages

# D1 — no hardcoded hex left in gt-lp.css outside the documented allowlist.
#      Allowlist = the drink-swatch tokens kept by W1 (see W1 for the exact list).
grep -oE '#[0-9A-Fa-f]{3,6}' out/gt-lp.css | sort -u   # every line must be on W1's allowlist

# D2 — no page still carries an invented accent.
grep -E 'accent="#(B5731F|3F7A2E|A31F34|6B47BE)"' gen.py            # must find nothing

# D3 — the button is the site's species. POSITIVE proof; empty output means NOT done.
awk '/\.g-btn\{/,/\}/' out/gt-lp.css | grep -E 'border-radius:999px'  # must find a line

# D4 — one container width.
grep -E 'g-wrap\{max-width:1240px' out/gt-lp.css                     # must find a line

# D5 — out/ is regenerated and committed, not hand-edited.
#      Run AFTER committing W5's output. Must exit 0.
python3 gen.py && git diff --exit-code out/

# D7 — the collision audit. See W5 for the script. Must print 0.
```

| # | Condition | Closed by |
|---|---|---|
| D1 | Every colour in `gt-lp.css` is a `gt-site.css` token or on W1's allowlist | W1 |
| D2 | The four accents resolve to the site's per-concentrate tokens | W2 |
| D3 | Buttons are the site's species, not a second one | W3 |
| D4 | `.g-wrap` and `.wrap` share one max-width | W3 |
| D5 | The four sections are regenerated and committed, not hand-edited | W5 |
| D6 | All 14 deployed files match their built bytes — list and method in §2.5 | W5 |
| D7 | The `g-` collision audit returns zero | W5 |
| D8 | All four page records are still unpublished | never violated |
| D9 | Small accent text measures ≥ 4.5:1 on its own background — table in W2 | W2 |
| D10 | The `iced-tea` preview renders correctly at 1440px and 390px — screenshots | W5 |

Anything not on this list is out of scope unless Tom asks.

### 1.1 Settled — do not reopen

- **The `g-` prefix stays.** It was not stylistic caution. `gt-site.css:91` carries an
  unscoped `.glass{position:absolute;…opacity:0}` that pulled every drink's glass out of
  its card grid and collapsed the column to 0px. Reconciling the *values* does not mean
  dropping the *namespace*. Decided in `README.md §Namespacing`.
- **The drawn glass stays.** Each card draws its own glass with bands sized by the
  millilitres in that drink's own recipe (`build_stack.py`). It is the pages' signature
  and it is honest. Do not replace it with a photo.
- **The figures stay.** Transcribed from Canva `DAHTYkRvEnM`, proven equal to
  `drinks_final_figures.json` 2026-08-27: 48/48 names matched, 0 figure deviations,
  margin re-derived from `price/1.18 − cost` with 0/48 mismatches. Do not re-derive
  them and do not type one by hand.
- **Pages stay unpublished.** `gt-acquisition-os/CLAUDE.md` §Absolute non-negotiables:
  never publish a live Shopify page.

## 2. Ground truth — measured 2026-09-02; re-verify at boot

### 2.1 What is built, and the one thing that is out of sync

Theme `gid://shopify/OnlineStoreTheme/162206646513` — `GT Site v5 — Hebrew (do not
publish)`, role `UNPUBLISHED`.

**Deployed surface is 14 files**, not the six the build prints: `assets/gt-lp.css`,
`assets/gt-lp.js`, `sections/gt-lp-{chai,iced-tea,matcha,ube}.liquid`,
`templates/page.{chai,iced-tea,matcha,ube}.json`,
`templates/index.{chai,iced-tea,matcha,ube}.json`.

**One file is stale in the theme and must be deployed first — this is W0.**
Repo commit `577117f` (2026-09-02) regenerated `out/gt-lp-iced-tea.liquid` because
`b35af14` corrected four concentrate names in `drinks.json` without re-running `gen.py`.
The theme still serves the pre-fix section.

| file | theme bytes (2026-09-02) | repo bytes at `577117f` | |
|---|---|---|---|
| `assets/gt-lp.css` | 13,156 | 13,156 | match |
| `assets/gt-lp.js` | 3,410 | 3,410 | match |
| `sections/gt-lp-chai.liquid` | 19,911 | 19,911 | match |
| `sections/gt-lp-matcha.liquid` | 29,432 | 29,432 | match |
| `sections/gt-lp-ube.liquid` | 14,608 | 14,608 | match |
| `sections/gt-lp-iced-tea.liquid` | 24,919 | **24,873** | **stale — W0** |

The four page records exist, all `isPublished: false`, `publishedAt: null`, with
suffixes `ube` · `matcha` · `chai` · `iced-tea`.

`layout/gt.liquid` (2,446 bytes) is chrome-free: Bellefair, Assistant 300–800, Playfair
Display 700/900 + italic 700 from Google Fonts, then `gt-site.css`. It was last written
`2026-09-02T07:51:05Z` — it is **the only theme file touched that day**, and the sole
hand-edit collision risk. The landing-page files were last written `2026-08-31T14:17–14:21Z`.

### 2.2 The numbers — the reorganizing fact

`gt-site.css` declares **20 colour tokens** in `:root`, including a per-concentrate
system. `gt-lp.css` declares **15 of its own** on `.g-lp` and reads none of the site's.
The two palettes are near-misses, not matches. **Three greys diverge; `--paper` matches:**

| token | `gt-site.css` | `gt-lp.css` | |
|---|---|---|---|
| `--paper` | `#FBF8F2` | `#FBF8F2` | same |
| `--ink` | `#20241F` | `#191B14` | **diverges** |
| `--ink-soft` / `--soft` | `#4B5148` | `#57604E` | **diverges** |
| `--line` | `#E7E1D3` | `#E5DECE` | **diverges** |

Every per-page accent in `gen.py` shadows a token the site already owns:

| page | `gen.py` accent | the site's own token |
|---|---|---|
| chai | `#B5731F` | `--nama:#D96B3F` |
| matcha | `#3F7A2E` | `--matcha:#5FA34C` |
| iced tea | `#A31F34` | `--fresh:#E63950` |
| ube | `#6B47BE` | `--ube:#7B5CC6` |

Geometry and component behaviour diverge the same way:

| | `gt-site.css` | `gt-lp.css` |
|---|---|---|
| container | `.wrap{max-width:1240px}` | `.g-wrap{max-width:1200px}` |
| radii in use | 20 distinct values, `2px`→`999px` | two values, `1px` and `2px` |
| button | `.btn` pill `border-radius:999px`, `background:var(--ink)`, uppercase, `letter-spacing:.06em`, hover → `var(--gt-d)`, `.arr` translates `4px` | `.g-btn` `border-radius:2px`, hardcoded `#FBF8F2`, no uppercase, no tracking, hover = `translateY(-2px)` |
| card | `.fcard` `border-radius:26px`, hover `translateY(-8px)` + `box-shadow:0 30px 60px -18px rgba(32,36,31,.22)`, photo `filter:saturate(1.12)` | `.g-drink` `border-radius:0`, hover changes border colour only |
| eyebrow | `.eyebrow` carries a `34px` rule via `:before`, `12px`, `var(--terra)` | `.g-eyebrow` no rule, `11px`, `var(--a)` |
| reveal | `.rv` `translateY(26px)`, `.7s` | `.g-reveal .g-drink` `translateY(14px)`, `.55s` |
| stat block | `.stat` `border-radius:20px`, translucent white on dark | `.g-ledger` square, solid `var(--deep)` |

**The reframe:** these pages are not under-designed. They are a second design system
running beside the real one at roughly ninety percent similarity — which reads worse
than an obvious difference, because the eye registers the mismatch without being able
to name it. The `g-` namespace that correctly protected the pages from `.glass` was
applied as a blanket policy, and the cost is that they re-implement, slightly worse,
what `gt-site.css` already does well.

### 2.3 What is NOT built

- No landing page uses the site's two signature devices: the giant Bellefair watermark
  word (`gt-site.css:134` and `:176`, `clamp(180px,30vw,420px)`, `opacity:.045`) and the
  full-bleed caption band (`.bandcap`, `clamp(46px,7.4vw,138px)` with a gradient scrim).
- The site's display scale runs to `clamp(64px,8.6vw,152px)`. The landing pages stop at
  `clamp(34px,5.2vw,64px)`. They never open at the register the rest of the site does.
- `layout/gt.liquid` sets one `og:title`, one `og:description`, one `og:image` for the
  whole theme, so all four landing pages share the index page's social card.
- No page has `focus-visible` on `.g-btn` or on any link; only `.g-capture input` has
  one. **`gt-site.css` has zero `focus-visible` rules anywhere**, so this is net-new
  work, not adoption.

### 2.4 Known-broken, adjacent, out of scope

- `assets/bss-b2b-js.js` is 948,810 bytes on the main theme. Not on the `gt` layout,
  not yours.
- The `iced-tea` page carries 16 drinks and the largest section (24,873 bytes). It is
  the worst case for any layout change. Test there first; D10 screenshots it.
- `gen.py` writes `__pycache__/`; `577117f` added a `.gitignore` for it.

### 2.5 Re-verification — non-destructive

`gen.py` **writes** `out/`. Never run it as your first act: it overwrites the deployed
baseline before you can diff against it. Build into a copy instead.

```bash
# regenerates §2.1's repo column without touching out/. 2026-09-02 baseline is in §2.1.
cd tools/landing-pages && rm -rf /tmp/lp-verify && cp -r . /tmp/lp-verify \
  && (cd /tmp/lp-verify && python3 gen.py >/dev/null) \
  && diff -rq out /tmp/lp-verify/out && echo "out/ is in sync with drinks.json"
```

```graphql
# theme + page state, all 14 deployed files. Compare against §2.1.
query { theme(id: "gid://shopify/OnlineStoreTheme/162206646513") {
    role updatedAt
    files(first: 20, filenames: [
      "assets/gt-lp.css","assets/gt-lp.js",
      "sections/gt-lp-chai.liquid","sections/gt-lp-iced-tea.liquid",
      "sections/gt-lp-matcha.liquid","sections/gt-lp-ube.liquid",
      "templates/page.chai.json","templates/page.iced-tea.json",
      "templates/page.matcha.json","templates/page.ube.json",
      "templates/index.chai.json","templates/index.iced-tea.json",
      "templates/index.matcha.json","templates/index.ube.json"]) {
      nodes { filename size } } }
  pages(first: 10, query: "chai OR matcha OR ube OR tea") {
    nodes { handle isPublished templateSuffix } } }
```

### 2.5b Fetching the design system

`assets/gt-site.css` is 66,820 bytes and lives only in the theme. This returns its body;
save it to disk before reading, because it will exceed a single tool result.

```graphql
query { theme(id: "gid://shopify/OnlineStoreTheme/162206646513") {
    files(first: 1, filenames: ["assets/gt-site.css"]) {
      nodes { body { ... on OnlineStoreThemeFileBodyText { content } } } } } }
```

## 3. What the hard part actually is

1. **It looks like a styling task. It is a reconciliation task.** Nothing here is ugly.
   Every value is defensible alone. The defect exists only in the relationship between
   two files, so you cannot find it by looking at a landing page — only by diffing it
   against `gt-site.css`.
2. **The namespace is the cause and must survive the cure.** The obvious move is to
   delete `g-` and inherit. That reintroduces the `.glass` collapse. The correct move is
   to keep every selector `g-` prefixed and make the *values* come from the site —
   `var(--ink)` instead of `#191B14`.
3. **"Beautiful" here means less invention, not more.** The pages already have a
   genuinely original signature — the drawn glass. What they lack is the site's
   vocabulary. Adopt the pill button, the card lift, the eyebrow rule, the watermark
   word. Do not design a fifth thing.
4. **Adopting the site's accents costs contrast.** Three of the four site tokens are
   lighter than the values they replace, and two of those currently pass 4.5:1 and stop
   passing. W2 is therefore not a find-and-replace; it needs a second token. This is the
   single place where the site's design system is not simply better.
5. **Four pages, one generator.** If a fix would be applied in four places it belongs in
   `gen.py` or `gt-lp.css`, never in `out/*.liquid`. `README.md`: *"Do not hand-edit
   `out/gt-lp-*.liquid`. Four pages from one template is the point."*

## 4. Workstreams

### W0 — Ship the stale section before changing anything
Deploy the repo's `out/gt-lp-iced-tea.liquid` (24,873 bytes at `577117f`) to the theme,
replacing the 24,919-byte copy. This carries four already-approved Hebrew corrections
into the page: `מנגו סנצ׳ה`→`revive`, `תפוח היביסקוס`→`fresh`,
`consciousness lychee`→`Consciousness`, `fresh apple`→`fresh`. Do this first so that
from here on any byte mismatch genuinely means a hand edit.
**Acceptance:** §2.5's GraphQL shows 24,873 for that file.

### W1 — Adopt the site's tokens
On `.g-lp`, delete `--ink`, `--soft` and `--line` and reference the site's instead:
`var(--ink)`, `var(--ink-soft)`, `var(--line)`. They resolve because `.g-lp` is inside
`<body>`. Keep `--paper` (identical value; keeping it costs nothing and documents intent).
Rename every use of `--soft` to `--ink-soft` so both files use one name for one thing.

**The allowlist D1 checks against** — colours that stay hardcoded because the site has
no equivalent, each needing a one-line comment saying so:
`--white:#fff` · the nine drink swatches `--ice:#D8E8EE` `--water:#C9DFE8`
`--soda:#B4D6E3` `--milk:#F2E8D2` `--foam:#FCF6E9` `--fruit:#E9B47E` `--coffee:#6B4A32`
`--syrup:#E9C965` `--leaf:#8FA870` · and the error pair `#8E2417` / `#F7E7E3`.

**Not on the allowlist, and currently hardcoded — resolve each:** `--rule:#D5CAB2`
(five rules use it; map to `var(--line)` or keep with a comment), `#D9D3C4` ×2,
`#DBD5C7`, `#F1ECE0`, `#9C9585`, `#E7E2D6`. All are greys on dark grounds; map them to
site tokens or to `color-mix()` over `--paper`, and state which you chose.
**Acceptance:** D1.

### W2 — Point the accents at the site's tokens, without losing contrast
Replace each literal `accent=` in `gen.py` `PAGES` with the site's token value:
chai → `#D96B3F`, matcha → `#5FA34C`, iced tea → `#E63950`, ube → `#7B5CC6`.
Derive `tint` and `deep` from the accent rather than inventing a third and fourth colour.

**Measured contrast on white, before and after:**

| page | today | after swap | verdict for small text |
|---|---|---|---|
| chai | `#B5731F` 3.86 | `#D96B3F` 3.43 | fails today, worse after |
| matcha | `#3F7A2E` 5.20 | `#5FA34C` 3.07 | **passes today, fails after** |
| iced tea | `#A31F34` 7.49 | `#E63950` 4.15 | **passes today, fails after** |
| ube | `#6B47BE` 6.42 | `#7B5CC6` 5.01 | passes |

`--a` is one custom property set inline on `.g-lp` and consumed by **14 rules**, so it
cannot be darkened for small text only. Emit a **second** token from `gen.py`,
`--a-text`, being the accent darkened until it measures ≥ 4.5:1 on its own background,
and point these at it: `.g-eyebrow` (11px), `.g-drink summary` (12px),
`.g-fig .g-keep dt` (10px at `.85` opacity — the worst case), `.g-fig .g-keep dd`
(21px on white), and `.g-btn.g-solid` (white label on accent — the primary CTA).
Leave `--a` on the large and non-text uses: `.g-pr-base`, the `.g-need` top border, the
`.g-story li:before` square, `.g-drink:hover` border, the `.g-display em` underline.

Note: `.g-hero-in .g-display em` is **white** (`out/gt-lp.css:45`); the accent is only
its `text-decoration-color`. There is no accent-text-on-dark problem in the hero — do
not go looking for one.
**Acceptance:** D2, D9.

### W3 — One button, one card, one eyebrow, one gutter
Restyle `.g-btn` to the site's species: `border-radius:999px`, `var(--ink)` ground,
`text-transform:uppercase`, `letter-spacing:.06em`, hover to `var(--gt-d)`. Give the
arrow a class and animate it — **`gen.py` emits `<span aria-hidden="true">←</span>` on a
`dir="rtl"` page, so the site's `translateX(4px)` moves it against the direction it
points.** Use a logical translate or `-4px`.
Give `.g-drink` the site's card behaviour: a radius from the site's scale, the
`translateY(-8px)` lift, the `0 30px 60px -18px rgba(32,36,31,.22)` shadow.
Give `.g-eyebrow` the `34px` `:before` rule at `12px`. Set `.g-wrap` to `1240px`.
Match `.g-reveal` to `.rv`'s `26px` / `.7s`.
Every new transform goes **inside** the existing `@media(prefers-reduced-motion:reduce)`
block at `out/gt-lp.css:245-248`, or the page ignores the setting for the new motion only.
**Acceptance:** D3, D4.

### W4 — Reach the site's register
Add the watermark word behind `.g-story` carrying the page's own word — `צ׳אי` ·
`מאצ׳ה` · `תה קר` · `אובה` — at `clamp(180px,30vw,420px)`, `opacity:.045`,
`pointer-events:none`, `aria-hidden="true"`.
**Name it `.g-ghostword`.** `.ghost` exists in `gt-site.css` (scoped to `.tea2` and
`.bigcta`, so it would inherit nothing) and would fail the W5 audit; `.g-ghost` is
already taken at `out/gt-lp.css:54` for the outline-button modifier. Re-declare the
values; do not try to inherit them.
Raise `.g-display` in `.g-hero-in` and `.g-capture` toward the site's
`clamp(44px,5vw,80px)`. Add a `focus-visible` ring on `.g-btn` and `.g-contact a`,
matching the one `.g-capture input` already has.
**Acceptance:** D7 stays zero; no other D-condition regresses.

### W5 — Regenerate, audit, deploy, look
Run `python3 gen.py`. Re-run the collision audit `README.md` requires — every class the
sections emit must be absent from `gt-site.css` as a top-level selector:

```bash
cd tools/landing-pages
grep -ohE 'class="[^"]+"' out/gt-lp-*.liquid | tr ' "' '\n\n' | grep '^g-' | sort -u > /tmp/lp-classes.txt
grep -oE '^\.[a-zA-Z0-9_-]+' /path/to/gt-site.css | sed 's/^\.//' | sort -u > /tmp/site-classes.txt
comm -12 /tmp/lp-classes.txt /tmp/site-classes.txt | tee /tmp/collisions.txt | wc -l   # must be 0
```

Commit `out/`, then run D5 — it must exit **zero**, because the regenerated output is
now the committed output. Deploy all changed files and re-run §2.5 until every deployed
byte count equals its built one. Then open the `iced-tea` preview via the `?view=`
route documented in `README.md §Preview without publishing` and screenshot it at 1440px
and 390px. Byte parity does not prove the render: Shopify serves theme assets from a
versioned CDN path, so reload with cache busting before believing what you see.
**Acceptance:** D5, D6, D7, D10.

## 5. Scope

**IN:** `tools/landing-pages/gen.py`, `out/gt-lp.css`, `out/gt-lp.js`, the regenerated
`out/*.liquid`, and the deploy of those files to theme `162206646513`.

**`layout/gt.liquid` is IN, for one change only.** Per-page `og:` tags cannot come from
a section: `{{ content_for_layout }}` sits inside `<body>`, and meta tags emitted there
are ignored by every crawler. The layout already varies per page — it branches on
`request.page_type` for `<title>` — so add a branch on `template.suffix` for
`og:title` / `og:description` / `og:image`. Change nothing else in that file; it is the
one theme file edited by hand on 2026-09-02.

**OUT — do not touch, do not "improve":**
- `assets/gt-site.css`. It governs the whole site; you are matching it, not editing it.
- `tools/landing-pages/catalog.py` and `drinks.py`. The 48 figures are settled (§1.1).
- `tools/landing-pages/build_stack.py`. The pour classifier is the glass's engine.
- Any page's published state, any theme's role, any product, any price.
- The other twelve themes. `HE-RU Vodoma 2024` is `MAIN` and live.
- `out/index.*.json`. They are the preview route and are working.

## 6. Tom's part — the complete list, nothing else is his

**A. Approve the accent swap (W2).** The four accents become the site's own concentrate
colours, which are lighter — chai from a dark amber to `#D96B3F`, iced tea from wine to
`#E63950`. Show him one before/after of the iced-tea hero, and tell him plainly that
matcha and iced tea currently pass the 4.5:1 small-text threshold and stop passing on
the accent alone, which is why W2 adds a darkened `--a-text`. Two minutes.
**If he does not answer: ship W0, W1, W3, W4, W5 and report D2 and D9 as blocked, not
failed.** Do not swap the accents without his word.

**B. Decide whether the pages go live.** Every page record is `isPublished: false` and
the theme is `UNPUBLISHED`. Publishing is a human act under
`gt-acquisition-os/CLAUDE.md` §Absolute non-negotiables. Do not ask for it as part of
this work.

**C. Supply four social images (W4/§5)** if he wants four distinct cards rather than
four pages sharing the index card. One landscape image per page. If he does not supply
them, ship the `og:` branch pointing at the existing shared image and say so.

## 7. Landmines — do not rediscover these

1. **You delete the `g-` prefix to inherit the site's styles, and every drink card loses
   its glass.** `gt-site.css:91` carries an unscoped `.glass{position:absolute;…
   opacity:0}`. It pulls the glass out of the card's grid column, which collapses to
   0px. Everything else still looks fine, so the diagnosis lands on the glass markup
   rather than on a selector in another file → keep every selector `g-` prefixed and
   change only the *values*.
2. **You run `python3 gen.py` to check whether `out/` is current, and destroy the
   baseline you were checking.** `gen.py` writes in place → use §2.5, which builds into
   a copy.
3. **You hand-edit `out/gt-lp-chai.liquid` because the fix is three lines.** The next
   `gen.py` erases it and the four pages silently diverge → every change goes in
   `gen.py` or `gt-lp.css`.
4. **You grep a multi-line CSS rule and conclude the work is done.** `gt-lp.css` writes
   `.g-lp .g-btn{` and `border-radius:2px` on different lines, so a single-line `grep`
   for both together matches nothing whether or not the change was made → the D-block
   in §1 uses `awk` range matching for exactly this reason. Do not rewrite those
   commands into one-line greps.
5. **You swap the accents and `נשאר אצלכם` becomes unreadable.** `.g-fig .g-keep dt` is
   the accent at 10px and `.85` opacity — the worst instance, and not the one people
   check → measure on that element, per the W2 table.
6. **Deployed bytes match but the page still looks old.** Shopify serves theme assets
   from a versioned CDN path; a correct `gt-lp.css` can sit behind a cached copy →
   verify in the theme preview with a cache-busting reload. D10 exists because of this.
7. **You add `.ghost` and the collision audit fails.** It is already in `gt-site.css`;
   `.g-ghost` is already the outline-button modifier → `.g-ghostword`, per W4.
8. **You add the card lift and the page ignores `prefers-reduced-motion`.** The
   stylesheet ends with a reduce block covering only the two existing transforms →
   `out/gt-lp.css:245-248`, add yours.
9. **You emit `og:` tags from the section and they never appear.** They land inside
   `<body>` → §5, the layout branch.

## 8. Halt conditions

Inherited set cited in §0. Additions specific to this work:

- After W0, any deployed byte count in §2.5 differs from the freshly built one →
  **STOP**. Someone edited the theme by hand. Surface the diff; do not overwrite.
  Before W0, exactly one mismatch is expected: `gt-lp-iced-tea.liquid` (§2.1).
- A `gt-site.css` token would have to change to make a landing page work → **STOP**.
  That inverts the dependency and is not this work.
- `/tmp/collisions.txt` is non-empty → **STOP**, rename the landing-page class, re-run.
  Do not ship the collision.
- A darkened `--a-text` cannot reach 4.5:1 without ceasing to read as the brand colour →
  **STOP** and put it to Tom. Do not ship failing contrast and do not silently keep the
  old accent.
- Any action would set a page's `isPublished` to `true` or change a theme's role →
  **STOP**. That is §6.B.

## 9. Final report

1. What a stranger can now watch working, end to end
2. Each of D1–D10 ✅ / ❌ / blocked, with the command or screenshot that proves it —
   no partial credit
3. The numbers: deployed bytes against built bytes for all 14 files; the contrast ratio
   measured for each of the five small-text instances in W2; the collision count
4. The artifacts, and where they are
5. What is still Tom's (§6), and what remains genuinely unfinished
6. The single next action

If anything is not ready, say so first and plainly. Then set this file's **STATUS** line
to `SHIPPED` with evidence pointers, or `ABANDONED — why`.
