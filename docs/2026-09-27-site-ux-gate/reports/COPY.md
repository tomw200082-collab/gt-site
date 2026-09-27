## ux-content-state-designer — brand site lead dialog and page

### Not applicable from my definition
`portal_ux_standard.md`, English-first, RTL-forbidden and Hebrew-is-P0 belong to the operations portal; RUNTIME_READY, shadcn/Tailwind and Operational Precision tokens do not apply. This surface is Hebrew RTL by Tom's explicit approval. "Operator" maps to visitor throughout.

---

### Findings

| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact copy) | Evidence |
|---|---|---|---|---|---|---|
| COPY-01 | P1 | S | About section — all states | `alt` text on the About section image is the placeholder `תמונות מפעל וצוות — ממתין לחומרים`. A screen-reader user (Task V7) hears this verbatim as the image description. The 2026-09-03 review noted the photograph has not yet been supplied; the placeholder should not ship. | `he_visible_3.py` t0433: change to `""` (empty alt, marking the element decorative until the photograph exists). Generator sets the attribute; fix is one string change. | `file:he_visible_3.py:55` — `"t0433": "תמונות מפעל וצוות — ממתין לחומרים"` |
| COPY-02 | P1 | S | Hero — all states | `אני מעוניין` is masculine singular. The rest of the page addresses visitors in plural and gender-neutral forms (אתכם, שלכם, רוצים, הוסיפו). In commercial Hebrew targeting café and restaurant owners — a mixed-gender audience — defaulting to masculine is considered unprofessional. The brief explicitly asks this to be checked. | `he_visible_1.py` t0029: current `"אני מעוניין"` → proposed `"מעוניין/ת"`. Minimal change: one character added, every other word preserved. | shot:`p390-page-01.png` (hero visible); `file:he_visible_1.py:29` |
| COPY-03 | P2 | S | Dialog — missing_fields error state | Error reads `חסרים פרטי חובה. בדקו שם, שם העסק, עיר וטלפון.` The first field's visible label is `שם מלא`, not bare `שם`. A visitor re-reading the error while glancing at the form sees a label mismatch: "which 'שם'?" | `patch_form.py` line 153: current `'חסרים פרטי חובה. בדקו שם, שם העסק, עיר וטלפון.'` → proposed `'חסרים פרטי חובה. בדקו שם מלא, שם העסק, עיר וטלפון.'` | shot:`d1360-lead-03-error.png`; `file:patch_form.py:153` |
| COPY-04 | P2 | S | i18n source — maintenance | t0495 still contains the old mailto success copy: `"אפליקציית המייל שלכם נפתחה עם המכתב המוכן. אם לא — כתבו ל־info@gteveryday.com"`. This string is overwritten by `patch_form.py` in the build, so visitors never see it — but if patch order changes or the patch is regenerated, the stale copy can resurface. | `he_visible_3.py` t0495: replace with the live success text: `"קיבלנו את הפרטים ונחזור אליכם תוך יום עסקים אחד. אם דחוף — 054-398-2444."` so source and rendered output match. | `file:he_visible_3.py:124` |
| COPY-05 | P2 | L | All CTAs — page voice | Nineteen CTAs address the visitor in at least three distinct grammatical voices: first-person singular (`אני מעוניין`, `רוצה מחירון`), plural imperative (`רוצים להתחיל`, `הוסיפו לתפריט`), and infinitive phrase (`לקבלת הקטלוג המלא`). The 2026-09-03 review already noted this and deferred to Tom as brand voice. Re-flagging here per the brief's explicit check. No proposed fix from this dimension — Tom's decision. | No fix proposed; Tom's call. | `file:he_visible_1.py:29`, `file:he_visible_3.py:145`, `file:patch_lead_dialog.py:253-264` |

---

### String inventory

