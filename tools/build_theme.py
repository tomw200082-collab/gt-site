#!/usr/bin/env python3
"""Split the built Hebrew page into a Shopify theme layer under theme/.

The page is one self-contained file; a theme wants it in pieces:

    (theme/layout/gt.liquid is NOT generated -- see the note below)
    theme/sections/gt-home.liquid the markup, plus a schema so it can be
                                  placed from the theme editor
    theme/templates/index.json    orders that one section
    theme/assets/gt-site.css      the stylesheet
    theme/assets/gt-site.js       the scripts
    theme/assets.manifest.json    image name -> source URL, for themeFilesUpsert

The layout used to be generated here too, assembled from the <head> of the source
page. It is now hand-maintained, because it carries per-page Liquid -- the share card
and SEO description each landing page needs -- that cannot be derived from a static
page. Generating it meant that anyone running this script silently reverted that.
Edit theme/layout/gt.liquid directly, and keep its tags in step with the record in
docs/2026-09-02_analytics.md.

Images: the page pulls 152 remote images through a third-party resizing proxy.
Five of them are gone — their origin now answers 403 — and those entries are
dropped so the page's own fallbacks take over instead of requesting a 404.
The rest become theme assets. Liquid resolves them in the markup; the script
file is not Liquid, so it carries bare filenames and prefixes them at runtime
from a base the section hands it.
"""
import hashlib
import html as htmllib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"
THEME = ROOT / "theme"

DEAD = (
    "hf_20260722_193042", "hf_20260722_193057", "hf_20260722_193119",
    "hf_20260722_195431", "hf_20260727_092900",
)

# Each asset is named `gt-<sha1(canonical url)[:10]>.<ext>`, and the extension
# records what the origin actually served — the one thing the URL alone does
# not tell us. `theme/assets.manifest.json` maps every asset back to its URL,
# so it carries that fact durably; the content-type survey it was first built
# from was a scratch file and is long gone.
MANIFEST = THEME / "assets.manifest.json"
MIME = {}
if MANIFEST.exists():
    for name, url in json.loads(MANIFEST.read_text(encoding="utf-8")).items():
        want = f"gt-{hashlib.sha1(url.encode()).hexdigest()[:10]}{Path(name).suffix}"
        if want != name:
            sys.exit(f"FAIL: manifest entry {name} does not hash from its own URL "
                     f"(expected {want}) — the manifest and the naming rule disagree")
        MIME[url] = "image/png" if name.endswith(".png") else "image/webp"

text = SRC.read_text(encoding="utf-8")

# ── 1. collect every remote image URL ───────────────────────────────────
def all_image_urls(s):
    out = set()
    for pat in (r'https://wsrv\.nl/\?[^"\'\s)\\]+',
                r'https://d2ol7oe51mr4n9\.cloudfront\.net/[^"\'\s)\\]+',
                # The partner logos and Tom's own photographs are the image
                # families this repo owns rather than borrows: they live in
                # theme/logos/ and theme/photos/ and are served from the repo, so
                # the same hash-name-and-manifest machinery carries them too.
                r'https://raw\.githubusercontent\.com/tomw200082-collab/gt-site/'
                r'main/theme/(?:logos|photos)/[^"\'\s)\\]+'):
        for m in re.finditer(pat, s):
            out.add(m.group(0))
    return out

raw_urls = all_image_urls(text)
# the same asset appears both HTML-escaped and raw; normalise for lookup
def canon(u):
    return htmllib.unescape(u)

asset_name = {}
skipped = []
for u in sorted(raw_urls):
    c = canon(u)
    if any(d in c for d in DEAD):
        skipped.append(u)
        continue
    mime = MIME.get(c, "image/webp")
    ext = "png" if mime.endswith("png") else "webp"
    asset_name[u] = f"gt-{hashlib.sha1(c.encode()).hexdigest()[:10]}.{ext}"

