# UX release gate: the brand site's lead dialog and page (brief for every UX agent)

Read this first. It re-aims your agent definition for one audit. Where this brief and your
definition disagree, this brief wins. The surface is GT's public brand site, not the operations
portal, and it is Hebrew RTL by design.

Shape taken from the 2026-09-25 customer-portal gate
(`gt-factory-os/docs/superpowers/plans/2026-09-25-customer-portal-ux-gate/BRIEF.md`).

## 1. What is under audit

`gteveryday.com`, the home page, as it renders on the preview theme `186698334449`
(`https://gteveryday.com/?preview_theme_id=186698334449`). Three things:

1. **The lead dialog.** Every lead call-to-action (every `a[href="#contact"]`) now opens the enquiry
   form in a native modal dialog, instead of scrolling the visitor to the form at the bottom. The
   dialog sends the lead and shows a check and the thanks. The page stays where it was. From round 2
   the dialog has steps (Tom, 2026-09-27; §9): whether the visitor has a business, the form, then the
   line that interests them, which opens WhatsApp.
2. **The call-to-action flow.** There are nineteen links: the nav, the hero, ten hero slides, the
   catalogue, the economics card, the closing banner, the product window's «הוסיפו לתפריט», and
   three flavour cards. The flavour cards open the product window first.
3. **The page's words and visuals.** Headings, call-to-action labels (one destination has at least
   four different labels: `רוצים להתחיל`, `אני מעוניין`, `רוצה מחירון`, `לקבלת הקטלוג המלא`,
   `רוצה מחירון ותמחירים`), the form's lines, hierarchy, rhythm, and the first screen on a phone.
   The earlier review of the same page is `gt-site/docs/2026-09-03_ux-review.md`.

**Source.** The page is generated, so a fix names the generator, never an output.
- `gt-site/src/index.en.html` is the delivered English design and is never edited.
- The Hebrew copy lives in `gt-site/i18n/parts/he_visible_{1,2,3}.py` (`he_js*.py` for script
  strings). It is applied by `tools/build.sh`, which then runs the patches in order.
- The dialog is `gt-site/tools/patch_lead_dialog.py`: markup, CSS and JS, and it runs last. The
  form's sender is `tools/patch_form.py`, and the patches before it are `patch_a11y.py`,
  `patch_ux.py`, `patch_launch.py` and `patch_ipad.py`.
- Built outputs, to read but never to fix: `src/index.html`, `theme/sections/gt-home.liquid`,
  `theme/assets/gt-site.css` and `gt-site.js`.
- The lead intake is `gt-factory-os/supabase/functions/website_lead_intake/index.ts`. It is out of
  scope for change (see §4).

## 2. Who arrives, and the bar

- **Who:** the owner or manager of a café, bar or restaurant in Israel. Mostly on a phone, often
  arriving from an ad or a WhatsApp share, between tasks, one-handed. Some come on an office
  desktop. They decide in seconds whether GT is worth a call.
- **The page's one job:** turn that visitor into a lead. The lead goes to the sales team's queue,
  and a person calls back within a business day.
- **The bar, in Tom's words (2026-09-27):**
  `חלונית שבה משאירים פרטים בצורה פשוטה ברורה ומאוד מאוד יפה ופשוטה וחזקה שממירה הכי הרבה` ·
  `כאשר הוא משאיר את הפרטים החלונית תיסגר אוטומטית והוא יוכל להמשיך לגלול`.
  Think of the best consumer checkout sheets and Apple-level touch craft, on the cheapest Android
  in a kitchen.
- **The brand is set:**
  - paper `--paper #FBF8F2`, ink `--ink #20241F`, green `--gt #3E6E34`;
  - Heebo, with Roca One named first;
  - flavour colours, bottle photography, rounded cards (26 px) and pill buttons.

  Refine within that world. A second style bolted onto a finished page is a finding, not a feature.

## 3. Rules from your definition that do NOT apply here

Say so once in your report, then move on.

- `gt-factory-os-portal/docs/portal_ux_standard.md`, "English-first", "RTL forbidden" and "Hebrew
  is P0" belong to the operations portal. This page is Hebrew RTL by Tom's approval.
- Operational Precision tokens, shadcn/Tailwind and RUNTIME_READY do not apply. The page is one
  static Shopify section.
- The persona is a visitor, not a factory operator. Map "operator" to **visitor** everywhere, and
  `operator-task-simulation` to **visitor-task-simulation** (§6).

## 4. Constraints on proposals (settled — do not reopen)

