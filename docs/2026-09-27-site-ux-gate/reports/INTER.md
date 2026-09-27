## Action Completeness Matrix

| Action | Disabled | Loading | Feedback | Undo / Recovery | Error | Double-activation safe | Keyboard |
|---|---|---|---|---|---|---|---|
| Nav "רוצים להתחיל" | No — always enabled | No | Dialog opens, hero-bottles tint on rim | ×, Esc, backdrop, back button | N/A | Yes — `if(d.open)return false` guard | Yes — native `<a>` |
| Hero "אני מעוניין" | No | No | Dialog opens | ×, Esc, backdrop, back | N/A | Yes | Yes |
| Slides ×10 "רוצה מחירון" | No | No | Dialog + "המחירון המלא" preset, slide photo+tint | ×/Esc/backdrop/back — preset reset on close-without-send | N/A | Yes | Yes |
| Catalogue "לקבלת הקטלוג המלא" | No | No | Dialog + "המחירון המלא" preset | preset reset on close-without-send | N/A | Yes | Yes |
| Economics "רוצה מחירון ותמחירים" | No | No | Dialog + preset | preset reset | N/A | Yes | Yes |
| Closing "רוצים להתחיל" | No | No | Dialog opens (no preset) | ×, Esc, backdrop, back | N/A | Yes | Yes |
| Product window "הוסיפו לתפריט" | No | No | Dialog opens; product name as interest fallback | × closes dialog but fmodal stays open — **INTER-01** | N/A | Yes | Yes |
| Close × | No | No | Dialog closes; page y unchanged; focus returned to opener | N/A | N/A | Yes — button | Yes — native `<button>` |
| Esc key | n/a | n/a | Same as × | N/A | N/A | n/a | Yes — native `<dialog>` |
| Backdrop click | n/a | n/a | Same as × | N/A | N/A | n/a | No — pointer-only; intentional |
| Phone back button (popstate) | n/a | n/a | Same as × (history.back() not double-fired due to ldDoc guard) | N/A | N/A | n/a | n/a |
| "עוד פרטים (לא חובה)" disclosure | n/a | No | Optional fields appear/collapse | Re-collapse | N/A | Yes — native `<details>` | Yes — native Space/Enter |
| Consent checkbox | n/a | No | Checked/unchecked | Re-uncheck | Browser tooltip on submit-without-consent | n/a | Yes |
| "שליחה" submit | Yes — on send start | Yes — "שולח…", button disabled | Error banner or sent state | All values kept on error; button re-enabled | Per-type banners + WA/phone links | Yes — `btn.disabled=true` on first click | Yes — `<button>` |
| WhatsApp link | No | No | Opens WA with no pre-filled message — upgrade opportunity | N/A | N/A | n/a | Yes — `<a>` |
| Phone 054-398-2444 | No | No | Opens dialler | N/A | N/A | n/a | Yes — `<a href="tel:">` |
| Auto-close after sent | n/a | Countdown bar (.ld-bar) shrinks right→left over 2 s | Dialog dismisses; page y unchanged; focus to opener | n/a | Bar disabled under `prefers-reduced-motion`; timer still fires — **INTER-03** | n/a | n/a |

## Dialog and Form State Coverage

| State | Implementation | Finding |
|---|---|---|
| Closed (fresh) | Page at original y; focus returned; history entry removed | Clean — y0=y1=y2 across all 19 CTAs, all viewports |
| Open — fresh | Form shown; `pf-name` focused on pointer:fine; `.ld-x` focused on touch | INTER-02 |
| Open — data-price CTA | "המחירון המלא" preset in interest select | Clean |
| Open — product window origin | Interest empty; product name (`ldCtx`) sent as interest fallback on submit | Clean |
| Sending — 3 s hold active | Button "שולח…", disabled; no HTTP request until `3050−performance.now()` elapses | INTER-06 |
| Sending — fetch in flight | Button still disabled; 15 s timeout guards against hung request | Clean |
| Error: missing_fields | Banner "חסרים פרטי חובה. בדקו שם, שם העסק, עיר וטלפון."; all fields kept; button re-enabled | INTER-04 |
| Error: bad_phone | Banner "מספר הטלפון לא נראה תקין…"; fields kept | Clean |
| Error: 502 / timeout / offline | Generic banner with WA + phone links; fields kept | Clean |
| Error: silent drop (was_new absent) | Same generic banner as 502 — correct (3 s hold prevents real-user hits) | Clean |
| Sent | Check-draw animation (0.45 s ease-out), "תודה רבה!", countdown bar 2 s, auto-close | Excellent |
| Sent — prefers-reduced-motion | Check static (stroke-dashoffset:0); bar animation none; timer still fires at 2 s | INTER-03 |
| Reopened after sent | Sent state shown; no re-fill possible | Correct |
| After auto-close | Page at original y; form in `#pf-slot` with `.sent` class; focus to opener | Clean |
| No-JS / deep link `#contact` | Scrolls to `#contact`; tel/WA/mail links visible (telOpacity:"1"); no dialog | Clean — `facts.noJs.ok:true` |
| History hygiene | pushState on open; `history.back()` on close-by-×/Esc/backdrop; NOT called when popstate triggers close (ldDoc guard prevents double-back) | Excellent |
| Focus trap | `tabLeftDialog: 0` on p390 and d1360 | Excellent |
| Page never moves | y0=y1=y2 across every CTA, every error reply, every close path | Excellent |

