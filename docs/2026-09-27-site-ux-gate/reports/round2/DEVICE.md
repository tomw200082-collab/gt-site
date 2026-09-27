## interaction-design-specialist — brand site lead dialog and page (ROUND 2)

### Not applicable from my definition
`portal_ux_standard.md`, English-first, LTR, RUNTIME_READY, shadcn/Tailwind, Operational Precision tokens, and the factory-operator persona do not apply. This surface is GT's public Hebrew RTL brand site by Tom's approval; visitor replaces operator throughout.

---

### Round-1 findings

| ID | Status | Evidence |
|---|---|---|
| DEV-01 | FIXED | `.ld-grab` span is absent from `SHELL` in `tools/patch_lead_dialog.py:155–158`. No grab handle element anywhere in the CSS block. §9.2 confirms. |
| DEV-02 | ACCEPTED | §9.3 reason holds: all four page modals use `left:22px`; the dialog matches with `#ldlg .ld-x{left:12px}` at `patch_lead_dialog.py:227`. Changing only the dialog would break the cross-modal consistency that exists by design. Shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-02-open.png`. |
| DEV-03 | OPEN (P2) | `FIELDS_NEW` at `patch_lead_dialog.py:98–116` still has no `*` superscript or any required-field marker on any of the four required labels. Shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-02b-form.png`. |
| DEV-04 | ACCEPTED | §9.3 reason holds: a lead form in landscape on a phone is rare. The submit button is still in scrollable content (`patch_lead_dialog.py:233`), not sticky. Inferred, not observed on WebKit. |
| DEV-05 | FIXED | Auto-close timer and `.ld-bar` animation are gone. The dialog now closes via `visibilitychange` when the visitor returns from WhatsApp (`patch_lead_dialog.py:287–288`). §9.2 confirms "DEV-05 (no timer)". Facts: `replies.ok.stayedOpen:true`, `closedOnReturn:true`. |

---

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact CSS/HTML/JS) | Evidence |
|---|---|---|---|---|---|---|
| DEV-03 | P2 | S | Form — all viewports | The four required fields (שם מלא, שם העסק, עיר, טלפון) have no visual required indicator. The structural grouping (required above the fold, optional behind disclosure) implies the distinction but does not mark it — a visitor who expands the optional section loses the only structural cue and cannot tell which fields are mandatory without triggering the validation error. | In `patch_lead_dialog.py` lines 99–102, add `<sup aria-hidden="true">*</sup>` inside each required `<span>`: e.g., `<span>שם מלא<sup aria-hidden="true"> *</sup></span>`. Style with `#ldlg .pf-f>span sup{color:var(--gt);font-size:11px;margin-inline-start:1px}` in the CSS block. Copy decision (asterisk convention vs. legend) deferred to ux-content-state-designer. | `patch_lead_dialog.py:98–116`; shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-02b-form.png` |
| DEVICE-R2-01 | P1 | M | Phone bottom sheet — ask→form step transition, p320/p390/p430 | When the visitor taps "כן, יש לי עסק" on any phone width, the bottom-sheet height jumps from 308 px (ask step) to 714 px (form step) at p390 — a 406 px expansion — with no CSS transition or animation. Because the sheet is anchored to the screen bottom (`margin:auto auto 0`), its top moves upward by 406 px in a single frame: a full-sheet jump on the primary V1 path. `height:auto` rules out a direct CSS transition; the step toggle uses `display:none → display:grid` which is not transitionable. For a surface held to "Apple-level touch craft, on the cheapest Android in a kitchen," an instant sheet resize at the first deliberate action is below the bar. The jump at p390 moves the dialog top from y=536 to y=130 — the top of the visible page content — in one frame. | **S path (partial improvement):** in `patch_lead_dialog.py` CSS block, add a slide-in animation for the form content when it first becomes visible: `.partner:not(.ask):not(.priv):not(.sent) .pf-req,.partner:not(.ask):not(.priv):not(.sent) .pf-more{animation:ld-up .32s cubic-bezier(.2,.8,.25,1)}`. This reuses the existing `ld-up` keyframe (`translateY(40px)→translateY(0)`) so the form fields appear to grow into the space. The dialog outline still expands instantly, but the content arrival gives the expansion visual intent. **M path (gold standard):** before toggling the step class, capture `d.offsetHeight`, apply the class change, then animate from captured height to `d.offsetHeight` using `requestAnimationFrame` with `d.style.height` — the FLIP technique — then clear `d.style.height` after the transition. Add `#ldlg{transition:height .32s cubic-bezier(.2,.8,.25,1)}` while animating. This makes the sheet expansion smooth end-to-end, matching consumer app standards. | Facts: `p390.lead.open.box=[0,536,390,308]` vs `p390.lead.form.box=[0,130,390,714]`; shots: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-02-open.png` → `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-02b-form.png` |