| Location | Current string | Decision |
|---|---|---|
| `he_visible_1.py` t0029 | `אני מעוניין` (hero CTA) | **change** — COPY-02 |
| `he_visible_1.py` t0026 | `רוצים להתחיל` (nav CTA) | keep |
| `he_visible_1.py` t0040/48/56/64/72/80/88/96/104/112 | `רוצה מחירון` (ten slides × 10) | keep |
| `he_visible_1.py` t0209 | `לקבלת הקטלוג המלא` (catalogue CTA) | keep |
| `he_visible_2.py` t0271 | `רוצה מחירון ותמחירים` (economics CTA) | keep |
| `he_visible_3.py` t0446 / `patch_lead_dialog.py:263` | `רוצים להתחיל` (closing CTA) | keep |
| `he_visible_3.py` t0512 | `הוסיפו לתפריט ←` (product modal CTA) | keep |
| `patch_lead_dialog.py:118` (SHELL) | `סגירה` (aria-label on × button) | keep |
| `he_visible_3.py` t0468 / `patch_lead_dialog.py:270` | `בקשת מחירון וטעימה` (dialog heading, `id="ld-h"`) | keep — accurate and matches the form's purpose |
| `he_visible_3.py` t0469 | `עונים תוך יום עסקים אחד` (dialog subhead) | keep — excellent trust signal |
| `patch_lead_dialog.py:91` | `שם מלא` (field label) | keep |
| `patch_lead_dialog.py:92` | `שם העסק` (field label) | keep |
| `patch_lead_dialog.py:93` | `עיר` (field label) | keep |
| `patch_lead_dialog.py:94` | `טלפון` (field label) | keep |
| `patch_lead_dialog.py:96` | `עוד פרטים (לא חובה)` (disclosure toggle) | keep |
| `patch_lead_dialog.py:97` | `תפקיד` (optional label) | keep |
| `patch_lead_dialog.py:101` | `אימייל` (optional label) | keep |
| `patch_lead_dialog.py:102` | `מה מעניין אתכם` (optional label) | keep |
| `patch_lead_dialog.py:107` | `משהו שכדאי שנדע?` (optional textarea label) | keep |
| `patch_lead_dialog.py:103–108` | `המחירון המלא` / `טעימה במקום` / `תמציות תה` / `מאצ׳ה ואבקות` / `מחיות פרי` / `כלי בר ואביזרים` / `כל תפריט הקיץ` (interest options) | keep |
| `he_visible_3.py` t0490 | `אפשר לפנות אליי בנושא אספקה סיטונאית.` (consent) | keep — fixed per §4 constraints |
| `patch_form.py:179` (PF_LABEL) | `שליחה ←` (submit button) | keep |
| `patch_form.py:135` | `שולח…` (sending state) | keep |
| `patch_form.py:149` | `נשלח ✓` (sent button) | keep |
| `patch_form.py:153` | `חסרים פרטי חובה. בדקו שם, שם העסק, עיר וטלפון.` (missing_fields error) | **change** — COPY-03 |
| `patch_form.py:155` | `מספר הטלפון לא נראה תקין. בדקו אותו ונסו שוב.` (bad_phone error) | keep — actionable and correctly gendered |
| `patch_form.py:157` | `כתובת המייל לא נראית תקינה. בדקו אותה ונסו שוב.` (bad_email error) | keep — "תקינה" agrees with "כתובת" (feminine) |
| `patch_form.py:181–183` (PF_ERR) | `לא הצלחנו לשלוח את הפנייה. נסו שוב, או דברו איתנו ישירות: וואטסאפ · 054-398-2444.` (fallback error) | keep — names two recovery paths |
| `he_visible_3.py` t0494 | `תודה רבה!` (sent heading) | keep |
| `patch_form.py:111–113` | `קיבלנו את הפרטים ונחזור אליכם תוך יום עסקים אחד. אם דחוף — 054-398-2444.` (sent body) | keep — excellent: names who acts, when, and the urgent-contact path |
| `he_visible_3.py` t0492/t0493 | `או כתבו לנו · בוואטסאפ` (WhatsApp line) | keep |
| `he_visible_3.py` t0495 | `אפליקציית המייל שלכם נפתחה עם המכתב המוכן. אם לא — כתבו ל־info@gteveryday.com` | **change** — COPY-04 (stale source, not displayed) |
| `he_visible_3.py` t0433 | `תמונות מפעל וצוות — ממתין לחומרים` (About image alt) | **change** — COPY-01 |
| All product copy (t0131–t0512) | Hebrew typography: geresh ׳ in מאצ׳ה/הוג׳יצ׳ה/צ׳אי/ג׳ינג׳ר, gershayim ״ in בע״מ/מ״ל/ק״ג, maqaf ־ in ו־Fresh/ל־500 | keep — all used correctly |

---

### Approval batch

**(a) Must-fix — gate-blocking for screen-reader conformance or professional tone:**

| ID | Current | Proposed | Why |
|---|---|---|---|
| COPY-01 | `he_visible_3.py` t0433: `"תמונות מפעל וצוות — ממתין לחומרים"` | `""` (empty alt — marks element decorative until photograph is supplied) | A screen-reader visitor hears a content-management placeholder verbatim; the photograph does not yet exist per 2026-09-03 review |
| COPY-02 | `he_visible_1.py` t0029: `"אני מעוניין"` | `"מעוניין/ת"` | Masculine default in commercial Hebrew targeting a mixed-gender audience is unprofessional by 2026 Israeli market standards; minimal change preserves every other word |

