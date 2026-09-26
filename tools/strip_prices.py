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

The switch is `data/site_flags.json` → `show_prices`, read here for the theme, the
landing pages and CI alike. Every edit asserts its anchor and its count, so a moved
anchor fails the build instead of leaving a price behind, and `assert_clean()`
refuses any price token that survives anywhere.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "data" / "site_flags.json"

# What a price looks like on a served page, in markup or in a JS literal, plus the
# labels that only ever stand beside one. Labels, not words: "אותה עלות מנה" in a
# sentence is not a price, "<dt>עלות מנה" is. `find_prices()` is the one scan over
# this list; `assert_clean()` and the CI guard in .github/workflows/build.yml both
# call it. Every token matches in any case (\u20AA, &#X20AA;, nis); the currency
# codes only between non-letters, so "garnish" and "details" are not prices.
PRICE_TOKENS = ("₪", "\\u20aa", "&#8362;", "&#x20aa;", "ש״ח", 'ש"ח', "שקלים", "NIS", "ILS",
                "מחיר מומלץ", "<dt>עלות מנה", "מחירון סיטונאי גלוי", "מחירון גלוי")
CURRENCY_CODES = ("NIS", "ILS")
PRICE_RE = re.compile("|".join(
    rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z])" if t in CURRENCY_CODES else re.escape(t)
    for t in PRICE_TOKENS), re.IGNORECASE)

applied: list[str] = []


def show_prices() -> bool:
    return json.loads(FLAGS.read_text(encoding="utf-8"))["show_prices"]


def die(msg: str) -> None:
    sys.exit(f"FAIL [strip_prices]: {msg}")


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        die(f"{label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new)


def sub_re(label: str, pattern: str, repl: str, text: str, count: int) -> str:
    out, n = re.subn(pattern, repl, text)
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
        '<div class="stat"><b class="num" dir="ltr">20–25</b><span>כוסות מכל בקבוק</span></div>',
        markup, 1)
    markup = sub_re(
        "econ menu stat",
        r'<div class="stat"><b class="num">' + PRICE + r"</b><span>מחירי תפריט מומלצים</span></div>",
        '<div class="stat"><b class="num">48</b><span>מתכונים מוכנים לתפריט</span></div>',
        markup, 1)

    # Bar tools: name and English kicker stay, the price goes.
    markup = sub_re("tool prices", r"<i>" + PRICE + r"</i>", "", markup, 8)

    # The recipe modal's figures row: margin stays, the three money cells —
    # cost, recommended price, profit per cup — go.
    return sub_re("modal money cells", r'<div><i>[^<]*</i><b id="cm-(?:fc|p|pr)"></b></div>', "", markup, 3)


def price_list(markup: str, shown: bool) -> str:
    """The wholesale price list, and the nav item and three card links into it.

    Shown, the section is wrapped in the theme editor's `show_pricing` switch — the
    open question in PUBLISH.md B3, whether 116 wholesale figures belong on a public
    URL, stays a click, reversible both ways. Not shown, it is not written at all.
    Either way a hidden list takes its nav item with it, and the three product cards
    send a reader who wants a price to the enquiry form, which is where the price
    list is sent from.
    """
    start = markup.find('<section id="pricing"')
    end = markup.find("</section>", start) + len("</section>")
    if start < 0 or not start < end <= markup.find('<section id="about"'):
        die("price list section not found before #about")
    if shown:
        on, off = "{% if section.settings.show_pricing %}", "{% endif %}"
        markup = markup[:start] + on + markup[start:end] + off + markup[end:]
        nav = on + '<a href="#pricing">מחירון</a>' + off
        card = f'href="{on}#pricing{{% else %}}#contact{off}"'
    else:
        markup = markup[:start] + markup[end:]
        nav, card = "", 'href="#contact"'
    applied.append("price list section")
    markup = sub_re("price list card links", r'href="#pricing"(?!>מחירון</a>)', card, markup, 3)
    return sub("price list nav", '<a href="#pricing">מחירון</a>', nav, markup)


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

    # The three "what it makes" renderers and the recipe modal. A row keeps its
    # margin; the recipe footer under it only repeated the figures, so with the
    # prices gone it goes too.
    js = sub("row price", "<i>\\u20aa'+d.p+' \\u00b7 <b>", "<i>רווחיות <b>", js, 3)
    js = sub_re("recipe footer", r"""'</ol><div class="fc">[^<]*</div></div></details>'""",
                "'</ol></div></details>'", js, 2)
    return sub_re("modal money lines",
                  r"\s*document\.getElementById\('cm-(?:fc|pr|p)'\)\.textContent='\\u20aa'\+d\.\w+;",
                  "", js, 3)


CSS = """
/* No prices on the served page (tools/strip_prices.py): the recipe modal's
   figures row is down to the margin, so it spans the card. */
.cm-stats{grid-template-columns:1fr}
"""


def find_prices(text: str) -> list[re.Match]:
    """Every price token in `text`, in the order it appears."""
    return list(PRICE_RE.finditer(text))


def assert_clean(label: str, text: str) -> None:
    hits = find_prices(text)
    for m in hits:
        print(f"  {label}: {m.group(0)!r} at {m.start()}: "
              f"…{text[max(0, m.start() - 80):m.end() + 40]!r}…", file=sys.stderr)
    if hits:
        die(f"{label}: {len(hits)} price(s) survived")
