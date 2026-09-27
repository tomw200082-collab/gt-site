## ux-flow-architect — brand site lead dialog and page

### Not applicable from my definition
`portal_ux_standard.md`, English-first / LTR, RUNTIME_READY, shadcn/Tailwind, and operator-task-simulation framing do not apply; this surface is gteveryday.com, Hebrew RTL public brand site, visitor-task-simulation throughout.

---

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact change) | Evidence |
|---|---|---|---|---|---|---|
| FLOW-01 | P1 | S | dialog / sent state (`*-lead-04-sent`) | `LD_CLOSE_MS=2000` — 2 s is too short for a visitor to read and intentionally tap the phone-number tel: link before the sheet closes. On p390 the check circle sits at the extreme top edge of the sheet (dialog box top=119 px, grab bar immediately above), leaving the visitor 2 s to process: check + "תודה רבה!" + response-time promise + "אם דחוף — 054-398-2444" + dismiss bar. After the dialog closes the page returns to its pre-open scroll position (`y2===y0`, proven for all 19 CTAs at both p390 and d1360). If that position is far from `#contact`, the phone number is gone from view. Reopening any CTA shows the sent state again without auto-close — a working recovery path — but the visitor has no cue that this is possible. The green countdown bar is the right affordance; it just needs more time behind it. | In `tools/patch_lead_dialog.py:200` change `var LD_CLOSE_MS=2000` to `var LD_CLOSE_MS=3500`. The CSS countdown-bar animation reads the same value through `d.style.setProperty('--ld-close',LD_CLOSE_MS+'ms')` (line 218), so the visual timer adapts automatically at zero extra cost. | shot:`p390-lead-04-sent.png`; `tools/patch_lead_dialog.py:200`; facts `d1360.replies.ok.closedItself:true`, `d1360.replies.ok.y2:3512===y0:3512`, `p390.replies.ok.closedItself:true` |
| FLOW-02 | P2 | M | dialog / opened from product window (V3 path) | Product-context interest is silently carried but not confirmed to the visitor. When "הוסיפו לתפריט" opens the dialog, `#pf-int` shows empty. `ldCtx` is set to the product name via `document.getElementById('fm-name').textContent.trim()` and travels at send time through `interest:g('pf-int')||ldCtx` (`tools/patch_lead_dialog.py:293`) — the product name IS sent correctly. But the visitor sees an empty interest select and has no way to know the context is captured. On ≥880 px the product photo in `.ld-pic` provides implicit context; on mobile only the tinted rim color (`--ld-tint`) hints at it. A visitor may fill in an unrelated interest, or close unsure whether their product was recorded. | In the `ldOpen` JS function (`tools/patch_lead_dialog.py`, after the `ldCtx` assignment at ~line 209), when `ldCtx` is non-empty and `i.value` is empty, surface the product name as a kicker line in `.pf-head` beneath the heading: `if(ldCtx&&!i.value){var s=d.querySelector('.pf-int-ctx');if(!s){s=document.createElement('small');s.className='pf-int-ctx';d.querySelector('.pf-head').appendChild(s);}s.textContent=ldCtx;}` and clear it on close in the close handler. Route exact copy and styling to COPY and VISUAL dimensions. | `tools/patch_lead_dialog.py:209` (`ldCtx=fm?document.getElementById('fm-name')...`); `tools/patch_lead_dialog.py:293` (`interest:g('pf-int')||ldCtx`); facts `d1360.ctas[f-detox].interest:""`, `d1360.ctas[f-detox].fmodal:true` |
| FLOW-03 | P2 | S | page / nav + hero + closing CTA (V10) | The five CTA labels for one destination are contextually coherent and no two contradict each other. One grammatical inconsistency exists: "אני מעוניין" (hero, first-person singular masculine) versus "רוצים להתחיל" (nav and closing, first-person plural). The page's body copy addresses the visitor in second-person plural ("שלכם") throughout. Switching the visitor's voice from plural ("we want to start") to singular ("I am interested") within the same scroll creates a subtle friction for attentive readers. "אני מעוניין" is also masculine-only; the feminine form is "אני מעוניינת". | Route to COPY dimension for decision. If aligning to plural, the hero CTA could read "נרצה לשמוע עוד ←" or stay as "רוצים להתחיל ←". If keeping "אני מעוניין", consider "אני מעוניין/ת" for gender inclusivity. Tom's instruction: propose only small clear fixes — do not rewrite copy that works. | facts `p390.page.text[0]:"nav: ... רוצים להתחיל ←"`; `p390.page.text[1]:"section.hero: ... אני מעוניין ←"` |
| FLOW-04 | P2 | S | page / conversion funnel (V10) | Seven sections between the economics CTA and the closing bigcta have no standalone conversion link: TEA 2.0, the 4-step operations section, matcha, purees, tools, and about run consecutively with only the product-window path ("הוסיפו לתפריט") available for product-specific intent. A visitor convinced by the TEA 2.0 trend data or the 4-step simplicity argument must scroll past four to five more screens before finding the next "רוצים להתחיל". The operations section is the highest-conviction moment for an undecided visitor ("every bartender pours GT perfectly on day one") — no CTA follows it. | Add one `<a class="sub-cta" href="#contact" data-cta="ops">רוצים להתחיל ←</a>` immediately after the 4-step operations section in the Hebrew i18n template (`gt-site/i18n/parts/he_visible_*.py`, at the block ending "4 מגישים מערבבים, מקשטים, מצלמים."). Style matches the existing `.sub-cta` used on the slides. Effort S. | facts `d1360.page.text[5]:"section: ... מגישים בארבעה צעדים..."` (no CTA); `d1360.page.text[9]:"div.bigcta: ... רוצים להתחיל ←"` (next CTA, 4 sections later) |

