## visual-system-designer — brand site lead dialog and page (round 2)

### Not applicable from my definition
`portal_ux_standard.md`, English-first, Operational Precision tokens (shadcn/Tailwind), and RUNTIME_READY do not apply; this is GT's public Hebrew RTL brand site.

---

### Round-1 findings

| ID | Status | Evidence |
|---|---|---|
| VIS-01 | ACCEPTED | §9.3 reason holds: product window (`.fmodal`) also places photo on the right (RTL leading) and text on the left; a V3 visitor sees one arrangement across both modals, not two. shot:`d1360-lead-02-open.png` |
| VIS-02 | FIXED | `fits.send:true` at p320 in `site_ipad_facts.json`; all four fields, consent and send button land within the 640 px sheet height. shot:`p320-lead-02b-form.png` |
| VIS-03 | OPEN | `patch_lead_dialog.py:232` still reads `background:#fff` — literal hex, not `var(--white)`. |
| VIS-04 | OPEN | `patch_lead_dialog.py:198–199` still uses `rgba(24,26,22,.45)` and `rgba(24,26,22,.55)` — shifted 8/8/9 from `--ink:#20241F`. |
| VIS-05 | OPEN | No `font-size` override for `.partner .pf-head span` in the dialog CSS block; the inherited 12.5 px page value persists. `#6b6659` is now applied site-wide by `patch_a11y.py` as a string replace of `#8a8577`, but it remains a hardcoded hex with no `:root` entry. |
| VIS-06 | OPEN | `patch_form.py:97–99` error-box colors (`background:#FBEAE7;border:1px solid #E5B4AB;color:#7A2E1E`) unchanged; not listed in §9.2. shot:`p390-lead-03-error.png` |
| VIS-07 | OPEN | `patch_lead_dialog.py` SHELL: `✕` (U+2715) glyph unchanged. |
| VIS-08 | OPEN | Hero slides: `הוסיפו לתפריט` (lead CTA) is a text link; `למתכונים ←` is a filled dark pill. The label changed from round 1 but the visual-weight disparity is unchanged. shot:`p390-page-01.png`, `d1360-page-01.png` |
| VIS-09 | ACCEPTED | §9.3 reason holds: `patch_rtl_shell.py` has `.step:not(:last-child):after{content:'←'}` already; the round-1 finding was incorrect. |

---

### New steps audit (round-2 dimension work)

**Ask step (`-lead-02-open`), all widths**

Phones (p320, p390, p430): the sheet rim carries `--ld-tint` (green from the hero, correct), `border-top:6px solid var(--ld-tint)` is token-correct. The heading "בואו נעבוד יחד" (28 px, Heebo heavy, RTL) anchors the dialog name. Below it, "עונים תוך יום עסקים אחד" in the inherited 12.5 px muted tone (see VIS-05, open). The question "יש לכם עסק?" at 20 px/800 weight reads as the primary step prompt. Two buttons stack vertically: "כן, יש לי עסק" is a full-width dark-fill pill (correct primary weight); "לא, לשימוש פרטי" is a ghost/outline pill (`box-shadow:inset 0 0 0 1.5px var(--line)`, `background:none`), correctly subordinate. Both buttons are 52 px tall, both visible without scroll (facts: `ask[0].shown:true`, `ask[1].shown:true`). Rhythm and density are clean.

Tablet and iPad (i744–li1366, 640–879 px): the sheet transitions to a centred card (max-width:480 px, border-radius:26 px), no photo panel. Content is identical, rhythm holds.

Desktop two-column (880 px+, li1180, li1366, d1360, d1920): left form panel uses `justify-content:center` so the ask content floats vertically centred in the fixed card height. At d1920 the whitespace above and below the two buttons is large but intentional (CSS comment: "one card height for every step: the short ones sit in the middle"). Photo panel on right shows the hero shelf bottles. Hierarchy is clear.

One issue raised below (VIS-R2-01): "עונים תוך יום עסקים אחד" visible in the ask step.