manifest = {}
for u, name in asset_name.items():
    manifest[name] = canon(u)

# ── 2. split out css / js ───────────────────────────────────────────────
styles = re.findall(r"<style>(.*?)</style>", text, re.S)
scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
if len(styles) != 1:
    sys.exit(f"expected 1 <style>, found {len(styles)}")

css = styles[0]
js = "\n;\n".join(scripts)

markup = re.sub(r"<style>.*?</style>", "", text, flags=re.S)
markup = re.sub(r"<script>.*?</script>", "", markup, flags=re.S)

# ── 2b. no prices on the served page ─────────────────────────────────────
#
# Tom, 2026-09-24: take the prices down so they are not seen. src/index.html stays
# the full, figure-verified build; the theme — markup and gt-site.js alike — is
# written without a single shekel while data/site_flags.json says show_prices: false.
# See tools/strip_prices.py for what goes and what stays.
sys.path.insert(0, str(ROOT / "tools"))
import strip_prices  # noqa: E402
SHOW_PRICES = strip_prices.show_prices()
if not SHOW_PRICES:
    markup = strip_prices.strip_markup(markup)
    js = strip_prices.strip_js(js)
    css += strip_prices.CSS

# ── 3. rewrite image references ─────────────────────────────────────────
def rewrite_markup(s):
    for u, name in asset_name.items():
        s = s.replace(u, "{{ '" + name + "' | asset_url }}")
    for u in skipped:
        s = s.replace(u, "")
    return s

def rewrite_js(s):
    """Turn each image URL literal into a concatenation against the asset base.

    Every URL in this file is a complete string literal (verified: none is
    embedded inside a longer string), and the data blobs holding them are
    declared with const/let or inside an IIFE — so they never reach `window`
    and cannot be fixed up at runtime. Rewriting the literal itself is the
    only form that works in every scope.
    """
    for u, name in asset_name.items():
        for quote in ('"', "'"):
            s = s.replace(quote + u + quote,
                          '(GT_ASSET_BASE+' + quote + name + quote + ')')
    return s

# ── 3b. two things Tom can switch without a deploy ──────────────────────
#
# Only settings the generator does NOT own may go in the theme editor. The page
# copy is built from i18n/parts/, so exposing it here would create a second
# source: an edit made in the editor is silently overwritten by the next
# build_theme.py. These two are safe because nothing in the build writes them.
#
# show_pricing is one of them while prices are shown at all: strip_prices.price_list()
# either wraps the wholesale price list in it or leaves the list out of the theme.
markup = strip_prices.price_list(markup, SHOW_PRICES)

# show_portal_entry (gate G-27, W10): the three placements of the customer portal entry
# that patch_rtl_shell.py writes are wrapped in one theme-editor switch, default off, so
# the staged theme carries the iPad recipe fixes without the entry until M5.
_portal_links = re.findall(r'<a class="portal-(?:ico|link|pill)"[^>]*>.*?</a>', markup, flags=re.S)
if len(_portal_links) != 3:
    sys.exit(f"expected 3 portal entry links, found {len(_portal_links)}")
for _a in _portal_links:
    markup = markup.replace(_a, "{% if section.settings.show_portal_entry %}" + _a + "{% endif %}", 1)


# ── 3c. width and height on every image ─────────────────────────────────
#
# Not one of the 67 <img> tags carried them, so the browser could not reserve
# space and the layout jumped as each image arrived — the page's one real Core
# Web Vitals problem. The intrinsic sizes come from theme/assets.dimensions.json,
# probed once by tools/probe_dimensions.py; nothing is fetched at build time.
# An asset with no recorded size is left alone rather than guessed at.
DIMENSIONS = json.loads((THEME / "assets.dimensions.json").read_text(encoding="utf-8")) \
    if (THEME / "assets.dimensions.json").exists() else {}

