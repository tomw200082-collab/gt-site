#!/usr/bin/env python3
"""Make the page's claims about itself true, and remove what is not finished.

`patch_figures.py` owns the drink tables. This owns the prose that describes
them — the sentences a reader checks the tables against — plus the one
placeholder the design shipped with.

Each claim is recomputed rather than transcribed, from the same record the
tables come from or from the page's own data, so none of them can drift the
next time a price moves or a drink is added.

Two claims were checked and left exactly as written, because they are true:

  `תמצית אחת בונה עד 13 פריטים בתפריט` — the NAMASTEA masala blend appears in
  precisely 13 of the 48 menu drinks (verified against COLS).
  `ומוזגת 20–25 כוסות` — a 1 l bottle at the recipes' 40–50 ml dose.

One claim was put to Tom and decided, so it is deliberately untouched:

  `20–30% פחות אלכוהול מאשר לפני עשור` — no source exists anywhere in the repo.
  Raised on 2026-08-31; Tom's answer was to leave it exactly as written, so it
  is `user_confirmed` rather than unsourced (`docs/2026-08-31_decisions.md`
  D-1). Do not re-open it as a finding and do not rewrite the sentence.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"
RECORD = ROOT / "data" / "drinks_final_figures.json"

applied: list[str] = []


def die(msg: str) -> None:
    sys.exit(f"FAIL [patch_claims]: {msg}")


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        die(f"{label}: expected {count} occurrence(s) of {old!r}, found {n}")
    applied.append(f"{label}: {old.strip()!r} -> {new.strip()!r}" if new else f"{label}: removed")
    return text.replace(old, new, count)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    record = json.loads(RECORD.read_text(encoding="utf-8"))["pages"]

    def num(v):
        return float(re.sub(r"[^\d.]", "", str(v)))

    min_cost = min(num(v["cost"]) for v in record.values())
    max_marg = max(int(num(v["marg"])) for v in record.values())

    # ── the two headline figures, from the record ───────────────────────
    # Both were the superseded set's min/max: ₪3.25 was the old cheapest cup
    # and 85% the old best margin. The record's are ₪2.85 and 87%, both from
    # מאצ'ה אגבה על הקרח.
    text = sub("cheapest cup", "עלות חומר גלם מ־₪3.25 לכוס",
               f"עלות חומר גלם מ־₪{min_cost:.2f} לכוס", text)
    text = sub("best margin", "רווחיות של עד 85% בהגשות העליונות",
               f"רווחיות של עד {max_marg}% בהגשות העליונות", text)

    # The same two figures again, as the stat cards beside that paragraph and
    # in the Tea 2.0 band. The superseded values had survived there, so the
    # page argued ₪2.85 / 87% in one sentence and ₪3.25 / 85% three lines
    # below it (found by the 2026-09-03 UX review).
    text = sub("stat margin", '<b class="num">85%</b>',
               f'<b class="num">{max_marg}%</b>', text)
    text = sub("band margin", '<b style="color:var(--fresh)">85%</b>',
               f'<b style="color:var(--fresh)">{max_marg}%</b>', text)
    text = sub("stat cost", '<b class="num">₪3.25</b>',
               f'<b class="num">₪{min_cost:.2f}</b>', text)

    # ── what the flavour cards actually hold ────────────────────────────
    # The cards render from MK, except the three pouch flavours, which render
    # their matching COLS collection. Count both the way the page does.
    cols = json.loads(re.search(r"const COLS=(\[.*?\]);", text, re.S).group(1))
    mk = re.search(r"const MK=\{(.*?)\n\};", text, re.S).group(1)
    products = json.loads(re.search(r"(?:const|var) FLCARD=(\{.*?\});", text, re.S).group(1))
    pouch = json.loads(
        re.search(r"var POUCHCH=(\{.*?\});", text, re.S).group(1).replace("׳", "׳")
    )
    by_title = {c["t"]: c for c in cols}

    drinks = len(re.findall(r'\{t:"', mk))
    for title in pouch.values():
        if title in by_title:
            drinks += len(by_title[title]["drinks"])

    if not 1 <= drinks <= 200:
        die(f"flavour-card drink count came out as {drinks} — refusing to write it")

    text = sub("flavour-card count", "מה יוצא מכל מוצר — 51 משקאות מ־12 מוצרים",
               f"מה יוצא מכל מוצר — {drinks} משקאות מ־{len(products)} מוצרים", text)

    # ── the placeholder ─────────────────────────────────────────────────
    # The About section opens with a slot for factory and team photographs that
    # were never supplied. It cannot go live either way: with the placeholder it
    # says so out loud, and empty it is a gap in the layout. Removed here; the
    # photographs are Tom's to provide, and the block returns with them.
    text = sub(
        "About placeholder",
        '  <div class="ph rv">תמונות מפעל וצוות — ממתין לחומרים</div>\n',
        "",
        text,
    )
    # The section is a two-column grid whose first column was that block, so
    # removing it alone would leave half the row empty. One column until the
    # photographs arrive; restoring the block restores the pair.
    text = sub(
        "About single column",
        ".about .in{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}",
        ".about .in{display:grid;grid-template-columns:1fr;gap:60px;align-items:center;"
        "max-width:760px}",
        text,
    )

    SRC.write_text(text, encoding="utf-8")
    print(f"claims: {len(applied)} rewritten")
    for a in applied:
        print("  " + a)


if __name__ == "__main__":
    main()