---

## interaction-design-specialist — brand site lead dialog and page

### Not applicable from my definition

`portal_ux_standard.md`, English-first/RTL-forbidden rules, Operational Precision tokens, shadcn/Tailwind components, and RUNTIME_READY gates do not apply; this is GT's public brand site, Hebrew RTL by Tom's approval, on a single static Shopify section.

### Motion assessment

All four animations are purposeful and compositor-friendly (transform + opacity only):

- **Sheet entrance** (`translateY(40px) opacity:0 → 0` in 0.32 s, cubic-bezier(.2,.8,.25,1)): communicates spatial origin correctly for a bottom sheet. Fast enough to feel snappy, slow enough to perceive.
- **Backdrop** (opacity fade 0.32 s ease): standard, unobtrusive.
- **Check draw** (stroke-dashoffset 40→0 in 0.45 s ease-out, 0.1 s delay): the delay lets the circle render first; ease-out gives a satisfying deceleration. Earns the success moment rather than decorating it.
- **Countdown bar** (scaleX 1→0 over 2 s linear, transform-origin:right): correct for RTL — the bar drains from its visual-end (left) toward its visual-start (right), leaving no ambiguity about the direction of time. Linear easing is correct for a timer.
- **Reduced-motion path** (`animation:none` for all four; `stroke-dashoffset:0` for check): complete. The one gap is that the 2 s auto-close timer fires regardless (INTER-03).

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact change) | Evidence |
|---|---|---|---|---|---|---|
| INTER-01 | P1 | M | Flavour card → product window → "הוסיפו לתפריט" → dialog close | When the lead dialog closes (×, Esc, backdrop, auto-close, back), the product window (fmodal) remains open. The `close` event handler returns focus to `ldCard` but never calls any fmodal close function. After a successful lead send and auto-close, the product window reappears in the foreground; visitor must close it manually before continuing to browse. | In `patch_lead_dialog.py`, inside the `close` listener at line 228, after the `if(ldAuto…)` reset block, add: `if(ldCtx&&window.closeF)window.closeF();` — `closeF` is the existing fmodal close function mirrored by the same hook pattern used for `openF`. | `patch_lead_dialog.py:227-235` — no fmodal close call; `ldCtx` is set on fmodal-origin opens (`:209`). Inferred: `facts.d1360.ctas[14-16].ok:true` but fmodal post-close state not measured in harness. |
| INTER-02 | P1 | S | Dialog open — touch devices (p320, p390, p430) | `showModal()` focuses the first focusable child, which is `.ld-x` (aria-label="סגירה"). A VoiceOver or TalkBack user hears "Close, button" before the dialog heading is announced. On pointer:fine (desktop), `pf-name` is focused explicitly; on touch, no explicit focus is set. | In `patch_lead_dialog.py` shell string (`:116`), add `tabindex="-1"` to the heading element: `<b id="ld-h" tabindex="-1">בקשת מחירון וטעימה</b>`. In `ldOpen` (`:223`), after `d.showModal();d.scrollTop=0;`, add: `if(!matchMedia('(pointer:fine)').matches)document.getElementById('ld-h').focus({preventScroll:true});`. The `tabindex=-1` allows programmatic focus without adding the heading to the tab sequence and without triggering the software keyboard. | `patch_lead_dialog.py:116` (shell, `.ld-x` is first focusable), `:222-223` (focus only for pointer:fine). `facts.p390.lead.open.focus="button"` vs `facts.d1360.lead.open.focus="input#pf-name"`. Handoff: accessibility-usability-auditor. |
| INTER-03 | P1 | S | Sent state — `prefers-reduced-motion: reduce` | `@media(prefers-reduced-motion:reduce)` disables `.ld-bar` animation (`animation:none`), leaving the visitor no visual indicator the dialog will auto-close. `setTimeout(ldClose, LD_CLOSE_MS)` fires unconditionally at 2 s. A screen reader user finishing the "תודה רבה!" announcement has the dialog dismissed before they complete processing, with no warning. | In `patch_lead_dialog.py`, at the success close block (`:300`), replace: `ldTimer=setTimeout(ldClose,LD_CLOSE_MS);` with: `var rm=matchMedia('(prefers-reduced-motion:reduce)').matches;ldTimer=setTimeout(ldClose,rm?6000:LD_CLOSE_MS);`. Additionally, inject a visually-hidden `<span role="status" id="ld-status"></span>` into the shell; on success set `document.getElementById('ld-status').textContent='הפרטים נשלחו. החלון ייסגר בעוד שתי שניות.'`. Copy text: handoff to ux-content-state-designer. | `patch_lead_dialog.py:194` (`animation:none` under reduced-motion), `:200` (`LD_CLOSE_MS=2000`, unconditional). `facts.p390.lead.reducedMotion="none"` — harness did not test reduced-motion path. |
| INTER-04 | P2 | S | Submit button — all states | `PF_LABEL = 'שליחה <span class="arr">←</span>'` is written via `innerHTML`. The `.arr` span has no `aria-hidden="true"`. Screen readers announce the decorative left-arrow character ("left-pointing arrow" or equivalent) as part of the button label, adding noise to the action announcement. | In `patch_form.py:179`, change to: `"var PF_LABEL='שליחה <span class=\"arr\" aria-hidden=\"true\">\\u2190</span>';\n"` | `patch_form.py:179` |
| INTER-05 | P2 | S | Form open — required fields | The four required fields (שם מלא, שם העסק, עיר, טלפון) carry `required` on their inputs but show no visual required-field indicator. The disclosure label uses "(לא חובה)" to imply others are mandatory, but this convention is indirect for a first-visit visitor who may not notice it before attempting to submit. | In `patch_lead_dialog.py` `FIELDS_NEW` (`:89`), inside each required label append `<span aria-hidden="true" class="pf-star"> ✱</span>` to the label text span. Add one CSS rule to the `CSS` constant: `.pf-star{color:var(--gt);font-size:10px;vertical-align:super}`. The `aria-hidden` keeps the indicator decorative; the `required` attribute handles the screen reader announcement. | `patch_lead_dialog.py:90-95` (four required labels, no marker). shot:`p390-lead-02-open.png` — labels visible, no indicator. |
| INTER-06 | P2 | S | "שליחה" → sending state on recently-loaded page | The 3 s hold is architecturally correct. On a cached mobile page where `performance.now()` is low at submit time, the hold can reach ~1–2 s of "שולח…" with no network activity. There is no UX differentiation between "preparing" and "actively sending", so the button may read as frozen. | In `patch_form.py`, modify the button-disable block: replace `btn.innerHTML='שולח\\u2026';` with two phases: set `btn.innerHTML='מכין…'` at disable time; inside the `setTimeout` callback, immediately before `fetch(…)`, set `btn.innerHTML='שולח…'`. One-line CSS addition to `patch_form.py` error style block: `.partner button[disabled][data-phase="sending"]{…}` if a data-phase attribute is used to style them differently. | `patch_lead_dialog.py:288-291` (setTimeout wraps fetch). `facts.p390.lead.fast`: tOpen=2019 ms, tSubmit=2326 ms, elapsed_ms=3050 ms — delay at submission was 724 ms of silent waiting. |

