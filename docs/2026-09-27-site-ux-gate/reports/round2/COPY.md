## ux-content-state-designer — brand site lead dialog and page (round 2)

### Not applicable from my definition
`portal_ux_standard.md`, English-first, RTL-forbidden, Hebrew-is-P0, RUNTIME_READY, shadcn/Tailwind and Operational Precision tokens belong to the operations portal and do not apply. This surface is Hebrew RTL by Tom's explicit approval. "Operator" maps to visitor throughout.

---

### Round-1 findings

| ID | Status | Evidence |
|---|---|---|
| COPY-01 | ACCEPTED | §9.3 reason holds: `tools/patch_claims.py` removes the About section block entirely; the alt text `תמונות מפעל וצוות — ממתין לחומרים` never renders. |
| COPY-02 | FIXED | `i18n/parts/he_visible_1.py` t0029: `"אני מעוניין"` → `"בואו נעבוד יחד"` (plural, gender-neutral). Confirmed in git diff and `strings.he.json`. §9.2. |
| COPY-03 | FIXED | `tools/patch_form.py` error text: `"בדקו שם מלא, שם העסק, עיר וטלפון."` — confirmed in `replies.missing.err: "חסרים פרטי חובה. בדקו שם מלא, שם העסק, עיר וטלפון."` (facts, p390) and rendered in shot `p390-lead-03-error.png`. §9.2. |
| COPY-04 | OPEN | `i18n/parts/he_visible_3.py` line 124, t0495 unchanged: still `"אפליקציית המייל שלכם נפתחה עם המכתב המוכן. אם לא — כתבו ל־info@gteveryday.com"`. Not in round-2 diff. Not in §9.2 or §9.3. Remains P2. |
| COPY-05 | FIXED | Tom settled voice with §9.1 item 5. All 14 CTAs updated: the five page links and dialog heading to `בואו נעבוד יחד`; all ten hero slides to `הוסיפו לתפריט`. Confirmed across `he_visible_1.py`, `he_visible_2.py`, `he_visible_3.py` and `strings.he.json` diffs. |

---

### New strings review — U-16 to U-25 (gate record §5.5)

| U | String(s) | Decision | Note |
|---|---|---|---|
| U-16 | `עוד פרטים (לא חובה)` | **Approved** | Plural, gender-neutral, professional. Visible in `p390-lead-02b-form.png`. |
| U-17 | `סגירה` (four modal × buttons) | **Approved** | Minimal, correct, screen-reader–safe. |
| U-18 | `יש לכם עסק?` · `אנחנו עובדים רק עם עסקים, בסיטונאות.` · `כן, יש לי עסק` · `לא, לשימוש פרטי` | **Approved** | Question in plural (לכם), explanatory line professional and precise. "כן, יש לי עסק" switches to singular first-person for the answer, which is natural — the decision-maker speaks for themselves. "לא, לשימוש פרטי" is gender-neutral per Tom's explicit choice (gate record U-18). Rendered correctly in `p390-lead-02-open.png` and `d1360-lead-02-open.png`. |
| U-19 | `אנחנו עובדים רק עם עסקים.` · `ללקוחות פרטיים, המוצרים שלנו נמכרים באתר של אליטה אופק.` · `למוצרי GT אצל אליטה אופק` · `חזרה` | **Approved** | "ללקוחות פרטיים" uses masculine plural as grammatical default for "customers" — standard and correct. Link names the destination precisely. `חזרה` clear. Rendered correctly in `p390-lead-06-private.png`. The subline `עונים תוך יום עסקים אחד` is hidden in this step (CSS `.partner.priv .pf-head span{display:none}`) — correct. |
| U-20 | `מה הכי מעניין אתכם?` · `נשלח לכם את התפריט בוואטסאפ.` · `מאצ׳ה` · `אובה` · `צ׳אי מסאלה` · `תמציות תה` · `בניית תפריט משקאות בעסק שלי` | **Approved** | Heading and subline plural (אתכם, לכם). Geresh (׳) correct in `מאצ׳ה` and `צ׳אי מסאלה`. "בניית תפריט משקאות בעסק שלי" uses first-person singular — natural as the visitor's own intent statement; Tom specified this phrasing. `נשלח לכם את התפריט בוואטסאפ.` is a promise the page can keep (U-21 links go straight to WhatsApp with the message). Rendered correctly in `p390-lead-04-sent.png` and `d1360-lead-04-sent.png`. |
| U-21 | `היי, אני מעוניין ב{line}` (WhatsApp pre-write) | **Approved — Tom's explicit phrasing** | Masculine singular. Tom specified this exact form in writing (gate record U-21: «היי אני מעוניין במה שהוא בחר»). The visitor can edit before sending. Confirmed in facts: `lines[].text: "היי, אני מעוניין במאצ׳ה"` etc. No proposed change — Tom's decision. |
| U-22 | Heading `בואו נעבוד יחד` (supersedes `בקשת מחירון`); contact line and closing banner revised (see U-25) | **Approved** | "Tasting" (`טעימה`) removed from all visible strings. Confirmed in diff: t0468, t0445, t0464, t0446. |
| U-23 | `חסרים פרטי חובה. בדקו שם מלא, שם העסק, עיר וטלפון.` | **Approved** | Fixed (COPY-03 above). |
| U-24 | `בואו נעבוד יחד` (five page CTAs + dialog heading) · `הוסיפו לתפריט` (ten slides + product window) | **Approved** | Voice unified. Confirmed in diff and all screenshots. `המחירון המלא` removed from interest options. |
| U-25 | `השאירו פרטים — נחזור אליכם ונבנה יחד את תפריט המשקאות שלכם.` · `נבנה יחד תפריט משקאות שהאורחים שלכם יצלמו.` | **Approved** | Both lines are plural, warm, active voice, promise-led. Professional tone. Confirmed in diff: t0464 and t0445. |