- **The intake contract is fixed.** The required fields are `contact_name`, `venue`, `city` and
  `phone` (9+ digits), plus the consent `אפשר לפנות אליי בנושא אספקה סיטונאית.`. There is no new
  field and no new `form_name`. Optional fields may be offered but never required.
- **One form.** The dialog borrows `#pform` from `#contact` and returns it: one sender, one state.
  Without JavaScript the links still reach `#contact`. A page opened with `#contact` scrolls there
  and does not open the dialog.
- **The page must not move.** Once the script has loaded, no call-to-action moves the page.
- **The honest thank-you.** Success means the intake stored the lead, marked by a `was_new` key.
  Sends are held until 3 s after navigation start, because the intake silently drops faster ones.
- **Settled by Tom:**
  - no prices on the served page (`data/site_flags.json` `show_prices: false`);
  - WhatsApp `054-398-2444`;
  - the business entry reads `כניסה לעסקים` / `לעסקים`;
  - the products stand on a soft floor shadow.
- **Copy.** Quote the current string and give the exact proposed Hebrew. **Tom, 2026-09-27:**
  `אל תשנה בצורה משמעותית. רק דברים שאתה בטוח שצריך לשפר, כמו שגיאות, ניסוחים לא מקצועיים בעברית מדוברת, וכאלה.`
  Propose only errors, unprofessional or colloquial phrasing, and small clear fixes, not a rewrite of
  copy that works. The gate's COPY dimension and the governor approve the batch, and Tom reads it in the
  report.
- **Out of scope:**
  - the landing pages' own forms and publication;
  - the ordering portal;
  - analytics and GTM configuration;
  - the intake itself.
- **Chromium only.** There is no WebKit in the harness. For Safari-only behaviour, reason from the
  CSS/JS and say that it is inferred: `dvh` and the toolbar, the keyboard over a sheet,
  `overflow:hidden` on iOS, focus zoom under 16 px, `<dialog>` quirks, sticky `:hover`.

## 5. Evidence

Regenerate it with `node gt-factory-os/api/scripts/site_ipad_shots.mjs`, with
`SITE_URL=https://gteveryday.com/?preview_theme_id=186698334449` and `AXE_JS` set to
axe-core 4.11.3. Every request to the intake is stubbed, and no real lead is sent.

The run writes to `$UX_OUT/site-ipad/`. **Before** is the live theme, where every call-to-action
scrolls to the form. **After** is the preview.

- **Viewports:**
  - phones `p320` (320×640), `p390` (390×844), `p430` (430×932), with an iPhone UA and touch;
  - tablet `t768`, and iPad `i744`, `i820`, `i1024`, `li1180`, `li1366`, with an iPadOS UA and touch;
  - desktops `d1360` (1360×860) and `d1920` (1920×1080), with no touch.
- **Lead shots (p390 and d1360):**
  - `-lead-01-before`: the catalogue call-to-action in view;
  - `-lead-02-open`;
  - `-lead-03-error` (400 `missing_fields`);
  - `-lead-04-sent`;
  - `-lead-05-after-close`: the page where it was.

  Every other viewport has `-lead-02-open`.
- **Page shots (p390, d1360):** `-page-NN`, the whole page in shots two screens tall, after one
  scroll through.
- **iPad shots:** `-home-*` and `-lp-*`, from the 2026-09-25 gate's scenes. They are regression
  checks.
- **Facts:** `site_ipad_facts.json`, per viewport.
  - `lead.ctas[]` is every call-to-action: `y0`/`y1`/`y2` (scrollY before, open, after close),
    `open`, `closed`, `closedBy` (×, Esc, backdrop), `focusBack` and `interest`.
  - `lead.replies{}` has one entry per intake answer: ok, the silent drop, missing fields, bad
    phone, 502, 15 s timeout, offline. Each entry records the state, the error text, whether the
    typed values were kept, the `generate_lead` count, the request body keys and `elapsed_ms`, the
    automatic close, and whether reopening shows the sent state.
  - `lead.fast`: the 3 s hold.
  - `lead.noJs` and `lead.deepLink`.
  - `lead.fits`: the required fields visible without scrolling.
  - `lead.fields`: labels, `autocomplete`, font size.
  - `lead.axe` (dialog only), `lead.axePage` (the whole page), `lead.tabLeftDialog` and
    `lead.reducedMotion`.
  - `lead.overflow`, per viewport.
  - `page.text`: the visible text of each section.

**Citations.** A visual or layout finding MUST cite a shot path. A structural, flow, copy or
semantic finding cites `file:line` in a generator or source file. Open the images: the Read tool
renders PNGs.

