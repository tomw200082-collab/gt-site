## factory-os-governor — UX release gate for gteveryday.com

**VERDICT: PROCEED WITH CONSTRAINTS**

The gate is signed off. Round 2 met the SHIP rule at close — six-of-six dimensions GREEN, two P1s total (the maximum allowed), no P0, two rounds — and the code that ships (`9a7944d`) resolves the one remaining P1 without breaking anything the harness measured. Merge is authorised on the executor's own green checks. The live-theme push still needs Tom's own written go per masterprompt §6-C; no governor verdict substitutes for that.

---

### 1. What was decided

Release-gate sign-off for the brand-site lead dialog and page (masterprompt `/home/user/gt-factory-os-production-brain/docs/plans/2026-09-27-brand-site-lead-modal-masterprompt.md`, W5 gate + W6 hand-off + W7 pre-live check-point).

### 2. Evidence I opened and read

- `/home/user/gt-site/docs/2026-09-27-site-ux-gate.md` — both rounds, decisions, deferrals; §3 shows Round 2 = 0 P0, 2 P1 total, all six dimensions GREEN
- `/home/user/gt-site/docs/2026-09-27-site-ux-gate/BRIEF.md` — §7 severity, §9.1 Tom's flow, §9.3 accepted carry-overs
- All twelve reports — six under `reports/` (round 1) and six under `reports/round2/`
- `/home/user/gt-factory-os-production-brain/docs/plans/2026-09-27-brand-site-lead-modal-masterprompt.md` — §1.1 (Tom's decisions), §5 (scope), §6 (what is Tom's), §7 (landmines), §8 (halt conditions)
- `git log 1a276ec..HEAD` — 20 commits; the ship head is `7b77e17` (`docs(gate): the p390 re-run passed on the build that ships`); the last code commit is `9a7944d` (`fix(site): the sheet grows smoothly between steps; round-2 polish`)
- `git show 9a7944d -- tools/` — reviewed the FLIP height animation in `patch_lead_dialog.py:264-272` and the sender substitution at line 387
- `/home/user/gt-site/tools/patch_lead_dialog.py` — full file, 400 lines: `LINES` = the five approved lines with `WA_LEAD = wa.me/972547588132`, `ASK`/private step, `pf-slot` borrow of `#pform`, `was_new` gate on success, 3 s hold, `ldGrow()` FLIP animation with reduced-motion guard and 880 px opt-out
- Facts: `gate-r2/site-ipad/site_ipad_facts.json` (11 viewports, build `8cf918d`), and the four `9a7944d` runs `r3-C`, `r3-C2`, `r3-D`, `r3-E` covering p390 (twice, second is the offline re-run), d1360 and the remaining nine viewports
- Grep sweep across `theme/*` and `src/index.html`: `טעימה` appears 0 times in delivered files; `wa.me/972547588132` = the lead-flow number (Sales-Machine D-014), `054-398-2444` = the site's own contact WhatsApp — two numbers, both intended, no collision

### 3. Ruling on each named item

**The SHIP rule — met at Round 2.**
Round 2 was `0 P0 · 2 P1 · GREEN across FLOW / INTER / VIS / COPY / A11Y / DEVICE`. That is exactly the ceiling ("at most two P1s") in two rounds, well inside the three-round limit. The gate closed GREEN at that moment; `9a7944d` is a post-GREEN polish, not a re-attempt.

**A11Y-R2-01 (the one contrast node, the `.tea2 > .ghost[aria-hidden="true"]` 180 px "TEA 2.0" watermark, 1.13:1).**
Accepted. WCAG 2.2 SC 1.4.3 Exception 2 (Incidental) exempts pure decoration; the element carries `aria-hidden="true"` (round-1 patch `patch_a11y.py`, 2026-09-03) so it is programmatically hidden from assistive technology, and the record names the exact selector. This is a valid decoration exemption, not a P1 that requires a fix or a Tom-approved carve-out.

