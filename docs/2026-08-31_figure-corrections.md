# Drink figures corrected to the record — 2026-08-31

The site was built from `docs/pricing/2026-08-05_drinks_final_figures.json`.
The figures of record are `.claude/skills/drinks-pricelist/drinks_final_figures.json`
(`2026-08-27`, sha256 `5d38f621eda8e1d0`), named as such by
`docs/pricing/2026-08-27_COST_MODEL.md:78`. Every figure on the page now comes from it.

**277 values rewritten** across five surfaces: 48 drinks x 4 fields, 10 collection
headline prices, 23 flavour-card rows x 3 fields, 10 static collection cards, and
16 labels in the scrolling ticker under the hero.

The ticker was the fifth surface and the last one found — not by reading the
source, but by looking at a render and noticing the strip still said ₪19 while
the hero chip directly above it said ₪20. `tools/verify_figures.py` now checks
all five.

**36 of 48 recommended prices moved — every one of them upward.** The superseded
set was recommending less than GT prices at.

| drink | was | now | Δ | margin | food cost |
|---|---:|---:|---:|---|---|
| מאצ'ה קוקוס תות | ₪28 | **₪44** | +16 | 70% → 84% | ₪7.06 → ₪5.79 |
| מאצ'ה קוקוס מנגו | ₪28 | **₪44** | +16 | 70% → 84% | ₪7.06 → ₪5.79 |
| מאצ'ה קוקוס אפרסק | ₪28 | **₪44** | +16 | 70% → 84% | ₪7.06 → ₪5.79 |
| אייס מאצ'ה מנגו | ₪26 | **₪39** | +13 | 72% → 80% | ₪6.17 → ₪6.46 |
| אייס מאצ'ה תות | ₪26 | **₪39** | +13 | 72% → 80% | ₪6.17 → ₪6.46 |
| אייס מאצ'ה אפרסק | ₪26 | **₪39** | +13 | 72% → 80% | ₪6.17 → ₪6.46 |
| גזוז מדברי ואפרסק | ₪22 | **₪33** | +11 | 69% → 83% | ₪5.79 → ₪4.80 |
| אייס מאצ'ה מסאלה | ₪26 | **₪37** | +11 | 71% → 78% | ₪6.37 → ₪6.86 |
| דירטי צ'אי | ₪24 | **₪32** | +8 | 72% → 76% | ₪5.65 → ₪6.57 |
| חליטת אפרסק מדברית | ₪24 | **₪31** | +7 | 73% → 82% | ₪5.41 → ₪4.80 |
| חליטת תות לואיזה | ₪24 | **₪31** | +7 | 73% → 82% | ₪5.41 → ₪4.80 |
| חליטת מנגו סנצ'ה | ₪24 | **₪31** | +7 | 73% → 82% | ₪5.41 → ₪4.80 |
| מאצ'ה קוקוס אגבה | ₪28 | **₪34** | +6 | 78% → 86% | ₪5.33 → ₪4.04 |
| מאצ'ה קוקוס ליצ'י | ₪28 | **₪32** | +4 | 78% → 85% | ₪5.14 → ₪4.07 |
| אייס צ'אי מסאלה קלאסי | ₪24 | **₪28** | +4 | 75% → 77% | ₪5.00 → ₪5.57 |
| צ'אי מסאלה ומיץ תפוזים | ₪24 | **₪28** | +4 | 75% → 78% | ₪5.11 → ₪5.25 |
| צ'אי תאילנדי קוקוס קולד פואם | ₪28 | **₪32** | +4 | 76% → 82% | ₪5.79 → ₪4.90 |
| לימונדת היביסקוס וליים | ₪19 | **₪22** | +3 | 74% → 79% | ₪4.19 → ₪3.95 |
| לימונדה מדברית | ₪19 | **₪22** | +3 | 74% → 79% | ₪4.19 → ₪3.95 |
| לימונדת צ'אי מסאלה | ₪19 | **₪22** | +3 | 74% → 79% | ₪4.19 → ₪3.95 |
| גזוז יסמין וליצ'י | ₪22 | **₪25** | +3 | 76% → 85% | ₪4.52 → ₪3.08 |
| צ'אי מסאלה קולד פואם בננה | ₪28 | **₪31** | +3 | 77% → 84% | ₪5.50 → ₪4.20 |
| אייס אובה מסאלה | ₪28 | **₪31** | +3 | 76% → 76% | ₪5.58 → ₪6.27 |
| צ'אי מסאלה תפוז וטוניק | ₪24 | **₪26** | +2 | 77% → 78% | ₪4.76 → ₪4.75 |
| צ'אי מסאלה קולד פואם פיסטוק | ₪28 | **₪30** | +2 | 77% → 81% | ₪5.45 → ₪4.90 |
| אייס אובה תות | ₪28 | **₪30** | +2 | 80% → 79% | ₪4.73 → ₪5.22 |
| אייס אובה מנגו | ₪28 | **₪30** | +2 | 80% → 79% | ₪4.73 → ₪5.22 |
| אייס אובה אפרסק | ₪28 | **₪30** | +2 | 80% → 79% | ₪4.73 → ₪5.22 |
| חליטת היביסקוס וליים | ₪19 | **₪20** | +1 | 77% → 81% | ₪3.76 → ₪3.25 |
| חליטת קמומיל ותפוח | ₪19 | **₪20** | +1 | 77% → 81% | ₪3.76 → ₪3.25 |
| חליטה מדברית | ₪19 | **₪20** | +1 | 77% → 81% | ₪3.76 → ₪3.25 |
| חליטת סנצ'ה ופסיפלורה | ₪19 | **₪20** | +1 | 77% → 81% | ₪3.76 → ₪3.25 |
| חליטת תה ירוק לואיזה וליים | ₪19 | **₪20** | +1 | 77% → 81% | ₪3.76 → ₪3.25 |
| חליטת תה ירוק ולמון גראס | ₪19 | **₪20** | +1 | 77% → 81% | ₪3.76 → ₪3.25 |
| חליטת יסמין וליצ'י | ₪19 | **₪20** | +1 | 77% → 81% | ₪3.76 → ₪3.25 |
| אייס מאצ'ה קפה | ₪28 | **₪29** | +1 | 81% → 79% | ₪4.52 → ₪5.26 |

