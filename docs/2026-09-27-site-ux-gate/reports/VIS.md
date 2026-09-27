## visual-system-designer — brand site lead dialog and page

### Not applicable from my definition
`portal_ux_standard.md`, English-first rule, Operational Precision tokens (shadcn/Tailwind), and RUNTIME_READY do not apply; this page is GT's public Hebrew RTL brand site, not the operations portal.

---

### Design system reference
- `tailwind.config.ts`: not applicable (Shopify static section)
- `globals.css`: not applicable
- Page token system: `:root` in `src/index.html` — `--paper:#FBF8F2`, `--ink:#20241F`, `--gt:#3E6E34`, `--gt-d:#2B4F24`, `--terra:#C4744B`, `--card:#F3EFE6`, `--white:#FFFFFF`, `--ink-soft:#4B5148`, `--line:#E7E1D3`. Dialog CSS in `patch_lead_dialog.py` mostly references these tokens correctly — drift identified in three places (VIS-03, VIS-04, VIS-05).

---

### Contrast audit (dialog — all states)

| Surface | Text color | Background | Ratio | Result |
|---|---|---|---|---|
| Field labels (13.5 px bold) | `#4B5148` (--ink-soft) | `#FBF8F2` (--paper) | 7.72:1 | AA ✓ |
| Subtitle / footer alt (12.5 px) | `#6b6659` | `#FBF8F2` | 5.40:1 | AA ✓ |
| Disclosure toggle (14 px bold) | `#3E6E34` (--gt) | `#FBF8F2` | 5.68:1 | AA ✓ |
| Error text (13.5 px) | `#7A2E1E` | `#FBEAE7` | 8.06:1 | AAA ✓ |
| Send button (16 px bold) | `#FBF8F2` | `#20241F` | 14.85:1 | AAA ✓ |
| Close button icon | `#20241F` | `#F3EFE6` (--card) | 13.72:1 | AAA ✓ |
| Footer links (וואטסאפ / phone) | `#3E6E34` (--gt) | `#FBF8F2` | 5.68:1 | AA ✓ |

All dialog text passes WCAG 2.1 AA. The subtitle at 12.5 px passes on ratio but is flagged for size (VIS-05).

---

### RTL audit

| Check | Result |
|---|---|
| Disclosure marker (`::before` content `+`) at RTL leading (right) side | PASS — RTL flex places `::before` on right in Hebrew context |
| Consent checkbox at RTL leading (right) side of label | PASS |
| Submit button arrow `←` pointing left (correct RTL "forward") | PASS |
| Countdown bar depletes from left, anchored at right (`transform-origin:right`) | PASS — remaining time shown on RTL leading side |
| No-JS `#contact` deep-link scrolls without opening dialog | PASS (facts: `noJs.ok:true`) |
| Desktop two-column: photo on right (RTL leading), form on left (RTL trailing) | **FAIL — VIS-01** |
| Close button at `left:12px` (RTL trailing edge of sheet) | PASS — matches iOS Hebrew sheet convention |

