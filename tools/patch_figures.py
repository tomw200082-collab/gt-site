#!/usr/bin/env python3
"""Write every drink figure on the page from the figures of record.

`docs/pricing/2026-08-27_COST_MODEL.md` names
`.claude/skills/drinks-pricelist/drinks_final_figures.json` as the figures of
record. This step makes that file the only place a drink price, food cost or
margin is written down: the page states its figures across five separate
surfaces, and before this step all five carried the superseded 2026-08-05 set.

The five surfaces:

  1. `COLS[].drinks[]`  — `fc` food cost, `p` price, `m` margin, `pr` profit/cup.
                          Rendered in the drink modal and the collection lists.
  2. `COLS[].p`         — the collection's headline "recommended price", shown
                          in the hero chips and the ticker. Derived: one price
                          if the collection's drinks agree, else a `₪min–max`
                          range. The design already uses that range form for
                          the wholesale list, so it is not a new idiom.
  3. `MK[flavour][]`    — the "menu drinks it makes" rows on the flavour cards,
                          which carry their own titles and their own copy of
                          `p` / `m` / `fc`.
  4. The static collection cards in the markup, which repeat `COLS[].p` in
     hand-written HTML.
  5. The scrolling ticker under the hero, which repeats eight of them again,
     twice each, under its own shortened labels. It was the last one found, and
     only by looking at a render — the DOM was correct and the figures were a
     month old.

Nothing here computes a figure. Every number is copied from the record, and
anything the record does not cover halts the build rather than being guessed.

Run after the other patches — it is the last word on any number.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"
RECORD = ROOT / "data" / "drinks_final_figures.json"

# ── name resolution ─────────────────────────────────────────────────────
# 47 of the 48 drink names on the page are byte-identical to the record. One
# differs, and it is resolved by elimination rather than by guesswork:
#
#   The page's cold-infusion collection holds exactly 7 drinks; the record's
#   cold-infusion block (pages 8-14) holds exactly 7 entries; 6 of the 7 names
#   match exactly on both sides. Only one name is left on each side, so the
#   pairing is forced. It is also figure-irrelevant: the record gives all seven
#   cold infusions identical cost, price and margin, so this drink takes the
#   same numbers whichever of the two names it is filed under.
#
# The wording difference itself (the page names the lemon verbena, the record
# does not) is a copy question for Tom, not a figures question.
ALIAS = {
    "חליטת תה ירוק לואיזה וליים": "חליטת תה ירוק וליים",
}

# The page's cold-infusion class. Every member carries identical figures in the
# record; `cold_infusion_class()` asserts that before relying on it.
COLD_INFUSIONS = (
    "חליטת היביסקוס וליים",
    "חליטת קמומיל ותפוח",
    "חליטה מדברית",
    "חליטת סנצ'ה ופסיפלורה",
    "חליטת תה ירוק וליים",
    "חליטת תה ירוק ולמון גראס",
    "חליטת יסמין וליצ'י",
)

# ── MK: flavour-card rows -> the record ─────────────────────────────────
# MK rows carry their own marketing titles rather than the menu drink names, so
# the mapping is written out rather than matched. Each entry is (title, record
# name); `None` means "the cold-infusion class figure" — used only for
# AMERICAN, which is a Tom-approved tea extract
# (`gt-factory-os-production-brain/docs/warehouses/catalog-truth.md`, grade
# מאושר-טום, ₪65/₪33, no active SKU) whose cold infusion is the same
# preparation as the other seven but is not itself one of the 48 menu drinks.
MK_MAP = {
    "Detox": [
        ("חליטת Detox קרה — רגילה או מוגזת", None),
        ("משקה דגל תות־לואיזה", "חליטת תות לואיזה"),
    ],
    "Revive": [
        ("חליטת Revive קרה — רגילה או מוגזת", None),
        ("משקה דגל מנגו־סנצ׳ה", "חליטת מנגו סנצ'ה"),
    ],
    "Energy": [
        ("חליטת Energy קרה — רגילה או מוגזת", None),
    ],
    "Consciousness": [
        ("חליטת יסמין־ליצ׳י", "חליטת יסמין וליצ'י"),
        ("גזוז ליצ׳י", "גזוז יסמין וליצ'י"),
    ],
    "American": [
        ("חליטת American קרה — רגילה או מוגזת", None),
    ],
    "Fresh": [
        ("חליטת Fresh", "חליטת היביסקוס וליים"),
        ("לימונדת היביסקוס־ליים", "לימונדת היביסקוס וליים"),
        ("משקה דגל תפוח־היביסקוס", "חליטת תפוח היביסקוס"),
        ("גזוז היביסקוס־תפוח", "גזוז היביסקוס ותפוח"),
    ],
    "Desertea": [
        ("חליטה מדברית", "חליטה מדברית"),
        ("לימונדה מדברית", "לימונדה מדברית"),
        ("משקה דגל מדברי־אפרסק", "חליטת אפרסק מדברית"),
        ("גזוז מדברי־אפרסק", "גזוז מדברי ואפרסק"),
    ],
    "Calm": [
        ("חליטת קמומיל־תפוח — רגילה או מוגזת", "חליטת קמומיל ותפוח"),
    ],
    "Namastea": [
        ("אייס צ׳אי מסאלה קלאסי", "אייס צ'אי מסאלה קלאסי"),
        ("צ׳אי מסאלה על קרח", "צ'אי מסאלה על הקרח"),
        ("דירטי צ׳אי (עם אספרסו)", "דירטי צ'אי"),
        ("צ׳אי וטוניק תפוז מיובש", "צ'אי מסאלה תפוז וטוניק"),
        ("טוניק ורדים ורוד", "צ'אי מסאלה פינק טוניק"),
        ("צ׳אי קולד פואם וניל", "צ'אי מסאלה קולד פואם וניל"),
    ],
}

# The static collection cards, keyed by the English kicker that precedes each.
CARD_ANCHORS = [
    "Iced Tea", "Lemonade", "Signature", "Gazoz", "Ice Matcha",
    "Matcha Specials", "Matcha Coconut", "Chai Massala", "Cold Foam", "Ube",
]

# The scrolling ticker under the hero: eight of the ten collections, in its own
# order, under shortened labels, and written out twice so the strip can loop.
# Its labels are not the collection names — `קולד פואם` is the chai cold-foam
# collection, and it spells the geresh differently — so the mapping is by
# position in COLS rather than by matching the text.
TICKER = [
    ("חליטות קרות", 0),
    ("לימונדות", 1),
    ("גזוז", 3),
    ("משקאות הדגל", 2),
    ("אייס מאצ׳ה", 4),
    ("צ׳אי מסאלה", 7),
    ("קולד פואם", 8),
    ("אובה", 9),
]

changes: list[tuple[str, str, str, str]] = []


def die(msg: str) -> None:
    sys.exit(f"FAIL [patch_figures]: {msg}")


def money(v: str) -> str:
    """'₪13.70 לכוס' -> '13.70';  '₪20' -> '20';  '81%' -> '81'."""
    return re.sub(r"[^\d.]", "", str(v).split("לכוס")[0])


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    by_name = {v["name"]: v for v in record["pages"].values()}
    if len(by_name) != record["_meta"]["pages_total"]:
        die(f"record holds {len(by_name)} distinct names, _meta says {record['_meta']['pages_total']}")

    # The cold-infusion class figure, asserted uniform before it is used.
    figures = {by_name[n]["cost"] + "|" + by_name[n]["price"] + "|" + by_name[n]["marg"]
               + "|" + by_name[n]["prof"] for n in COLD_INFUSIONS if n in by_name}
    if len(figures) != 1:
        die("the record no longer gives every cold infusion the same figures; "
            "the AMERICAN row can no longer be derived — resolve with Tom")
    cold = by_name[COLD_INFUSIONS[0]]

    def lookup(name: str | None) -> dict:
        if name is None:
            return cold
        entry = by_name.get(ALIAS.get(name, name))
        if entry is None:
            die(f"{name!r} is not in the figures of record — halt rather than guess")
        return entry

    # ── 1 + 2. COLS ─────────────────────────────────────────────────────
    m = re.search(r"const COLS=(\[.*?\]);", text, re.S)
    if not m:
        die("could not find `const COLS=[...]`")
    cols = json.loads(m.group(1))
    if len(cols) != len(CARD_ANCHORS):
        die(f"expected {len(CARD_ANCHORS)} collections, found {len(cols)}")

    headline: list[str] = []
    for col in cols:
        prices = []
        for d in col["drinks"]:
            r = lookup(d["he"])
            for field, new in (
                ("fc", money(r["cost"])),
                ("p", int(money(r["price"]))),
                ("m", int(money(r["marg"]))),
                ("pr", money(r["prof"])),
            ):
                if d[field] != new:
                    changes.append((f"COLS/{d['he']}", field, str(d[field]), str(new)))
                d[field] = new
            prices.append(d["p"])
        lo, hi = min(prices), max(prices)
        new_p = f"₪{lo}" if lo == hi else f"₪{lo}–{hi}"
        if col["p"] != new_p:
            changes.append((f"COLS/{col['he']}", "p", col["p"], new_p))
        col["p"] = new_p
        headline.append(new_p)

    text = text[: m.start(1)] + json.dumps(cols, ensure_ascii=False) + text[m.end(1):]

    # ── 3. MK ───────────────────────────────────────────────────────────
    mk = re.search(r"const MK=\{.*?\n\};", text, re.S)
    if not mk:
        die("could not find `const MK={...}`")
    block = mk.group(0)
    seen = 0
    for flavour, rows in MK_MAP.items():
        if f'"{flavour}":[' not in block:
            die(f"MK has no {flavour!r} group")
        for title, target in rows:
            r = lookup(target)
            pat = re.compile(
                r'(\{t:"' + re.escape(title) + r'",p:)(\d+)(,m:)(\d+)(,fc:")([\d.]+)(")'
            )
            found = pat.findall(block)
            if len(found) != 1:
                die(f"MK row {title!r}: expected 1 match, found {len(found)}")
            new = (money(r["price"]), money(r["marg"]), money(r["cost"]))
            old = found[0]
            for field, o, n in (("p", old[1], new[0]), ("m", old[3], new[1]), ("fc", old[5], new[2])):
                if o != n:
                    changes.append((f"MK/{flavour}/{title}", field, o, n))
            block = pat.sub(lambda mm: mm.group(1) + new[0] + mm.group(3) + new[1]
                            + mm.group(5) + new[2] + mm.group(7), block)
            seen += 1
    if seen != 23:
        die(f"expected 23 MK rows, mapped {seen}")
    text = text[: mk.start()] + block + text[mk.end():]

    # ── 4. the static collection cards ──────────────────────────────────
    for anchor, new_p in zip(CARD_ANCHORS, headline):
        pat = re.compile(
            r'(<div class="heh">' + re.escape(anchor) + r"</div>.*?"
            r"<span>מחיר מומלץ )(₪[\d–]+)(</span>)",
            re.S,
        )
        found = pat.findall(text)
        if len(found) != 1:
            die(f"collection card {anchor!r}: expected 1 match, found {len(found)}")
        if found[0][1] != new_p:
            changes.append((f"card/{anchor}", "price", found[0][1], new_p))
        text = pat.sub(lambda mm: mm.group(1) + new_p + mm.group(3), text, count=1)

    # ── 5. the ticker under the hero ────────────────────────────────────
    for label, idx in TICKER:
        want = headline[idx]
        pat = re.compile(r"(<span>" + re.escape(label) + r" <b>)(₪[\d–]+)(</b></span>)")
        found = pat.findall(text)
        if len(found) != 2:
            die(f"ticker {label!r}: expected 2 copies, found {len(found)}")
        for _, old, _ in found:
            if old != want:
                changes.append((f"ticker/{label}", "price", old, want))
        text = pat.sub(lambda mm: mm.group(1) + want + mm.group(3), text)

    SRC.write_text(text, encoding="utf-8")

    drink_prices = [c for c in changes if c[1] == "p" and c[0].count("/") == 1
                    and c[0].split("/")[1] not in {col["he"] for col in cols}]
    print(f"figures: record {record['_meta']['date']} · "
          f"{len(changes)} values rewritten across 5 surfaces "
          f"({len(drink_prices)} drink prices moved)")


if __name__ == "__main__":
    main()
