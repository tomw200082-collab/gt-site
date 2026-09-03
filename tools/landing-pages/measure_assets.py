#!/usr/bin/env python3
"""Measure every theme asset the pages reference and write assets.json.

The <img> width/height attributes exist to give the browser the aspect ratio before
the bytes arrive. Hand-written guesses had all 13 of them wrong -- the plate image was
declared 720x720 against a real 700x1585, so the browser reserved a square and reflowed
to something 2.26x taller once the file landed. Measuring beats guessing; re-run this
whenever an asset is replaced.

Theme assets are not in this repo, so it reads them from the theme's public asset CDN.
"""
import io, json, os, re, sys, glob, urllib.request
from PIL import Image

CDN = 'https://cdn.shopify.com/s/files/1/0484/4319/5552/t/124/assets/'
HERE = os.path.dirname(os.path.abspath(__file__))

names = set()
for f in glob.glob(os.path.join(HERE, 'out', 'gt-lp-*.liquid')):
    names |= set(re.findall(r"\{\{ '([^']+)' \| asset_url \}\}", io.open(f, encoding='utf-8').read()))
if not names:
    sys.exit('no asset references found -- run gen.py first')

out = {}
for n in sorted(names):
    with urllib.request.urlopen(CDN + n) as r:
        out[n] = list(Image.open(io.BytesIO(r.read())).size)
    print(f'{n:24} {out[n][0]}x{out[n][1]}')

json.dump({'_': f'Intrinsic size of every theme asset the pages reference, measured from '
                f'{CDN} . Regenerate with measure_assets.py after replacing an asset.',
           'cdn': CDN, 'size': out},
          io.open(os.path.join(HERE, 'assets.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'\nassets.json: {len(out)} assets')
