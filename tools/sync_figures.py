#!/usr/bin/env python3
"""Keep data/drinks_final_figures.json identical to the figures of record.

The record lives in the production brain, not here:

    gt-factory-os-production-brain/.claude/skills/drinks-pricelist/
        drinks_final_figures.json

`docs/pricing/2026-08-27_COST_MODEL.md` names it as the figures of record. This
repo vendors a copy so the build works in CI, where the brain is not checked
out, and records its sha256 in a provenance sidecar.

Run with the brain present and the copy is refreshed from it, so correcting a
price is still a one-place edit: change the record, rebuild, and every figure on
the page moves. Run without it and the vendored copy is used as-is — the build
says which of the two it read, so a stale copy is never silent.

    python3 tools/sync_figures.py           # refresh if the brain is present
    python3 tools/sync_figures.py --check   # fail on drift, change nothing
"""
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDORED = ROOT / "data" / "drinks_final_figures.json"
PROVENANCE = ROOT / "data" / "drinks_final_figures.provenance.json"

# The brain sits beside this repo in the standard workspace layout. Paths are
# repo-relative by policy (brain CLAUDE.md §Workspace), so this is a sibling
# lookup, not a hardcoded machine path.
SOURCE = (
    ROOT.parent
    / "gt-factory-os-production-brain"
    / ".claude"
    / "skills"
    / "drinks-pricelist"
    / "drinks_final_figures.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(SOURCE.parents[3]), *args],
            capture_output=True,
            text=True,
            check=False,
        )
        return out.stdout.strip()
    except OSError:
        return ""


def main() -> None:
    check_only = "--check" in sys.argv

    if not VENDORED.exists():
        sys.exit(f"FAIL: {VENDORED.relative_to(ROOT)} is missing and is the build's input")

    vendored_hash = sha256(VENDORED)

    if not SOURCE.exists():
        if check_only:
            print(f"figures: brain not present — vendored copy {vendored_hash[:12]} unverified")
            return
        print(f"figures: brain not present — using vendored copy {vendored_hash[:12]}")
        return

    source_hash = sha256(SOURCE)
    if source_hash == vendored_hash:
        print(f"figures: vendored copy matches the record ({vendored_hash[:12]})")
        return

    if check_only:
        sys.exit(
            "FAIL: data/drinks_final_figures.json has drifted from the record.\n"
            f"  record   {source_hash[:12]}  {SOURCE}\n"
            f"  vendored {vendored_hash[:12]}\n"
            "  run: python3 tools/sync_figures.py"
        )

    VENDORED.write_bytes(SOURCE.read_bytes())
    meta = json.loads(VENDORED.read_text(encoding="utf-8"))["_meta"]
    PROVENANCE.write_text(
        json.dumps(
            {
                "source_repo": "gt-factory-os-production-brain",
                "source_path": ".claude/skills/drinks-pricelist/drinks_final_figures.json",
                "sha256": source_hash,
                "record_date": meta["date"],
                "pages_total": meta["pages_total"],
                "brain_head_at_sync": git("rev-parse", "HEAD"),
                "last_commit_touching_record": git(
                    "log", "-1", "--format=%H %ad", "--date=short",
                    "--", ".claude/skills/drinks-pricelist/drinks_final_figures.json",
                ),
                "synced": date.today().isoformat(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"figures: refreshed from the record {vendored_hash[:12]} -> {source_hash[:12]}")


if __name__ == "__main__":
    main()