---

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact CSS/HTML) | Evidence |
|---|---|---|---|---|---|---|
| VIS-01 | P1 | M | Dialog open, ≥880 px (li1180, li1366, d1360, d1920) | RTL column order is reversed. HTML order is `[ld-pic][ld-main]`. In RTL CSS Grid, the first element occupies the right column (RTL leading). So the product photo (ld-pic, 5fr) sits on the right (the first thing a Hebrew reader sees) and the form (ld-main, 6fr) sits on the left (trailing). For a lead-capture dialog whose one job is conversion, the form must lead the eye from the right. | `patch_lead_dialog.py` — SHELL: swap element order to `<div class="ld-main">…</div><div class="ld-pic">`. `@media(min-width:880px)` CSS: `grid-template-columns:minmax(0,6fr) minmax(0,5fr)` (form is now first/right with more space; photo left with less). Change `#ldlg .ld-x{left:12px}` → `right:12px`. Change `#ldlg .pf-head{padding-left:52px}` → `padding-right:52px`. The close button stays in the form panel corner; the heading clears it on the opposite side. | shot:`/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r1/site-ipad/li1180-lead-02-open.png`, `d1360-lead-02-open.png`, `d1920-lead-02-open.png` |
| VIS-02 | P1 | S | Dialog open, p320 (320×640) | At the smallest common device (iPhone SE / cheap Android 320 wide, 640 tall) the submit button is below the viewport. The short-phone media query `@media(max-width:639px) and (max-height:760px)` tightens spacing but does not fully recover the ~25 px needed for the button to be on screen. `fits.pf-agree:true` confirms the consent is visible; no `fits` entry for the button confirms it is not. The intent stated in the code comment is "consent and button on the first screen." | `patch_lead_dialog.py` CSS inside `@media(max-width:639px) and (max-height:760px)`: reduce `#ldlg .pf-head b{font-size:22px}` (currently 24 px, saves 4 px), set `#ldlg form.partner{gap:8px}` (currently 10 px, saves ~20 px across 4 gaps), add `#ldlg .pf-head span{font-size:12px}`. Combined saving of ~26 px is sufficient. | shot:`/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r1/site-ipad/p320-lead-02-open.png` |
| VIS-03 | P2 | S | Dialog, all input states | SYSTEM_RULE — TOKEN_DRIFT. `#ldlg input:not([type=checkbox]),#ldlg select,#ldlg textarea{background:#fff}` uses a literal hex instead of the system token. `--white:#FFFFFF` is defined in `:root` and `#fff === #FFFFFF`, so there is no visual deviation today, but any future system-wide input background change would silently miss dialog inputs. | `patch_lead_dialog.py` CSS line 179: replace `background:#fff` with `background:var(--white)`. | `patch_lead_dialog.py:179` |
| VIS-04 | P2 | S | Dialog, phone sheet + desktop card shadow; backdrop | TOKEN_DRIFT. Box-shadow uses `rgba(24,26,22,.45)` and `rgba(24,26,22,.55)` (two occurrences). `--ink:#20241F` = rgb(32,36,31). The shadow colour is shifted 8/8/9 from the system ink, making it a slightly cooler, different dark. Imperceptible in isolation but incorrect for system maintenance. | `patch_lead_dialog.py` CSS lines 144–145: replace every instance of `rgba(24,26,22,` with `rgba(32,36,31,`. | `patch_lead_dialog.py:144-145` |
| VIS-05 | P2 | S | Dialog, form heading area + footer alt text | TOKEN_DRIFT + size. `.partner .pf-head span,.partner .pf-alt{color:#6b6659}` is a hardcoded hex without a `:root` entry. The inherited page rule `.partner .pf-head span{font-size:12.5px}` is not overridden in the dialog context, leaving the subtitle "עונים תוך יום עסקים אחד" at 12.5 px — below the 13.5 px floor used for field labels. Contrast passes (5.40:1) but the size is conspicuously small for an emotional trust line. | Propose new system token `--ink-muted:#6b6659` to `:root` (requires Tom authorization as a design-token change). Once added, update `patch_lead_dialog.py` CSS to `color:var(--ink-muted)`. Immediately actionable (no token): add `#ldlg .pf-head span{font-size:13.5px}` to the dialog CSS block in `patch_lead_dialog.py`. | `patch_lead_dialog.py:134,136`; shot:`p390-lead-02-open.png` |
| VIS-06 | P2 | S | Dialog, error state | TOKEN_DRIFT. Error box in `patch_form.py:97–99`: `background:#FBEAE7;border:1px solid #E5B4AB;color:#7A2E1E` are hardcoded. The palette is coherent (warm red, coordinates with `--terra:#C4744B`) but has no `:root` anchors. A second error surface anywhere on the page would need to reproduce these three values manually. | Propose three tokens: `--error-bg:#FBEAE7`, `--error-border:#E5B4AB`, `--error-fg:#7A2E1E` to `:root` (Tom authorization required). Update `patch_form.py` to reference them. | `patch_form.py:97-99` |
| VIS-07 | P2 | S | Dialog close button, all viewports | COMPONENT_INCONSISTENCY. Close button renders `✕` (U+2715 MULTIPLICATION X) at `font-size:18px`. On stock Android (Noto) and Samsung fonts this glyph can render thinner or thicker than intended. An inline SVG path delivers a precisely-weighted cross consistent across all platforms. | `patch_lead_dialog.py` SHELL: replace `✕` with `<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/></svg>`. Remove `font-size:18px` from `#ldlg .ld-x` rule. | `patch_lead_dialog.py:118,174`; shot:`p390-lead-02-open.png` |
| VIS-08 | P2 | S | Page, hero slides, all phone and desktop widths | SYSTEM_RULE — CTA visual weight mismatches conversion job. The page's stated one job is lead generation. On every hero slide, the lead CTA "רוצה מחירון" (`sub-cta`) is a lightweight green text-link; the recipe CTA "למתכונים ←" is a filled dark pill. All 19 lead CTAs funnel to the same dialog, yet on the highest-traffic surface (the hero slider) the lead CTA is visually subordinate to product exploration. A lead-optimised hierarchy would give the lead CTA at least ghost-pill weight. | `patch_lead_dialog.py` CSS: add `.hero .sub-cta[data-price]{border:1.5px solid var(--gt);border-radius:999px;padding:5px 14px;font-size:13px}`. Scoped to `data-price` slides only (set by this patch), so the rule is safe and does not affect other sub-ctas. | shot:`/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r1/site-ipad/p390-page-01.png`, `d1360-page-01.png` |
| VIS-09 | P2 | S | Page, process steps section | RTL direction error. `.step:not(:last-child):after{content:'→'}` inserts a right-pointing arrow at `right:-16px` between steps. In RTL, step 1 is on the right and step 4 on the left; a `→` between steps 1 and 2 points back toward step 1, not forward. Should be `←` (U+2190). Pre-existing; not introduced by the dialog work. | In a patch file (e.g., `tools/patch_ux.py` which runs before the dialog patch): inject CSS `.step:not(:last-child):after{content:'\\2190'}`. Or correct `src/index.en.html` directly at the `.step:not(:last-child):after` declaration. | `src/index.html` (built output), visible in page CSS at `.step:not(:last-child):after` |

