# -*- coding: utf-8 -*-
"""Cut the 48 drink photographs out of their Canva exports, onto one shared canvas.

Run:  python3 cut_shots.py <dir-of-canva-exports> <out-dir>

Each export is a transparent PNG of one glass standing on a soft drop shadow. Two
things have to come out of that, and they pull in opposite directions: every glass
must render at exactly the same size on the card, and no glass or shadow may be
sliced by the edge of its own image.

The first cut of this pipeline trimmed each export to its alpha bounding box at
alpha>=160. That threshold was chosen to keep the drop shadow out of the box, and it
did — along with the outside of the glass. A glass is glass: its wall, its rim and
the highlight along it sit well under alpha 160, so the box closed inside them and
45 of the 48 shots shipped with the drink chopped flat against one or more edges.

What separates a glass from its shadow is shape, not value. Measured on
DAHUB19gTQ0: across the right wall the alpha falls 236 -> 69 in four pixels and then
decays over the next hundred; the wall is a cliff, the shadow is a hill. So the
glass is found by growing what is certainly glass (alpha>=140) by a radius wider
than that cliff and far narrower than the hill, and keeping the faint pixels that
growth reaches. The shadow is then still there, still whole — it is simply no longer
what decides the crop.

With the glass located, every shot is scaled so the glass is GLASS_H tall and pasted
into one canvas, the same size for all 48, with PAD of room around the glass for the
shadow. PAD is the widest overhang any of the 48 needs, measured at alpha 8 — below
that a grey shadow on a white card is under one part in thirty of a shade and cannot
be seen. Because the canvas is identical everywhere, the card's object-fit:contain
box does no work: all 48 glasses land at one size, on one baseline, aligned.

The costs, stated: the glass fills 73% of the canvas height rather than all of it,
so the card's image box has to be about a quarter larger to hold the same drink at
the same size; and a garnish that stands above the rim counts as part of the glass,
so a tall sprig makes that drink's glass smaller. Both are the price of a shadow
that is not cut, which is the thing being bought here.
"""
import json
import os
import sys
from PIL import Image, ImageChops, ImageFilter

# The glass itself, identical on every shot. 760 gives the card's 203px box a 2x
# master and Shopify something to downscale from; nothing on the page paints it
# at full size.
GLASS_H = 760

# Alpha below this is invisible against the white card, so it does not have to fit.
FAINT = 8

# Room for the shadow, as a fraction of the glass's height: the widest overhang any
# of the 48 exports needs at alpha FAINT, plus SLACK. The shadow falls right and
# down on every shot, which is why the box is not symmetric. Re-measure with
# --measure if the folder is ever re-shot; --measure prints these numbers without
# the slack, which is added here.
#
# The slack is not decoration. Measuring the overhang at alpha FAINT puts the
# outermost pixel *at* alpha FAINT, so a canvas sized to exactly that lands with
# one row of alpha-8 pixels against the edge and the audit below — correctly —
# calls it clipped. A few thousandths of the glass height is enough to clear it.
SLACK = 0.006
PAD = {"l": 0.118 + SLACK, "r": 0.331 + SLACK, "t": 0.115 + SLACK, "b": 0.257 + SLACK}

# The widest glass in the folder, as width / height. The canvas has to hold it.
WIDEST = 0.756

# Certainly glass. Anything above this is opaque drink, wall or garnish.
SOLID = 140
# The growth radius, as a fraction of image height: wider than the glass's own
# anti-aliased edge (~4px at 1560), far narrower than the shadow (~100px).
GROW = 0.008


# The morphology runs on the alpha channel shrunk by this factor. A max filter is
# O(radius^2) per pixel in PIL and the radius here is twelve, so full resolution
# costs about a minute an image for a result that is only ever used as a bounding
# box. Quartering the side lengths is a sixteen-fold saving and can misplace an edge
# by at most SHRINK pixels, which the box is then grown by to stay conservative —
# and the box only decides framing, never which pixels survive.
SHRINK = 4


