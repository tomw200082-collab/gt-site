## interaction-design-specialist — brand site lead dialog and page (round 2)

### Not applicable from my definition

`portal_ux_standard.md`, English-first/RTL-forbidden rules, Operational Precision tokens, shadcn/Tailwind components, and RUNTIME_READY gates do not apply; this is GT's public brand site, Hebrew RTL by Tom's approval, on a single static Shopify section.

---

### Round-1 findings

| ID | Status | Evidence |
|---|---|---|
| INTER-01 (P1) — product window stays open after dialog close | **FIXED** | `fmodalAfter: False` on all 19 CTAs, including the three card CTAs (14, 15, 16) and the fmodal CTA (18) in `site_ipad_facts.json` (both p390 and d1360). The `onclick=` on the product window link was always closing fmodal before `ldOpen()` ran; BRIEF §9.3 confirms it was never reproduced. |
| INTER-02 (P1) — initial focus lands on × on touch | **FIXED** | `ldStep()` function added in `patch_lead_dialog.py` (JS section). On open, focus goes to the step's question: `focusOnOpen: 'p#pf-ask-q'` on p390; `focusYes: 'b#ld-h'` (touch) / `input#pf-name` (pointer:fine). The × button is no longer the first focus target on any step. |
| INTER-03 (P1) — auto-close fires at 2 s under reduced motion | **FIXED** | `LD_CLOSE_MS`, `ldTimer`, `ldAuto`, and the entire `.ld-bar`/`.closing` countdown mechanism are removed in the round-2 diff. The dialog now stays open after a send and closes when the visitor returns from WhatsApp (`closedOnReturn: True` on both viewports). Reduced-motion users have no auto-dismiss. |
| INTER-04 (P2) — decorative ← in submit button not aria-hidden | **FIXED** | Listed in BRIEF §9.2 as fixed. The `patch_form.py` diff (index `4fd70f8..2f3240c`) includes this fix. The `.arr` span in the button's `innerHTML` now carries `aria-hidden="true"`. |
| INTER-05 (P2) — no visual required-field indicator | **OPEN** | BRIEF §9.3: "P2s not listed in §9.2 deferred to the report." No ✱ or asterisk marker visible on שם מלא, שם העסק, עיר, or טלפון labels in `p390-lead-02b-form.png`. The four `<label class="pf-f">` spans in `patch_lead_dialog.py:99-102` carry no marker. |
| INTER-06 (P2) — 3 s hold shows "שולח…" with no network activity | **OPEN** | Same reason. `fast: {tOpen:2028, tSubmit:2338, elapsed_ms:3050}` on p390 — the gap between submit click and actual fetch is still ~712 ms. The button reads "שולח…" with no visible network progress during that window. |

---

### Findings

#### [INTER-05] No visual required-field indicator on the four required fields