**DEVICE-R2-01 (the 285 → 714 px single-frame jump when the visitor answers "yes" on a phone).**
Fixed in `9a7944d`. The evidence is sufficient without a third audit round, for four converging reasons:

1. Round 2 was already SHIP-eligible before this fix; DEVICE-R2-01 counted as the second of two allowable P1s, so its resolution is a bonus, not a gate condition.
2. The fix's mechanism is directly readable: `ldGrow()` at `tools/patch_lead_dialog.py:266-272` captures `d.offsetHeight`, applies the class change, forces a reflow (`d.offsetHeight;`), sets `transition:height .32s cubic-bezier(.2,.8,.25,1)` and animates to the new height — the FLIP technique DEVICE-R2-01 asked for as its "M path (gold standard)". `patch_lead_dialog.py:387` wraps `f.classList.add('sent')` in the same `ldGrow()` so the thanks step also grows, not just the yes branch.
3. Reduced-motion is honoured (line 268: `matchMedia('(prefers-reduced-motion:reduce)').matches → change();return;`); the ≥880 px card is left flat (CSS at line 212: `#ldlg[open]{…min-height:min(520px,92dvh)}` plus `.ld-main{…justify-content:center}` at 215) — both landmines from BRIEF §7 and §9 respected.
4. The endpoint measurements the record cites (285 px pre, 714 px post at p390; 285 → 519 at t768) are the same numbers the `9a7944d` harness runs (`r3-C`/`r3-C2` p390.lead.open.box = [0,559,390,**285**], p390.lead.form.box = [0,130,390,**714**]; matched at t768 in `r3-E`). The intermediate frames in the record (522, 610, 697, 706, 712 at 60/120/180/240/300 ms) are the executor's own probe of the running animation — they cannot be present in the JSON snapshot, which captures pre- and post-states only. That probe is not a re-audit and does not have to be one: the animation's presence is proven by the JS diff, its shape by the two endpoints, its accessibility by the reduced-motion branch, and the surrounding surface's stability by `r3-C/C2/D/E` reproducing every other Round-2 measurement (19 of 19 CTAs, page never moves, private-buyer `sends: 0`, `was_new`-gated success, `axe:[] on the dialog, `openWhileAway / closedOnReturn: true`, offline recovered on the re-run).

A third audit round is not required and would not add signal.

**Each deferred P2 — accepted, with the record's reasons standing.**
- **Required-field markers (DEV-03 / INTER-05 / A11Y-R2-04):** every visible field is required; the convention when most fields are mandatory is to mark the optional ones (which the disclosure does with `(לא חובה)`), and `required` is on for AT. Accepted.
- **Product name shown in the dialog (FLOW-02):** the lead carries `ldCtx` at send; showing it is new visible copy and belongs to Tom's next copy round. Accepted; put on the follow-up list.
- **CTA after the operations section (FLOW-04):** adds a new page link, which is Tom's call. Accepted; put on the follow-up list.
- **Two-phase send label (INTER-06):** new copy; measured hold is 712 ms on cache-warm pages, under a second. Accepted.
- **"Opens in a new window" SR announcement (A11Y-R2-05):** the `.pf-lines` group is already labelled `נשלח לכם את התפריט בוואטסאפ.`, which names the destination. Accepted.
- **Frame titles + landmarks (A11Y-R2-02, A11Y-R2-03):** the frames are Shopify's own; landmarks need a page-structure change outside this work. Accepted.
- **Colour tokens (VIS-R2-02 to VIS-R2-05):** no visible change; a new `:root` token is a design-token addition and needs Tom. Accepted.
- **Close glyph SVG (VIS-R2-06):** polish for Android's `✕` rendering. Accepted.
- **Stale source string (COPY-04):** `t0495` is overwritten by `patch_form.py` and never rendered; changing it means moving that patch's anchor. Accepted; documented as maintenance. Note: the same class of orphan applies to `t0483: "טעימה במקום"` in `i18n/parts/he_visible_3.py:112` — the source string still holds the word "tasting", but grep confirms 0 occurrences in `theme/sections/gt-home.liquid`, `theme/assets/gt-site.{css,js}` and `src/index.html`, and the only other reference is `FIELDS_OLD` in `patch_lead_dialog.py:89`, which is the *needle* for the substitution that replaces it with `FIELDS_NEW` (which contains no "טעימה"). Tom's "אל תכתוב טעימה" rule is respected on the delivered page. The source string should be scheduled with COPY-04 in a next copy-cleanup pass; it is not a gate blocker.

