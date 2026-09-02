#!/usr/bin/env python3
"""Extract every user-visible string from the v5 source page.

Emits an ordered JSON catalogue where each record carries the exact character
span it occupies in the source file, so a translated catalogue can be applied
back losslessly (see apply_translation.py).
"""
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "index.en.html"
OUT = Path(__file__).resolve().parents[1] / "i18n" / "strings.en.json"

# Attributes whose values are read by a human.
ATTRS = ("placeholder", "alt", "title", "aria-label")

# JS string literals we must never touch: URLs, selectors, DOM ids, colours,
# format tokens and other machine-facing values.
JS_SKIP = re.compile(
    r"""^(?:
          \s*$                      # blank
        | https?://.*               # url
        | [#.\[][\w\-\[\]="'.:# ]*   # css selector
        | \#[0-9a-fA-F]{3,8}         # colour
        | [\w\-]+                    # single bare token (id / key / class)
        | [\d\s.,%+\-/*()]+          # numeric
        | \s*[<>&][^ ]*.*            # markup fragment
    )$""",
    re.X,
)


def regions(text, tag):
    """Yield (start, end) spans of <tag>...</tag> bodies."""
    for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", text, re.S | re.I):
        yield m.start(1), m.end(1)


def in_any(pos, spans):
    return any(a <= pos < b for a, b in spans)


def nearest_anchor(text, pos):
    """Closest preceding id= or section/class marker — context for the translator."""
    head = text[max(0, pos - 6000):pos]
    ids = re.findall(r'<(?:section|div|form|footer|nav)[^>]*id="([\w\-]+)"', head)
    if ids:
        return ids[-1]
    cls = re.findall(r'<section[^>]*class="([\w\- ]+)"', head)
    return cls[-1].split()[0] if cls else "page"


def js_context(text, pos):
    head = text[max(0, pos - 4000):pos]
    var = re.findall(r"(?:var|const|let)\s+([A-Za-z_$][\w$]*)\s*=", head)
    return var[-1] if var else "js"


def main():
    text = SRC.read_text(encoding="utf-8")
    style_spans = list(regions(text, "style"))
    script_spans = list(regions(text, "script"))
    masked = style_spans + script_spans

    records = []

    # --- HTML text nodes -------------------------------------------------
    for m in re.finditer(r">([^<>]+)<", text):
        start, end = m.start(1), m.end(1)
        if in_any(start, masked):
            continue
        raw = m.group(1)
        if not raw.strip():
            continue
        # Preserve surrounding whitespace; translate only the trimmed core.
        lead = len(raw) - len(raw.lstrip())
        trail = len(raw) - len(raw.rstrip())
        core = raw[lead: len(raw) - trail]
        if not re.search(r"[A-Za-z֐-׿]", core):
            continue  # pure punctuation / digits / arrows
        records.append(
            {
                "id": f"t{len(records):04d}",
                "kind": "text",
                "ctx": nearest_anchor(text, start),
                "start": start + lead,
                "end": end - trail,
                "en": core,
            }
        )

    # --- translatable attributes ----------------------------------------
    attr_re = re.compile(rf'\b({"|".join(ATTRS)})\s*=\s*"([^"]*)"')
    for m in attr_re.finditer(text):
        start, end = m.start(2), m.end(2)
        if in_any(start, style_spans):
            continue
        val = m.group(2)
        if not val.strip() or not re.search(r"[A-Za-z֐-׿]", val):
            continue
        if val.startswith(("http", "//", "data:")):
            continue
        records.append(
            {
                "id": f"a{len(records):04d}",
                "kind": f"attr:{m.group(1)}",
                "ctx": nearest_anchor(text, start),
                "start": start,
                "end": end,
                "en": val,
            }
        )

    # --- JS string literals ----------------------------------------------
    lit_re = re.compile(r"""(?<![\w\\])(["'])((?:[^"'\\\n]|\\.)*?)\1""")
    for a, b in script_spans:
        for m in lit_re.finditer(text, a, b):
            val = m.group(2)
            if not val or JS_SKIP.match(val):
                continue
            if not re.search(r"[A-Za-z֐-׿]{3}", val):
                continue
            # object key (followed by a colon) -> machine-facing, keep
            tail = text[m.end(): m.end() + 3]
            if tail.lstrip().startswith(":"):
                continue
            records.append(
                {
                    "id": f"j{len(records):04d}",
                    "kind": "js",
                    "ctx": js_context(text, m.start()),
                    "start": m.start(2),
                    "end": m.end(2),
                    "en": val,
                }
            )

    records.sort(key=lambda r: r["start"])
    for i, r in enumerate(records):
        r["id"] = f"{r['id'][0]}{i:04d}"

    # sanity: no overlapping spans
    for prev, cur in zip(records, records[1:]):
        if cur["start"] < prev["end"]:
            sys.exit(f"overlapping spans: {prev['id']} / {cur['id']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    kinds = {}
    for r in records:
        kinds[r["kind"].split(":")[0]] = kinds.get(r["kind"].split(":")[0], 0) + 1
    print(f"{len(records)} strings -> {OUT}")
    print("by kind:", kinds)
    print("words:", sum(len(r["en"].split()) for r in records))


if __name__ == "__main__":
    main()