- **Class:** POLISH_ACCELERATION
- **Sev / Effort:** P2 / S
- **Surface / state:** Form step (after "כן, יש לי עסק"), all viewports
- **Finding:** The four required labels — שם מלא, שם העסק, עיר, טלפון — are bold-weighted but carry no visual required marker. The "(לא חובה)" label on the disclosure implies others are required, but this is an indirect convention. A first-visit visitor does not know which fields are required until they hit a submit error. The `required` attribute is present on the inputs; no visual complement exists.
- **Proposed fix:** In `patch_lead_dialog.py`, in `FIELDS_NEW` (lines 99–102), append `<span aria-hidden="true" class="pf-star"> ✱</span>` inside each of the four required `<label class="pf-f"><span>…` label spans. Add one CSS rule to the `CSS` constant: `.pf-star{color:var(--gt);font-size:10px;vertical-align:super}`. The `aria-hidden="true"` keeps the marker decorative; the existing `required` attribute handles the screen-reader announcement.
- **Acceptance criterion:** All four required fields display a visible ✱ marker; screen readers do not announce it; the marker does not appear on the optional fields inside `<details>`.
- **Evidence:** `patch_lead_dialog.py:99-102`; shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-02b-form.png`

---

#### [INTER-06] 3 s hold renders the submit button unresponsive on fast-cached pages

- **Class:** POLISH_ACCELERATION
- **Sev / Effort:** P2 / S
- **Surface / state:** "שליחה" button — sending state, any viewport where the page loaded recently
- **Finding:** The intake silently drops submissions with `elapsed_ms < 3000`, so the sender correctly holds the fetch until 3 050 ms past navigation start. When the visitor submits soon after page load, the button becomes disabled and shows "שולח…" while no network request is in flight. On p390 the measured hold was 712 ms (`tSubmit: 2338`, `elapsed_ms: 3050`). The visitor sees no differentiation between "preparing" and "actively sending." On a slow Android this reads as a frozen button.
- **Proposed fix:** In `patch_form.py`, at the send start block, set `btn.innerHTML='מכין…'` at disable time. Inside the `setTimeout` callback, immediately before `fetch(…)`, set `btn.innerHTML='שולח…'`. The copy text is for the content-state-designer to review; the mechanism is a two-phase label. No intake change is needed.
- **Acceptance criterion:** The visitor sees "מכין…" during the hold period and "שולח…" only while the fetch is in flight.
- **Evidence:** `patch_lead_dialog.py:351-361` (setTimeout wrapping fetch); `site_ipad_facts.json` p390: `fast.tOpen=2028, fast.tSubmit=2338, fast.elapsed_ms=3050`.

---

#### [INTER-R2-01] No `:active` tap feedback on the five interest line links and the "חזרה" button

- **Class:** POLISH_ACCELERATION
- **Sev / Effort:** P2 / S
- **Surface / state:** Sent state (five line links) and private-buyer step ("חזרה" back button)
- **Finding:** The "yes/no" answer buttons use `.btn` and receive `transform:scale(.98)` on `:active` — a tap confirmation consistent with every other button on the page. The five interest links (`.pf-lines a`) and the "חזרה" button (`.pf-back`) have no `:active` style. On mobile touch — the primary device for this audience — there is no visual confirmation that a tap has registered. For the WhatsApp links this matters most: the visitor taps a line and the dialog hangs open (by design, waiting for the `visibilitychange` return), so the absence of tap feedback for ~200–400 ms before WhatsApp opens could read as a frozen link.
- **Proposed fix:** In `patch_lead_dialog.py` in the `CSS` constant, add two rules: `.partner .pf-lines a:active{transform:scale(.97);transition:none}` and `.partner .pf-back:active{opacity:.7}`. The `transition:none` override cancels the `box-shadow .2s` delay so the tap feedback is instant. These are one-line additions to the `.partner .pf-lines a` and `.pf-back` blocks.
- **Acceptance criterion:** A tap on any interest line pill shows a brief scale-down. A tap on "חזרה" shows a brief opacity change. Both are imperceptible to hover/mouse users.
- **Evidence:** `patch_lead_dialog.py:193-194` (`.pf-lines a` block, no `:active`), `patch_lead_dialog.py:191` (`.pf-back` block, no `:active`); shot: `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/p390-lead-04-sent.png`.

---

### New steps — interaction review (BRIEF §9.1 controls)

**"כן, יש לי עסק" / "לא, לשימוש פרטי" buttons (ask step):**
All states clean. `ask: [{h:52,shown:True},{h:52,shown:True}]` — both 52 px tall, above the 44 px minimum. Focus goes to `pf-ask-q` on open across all viewports (`focusOnOpen: 'p#pf-ask-q'`). The primary/secondary visual split (filled dark vs. outline) correctly weights the intended path. Active state inherited from `.btn`. Keyboard reachable by Tab inside the dialog; Space/Enter activates. No loading state needed (instant step transition). `sends: 0` confirms the question step sends nothing. Clean.

**"לא, לשימוש פרטי" → private-buyer step:**
`focusNo: 'p#pf-priv-q'` ✓. "Elita Ofek" link: `blank:True`, correct URL, `rel="noopener"` ✓. "חזרה": `data-biz=""` triggers `f.classList.add('ask')` correctly — returns to ask step, `stepBack: 'ask'` ✓. `axePrivate: []` ✓. The dialog does not close when the visitor opens Elita Ofek (no `visibilitychange` listener is registered for that link — only for the WhatsApp lines). This is intentional and acceptable: the × remains reachable on return. The `:active` tap feedback gap on "חזרה" is INTER-R2-01.

**"כן, יש לי עסק" → form step:**
`stepYes: 'form'`, `focusYes: 'b#ld-h'` (touch) / `input#pf-name` (pointer:fine). Focus on the heading on touch prevents the software keyboard from appearing unprompted. All four required fields visible without scrolling (`fits: all true`). Clean.

**The five interest lines (sent step):**
`focusSent: 'p#pf-pick-q'` ✓. All five links open `wa.me/972547588132` with `היי, אני מעוניין ב…` pre-written — correct per BRIEF §9.1 item 3. `role="group" aria-labelledby="pf-pick-q"` on the container ✓. Each link is 52 px tall ✓. Hover/focus-visible ring at `inset 0 0 0 2px var(--gt)` ✓. Missing `:active` — INTER-R2-01. "בניית תפריט משקאות בעסק שלי" spans full width (`grid-column:1/-1`) — correct per §9.1 item 3.

