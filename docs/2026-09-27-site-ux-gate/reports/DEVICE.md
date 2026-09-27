## interaction-design-specialist — brand site lead dialog and page

### Not applicable from my definition
`portal_ux_standard.md`, English-first, LTR, RUNTIME_READY, shadcn/Tailwind, Operational Precision tokens, and the factory-operator persona do not apply. This surface is GT's public Hebrew RTL brand site by Tom's approval; visitor replaces operator throughout.

---

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact CSS/JS) | Evidence |
|---|---|---|---|---|---|---|
| DEV-01 | P1 | S | Phone bottom sheet — open, all phone widths | The `.ld-grab` pill handle renders on p320, p390, p430 (bottom-sheet layout, `<640px`) and signals "swipe down to dismiss" — the universal mobile affordance. No `touchstart`/`touchmove`/`touchend` handler is registered anywhere in the JS. Visitors who try to drag the sheet closed (the first natural reflex on any phone) get no response and must discover the × or the back gesture. | In `patch_lead_dialog.py` JS block (after the `close` event listener), add a touch-drag handler on `#ldlg`: track `touchstart` Y, on `touchend` check if downward delta exceeds 80 px and call `ldClose()`. Alternatively, if swipe is not planned, remove the `.ld-grab` span entirely from `SHELL` (line 117) and its CSS (line 172). Removing is the S path; adding swipe is M. | `patch_lead_dialog.py:117` (SHELL), `:172` (CSS), `:226-244` (JS — no swipe handler); shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r1/site-ipad/p390-lead-02-open.png`, `p430-lead-02-open.png` |
| DEV-02 | P1 | S | Dialog — open, all viewports | The × close button is positioned at `left:12px` (physical left edge). In Hebrew RTL, physical left is the logical END (trailing side). Every Hebrew-first mobile app (WhatsApp, Wolt, Booking.com in Hebrew) and Apple/Material RTL mirroring rules place the primary dismiss action on the logical START (physical right, `right:12px`). The heading's `padding-left:52px` also clears the wrong side — it creates left padding to avoid the × that is already on the left, but in RTL reading the heading renders from the right and the left-side padding is wasted space on the start side. | In `patch_lead_dialog.py` CSS (line 174), change `left:12px` → `right:12px`. Change line 178 `padding-left:52px` → `padding-right:52px`. Use logical properties if preferred: `inset-inline-start:12px` and `padding-inline-start:52px` (both resolve to physical right in RTL). No change needed to button dimensions. | `patch_lead_dialog.py:174` (`#ldlg .ld-x`), `:178` (`#ldlg .pf-head`); shot: `p390-lead-02-open.png`, `i744-lead-02-open.png`, `li1180-lead-02-open.png` |
| DEV-03 | P2 | S | Form — all viewports | The four required fields carry no visual required indicator. The form uses grouping (required first, optional behind "עוד פרטים (לא חובה)") to imply the distinction, which works for fluent users. First-time visitors who expand the optional section lose the structural cue and cannot tell which fields are mandatory without triggering the error. | In `patch_lead_dialog.py` lines 91–94, add a `*` superscript inside each required field `<span>`: e.g., `<span>שם מלא<sup aria-hidden="true"> *</sup></span>`. Style `sup` with `color:var(--gt);font-size:11px` so it reads as "required" without alarming visual weight. Copy review (asterisk vs. asterisk + legend) deferred to `ux-content-state-designer`. | `patch_lead_dialog.py:91-94`; shot: `p390-lead-02-open.png` |
| DEV-04 | P1 | M | Phone bottom sheet — keyboard raised, landscape orientation; inferred, not observed on WebKit | On a phone in landscape (e.g., iPhone 14 Pro at 932×430), `max-height:92dvh` caps the dialog at ~396 px. Single-column form height on a phone (heading ~75 px + 4 field-label pairs ~220 px + optional disclosure ~44 px + consent ~44 px + submit button ~54 px + WhatsApp line ~30 px = ~467 px) already requires scrolling before the keyboard appears. When the visitor taps any text field on iOS Safari, the software keyboard (~260 px in landscape) resizes the visual viewport but NOT the CSS `dvh` value. The keyboard slides over the bottom of the dialog; the submit button is inside the scrollable dialog content rather than pinned, so the visitor must scroll the dialog after typing in the last field to reach שליחה. `overscroll-behavior:contain` is correct and prevents page bleed, but the submit button is not keyboard-accessible without an additional scroll. | In `patch_lead_dialog.py` CSS phone block (lines 158–167), add `#ldlg form.partner>button.btn{position:sticky;bottom:env(safe-area-inset-bottom,0);z-index:1}`. This pins שליחה to the bottom of the dialog scroll container on all phone widths, making it reachable without a scroll regardless of keyboard height. The WhatsApp fallback line sits above the sticky button (it already has `order:1` in sent state; in normal state it follows the button, which is acceptable). Inferred from CSS — verify on a physical iPhone in landscape before shipping. | `patch_lead_dialog.py:158-167` (short-phone CSS), `:143` (`max-height:92dvh`), `:180` (submit button rule); inferred, not observed on WebKit |
| DEV-05 | P2 | S | Dialog — sent / auto-close | After a successful send, the dialog shows the "תודה רבה!" state and starts the 2-second `.ld-bar` countdown animation before closing itself. Sighted users see the progress bar contract. Screen readers receive no announcement that the dialog is about to close, no live region update, and no warning before `d.close()` fires. This is an accessibility-auditor concern, flagged here because the interaction mechanism (auto-close with no reversal path) owns the timing contract. | Add an `aria-live="polite"` region inside the dialog (alongside `.pf-done`) that is populated with a dismissal countdown message on success, e.g., "החלונית תיסגר אוטומטית בעוד רגע" injected at the same moment `d.classList.add('closing')` is set. Exact Hebrew copy deferred to `ux-content-state-designer`; handoff to `accessibility-usability-auditor` for role/live level and VoiceOver testing. | `patch_lead_dialog.py:299-301` (auto-close JS); `patch_lead_dialog.py:181-193` (CSS — `.ld-bar` animation) |