## 6. Visitor tasks to simulate

| Task | The visitor and what they do |
|---|---|
| V1 | Phone, from an ad: first screen, understand what GT offers, tap `רוצה מחירון` on a hero slide, send the four details, keep scrolling. Target: under 30 s, one-handed. |
| V2 | Desktop: read the products, `לקבלת הקטלוג המלא`, send. |
| V3 | Product interest: a flavour card, then the product window, then `הוסיפו לתפריט`, then send. The lead carries the product. |
| V4 | Hesitant: open the dialog and leave it by ×, Esc, the backdrop, and the phone's back button. Nothing is lost, and the page is where it was. |
| V5 | Failure: a bad phone number, a network error, a timeout, offline. Understand it, and recover or use WhatsApp. |
| V6 | Already sent: tap another call-to-action, see that it was sent, and see the WhatsApp line. |
| V7 | A Hebrew screen-reader user (VoiceOver/TalkBack): open, fill, send, hear the result, focus returns. |
| V8 | Keyboard only, desktop. |
| V9 | No JavaScript or a slow network: the link still reaches `#contact`, and the phone, WhatsApp and mail links are visible. |
| V10 | Read the whole page on a phone: offer, trust, clarity, and one voice across the call-to-action labels. |

## 7. Severity for a lead surface

| Severity | Meaning |
|---|---|
| **P0** | Any of: a visitor cannot complete V1–V3 confidently; a lead can be lost silently or thanked falsely; the page moves unexpectedly; a common device or width breaks; a keyboard or screen-reader blocker on the core task. |
| **P1** | Significant friction, confusion or a trust gap on a primary path, or clearly below the bar on a primary surface. |
| **P2** | Polish, delight or refinement. |

| Effort | Meaning |
|---|---|
| **S** | Under an hour, CSS, copy, or one function. |
| **M** | A few hours. |
| **L** | A day or more, or out of scope (§4). |

## 8. Output, in this exact shape (markdown, returned as your final message)

```
## <agent> — brand site lead dialog and page

### Not applicable from my definition
<one line>

### Findings
| ID | Sev | Effort | Surface / state | Finding | Proposed fix (generator file + exact CSS/HTML/JS, or Hebrew copy with the current string) | Evidence |
|---|---|---|---|---|---|---|
| <DIM>-01 | P0 | S | ... | ... | ... | shot:`...png` or `file:line` |

### World-class upgrades (beyond defects — what would make this the best lead flow in its category)
1. ...

### Visitor task results
| Task | Result (PASS / FRICTION / FAIL) | Where it breaks |
|---|---|---|

### Scorecard
| P0 | P1 | P2 | Status (GREEN ≤2 P1 and no P0 / AMBER / RED any P0) |
```

- Be exhaustive and specific: name the pixel, the line and the string.
- Prefer one precise finding over a vague theme.
- Do not pad. If something is excellent, say so in one line.
- Do not edit any file. This is read-only, and your report is the deliverable.

## 9. Round 2 (2026-09-27): what changed, and what was decided on round 1

The six round-1 reports are in `reports/`. Round 1 did not pass: A11Y was RED (2 P0), DEVICE and
INTER were AMBER. Round 2 audits the preview built from `8cf918d` on the branch
`claude/caveman-ponytail-sd3opc`.

### 9.1 Tom's flow (2026-09-27, in writing; settled, do not reopen)

1. **Businesses only.** The form first asks `יש לכם עסק?` (`אנחנו עובדים רק עם עסקים, בסיטונאות.`),
   with `כן, יש לי עסק` and `לא, לשימוש פרטי`. "No" shows that private buyers get GT at Elita Ofek's
   shop, with a link to its GT page (`https://elitaofek.co.il/product-category/gt/`) and `חזרה`.
   Nothing is sent. The answer holds for the visit.
2. **The details**, as in round 1.
3. **After a send**, `מה הכי מעניין אתכם?` with five links: `מאצ׳ה`, `אובה`, `צ׳אי מסאלה`,
   `תמציות תה` and `בניית תפריט משקאות בעסק שלי`. Each opens the lead number's WhatsApp
   (`wa.me/972547588132`) with `היי, אני מעוניין ב…` already written. The dialog does not close on a
   timer. It closes when the visitor comes back to the page from WhatsApp.
