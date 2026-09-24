#!/usr/bin/env python3
"""Take every shekel figure off the pages the store serves.

Tom, 2026-09-24: "צריך גם להוריד את המחירים שלא יראו אותם" — take the prices down
so they are not seen. That is every price on the site, not only the wholesale list
the earlier `show_pricing` switch covered: GT's own prices on the product cards, the
per-cup cost, the recommended menu price and the profit per cup. The margin
percentage stays — it is the page's argument to a café owner, and it is not a price.

Why here and not in `src/index.html`
    `src/index.html` is the full build: `patch_figures.py` writes every figure into
    it and `verify_figures.py` proves each one against the record. That stays whole,
    so the figures remain checked and can come back with one flag. This module runs
    inside `build_theme.py`, on the way into the theme, so what the store serves —
    the section *and* `gt-site.js` — carries no price at all. Hiding them with CSS
    would have left all 48 drinks' costs one "view source" away.

The switch is `data/site_flags.json` → `show_prices`. Every edit asserts its anchor
and its count, so a moved anchor fails the build instead of leaving a price behind,
and `assert_clean()` refuses any ₪ that survives anywhere.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "data" / "site_flags.json"

applied: list[str] = []


def show_prices() -> bool:
    if not FLAGS.exists():
        return True
    return bool(json.loads(FLAGS.read_text(encoding="utf-8")).get("show_prices", True))


def die(msg: str) -> None:
    sys.exit(f"FAIL [strip_prices]: {msg}")


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        die(f"{label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new)


def sub_re(label: str, pattern: str, repl: str, text: str, count: int, flags=0) -> str:
    out, n = re.subn(pattern, repl, text, flags=flags)
    if n != count:
        die(f"{label}: expected {count} match(es), found {n}")
    applied.append(f"{label} ×{n}")
    return out


PRICE = r"₪[\d.,]+(?:–[\d.,]+)?"


def strip_markup(markup: str) -> str:
    """The section's HTML, with every price element removed or reworded."""
    # Hero slides: "7 משקאות · מחיר מומלץ ₪20" keeps its drink count.
    markup = sub_re("hero chips", r"<span>מחיר מומלץ " + PRICE + r"</span>", "", markup, 10)

    # The ticker under the hero keeps its collection names.
    markup = sub_re("ticker", r" <b>" + PRICE + r"</b>", "", markup, 16)

    # Concentrates intro: the bottle prices go, the rest of the sentence stays.
    markup = sub_re("bottle line", r"₪\d+ ל־500 מ״ל · ₪\d+ לליטר\.\s*", "", markup, 1)

    # Product cards and the product modal: the size stays, its price goes.
    # 9 concentrate cards x2, the modal x2, matcha x2, hojicha, ube x2, three purées.
    markup = sub_re("size chips", r"(<span>[^<]*?) · " + PRICE + r"(</span>)", r"\1\2", markup, 28)

    # The ten collection cards: the price badge goes.
    markup = sub_re("collection cards", r'<div class="pr">' + PRICE + r"</div>", "", markup, 10)

    # "כל מתכון מתומחר… — עם מחירים מומלצים ₪19–28." keeps everything but the range.
    markup = sub_re("collections intro", r" — עם מחירים מומלצים " + PRICE + r"\.", ".", markup, 1)

    # The economics card: cost per cup leaves the sentence, and two of its four
    # stats were prices. They become the two facts the card argues from anyway.
    markup = sub_re("econ sentence", r"עלות חומר גלם מ־" + PRICE + r" לכוס, ", "", markup, 1)
    markup = sub_re(
        "econ cost stat",
        r'<div class="stat"><b class="num">' + PRICE + r"</b><span>עלות חומר גלם לכוס, החל מ־</span></div>",
        '<div class="stat"><b class="num">20–25</b><span>כוסות מכל בקבוק</span></div>',
        markup, 1)
    markup = sub_re(
        "econ menu stat",
        r'<div class="stat"><b class="num">' + PRICE + r"</b><span>מחירי תפריט מומלצים</span></div>",
        '<div class="stat"><b class="num">48</b><span>מתכונים מוכנים לתפריט</span></div>',
        markup, 1)

    # Bar tools: name and English kicker stay, the price goes.
    markup = sub_re("tool prices", r"<i>" + PRICE + r"</i>", "", markup, 8)

    # The recipe modal's figures row: margin stays, the three money cells go.
    markup = sub("modal cost cell", '<div><i>עלות חומר גלם · ללא מע״מ</i><b id="cm-fc"></b></div>', "", markup)
    markup = sub("modal price cell", '<div><i>מחיר מומלץ · כולל מע״מ</i><b id="cm-p"></b></div>', "", markup)
    markup = sub("modal profit cell", '<div><i>רווח לכוס</i><b id="cm-pr"></b></div>', "", markup)

    # The wholesale price list itself, and the four links that pointed into it:
    # the nav item goes with it, the three product cards send a reader who wants
    # a price to the form — where the price list is sent from.
    start = markup.find('<section id="pricing"')
    if start < 0:
        die("pricing section not found")
    end = markup.find("</section>", start)
    if end < 0 or markup.find('<section id="about"') < end:
        die("pricing section end not found before #about")
    markup = markup[:start] + markup[end + len("</section>"):]
    applied.append("price list section")
    markup = sub("price list nav", '<a href="#pricing">מחירון</a>', "", markup)
    markup = sub("price list card links", 'href="#pricing"', 'href="#contact"', markup, 3)
    return markup


