#!/usr/bin/env python3
"""Code changes the Hebrew build needs, applied to src/index.html.

Translating the copy alone is not enough: two renderers in this page read the
copy itself. `STEP_ICONS` matches English recipe steps (so it goes blank once
the steps are Hebrew) and `glassSVG`'s LAYER_MAP matches Hebrew ingredients (so
it only starts working now). Both are handled here, together with the document
direction and the drink names the modal was discarding.

Every edit asserts its anchor exists, so a silent no-op is impossible.
"""
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "index.html"
text = SRC.read_text(encoding="utf-8")
applied = []


def sub(label, old, new, count=1):
    global text
    n = text.count(old)
    if n != count:
        sys.exit(f"FAIL [{label}]: expected {count} occurrence(s), found {n}")
    text = text.replace(old, new, count)
    applied.append(label)


# ── A. document direction + head ────────────────────────────────────────
sub("html lang/dir", '<html lang="en">', '<html lang="he" dir="rtl">')

sub(
    "head meta",
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '<meta name="description" content="GT Everyday — יצרנית בוטיק ישראלית של '
    'תמציות תה, מאצ׳ה ומחיות פרי לבתי קפה, מסעדות ומלונות. 48 משקאות, מתכונים '
    'מתומחרים ומחירון סיטונאי גלוי.">\n'
    '<meta name="theme-color" content="#3E6E34">\n'
    '<meta property="og:type" content="website">\n'
    '<meta property="og:locale" content="he_IL">\n'
    '<meta property="og:site_name" content="GT Everyday">\n'
    '<meta property="og:title" content="GT Everyday · סיטונאות למסעדנות">\n'
    '<meta property="og:description" content="48 משקאות. ספק אחד. מחירון גלוי.">\n'
    '<meta name="twitter:card" content="summary_large_image">',
)

# ── B. collection titles the extractor could not reach ──────────────────
# Bare one-word values are indistinguishable from object keys, so they were
# skipped by the string extractor and are set here in place.
for num, en, he in (
    ("02", "Lemonade", "לימונדות"),
    ("03", "Signature", "משקאות הדגל"),
    ("04", "Gazoz", "גזוז"),
    ("10", "Ube", "אובה"),
):
    sub(f"COLS {num} title", f'{{"n": "{num}", "t": "{en}"', f'{{"n": "{num}", "t": "{he}"')

# POUCHCH values are matched against COLS[].t, so they move together.
sub("POUCHCH", 'var POUCHCH={"Matcha":"אייס מאצ׳ה","Ube":"Ube"}',
    'var POUCHCH={"Matcha":"אייס מאצ׳ה","Ube":"אובה"}')

# Single bare words are indistinguishable from object keys to the extractor,
# so these ingredient/step values are translated in place.
sub("ing Ice", '"ing": ["Ice"', '"ing": ["\u05e7\u05e8\u05d7"', 48)
sub("ing Garnish", '"40 \u05de\u05f4\u05dc \u05ea\u05e8\u05db\u05d9\u05d6 GT", "Garnish"]',
    '"40 \u05de\u05f4\u05dc \u05ea\u05e8\u05db\u05d9\u05d6 GT", "\u05e7\u05d9\u05e9\u05d5\u05d8"]', 4)
sub("step Garnish", '(\u05db\u05be150 \u05de\u05f4\u05dc)","Garnish"]',
    '(\u05db\u05be150 \u05de\u05f4\u05dc)","\u05de\u05e7\u05e9\u05d8\u05d9\u05dd"]')
sub("ing cinnamon", '"cinnamon"]', '"\u05e7\u05d9\u05e0\u05de\u05d5\u05df"]')

# ── C. render the Hebrew drink name the data already carries ────────────
# Every drink in COLS has a `he` name. The English build wrote '' into #cm-he
# and showed `en` — so all 48 Hebrew names were loaded and thrown away.
sub(
    "dn() helper",
    "function cmRender(){",
    "// Hebrew name when the drink has one; the English name becomes the kicker.\n"
    "function dn(d){return (d && d.he) || (d && d.en) || '';}\n"
    "function cmRender(){",
)
sub("modal headline", "document.getElementById('cm-en').textContent=d.en;",
    "document.getElementById('cm-en').textContent=dn(d);")
sub("modal kicker", "document.getElementById('cm-he').textContent='';",
    "document.getElementById('cm-he').textContent=d.en||'';")
sub("modal image alt", "alt=\"'+d.en+'\"", "alt=\"'+dn(d)+'\"")
sub("modal chip", "sp.textContent=dd.en;", "sp.textContent=dn(dd);")
sub("pouch list", "<summary><span>'+d.en+'</span>", "<summary><span>'+dn(d)+'</span>")
sub("mixer button", "COLS[ci].drinks[di].en+'</button>'",
    "dn(COLS[ci].drinks[di])+'</button>'")
sub("source list", "<span class=\"nm\">'+d.en+'<em>", "<span class=\"nm\">'+dn(d)+'<em>")

