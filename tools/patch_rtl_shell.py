#!/usr/bin/env python3
"""RTL layout, mobile navigation and document semantics for the Hebrew build.

`dir="rtl"` flips normal flow for free, but three things it does not fix:
  · transform-driven tracks (hero slider, ticker) whose maths assumes LTR,
  · absolutely positioned chrome (close buttons, arrows, markers),
  · styles this page injects inline from JS, which no stylesheet can override.
Each is handled below and nowhere else, so the original stylesheet stays intact.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "index.html"
text = SRC.read_text(encoding="utf-8")
applied = []


def sub(label, old, new, count=1):
    global text
    n = text.count(old)
    if n != count:
        sys.exit(f"FAIL [{label}]: expected {count}, found {n}")
    text = text.replace(old, new, count)
    applied.append(f"{label} ×{count}")


# ── CTA arrows point the way the reader reads ───────────────────────────
sub("cta arrows", 'class="arr">→</span>', 'class="arr">←</span>', 15)

# ── hero slides: one h1 for the document, h2 for the ten slides ─────────
sub("slide headings", "<h1>", "<h2 class=\"hs-h\">", 10)
sub("slide headings close", "</h1>", "</h2>", 10)
# the slide styling was bound to the tag, so move the selectors with it
sub("slide heading css", ".hs-copy h1", ".hs-copy .hs-h", 2)
sub(
    "document h1",
    '<div class="ticker">',
    '<h1 class="sr-only">GT Everyday — תרכיזי תה, מאצ׳ה ופירה פירות '
    'לבתי קפה, מסעדות ומלונות</h1>\n<div class="ticker">',
)

# ── hero art: mirror the photograph, not the slide ──────────────────────
# All ten hero photographs put the drinks right of centre (measured: 59–66% of
# the frame) with clear wall on the left — composed for the English build,
# where the copy sat on the left. Under RTL the copy moved right, on top of the
# glasses. Mirroring the whole slide would carry the copy along with it, so the
# image is handed to CSS as a custom property and flipped on ::before alone.
sub("slide bg to custom property",
    'el.style.backgroundImage="url(\'"+el.dataset.hsbg+"\')"',
    'el.style.setProperty("--hsbg","url(\'"+el.dataset.hsbg+"\')")')

# ── mobile navigation (there was none under 980px) ──────────────────────
sub(
    "burger button",
    '  <div class="nav-links">',
    '  <button class="nav-burger" aria-label="תפריט" aria-expanded="false"'
    ' aria-controls="nav-links" onclick="navToggle(this)">'
    '<i></i><i></i><i></i></button>\n'
    '  <div class="nav-links" id="nav-links">',
)

sub(
    "nav toggle script",
    "const io=new IntersectionObserver(",
    "function navToggle(b){var n=b.closest('nav');var open=n.classList.toggle('open');\n"
    " b.setAttribute('aria-expanded',open?'true':'false');\n"
    " document.body.style.overflow=open?'hidden':'';}\n"
    "document.addEventListener('click',function(e){var a=e.target.closest('.nav-links a');\n"
    " if(!a)return;var n=a.closest('nav');if(!n||!n.classList.contains('open'))return;\n"
    " n.classList.remove('open');document.body.style.overflow='';\n"
    " var b=n.querySelector('.nav-burger');if(b)b.setAttribute('aria-expanded','false');});\n"
    "document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;\n"
    " var n=document.querySelector('nav.open');if(!n)return;\n"
    " n.classList.remove('open');document.body.style.overflow='';\n"
    " var b=n.querySelector('.nav-burger');if(b)b.setAttribute('aria-expanded','false');});\n"
    "const io=new IntersectionObserver(",
)

RTL_CSS = """
/* ====================================================================
   Hebrew build — RTL corrections, mobile navigation.
   Appended last so it wins without touching the rules above.
   ==================================================================== */

/* chevrons: "previous" sits on the right in Hebrew, so it points right too.
   Swapped in CSS rather than in the markup, which keeps the English source
   file and the aria-labels untouched. */
.hs-arr.prev,.pm-nav.prev,.hs-arr.next,.pm-nav.next{font-size:0}
.hs-arr.prev:after,.pm-nav.prev:after{content:"\\203A"}
.hs-arr.next:after,.pm-nav.next:after{content:"\\2039"}
.hs-arr:after,.pm-nav:after{font-size:22px;line-height:1}

.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;
  overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}

/* --- hero photographs are mirrored so their negative space falls under the
       copy. ::before is free here: a later rule in the original stylesheet
       sets its gradient to `none`, and the dark panel behind the copy comes
       from .hs-copy instead. --- */
.hs-slide{background-image:none!important}
.hs-slide:before{
  content:'';position:absolute;inset:0;z-index:0;
  background-image:var(--hsbg,none);
  background-size:cover;background-position:center bottom;
  transform:scaleX(-1);
}
@media(max-width:760px){ .hs-slide:before{background-size:auto 185%} }
.hs-slide>.in{position:relative;z-index:1}