def stamp_dimensions(s: str) -> tuple[str, int]:
    stamped = 0

    def one(m):
        nonlocal stamped
        tag = m.group(0)
        if "width=" in tag or "height=" in tag:
            return tag
        src = re.search(r'src="([^"]+)"', tag)
        if not src:
            return tag
        name = asset_name.get(src.group(1)) or asset_name.get(htmllib.unescape(src.group(1)))
        size = DIMENSIONS.get(name) if name else None
        if not size:
            return tag
        stamped += 1
        return tag[:-1].rstrip() + f' width="{size[0]}" height="{size[1]}">'

    return re.sub(r"<img\b[^>]*>", one, s), stamped

markup, stamped_imgs = stamp_dimensions(markup)

markup = rewrite_markup(markup)
js = rewrite_js(js)

# Drop the five dead entries so the page's own fallbacks are used.
removed = 0
for d in DEAD:
    # "key": "https://…hf_xxx…"   and   "key": ["https://…"]
    js, n = re.subn(r'"[^"]{1,60}"\s*:\s*"[^"]*' + d + r'[^"]*"\s*,?', "", js)
    removed += n
    js, n = re.subn(r'"[^"]{1,60}"\s*:\s*\{[^{}]*' + d + r'[^{}]*\}\s*,?', "", js)
    removed += n
    # CHAPTER_SCENES uses bare numeric keys and single quotes:  4:{url:'…',n:6},
    js, n = re.subn(r"[\w\"']{1,40}\s*:\s*\{[^{}]*" + d + r"[^{}]*\}\s*,?", "", js)
    removed += n
js = re.sub(r",\s*\}", "}", js)
js = re.sub(r"\{\s*,", "{", js)

PRELUDE = """/* This file is served as a static asset, so Liquid never runs over it.
   Image references below are written as GT_ASSET_BASE + "<filename>"; the
   section sets window.GT_ASSET_BASE before this script loads. */
var GT_ASSET_BASE = (typeof window !== 'undefined' && window.GT_ASSET_BASE) || '';
"""

js = PRELUDE + js

# ── 4. assemble the theme ───────────────────────────────────────────────
body = re.search(r"<body[^>]*>(.*)</body>", markup, re.S)
if not body:
    sys.exit("no <body> found")
body_html = body.group(1).strip()

# GA4, when Tom puts an id in the theme editor. Appended to the body rather than
# the markup because the assembly above takes only what is inside <body>.
body_html += """
{%- if section.settings.analytics_id != blank -%}
<script async src="https://www.googletagmanager.com/gtag/js?id={{ section.settings.analytics_id }}"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());gtag('config','{{ section.settings.analytics_id }}');
</script>
{%- endif -%}
"""

OG_IMAGE = "gt-cd7b9d4764.webp"
if OG_IMAGE not in manifest:
    sys.exit(f"FAIL: og:image asset {OG_IMAGE} is not in the manifest — "
             "theme/layout/gt.liquid names it as the default share card")

# ── structured data ─────────────────────────────────────────────────────
#
# The FAQ this page already answers. The questions are read out of the built
# markup rather than retyped, so the schema cannot drift from what a reader sees
# — the same rule the figures follow. Organization lives in the layout, once, on
# every page rather than only this one.
def faq_pairs(html_: str):
    out = []
    for m in re.finditer(r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>",
                         html_, re.S):
        q = re.sub(r"<[^>]+>", " ", m.group(1))
        a = re.sub(r"<[^>]+>", " ", m.group(2))
        q, a = " ".join(q.split()), " ".join(a.split())
        # The drink modal uses <details> too; only real prose Q&A qualifies.
        if q.endswith("?") and 20 <= len(a) <= 900:
            out.append((q, a))
    return out

_faq = faq_pairs(body_html)
STRUCTURED_DATA = "" if not _faq else (
    '<script type="application/ld+json">'
    + json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in _faq
        ],
      }, ensure_ascii=False, separators=(",", ":"))
    + "</script>"
)

