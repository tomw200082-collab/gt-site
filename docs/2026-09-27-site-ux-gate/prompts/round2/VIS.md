<!-- As sent by the 2026-09-27 gate, round 2. Evidence paths are the executing session's scratchpad (regenerate with BRIEF §5). -->

You are running as `visual-system-designer` for the VIS dimension of the `/ux-release-gate` for GT's BRAND SITE (gteveryday.com), ROUND 2. Round 1 did not pass. Tom then set the lead flow (BRIEF §9.1), and the fixes and the decisions on round 1 are in BRIEF §9.2 and §9.3.

STEP 1 — read `/home/user/gt-site/docs/2026-09-27-site-ux-gate/BRIEF.md` in full; §9 is new. Read your round-1 report, `/home/user/gt-site/docs/2026-09-27-site-ux-gate/reports/VIS.md`, and your round-1 prompt, `/home/user/gt-site/docs/2026-09-27-site-ux-gate/prompts/VIS.md`: its checks still apply. Then read `/home/user/gt-site/tools/patch_lead_dialog.py` in full, the round's change (`git -C /home/user/gt-site diff 1a276ec 8cf918d -- tools/ i18n/`), and the built `/home/user/gt-site/src/index.html` around `#contact`, the dialog and its script. Open the evidence in `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/` (Read renders PNGs) with `site_ipad_facts.json`. Round 1's evidence is in `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r1/site-ipad/`.

DO (BRIEF §9.6):
1. Each of your round-1 findings: FIXED, OPEN or ACCEPTED, with the shot or fact that shows it. Where §9.3 keeps a finding of yours unchanged, say whether the reason holds; if it does not, the finding is open, with its severity.
2. The new steps, in your dimension: the three new states (`-lead-02-open`, `-lead-06-private`, `-lead-04-sent`) at every width you have: hierarchy, rhythm, the answers' weight, the five pills, the divider in the sent state, the page's darkened colours (eyebrows, card origins) against the brand, and the new call-to-action words on every button they sit on (the nav pill on phones, the hero, the slides' links, the closing banner): length, wrapping, weight.
3. V11 and V12 (BRIEF §9.5), and V1 and V6 as they run now.

OUTPUT: exactly the shape in BRIEF §8 (ID prefix VIS-R2-), opening with a table "Round-1 findings" (ID · FIXED / OPEN / ACCEPTED · evidence), then only the findings open now. Exhaustive, concrete, no padding. Read-only: do not edit, create or delete any file anywhere.