### World-class upgrades (beyond defects — what would make this the best lead flow in its category)

1. **Product-specific thank-you.** `ldCtx` already carries the product name when "הוסיפו לתפריט" is used. In the success block (`patch_lead_dialog.py:300`), check `ldCtx` and replace the generic heading text with "נשלח לך מחירון שכולל [ldCtx]!" — zero intake changes, one JS line, meaningfully more personal.

2. **WhatsApp with pre-filled context.** The current link `https://wa.me/972543982444` opens WhatsApp with an empty draft. Change it to `https://wa.me/972543982444?text=שלום%20GT%2C%20אני%20מעוניין%20לקבל%20מחירון` in `patch_form.py`. The sales team sees intent immediately; the visitor saves typing.

3. **Sticky × through disclosure-expanded scroll.** When "עוד פרטים" is open and the visitor scrolls down inside the sheet, the × button (`position:absolute;top:12px`) scrolls out of view. Change `.ld-x` to `position:sticky;top:12px;align-self:flex-start` inside the scrolling `#ldlg` container. One CSS rule in `patch_lead_dialog.py`; exit always reachable.

4. **Page-level post-close confirmation.** After the dialog auto-closes, the page is silent. Add a two-second toast (or change the triggering CTA label to "נשלח ✓" for 3 s) immediately after `ldClose()` completes. Gives the visitor page-level confirmation without requiring a scroll to `#contact`.

