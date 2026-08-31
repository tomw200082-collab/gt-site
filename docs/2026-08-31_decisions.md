# Tom's decisions — 2026-08-31

Four open questions from the build session, answered by Tom in session, in
Hebrew. Recorded here with an authority grade because the constitution requires
one (`Sales-Machine/CLAUDE.md`, truth rule 1) and because two of them are
decisions a later session would otherwise re-open as findings.

Grade for all four: **`user_confirmed`** — Tom said it. Date: 2026-08-31.

---

## D-1 · The alcohol claim stays exactly as written

**On the page:** `האורחים שלכם שותים 20–30% פחות אלכוהול מאשר לפני עשור.`

**The concern, as raised:** no source for the 20–30% figure exists anywhere —
not in `gt-site`, not in the production brain, not in `Sales-Machine`. It is a
specific statistic on a page that sells to restaurateurs.

**Tom:** *"תשאיר בדיוק כמו שהוא."*

**Consequence.** The sentence is unchanged. Its grade moves from *unsourced* to
`user_confirmed`, which is a grade the constitution recognises — the difference
being that someone accountable has now put their name to it. It is no longer a
publication blocker, and **a later session should not re-open it as a finding.**
If a citation ever turns up, add it here; it does not change the copy.

## D-2 · Wholesale price visibility — pending, mechanism ready

**Tom:** *"אחזיר לך תשובה על זה עוד מעט — זה שיש אופציה לכבות ברגע זה מעולה!"*

**State.** Undecided. The list stays public in the meantime, which is the
design's own intent (`כל המחירים. על השולחן.`), and `U-003` in
`Sales-Machine/doctrine/pricing-logic.md` stays open.

**What was built for it.** `show_pricing` in the theme editor hides the entire
wholesale section in one click and restores it in one click. It changes no
figure and needs no deploy, so the decision is cheap in both directions and can
be made after the site is live.

## D-3 · Two copy items stay as they are

**Tom:** *"תשאיר ככה בדיוק את שניהם."*

1. **The cold infusion keeps the page's name.** The page says
   `חליטת תה ירוק לואיזה וליים`; the figures of record say
   `חליטת תה ירוק וליים`. Same drink — both sides list exactly seven cold
   infusions, six names match byte-for-byte, and the record gives all seven
   identical cost, price and margin, so the pairing is forced and
   figure-irrelevant. The page names the lemon verbena and will keep naming it.
   `tools/patch_figures.py` carries this as a deliberate `ALIAS`, not a
   mismatch to be tidied away.
2. **`Don't Drink Boring.` stays in English**, in the footer. Deliberate.

## D-4 · Every lead goes to `sales_core`, not HubSpot

**Tom:** *"שכל הלידים יעברו למערכת מכירות שלנו ולא להאבספוט כרגע."*

**Already the implemented state, verified.** There is no HubSpot script, form,
embed or endpoint anywhere in `src/`, `theme/`, `i18n/` or `tools/`. The
enquiry form posts to `website_lead_intake`, which forwards to the `/ingest`
route on `sales-leads-poll`. The only `mailto:` left is the form's own no-JS
fallback to `info@gteveryday.com`.

**Not done, and deliberately.** Nothing was migrated out of HubSpot and nothing
was closed there — "כרגע" is a routing decision, not a cleanup instruction.
Whatever sits in that account still sits there, unread by anyone we know of.
Worth a separate look, and not part of this site's work.

---

**Still Tom's, unanswered:** open the preview in a real browser; the About
photographs; the publish decision itself. All three are in `PUBLISH.md`.