def glass_box(img):
    """The bounding box of the glass, with its drop shadow left out.

    Not a threshold: see the module docstring. Growing the solid core by GROW and
    intersecting with the faint mask keeps the translucent wall, which any single
    threshold high enough to drop the shadow would cut off."""
    w, h = img.size
    a = img.getchannel("A").resize((max(1, w // SHRINK), max(1, h // SHRINK)),
                                   Image.BILINEAR)
    core = a.point(lambda v: 255 if v >= SOLID else 0)
    faint = a.point(lambda v: 255 if v >= 10 else 0)
    r = max(2, round(h * GROW / SHRINK))
    grown = core.filter(ImageFilter.MaxFilter(2 * r + 1))
    b = ImageChops.multiply(grown, faint).getbbox()
    return (max(0, b[0] * SHRINK - SHRINK), max(0, b[1] * SHRINK - SHRINK),
            min(w, b[2] * SHRINK + SHRINK), min(h, b[3] * SHRINK + SHRINK))


def canvas_size():
    w = round(GLASS_H * (WIDEST + PAD["l"] + PAD["r"]))
    h = round(GLASS_H * (1 + PAD["t"] + PAD["b"]))
    return w, h


def place(img):
    """One export -> the shared canvas, glass scaled to GLASS_H and set on the
    common baseline with PAD['l'] of room to its left."""
    W, H = canvas_size()
    gb = glass_box(img)
    s = GLASS_H / (gb[3] - gb[1])
    im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    g = [round(v * s) for v in gb]
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # Every glass gets the same left margin, so the row reads as one shelf rather
    # than as 48 photographs that happen to be side by side.
    gx = round(GLASS_H * PAD["l"])
    gy = round(GLASS_H * PAD["t"])
    out.alpha_composite(im, dest=(gx - g[0], gy - g[1]))
    return out


def edge_alpha(img):
    """The strongest alpha touching any edge. 0 means nothing is clipped at all;
    anything under FAINT cannot be seen on the card."""
    a = img.getchannel("A").load()
    w, h = img.size
    return max(max(a[0, y] for y in range(h)), max(a[w - 1, y] for y in range(h)),
               max(a[x, 0] for x in range(w)), max(a[x, h - 1] for x in range(w)))


def measure(src):
    """What PAD would have to be for this folder. Prints the widest overhang per
    side, so the constants above can be re-derived rather than guessed."""
    worst = {"l": 0.0, "r": 0.0, "t": 0.0, "b": 0.0}
    widest = 0.0
    for f in sorted(os.listdir(src)):
        if not f.endswith(".png"):
            continue
        im = Image.open(os.path.join(src, f)).convert("RGBA")
        gb = glass_box(im)
        fb = im.getchannel("A").point(lambda v: 255 if v >= FAINT else 0).getbbox()
        gh = gb[3] - gb[1]
        worst["l"] = max(worst["l"], (gb[0] - fb[0]) / gh)
        worst["r"] = max(worst["r"], (fb[2] - gb[2]) / gh)
        worst["t"] = max(worst["t"], (gb[1] - fb[1]) / gh)
        worst["b"] = max(worst["b"], (fb[3] - gb[3]) / gh)
        widest = max(widest, (gb[2] - gb[0]) / gh)
    print("PAD = " + json.dumps({k: round(v, 3) for k, v in worst.items()}))
    print(f"WIDEST = {widest:.3f}")


def main():
    if "--measure" in sys.argv:
        measure(sys.argv[1])
        return
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    W, H = canvas_size()
    print(f"canvas {W}x{H}  glass {GLASS_H} ({GLASS_H / H:.0%} of height)")
    worst = []
    for f in sorted(os.listdir(src)):
        if not f.endswith(".png"):
            continue
        did = f[:-4]
        out = place(Image.open(os.path.join(src, f)).convert("RGBA"))
        out.save(os.path.join(dst, f"gtd-{did}.webp"), "WEBP", quality=88, method=6)
        worst.append((edge_alpha(out), did))
    worst.sort(reverse=True)
    n = sum(1 for e, _ in worst if e >= FAINT)
    print(f"  shots            {len(worst):>4}")
    print(f"  clipped visibly  {n:>4}   (edge alpha >= {FAINT})")
    print("  strongest edge:  " + ", ".join(f"{d} {e}" for e, d in worst[:3]))
    if n:
        sys.exit("FAIL: a shot is cut where it can be seen — widen PAD")


if __name__ == "__main__":
    main()