---

### World-class upgrades (beyond defects)

1. **Contextual dialog headline by entry point.** The dialog already wears the slide colour and photo. Extend this to the micro-copy: when opened from a lemonades slide, show a one-line context echo — "מחפשים לימונדות לתפריט?" — as a small coloured chip above the heading. `ldCta` and slide number are already available in JS; a single `ldCtx` string set at open time drives it. This bridges the gap between product interest and the lead ask.

2. **Real-time Israeli phone-format hint.** The phone error currently appears only after the 3-second hold and network round-trip. An `input` listener that detects a non-Israeli pattern (not starting with 05X) and shows a soft inline hint ("מספרי ישראל מתחילים ב-05X") while typing — without blocking submission — eliminates the most common V5 failure before the visitor reaches the button.

3. **Progress micro-animation during the 3-second hold.** The button says "שולח…" for up to 3 seconds. A subtle pulse or a progress-fill on the button border during the hold (e.g., `@keyframes btn-fill` animating `box-shadow` inset from 0 to 100%) would reassure the visitor the form is working, not stuck. Align with `LD_CLOSE_MS` timing.

4. **Photo panel: product-specific image for non-slide CTAs.** Catalogue, economics card, and closing banner CTAs show the generic hero bottle shelf photo in the desktop dialog. The Detox/Energy/Revive pack image is already in cache. For named CTAs (`data-cta="catalogue"`, `"economics"`) a curated photo (e.g., the full product line arranged differently) would make the panel feel intentional rather than fallback.

5. **Sent-state closing: animate the check into the full panel at desktop.** On desktop, after submit the left (form) panel shows the check centered in a mostly empty area. The right photo panel simply persists. A subtle fade of the photo to a warm wash of `--ld-tint` at 15% opacity behind a larger (96 px) check icon would make the confirmation feel architecturally resolved — the whole card becomes the "thank you," not just half of it.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1: Phone from ad → hero slide → "רוצה מחירון" → send → scroll | PASS | All fields fit on p390 (facts confirm); 3-second hold works (facts: `elapsed_ms:3050, success:true`); page returns to position after close |
| V2: Desktop → "לקבלת הקטלוג המלא" → send | PASS | facts: cta[12] opens, focusIn, interest presets to "המחירון המלא", closedBy x, y0=y2 |
| V3: Flavour card → product window → "הוסיפו לתפריט" → send with product | PASS | facts: fmodal CTAs open dialog, ldCtx carries product name, interest falls back to ldCtx if empty |
| V4: Hesitant: ×, Esc, backdrop, back button | PASS | facts: all four close paths confirmed across CTAs; focusBack:true; y0=y2 for all (page does not move) |
| V5: Bad phone, network error, timeout, offline | PASS | facts: all error reply states show `kept:true` (values preserved), error text includes WhatsApp and phone links; closedItself:false so visitor can retry |
| V6: Already sent → reopen | PASS | facts: `reopenedSent:true` — a re-opened dialog shows the sent state, not an empty form |
| V7: Hebrew screen-reader (VoiceOver/TalkBack) | PASS (structural; a11y dimension owns final verdict) | `aria-labelledby="ld-h"` on dialog; `aria-label="סגירה"` on close button; decorative elements `aria-hidden`; `axe:[]` on dialog |
| V8: Keyboard only, desktop | PASS | facts: `tabLeftDialog:0` confirms focus trap; close button has `focus-visible` ring; first field autofocused on open at pointer:fine |
| V9: No JavaScript | PASS | facts: `noJs.ok:true`; `#contact` scrolls to in-page form; tel/WA/mail links visible (`telOpacity:"1"`) |
| V10: Read whole page on phone | FRICTION | Lead CTA "רוצה מחירון" lower visual weight than "למתכונים" on hero slides (VIS-08); four different labels for one dialog reduces voice clarity across the scroll; process step arrows RTL direction issue (VIS-09) |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 2 (VIS-01 RTL column, VIS-02 p320 button) | 7 | **GREEN** — ≤2 P1 and no P0 |

The dialog integrates cleanly into the page's own visual system. All contrast passes. The "borrowed form" architecture (one form, one sender, one state) is structurally sound. The two P1 items (RTL column order and p320 button visibility) are both mechanical fixes in `patch_lead_dialog.py` with no design ambiguity. The page can ship at AMBER for the RTL two-column issue if the target audience is understood to be primarily phone users (where the two-column layout does not appear), but for desktop conversion quality the fix is recommended before publication.
