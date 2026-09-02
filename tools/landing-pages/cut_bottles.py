#!/usr/bin/env python3
"""Cut the concentrate bottles out of their studio grey, for the iced-tea line strip.

The source frames live in Shopify Files (fresh.jpg, detox.jpg, ...): the same bottle
shot eight times against a grey sweep. They were sitting unused while the iced-tea
page illustrated nine named concentrates with a single FRESH bottle.

Two things this does not do the obvious way, both learned the hard way:

* Border-seeded flood fill, not a global threshold. The glass carries bright specular
  highlights, and a plain "bright and unsaturated is background" test eats them out of
  the middle of the bottle. Flooding inward from the frame only removes ground that is
  actually connected to the edge.

* The brightness cut is derived per frame. These eight were shot at visibly different
  exposures -- the darkest border pixel is 128 on namastea and 82 on desert -- so one
  fixed cut of 100 left desert's and calm's dark corners outside the candidate mask,
  the flood had nothing to seed from there, and both came back with the whole frame
  still attached.

Writes cut/<name>.webp at a uniform 560px height. Upload as assets/gt-bot-<name>.webp,
then re-run measure_assets.py.
"""
import io, os, sys, urllib.request
from PIL import Image, ImageChops, ImageDraw, ImageFilter

FILES = 'https://cdn.shopify.com/s/files/1/0484/4319/5552/files/'
NAMES = ['fresh', 'detox', 'revive', 'energy', 'consciousness', 'calm', 'desert', 'namastea']
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cut')
os.makedirs(OUT, exist_ok=True)

for name in NAMES:
    with urllib.request.urlopen(f'{FILES}{name}.jpg?width=700') as r:
        im = Image.open(io.BytesIO(r.read())).convert('RGB')
    w, h = im.size
    lum = im.convert('L')
    border = ([lum.getpixel((x, y)) for x in range(0, w, 6) for y in (0, h - 1)] +
              [lum.getpixel((x, y)) for y in range(0, h, 6) for x in (0, w - 1)])
    cut = max(60, min(border) - 12)

    r_, g_, b_ = im.split()
    mx = ImageChops.lighter(ImageChops.lighter(r_, g_), b_)
    mn = ImageChops.darker(ImageChops.darker(r_, g_), b_)
    sat = ImageChops.subtract(mx, mn)
    work = ImageChops.multiply(Image.eval(sat, lambda v: 255 if v < 30 else 0),
                               Image.eval(lum, lambda v: 255 if v > cut else 0)).convert('L')
    for x in range(0, w, 8):
        for y in (0, h - 1):
            if work.getpixel((x, y)) == 255: ImageDraw.floodfill(work, (x, y), 128, thresh=0)
    for y in range(0, h, 8):
        for x in (0, w - 1):
            if work.getpixel((x, y)) == 255: ImageDraw.floodfill(work, (x, y), 128, thresh=0)

    alpha = work.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MedianFilter(5))
    out = im.copy(); out.putalpha(alpha); out = out.crop(alpha.getbbox())
    out = out.resize((max(1, round(out.width * 560 / out.height)), 560), Image.LANCZOS)
    out.save(f'{OUT}/{name}.webp', 'WEBP', quality=88, method=4)
    print(f'{name:15} border-min {min(border):3}  cut {cut:3}  -> {out.size}')

print(f'\n{len(NAMES)} cut into {OUT}/  '
      '-- a bottle whose width lands far from ~245 means the ground survived; look at it.')
