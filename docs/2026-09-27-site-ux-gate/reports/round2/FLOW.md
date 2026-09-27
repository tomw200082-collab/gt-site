## ux-flow-architect — brand site lead dialog and page (round 2)

### Not applicable from my definition
`portal_ux_standard.md`, English-first / LTR, RUNTIME_READY, shadcn/Tailwind, and operator-task-simulation framing do not apply; this is gteveryday.com, Hebrew RTL public brand site, visitor-task-simulation throughout.

---

### Round-1 findings

| ID | Status | Evidence |
|---|---|---|
| FLOW-01 | FIXED | No `LD_CLOSE_MS` variable or auto-close timer exists in `tools/patch_lead_dialog.py`. Docstring explicitly: "It does not close on a timer: two seconds cut the thanks off for a screen reader." `p390.replies.ok.stayedOpen:true`, `openWhileAway:true`, `closedOnReturn:true`. §9.2 confirms it. |
| FLOW-02 | OPEN | `d1360.ctas[f-detox].interest:''`; the `ldCtx` fallback still carries the product name silently at send time but nothing is shown to the visitor confirming capture. With the new three-step flow (ask → form → send), the product context is one step further removed from the trigger. Unchanged. P2, M. |
| FLOW-03 | FIXED | i18n diff: all five old label variants (`רוצים להתחיל`, `אני מעוניין`, `רוצה מחירון`, `לקבלת הקטלוג המלא`, `רוצה מחירון ותמחירים`) replaced by `בואו נעבוד יחד` (page CTAs) and `הוסיפו לתפריט` (slides). CTA facts confirm: `d1360.ctas[*].label` is uniformly `בואו נעבוד יחד ←` or `הוסיפו לתפריט`. §9.2 confirms it. |
| FLOW-04 | OPEN | `p390.page.text[5]` (TEA 2.0) and `p390.page.text[6]` (operations "מגישים בארבעה צעדים") contain no CTA. Next unconditional CTA is `div.bigcta` at `p390.page.text[11]` — five section scrolls later. Not addressed in round 2. §9.3 defers all P2s to the report. P2, S. |

---

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + change) | Evidence |
|---|---|---|---|---|---|---|
| FLOW-02 | P2 | M | dialog / form step (V3 path) | When the product window's `הוסיפו לתפריט` CTA opens the dialog, the form advances through ask → yes → form. The product name (`ldCtx`, captured from `fm-name` at open time) is silently carried to the send body via `interest:g('pf-int')||ldCtx`, but nothing visible confirms to the visitor that the product context is captured. The optional interest select in `<details>` is empty; the three steps between product-window tap and send deepen the disconnect. | In `ldOpen()` in `tools/patch_lead_dialog.py` (after the `ldCtx` assignment near line 265), when `ldCtx` is non-empty inject a small kicker line into `.pf-head` beneath the heading: only while the dialog is open from a product or slide CTA, remove on `ldClose()`. Route exact copy and styling to COPY and VISUAL dimensions. | `tools/patch_lead_dialog.py:265` (`ldCtx=fm?…fm-name…:sl?…hs-h…:'';`); `d1360.ctas[f-detox].interest:''`; `d1360.replies.ok.body.interest:''` (no product context in sent body when interest select is left empty — ldCtx applies only if `#pf-int` is blank, which it is by default) |
| FLOW-04 | P2 | S | page / scroll funnel (V10) | Sections TEA 2.0 (`p390.page.text[5]`) and operations — "מגישים בארבעה צעדים" (`p390.page.text[6]`) — carry high conviction copy but no conversion link. The next unconditional CTA (`div.bigcta`) is five section-heights below. A visitor persuaded by "כל ברמן מוזג GT מושלם כבר ביום הראשון" must scroll past matcha cards, purees cards, tools, and the about section before finding the next `בואו נעבוד יחד`. The matcha and purees sections have two-step flavour-card paths, not a direct link. | Add `<a class="sub-cta" href="#contact" data-cta="ops">בואו נעבוד יחד ←</a>` immediately after the four-step operations block in the relevant `gt-site/i18n/parts/he_visible_*.py` file (the block ending "מגישים, מערבבים, מקשטים, מצלמים."). Style is the existing `.sub-cta` rule used on the slides. | `p390.page.text[6]`: "תפעול מגישים בארבעה צעדים…" — no CTA text; `p390.page.text[11]`: "div.bigcta: … בואו נעבוד יחד ←" (next CTA, five sections later) |

