#!/usr/bin/env python3
"""Apply a translated catalogue back onto the source page.

Replacements are made by character span, right to left, so earlier offsets stay
valid. A record with no "he" value (or an empty one) keeps its English text.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue", default=ROOT / "i18n" / "strings.he.json")
    ap.add_argument("--source", default=ROOT / "src" / "index.en.html")
    ap.add_argument("--out", default=ROOT / "src" / "index.html")
    ap.add_argument("--identity", action="store_true",
                    help="re-insert the English text (round-trip self-test)")
    args = ap.parse_args()

    text = Path(args.source).read_text(encoding="utf-8")
    records = json.loads(Path(args.catalogue).read_text(encoding="utf-8"))

    applied = missing = 0
    for r in sorted(records, key=lambda x: x["start"], reverse=True):
        new = r["en"] if args.identity else (r.get("he") or "").strip()
        if not new:
            missing += 1
            continue
        assert text[r["start"]:r["end"]] == r["en"], f"span drift at {r['id']}"
        text = text[:r["start"]] + new + text[r["end"]:]
        applied += 1

    Path(args.out).write_text(text, encoding="utf-8")
    print(f"applied {applied}, untranslated {missing} -> {args.out}")


if __name__ == "__main__":
    main()