---

### Findings (open only)

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact copy) | Evidence |
|---|---|---|---|---|---|---|
| COPY-04 | P2 | S | `he_visible_3.py` — source only, not rendered | t0495 still contains the old mailto success copy `"אפליקציית המייל שלכם נפתחה עם המכתב המוכן. אם לא — כתבו ל־info@gteveryday.com"`. `patch_form.py` overrides it in the build so visitors never see it, but if patch order changes or the file is regenerated this stale string can resurface. | `i18n/parts/he_visible_3.py` line 124, t0495: change to `"קיבלנו את הפרטים ונחזור אליכם תוך יום עסקים אחד. אם דחוף — 054-398-2444."` — syncs the source with the live build output. | `file:i18n/parts/he_visible_3.py:124` |

---

### World-class upgrades (beyond defects)

1. **The pick-step subline promises the menu PDF.** `נשלח לכם את התפריט בוואטסאפ.` is a promise that currently a person fulfils manually (BRIEF §9.1 item 6). Once the automatic PDF send is live, this line delivers exactly what it says. The copy is already future-proof.

2. **`בניית תפריט משקאות בעסק שלי` (full-width pill).** The broadest, least product-specific option is the last and widest. For a business owner still deciding, this is the lowest-commitment pick. Positioning it as the floor option, full-width, is a good conversion choice — no change needed.

3. **The private-buyer redirect is warm, not a wall.** "המוצרים שלנו נמכרים באתר של אליטה אופק" names a specific destination and names GT's presence there, so the private visitor doesn't feel ejected. The copy accomplishes what the best e-commerce gatekeepers do: redirect without rejection.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 (phone, ad, `כן יש לי עסק`, send) | PASS | Business question fits on screen without scrolling (p390 `ask` height confirmed in facts; both buttons shown: h=52); form step has all four fields above the fold (`fits` all true, p390); sent state clear. `shot:p390-lead-02-open.png`, `shot:p390-lead-02b-form.png` |
| V2 (desktop, catalogue CTA, send) | PASS | Catalogue CTA is now `בואו נעבוד יחד`; dialog opens to ask step; `d1360-lead-02-open.png` confirms clean two-panel layout. |
| V3 (flavour → product window → `הוסיפו לתפריט` → send) | PASS | `steps.stepYes: "form"`, `fmodalAfter` confirmed; product window sends product name as interest via `ldCtx`. |
| V4 (hesitant, all close paths) | PASS | ×, Esc, backdrop confirmed; `steps.y2 = steps.y0` (page stays put); `focusBack` returns. |
| V5 (bad phone, network error, timeout, offline) | PASS | All four error texts correct Hebrew, `kept: true`, values preserved. `missing` reply: `"חסרים פרטי חובה. בדקו שם מלא, שם העסק, עיר וטלפון."` confirmed. `shot:p390-lead-03-error.png` |
| V6 (already sent, reopens to thanks and five lines) | PASS | On reopen, form is in `sent` state; `ldStep(f)` focuses `pf-pick-q`; the five line pills are visible. `replies.ok.stayedOpen: true`. |
| V7 (Hebrew screen-reader) | PASS | `lead.axe: []` (zero axe violations in dialog); `aria-labelledby="ld-h"` correct; all step questions are `tabindex="-1"` elements focused by `ldStep`; close button `aria-label="סגירה"`; pick group has `role="group" aria-labelledby="pf-pick-q"`. The About alt-text finding (COPY-01) is now moot — block removed. |
| V8 (keyboard only, desktop) | PASS | `lead.tabLeftDialog: 0`; `focusBack: true`; `axe: []`. |
| V9 (no JavaScript) | PASS | `noJs.ok: true`; `noJs.asks: false` (business-question step invisible without JS — visitor sees the static form directly, correct); `noJs.fieldsShown: true`; `telOpacity: "1"`. |
| V10 (read whole page on phone) | PASS | All CTAs now one voice (`בואו נעבוד יחד` / `הוסיפו לתפריט`). Hebrew typography correct throughout. No machine-translation patterns detected. COPY-02 and COPY-05 resolved. |
| V11 (private buyer) | PASS | Opens ask step → answers `לא, לשימוש פרטי` → sees private-buyer screen with Elita Ofek link → `חזרה` works. `steps.sends: 0` confirmed (nothing sent). `axePrivate: []` (zero violations). `shot:p390-lead-06-private.png` |
| V12 (after send, picks line, dialog closes on return) | PASS | `replies.ok.stayedOpen: true`; `focusSent: "p#pf-pick-q"`; five line pills present with correct WhatsApp targets (`https://wa.me/972547588132`) and pre-written messages; harness signals page hidden then visible → `ldClose()` called on `visibilitychange`. `shot:d1360-lead-04-sent.png` |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 0 | 1 (COPY-04) | **GREEN** — no P0, no P1; one maintenance P2 |
