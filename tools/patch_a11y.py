#!/usr/bin/env python3
"""Fix what an accessibility audit of the built page actually found.

axe-core 4.10.2 (WCAG 2.0/2.1 A + AA) against the rendered Hebrew page reported
two violations and 24 passes. Both are handled here, together with the keyboard
gap axe cannot see.

  select-name (critical, 2 nodes)
      The enquiry form's two dropdowns have no accessible name. A screen reader
      announces them as an unlabelled combo box, so the one form on the site
      that has a job is the least usable part of it.

  color-contrast (serious, 3 nodes)
      The two footer lines sit at 3.12:1 and need 4.5:1. The third is the
      420px `TEA 2.0` watermark at 1.13:1 — decoration, not text anyone is
      meant to read, so it is hidden from assistive technology rather than
      recoloured, which is what it is for.

  Keyboard reach (not an axe finding)
      Ten collection cards are `<div onclick>`. A mouse opens them; a keyboard
      cannot reach them and a screen reader is not told they do anything, so ten
      of the site's main entry points are mouse-only. They become real buttons
      in the accessibility tree, focusable in document order, and a single
      delegated listener activates them on Enter or Space — one listener rather
      than ten more inline handlers.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"

applied: list[str] = []


def die(msg: str) -> None:
    sys.exit(f"FAIL [patch_a11y]: {msg}")


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        die(f"{label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new, count)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ── select-name ─────────────────────────────────────────────────────
    # The visible first <option> is the label a sighted user reads, so it is
    # the right accessible name too.
    text = sub("select pf-role", '<select id="pf-role">',
               '<select id="pf-role" aria-label="תפקיד">', text)
    text = sub("select pf-int", '<select id="pf-int">',
               '<select id="pf-int" aria-label="מה מעניין אתכם">', text)

    # ── colour contrast: the footer ─────────────────────────────────────
    # #8A8F82 on the paper #FBF8F2 is 3.12:1. #6B7065 is 4.54:1 — the smallest
    # darkening that clears AA while keeping the footer quiet.
    text = sub("footer contrast", "footer.site{padding:40px 0;font-size:14px;color:#8A8F82;",
               "footer.site{padding:40px 0;font-size:14px;color:#6B7065;", text)

    # ── colour contrast: the rest of the page (UX gate, 2026-09-27) ────
    # axe after one scroll through the served page: 46 nodes under 4.5:1. Each
    # colour is darkened by the smallest step that clears AA against its worst
    # background, as the footer was, so the page keeps its look:
    #   #9A9F93 (card origins, the catalogue note) on the darkest card #F6D9CF
    #     was 2.03:1; #60635C is 4.58:1.
    #   #8a8577 (the form's grey lines, the product window's labels) on the
    #     paper was 3.47:1; #6b6659, the consent's colour, is 5.4:1.
    #   the terra eyebrows on the card #F3EFE6 were 3.07:1; #9C5C3C is 4.56:1.
    #     Only their text: the rule beside them keeps the terra.
    #   the dimmed second size (opacity .55 on the cards) was 3.34:1; .7 clears it.
    #   the tools' English names #77796d on white were 4.43:1; #75776B is 4.56:1.
    n = text.count("color:#9A9F93")
    if n < 1:
        die("no color:#9A9F93 left to darken")
    text = text.replace("color:#9A9F93", "color:#60635C")
    applied.append(f"contrast #9A9F93 x{n}")
    n = text.count("color:#8a8577")
    if n < 1:
        die("no color:#8a8577 left to darken")
    text = text.replace("color:#8a8577", "color:#6b6659")
    applied.append(f"contrast #8a8577 x{n}")
    text = sub("contrast: eyebrow",
               "text-transform:uppercase;color:var(--terra);font-weight:800}",
               "text-transform:uppercase;color:#9C5C3C;font-weight:800}", text)
    text = sub("contrast: the dimmed size", ".fcard .prow span:last-child{opacity:.55}",
               ".fcard .prow span:last-child{opacity:.7}", text)
    text = sub("contrast: tool names", ".tool-card .ti span{font-size:12.5px;color:#77796d}",
               ".tool-card .ti span{font-size:12.5px;color:#75776B}", text)

    # ── the modals have names (UX gate, 2026-09-27) ─────────────────────
    # The product window had no role and no name, and four of the modals'
    # buttons were a bare glyph to a screen reader. The product window's title
    # takes focus when it opens (patch_lead_dialog.py), so it is focusable.
    text = sub("product window: a named modal dialog", '<div class="fmodal" id="fmodal" onclick=',
               '<div class="fmodal" id="fmodal" role="dialog" aria-modal="true" aria-labelledby="fm-name" onclick=', text)
    text = sub("product window: its title takes focus", '<h3 id="fm-name"></h3>',
               '<h3 id="fm-name" tabindex="-1"></h3>', text)
    text = sub("product window: close", '<button class="x" onclick=',
               '<button class="x" aria-label="סגירה" onclick=', text)
    text = sub("recipe card: close", '<button class="cm-x" onclick=',
               '<button class="cm-x" aria-label="סגירה" onclick=', text)
    text = sub("recipe card: named", '<div id="cmodal" role="dialog" aria-modal="true">',
               '<div id="cmodal" role="dialog" aria-modal="true" aria-labelledby="cm-en cm-he">', text)
    text = sub("gallery: named", '<div id="pmodal" role="dialog" aria-modal="true">',
               '<div id="pmodal" role="dialog" aria-modal="true" aria-labelledby="pm-title">', text)
    text = sub("gallery: close", '<button class="pm-x" onclick=',
               '<button class="pm-x" aria-label="סגירה" onclick=', text)
    text = sub("gallery: previous", '<button class="pm-nav prev" onclick=',
               '<button class="pm-nav prev" aria-label="הקודם" onclick=', text)
    text = sub("gallery: next", '<button class="pm-nav next" onclick=',
               '<button class="pm-nav next" aria-label="הבא" onclick=', text)

    # ── the watermarks are decoration ───────────────────────────────────
    n = text.count('<div class="ghost">')
    if n != 2:
        die(f"expected 2 ghost watermarks, found {n}")
    text = text.replace('<div class="ghost">', '<div class="ghost" aria-hidden="true">', 2)
    applied.append("ghost aria-hidden")

    # ── keyboard reach for the collection cards ─────────────────────────
    cards = re.findall(r'<div class="ccard rv" data-ci="(\d+)" onclick="cmOpen\(\d+\)"', text)
    if len(cards) != 10:
        die(f"expected 10 collection cards, found {len(cards)}")
    text = re.sub(
        r'<div class="ccard rv" (data-ci="\d+" onclick="cmOpen\(\d+\)")',
        r'<div class="ccard rv" role="button" tabindex="0" \1',
        text,
    )
    applied.append("cards focusable")

    # One delegated listener, so a card added later is reachable without
    # remembering to wire it. Space is swallowed on keydown to stop the page
    # scrolling underneath the modal that is about to open.
    hook = (
        "\ndocument.addEventListener('keydown',function(e){"
        "var t=e.target;"
        "if(!t||!t.matches||!t.matches('[role=\"button\"][onclick]'))return;"
        "if(e.key!=='Enter'&&e.key!==' ')return;"
        "e.preventDefault();t.click();});\n"
    )
    marker = "function navToggle(b){"
    if text.count(marker) != 1:
        die("could not find navToggle to anchor the keyboard listener")
    text = text.replace(marker, hook + marker, 1)
    applied.append("keyboard activation")

    SRC.write_text(text, encoding="utf-8")
    print(f"a11y: {len(applied)} fixes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
