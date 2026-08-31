#!/usr/bin/env python3
"""Split the built Hebrew page into a Shopify theme layer under theme/.

The page is one self-contained file; a theme wants it in pieces:

    theme/layout/gt.liquid        minimal shell (the design brings its own
                                  header and footer, so Vodoma's chrome is
                                  deliberately not wrapped around it)
    theme/sections/gt-home.liquid the markup, plus a schema so it can be
                                  placed from the theme editor
    theme/templates/index.json    orders that one section
    theme/assets/gt-site.css      the stylesheet
    theme/assets/gt-site.js       the scripts
    theme/assets.manifest.json    image name -> source URL, for themeFilesUpsert

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

survey = {}
for line in (Path("/tmp/imgs/survey.tsv")).read_text().splitlines():
    idx, code, size, mime = line.split("\t")
    survey[idx] = mime
indexed = {}
for line in (Path("/tmp/imgs/indexed.tsv")).read_text().splitlines():
    idx, url = line.split("\t", 1)
    indexed[idx] = url
MIME = {url: survey[i] for i, url in indexed.items()}

text = SRC.read_text(encoding="utf-8")

# ── 1. collect every remote image URL ───────────────────────────────────
def all_image_urls(s):
    out = set()
    for pat in (r'https://wsrv\.nl/\?[^"\'\s)\\]+',
                r'https://d2ol7oe51mr4n9\.cloudfront\.net/[^"\'\s)\\]+'):
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

head = re.search(r"<head>(.*)</head>", markup, re.S).group(1)
metas = "\n".join(m.group(0) for m in re.finditer(r'<meta [^>]*>', head)
                  if 'charset' not in m.group(0) and 'viewport' not in m.group(0))
title = re.search(r"<title>(.*?)</title>", head, re.S).group(1).strip()
fonts = "\n".join(m.group(0) for m in re.finditer(r'<link [^>]*fonts\.[^>]*>', head))
preconnect = "\n".join(m.group(0) for m in re.finditer(r'<link rel="preconnect"[^>]*>', head))

SECTION = f"""{{%- comment -%}}
  GT Everyday brand site — the whole v5 R124 page as one section.
  Generated by tools/build_theme.py from src/index.html. Edit the source and
  rebuild; changes made here are overwritten.
{{%- endcomment -%}}

<script>
  window.GT_ASSET_BASE = "{{{{ 'gt-site.css' | asset_url | split: '?' | first | remove: 'gt-site.css' }}}}";
</script>

{body_html}

<script src="{{{{ 'gt-site.js' | asset_url }}}}" defer></script>

{{% schema %}}
{{
  "name": "GT brand site",
  "settings": [],
  "presets": [{{ "name": "GT brand site" }}]
}}
{{% endschema %}}
"""

LAYOUT = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{{{ page_title }}}}</title>
{preconnect}
{fonts}
{metas}
<link rel="canonical" href="{{{{ canonical_url }}}}">
{{{{ content_for_header }}}}
<link rel="stylesheet" href="{{{{ 'gt-site.css' | asset_url }}}}">
</head>
<body>
{{{{ content_for_layout }}}}
</body>
</html>
"""

INDEX = {
    "layout": "gt",
    "sections": {"main": {"type": "gt-home", "settings": {}}},
    "order": ["main"],
}

THEME.mkdir(exist_ok=True)
for sub in ("layout", "sections", "templates", "assets"):
    (THEME / sub).mkdir(exist_ok=True)

(THEME / "layout" / "gt.liquid").write_text(LAYOUT, encoding="utf-8")
(THEME / "sections" / "gt-home.liquid").write_text(SECTION, encoding="utf-8")
(THEME / "templates" / "index.json").write_text(
    json.dumps(INDEX, indent=2) + "\n", encoding="utf-8")
(THEME / "assets" / "gt-site.css").write_text(css, encoding="utf-8")
(THEME / "assets" / "gt-site.js").write_text(js, encoding="utf-8")
(THEME / "assets.manifest.json").write_text(
    json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")

b = lambda p: len((THEME / p).read_text(encoding="utf-8").encode())
print(f"  layout/gt.liquid        {b('layout/gt.liquid'):>8,} bytes")
print(f"  sections/gt-home.liquid {b('sections/gt-home.liquid'):>8,} bytes  (limit 256 KB)")
print(f"  templates/index.json    {b('templates/index.json'):>8,} bytes")
print(f"  assets/gt-site.css      {b('assets/gt-site.css'):>8,} bytes")
print(f"  assets/gt-site.js       {b('assets/gt-site.js'):>8,} bytes")
print(f"  images in manifest      {len(manifest):>8,}")
print(f"  dead images dropped     {len(skipped):>8,}  ({removed} data entries removed)")
lo = [n for n in (b('sections/gt-home.liquid'),) if n > 256*1024]
if lo:
    sys.exit("section exceeds the 256 KB Liquid file limit")