---

### New steps — round-2 audit (§9.1)

**Wholesale clarity at entry.** The business question opens every dialog: bold `יש לכם עסק?` with subtitle `אנחנו עובדים רק עם עסקים, בסיטונאות.` at the very first screen of the sheet. `p390.lead.open.step:'ask'`, `focus:'p#pf-ask-q'`. A café owner reads the qualification instantly; no ambiguity about B2B-only. PASS.

**Private buyer path (V11).** `steps.stepNo:'priv'` → private screen shows `אנחנו עובדים רק עם עסקים.` (bold) + `ללקוחות פרטיים, המוצרים שלנו נמכרים באתר של אליטה אופק.` + "למוצרי GT אצל אליטה אופק ←" (correct href, `blank:true`) + `חזרה` button (`min-height:44px`). `steps.sends:0` — nothing reaches sales. `steps.stepBack:'ask'` — "חזרה" returns to the question, no dead end. `steps.axePrivate:[]`. `steps.y2===steps.y0`. PASS.

**Sent step and WhatsApp (V12).** After a successful send: `replies.ok.focusSent:'p#pf-pick-q'` (screen reader announces "מה הכי מעניין אתכם?"); five lines render at `h:52px` (adequate touch target); each is `blank:true`; each carries the correct pre-written message (`היי, אני מעוניין ב<line>`); all link to `https://wa.me/972547588132`. `replies.ok.stayedOpen:true` while visitor is on WhatsApp; `closedOnReturn:true` and `y2===y0` on return. `reopenedSent:true` — a second CTA tap after send reopens to the thanks + five lines without auto-close. PASS.

**Answer held for the visit.** `steps.stepReopen:'form'` — after answering yes and submitting, reopening any CTA shows the form directly, skipping the business question. Saves one tap for the common case of a returning visitor. PASS.

**Five lines as labels.** The five lines — מאצ׳ה, אובה, צ׳אי מסאלה, תמציות תה, בניית תפריט משקאות בעסק שלי — map unambiguously to the four product lines that appear in the hero slides (and have or will have landing pages) and the menu-building service. The fifth (`בניית תפריט משקאות בעסק שלי`) is full-width in the grid (`pf-wide` class), visually differentiated as a service rather than a product. Labels are clear and decision-grade.

**One voice: page CTA → dialog heading → first question.** Page CTAs say `בואו נעבוד יחד`; the dialog heading repeats it verbatim; the first question `יש לכם עסק?` is a natural qualification step under that invitation. The transition from `הוסיפו לתפריט` (slide/product CTA) to `בואו נעבוד יחד` (dialog heading) is a mild register shift — product interest to partnership framing — but it is deliberate per §9.1 item 5 and the COPY dimension holds the words. No flow gap.

