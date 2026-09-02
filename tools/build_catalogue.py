#!/usr/bin/env python3
"""Merge the hand-written Hebrew parts into i18n/strings.he.json.

Visible strings are keyed by string id; JS strings are keyed by their English
text (the same sentence recurs across dozens of recipes and is translated once).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "i18n" / "parts"))

import he_visible_1, he_visible_2, he_visible_3, he_js, he_js2  # noqa: E402

BY_ID = {}
for mod in (he_visible_1, he_visible_2, he_visible_3):
    BY_ID.update(mod.HE)

BY_TEXT = {}
BY_TEXT.update(he_js.EN2HE)
BY_TEXT.update(he_js2.EN2HE)
SKIP = set(he_js.SKIP)

# Literals the renderers read as code, not copy.
MACHINE = re.compile(
    r"^\s*[+$]|[<>]|\$\{|^\s*\.|var\(--|^rgba?\(|^[a-z-]+:"
    r"|^\s*[a-z]+\.[a-z]+|^ ?data-|^[A-Za-z]+\[|classList|^a\."
    r"|^\\u[0-9a-f]{4}"          # emoji escapes (STEP_ICONS glyphs)
)

records = json.loads((ROOT / "i18n" / "strings.en.json").read_text(encoding="utf-8"))

stats = {"by_id": 0, "by_text": 0, "machine": 0, "already_he": 0, "MISSING": 0}
missing = []
for r in records:
    en = r["en"]
    if r["id"] in BY_ID:
        r["he"] = BY_ID[r["id"]]
        stats["by_id"] += 1
    elif en in BY_TEXT:
        r["he"] = BY_TEXT[en]
        stats["by_text"] += 1
    elif en in SKIP or MACHINE.search(en):
        r["he"] = ""                       # keep the source literal
        stats["machine"] += 1
    elif re.search(r"[֐-׿]", en):
        r["he"] = ""                       # already Hebrew in the source
        stats["already_he"] += 1
    else:
        r["he"] = ""
        stats["MISSING"] += 1
        missing.append(r)

(ROOT / "i18n" / "strings.he.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8"
)

print(" ".join(f"{k}={v}" for k, v in stats.items()))
if missing:
    print(f"\n--- {len(missing)} untranslated ---")
    for r in missing[:60]:
        print(f'  {r["id"]} [{r["ctx"]}] {r["en"][:88]!r}')