---

### Regression: changed facts between baseline and gate run

All `modal`, `navMode`, `afterNext`, `afterChip`, `swipeRightIsNext`, `swipeLeftIsPrev`, `pageScrolledBehindModal`, `backCloses`, `deepLinkOpens`, `heroSwipeStep`, `afterMatrix`, `homeProbe`, `matrixProbe` facts are byte-identical between `/scratchpad/facts-before-live-ipad/site_ipad_facts.json` and `/scratchpad/gate-r1/site-ipad/site_ipad_facts.json` for every iPad viewport (i744, i820, i1024, li1180, li1366) and the tablet viewport (t768). No regressions.

The only changed fact values are:

| Fact | Before | After | Assessment |
|---|---|---|---|
| `i744.afterDropdownTapUrl` | `https://gteveryday.com/` | `https://gteveryday.com/?preview_theme_id=186698334449` | Preview URL param only — destination identical |
| `i820.afterDropdownTapUrl` | `https://gteveryday.com/` | same with preview param | Same |
| `i744.afterFlavourTap` | `"/"` | `"/?preview_theme_id=186698334449"` | Preview param only |
| `i820.afterFlavourTap` | `"/"` | same with preview param | Same |
| `i1024.afterFlavourTap` | `"/"` | same with preview param | Same |
| `li1180.afterFlavourTap` | `"/"` | same with preview param | Same |
| `li1366.afterFlavourTap` | `"/"` | same with preview param | Same |

New keys in gate run (expected, not regressions): `lead.*` (the new dialog feature), `lp-chai/matcha/iced-tea/ube` (new landing page tests), `ddHiddenHits` (new measurement). All new `lead.*` facts show `hasDialog:true`, all 19 CTAs open/close correctly, `pageScrolledBehindModal:false`, and all `lp-*` entries have `overflowX:false`, `fits:true`, `gridInflated:false`.

---

### Interaction mechanics that are working correctly

These are not findings — they are evidence of the design working as intended:

- All 19 CTAs open the dialog; all three close mechanisms (×, Esc, backdrop) work on every viewport; `y0=y1=y2` for all CTAs confirms the page never moves.
- `lead.fits` is `true` for all four required fields and the consent checkbox on every phone and tablet viewport, including p320×640 (short phone with compact CSS active).
- All error responses (missing fields, bad phone, 502, 15 s timeout, offline) keep field values, show actionable error messages with WhatsApp and phone links, re-enable the button, and leave the dialog open for retry.
- The "silent drop" path (server returns `{ok:true}` without `was_new`) correctly shows the generic error rather than a false thank-you — no phantom conversions.
- The 3 s hold works on p390 (`fast.ok:true`, `elapsed_ms:3050`).
- `backCloses:true` on all iPad viewports — the history.pushState + popstate pattern delivers the expected "phone back gesture closes the dialog" behavior.
- `deepLink.dialogOpen:false` — a URL opened with `#contact` scrolls to the section without opening the dialog, as specified.
- `noJs.ok:true` — without JavaScript the links fall through to `#contact`, the phone/WhatsApp/mail links are visible.
- `tabLeftDialog:0` on d1360 and p390 — focus is fully trapped inside the dialog.
- All fields report `px:16` — no text input will trigger iOS focus zoom.
- `overflowX:false` on every viewport; `pageScrolledBehindModal:false` on all iPad viewports.
- Auto-focus on desktop (`focus:"input#pf-name"`), no auto-focus on touch (`focus:"button"`) — keyboard does not pop immediately on phone open.
- `reducedMotion:"none"` in harness; CSS reduced-motion block is in place for the open animation, the check-mark draw, and the bar.
- `reopenedSent:true` — a second CTA tap after a successful send shows the sent state, not a blank form.
- The 880px side-by-side photo layout on landscape iPad (li1180, li1366) renders correctly; the tint colour and bottle photo are visible in the right column (`li1180-lead-02-open.png`).
- The 2-column required-fields grid on 640 px+ viewports (i744, d1360) is readable and correct in RTL order (שם מלא on the right column, שם העסק on the left column in the first row).