5. **`autocapitalize="words"` on שם מלא and שם העסק.** Android keyboard suggestions for name/business inputs work better with `autocapitalize="words"`. One attribute per input in `patch_lead_dialog.py:90-91`; iOS already capitalises by default.

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 — Phone, ad, slide CTA, send in ≤30 s | PASS | Dialog opens from slide instantly; preset saves a step; all 4 fields and consent visible without scrolling on p390 (`facts.fits` all true); submit button reachable. Under 30 s achievable. |
| V2 — Desktop, read products, catalogue CTA, send | PASS | 820 px split-panel dialog with bottle photo; 2-column required-field grid; interest preset. Clean. |
| V3 — Flavour card → product window → הוסיפו לתפריט → send | FRICTION | Send works; product name travels as interest fallback; lead stored. After dialog closes (success auto-close or ×), product window remains open and requires a second manual close — **INTER-01**. |
| V4 — Hesitant: open then leave by ×, Esc, backdrop, back | PASS | All four dismissal paths verified (`facts.d1360.ctas`: all 19 CTAs closed, y0=y1=y2, focusBack:true). Interest preset correctly reset. |
| V5 — Bad phone / network error / timeout / offline | PASS | Per-error copy shown; all values kept; button re-enabled; WA + phone links in error banner. `facts.d1360.replies.phone/e502/timeout/offline.ok:true`. |
| V6 — Already sent, tap another CTA | PASS | Reopened dialog shows sent state (`facts.d1360.replies.ok.reopenedSent:true`). WhatsApp + phone links visible. |
| V7 — Screen reader user | FRICTION | Initial focus on × not heading (**INTER-02**); 2 s auto-close fires with no announcement under reduced motion (**INTER-03**); decorative ← in button label unmasked (**INTER-04**). Core task completable but requires extra navigation and creates timing risk. |
| V8 — Keyboard-only desktop | PASS | All controls reachable; `tabLeftDialog:0`; × has `focus-visible` outline (`2px solid var(--gt)`); `<details>` keyboard-operable; Esc closes; Tab cycles inside dialog. |
| V9 — No JavaScript / slow network | PASS | `facts.d1360.lead.noJs.ok:true`; links scroll to `#contact`; tel/WA/mail links have full opacity. |
| V10 — Read whole page on phone | PASS | All sections readable on p390; 19 CTAs with 5 distinct labels noted for COPY dimension (label consistency across nav/hero/slides/catalogue/economics/closing). |

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 3 (INTER-01, INTER-02, INTER-03) | 3 (INTER-04, INTER-05, INTER-06) | AMBER — no P0; three P1s, two of which (INTER-02, INTER-03) are each ≤1 h fixes |

---

### Handoff packet