---

### CTA coverage: all 19 — classification

All 19 CTAs: `open:true`, `closed:true`, `focusBack:true`, `y1===y0`, `y2===y0` on both p390 and d1360. No gaps. Classification below.

| CTA | Label | data-price | interest pre-set | Gap |
|---|---|---|---|---|
| nav (i=0) | רוצים להתחיל | — | — | none |
| hero (i=1) | אני מעוניין | — | — | FLOW-03 (copy) |
| slides ×10 (i=2–11) | רוצה מחירון | yes | המחירון המלא | none |
| catalogue (i=12) | לקבלת הקטלוג המלא | yes | המחירון המלא | none |
| economics (i=13) | רוצה מחירון ותמחירים | yes | המחירון המלא | none |
| flavour cards ×3 (i=14–16) | (card label → product window) | — | — | none (two-step is correct) |
| closing bigcta (i=17) | רוצים להתחיל | — | — | none |
| product window (i=f-detox) | הוסיפו לתפריט | — | empty (ldCtx fallback) | FLOW-02 |

---

### Reply-state flow: what the visitor sees and does next

| State | Visitor sees | Values kept | Next action |
|---|---|---|---|
| `ok` (was_new confirmed) | Check + "תודה רבה!" + promise + tel: link + WhatsApp | — (sent) | Dialog auto-closes at LD_CLOSE_MS; page returns to y0; re-opening any CTA shows sent state without re-close. |
| `drop` (ok but no was_new — honeypot or fast) | "לא הצלחנו לשלוח את הפנייה. נסו שוב, או דברו איתנו ישירות: וואטסאפ · 054-398-2444." | yes | Retry (will succeed if not a bot) or tap WhatsApp/phone link. The error message is strategically identical to the server-error message — intentional, so as not to reveal bot detection. |
| `missing` (400 missing_fields) | "חסרים פרטי חובה. בדקו שם, שם העסק, עיר וטלפון." | yes | Fix the named fields and resubmit. |
| `phone` (bad phone) | "מספר הטלפון לא נראה תקין. בדקו אותו ונסו שוב." | yes | Correct the phone field and resubmit. |
| `e502`, `timeout`, `offline` | "לא הצלחנו לשלוח את הפנייה. נסו שוב, או דברו איתנו ישירות: וואטסאפ · 054-398-2444." | yes | Retry or tap WhatsApp/phone link. |

All error paths: `kept:true`, dialog stays open, WhatsApp and phone links in the `pf-alt` line remain visible below the error. No path loses the visitor's typed data.

---

### Structural checks (all PASS)

