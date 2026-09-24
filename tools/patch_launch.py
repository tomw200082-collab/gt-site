#!/usr/bin/env python3
"""The pre-launch pass, 2026-09-24: what a render of the live preview still showed.

Tom asked for the site to go up without a single mistake, with photographs that
look right and Hebrew that does not read as translated. The preview theme was
walked on a phone (390px) and a desktop (1440px), every modal opened, and each
finding below was confirmed in a render before it was fixed here. The copy itself
is fixed at its source in i18n/parts/; this file carries what is not copy.

  The hero's photo slot was empty
      A soft green panel waiting for Tom's photograph since 2026-09-03. It is now
      his shot of the whole line on three shelves, shown at its own 3:4 ratio so no
      bottle is cropped away, preloaded from the layout as the page's largest paint.

  The page was wider than a phone
      The economics card kept its 60px desktop padding and a two-column grid of
      38px figures below 980px, so its content needed 425px on a 390px screen and
      the whole document scrolled sideways. Everything else was fine.

  English left in the product modal
      "Menu drinks it makes — tap to open the recipe" and "Food cost … ex-VAT ·
      recommended price … incl. VAT · margin" sit in JS string literals the
      extractor skips, so they never reached the catalogue. They rendered on every
      product card a visitor opened.

  White titles on bright photographs
      The collection cards darken their photograph with a ::after gradient — and a
      later `.ccard:after` rule for the decorative circle overwrote it, because
      ::after and :after are the same pseudo-element. On the lemonade and iced-tea
      cards the white title and drink count sat on pale yellow. The gradient moves
      to ::before, where nothing competes for it.

  The "open recipe" arrow pointed backwards
      Every forward arrow on the page points ← (the reader's direction); the rows
      in the product modal pointed →.

Every edit asserts its anchor, so a silent no-op is impossible.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"

applied: list[str] = []

# Served from the repo like the partner logos: build_theme.py turns each URL into a
# hash-named theme asset and records it in theme/assets.manifest.json.
PHOTO = "https://raw.githubusercontent.com/tomw200082-collab/gt-site/main/theme/photos/"
HERO = {600: 804, 900: 1206, 1200: 1607}


def die(msg: str) -> None:
    sys.exit(f"FAIL [patch_launch]: {msg}")


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        die(f"{label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new)


def hero_img() -> str:
    srcset = ", ".join(f"{PHOTO}hero-bottles-{w}.webp {w}w" for w in HERO)
    return (f'<img src="{PHOTO}hero-bottles-900.webp" srcset="{srcset}"'
            ' sizes="(max-width: 980px) min(92vw, 520px), 480px"'
            ' alt="תמציות התה של GT — עשרה בקבוקים על שלושה מדפים"'
            f' width="900" height="{HERO[900]}" fetchpriority="high" decoding="async">')


CSS = """
/* ====================================================================
   Pre-launch pass 2026-09-24 (tools/patch_launch.py). Appended last.
   ==================================================================== */
/* the hero photograph, at its own 3:4 so no bottle is cropped */
.hero .side{height:auto;padding:0;background:#F3E3C9;overflow:hidden;display:block;
  width:min(100%,calc(min(640px,74vh) * 0.7466));aspect-ratio:1744/2336;justify-self:center}
.hero .side:before{display:none}
.hero .side img{display:block;width:100%;height:100%;object-fit:cover}
@media(max-width:980px){
  .hero .side{height:auto;width:min(100%,520px)}
}
@media(max-width:640px){
  .hero{padding:40px 0 64px}
  .hero .in{gap:36px}
  .hero h2{margin-bottom:24px}
}
/* the economics card fits a phone */
@media(max-width:640px){
  .econ{padding:40px 22px;gap:30px;border-radius:26px}
  .stats{gap:10px}
  .stat{padding:18px 14px}
  .stat b{font-size:30px}
}
/* collection cards: darken the top, where the title and count sit */
.ccard::before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(180deg,rgba(15,15,12,.55) 0%,rgba(15,15,12,.18) 34%,rgba(15,15,12,0) 55%)}
.ccard h4,.ccard small,.ccard .idx{text-shadow:0 1px 14px rgba(0,0,0,.35)}
/* a line of text beside a button wraps under it instead of running into it */
.center-cta{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 18px}
.center-cta>span{margin:0!important}
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ── the hero photograph ─────────────────────────────────────────────
    text = sub("hero photo", '<div class="side"></div>', f'<div class="side">{hero_img()}</div>', text)

    # ── English left in the product modal ───────────────────────────────
    text = sub("makes header", "Menu drinks it makes \\u2014 tap for recipe",
               "מה מכינים ממנו \\u2014 לחצו למתכון", text, 2)
    text = sub("makes header (links)", "Menu drinks it makes \\u2014 tap to open the recipe",
               "מה מכינים ממנו \\u2014 לחצו לפתיחת המתכון", text)
    text = sub("recipe footer",
               "'</ol><div class=\"fc\">Food cost \\u20aa'+d.fc+' ex-VAT \\u00b7 recommended price \\u20aa'+d.p+"
               "' incl. VAT \\u00b7 margin '+d.m+'%</div></div></details>'",
               "'</ol><div class=\"fc\">עלות חומר גלם \\u20aa'+d.fc+' ללא מע״מ \\u00b7 מחיר מומלץ \\u20aa'+d.p+"
               "' כולל מע״מ \\u00b7 רווחיות '+d.m+'%</div></div></details>'", text, 2)

    # ── the forward arrow points the reader's way ───────────────────────
    text = sub("recipe link arrow", "<u>\\u2192</u>", "<u>\\u2190</u>", text)

    text = sub("launch stylesheet", "</style>", CSS + "</style>", text)

    SRC.write_text(text, encoding="utf-8")
    print(f"launch: {len(applied)} fixes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