# ── 3f. the third-party pixels ──────────────────────────────────────────
#
# The tag manager the live homepage carries lives in theme/layout/gt.liquid,
# which is hand-maintained — this script no longer writes that file. What the
# live homepage loads, and why GA4 needs no ID pasted anywhere, is measured in
# docs/2026-09-02_analytics.md.
#
# The two vendor pixels the live homepage also carries. Behind a switch because
# they are marketing tooling rather than measurement, and a page aimed at cafe
# owners may not want either — the default matches the live page so publishing
# changes nothing, and turning them off is a click rather than a build.
# Both are loaded async here; on the live theme rmShopifyUtils.min.js is a
# render-blocking <script src>, which is the very cost this page spent effort
# removing.
THIRD_PARTY = """
{% if section.settings.third_party_pixels %}
<!-- Taboola -->
<script>
window._tfa = window._tfa || [];
window._tfa.push({notify: 'event', name: 'page_view', id: 1547330});
!function (t, f, a, x) { if (!document.getElementById(x)) {
  t.async = 1; t.src = a; t.id = x; f.parentNode.insertBefore(t, f); } }
(document.createElement('script'), document.getElementsByTagName('script')[0],
 '//cdn.taboola.com/libtrc/unip/1547330/tfa.js', 'tb_tfa_script');
</script>
<!-- Retention Rocket -->
<script>
var _rmData = _rmData || [];
_rmData.push(['setStoreKey', 'ym6nRgm7']);
{% if customer %}_rmData.push(['setCustomer', {{ customer.email | json }}]);{% endif %}
</script>
<script async src="https://d3ryumxhbd2uw7.cloudfront.net/webtracking/track.js"></script>
<script async src="https://d3ryumxhbd2uw7.cloudfront.net/webtracking/rmShopifyUtils.min.js"></script>
{% endif %}
"""

PRICING_SETTING = ("""    { "type": "checkbox", "id": "show_pricing", "default": true,
      "label": "\u05d4\u05e6\u05d2\u05ea \u05de\u05d7\u05d9\u05e8\u05d5\u05df \u05e1\u05d9\u05d8\u05d5\u05e0\u05d0\u05d9",
      "info": "\u05db\u05d9\u05d1\u05d5\u05d9 \u05de\u05e1\u05ea\u05d9\u05e8 \u05d0\u05ea \u05db\u05dc \u05e8\u05e9\u05d9\u05de\u05ea \u05d4\u05de\u05d7\u05d9\u05e8\u05d9\u05dd \u05de\u05d4\u05e2\u05de\u05d5\u05d3. \u05d4\u05de\u05d7\u05d9\u05e8\u05d9\u05dd \u05e2\u05e6\u05de\u05dd \u05dc\u05d0 \u05de\u05e9\u05ea\u05e0\u05d9\u05dd." },
""" if SHOW_PRICES else "")

PORTAL_SETTING = """    { "type": "checkbox", "id": "show_portal_entry", "default": false,
      "label": "\u05db\u05e0\u05d9\u05e1\u05ea \u05dc\u05e7\u05d5\u05d7\u05d5\u05ea \u05d1\u05ea\u05e4\u05e8\u05d9\u05d8",
      "info": "\u05de\u05e6\u05d9\u05d2 \u05d0\u05ea \u05d4\u05e7\u05d9\u05e9\u05d5\u05e8 \u05dc\u05e4\u05d5\u05e8\u05d8\u05dc \u05d4\u05d4\u05d6\u05de\u05e0\u05d5\u05ea \u05d1\u05ea\u05e4\u05e8\u05d9\u05d8 \u05d5\u05d1\u05db\u05d5\u05ea\u05e8\u05ea. \u05dc\u05d4\u05e4\u05e2\u05d9\u05dc \u05e8\u05e7 \u05d0\u05d7\u05e8\u05d9 \u05e9\u05d4\u05e4\u05d5\u05e8\u05d8\u05dc \u05e4\u05ea\u05d5\u05d7 \u05dc\u05db\u05dc \u05d4\u05dc\u05e7\u05d5\u05d7\u05d5\u05ea." },
"""

