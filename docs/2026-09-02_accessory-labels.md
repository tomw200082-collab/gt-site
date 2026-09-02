# Two bar-tool cards carried each other's name — 2026-09-02

Tom, from a render of the tools grid:

> יש טעות ה600 מל זה מה שמימין למעלה ומה שכתוב כוס זכוכוית 600 מל זה אמור להיות
> הכוס מדידה (ג'יגר).

He is right, and the store proves it. Two of the eight cards in `#tools` had the
wrong caption under the photograph:

| photograph | said | is | price said | price of record |
|---|---|---|---:|---:|
| graduated glass beaker | `מכל מדידה` / Measuring glass | `Matcha 600ml glass pot`, SKU `AP-CUP-MAT-600` | ₪20 | **₪30** |
| printed jigger | `כוס זכוכית 600 מ״ל` / Printed glass 600 ml | `Measuring Cup`, SKU `GT-GLA-CUP` | ₪30 | **₪20** |

Source: the Shopify admin catalogue, read 2026-09-02 — both products ACTIVE.
The 600 ml pot's own description is `כלי זכוכית בנפח 600 מ״ל להכנה מדויקת של
מאצ'ה`, and its product photograph is a lab beaker (`…potiri-zeseos-glass-600ml`,
Greek *potíri zéseos*, "beaker"). Authority grade: `system_verified`.

## What that means for the numbers

Nothing moved that was not already wrong. Each caption's **name and price were a
matching pair** — ₪20 with the measuring cup, ₪30 with the 600 ml pot — but the
pair sat under the other product's photograph. So the fix is a swap of the two
captions, not a repricing: the two prices on the page are the same two prices,
now over the right pictures.

The wholesale price list further down the same page was **already correct**
(`קנקן זכוכית · 600 מ״ל ₪30`, `כוס מדידה ₪20`) and is untouched. The card names
were made identical to those rows rather than inventing new ones. Tom's "(ג׳יגר)"
was how he identified the item for me; it is not the name in the record, so it is
not on the page.

## Two sentences of prose followed the name

`מכל מדידה` was not only a card. The tools band and two recipe/FAQ steps pointed
readers at "מכל המדידה שלנו" — a name that, after this correction, no product on
the page carries. All three now say `כוס המדידה`, which is also the right tool for
the job they describe (50 ml of concentrate is a jigger pour, not a 600 ml pot).
The English source says "our measure" / "our measuring tool" and needed no change.

## Where it was fixed

At the source, not in a patch: `src/index.en.html` (English copy, alt text and the
two prices) and `i18n/parts/he_visible_2.py` / `he_visible_3.py` (Hebrew). Seven
catalogue strings changed and the string-id count is unchanged at 1178, so no
translation shifted onto the wrong span. `src/index.html` and
`theme/sections/gt-home.liquid` are regenerated from those.

## Checks

- `./tools/build.sh` — clean, every patch anchor still found.
- `python3 tools/verify_figures.py` — 0 disagreements (this grid is not one of the
  five generated figure surfaces; the drink figures are unaffected).
- `python3 tools/sync_figures.py --check` — vendored record still matches.
- Rendered at 1280 / 760 / 390 px: no text overflow, and card heights are
  byte-for-byte the same pattern as before, so the longer Hebrew label
  `קנקן זכוכית 600 מ״ל` costs the grid nothing.
