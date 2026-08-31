# gt-site

The GT Everyday brand site (`v5 R124`), built in Hebrew.

The source of the design is a single self-contained page — 13 sections, ten
drink collections, 48 costed drink recipes, a wholesale price list — authored
in English. This repo turns that page into the Hebrew site without forking it:
`src/index.en.html` stays byte-for-byte as delivered, and every Hebrew build is
regenerated from it plus a translation catalogue.

```
src/index.en.html     the delivered design — never edited
src/index.html        the built Hebrew page  (generated, committed)
i18n/strings.en.json  1,178 extracted strings, each with its exact span
i18n/strings.he.json  the same strings with Hebrew
i18n/parts/           the Hebrew copy, hand-written, grouped by area
tools/                extract → catalogue → apply → patch → validate
```

## Build

```sh
./tools/build.sh
```

Runs five steps and a validator. It is safe to run repeatedly — the English
source is only ever read.

| step | what it does |
|---|---|
| `extract_strings.py` | walks the English page and records every human-readable string with the exact character span it occupies |
| `build_catalogue.py` | merges `i18n/parts/*.py` onto those records; anything machine-facing is left in English on purpose |
| `apply_translation.py` | writes the Hebrew back by span, right to left |
| `patch_hebrew_build.py` | the code changes Hebrew needs (below) |
| `patch_rtl_shell.py` | RTL corrections, mobile navigation, document semantics |
| `validate.js` | parses every inline script, checks attribute quoting and tag balance |

Every patch asserts its anchor exists and the build fails loudly if one moved,
so a silent no-op is not possible. `apply_translation.py --identity` re-inserts
the English text and reproduces `src/index.en.html` byte-for-byte.

## Why translating the copy alone was not enough

Two renderers in this page read the copy itself rather than a data field.

**`STEP_ICONS` → the step strip in the drink modal.** It picks an icon by
regex-matching the recipe step text, in English (`/ice/i`, `/milk/i`). Hebrew
steps match nothing, so the strip would have degraded to bullets. The patterns
now carry Hebrew alongside English: **221/221 steps resolve** (the English
build resolved 214/221 — pistachio, black sesame and coconut cream never
matched there either).

**`glassSVG` / `LAYER_MAP` → a layered-glass illustration.** It matches Hebrew
ingredient words. It is **dead code** — defined once, never called — so it
renders nothing in either language. The Hebrew ingredient strings are worded to
match its patterns anyway, so it works the day it is wired up.

The drink names needed no translation at all: all 48 drinks in `COLS` already
carried a `he` name, and the English build wrote `''` into the element meant to
show it. The Hebrew name is now the headline and the English name is the Latin
kicker, the same pairing the collection cards use.

## What the Hebrew build changes beyond copy

- `lang="he" dir="rtl"`, and a `<head>` that had no description, canonical or
  social tags.
- Transform-driven tracks (hero slider, ticker) are pinned LTR so their
  translate maths still lands; their content goes back to RTL.
- Chrome that was pinned to the physical left — close buttons, the FAQ marker,
  the flavour dropdown, prev/next — moves to the reader's side, chevrons
  included.
- A mobile menu. Under 980px the old page hid `.nav-links` and put nothing in
  its place, so every phone had no navigation at all.
- One `<h1>` for the document; the ten slide headings become `<h2>`.

## Where it runs

The Hebrew page is live as an **unpublished** Shopify theme on
`greenteaeveryday.myshopify.com`. Nothing is published — `HE-RU Vodoma 2024`
is still the live theme.

| | |
|---|---|
| Theme | `GT Site v5 — Hebrew (do not publish)` · id `162206646513` |
| Preview | `https://gteveryday.com/?preview_theme_id=162206646513` |
| Old homepage | kept as `templates/index.vodoma.json` → `?view=vodoma` |

Open the full preview URL in a browser: Shopify sets a cookie and redirects, so
a client that drops cookies gets the live theme back instead. The preview then
sticks to that browser until it is closed — seeing the new site at a bare
`gteveryday.com` does **not** mean it was published.

The theme is a duplicate of the live one, so product, collection, cart and
account routes all still render from Vodoma underneath; only the homepage is
ours.

### Deploying a change

```sh
./tools/build.sh        # regenerate src/index.html
python3 tools/build_theme.py   # regenerate theme/
git commit && git push
```

then `themeFilesUpsert` the changed files, pointing `body.type: URL` at the
raw.githubusercontent.com URLs for the pushed commit — Shopify fetches them
itself. `theme/assets.manifest.json` maps each image asset to the URL it was
fetched from.

Details and the traps worth knowing:
`gt-factory-os-production-brain/.claude/skills/shopify-theme/SKILL.md`.