**Private step (`-lead-06-private`), p390 and d1360**

The heading "בואו נעבוד יחד" is retained (correct — it names the dialog). The subtitle "עונים תוך יום עסקים אחד" is correctly hidden (`.partner.priv .pf-head span{display:none}` confirmed in CSS and in the rendered shot). The bold question "אנחנו עובדים רק עם עסקים." at 20 px/800 reads clearly. Body text "ללקוחות פרטיים, המוצרים שלנו נמכרים באתר של אליטה אופק." at 15 px/`--ink-soft`. The Elita Ofek button is a full-width dark-fill pill with the `←` RTL-forward arrow — correct primary action weight. "חזרה" is a `<button>` in green, no border, no background, centered below — correctly the least prominent element. At desktop the same content is vertically centred in the left panel; the photo panel persists unchanged. Facts: `steps.stepNo:'priv'`, `steps.sends:0`, `shop.blank:true`. PASS.

**Sent step (`-lead-04-sent`), p390 and d1360**

Check icon: 64 px, `fill:#EEF4EA` (soft green tint, within brand), `stroke:var(--gt)` (token-correct). "תודה רבה!" at 28 px Roca One/Heebo 400 weight — matches the form heading weight class, brand voice. Body text 15 px/`--ink`. The phone number link is underlined and in the page's green.

Divider: `border-top:1px solid var(--line)` — uses the correct system token. Renders as a clean light separator between the thanks and the pick section. PASS.

Five pills: 2×2 grid plus one full-width `.pf-wide`. Pill style: `background:var(--white); box-shadow:inset 0 0 0 1.5px var(--line); color:var(--ink); border-radius:999px; min-height:52px` — all token-correct and consistent with the ask-step ghost button pattern. Ink-on-white contrast 14.85:1. On hover/focus, border shifts to `inset 0 0 0 2px var(--gt)`. "בניית תפריט משקאות בעסק שלי" (24 chars) spans the full width and fits on one line at all widths tested. Facts: all five lines confirmed with correct `wa.me` href and prefilled messages.

At desktop (d1360): left panel shows check + thanks + divider + pick pills; right photo panel retains the static bottle image. The asymmetry (transformed left / unchanged right) is visually acceptable though not architecturally resolved (world-class upgrade below). PASS.

**Darkened page colours (eyebrows and card origins)**

Card eyebrow text: `patch_a11y.py` sets `color:#9C5C3C` (was `--terra:#C4744B`). Against `--card:#F3EFE6` the ratio is ≈6.7:1; the colour stays firmly within the terra-warm brand arc — no perceptible hue shift, just darker. shot:`d1360-page-02.png`.

Card origin labels: darkened from `#9A9F93` to `#60635C`. Against `--paper:#FBF8F2` and the card fill, these read as muted secondary labels within the existing type scale. No brand drift. PASS.

**New call-to-action words — length, wrapping, weight**

| Placement | Label | Width tested | Wraps? | Weight |
|---|---|---|---|---|
| Nav pill (phone) | בואו נעבוד יחד ← | p390 | No | Dark-fill pill, correct primary |
| Hero CTA | בואו נעבוד יחד ← | p390, d1360 | No | Dark-fill pill, correct primary |
| Hero slides (×10) | הוסיפו לתפריט | p390, d1360 | No | Text link — see VIS-08 (open) |
| Catalogue / economics / closing | בואו נעבוד יחד ← | d1360 | No | Pill/ghost on its background, correct |
| Closing banner body | נבנה יחד תפריט משקאות שהאורחים שלכם יצלמו. | d1360 | Wraps at narrow | Intentional wrap, reads cleanly |