**Dialog height between steps:**
Desktop (≥880 px): `min-height:min(520px,92dvh)` with `flex-direction:column;justify-content:center` on `.ld-main` — the card holds its height across all three steps; short steps are vertically centred. No height jump on desktop. Confirmed in `d1360-lead-02-open.png` and `d1360-lead-04-sent.png` (card height identical).
Mobile: bottom sheet is content-driven; the ask step is shorter (~40% of viewport height, `p390-lead-02-open.png`) and the form step is taller (~60%, `p390-lead-02b-form.png`). The expansion when answering "yes" is instant (`transition:none`). This is expected bottom-sheet behaviour; noted as a world-class upgrade candidate.

**Close on return (`openWhileAway`, `closedOnReturn`):**
`openWhileAway: True` ✓ — dialog remains open while the visitor is on WhatsApp.
`closedOnReturn: True` ✓ — `visibilitychange` fires on return, `ldClose()` runs, history entry is stepped back, focus returns to the opener (`focusBack: True`), page is at original y (`y2=y0`).

**Visitor never leaves:**
The dialog stays open with the check + thanks + five lines. The × button (44 × 44 px, `aria-label="סגירה"`, `focus-visible` ring), Esc, backdrop click, and popstate all close it. No auto-close timer. After manual close, the form carries `.sent`; next open shows the sent state. Clean.

**Visitor picks twice:**
Two `visibilitychange` listeners accumulate. On first return, listener 1 calls `ldClose()`, removes itself. Listener 2 remains but fires `ldClose()` as a no-op (dialog already closed) on the next visibility change. No user-visible bug. `leadsAfter: 1` — no double-send.

---

### V11 and V12

**V11 — private buyer:**
`stepNo: 'priv'`, `focusNo: 'p#pf-priv-q'`, shop link `blank: True`, correct URL, `sends: 0`, `stepBack: 'ask'`, `axePrivate: []`. Visitor can reach Elita Ofek in two taps; nothing reaches the sales queue. PASS.

**V12 — pick a line, return:**
`stayedOpen: True`, `closedOnReturn: True`, `y2=y0`, `focusBack: True`, `leadsAfter: 1`. Pre-filled WhatsApp messages confirmed for all five lines. Dialog gone when visitor returns, page where it was. PASS.

---

### V1 and V6 as they run now

**V1 (phone, ad, one-handed):**
Dialog opens at ask step — `focusOnOpen: 'p#pf-ask-q'`, no keyboard popup. One extra tap ("כן") versus round 1. After "yes", focus goes to `ld-h` (touch), fields visible, `fits: all true`. V1 under 30 s remains achievable. PASS.

**V6 (already sent, tap another CTA):**
`reopenedSent: True` — dialog reopens to the sent state (check + thanks + five lines). Focus goes to `pf-pick-q` (`focusSent: 'p#pf-pick-q'`). The WhatsApp lines are available. The business question is not re-asked. PASS.

---

### World-class upgrades

1. **Smooth bottom-sheet expansion on "yes".** On phones, the sheet jumps from ~40% to ~60% of viewport height when the visitor answers "yes". A `max-height` transition on `#ldlg` (e.g., `max-height:92dvh; transition:max-height .3s cubic-bezier(.2,.8,.25,1)`) would soften this. Requires careful interaction with `overflow:auto` and safe-area padding. M effort.

2. **Product-specific "מה הכי מעניין אתכם?" heading.** `ldCtx` already carries the product name or slide collection. In the success handler, use it to personalise the pick heading: `"מה הכי מעניין אתכם מ[ldCtx]?"` when `ldCtx` is non-empty. Zero intake changes; one JS line in `patch_lead_dialog.py`. S effort.

3. **"חזרה" focus-visible ring.** The `.pf-back` button has no `:focus-visible` rule. Add `.partner .pf-back:focus-visible{outline:2px solid var(--gt);outline-offset:3px;border-radius:4px}` in the CSS constant. S effort. (Full handoff: accessibility-usability-auditor.)

