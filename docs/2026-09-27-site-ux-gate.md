# UX release gate: the brand site's lead dialog and page (2026-09-27)

The gate for `gt-factory-os-production-brain/docs/plans/2026-09-27-brand-site-lead-modal-masterprompt.md`.
Six dimensions audited the preview theme `186698334449` in two rounds: FLOW, INTER, VIS, COPY, A11Y and
DEVICE. The brief is `2026-09-27-site-ux-gate/BRIEF.md` (§9 for round 2). The reports are saved verbatim
in `2026-09-27-site-ux-gate/reports/` (round 1) and `reports/round2/`. The prompts, as sent, are in
`prompts/` and `prompts/round2/`.

**SHIP rule:** no P0, and every dimension GREEN (at most two P1s), signed off by `factory-os-governor`,
in at most three rounds.

## 1. Round 1 — HOLD

| Dimension | P0 | P1 | P2 | Status |
|---|---|---|---|---|
| FLOW | 0 | 1 | 3 | GREEN |
| INTER | 0 | 3 | 3 | AMBER |
| VIS | 0 | 2 | 7 | GREEN |
| COPY | 0 | 2 | 3 | GREEN |
| A11Y | 2 | 5 | 4 | RED |
| DEVICE | 0 | 3 | 2 | AMBER |

The two P0s were A11Y-01 (the two-second close cut the thanks off for a screen reader) and A11Y-02 (the
product window had no dialog role, no name and no focus management, on the V3 path).

## 2. Between the rounds

**Tom's decisions (2026-09-27, in writing; recorded in the masterprompt §1.1):**
- No "tasting" anywhere.
- Businesses only. The dialog first asks whether the visitor has a business. A private buyer is sent to
  Elita Ofek's GT page, and nothing reaches sales.
- After a send, "what interests you most": matcha, ube, chai masala, tea concentrates, or building a
  drinks menu. Each opens the lead number's WhatsApp (054-758-8132) with his message already written.
- The calls-to-action invite a partnership, not a price list. The page's links and the dialog's heading
  read `בואו נעבוד יחד`, and a drink's link reads `הוסיפו לתפריט`.

**Fixed** (BRIEF §9.2):
- A11Y-01, INTER-03, FLOW-01 and DEV-05: there is no timer; the dialog closes when the visitor comes back
  from WhatsApp.
- A11Y-02: the product window is now a named modal dialog.
- A11Y-03 and INTER-02: each step focuses its question.
- A11Y-04 and A11Y-05: the modals' buttons have names.
- A11Y-06: the page's failing colours are darkened by the smallest step.
- A11Y-11, DEV-01, VIS-02, INTER-04, COPY-03.
- COPY-02 and FLOW-03: resolved by the partnership calls-to-action.

**Kept, with the reason** (BRIEF §9.3; round 2 agreed with each):
- INTER-01, VIS-09 and COPY-01 were not reproduced on the page.
- VIS-01 and DEV-02 stay as they are, to match the page's four other modals.
- DEV-04 is inferred, not observed.
- A11Y-07 is pre-existing.

**Found by the round-2 harness and fixed before the audit:** the sender took the form's first button,
which became "כן, יש לי עסק" once the question was added, so the send button stayed live during a send
(`ba4985b`).

## 3. Round 2 — all GREEN

Audited on the build `8cf918d`.

| Dimension | P0 | P1 | P2 | Status |
|---|---|---|---|---|
| FLOW | 0 | 0 | 2 | GREEN |
| INTER | 0 | 0 | 3 | GREEN |
| VIS | 0 | 0 | 7 | GREEN |
| COPY | 0 | 0 | 1 | GREEN (U-16 to U-25 approved) |
| A11Y | 0 | 1 | 4 | GREEN |
| DEVICE | 0 | 1 | 1 | GREEN |

**The two P1s:**
- **A11Y-R2-01**, one contrast node: axe on the preview names it
  `.tea2 > .ghost[aria-hidden="true"]`, the 180 px "TEA 2.0" watermark at 1.13:1. It is decoration,
  hidden from assistive technology (`patch_a11y.py`, 2026-09-03). WCAG 1.4.3 exempts pure decoration.
  **Accepted.**
- **DEVICE-R2-01**: the phone sheet jumped 406 px in one frame when the visitor answered "yes".
  **Fixed after round 2** (`9a7944d`). A step now animates the dialog's height over 0.32 s, and so does
  the thanks. Measured on the preview at p390: 285 → 522 → 610 → 697 → 706 → 712 → 714 px at 0, 60,
  120, 180, 240, 300 and 400 ms. At t768: 285 → 519 px over the same time. Under reduced motion it is
  instant, and from 880 px the card keeps one height.

**P2s fixed with it** (`9a7944d`):
- VIS-R2-01: the reply-time line shows only with the form.
- INTER-R2-01: tap feedback on the five lines and "back".
- VIS-R2-07: a slide's "הוסיפו לתפריט" is an outlined pill beside the recipes pill.

**P2s deferred, with the reason:**
- **Required-field markers** (DEV-03, INTER-05, A11Y-R2-04): every visible field is required, and the
  optional ones are marked `(לא חובה)` behind their disclosure. Marking the optional fields when most are
  required is the convention; each input carries `required` for assistive technology.
- **The product's name shown in the dialog** (FLOW-02): the lead carries it already. Showing it is new copy
  and a new element, for Tom's next copy round.
- **A call-to-action after the operations section** (FLOW-04): it adds a link to the page, so it is Tom's
  call.
- **Two-phase send label** (INTER-06): new copy, and the hold is under a second for most visitors.
- **"Opens in a new window" for screen readers** (A11Y-R2-05): the lines' group is labelled
  `מה הכי מעניין אתכם? נשלח לכם את התפריט בוואטסאפ.`, which names the destination.
- **Frame titles and landmarks** (A11Y-R2-02, A11Y-R2-03): the frames are Shopify's own; landmarks need a
  page-structure change.
- **Colour tokens** (VIS-R2-02 to VIS-R2-05): no visible change. A new `:root` token is Tom's to authorise.
- **The close glyph** (VIS-R2-06): an SVG for Android's `✕`, as polish.
- **A stale source string** (COPY-04): `t0495` is overwritten by `patch_form.py` and never shown.
  Changing it means moving that patch's anchor.

## 4. Evidence

- **Harness:** `gt-factory-os/api/scripts/site_ipad_shots.mjs`, run against the preview with the intake
  stubbed, at 11 viewports.
- **Round 2 on `8cf918d`:**
  - 19 of 19 calls-to-action at p390 and d1360: open, close by ×, Esc and backdrop, and the page does
    not move;
  - all seven intake answers behave correctly;
  - the private-buyer path sends nothing;
  - the 3 s hold holds;
  - no-JS and `#contact` deep links work;
  - axe on the dialog finds 0 in every state;
  - at every viewport, the fields, the consent and the send button fit unscrolled.
- **After `9a7944d`** (the build that ships), the same run: the same results at every viewport, and
  the height probe above. At p390, the offline answer's page load failed through the proxy before its
  test ran (`net::ERR_FAILED`), and it was re-run alone.
- **Evidence folders:** in the executing session's scratchpad: `gate-r2/site-ipad/` (round 2), and
  `r3-C`, `r3-D`, `r3-E` and `r3-C2` (after `9a7944d`).
- **Copy:** `node gt-factory-os/api/scripts/portal_copy_check.mjs` reports 0 unapproved, and its
  self-test fails on a planted string.

## 5. Governor sign-off

Pending.
