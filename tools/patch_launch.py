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

  The footer's social names were text, not links
      "אינסטגרם · פייסבוק · יוטיוב" looked like three links and went nowhere. They
      now point at the accounts the live store already links to.

  Three product cards opened empty
      openF() looked each product up by its card heading, and the matcha, hojicha
      and ube headings are Hebrew while every data table is keyed in Latin — so
      those three modals listed no drinks. The heading stays; the lookup uses the key.

  English the extractor never reached
      The product matrix ("Detox 2 drinks", "Matcha"), its empty note, the recipe's
      "על בסיס Matcha" chip, the purée modal title ("Mango · …") and the price
      list's "Expand all" were all JS literals outside the catalogue.

  Arrows and a minus sign pointing the wrong way
      Every forward arrow on the page points ← (the reader's direction); the recipe
      rows, the four-step strip and the matrix links pointed →. "−25%" put its
      minus on the right.

  "0 מקום במקרר"
      A zero with a singular noun, and the weakest way to make the point. The stat
      is now the approved shelf life: 12 months closed, no refrigeration
      (Sales-Machine knowledge/claims/public-claims.yaml #shelf_life).

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
.ccard h4{line-height:1.12}
.ccard small{display:block;margin-top:3px}
/* a line of text beside a button wraps under it instead of running into it */
.center-cta{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 18px}
.center-cta>span{margin:0!important}
/* footer.site's `padding:40px 0` erased .wrap's side gutter: text ran to the screen edge */
footer.site{padding:40px 28px}
@media(max-width:640px){footer.site{padding:32px 20px;justify-content:flex-start}}
footer.site .social a{color:inherit;text-decoration:none;border-bottom:1px solid transparent}
footer.site .social a:hover,footer.site .social a:focus-visible{border-color:currentColor}
"""


def isolate_ranges(text: str) -> str:
    """Wrap every non-price number range in the page's text nodes in LRI/PDI."""
    parts = re.split(r"(<script>.*?</script>|<style>.*?</style>)", text, flags=re.S)
    n = 0

    def in_text(chunk: str) -> str:
        nonlocal n

        def node(m):
            nonlocal n
            s, k = re.subn(r"(?<![₪\d.,])(\d{1,3}%?–\d{1,3}%?)(?![\d%])",
                           "\u2066\\1\u2069", m.group(0))
            n += k
            return s
        return re.sub(r">[^<>]*<", node, chunk)

    out = "".join(p if p.startswith(("<script>", "<style>")) else in_text(p) for p in parts)
    if n != 4:
        die(f"number ranges: expected 4 (econ, alcohol line, FAQ, bottle chip), found {n}")
    applied.append(f"number ranges ×{n}")
    return out


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

    # ── the footer's social names were plain text that looked like links ─
    # The URLs are the store's own, read from the live theme's settings_data.json
    # (social_instagram_link / social_facebook_link / social_youtube_link).
    text = sub("footer social links", "<span>אינסטגרם · פייסבוק · יוטיוב</span>",
               '<span class="social"><a href="https://www.instagram.com/gteveryday/" target="_blank" rel="noopener">אינסטגרם</a>'
               ' · <a href="https://facebook.com/greenteaeveryday" target="_blank" rel="noopener">פייסבוק</a>'
               ' · <a href="https://www.youtube.com/channel/UC7U7qL5vs9xt6Rzxj2GiSOg" target="_blank" rel="noopener">יוטיוב</a></span>',
               text)

    # ── the matcha, hojicha and ube cards opened empty ──────────────────
    # openF() looks the product up by its card heading — FLMAP, POUCHCH, MKMORE
    # and FL are keyed by the Latin names — and the three pouch cards' headings
    # are Hebrew. So those three modals listed no drinks at all. The heading
    # stays what the reader sees; the lookup uses the key.
    text = sub("pouch lookup key", "const n=c.querySelector('h4').textContent.trim();",
               "const n0=c.querySelector('h4').textContent.trim(),"
               "n=({\"מאצ׳ה\":\"Matcha\",\"הוג׳יצ׳ה\":\"Hojicha\",\"אובה\":\"Ube\"})[n0]||n0;", text)
    text = sub("pouch modal title", "getElementById('fm-name').textContent=n;",
               "getElementById('fm-name').textContent=n0;", text)

    # ── English the extractor never saw, in the product matrix ──────────
    text = sub("matrix product names",
               "<span class=\"pn\">'+p+'</span><span class=\"pc\">'+(pairs.length?pairs.length+"
               "(pairs.length===1?' drink':' drinks'):'\\u2014')+'</span></div>';",
               "<span class=\"pn\">'+({Matcha:'מאצ׳ה',Ube:'אובה',Hojicha:'הוג׳יצ׳ה'}[p]||p)+"
               "'</span><span class=\"pc\">'+(pairs.length?(pairs.length===1?'משקה אחד':"
               "pairs.length+' משקאות'):'\\u2014')+'</span></div>';", text)
    text = sub("matrix empty note", "'No menu drinks yet.'", "'עדיין בלי מתכוני תפריט.'", text)
    text = sub("recipe source chip", "'\">'+n+' \\u2190</a>'",
               "'\">'+({Matcha:'מאצ׳ה',Ube:'אובה',Hojicha:'הוג׳יצ׳ה'}[n]||n)+' \\u2190</a>'", text)
    text = sub("price list toggle", "'Expand all'", "'פתחו הכול'", text)

    # ── the purée modal's title: "Mango · …" in English, and glued ──────
    text = sub("puree title",
               "getElementById('pm-title').textContent=p.t+' · באילו משקאות היא נכנסת';",
               "getElementById('pm-title').textContent='מחית '+({mango:'מנגו',strawberry:'תות',"
               "peach:'אפרסק'}[id]||p.t)+' · באילו משקאות היא נכנסת';", text)

    # ── "Massala": two recipe kickers kept the English source's misspelling ─
    text = sub("masala spelling", '"en": "Massala"', '"en": "Masala"', text, 2)

    # ── the four-step strip and the matrix links read the reader's way ──
    text = sub("step strip arrow", '<span class="sep">\\u2192</span>',
               '<span class="sep">\\u2190</span>', text)
    text = sub("matrix link arrow", "' \\u00b7 '+COLS[ci].t+' \\u2192</span>'",
               "' \\u00b7 '+COLS[ci].t+' \\u2190</span>'", text)

    # ── "−25%" rendered its minus on the wrong side in RTL ──────────────
    text = sub("minus sign direction", '<b style="color:var(--energy)">−25%</b>',
               '<b style="color:var(--energy)" dir="ltr">−25%</b>', text)

    # ── "0 מקום במקרר" becomes the shelf life, which is the same point ──
    # Tom-approved (Sales-Machine knowledge/claims/public-claims.yaml
    # #shelf_life): a closed bottle keeps a year with no refrigeration.
    text = sub("shelf-life stat", '<b class="num">0</b><span>חודשים על המדף לבקבוק סגור</span>',
               '<b class="num">12</b><span>חודשים על המדף לבקבוק סגור</span>', text)

    # ── the forward arrow points the reader's way ───────────────────────
    text = sub("recipe link arrow", "<u>\\u2192</u>", "<u>\\u2190</u>", text)

    # ── number ranges inside Hebrew run backwards ────────────────────────
    # "20–25 כוסות" rendered as "25–20": the en dash between two numbers takes
    # the paragraph's right-to-left direction, so the bidi algorithm swaps the
    # numbers. Each range is wrapped in an invisible left-to-right isolate (U+2066
    # … U+2069) — no visible character changes, so the approved alcohol sentence
    # keeps its exact wording and simply reads the way it was written. Price
    # ranges are left alone: they never reach the served page (strip_prices.py).
    text = isolate_ranges(text)

    text = sub("launch stylesheet", "</style>", CSS + "</style>", text)

    SRC.write_text(text, encoding="utf-8")
    print(f"launch: {len(applied)} fixes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