def strip_js(js: str) -> str:
    """gt-site.js, with the price fields gone from the data and the renderers."""
    # COLS: the collection's price range, and each drink's cost, price and profit.
    m = re.search(r"const COLS=(\[.*?\]);", js, re.S)
    if not m:
        die("COLS not found")
    cols = json.loads(m.group(1))
    drinks = 0
    for col in cols:
        if "p" not in col:
            die(f"COLS/{col.get('t')}: no collection price to remove")
        del col["p"]
        for d in col["drinks"]:
            for k in ("fc", "p", "pr"):
                if k not in d:
                    die(f"COLS/{d.get('he')}: field {k} missing")
                del d[k]
            if "m" not in d:
                die(f"COLS/{d.get('he')}: margin missing")
            drinks += 1
    if drinks != 48:
        die(f"COLS: {drinks} drinks, expected 48")
    js = js[:m.start(1)] + json.dumps(cols, ensure_ascii=False) + js[m.end(1):]
    applied.append("COLS fields ×48")

    # MK flavour-card rows: {t:"…",p:20,m:81,fc:"3.25",st:…}
    js = sub_re("MK rows", r',p:\d+,m:(\d+),fc:"[\d.]+"', r",m:\1", js, 23)

    # The three "what it makes" renderers and the recipe modal. A row's summary
    # keeps its margin; the recipe footer under it only repeated the figures, so
    # with the prices gone it goes too.
    js = sub("list price", "<i>\\u20aa'+d.p+' \\u00b7 <b>'+d.m+'%</b></i></summary>'",
             "<i>רווחיות <b>'+d.m+'%</b></i></summary>'", js, 2)
    js = sub("recipe footer",
             "'</ol><div class=\"fc\">עלות חומר גלם \\u20aa'+d.fc+' ללא מע״מ \\u00b7 מחיר מומלץ \\u20aa'+d.p+"
             "' כולל מע״מ \\u00b7 רווחיות '+d.m+'%</div></div></details>'",
             "'</ol></div></details>'", js, 2)
    js = sub("link price", "'<i>\\u20aa'+d.p+' \\u00b7 <b>'+d.m+'%</b>",
             "'<i>רווחיות <b>'+d.m+'%</b>", js)
    for cell in ("cm-fc", "cm-pr"):
        js = sub_re(f"modal {cell}", r"\s*document\.getElementById\('" + cell + r"'\)\.textContent='\\u20aa'\+d\.\w+;",
                    "", js, 1)
    js = sub_re("modal cm-p", r"\s*document\.getElementById\('cm-p'\)\.textContent='\\u20aa'\+d\.p;", "", js, 1)
    return js


CSS = """
/* No prices on the served page (tools/strip_prices.py): the recipe modal's
   figures row is down to the margin, so it spans the card. */
.cm-stats{grid-template-columns:1fr}
"""


def assert_clean(label: str, text: str) -> None:
    for token in ("₪", "\\u20aa", "&#8362;", "ש״ח", 'ש"ח'):
        i = text.find(token)
        if i >= 0:
            die(f"{label}: a price survived — …{text[max(0, i - 80):i + 40]}…")


if __name__ == "__main__":
    print("strip_prices is a module; build_theme.py runs it when data/site_flags.json says show_prices: false")
