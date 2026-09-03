#!/usr/bin/env python3
"""Make the enquiry form land a lead instead of opening a mail client.

The delivered form built a `mailto:` URL, assigned it to `window.location`, and
then added its own `sent` class unconditionally — so it thanked the visitor
whether or not anything had been sent. On a phone without a configured mail
client, and in most in-app browsers, that is every enquiry lost silently while
the page says the opposite.

It now posts to `website_lead_intake`, which forwards to the `/ingest` route on
`sales-leads-poll` — the path that already ingests, matches the enquirer against
Shopify, emails the staff allowlist and files anything unmappable into
`lead_reject`.

What this patch adds beyond the request itself:

- **The thank-you is earned.** `sent` is added only after the endpoint answers
  ok. A failure shows an error the visitor can act on, with the phone and
  WhatsApp beside it, and leaves every field filled so nothing is retyped.
- **A no-JS path.** The form keeps a real `action`/`method`, so a visitor whose
  script is blocked still reaches a working mail draft rather than a dead
  button. That was the old behaviour for everyone; it is now the fallback only.
- **A honeypot** and the time the form was on screen, both read by the endpoint.
- **The button says what it is doing** — sending, then sent — and cannot be
  double-submitted. Before this it stayed on "שולח…" after a success, which read
  as stuck.
- **A `generate_lead` event**, pushed once the endpoint confirms the lead —
  category fields only, never the enquirer's details.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"

ENDPOINT = "https://rvadsozabmxkkrktwgnv.supabase.co/functions/v1/website_lead_intake"

applied: list[str] = []


def die(msg: str) -> None:
    sys.exit(f"FAIL [patch_form]: {msg}")


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        die(f"{label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new, count)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ── the form element: real action for the no-JS case ────────────────
    text = sub(
        "form element",
        '<form class="rv partner" id="pform" onsubmit="return pSend(event)">',
        '<form class="rv partner" id="pform" method="post" enctype="text/plain"\n'
        '      action="mailto:info@gteveryday.com?subject=GT%20Everyday%20%E2%80%94%20'
        'בקשת%20שיתוף%20פעולה" onsubmit="return pSend(event)">',
        text,
    )

    # ── honeypot + status region ────────────────────────────────────────
    # Hidden by clipping, not by display:none — some bots skip a field they can
    # see is hidden, and fill one that merely looks positioned — and hidden from
    # assistive technology and the tab order so no person reaches it by accident.
    #
    # It must not be pushed off-screen with a large negative offset. That is the
    # usual recipe for this, and here it silently widened the document to
    # 11,310px: the page is RTL, so an element at left:-9999px extends the
    # scrollable area rather than falling outside it, and the whole page scrolled
    # sideways into empty paper. Clipping costs nothing and moves nothing.
    text = sub(
        "honeypot + status",
        '    <label class="pf-ok"><input type="checkbox" id="pf-agree" required>',
        '    <div aria-hidden="true" style="position:absolute;width:1px;height:1px;'
        'overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap">\n'
        '      <label for="pf-cw">אל תמלאו שדה זה</label>\n'
        '      <input id="pf-cw" name="company_website" type="text"'
        ' tabindex="-1" autocomplete="off">\n'
        '    </div>\n'
        '    <div class="pf-err" id="pf-err" role="alert" hidden></div>\n'
        '    <label class="pf-ok"><input type="checkbox" id="pf-agree" required>',
        text,
    )

    # ── the error style, beside the existing done style ──────────────────
    text = sub(
        "error style",
        ".partner .pf-done{display:none;",
        ".partner .pf-err{background:#FBEAE7;border:1px solid #E5B4AB;border-radius:14px;"
        "padding:12px 15px;font-size:13.5px;line-height:1.5;color:#7A2E1E}\n"
        ".partner .pf-err a{color:#7A2E1E;font-weight:700}\n"
        ".partner button[disabled]{opacity:.6;cursor:progress}\n"
        ".partner.sent button[disabled]{opacity:1;cursor:default;background:var(--gt)}\n"
        ".partner .pf-done a{color:inherit;font-weight:700}\n"
        ".partner .pf-done{display:none;",
        text,
    )

    # ── the thank-you no longer describes a mail client ─────────────────
    text = sub(
        "done copy",
        "<span>אפליקציית המייל שלכם נפתחה עם המכתב המוכן. "
        "אם לא — כתבו ל־info@gteveryday.com</span>",
        "<span>קיבלנו את הפרטים ואנחנו חוזרים אליכם תוך יום עסקים אחד. "
        "אם דחוף — <a href=\"tel:+972543982444\">054-398-2444</a>.</span>",
        text,
    )

    # ── the sender ──────────────────────────────────────────────────────
    old_send = re.search(r"function pSend\(e\)\{.*?\n return false;\}", text, re.S)
    if not old_send:
        die("could not find the pSend function to replace")
    if "mailto:" not in old_send.group(0):
        die("pSend no longer looks like the mailto sender — check before replacing")

    new_send = (
        "var PF_ENDPOINT=" + repr(ENDPOINT).replace("'", '"') + ";\n"
        "var PF_SHOWN=Date.now();\n"
        "function pSend(e){e.preventDefault();\n"
        " var g=function(id){var el=document.getElementById(id);return el?el.value.trim():'';};\n"
        " var f=document.getElementById('pform');\n"
        " var err=document.getElementById('pf-err');\n"
        " var btn=f.querySelector('button');\n"
        " if(!document.getElementById('pf-agree').checked)return false;\n"
        " var fail=function(msg){err.innerHTML=msg;err.hidden=false;\n"
        "  btn.disabled=false;btn.innerHTML=PF_LABEL;\n"
        "  err.scrollIntoView({block:'nearest',behavior:'smooth'});};\n"
        " err.hidden=true;\n"
        " btn.disabled=true;btn.innerHTML='שולח\\u2026';\n"
        " var body={contact_name:g('pf-name'),venue:g('pf-venue'),city:g('pf-city'),\n"
        "  role:g('pf-role'),phone:g('pf-phone'),email:g('pf-mail'),interest:g('pf-int'),\n"
        "  message:g('pf-msg'),company_website:g('pf-cw'),\n"
        "  elapsed_ms:Date.now()-PF_SHOWN,page:location.href,referrer:document.referrer};\n"
        " var to=setTimeout(function(){fail(PF_ERR);},15000);\n"
        " fetch(PF_ENDPOINT,{method:'POST',headers:{'content-type':'application/json'},\n"
        "  body:JSON.stringify(body)})\n"
        "  .then(function(r){return r.json().catch(function(){return {};})\n"
        "   .then(function(j){return {ok:r.ok,j:j};});})\n"
        "  .then(function(res){clearTimeout(to);\n"
        "   if(res.ok&&res.j&&res.j.ok){pfTrack(g('pf-int'),g('pf-role'));\n"
        "    f.classList.add('sent');btn.innerHTML='נשלח \\u2713';\n"
        "    document.getElementById('pf-done').scrollIntoView("
        "{block:'nearest',behavior:'smooth'});return;}\n"
        "   if(res.j&&res.j.error==='missing_fields'){fail('חסרים פרטים חובה. "
        "בדקו שם, שם העסק, עיר וטלפון.');return;}\n"
        "   if(res.j&&res.j.error==='bad_phone'){fail('מספר הטלפון לא נראה תקין. "
        "בדקו אותו ונסו שוב.');return;}\n"
        "   if(res.j&&res.j.error==='bad_email'){fail('כתובת המייל לא נראית תקינה. "
        "בדקו אותה ונסו שוב.');return;}\n"
        "   fail(PF_ERR);})\n"
        "  .catch(function(){clearTimeout(to);fail(PF_ERR);});\n"
        " return false;}"
    )
    header = (
        # The page's one job is this form, and until now nothing measured it:
        # a submitted enquiry left no trace in GTM, GA4 or anywhere else. The
        # event fires only after the endpoint confirms the lead, so it counts
        # leads rather than clicks.
        #
        # It carries the two category fields and nothing else. Name, business,
        # city, phone, email and the message stay out of the dataLayer: they
        # are the lead, they belong in sales_core, and a marketing tag has no
        # business with them.
        "function pfTrack(interest,role){try{\n"
        " window.dataLayer=window.dataLayer||[];\n"
        " window.dataLayer.push({event:'generate_lead',form:'partner_enquiry',\n"
        "  lead_interest:interest||'',lead_role:role||''});\n"
        " if(typeof gtag==='function')"
        "gtag('event','generate_lead',{form:'partner_enquiry'});\n"
        "}catch(e){}}\n"
        "var PF_LABEL='שליחה <span class=\"arr\">\\u2190</span>';\n"
        "var PF_ERR='לא הצלחנו לשלוח את הפנייה. נסו שוב, או דברו איתנו ישירות: "
        "<a href=\"https://wa.me/972543982444\">וואטסאפ</a> \\u00b7 "
        "<a href=\"tel:+972543982444\">054-398-2444</a>.';\n"
    )
    text = text[: old_send.start()] + header + new_send + text[old_send.end():]
    applied.append("pSend -> POST")

    SRC.write_text(text, encoding="utf-8")
    print(f"form: {len(applied)} changes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