# ── D. STEP_ICONS: match the Hebrew steps ───────────────────────────────
# The English patterns are kept alongside so a step that is still English
# (or a future mixed one) still resolves to an icon instead of a bullet.
sub(
    "STEP_ICONS Hebrew",
    """STEP_ICONS=[
 [/ice/i,'\\ud83e\\uddca','Ice'],
 [/matcha/i,'\\ud83c\\udf75','Matcha'],
 [/ube/i,'\\ud83c\\udf60','Ube'],
 [/GT (massala )?(concentrate|essence)|GT massala/i,'\\ud83e\\uddc9','GT 50ml'],
 [/milk foam|cold foam|foam/i,'\\u2601\\ufe0f','Foam'],
 [/milk/i,'\\ud83e\\udd5b','Milk'],
 [/soda|tonic|sparkl/i,'\\ud83e\\udd64','Soda'],
 [/water/i,'\\ud83d\\udca7','Water'],
 [/espresso|coffee/i,'\\u2615','Espresso'],
 [/agave/i,'\\ud83c\\udf6f','Agave'],
 [/mango|strawberry|peach|lychee|apple|banana|orange|lemonade|juice|pur\\u00e9e/i,'\\ud83c\\udf53','Fruit'],
 [/garnish|dust|sprinkle|crown|stir|vanilla pod/i,'\\ud83c\\udf3f','Finish'],
];""",
    """STEP_ICONS=[
 [/\\u05e7\\u05e8\\u05d7|ice/i,'\\ud83e\\uddca','\\u05e7\\u05e8\\u05d7'],
 [/\\u05de\\u05d0\\u05e6['\\u05f3]?\\u05d4|matcha/i,'\\ud83c\\udf75','\\u05de\\u05d0\\u05e6\\u05f3\\u05d4'],
 [/\\u05d0\\u05d5\\u05d1\\u05d4|ube/i,'\\ud83c\\udf60','\\u05d0\\u05d5\\u05d1\\u05d4'],
 [/\\u05ea\\u05e8\\u05db\\u05d9\\u05d6 (\\u05de\\u05e1\\u05d0\\u05dc\\u05d4 )?GT|\\u05de\\u05e1\\u05d0\\u05dc\\u05d4 GT|GT (massala )?(concentrate|essence)|GT massala/i,'\\ud83e\\uddc9','GT 50 \\u05de\\u05f4\\u05dc'],
 [/\\u05e7\\u05e6\\u05e3|\\u05e7\\u05e8\\u05dd \\u05e7\\u05d5\\u05e7\\u05d5\\u05e1|milk foam|cold foam|foam|coconut cream/i,'\\u2601\\ufe0f','\\u05e7\\u05e6\\u05e3'],
 [/\\u05d7\\u05dc\\u05d1|milk/i,'\\ud83e\\udd5b','\\u05d7\\u05dc\\u05d1'],
 [/\\u05e1\\u05d5\\u05d3\\u05d4|\\u05d8\\u05d5\\u05e0\\u05d9\\u05e7|soda|tonic|sparkl/i,'\\ud83e\\udd64','\\u05e1\\u05d5\\u05d3\\u05d4'],
 [/\\u05de\\u05d9\\u05dd|water/i,'\\ud83d\\udca7','\\u05de\\u05d9\\u05dd'],
 [/\\u05d0\\u05e1\\u05e4\\u05e8\\u05e1\\u05d5|espresso|coffee/i,'\\u2615','\\u05d0\\u05e1\\u05e4\\u05e8\\u05e1\\u05d5'],
 [/\\u05d0\\u05d2\\u05d1\\u05d4|agave/i,'\\ud83c\\udf6f','\\u05d0\\u05d2\\u05d1\\u05d4'],
 [/\\u05de\\u05e0\\u05d2\\u05d5|\\u05ea\\u05d5\\u05ea|\\u05d0\\u05e4\\u05e8\\u05e1\\u05e7|\\u05dc\\u05d9\\u05e6['\\u05f3]?\\u05d9|\\u05ea\\u05e4\\u05d5\\u05d7|\\u05d1\\u05e0\\u05e0\\u05d4|\\u05ea\\u05e4\\u05d5\\u05d6|\\u05dc\\u05d9\\u05de\\u05d5\\u05e0\\u05d3\\u05d4|\\u05de\\u05d9\\u05e5|\\u05e4\\u05d9\\u05e8\\u05d4|mango|strawberry|peach|lychee|apple|banana|orange|lemonade|juice|pur\\u00e9e/i,'\\ud83c\\udf53','\\u05e4\\u05e8\\u05d9'],
 [/\\u05de\\u05e7\\u05e9\\u05d8|\\u05e7\\u05d9\\u05e9\\u05d5\\u05d8|\\u05de\\u05e4\\u05d6\\u05e8|\\u05de\\u05db\\u05ea\\u05d9\\u05e8|\\u05de\\u05e2\\u05e8\\u05d1|\\u05d5\\u05e0\\u05d9\\u05dc|\\u05e4\\u05d9\\u05e1\\u05d8\\u05d5\\u05e7|\\u05e9\\u05d5\\u05de\\u05e9\\u05d5\\u05dd|garnish|dust|sprinkle|crown|stir|vanilla|pistachio|sesame/i,'\\ud83c\\udf3f','\\u05e1\\u05d9\\u05d5\\u05dd'],
];""",
)

SRC.write_text(text, encoding="utf-8")
print(f"{len(applied)} patches applied:")
for a in applied:
    print("  ✓", a)