SECTION = f"""{{%- comment -%}}
  GT Everyday brand site — the whole v5 R124 page as one section.
  Generated by tools/build_theme.py from src/index.html. Edit the source and
  rebuild; changes made here are overwritten.
{{%- endcomment -%}}

<script>
  window.GT_ASSET_BASE = "{{{{ 'gt-site.css' | asset_url | split: '?' | first | remove: 'gt-site.css' }}}}";
</script>

{body_html}

{STRUCTURED_DATA}

<script src="{{{{ 'gt-site.js' | asset_url }}}}" defer></script>
{THIRD_PARTY}
{{% schema %}}
{{
  "name": "GT brand site",
  "settings": [
{PRICING_SETTING}{PORTAL_SETTING}    {{ "type": "checkbox", "id": "third_party_pixels", "default": true,
      "label": "פיקסלים של צד שלישי",
      "info": "Taboola ו־Retention Rocket — אותם פיקסלים שרצים היום בעמוד הבית. כיבוי מסיר אותם מהעמוד הזה בלבד." }},
    {{ "type": "text", "id": "analytics_id", "label": "GA4 Measurement ID נוסף",
      "info": "השאירו ריק. נכס ה־GA4 של החנות כבר רץ בעמוד הזה דרך ערוץ Google של שופיפיי, והזנה כאן תטען gtag פעם שנייה ותספור כל צפייה פעמיים. השדה קיים רק למדידה נפרדת ונוספת — ראו docs/2026-09-02_analytics.md." }}
  ],
  "presets": [{{ "name": "GT brand site" }}]
}}
{{% endschema %}}
"""

INDEX = {
    "layout": "gt",
    "sections": {"main": {"type": "gt-home", "settings": {}}},
    "order": ["main"],
}

if not SHOW_PRICES:
    strip_prices.assert_clean("sections/gt-home.liquid", SECTION)
    strip_prices.assert_clean("assets/gt-site.js", js)

THEME.mkdir(exist_ok=True)
for sub in ("layout", "sections", "templates", "assets"):
    (THEME / sub).mkdir(exist_ok=True)

(THEME / "sections" / "gt-home.liquid").write_text(SECTION, encoding="utf-8")
(THEME / "templates" / "index.json").write_text(
    json.dumps(INDEX, indent=2) + "\n", encoding="utf-8")
(THEME / "assets" / "gt-site.css").write_text(css, encoding="utf-8")
(THEME / "assets" / "gt-site.js").write_text(js, encoding="utf-8")
(THEME / "assets.manifest.json").write_text(
    json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")

b = lambda p: len((THEME / p).read_text(encoding="utf-8").encode())
print(f"  sections/gt-home.liquid {b('sections/gt-home.liquid'):>8,} bytes  (limit 256 KB)")
print(f"  templates/index.json    {b('templates/index.json'):>8,} bytes")
print(f"  assets/gt-site.css      {b('assets/gt-site.css'):>8,} bytes")
print(f"  assets/gt-site.js       {b('assets/gt-site.js'):>8,} bytes")
print(f"  images in manifest      {len(manifest):>8,}")
print(f"  images sized              {stamped_imgs:>8,}  (width/height stamped)")
print(f"  FAQ entries in schema     {len(_faq):>8,}")
print(f"  dead images dropped     {len(skipped):>8,}  ({removed} data entries removed)")
print(f"  prices                  {'shown' if SHOW_PRICES else 'none — ' + str(len(strip_prices.applied)) + ' edits'}")
lo = [n for n in (b('sections/gt-home.liquid'),) if n > 256*1024]
if lo:
    sys.exit("section exceeds the 256 KB Liquid file limit")
