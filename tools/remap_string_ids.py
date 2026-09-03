#!/usr/bin/env python3
"""Move the Hebrew catalogue onto new string ids after the source page changes.

`extract_strings.py` numbers visible strings by document order, and
`i18n/parts/he_visible_*.py` keys its Hebrew by those numbers. So inserting or
removing anything translatable renumbers every string after it, and every later
translation silently lands on the wrong sentence — a failure that produces a
page which builds cleanly and reads like nonsense.

This aligns the old catalogue against the new one by their English text, in
order, and rewrites the parts files onto the new ids. Text is the anchor, not
position: an untouched sentence keeps its Hebrew no matter how far it moved.

    python3 tools/remap_string_ids.py            # rewrite the parts files
    python3 tools/remap_string_ids.py --dry-run  # report, change nothing

Run it once, immediately after editing src/index.en.html, and read the report:
dropped ids are strings you deleted, and the ids listed as owed are strings you
added and still have to translate by hand.
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = sorted((ROOT / "i18n" / "parts").glob("he_visible_*.py"))
CATALOGUE = ROOT / "i18n" / "strings.en.json"
# A key already rewritten must not match the pattern again: if a0348 becomes
# a0352 and a0352 is itself a key in the same file, a second pass would move it
# twice. This prefix parks a rewritten key outside the pattern until the end.
MARK = "@@"


def old_catalogue():
    r = subprocess.run(["git", "show", "HEAD:i18n/strings.en.json"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit("FAIL: cannot read the committed catalogue — commit before remapping")
    return json.loads(r.stdout)


def main() -> None:
    dry = "--dry-run" in sys.argv
    old = old_catalogue()
    subprocess.run([sys.executable, "tools/extract_strings.py"], cwd=ROOT, check=True,
                   capture_output=True)
    new = json.loads(CATALOGUE.read_text(encoding="utf-8"))

    o_ids, o_en = [r["id"] for r in old], [r["en"] for r in old]
    n_ids, n_en = [r["id"] for r in new], [r["en"] for r in new]
    print(f"catalogue: {len(old)} -> {len(new)} strings")

    mapping = {}
    blocks = difflib.SequenceMatcher(None, o_en, n_en, autojunk=False).get_matching_blocks()
    for a, b, size in blocks:
        for k in range(size):
            mapping[o_ids[a + k]] = n_ids[b + k]
    moved = sum(1 for k, v in mapping.items() if k != v)
    print(f"aligned {len(mapping)} of {len(old)} old strings; {moved} changed id")

    used, dropped = set(), []
    for path in PARTS:
        src = path.read_text(encoding="utf-8")
        keys = re.findall(r'"([at]\d{4})"\s*:', src)
        out = src
        for k in dict.fromkeys(keys):
            if k in mapping:
                out = re.sub(rf'"{k}"(\s*:)', f'"{MARK}{mapping[k]}"' + r"\1", out)
                used.add(k)
            else:
                dropped.append((path.name, k))
        out = out.replace(MARK, "")
        if not dry:
            path.write_text(out, encoding="utf-8")
        print(f"  {path.name}: {len(keys)} keys")

    if dropped:
        print(f"{len(dropped)} translation(s) whose string no longer exists:")
        for f, k in dropped[:12]:
            print(f"    {f}  {k}")
    translated = {mapping[k] for k in used if k in mapping}
    # Only visible strings are keyed by id. The j#### ids are JS literals, which
    # build_catalogue.py matches on their English text, so they are never owed here.
    owed = [r for r in new
            if r["id"][0] in "at" and r["id"] not in translated]
    print(f"{len(owed)} new visible string(s) with no Hebrew yet:")
    for r in owed[:24]:
        print(f"    {r['id']}  {r['en'][:60]!r}")


if __name__ == "__main__":
    main()