/* --- transform-driven tracks stay LTR; their content goes back to RTL ---
   Both animate with a negative translateX over a duplicated/flex row, which
   only lands correctly while the box itself lays out left-to-right. */
.hs-track{direction:ltr}
.hs-slide{direction:rtl}
.ticker{direction:ltr}
.ticker span{direction:rtl;display:inline-block}
.ticker span{margin-right:0;margin-left:56px}

/* --- chrome that must sit on the reader's near side --- */
.fmodal .x,.cm-x,.pm-x{right:auto;left:22px}
.pm-x{left:18px}
.cm-num{right:auto;left:74px}
#faq summary::after{right:auto;left:2px}
.dd-menu{left:auto;right:-16px}
.fcard.v3 .badge{left:auto;right:14px}
.qcard .mark{left:auto;right:32px}
.bottle:after{left:auto;right:12px}
.nav-links a:after{left:auto;right:0}

/* previous/next swap sides: in Hebrew, "back" is to the right */
.hs-arr.prev{left:auto;right:10px}
.hs-arr.next{right:auto;left:10px}
.pm-nav.prev{left:auto;right:12px}
.pm-nav.next{right:auto;left:12px}
@media(max-width:900px){
  .hs-arr.prev{left:auto;right:14px}
  .hs-arr.next{left:auto;right:66px}
}

/* --- hover nudges follow the reading direction --- */
.btn:hover .arr{transform:translateX(-4px)}
.pm-list a:hover{transform:translateX(-4px)}
.fmodal a.mkgo i u{transform:translateX(4px)}

/* --- the hero's "copy-left" slide keeps its inset on the physical left,
       so under RTL the panel is pushed past the right edge and the first
       word of each line is clipped. Mirror the padding. --- */
.hs-slide.copy-left .in{padding-left:0;padding-right:clamp(68px,5vw,86px)}
@media(max-width:900px){ .hs-slide.copy-left .in{padding-left:0;padding-right:24px} }

/* --- text that was pinned to the physical left --- */
.hs-copy .heh,.hs-slide.copy-topcenter .hs-copy,
.bandcap.side,.bandcap.bottom,.bandcap.top,.mxtog{text-align:right}
.bandcap.side{padding:0 clamp(28px,5vw,86px) 0 0}

/* --- styles this page writes inline from JS need the extra weight --- */
.cyc-tag{right:auto!important;left:14px!important}
.cyc-dots{right:auto!important;left:16px!important}

/* --- mobile navigation (previously: the menu simply vanished) --- */
.nav-burger{display:none;flex-direction:column;justify-content:center;gap:5px;
  flex:0 0 44px;width:44px;height:44px;padding:0 10px;background:none;border:0;cursor:pointer}
.nav-burger i{display:block;height:2px;background:var(--ink);border-radius:2px;
  transition:transform .25s ease,opacity .2s ease}
nav.open .nav-burger i:nth-child(1){transform:translateY(7px) rotate(45deg)}
nav.open .nav-burger i:nth-child(2){opacity:0}
nav.open .nav-burger i:nth-child(3){transform:translateY(-7px) rotate(-45deg)}

@media(max-width:980px){
  .nav-burger{display:flex}
  /* nav carries backdrop-filter, which makes it the containing block for its
     position:fixed descendants — the panel would inherit the bar's height.
     It is opaque while the menu is open, so the blur is not needed then. */
  nav.open{backdrop-filter:none;-webkit-backdrop-filter:none;background:var(--paper)}
  .nav-links{display:block;position:fixed;inset:108px 0 0;z-index:90;
    background:var(--paper);border-top:1px solid var(--line);
    padding:22px 28px 40px;overflow-y:auto;
    transform:translateY(-8px);opacity:0;visibility:hidden;
    transition:opacity .22s ease,transform .22s ease,visibility .22s}
  nav.open .nav-links{opacity:1;visibility:visible;transform:none}
  .nav-links>*{display:block;font-size:20px;padding:14px 0;
    border-bottom:1px solid var(--line)}
  .nav-links .nav-dd{border-bottom:1px solid var(--line)}
  .nav-links .nav-dd>a .car{display:none}
  /* the flavour dropdown becomes an inline list instead of a hover panel */
  .nav-links .dd-menu{position:static;opacity:1;visibility:visible;
    transform:none;padding:0;box-shadow:none;background:none}
  .nav-links .dd-in{display:grid;grid-template-columns:1fr 1fr;gap:2px 18px;
    padding:6px 0 12px;background:none;box-shadow:none;border:0}
  .nav-links .dd-head{grid-column:1/-1;font-size:12px;letter-spacing:.2em;
    text-transform:uppercase;color:var(--terra);padding-top:10px}
  .nav-links .dd-in a{font-size:16px;padding:7px 0;border:0}
}
@media(max-width:640px){
  .nav-links{inset:80px 0 0}
}
"""

sub("rtl stylesheet", "</style>", RTL_CSS + "</style>", 1)

SRC.write_text(text, encoding="utf-8")
print(f"{len(applied)} patches applied:")
for a in applied:
    print("  ✓", a)
