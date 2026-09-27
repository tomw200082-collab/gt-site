#!/usr/bin/env python3
"""Put the whole GT file set on a theme, and prove the theme then holds exactly that set.

2026-09-27: three merged site PRs (#22, #23, #25) had never reached the live theme, the
landing pages there were two PRs behind, and the favicon existed only inside the live
theme. Each upload had sent only the files its own PR changed, previews were duplicated
from whichever theme looked newest, and publishing swaps the whole theme. So this tool
never sends a subset: it stages every GT file from this checkout, pushes all of them, and
compares the theme against the staged set file by file.

    python3 tools/theme_ship.py check <theme_id>                 read-only: what differs
    python3 tools/theme_ship.py push  <theme_id> [--allow-live]  push the set, then check

`push` = pull the target, stage, push with --nodelete, pull again, check. It exits 1 if
anything still differs. The live theme needs --allow-live, and only on Tom's word
(PUBLISH.md). Both use the Shopify CLI with SHOPIFY_CLI_THEME_TOKEN (Theme Access), and
leave the staged and pulled directories on disk as the evidence.

What the check compares:
  * Liquid, CSS and JS: md5, the same value the Admin API reports as checksumMd5.
  * templates/*.json: parsed JSON, ignoring the /* … */ header Shopify adds.
  * images: presence by name (content-addressed gt-<hash>.*, and every asset a staged
    section names).

Theme-owned, never overwritten from here: config/settings_data.json (the favicon lives
there) is not in the set, and each template's sections.main.settings are copied from the
target theme at staging time (show_portal_entry, third_party_pixels, analytics_id on the
home page).
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE = "greenteaeveryday.myshopify.com"
CLI = ["npx", "-y", "@shopify/cli@4.8.2", "theme"]
LP = ROOT / "tools" / "landing-pages" / "out"
# What `pull` fetches: a superset of the GT set, so the check sees every file it compares.
PULL_ONLY = ["layout/gt.liquid", "sections/gt-*", "assets/gt-*",
             "templates/index.json", "templates/index.*.json", "templates/page.*.json"]


def gt_set() -> dict[str, Path]:
    """Theme path -> source file, for every text file the GT set holds."""
    files = {"layout/gt.liquid": ROOT / "theme/layout/gt.liquid",
             "sections/gt-home.liquid": ROOT / "theme/sections/gt-home.liquid",
             "assets/gt-site.css": ROOT / "theme/assets/gt-site.css",
             "assets/gt-site.js": ROOT / "theme/assets/gt-site.js",
             "templates/index.json": ROOT / "theme/templates/index.json"}
    for f in sorted(LP.iterdir()):
        folder = {".liquid": "sections", ".css": "assets", ".js": "assets", ".json": "templates"}[f.suffix]
        files[f"{folder}/{f.name}"] = f
    return files


def images() -> list[str]:
    return sorted(json.loads((ROOT / "theme/assets.manifest.json").read_text(encoding="utf-8")))


def template(text: str) -> dict:
    """A JSON template, without the /* … */ header Shopify writes above it."""
    return json.loads(re.sub(r"^\s*/\*.*?\*/", "", text, count=1, flags=re.S))


def cli(*args: str) -> None:
    # The token reaches the CLI through its own environment variable; it is never an argument.
    subprocess.run(CLI + list(args) + ["--store", STORE], check=True)


def settled(theme: str) -> None:
    """Wait out a fresh duplicate. On 2026-09-27 a push landed while the copy job was still
    running, and the job then wrote the old sections back over it."""
    for _ in range(60):
        out = subprocess.run(CLI + ["list", "--json", "--store", STORE], check=True,
                             capture_output=True, text=True).stdout
        if not next(t for t in json.loads(out) if str(t["id"]) == theme)["processing"]:
            return
        time.sleep(5)
    sys.exit(f"FAIL: theme {theme} is still processing after 5 minutes")


def pull(theme: str) -> Path:
    out = Path(tempfile.mkdtemp(prefix=f"gt-pull-{theme}-"))
    cli("pull", "--theme", theme, "--path", str(out), *[a for g in PULL_ONLY for a in ("--only", g)])
    return out


def stage(target: Path) -> Path:
    """The GT set in theme layout, for the theme pulled into `target`."""
    out = Path(tempfile.mkdtemp(prefix="gt-stage-"))
    for sub in ("assets", "config", "layout", "locales", "sections", "snippets", "templates"):
        (out / sub).mkdir()  # the CLI wants a theme-shaped folder; empty ones upload nothing
    for rel, src in gt_set().items():
        text = src.read_text(encoding="utf-8")
        if rel.startswith("templates/") and (target / rel).exists():
            mine, theirs = json.loads(text), template((target / rel).read_text(encoding="utf-8"))
            mine["sections"]["main"]["settings"] = theirs["sections"]["main"].get("settings", {})
            text = json.dumps(mine, indent=2, ensure_ascii=False) + "\n"
        (out / rel).write_text(text, encoding="utf-8")
    urls = json.loads((ROOT / "theme/assets.manifest.json").read_text(encoding="utf-8"))
    for name in images():
        if not (target / "assets" / name).exists():
            (out / "assets" / name).write_bytes(urllib.request.urlopen(urls[name], timeout=60).read())
    staged = {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}
    extra = staged - set(gt_set()) - {f"assets/{n}" for n in images()}
    if extra:
        sys.exit(f"FAIL: staging holds files outside the GT set: {sorted(extra)}")
    print(f"staged {len(staged)} files in {out}")
    return out


def drift(staged: Path, theme: Path) -> list[str]:
    diffs = []
    md5 = lambda p: hashlib.md5(p.read_bytes()).hexdigest()
    for rel in gt_set():
        mine, theirs = staged / rel, theme / rel
        if not theirs.exists():
            diffs.append(f"missing  {rel}")
        elif rel.startswith("templates/"):
            if template(mine.read_text(encoding="utf-8")) != template(theirs.read_text(encoding="utf-8")):
                diffs.append(f"differs  {rel} (parsed JSON)")
        elif md5(mine) != md5(theirs):
            diffs.append(f"differs  {rel}  theme {md5(theirs)[:8]}  repo {md5(mine)[:8]}")
    named = set(images())
    for rel in gt_set():
        if rel.endswith(".liquid"):
            named |= set(re.findall(r"'([^']+)' \| asset_url", (staged / rel).read_text(encoding="utf-8")))
    diffs += [f"missing  assets/{n}" for n in sorted(named) if not (theme / "assets" / n).exists()]
    return diffs


def report(staged: Path, theme: Path) -> int:
    diffs = drift(staged, theme)
    for d in diffs:
        print(d)
    print(f"drift: {len(diffs)} difference(s) across {len(gt_set())} files and "
          f"{len(images())} images · staged {staged} · theme {theme}")
    return 1 if diffs else 0


def self_test() -> None:
    a, b = Path(tempfile.mkdtemp()), Path(tempfile.mkdtemp())
    for rel, src in gt_set().items():
        for d in (a, b):
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            (d / rel).write_bytes(src.read_bytes())
    (b / "assets").mkdir(exist_ok=True)
    for n in images() + ["gt-lp-ube-hero-cropped.webp", "gt-btl-fresh.webp"]:
        (b / "assets" / n).touch()
    named = {n for rel in gt_set() if rel.endswith(".liquid")
             for n in re.findall(r"'([^']+)' \| asset_url", (a / rel).read_text(encoding="utf-8"))}
    for n in named:
        (b / "assets" / n).touch()
    assert drift(a, b) == [], drift(a, b)
    idx = b / "templates/index.json"
    idx.write_text("/* Shopify's header */\n" + json.dumps(template(idx.read_text(encoding="utf-8"))))
    assert drift(a, b) == [], "a header and reformatting are not drift"
    (b / "assets/gt-site.js").write_text("changed")
    (b / "sections/gt-home.liquid").unlink()
    (b / "assets" / images()[0]).unlink()
    got = sorted(d.split()[1] for d in drift(a, b))
    assert got == sorted(["assets/gt-site.js", "sections/gt-home.liquid", f"assets/{images()[0]}"]), got
    print("self-test ok: identical passes, header ignored, changed/missing file and missing image caught")


def main() -> int:
    args = sys.argv[1:]
    if args == ["--self-test"]:
        self_test()
        return 0
    if len(args) < 2 or args[0] not in ("check", "push"):
        sys.exit(__doc__)
    cmd, theme, live = args[0], args[1], "--allow-live" in args
    settled(theme)
    target = pull(theme)
    staged = stage(target)
    if cmd == "check":
        return report(staged, target)
    cli("push", "--theme", theme, "--path", str(staged), "--nodelete", *(["--allow-live"] if live else []))
    return report(staged, pull(theme))


if __name__ == "__main__":
    sys.exit(main())