**(b) Small clear improvements:**

| ID | Current | Proposed | Why |
|---|---|---|---|
| COPY-03 | `patch_form.py:153` error text: `בדקו שם, שם העסק, עיר וטלפון.` | `בדקו שם מלא, שם העסק, עיר וטלפון.` | Aligns error text with visible field label `שם מלא`; eliminates ambiguity between person's name and business name |
| COPY-04 | `he_visible_3.py` t0495: `"אפליקציית המייל שלכם נפתחה עם המכתב המוכן. אם לא — כתבו ל־info@gteveryday.com"` | `"קיבלנו את הפרטים ונחזור אליכם תוך יום עסקים אחד. אם דחוף — 054-398-2444."` | Syncs i18n source with what the build actually produces; removes resurrection risk if patch order changes |

**(c) Tom's decision (no fix proposed from this dimension):**

- COPY-05: CTA voice fragmentation across 19 links — already deferred to Tom as brand voice in 2026-09-03 review; reconfirmed here.

---

### World-class upgrades (beyond defects)

1. **Subhead as a countdown promise.** `עונים תוך יום עסקים אחד` is good. The best converting lead forms in this category (Wolt, Lightspeed, Toast) name the *caller* and the *window* together: `הצוות שלנו מחזיר תוך יום עסקים — בשביל הפגישה, לא בשביל ה-pitch`. That one line does the objection-handling the dialog currently doesn't.

2. **Interest label as a signal, not a filter.** The optional `מה מעניין אתכם` select sits behind a disclosure and most visitors skip it. Moving the two most-tapped options (`המחירון המלא`, `טעימה במקום`) as visible pill toggles above the disclosure — selected by default based on the CTA that opened the dialog — would let the visitor confirm rather than choose, saving a decision.

3. **Sent state: name the next concrete step.** `ונחזור אליכם תוך יום עסקים אחד` is the promise. Adding one line after it — `תקבלו שיחה ממספר ישראלי של צוות GT` — removes the anxiety of an unknown caller and reduces no-answer rates.

---

### Visitor task results

| Task | Result | Where it breaks |
|---|---|---|
| V1 — phone, ad, hero CTA, send | PASS | Dialog opens instantly, all four fields fit on first screen (confirmed `lead.fits` all true, p390 screenshot), button visible without scrolling, sent state clear. Friction: `אני מעוניין` is masculine — minor |
| V2 — desktop, catalogue CTA, send | PASS | `לקבלת הקטלוג המלא` opens dialog; interest auto-selects `המחירון המלא`; `d1360-lead-02-open.png` confirms clean layout |
| V3 — flavour card → product modal → `הוסיפו לתפריט` → send | PASS | `fmodal` path confirmed in facts (`"kind":"fmodal"`, `"ok":true`); product name carried as `ldCtx` |
| V4 — hesitant, all close paths | PASS | ×, Esc, backdrop all confirmed (`closedBy` cycles through all three in facts); `focusBack: true` all cases; page stays at same `y2 = y0` |
| V5 — bad phone, network error, timeout, offline | PASS | All four error paths tested in facts; each shows correct Hebrew message, `kept: true` (typed values preserved), no false success |
| V6 — already sent, reopens dialog | PASS | `reopenedSent: true` in facts; second tap shows sent state with WhatsApp line |
| V7 — Hebrew screen-reader | FRICTION | COPY-01: About section image alt `תמונות מפעל וצוות — ממתין לחומרים` is spoken verbatim. Dialog itself is clean: `aria-labelledby="ld-h"` correctly labels the dialog; × button has `aria-label="סגירה"`; error region has `role="alert"`; `lead.axe: []` (dialog zero violations) |
| V8 — keyboard only, desktop | PASS | `lead.tabLeftDialog: 0` (no focus escaping); `lead.axe: []`; focus returns on close (`focusBack: true` all cases) |
| V9 — no JavaScript | PASS | `lead.noJs.ok: true`; links still reach `#contact`; tel/WhatsApp/mail links visible (`telOpacity: "1"`) |
| V10 — read whole page on phone | PASS with note | All sections readable; no machine-translation detected; Hebrew typography correct throughout. COPY-02 (`אני מעוניין`) is the one professional-tone note visible on the first screen |

---

### Scorecard

| P0 | P1 | P2 | Status |
|---|---|---|---|
| 0 | 2 (COPY-01, COPY-02) | 3 (COPY-03, COPY-04, COPY-05) | **GREEN** — no P0, ≤2 P1 |