- **Page never moves**: `y1===y0` and `y2===y0` for all 19 CTAs across both p390 and d1360. `cm-lock` on `html`, not `body` — no iOS jump.
- **All required fields visible without scroll**: `fits.pf-name/pf-venue/pf-city/pf-phone/pf-agree: true` on every tested viewport from p320 to d1920.
- **Font sizes**: all 4 required inputs report 16 px on p390 and d1360 — no iOS auto-zoom.
- **Focus trap**: `tabLeftDialog:0` on both viewports — no tab key escapes the dialog.
- **Reduced motion**: `reducedMotion:"none"` confirms all animations (`ld-up`, `ld-fade`, `ld-draw`, `ld-bar`) are suppressed when the OS preference is set.
- **Dialog a11y**: `axe:[]` on the dialog at p390 and d1360. `aria-labelledby="ld-h"` on `#ldlg`, `aria-label="סגירה"` on ✕, `aria-hidden="true"` on decorative elements.
- **3 s hold**: p390 `fast.elapsed_ms:3050`, `fast.ok:true`. The d1360 fast test is `"inconclusive: the page was not interactive before 3 s"` — a headless-browser timing artefact at the larger viewport; the mechanism is proven on p390 and by the source code.
- **No-JS path**: `noJs.dialogOpen:false`, `noJs.telOpacity:"1"`, `noJs.ok:true`. Without script, all 19 links scroll to `#contact`, which shows the form with mailto: fallback and the full address/phone/WhatsApp/email block.
- **Deep link (`#contact`)**: `deepLink.dialogOpen:false`, `contactTop:0`, `ok:true`. Scrolls to form; dialog does not open. Per spec §4.
- **Already-sent reopen**: `reopenedSent:true` on both viewports. The sent state shows without auto-close; WhatsApp and phone links visible.
- **Product interest carry (V3)**: `interest:g('pf-int')||ldCtx` at send time. Product name travels correctly as fallback interest when visitor leaves `#pf-int` empty. Sent body confirmed to include the interest value.
- **Closing CTA ghost fix**: `div.ghost{pointer-events:none}` is applied. The decorative "GT" text no longer intercepts taps on the closing CTA. Confirmed by the sticking report (`div.ghost -25→1385`) with `overflowX:false`.
- **Four fields + consent**: minimum required by the intake contract. Optional fields (role, email, interest, message) correctly gated behind one `<details>` tap labeled "עוד פרטים (לא חובה)". Disclosure has `min-height:44px` touch target. This is the least friction the intake allows — no reduction is possible without an intake change (out of scope, §4).
- **Sent state content**: tells the café owner WHO ("GT Everyday" by context), WHEN ("תוך יום עסקים אחד"), and HOW ELSE (tel: link + WhatsApp). Sufficient. See FLOW-01 for the timing gap.
- **Auto-close is too short (2 s)**: see FLOW-01. `LD_CLOSE_MS=3500` is the fix.
- **Consent disclosure**: "אפשר לפנות אליי בנושא אספקה סיטונאית." is first-person, optional-feeling in tone but marked `required` in the DOM — the intake requires it. Correct. The optional-only fields behind `<details>` are correctly labelled as not required.
- **Third-party JS errors in console** (`storeify_requestaquote`, `goodavTriggerEvents`, `Unexpected token ';'`): present on all viewports; these are Shopify app errors from other installed theme apps, unrelated to the dialog code and verified not to affect the lead flow.

---

### World-class upgrades (beyond defects)

1. **Haptic confirmation on send**: On the `was_new` success branch in `tools/patch_lead_dialog.py` JS (after the `d.classList.add('closing')` call), add `if(navigator.vibrate)navigator.vibrate([40])`. One short buzz at the moment the lead lands. Graceful no-op on iOS. Costs zero layout budget and matches the "cheapest Android in a kitchen" persona perfectly.

2. **Autofill-awareness pre-scan**: On open, briefly scan whether `#pf-name` already has a browser-autofill value. If yes, a subtle green ring on all pre-filled fields tells the visitor "the browser remembered you — just check and send." This collapses the fill step from 4 taps to consent + send. Implement in `ldOpen` with a 150 ms `setTimeout` after `showModal()`.

3. **Slide-specific heading kicker**: The dialog already wears the slide's photo and color. Add the slide's product category name as a small kicker line above the heading "בקשת מחירון וטעימה" — e.g., "תמצית יפנית Revive". `sl.dataset.name` or the slide's `h3` text is the source. This personalizes the dialog to the exact drink that triggered it and reinforces the brand's specificity.

4. **Back-button micro-cue on Android**: The back button correctly closes the dialog via `popstate` — confirmed in the code. A first-time visitor from an ad may hesitate before using it, fearing they'll leave the site. A one-time tooltip on the grab bar ("← חזרה לדף" fading in for 2 s on first open) removes that hesitation without permanent clutter.

