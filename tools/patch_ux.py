#!/usr/bin/env python3
"""Fix what the pre-launch UX review found, on the built page.

The page was walked as a café owner would walk it — on a phone first, then on a
desktop — with the enquiry form as its one job. Everything below is a defect
with a cost in enquiries; the findings that were taste rather than defect are
listed in docs/2026-09-03_ux-review.md and deliberately left alone.

  The sticky call-to-action wraps
      Under 640px the nav's "רוצים להתחיל" pill shrinks as a flex item and
      breaks onto two lines. It is the one control that reaches the form from
      every screen, and it looked broken on every screen.

  The phone number is not a phone number
      The contact list shows 054-398-2444 as plain text — on a phone there is
      nothing to tap. Same for the e-mail address and the Instagram handle.

  Numbers break across lines in RTL
      Inside a Hebrew sentence "054-398-2444" wraps at a hyphen and comes back
      as "-054 / 398-2444": in the error message and in the thank-you, the two
      lines a visitor reads most carefully.

  The phone field opens a text keyboard and nothing autofills
      No field carried type, inputmode or autocomplete — or a name, so the
      no-JS mailto fallback posted an empty body.

  Tap targets under 44px
      "רוצה מחירון" in the hero (28px), the FAQ questions (26px), the price
      list toggle (35px), the consent checkbox (16px), the WhatsApp and phone
      links under the form (15px).

  No visible focus on the buttons
      `.btn` transitions `all`, which swallows the browser's focus ring, so a
      keyboard user cannot see where they are.

  Motion ignores prefers-reduced-motion
      The hero advanced every 5s and the price ticker never stopped, whatever
      the visitor's setting. The partner logos already honoured it.

  One label still in English
      "Made with" in the recipe modal, at 2.6:1 contrast — the only
      untranslated word on the page.

Every edit asserts its anchor exists, so a silent no-op is impossible.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"

applied: list[str] = []


def die(msg: str) -> None:
    sys.exit(f"FAIL [patch_ux]: {msg}")


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        die(f"{label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new, count)


def sub_re(label: str, pattern: str, repl: str, text: str, count: int = 1) -> str:
    out, n = re.subn(pattern, repl, text)
    if n != count:
        die(f"{label}: expected {count} match(es), found {n}")
    applied.append(label)
    return out


CSS = """
/* ====================================================================
   Pre-launch UX review (tools/patch_ux.py). Appended last so it wins.
   ==================================================================== */

/* the sticky call-to-action never wraps */
nav .btn{white-space:nowrap;flex:0 0 auto}
@media(max-width:640px){nav .btn{padding:12px 18px;font-size:13px;gap:8px}}
@media(max-width:360px){nav .btn{padding:11px 14px;font-size:12px}}

/* a phone number is one word, whatever direction the sentence runs */
a[href^="tel:"],a[href^="https://wa.me"]{white-space:nowrap;unicode-bidi:isolate}

/* contact rows are tappable end to end and keep their look */
.contact li a{display:block;margin:-12px 0;padding:12px 0;color:inherit;text-decoration:none}
.contact li a:hover{color:var(--gt)}

/* tap targets: 44px, or as close as the design allows */
.sub-cta{display:inline-block;padding:10px 0 6px}
.pall{padding:12px 20px;font-size:13px}
#faq details{padding:0 22px}
#faq summary{padding:18px 0 18px 28px}
#faq summary::after{top:16px}
#faq details p{padding-bottom:18px}
.partner .pf-ok input{width:20px;height:20px;margin-top:0}
.partner .pf-alt a{display:inline-block;padding:10px 0}
.partner .pf-err a,.partner .pf-done a{display:inline-block;padding:6px 2px}

/* keyboard focus is visible on everything that acts */
.btn{transition:background-color .2s,color .2s,box-shadow .2s}
.btn:focus-visible,.sub-cta:focus-visible,.ccard:focus-visible,.mxtog:focus-visible,
.pall:focus-visible,.hs-arr:focus-visible,.nav-burger:focus-visible,
.nav-links a:focus-visible,#faq summary:focus-visible{outline:3px solid var(--gt);outline-offset:3px}
input:focus-visible,select:focus-visible,.partner textarea:focus-visible{outline:2px solid var(--gt);outline-offset:0}

/* the recipe modal: a readable source label, and "1 / 6" that reads 1 / 6 */
.cm-src .lbl{color:#6B7065;letter-spacing:.06em}
.cm-num{direction:ltr;unicode-bidi:isolate}

/* motion respects the visitor's setting (the hero is handled in script) */
@media(prefers-reduced-motion:reduce){.ticker .track{animation:none}}
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ── the contact list becomes tappable ───────────────────────────────
    # The text node inside each <li> is left byte-for-byte as it is, so the
    # string catalogue neither grows nor shifts.
    text = sub_re("tel link", r"<li>([^<]*054-398-2444)</li>",
                  r'<li><a href="tel:+972543982444">\1</a></li>', text)
    text = sub_re("mail link", r"<li>([^<]*info@gteveryday\.com)</li>",
                  r'<li><a href="mailto:info@gteveryday.com">\1</a></li>', text)
    text = sub_re("instagram link", r"<li>([^<]*@gteveryday)</li>",
                  r'<li><a href="https://www.instagram.com/gteveryday/" target="_blank" '
                  r'rel="noopener">\1</a></li>', text)

    # ── form fields: the right keyboard, autofill, a name for the fallback ─
    for old, new in (
        ('<input id="pf-name" ',
         '<input id="pf-name" name="name" autocomplete="name" '),
        ('<input id="pf-venue" ',
         '<input id="pf-venue" name="venue" autocomplete="organization" '),
        ('<input id="pf-city" ',
         '<input id="pf-city" name="city" autocomplete="address-level2" '),
        ('<select id="pf-role" ',
         '<select id="pf-role" name="role" '),
        ('<input id="pf-phone" ',
         '<input id="pf-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" '),
        ('<input id="pf-mail" type="email" ',
         '<input id="pf-mail" name="email" type="email" inputmode="email" autocomplete="email" '),
        ('<select id="pf-int" ',
         '<select id="pf-int" name="interest" '),
        ('<textarea id="pf-msg" ',
         '<textarea id="pf-msg" name="message" '),
    ):
        text = sub("field " + old.split('"')[1], old, new, text)

    # ── the thank-you is a status, so assistive technology reads it ─────
    text = sub("done role", '<div class="pf-done" id="pf-done">',
               '<div class="pf-done" id="pf-done" role="status">', text)

    # ── the hero stays put when the visitor asked for less motion ───────
    text = sub(
        "hero reduced motion",
        "function hsRestart(){clearInterval(hsTimer);"
        "hsTimer=setInterval(()=>hsGo(hsI+1),5000);}",
        "function hsRestart(){clearInterval(hsTimer);"
        "if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;"
        "hsTimer=setInterval(()=>hsGo(hsI+1),5000);}",
        text,
    )

    # ── the one English label left in the recipe modal ──────────────────
    # "Made with → Matcha" sits in a JS markup literal, which the string
    # extractor skips on purpose, so it never reached the catalogue.
    text = sub("modal source label", '<span class="lbl">Made with</span>',
               '<span class="lbl">על בסיס</span>', text)
    # Its chip pointed → at the product; the reader now reads towards ←.
    text = sub("modal chip arrow", "'\">'+n+' \\u2192</a>'", "'\">'+n+' \\u2190</a>'", text)

    text = sub("ux stylesheet", "</style>", CSS + "</style>", text)

    SRC.write_text(text, encoding="utf-8")
    print(f"ux: {len(applied)} fixes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