---

### World-class upgrades (beyond defects)

1. **Swipe-to-dismiss with spring physics.** Remove the passive grab handle and replace it with an active drag: `touchstart` captures Y, `touchmove` translates the dialog `transform:translateY(delta)` in real time, `touchend` with velocity > 300 px/s or displacement > 120 px closes, otherwise springs back with `transition:transform .25s cubic-bezier(.2,.8,.25,1)`. This is the interaction that separates a good mobile sheet from an excellent one; every consumer app (Google Maps, Airbnb, Uber) uses it.

2. **Autofill-group the 4 required fields.** Add `autocomplete="name"` (already present) but also set `enterkeyhint="next"` on name/venue/city, and `enterkeyhint="done"` on phone. This gives iOS users a "Next" key that advances focus through fields and a "Done" key on the last required field, letting a fast visitor complete the form without touching the screen between fields.

3. **One-tap from the sent state.** After auto-close, the CTA that opened the dialog gets its aria-label updated to "פנייה נשלחה" and its icon changed to a check mark for the rest of the session. This communicates conversion to the visitor and prevents accidental re-engagement without friction.

4. **Tint the sheet rim per product.** The `--ld-tint` variable is already set from the hero slide or product card colour. Extend it to the grab handle (`background:var(--ld-tint,var(--line))`). The visual connection between the drink's colour and the sheet handle makes the origin of the dialog legible at a glance, reinforcing the "this dialog is about that drink" intent that the photo side achieves at 880 px.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 — phone, ad → slide CTA → send in under 30 s | FRICTION | DEV-01: swipe-down attempt on sheet does nothing; DEV-02: × is on the unexpected (left) side, adds ~1 s to dismiss discovery |
| V2 — desktop, catalogue CTA → send | PASS | — |
| V3 — flavour card → product window → הוסיפו לתפריט → send | PASS | Lead carries product name as interest (`ldCtx` mechanism confirmed by `f-detox` CTA facts) |
| V4 — hesitant: × / Esc / backdrop / back | FRICTION | DEV-02: × is on left side; swipe attempt (DEV-01) produces no response, requires a second strategy |
| V5 — failure paths | PASS | All error messages are actionable; WhatsApp and phone links present; fields kept |
| V6 — already sent, reopen | PASS | `reopenedSent:true` confirmed; WhatsApp line visible in sent state |
| V7 — Hebrew screen reader | FRICTION | `tabLeftDialog:0` and all labels correct; DEV-05: no countdown announcement before auto-close (→ a11y auditor) |
| V8 — keyboard only, desktop | PASS | Focus trapped, all fields reachable, Esc closes, no tab escape |
| V9 — no JS | PASS | `#contact` receives scroll, phone/WhatsApp/mail visible, `telOpacity:"1"` |
| V10 — phone, whole page | FRICTION | DEV-01, DEV-02 create minor friction on dismiss; page structure, hierarchy and voice are coherent |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 3 (DEV-01, DEV-02, DEV-04) | 2 (DEV-03, DEV-05) | AMBER — no P0, but 3 P1 exceeds the ≤2 P1 green threshold |

---

### Handoffs

**Copy handoff to `ux-content-state-designer`:** DEV-03 requires a decision on the required-field marker convention (asterisk with or without a legend). DEV-05 requires the Hebrew text for the `aria-live` auto-close announcement.

**Accessibility handoff to `accessibility-usability-auditor`:** DEV-05 — auto-close with no `aria-live` notification; also confirm the `role` and `aria-modal` semantics of the `<dialog>` element under VoiceOver on iOS 16+ and TalkBack; confirm that the × button's `aria-label="סגירה"` is announced correctly in RTL with VoiceOver.