None of the deferrals must be fixed before merge. All are polish-tier and none touches the lead pipeline, the intake contract, or a Tom-locked decision.

**Contradictions with locked decisions — none found.**
- Brain `CLAUDE.md`: stock truth untouched, no frozen flag flipped (`SHOPIFY_FG_SYNC_LIVE_ADAPTER_WIRED`, `SHOPIFY_FULFILLMENT_BRIDGE_LIVE_ADAPTER_WIRED`, `SHOPIFY_BLIND_AVAILABLE_WRITE_ENABLED`, `LIONWHEEL_FG_OUT_BRIDGE_ENABLED`, `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` all unchanged), no factory-os core touched, no new authority docs, no `git add -A`, watching stays opt-in.
- Masterprompt §1.1: no "טעימה" delivered · businesses-only ask step present (`patch_lead_dialog.py:124-133`) with the Elita Ofek URL and `חזרה` back button · five approved WhatsApp lines with the sales lead number 054-758-8132 (`patch_lead_dialog.py:135-136`; distinct from the site's contact 054-398-2444, which stays in the contact section — both numbers are intended, per Sales-Machine `CURRENT_STATE.md` U-032 and D-014) · partnership CTAs `בואו נעבוד יחד` and `הוסיפו לתפריט` (line 336 and the ten-slide substitution at 341) · no timer; dialog closes on `visibilitychange` (`patch_lead_dialog.py:301-302`).
- Intake contract unchanged: `contact_name`, `venue`, `city`, `phone`, `agree` — the four required fields sit in `FIELDS_NEW` (`patch_lead_dialog.py:98-103`); no new `form_name`; success gated on `res.ok && res.j.ok && 'was_new' in res.j` (line 381); the 3 s hold is measured from navigation start via `Math.max(0, 3050 - performance.now())` (line 375). The `website_lead_intake` endpoint is not modified.
- One form: `#pform` is borrowed into the dialog (`patch_lead_dialog.py:286`) and returned to `#pf-slot` on close (line 307).
- No prices on the served page: `strip_prices.py` untouched; the automatic PDF-reply flow is explicitly a **separate build** behind `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` per §1.1 and is not implemented here — the pick-step subline promises only what a person can deliver today (`נשלח לכם את התפריט בוואטסאפ.`).
- Lane hygiene: writes limited to `gt-site` (patch + docs + built theme outputs) and `gt-factory-os` (harness `api/scripts/site_ipad_shots.mjs`, `SITE_FILES`, gate `§5.5` U-16…U-25 rows). No overreach into portal source, `api/src/portal/`, `supabase/functions/*` beyond harness, or any frozen surface. No cross-lane write.

### 4. Verdict

**PROCEED WITH CONSTRAINTS.** The gate closes SHIP. Merge is authorised on each PR's own green checks. Live theme push is not authorised until Tom's own written go per §6-C.

### 5. Constraints the merge and the live step must honour

C1. Before the executor merges gt-site, add my sign-off line to `/home/user/gt-site/docs/2026-09-27-site-ux-gate.md` §5 replacing "Pending." with a governor line pointing at Round-2 GREEN + the four `9a7944d` polish fixes + the `r3-*` non-regression + this verdict. That is the record D7 asks for.

C2. The height probe (285 → 522 → 610 → 697 → 706 → 712 → 714 at 0/60/120/180/240/300/400 ms on p390; 285 → 519 at t768; instant under reduced motion; flat from 880 px) is load-bearing evidence for accepting DEVICE-R2-01 without a third round. It stays in the record as-is; do not silently prune it in a later edit.

C3. The five follow-up items — FLOW-02 (kicker showing the product), FLOW-04 (CTA after the operations block), INTER-06 (two-phase send label), the required-field marker decision (DEV-03 / INTER-05 / A11Y-R2-04), and the orphan `t0483 = "טעימה במקום"` alongside COPY-04's `t0495` — are Tom's copy-round work. Name them in the gt-site PR body and in the Hebrew report §5 ("what is still Tom's") so they do not silently drop.

C4. The automatic PDF-on-WhatsApp reply named in §1.1 item 6 stays out of this ship. When it is scheduled, it is a Sales-Machine + integration build behind `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED`, and Tom owes the dry-run and ≥24 h soak on top of the written approval already given. The pick-step copy `נשלח לכם את התפריט בוואטסאפ.` must remain a promise a person can fulfil until then.

C5. Live push must go through the masterprompt's W1/W7 protocol: stage the whole GT set → drift = 0 on the preview → Tom's §6-C word → push to live with `--allow-live --nodelete` → drift = 0 on live. No partial upload; do not duplicate any theme other than MAIN at the moment of use. If `SHOPIFY_CLI_THEME_TOKEN` is absent the W7 fallback applies (MCP upsert to a fresh MAIN duplicate, hand Tom the id, drift-check after his Publish click). The frozen flags stay `false`.

C6. Intake contract is not to change during the ship. Four required fields + agreement; no new `form_name`; `was_new` still gates success. If any executor touches `supabase/functions/website_lead_intake/`, that is a lane violation and must halt.

C7. The site's contact WhatsApp stays 054-398-2444. The lead-flow WhatsApp (054-758-8132) is a separate number from Sales-Machine D-014 and applies only to the five after-send lines in the dialog. Do not merge or replace them.

C8. Do not run the D6 verification lead until Tom's §6-C word arrives. When it does, use the identity §6-C specifies (`054-398-2444`, `בדיקת מערכת — להתעלם`), and tell Tom in the same message that this one lead reaches the sales queue and the staff alert.

### 6. Blockers

None.

### 7. Re-route

Not applicable; the SHIP condition is met.

### 8. Tom approval required?

Yes, for one thing only: the live-theme push (masterprompt §6-C). Not for merge — the executor has merge autonomy under brain `CLAUDE.md` §Authorization on each PR's own green checks and this gate's SHIP.

### 9. Next action for Tom

Read the executor's Hebrew W7 report when it arrives, open the preview link it carries, and reply with the one word `go` (or a change request) so the executor can move the GT set from the preview theme to the live theme `166730072305`. Nothing else is his: not the merge, not the drift check, not the axe re-runs.

---

**Files referenced (absolute):**
- `/home/user/gt-site/docs/2026-09-27-site-ux-gate.md`
- `/home/user/gt-site/docs/2026-09-27-site-ux-gate/BRIEF.md`
- `/home/user/gt-site/docs/2026-09-27-site-ux-gate/reports/round2/{A11Y,COPY,DEVICE,FLOW,INTER,VIS}.md`
- `/home/user/gt-factory-os-production-brain/docs/plans/2026-09-27-brand-site-lead-modal-masterprompt.md`
- `/home/user/gt-site/tools/patch_lead_dialog.py` (esp. lines 124-136, 260-272, 293-302, 336-360, 372-388)
- `/home/user/gt-site/tools/patch_form.py:38,145` (endpoint + body assembly, unchanged contract)
- `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/gate-r2/site-ipad/site_ipad_facts.json`
- `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/r3-C/site-ipad/site_ipad_facts.json`
- `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/r3-C2/site-ipad/site_ipad_facts.json`
- `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/r3-D/site-ipad/site_ipad_facts.json`
- `/tmp/claude-0/-home-user/69951ae0-cef0-56a2-ac9c-bac1353b3e2f/scratchpad/r3-E/site-ipad/site_ipad_facts.json`
- Ship head: `7b77e17`; last code commit: `9a7944d`; Round-2 build: `8cf918d`.