4. **No "tasting"** anywhere.
5. **Partnership, not a price list** (Tom, 2026-09-27, in writing: `כפתור שהוא מעבר למחירון, שהוא מוביל
   לשותפות עסקית ביחד ותחילת עבודה איתנו`). The page's five lead links and the dialog's heading read
   `בואו נעבוד יחד`; each hero slide's link reads `הוסיפו לתפריט`, as the product window's does, and sends
   its collection as the interest. The contact line and the closing banner speak of building the drinks
   menu together. No link preselects the price list, and the optional interest list no longer offers it.
   The words are the session's; COPY judges them (gate record §5.5, U-24 and U-25).
6. **Out of scope:** the automatic reply that sends the line's menu PDF on WhatsApp. Tom approved it;
   it is a separate build, and until it is live a person sends it. The copy says only
   `נשלח לכם את התפריט בוואטסאפ.`

### 9.2 Round-1 findings: fixed

A11Y-01, INTER-03, FLOW-01 and DEV-05 (no timer) · A11Y-02 (the product window is a named modal; its
title takes focus, and the card takes it back) · A11Y-03 and INTER-02 (each step focuses its
question; on touch the form focuses its heading) · A11Y-04 and A11Y-05 (the modal buttons are named)
· A11Y-06 (every failing text colour is darkened by the smallest step that clears 4.5:1) · A11Y-11 ·
DEV-01 (the grab handle is gone) · VIS-02 (`lead.fits.send`) · INTER-04 · COPY-03 · COPY-02 and FLOW-03
(one voice: §9.1 item 5).

### 9.3 Round-1 findings: not changed, with the reason (the governor rules on each)

| Finding | Why it stays |
|---|---|
| INTER-01 (the product window stays open) | Not reproduced: its link's own `onclick` closes it before the dialog opens (`src/index.html`, `#fmodal a.cta`). Round 2 measures it: `lead.ctas[].fmodalAfter`. |
| VIS-09 (the step arrows point back) | Already `←` in RTL: `tools/patch_rtl_shell.py`, `.step:not(:last-child):after{…content:'←'}`. |
| COPY-01 (the About placeholder's alt text) | Not on the page: `tools/patch_claims.py` removes the block. |
| VIS-01 (photo on the right, form on the left from 880 px) | The product window, which the dialog follows, has its photo on the right too; a visitor on the V3 path sees one arrangement, not two. |
| DEV-02 (the × on the left) | All four of the page's modals put it on the left (`tools/patch_rtl_shell.py`: `.fmodal .x,.cm-x,.pm-x{right:auto;left:22px}`); the dialog matches them. |
| DEV-04 (landscape keyboard over the send button) | Inferred, not observed; a lead form in landscape on a phone is rare. Accepted as a P1 until a device shows it. |
| A11Y-07 (heading order) | Pre-existing across 29 card titles; the fix is the page's heading outline, not this work. Accepted as a P1. |
| P2s not listed in §9.2 | Deferred to the report. |

### 9.4 New evidence (the harness, extended)

- Shots: `-lead-02-open` is now the business question; `-lead-02b-form` is the form after `כן`
  (every viewport); `-lead-06-private` is the private-buyer answer (p390, d1360). `-lead-04-sent` is
  the thanks and the five lines; `-lead-05-after-close` is the page after the visitor came back.
- Facts: `lead.ask` (the two answers: label, height, on screen), `lead.form`, `lead.fits.send`,
  `lead.steps` (no, back, yes, reopen; `sends` must be 0), `lead.replies.ok` (`stayedOpen`,
  `focusSent`, `lines[]` with each link's target and message, `openWhileAway`, `closedOnReturn`,
  `y2`), `lead.ctas[]` (`fmodalFocus`, `fmodalAfter`), `lead.noJs` and `lead.deepLink` (`asks`,
  `fieldsShown`).
- The harness cannot hide a page. It records `openWhileAway` after the WhatsApp page opens, then
  signals the page hidden and visible again, which is what a phone does when the visitor switches back.

### 9.5 Tasks added to §6

| Task | The visitor and what they do |
|---|---|
| V11 | A private buyer: opens the dialog, answers no, understands that GT sells only to businesses, reaches Elita Ofek's GT page. Nothing reaches sales. |
| V12 | After a send: picks a line, WhatsApp opens with the message written; coming back, the dialog is gone and the page is where it was. |

V1 now starts with `כן, יש לי עסק`. V6 reopens to the thanks and the five lines.

### 9.6 What each dimension does in round 2

1. For each of your round-1 findings: FIXED, OPEN or ACCEPTED (§9.3), with the evidence that shows it.
2. Audit the new steps (§9.1) in your dimension, V11 and V12 included.
3. Report in the §8 shape, with only the findings that are open now.