4. **Page-level post-close confirmation for keyboard/screen-reader users.** After `ldClose()`, the page is silent. A `role="status"` region announcing "הפנייה נשלחה" for 3 s would close the feedback loop for users who cannot see the sent-state check. S effort. (Content: ux-content-state-designer.)

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 — Phone, ad, slide CTA, send in ≤30 s | PASS | Business question adds ~1 s; still under 30 s. All fields on screen. Focus managed. |
| V2 — Desktop, read products, catalogue CTA, send | PASS | Ask step → form; 2-column layout; product photo panel; all clean. |
| V3 — Flavour card → product window → הוסיפו לתפריט → send | PASS | `fmodalAfter: False` on all card CTAs; product window closes before dialog opens. Lead carries product name via `ldCtx`. |
| V4 — Hesitant: open then leave by ×, Esc, backdrop, back | PASS | All four paths tested; `y0=y1=y2`, `focusBack: True`, no dangling history entries. |
| V5 — Bad phone / network error / timeout / offline | PASS | Per-error Hebrew copy; values kept; button re-enabled; WA + phone links in banner. All `replies.*.ok: True`. |
| V6 — Already sent, tap another CTA | PASS | `reopenedSent: True`; sent state shown; WhatsApp lines available; business question not re-asked. |
| V7 — Hebrew screen-reader user | FRICTION | `.pf-back` has no `:focus-visible` ring (handoff: accessibility-usability-auditor). Core task completable. |
| V8 — Keyboard only, desktop | PASS | `tabLeftDialog: 0`; all new controls (ask/priv buttons, back, five lines) reachable by Tab; Esc closes. |
| V9 — No JavaScript | PASS | `noJs.ok: True`; page scrolls to `#contact`; tel/WA/mail links visible. |
| V10 — Read whole page on phone | PASS | Unified label "בואו נעבוד יחד" across nav/hero/catalogue/economics/closing. Slide CTAs unified to "הוסיפו לתפריט". One voice. |
| V11 — Private buyer | PASS | Shop link correct and opens new tab; `sends: 0`; back path returns to ask. |
| V12 — After send, pick a line, return | PASS | `closedOnReturn: True`; page at original y; focus returned. |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 0 | 3 (INTER-05, INTER-06, INTER-R2-01) | **GREEN** — no P0, no P1; three P2 polish items all ≤1 h fixes |

---

### Handoff packet

```yaml
handoff_packet:
  surface: gteveryday.com — lead dialog, step controls, and interest lines
  audit_date: 2026-09-27
  round: 2
  authored_by: interaction-design-specialist
  scope:
    - All 19 CTAs across nav / hero / slides / catalogue / economics / closing / product window
    - New ask step (two buttons), private-buyer step (Elita Ofek link + חזרה back button)
    - Form step (after yes), five interest line links (sent state)
    - Close paths: ×, Esc, backdrop, popstate, visibilitychange (WhatsApp return)
    - Height between steps (desktop vs. mobile), open-while-away, closed-on-return
    - Picking twice, picking and never leaving
    - V1 with ask step, V6 reopened-sent, V11 private buyer, V12 line pick + return
  contracts_inspected:
    - /home/user/gt-site/tools/patch_lead_dialog.py (current)
    - /home/user/gt-site/tools/patch_form.py (diff 1a276ec→8cf918d)
    - /tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/site_ipad_facts.json
  portal_tip: 8cf918d
  findings_open:
    - id: INTER-05
      class: POLISH_ACCELERATION
      sev: P2
      effort: S
      location: patch_lead_dialog.py:99-102
      description: No visual required-field indicator on the four required labels
      proposed_fix: aria-hidden ✱ span on each required label; one CSS rule .pf-star
      acceptance_criterion: >
        ✱ visible on שם מלא, שם העסק, עיר, טלפון; absent from optional fields;
        screen reader does not announce it.
    - id: INTER-06
      class: POLISH_ACCELERATION
      sev: P2
      effort: S
      location: patch_lead_dialog.py:351-361 (setTimeout wrapping fetch)
      description: >
        3 s hold shows "שולח…" with no network activity; perceptual freeze on
        fast-cached pages.
      proposed_fix: Two-phase button label (מכין… during hold, שולח… when fetch starts)
      acceptance_criterion: >
        Visitor sees "מכין…" during the 3 s hold; "שולח…" only while fetch is in flight.
    - id: INTER-R2-01
      class: POLISH_ACCELERATION
      sev: P2
      effort: S
      location: patch_lead_dialog.py:193-194, 191 (CSS for .pf-lines a and .pf-back)
      description: No :active tap feedback on the five interest line links or "חזרה" button
      proposed_fix: >
        .partner .pf-lines a:active{transform:scale(.97);transition:none}
        .partner .pf-back:active{opacity:.7}
      acceptance_criterion: >
        Tapping any interest line pill shows brief scale-down; tapping חזרה shows
        brief opacity change; no effect on hover/mouse.
  findings_fixed_this_round:
    - INTER-01 (product window stays open): fmodalAfter:false confirmed, never reproduced
    - INTER-02 (focus on × on touch): ldStep() focuses step question on open
    - INTER-03 (auto-close fires under reduced motion): timer and bar removed entirely
    - INTER-04 (arrow not aria-hidden): fixed in patch_form.py per BRIEF §9.2
  copy_handoff_to: ux-content-state-designer
  a11y_handoff_to: accessibility-usability-auditor (pf-back focus-visible ring)
  tom_approval_required: no
```

### Escalations

None. All three open findings are addressable within `patch_lead_dialog.py` or `patch_form.py`. No new backend endpoint, status enum, intake contract change, or schema change is required.