---

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact CSS/HTML) | Evidence |
|---|---|---|---|---|---|---|
| VIS-R2-01 | P2 | S | Dialog ask step, all widths | The heading subtitle "עונים תוך יום עסקים אחד" is visible before the visitor has confirmed they have a business. A visitor who selects "לא, לשימוש פרטי" has been shown a reply-speed promise that does not apply to them. The CSS hides the subtitle only in the `priv` step: `.partner.priv .pf-head span{display:none}` — the `ask` step is not covered. | `patch_lead_dialog.py` CSS: change `.partner.priv .pf-head span{display:none}` to `.partner.ask .pf-head span,.partner.priv .pf-head span{display:none}`. The subtitle then appears only in the form and sent steps, where the promise is relevant. | shot:`p390-lead-02-open.png` |
| VIS-R2-02 | P2 | S | Dialog, all input states | TOKEN_DRIFT. `patch_lead_dialog.py:232` uses `background:#fff` instead of `var(--white)`. Value is identical today; any future system-wide input-background change silently misses the dialog. | `patch_lead_dialog.py:232` — replace `background:#fff` with `background:var(--white)`. | `patch_lead_dialog.py:232` |
| VIS-R2-03 | P2 | S | Dialog sheet shadow and backdrop | TOKEN_DRIFT. `patch_lead_dialog.py:198–199` uses `rgba(24,26,22,` in two box-shadow values. `--ink` is `#20241F` = rgb(32,36,31); the shadow colour is shifted 8/8/9 away from the system ink. | `patch_lead_dialog.py:198–199` — replace `rgba(24,26,22,.45)` with `rgba(32,36,31,.45)` and `rgba(24,26,22,.55)` with `rgba(32,36,31,.55)`. | `patch_lead_dialog.py:198–199` |
| VIS-R2-04 | P2 | S | Dialog, form heading subtitle | TOKEN_DRIFT + size. `.partner .pf-head span` (renders "עונים תוך יום עסקים אחד") inherits the page's 12.5 px — below the 13.5 px field-label floor. The colour `#6b6659` is applied by `patch_a11y.py` as a string replacement of `#8a8577` with no `:root` entry. | (a) Propose `--ink-muted:#6b6659` to `:root` — requires Tom authorization as a design-token addition. Once added, reference `var(--ink-muted)` site-wide. (b) Immediately actionable without a new token: add `#ldlg .pf-head span{font-size:13.5px}` to the CSS block in `patch_lead_dialog.py`. | `patch_lead_dialog.py` CSS block; shot:`p390-lead-02b-form.png` |
| VIS-R2-05 | P2 | S | Dialog, error state | TOKEN_DRIFT. `patch_form.py:97–99` hardcodes `background:#FBEAE7;border:1px solid #E5B4AB;color:#7A2E1E`. A second error surface would need to reproduce all three values manually. | Propose three tokens: `--error-bg:#FBEAE7`, `--error-border:#E5B4AB`, `--error-fg:#7A2E1E` (Tom authorization required). Until then, document the three values in a CSS comment referencing their relationship to `--terra:#C4744B`. | `patch_form.py:97–99`; shot:`p390-lead-03-error.png` |
| VIS-R2-06 | P2 | S | Dialog close button, all viewports | COMPONENT_INCONSISTENCY. `patch_lead_dialog.py` SHELL uses `✕` (U+2715 MULTIPLICATION X) at `font-size:18px`. On Noto (stock Android) and Samsung fonts this glyph renders at variable weight across OS versions; an inline SVG delivers a precisely-weighted cross on all platforms. | `patch_lead_dialog.py` SHELL: replace `✕` with `<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/></svg>`. Remove `font-size:18px` from the `.ld-x` rule. | `patch_lead_dialog.py:157,227` |
| VIS-R2-07 | P2 | S | Page, hero slides, p390 and d1360 | SYSTEM_RULE. On every hero slide `הוסיפו לתפריט` (the lead CTA, text link) is visually subordinate to `למתכונים ←` (a filled dark pill). The label changed from "רוצה מחירון" but the weight disparity is unchanged: the slide's secondary action (recipe exploration) dominates the primary conversion action (lead capture). | `patch_lead_dialog.py` CSS: add `.hs-slide .sub-cta[href="#contact"]{border:1.5px solid currentColor;border-radius:999px;padding:5px 14px}`. This gives the lead link ghost-pill weight equal to the outline buttons used elsewhere in the dialog, without a new colour. Scoped to `[href="#contact"]` so it does not affect any other `.sub-cta`. | shot:`p390-page-01.png`, `d1360-page-01.png` |

