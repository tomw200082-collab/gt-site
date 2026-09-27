<!-- As sent by the 2026-09-27 gate, round 1. Evidence paths are the executing session's scratchpad (regenerate with BRIEF §5). -->

You are running as `visual-system-designer` inside the `/ux-release-gate` for GT's BRAND SITE (gteveryday.com). Tom wants the lead window "very, very beautiful, simple and strong" and the page's visuals improved through this gate (2026-09-27).

STEP 1 — read `/home/user/gt-site/docs/2026-09-27-site-ux-gate/BRIEF.md` in full. It overrides the operations-portal parts of your definition: this is GT's public brand site, Hebrew RTL by Tom's approval; portal_ux_standard.md, English-first, LTR and RUNTIME_READY do not apply. Then read the generator named in BRIEF §1 (`/home/user/gt-site/tools/patch_lead_dialog.py` in full, `tools/patch_form.py`, and the built `/home/user/gt-site/src/index.html` around `#contact`, the calls-to-action and the dialog script) and open the evidence in `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r1/site-ipad/` (Read renders PNGs) with `site_ipad_facts.json`. "Before" evidence (the live theme, where every call-to-action scrolls to the form) is in `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/ux-before-lead/site-ipad/`.

YOUR DIMENSION: Visual system. You own the re-aimed `/design-system-check` and the visual part of `/screen-scorecard` (specs: `/home/user/gt-factory-os-production-brain/.claude/commands/design-system-check.md`, `.../screen-scorecard.md`).

DO:
1. The dialog against the page's own system (the `:root` tokens in `src/index.html`, the form and modal rules, the CSS block in `patch_lead_dialog.py`): colour, type scale, spacing rhythm, radii, shadows, motion. Does it read as part of this page, or as a second style? Every width: `*-lead-02-open` at p320, p390, p430, t768, the five iPads, d1360, d1920; the sheet on phones, the card from 640 px; the error and sent states.
2. The page (`*-page-NN` at p390 and d1360): hierarchy, rhythm, the first screen on a phone, density, image scale, how the calls-to-action look (primary vs secondary vs text links) and whether their visual weight matches their job.
3. Compute contrast for every text in the dialog (labels on paper, the disclosure green, the consent grey, the error box, the sent state) and for the calls-to-action on their backgrounds (the closing banner's white on its gradient, the slides' `sub-cta`).
4. RTL: alignment, the close button's side, the disclosure marker, numerals and the phone number, the countdown bar's direction.
5. Lens references: `/home/user/gt-factory-os-portal/.claude/skills/better-ui/SKILL.md`, `better-typography/SKILL.md`, `better-layout/SKILL.md`, `better-colors/SKILL.md`, `apple-design/SKILL.md`, `/home/user/gt-factory-os-portal/.claude/skills/impeccable/reference/critique.md`, `polish.md`, `craft-floor.md`, `/home/user/gt-site/.claude/skills/taste-skill/SKILL.md`. Keep GT's brand world; state system rules, not one-off decoration.

OUTPUT: exactly the shape in BRIEF §8 (ID prefix VIS-), every visual finding with a shot path and concrete CSS values. Exhaustive, concrete, no padding. Read-only: do not edit, create or delete any file anywhere.