---

### Interaction mechanics that are working correctly (round-2 additions)

These confirm the new step mechanics are sound and do not generate findings:

- **Step mechanic, all viewports:** `lead.steps.ok:true` at p390. `stepOnOpen:"ask"`, `focusOnOpen:"p#pf-ask-q"` — the dialog always opens on the business question; focus lands on the question, not an input, so the touch keyboard does not open automatically. ✓
- **"Yes" path:** `stepYes:"form"`, `focusYes:"b#ld-h"` — on touch, the heading receives focus (no auto-keyboard); on pointer:fine (desktop), the first field receives focus. ✓
- **"No" path:** `stepNo:"priv"`, `focusNo:"p#pf-priv-q"`. `sends:0` — no lead is dispatched on the private-buyer path. ✓
- **Elita Ofek link:** `shop.href:"https://elitaofek.co.il/product-category/gt/"`, `shop.blank:true`, `shop.text:"למוצרי GT אצל אליטה אופק ←"` — correct URL, new tab, correct label. ✓
- **Back button:** `stepBack:"ask"` — "חזרה" correctly returns to the ask step. ✓
- **Answer persists:** `stepReopen:"form"` — a visitor who answered "yes" and closed without submitting reopens directly to the form, not the ask step. ✓
- **Sent state stays open:** `replies.ok.stayedOpen:true`; no timer closes the dialog. ✓
- **WhatsApp links:** all five lines verified — `to:"https://wa.me/972547588132"`, `blank:true`, text `"היי, אני מעוניין ב[line]"` for each of the five lines. ✓
- **Close on return:** `openWhileAway:true`, `closedOnReturn:true`, `y2=y0`, `focusBack:true`. The dialog stays open while the visitor is in WhatsApp and closes the moment the page regains visibility. ✓
- **Reopen after send:** `reopenedSent:true` — a second CTA tap after a successful send shows the thank-you state and the five WhatsApp lines, not a blank form. ✓
- **Five pills at all phone widths:** all five lines render in the 2-column grid (4 pills × 52 px, last spanning full width) and fit within the viewport at p390. Shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-04-sent.png`. ✓
- **Private-buyer step height:** at p390 ask.box=[0,536,390,308], priv step is compact (heading + two lines of text + link + back button ≈ 260 px); the sheet shrinks back down from the ask step. ✓
- **deepLink with JS:** `deepLink.asks:true`, `fieldsShown:false`, `dialogOpen:false` — a URL opened with `#contact` scrolls to the inline form and shows the business question (consistent with the dialog), without opening the dialog. ✓
- **Two-column required grid at ≥640 px (i744, i820, t768, all larger):** confirmed by `@media(min-width:640px){.partner .pf-req{grid-template-columns:1fr 1fr}}` and shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/i744-lead-02b-form.png`. ✓
- **Photo pane at ≥880 px (li1180, li1366, d1360, d1920):** the ask step and form step both render in the side-by-side layout; the product photo fills the right pane while the ask question appears on the left. Shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/li1180-lead-02-open.png`. ✓
- **iPad regression:** all nine `home-*` facts for i744, i820, i1024, li1180, li1366 are identical to round-1 (modal, bodyScrollLocked, afterNext, afterChip, swipeRightIsNext, swipeLeftIsPrev, pageScrolledBehindModal, backCloses, deepLinkOpens, heroSwipeStep, afterFlavourTap all match). No regressions. ✓
- **fmodalAfter:false for all 19 CTAs:** the product window is never left open behind the lead dialog (INTER-01 was not reproducible in round 1; now confirmed by measurement). ✓
- **Page-stays-still after close:** `y2=y0` for all 19 CTAs; `p390-lead-05-after-close.png` shows the page exactly where it was. ✓

