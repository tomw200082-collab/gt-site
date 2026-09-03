#!/usr/bin/env python3
"""Record the pixel size of every theme image, once, into a committed file.

Every `<img>` on the page ships without `width`/`height`. The browser therefore
cannot reserve space before an image arrives, so the layout jumps as 67 of them
load — the page's one real Core Web Vitals problem (CLS).

Fixing it needs the intrinsic size of each image, which is not in its URL. This
fetches the first 64 bytes of each asset and reads the dimensions out of the
container header — no decode, no image library, ~150 range requests once — and
writes `theme/assets.dimensions.json`. `build_theme.py` reads that file and
stamps the attributes; nothing fetches anything at build time.

    python3 tools/probe_dimensions.py            # fill in anything missing
    python3 tools/probe_dimensions.py --all      # re-probe everything

Assets whose origin is gone (the five known 403s) are simply absent from the
map, and the build leaves those images unstamped rather than guessing.
"""
import json
import struct
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "theme" / "assets.manifest.json"
OUT = ROOT / "theme" / "assets.dimensions.json"


def png_size(b: bytes):
    # 8-byte signature, 4-byte length, "IHDR", then two big-endian uint32.
    if b[:8] != b"\x89PNG\r\n\x1a\n" or b[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", b[16:24])


def webp_size(b: bytes):
    if b[:4] != b"RIFF" or b[8:12] != b"WEBP":
        return None
    chunk = b[12:16]
    if chunk == b"VP8 ":
        # lossy: 3-byte start code, then 16-bit width and height, 14 bits each
        w, h = struct.unpack("<HH", b[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if chunk == b"VP8L":
        # lossless: 1-byte signature, then 14 bits width-1, 14 bits height-1
        n = struct.unpack("<I", b[21:25])[0]
        return (n & 0x3FFF) + 1, ((n >> 14) & 0x3FFF) + 1
    if chunk == b"VP8X":
        # extended: 24-bit little-endian width-1 and height-1
        w = b[24] | b[25] << 8 | b[26] << 16
        h = b[27] | b[28] << 8 | b[29] << 16
        return w + 1, h + 1
    return None


def probe(url: str):
    req = urllib.request.Request(
        url,
        headers={
            # Without this the origin serves PNG for a .webp asset — the same
            # content negotiation that makes one hero image 800 KB instead of 94.
            "Accept": "image/webp,image/png,image/*",
            "Range": "bytes=0-63",
            "User-Agent": "gt-site-dimension-probe",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        head = r.read(64)
    return png_size(head) or webp_size(head)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    known = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    if "--all" in sys.argv:
        known = {}

    todo = [(n, u) for n, u in manifest.items() if n not in known]
    print(f"{len(known)} known, {len(todo)} to probe")

    failed = []
    for i, (name, url) in enumerate(todo, 1):
        try:
            size = probe(url)
        except Exception as e:  # a dead origin is expected for a few
            size = None
            failed.append((name, str(e)[:60]))
        if size:
            known[name] = list(size)
        elif not failed or failed[-1][0] != name:
            failed.append((name, "unreadable header"))
        if i % 25 == 0:
            print(f"  {i}/{len(todo)}")

    OUT.write_text(json.dumps(dict(sorted(known.items())), indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(known)} of {len(manifest)} assets sized")
    if failed:
        print(f"{len(failed)} not sized (left unstamped by the build):")
        for name, why in failed[:8]:
            print(f"  {name}  {why}")


if __name__ == "__main__":
    main()