12 prices unchanged. Margins moved on 46 of 48, food costs on 48 of 48.

## Two names, one drink

The page calls one cold infusion `חליטת תה ירוק לואיזה וליים`; the record calls it
`חליטת תה ירוק וליים`. Both sides list exactly seven cold infusions and six names match
exactly, so the pairing is forced rather than guessed — and the record gives all seven
identical figures, so it takes the same numbers either way. **Which name should the page
carry?** That is a copy decision, not a figures one.

## AMERICAN

The flavour card for AMERICAN offers a cold infusion. AMERICAN is a Tom-approved tea
extract (`docs/warehouses/catalog-truth.md`, grade `מאושר-טום`, ₪65/₪33, no active SKU)
but is not one of the 48 costed menu drinks. Its row takes the cold-infusion class
figure, which the record gives identically to all seven cold infusions; `patch_figures.py`
asserts that uniformity and halts the build if the record ever breaks it.

## Wholesale price list — checked, no change needed

The 23 wholesale rows were checked against
`docs/pricing/2026-08-05_shopify_products_exvat.tsv`: 22 match by price exactly. The
23rd, `הוג׳יצ׳ה 500 גרם ₪375`, is absent from the TSV because it has no active SKU, and
is Tom-approved in `catalog-truth.md`. The `כל 11 התערובות` count is also correct —
catalog-truth lists 11 tea extracts, AMERICAN included. The page's
`כל המחירים בשקלים, לפני מע״מ` matches the ex-VAT basis of both records.