---

### World-class upgrades (beyond defects)

1. **Desktop sent state: resolve the full card.** In d1360-lead-04-sent.png the right photo panel continues showing static bottles while the left panel transforms to a celebration. Fade the photo panel to a warm wash of `--ld-tint` at 12 % opacity behind a larger (96 px) check, so the whole dialog becomes the thank-you rather than half of it. Timing aligns with the `ld-draw` keyframe (0.45 s).

2. **Real-time Israeli phone hint.** An `input` listener that detects a non-`05X` pattern and shows a soft inline note ("מספרי ישראל מתחילים ב-05") while typing — without blocking submission — eliminates the most common V5 failure before the visitor reaches the button and the 3 s hold.

3. **Ask step: drop the subtitle "עונים תוך יום עסקים אחד" and replace with "בסיטונאות, לעסקים."** This echoes the same qualification signal as the button label and the question body, so the heading area speaks with one voice. The reply-speed promise then appears only on the form step where it is a direct commitment. (Tied to VIS-R2-01; this is the copy version of the same fix.)

4. **Contextual step heading on the form.** Once the visitor has tapped "כן, יש לי עסק", the form heading "בואו נעבוד יחד" could carry a one-line echo of the slide or product they opened from — set via `ldCtx` at open, already available in JS. Makes the form feel earned rather than generic.

5. **Photo panel: product-specific still for non-slide CTAs.** Catalogue, economics card, and closing banner CTAs all show the same hero-shelf photo. A curated full-lineup shot for `data-cta="catalogue"` and a different angle for `data-cta="economics"` would make the panel feel intentional rather than a fallback.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1: Phone from ad → hero slide → "הוסיפו לתפריט" → "כן, יש לי עסק" → fill four fields → send → scroll | PASS | Extra tap (business question) adds ~2 s but both ask buttons are on screen without scroll at p390 (facts). All four fields + consent + send fit (facts: `fits.send:true` at p390). Page returns to original scroll position after close (y0=y2). "הוסיפו לתפריט" text-link weight is weaker than "למתכונים" pill (VIS-R2-07, P2). |
| V6: Already sent → tap another CTA → see sent state and five lines | PASS | facts: `replies.ok.reopenedSent:true`. The sent form is preserved between opens; the pick step is shown immediately on reopen. |
| V11: Private buyer → "לא, לשימוש פרטי" → understand GT is B2B → reach Elita Ofek | PASS | facts: `steps.stepNo:'priv'`, `steps.sends:0`, `shop.href:'https://elitaofek.co.il/product-category/gt/'`, `shop.blank:true`. Nothing reaches sales. Hierarchy of private step is clear. Minor: visitor sees "עונים תוך יום עסקים אחד" in the preceding ask step (VIS-R2-01, P2). |
| V12: After send → pick a line → WhatsApp opens → return → dialog gone → page where it was | PASS | facts: `replies.ok.openWhileAway:true`, `closedOnReturn:true`, `y2:6904` equals `y0:6904`, `focusBack:true`. Visibility-change handler fires once and removes itself correctly. |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 0 | 7 (VIS-R2-01 through VIS-R2-07) | **GREEN** — no P0, no P1 |

The three new steps are visually coherent, correctly token-referenced for structure and rhythm, and integrate without any visible seam against the rest of the page. The button hierarchy within each step (dark fill > ghost > text link) is correctly observed. All seven open findings are P2 token-hygiene and component-consistency issues; none blocks a visitor task. The slide lead-CTA weight (VIS-R2-07) is the only finding that affects a high-traffic surface, and it is a polish improvement rather than a conversion blocker.