```yaml
handoff_packet:
  surface: gteveryday.com — lead dialog and inline form (preview_theme_id 186698334449)
  audit_date: 2026-09-27
  authored_by: interaction-design-specialist
  scope:
    - All 19 CTAs (nav, hero, 10 slides, catalogue, economics, closing, 3 flavour cards
      via product window → הוסיפו לתפריט)
    - Dialog close paths: ×, Esc, backdrop click, popstate (back button), auto-close
    - Form fields, עוד פרטים disclosure, consent checkbox, submit
    - All reply paths: ok, drop, missing_fields, bad_phone, e502, timeout, offline
    - Sent state and reopened-after-sent
    - No-JS and deep-link #contact paths
    - Reduced-motion path (CSS + JS analysis; not measured in harness — reducedMotion="none")
    - Motion: sheet entrance, backdrop, check-draw, countdown bar
    - Viewports: p320, p390, p430, t768, i744, i820, i1024, li1180, li1366, d1360, d1920
  contracts_inspected:
    - gt-site/tools/patch_lead_dialog.py
    - gt-site/tools/patch_form.py
    - /tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r1/site-ipad/site_ipad_facts.json
  action_review:
    - action: "All 19 CTAs (a[href='#contact'])"
      label: present
      disabled_state: defined (always enabled)
      loading_state: n/a
      destructive: no
      irreversible: no
      confirmation: not required
      post_action: defined (dialog opens)
      error_state: n/a
      finding_id: INTER-01 (product window path only)
    - action: "Close × button"
      label: present (aria-label="סגירה")
      disabled_state: defined
      loading_state: n/a
      destructive: no
      irreversible: no
      confirmation: not required
      post_action: defined (page y, focus return, history back)
      error_state: n/a
      finding_id: none
    - action: "שליחה submit"
      label: present
      disabled_state: defined (during send)
      loading_state: defined (שולח…)
      destructive: no
      irreversible: no
      confirmation: not required
      post_action: defined (error or success + auto-close)
      error_state: defined (per-type banners)
      finding_id: INTER-04 (aria-hidden), INTER-06 (3 s perceptual hold)
    - action: "Auto-close after sent"
      label: n/a
      disabled_state: n/a
      loading_state: defined (countdown bar)
      destructive: no
      irreversible: no
      confirmation: not required
      post_action: defined
      error_state: n/a
      finding_id: INTER-03
  findings:
    - id: INTER-01
      class: FLOW_COMPLETION
      location: patch_lead_dialog.py:227-235
      description: Product window (fmodal) stays open when lead dialog closes
      proposed_fix: Call closeF() in dialog close handler when ldCtx is set
      acceptance_criterion: >
        After V3 path completes (send or cancel), the product window is also dismissed;
        page returns to scrollable state with no residual layer requiring manual close.
    - id: INTER-02
      class: FLOW_COMPLETION
      location: patch_lead_dialog.py:116, 222-223
      description: >
        Initial focus lands on × button (not dialog heading) on touch devices;
        screen reader users hear "Close" before form context.
      proposed_fix: tabindex="-1" on ld-h; programmatic focus to ld-h on non-pointer:fine open
      acceptance_criterion: >
        TalkBack/VoiceOver announces dialog heading ("בקשת מחירון וטעימה") immediately on
        open on touch devices; software keyboard does not appear.
    - id: INTER-03
      class: FLOW_COMPLETION
      location: patch_lead_dialog.py:194, 200
      description: >
        Auto-close fires at 2 s for prefers-reduced-motion users with no countdown indicator
        or aria announcement; dialog dismisses mid-announcement on screen readers.
      proposed_fix: >
        Increase LD_CLOSE_MS to 6000 for reduced-motion users; add role="status" announcement
        on success.
      acceptance_criterion: >
        Under prefers-reduced-motion, visitor has ≥5 s to process the success state before
        auto-close; screen reader announces impending dismissal.
    - id: INTER-04
      class: POLISH_ACCELERATION
      location: patch_form.py:179
      description: Decorative arrow ← in submit button label not aria-hidden
      proposed_fix: aria-hidden="true" on .arr span
      acceptance_criterion: Screen reader announces "שליחה" only; no arrow character announced.
    - id: INTER-05
      class: POLISH_ACCELERATION
      location: patch_lead_dialog.py:90-95
      description: No visual required-field indicator on the four required fields
      proposed_fix: Aria-hidden ✱ marker on required label spans; one CSS rule
      acceptance_criterion: >
        Required fields display a visible marker; screen readers rely on the existing
        required attribute, not the marker.
    - id: INTER-06
      class: POLISH_ACCELERATION
      location: patch_lead_dialog.py:288-291
      description: >
        3 s hold shows "שולח…" with no network activity — perceptual freeze on
        fast-cached pages; no differentiation between preparing and sending phases.
      proposed_fix: Two-phase button label (מכין… then שולח…); aria-live status span
      acceptance_criterion: >
        Visitor perceives forward progress; "מכין…" visible during hold, "שולח…"
        only after fetch starts.
  copy_handoff_to: ux-content-state-designer
  a11y_handoff_to: accessibility-usability-auditor
  tom_approval_required: no
```

### Escalations

None. All six findings are addressable within `patch_lead_dialog.py` or `patch_form.py`. No new backend endpoint, status enum, intake contract change, or schema change is required.