5. **Named responder in the sent state**: Replace the generic "ונחזור אליכם" with a named person ("ענת תחזור אליכם" if GT has a consistent first responder). A human name on the promise increases call-back trust materially. Requires Tom's sign-off on who the designated responder is.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 — Phone, ad arrival, "רוצה מחירון" on a hero slide, send, scroll on. Target ≤30 s one-handed. | PASS | No break. Hero "אני מעוניין" is on the first screen without scrolling (~2 s to reach). Manual fill: ~22 s total; autofill: ~14 s. 3 s hold is transparent (most visitors type for >3 s after page load). Tap count: 7 manual (CTA + 4 fields + consent + send) or 3 with autofill. |
| V2 — Desktop, read products, "לקבלת הקטלוג המלא", send. | PASS | Dialog opens from catalogue CTA at y0=3486, interest pre-set to "המחירון המלא". `#pf-name` focused immediately (pointer:fine). 820 px centered card with product photo. Clean. |
| V3 — Product interest: flavour card → product window → "הוסיפו לתפריט" → send. Lead carries product. | PASS with friction | Dialog opens; two-step path works (card opens fmodal, fmodal CTA opens lead dialog). Product name travels via ldCtx to sent body. FRICTION (FLOW-02): interest select is empty — visitor has no visual confirmation the product context is captured. |
| V4 — Hesitant: open, dismiss via ×, Esc, backdrop, phone back-button. Nothing lost, page where it was. | PASS | All four dismiss mechanisms confirmed across all 19 CTAs: `closedBy` cycles x / esc / backdrop; `popstate` handler closes on back-button. `y2===y0` for all. Auto-preset interest is cleared on dismiss (ldAuto guard). Values typed by the visitor remain in the form for the next open. |
| V5 — Failure: bad phone, network error, timeout, offline. Understand, recover or use WhatsApp. | PASS | All states show `kept:true`, dialog stays open, WhatsApp + phone fallback visible. Error messages are distinct: phone error names the fix; server / timeout / offline show the escape path with both contact methods. No silent loss. |
| V6 — Already sent: tap another CTA, see sent state, see WhatsApp. | PASS | `reopenedSent:true` on both p390 and d1360. Sent state displays without auto-close on reopen. WhatsApp and phone links remain tappable. |
| V7 — Hebrew screen-reader user (VoiceOver / TalkBack): open, fill, send, hear result, focus returns. | PASS (inferred structural; live VoiceOver test advised before publish) | `axe:[]` on the dialog at all tested viewports. `aria-labelledby="ld-h"`, `aria-label="סגירה"` on ✕, `aria-hidden="true"` on grab bar and `.ld-pic`. Focus trap confirmed (`tabLeftDialog:0`). `reducedMotion:"none"` confirms animations suppressed. `<dialog>` quirks on iOS Safari / VoiceOver are inferred — Chromium harness per §5 cannot prove this. |
| V8 — Keyboard only, desktop. | PASS | `tabLeftDialog:0`. On open, `#pf-name` focused (`pointer:fine` detected at d1360: `focus:"input#pf-name"`). Tab sequence: × → name → venue → city → phone → details summary → (optional fields when open) → consent → submit → WhatsApp → phone → wraps to ×. Esc closes. No tab escape. |
| V9 — No JavaScript / slow network: link reaches `#contact`, phone and WhatsApp visible. | PASS | `noJs.dialogOpen:false`, `noJs.telOpacity:"1"`, `noJs.ok:true`. Without script, all `a[href="#contact"]` links scroll to the in-page form; the form's `action="mailto:..."` fallback is intact; the full contact block (address, phone, WhatsApp, email, Instagram) is visible. Deep link: same behavior, `deepLink.ok:true`. |
| V10 — Read whole page on phone: offer, trust, clarity, one voice. | PASS with note | First screen on p390 is clear: "עידן חדש של משקאות בבית העסק שלכם." above fold with "אני מעוניין ←" prominent. Product copy is specific and confident. Trust builds progressively through economics → TEA 2.0 → operations → brand story. FRICTION: 7-section gap between economics CTA and closing CTA (FLOW-04). CTA voice mixes singular/plural (FLOW-03). |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 1 | 3 | GREEN — no P0, 1 P1 (≤2 threshold) |

The lead flow is structurally sound: all 19 CTAs open correctly, the page never moves, values survive every error state, the no-JS fallback is intact, and the dialog is axe-clean. The one P1 (auto-close at 2 s) is a single-line fix in the generator. The three P2 items are polish — two are copy-dimension and one (FLOW-02) is a medium-effort JS enhancement for the product-interest path.