---

### World-class upgrades (beyond defects)

1. **JS FLIP height animation for step transitions.** The M-path fix in DEVICE-R2-01 — capture pre-step height, toggle class, animate to post-step height — would make the bottom-sheet expansion feel as smooth as Google Maps or Airbnb. Every consumer app uses this. The S-path content animation is a worthwhile interim improvement, but the full FLIP animation is what "Apple-level touch craft" requires here.

2. **`enterkeyhint` on required fields.** Add `enterkeyhint="next"` to `pf-name`, `pf-venue`, `pf-city` and `enterkeyhint="done"` to `pf-phone` in `patch_lead_dialog.py:99–102`. iOS visitors get a "Next" key between fields and a "Done" key on the last required field, completing the form without lifting their thumb to the screen between fields.

3. **Tint the sheet rim per drink.** `--ld-tint` is already set from the slide's colour. The 6 px `border-top` on `#ldlg` uses it. Extend the tint to the form-step's submit button: `.partner:not(.ask):not(.priv):not(.sent) form.partner>button.btn{background:var(--ld-tint,var(--gt))}` for slides (where the tint is a non-green colour). The button colour would match the drink the visitor came from, reinforcing the product connection that the photo achieves at ≥880 px.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 — phone, ad → slide CTA → business question → form → send | FRICTION | DEVICE-R2-01: 406 px height jump when tapping "כן"; extra tap for business question adds ~3 s to the V1 target; DEV-03: no required-field markers |
| V2 — desktop, catalogue CTA → send | PASS | — |
| V3 — flavour card → product window → הוסיפו לתפריט → send | PASS | `fmodalAfter:false` for all three flavour CTAs; product name travels as `ldCtx` interest |
| V4 — hesitant: ×, Esc, backdrop, back | PASS | All close mechanisms work at all viewports; `y2=y0` confirmed; `focusBack:true` |
| V5 — failure paths | PASS | All error variants (missing, bad phone, 502, timeout, offline) keep field values and surface actionable errors with WhatsApp and phone links |
| V6 — already sent, reopen | PASS | `reopenedSent:true`; second CTA opens to thank-you state + 5 WhatsApp lines |
| V7 — Hebrew screen reader | PASS (step focus correct); handoff to a11y-auditor for VoiceOver on priv and pick steps | Each step focuses its own question heading (`pf-ask-q`, `pf-priv-q`, `pf-pick-q`); `axe:[]` on the dialog in the sent state |
| V8 — keyboard only, desktop | PASS | `tabLeftDialog:0`; all fields reachable; Esc closes; no tab escape |
| V9 — no JS | PASS | `noJs.ok:true`; `asks:false`, `fieldsShown:true`; form fields visible; `telOpacity:"1"` |
| V10 — phone, whole page | FRICTION | DEV-03 (no required markers in form); DEVICE-R2-01 (height jump); page structure, hierarchy and voice are coherent |
| V11 — private buyer: no → Elita Ofek | PASS | `sends:0`; Elita Ofek link opens in new tab; "חזרה" returns to ask step |
| V12 — after send: pick a line → WhatsApp → return | PASS | `openWhileAway:true`; `closedOnReturn:true`; `y2=y0`; `focusBack:true` |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 1 (DEVICE-R2-01) | 1 (DEV-03) | **GREEN** — 0 P0, 1 P1 (≤2 P1 threshold) |

---

### Handoffs

**Copy handoff to `ux-content-state-designer`:** DEV-03 requires a decision on the required-field marker convention (asterisk with or without a legend at the form base).

**Accessibility handoff to `accessibility-usability-auditor`:** confirm focus management on the `pf-priv-q` and `pf-pick-q` headings under VoiceOver (TalkBack already measured via Chromium; iOS behaviour inferred); confirm the `visibilitychange`-triggered `ldClose()` does not mis-sequence announcements when the dialog closes on WhatsApp return.