**V1 tap count (round 2, p390).** CTA tap + `כן, יש לי עסק` + 4 fields + consent + send = 8 taps (vs. 7 in round 1). Autofill: 4 taps (CTA + yes + consent + send). `fits.send:true`, `fits.pf-name/venue/city/phone/agree:true` — all required elements visible without scroll after saying yes. Manual: ~24 s. Autofill: ~7 s. Target ≤30 s met with margin. PASS.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 — Phone, ad, hero CTA, send, scroll on. ≤30 s, one-handed. | PASS | 8 taps (was 7). Hero CTA opens ask step; `כן, יש לי עסק` reaches form; all fields above fold; consent + send visible. ~24 s manual. |
| V2 — Desktop, read products, catalogue CTA, send. | PASS | CTA now `בואו נעבוד יחד`; ask step adds one tap; d1360 card 820 px centred with photo. Clean. |
| V3 — Flavour card → product window → `הוסיפו לתפריט` → send. Lead carries product. | PASS with friction | Dialog opens ask step; product name travels via `ldCtx` at send; visitor has no visual confirmation the product context is captured (FLOW-02). |
| V4 — Open, dismiss via ×, Esc, backdrop, phone back-button. Nothing lost, page where it was. | PASS | All 19 CTAs: `closed:true`, `closedBy` cycles x/esc/backdrop; `popstate` closes on back; `y2===y0` for all; typed values survive (kept). |
| V5 — Bad phone, network error, timeout, offline. Understand, recover or WhatsApp. | PASS | All states: `kept:true`, dialog open, WhatsApp + phone fallback visible. Error messages distinct and actionable. |
| V6 — Already sent: tap another CTA, see sent state, see five lines. | PASS | `reopenedSent:true` on p390 and d1360. Sent state with five lines; no auto-close on reopen. |
| V7 — Hebrew screen-reader user: open, fill, send, hear result, focus returns. | PASS (inferred structural) | `axe:[]` dialog; `aria-labelledby="ld-h"` on `#ldlg`; focus: ask-q → (yes) → ld-h / pf-name → pf-pick-q on send; `tabLeftDialog:0`. iOS VoiceOver `<dialog>` behaviour remains inferred — Chromium-only harness per §5. |
| V8 — Keyboard only, desktop. | PASS | In ask step: × → כן button → לא button → × (wrap). After yes: × → pf-name → venue → city → phone → details summary → consent → send → WhatsApp → phone → ×. `tabLeftDialog:0`. Esc closes. |
| V9 — No JavaScript / slow network. | PASS | `noJs.dialogOpen:false`, `noJs.asks:false` (full form shown, no gating), `noJs.fieldsShown:true`, `noJs.telOpacity:'1'`. All 19 links scroll to `#contact`; full contact block visible. |
| V10 — Read whole page on phone: offer, trust, clarity, one voice. | PASS with note | First screen clear: "עידן חדש של משקאות בבית העסק שלכם." + `בואו נעבוד יחד ←` above fold. Voice is unified. FRICTION: sections TEA 2.0 and operations have no CTA (FLOW-04). |
| V11 — Private buyer: answers no, reaches Elita Ofek, nothing sent. | PASS | `steps.stepNo:'priv'`; shop link correct and blank; `steps.sends:0`; `חזרה` returns to ask; no dead end; `steps.axePrivate:[]`. |
| V12 — After send: pick a line, WhatsApp with message pre-written; return, dialog gone, page where it was. | PASS | `replies.ok.stayedOpen:true`; `openWhileAway:true`; `closedOnReturn:true`; `y2===y0:6904` (p390); all five lines correct target and message; `blank:true`. |

---

### World-class upgrades (beyond defects)

1. **Haptic on `was_new` confirmation**: `if(navigator.vibrate)navigator.vibrate([40])` after the sent class is applied in `tools/patch_lead_dialog.py`. One short buzz when the lead lands. Zero layout cost, graceful no-op on iOS, exactly right for a kitchen Android.

2. **Autofill pre-scan on open**: A 150 ms `setTimeout` after `showModal()` in `ldOpen()` checks whether `#pf-name` already has a browser-autofill value and applies a subtle green ring to pre-filled fields. Collapses the form to consent + send for returning visitors.

3. **Slide-specific kicker in the heading**: `ldCtx` already holds the slide's collection name. Show it as a small eyebrow above `בואו נעבוד יחד` in the dialog heading when the dialog is opened from a slide CTA — "אייס מאצ׳ה" above the heading. Source: `sl.querySelector('.hs-h').textContent`. Personalises the dialog to the exact drink.

4. **Named responder in the thanks**: Replace the generic "ונחזור אליכם" with a named person ("ענת תחזור אליכם") if GT has a consistent first responder. A human name on the promise increases call-back trust materially. Requires Tom's sign-off.

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 0 | 2 | GREEN — no P0, no P1 (the round-1 P1, FLOW-01, is fixed); 2 deferred P2s carried from round 1 |

The three-step flow (ask → form → lines) is implemented correctly: the business question gates private buyers cleanly, the five lines lead to WhatsApp with pre-written messages, the dialog stays open while the visitor is away and closes cleanly on return, the page never moves across all 19 CTAs, and all required-field visibility, focus, and tab-trap checks pass. The two remaining open findings (FLOW-02: product context not shown; FLOW-04: funnel gap after operations section) are both P2 and carry from round 1 unchanged.
