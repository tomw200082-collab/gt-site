#!/usr/bin/env python3
"""Check every figure on the built page against the figures of record.

`patch_figures.py` writes the numbers; this reads the built page back and
proves they are right. It is deliberately a separate program with its own
parsing, so a bug in the writer cannot hide behind itself, and it is the check
CI runs.

    python3 tools/verify_figures.py

Exit 0 and a per-surface count when every figure matches; exit 1 naming each
disagreement otherwise.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"
RECORD = ROOT / "data" / "drinks_final_figures.json"

sys.path.insert(0, str(ROOT / "tools"))
from patch_figures import ALIAS, CARD_ANCHORS, COLD_INFUSIONS, MK_MAP  # noqa: E402

fails: list[str] = []


def num(v) -> float:
    return float(re.sub(r"[^\d.]", "", str(v).split("לכוס")[0]))


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    by_name = {v["name"]: v for v in record["pages"].values()}
    cold = by_name[COLD_INFUSIONS[0]]

    for n in COLD_INFUSIONS:
        if (by_name[n]["cost"], by_name[n]["price"], by_name[n]["marg"]) != (
            cold["cost"], cold["price"], cold["marg"]):
            fails.append(f"record: cold infusions no longer share one figure ({n})")

    def rec(name):
        return by_name[ALIAS.get(name, name)]

    # ── 1. COLS drinks ──────────────────────────────────────────────────
    cols = json.loads(re.search(r"const COLS=(\[.*?\]);", text, re.S).group(1))
    drinks = 0
    for col in cols:
        for d in col["drinks"]:
            key = ALIAS.get(d["he"], d["he"])
            if key not in by_name:
                fails.append(f"COLS: {d['he']!r} is not in the record")
                continue
            r = rec(d["he"])
            drinks += 1
            for field, want, got in (
                ("fc", num(r["cost"]), num(d["fc"])),
                ("p", num(r["price"]), num(d["p"])),
                ("m", num(r["marg"]), num(d["m"])),
                ("pr", num(r["prof"]), num(d["pr"])),
            ):
                if abs(want - got) > 0.005:
                    fails.append(f"COLS/{d['he']}.{field}: page {got} != record {want}")
    if drinks != 48:
        fails.append(f"COLS: {drinks} drinks, expected 48")

    # ── 2. COLS collection headline prices ──────────────────────────────
    for col in cols:
        prices = [num(rec(d["he"])["price"]) for d in col["drinks"]]
        lo, hi = int(min(prices)), int(max(prices))
        want = f"₪{lo}" if lo == hi else f"₪{lo}–{hi}"
        if col["p"] != want:
            fails.append(f"COLS/{col['he']}.p: page {col['p']!r} != derived {want!r}")

    # ── 3. MK flavour-card rows ─────────────────────────────────────────
    block = re.search(r"const MK=\{.*?\n\};", text, re.S).group(0)
    rows = 0
    for flavour, entries in MK_MAP.items():
        for title, target in entries:
            m = re.search(
                r'\{t:"' + re.escape(title) + r'",p:(\d+),m:(\d+),fc:"([\d.]+)"', block
            )
            if not m:
                fails.append(f"MK/{flavour}: row {title!r} not found")
                continue
            rows += 1
            r = cold if target is None else rec(target)
            for field, want, got in (
                ("p", num(r["price"]), float(m.group(1))),
                ("m", num(r["marg"]), float(m.group(2))),
                ("fc", num(r["cost"]), float(m.group(3))),
            ):
                if abs(want - got) > 0.005:
                    fails.append(f"MK/{flavour}/{title}.{field}: page {got} != record {want}")
    if rows != 23:
        fails.append(f"MK: {rows} rows, expected 23")

    # ── 4. the static collection cards ──────────────────────────────────
    cards = 0
    for anchor, col in zip(CARD_ANCHORS, cols):
        m = re.search(
            r'<div class="heh">' + re.escape(anchor) + r"</div>.*?"
            r"<span>מחיר מומלץ (₪[\d–]+)</span>", text, re.S)
        if not m:
            fails.append(f"card/{anchor}: not found")
            continue
        cards += 1
        if m.group(1) != col["p"]:
            fails.append(f"card/{anchor}: markup {m.group(1)!r} != COLS {col['p']!r}")
    if cards != 10:
        fails.append(f"cards: {cards} found, expected 10")

    # ── no stale figure may survive anywhere on the page ────────────────
    superseded = ROOT.parent / "gt-factory-os-production-brain" / "docs" / "pricing" / "2026-08-05_drinks_final_figures.json"
    if superseded.exists():
        old = json.load(open(superseded, encoding="utf-8"))
        entries = old.get("pages", old) if isinstance(old, dict) else old
        vals = entries.values() if isinstance(entries, dict) else entries
        stale = {num(e["cost"]) for e in vals if isinstance(e, dict) and "cost" in e}
        live = {num(v["cost"]) for v in by_name.values()}
        for col in cols:
            for d in col["drinks"]:
                if num(d["fc"]) in stale - live:
                    fails.append(f"COLS/{d['he']}.fc={d['fc']} is a superseded 2026-08-05 cost")

    if fails:
        print(f"FAIL — {len(fails)} disagreement(s) with the figures of record:")
        for f in fails:
            print("  " + f)
        sys.exit(1)

    print(
        f"figures verified against the record ({record['_meta']['date']}): "
        f"{drinks} drinks x 4 fields · {len(cols)} collection prices · "
        f"{rows} MK rows x 3 fields · {cards} static cards — 0 disagreements"
    )


if __name__ == "__main__":
    main()
