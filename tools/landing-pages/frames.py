# -*- coding: utf-8 -*-
"""Cut the drinks section's ornamental frame, one per landing page.

Run:  python3 frames.py <dir-of-2048px-frame-pngs> <out-dir>

Source: Canva folder FAHUC3u8Qvw (Tom, 2026-09-03). Each is a square illustrated
border — birds, koi, blossom, lanterns — around a flat centre, and the four chosen
here are the ones whose centre colour is the page's own: amber for chai, green for
matcha, near-black for iced tea, deep purple for ube.

A square frame and a menu six rows tall do not fit each other. Tiling the border
would repeat a pheasant every 200px; stretching it would smear one. So the square is
used at full width twice, once anchored to the top of the section and once to its
bottom, and the ground between them is the frame's own centre colour. Only the
densest band of each end is ever on screen, so only those bands are shipped: the top
and bottom BAND fraction of the square, which is about a third of the pixels saved
against sending the whole thing.

The ground colour is measured from the centre of each frame rather than typed, and
the text colour is whichever of GT's ink or white clears 4.5:1 against it. Where
neither does -- amber sits almost exactly between them -- the ground is darkened in
small steps until the cream does, which is a change of a few percent and keeps the
band and the ground reading as one colour.
"""
import json
import os
import sys
from PIL import Image, ImageEnhance

# How much of each end of the square to ship. The section shows less than this at
# every viewport; the surplus is headroom for making the band taller in CSS without
# re-cutting the images. These are masters -- the page pulls a width-matched variant
# out of Shopify's resizer through srcset, so the master's own weight never lands on
# a reader.
BAND = 0.26

# The two colours gt-lp.css already puts on grounds: --ink for light ones, the
# --on-dark cream for dark ones. Pure white is deliberately not a candidate — nothing
# else on these pages sets text in it, and a fifth ink would be a fifth ink.
INK = (0x19, 0x1B, 0x14)
CREAM = (0xF1, 0xEC, 0xE0)
MIN_CONTRAST = 4.5


def luminance(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    lo, hi = sorted((la, lb))
    return (hi + 0.05) / (lo + 0.05)


def ground_and_text(im):
    """The frame's own centre colour, and a text colour that is legible on it."""
    w, h = im.size
    c = im.convert("RGB").crop((int(w * .44), int(h * .44), int(w * .56), int(h * .56)))
    px = list(c.getdata())
    g = tuple(sum(p[i] for p in px) // len(px) for i in range(3))

    best = max((CREAM, INK), key=lambda t: contrast(g, t))
    if contrast(g, best) >= MIN_CONTRAST:
        return g, best, 0
    # Neither passes -- amber sits almost exactly between them. Walk the ground toward
    # whichever side it is already closer to; darkening keeps the illustrated band and
    # the flat ground reading as one surface, which lightening would not.
    for step in range(1, 70):
        d = tuple(round(v * (1 - step / 100)) for v in g)
        if contrast(d, CREAM) >= MIN_CONTRAST:
            return d, CREAM, step
    raise SystemExit("no legible ground found")


def hexof(rgb):
    return "#%02X%02X%02X" % rgb


def main():
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    out = {}
    for page in ("chai", "matcha", "iced-tea", "ube"):
        im = Image.open(os.path.join(src, f"frame-{page}.png")).convert("RGB")
        w, h = im.size
        band = round(h * BAND)
        g, t, darkened = ground_and_text(im)
        # Where the ground had to be darkened for contrast, the band is darkened by
        # exactly the same amount. Otherwise the illustration keeps its original
        # ground colour and meets a darker one at the mask -- not a hard seam, but a
        # visible change of shade across what should be one surface.
        if darkened:
            im = ImageEnhance.Brightness(im).enhance(1 - darkened / 100)
        im.crop((0, 0, w, band)).save(
            os.path.join(dst, f"gtf-{page}-top.webp"), "WEBP", quality=86, method=6)
        im.crop((0, h - band, w, h)).save(
            os.path.join(dst, f"gtf-{page}-bot.webp"), "WEBP", quality=86, method=6)
        out[page] = {"ground": hexof(g), "on": hexof(t),
                     "contrast": round(contrast(g, t), 2), "darkened_pct": darkened}
        sz = [os.path.getsize(os.path.join(dst, f"gtf-{page}-{e}.webp")) for e in ("top", "bot")]
        print(f"  {page:<9} ground {hexof(g)}  text {hexof(t)}  "
              f"{contrast(g, t):.2f}:1  darkened {darkened}%  "
              f"{w}x{band} x2  {sum(sz)//1024} KB")
    out["_"] = ("Ornamental frame per landing page, from Canva folder FAHUC3u8Qvw "
                "(Tom, 2026-09-03), cut by tools/landing-pages/frames.py. 'ground' is "
                "measured from the centre of the frame, 'on' is the text colour that "
                "clears 4.5:1 on it, and 'darkened_pct' is how far the ground had to "
                "move for that -- 0 on three of the four.")
    out["band"] = BAND
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "frames.json"), "w"),
              ensure_ascii=False, indent=1)
    print("wrote frames.json")


if __name__ == "__main__":
    main()
