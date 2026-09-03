#!/usr/bin/env python3
"""Make the partner-enquiry form actually send the enquiry.

The delivered design builds a `mailto:` and then adds the form's "sent" class
unconditionally. On a phone with no mail client configured — which is most
phones — the visitor reads "תודה — הבקשה בדרך אלינו" and nothing has left the
device. There is no record of how many enquiries that lost, because losing them
silently is precisely what it does.

This is not a Hebrew concern and not an RTL one, so it lives in its own step
rather than being smuggled into either. It runs last, over the built page, and
replaces the handler with one that POSTs to the `website_lead_intake` Edge
Function — the public front of the sales system. That function validates the
enquiry, holds the ingest token the browser must never see, and hands the lead
to `sales-leads-poll /ingest`, which stores it and alerts the desk.

Three states instead of one:

    sending   the button is disabled and says so
    stored    the thank-you, shown ONLY when the server confirms the lead
    failed    says so, and points at WhatsApp, which works

and a 15s timeout, so a request that never returns is a failure rather than a
button that spins for ever.

Two fields carry defences the function enforces and cannot enforce alone: a
honeypot input that is off-screen, unfocusable and never autofilled, and the
time since page load — a person cannot fill nine fields in three seconds.

The endpoint is public by design and holds no secret of ours. Anyone can read
it out of this page; that is why every check lives on the server side.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "index.html"
text = SRC.read_text(encoding="utf-8")
applied = []

ENDPOINT = "https://rvadsozabmxkkrktwgnv.supabase.co/functions/v1/website_lead_intake"


def sub(label, old, new, count=1):
    global text
    n = text.count(old)
    if n != count:
        sys.exit(f"FAIL [{label}]: expected {count}, found {n}")
    text = text.replace(old, new, count)
    applied.append(f"{label} ×{count}")


# ── states the form did not have: busy, failed, and a hidden honeypot ───
sub(
    "form state css",
    ".partner.sent .pf-done{display:block}",
    ".partner.sent .pf-done{display:block}\n"
    ".partner.sent .pf-row,.partner.sent textarea,.partner.sent select,"
    ".partner.sent .pf-ok,.partner.sent button{display:none}\n"
    ".partner .pf-err{display:none;background:#FAEDEA;border:1px solid #EBCEC6;"
    "border-radius:14px;padding:14px 16px;font-size:13.5px;line-height:1.5;color:#7A3B2C}\n"
    ".partner .pf-err b{display:block;margin-bottom:3px}\n"
    ".partner.failed .pf-err{display:block}\n"
    ".partner button[disabled]{opacity:.55;cursor:default}\n"
    "/* Never shown to a person, never focusable, never autofilled. A bot fills\n"
    "   every input it finds, and that is the whole point of this one. */\n"
    ".partner .pf-hp{position:absolute;width:1px;height:1px;padding:0;margin:-1px;"
    "overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}",
)

sub(
    "honeypot field",
    '<label class="pf-ok"><input type="checkbox" id="pf-agree" required>'
    " אני מאשר/ת פנייה בנוגע לאספקה סיטונאית.</label>",
    '<label class="pf-ok"><input type="checkbox" id="pf-agree" required>'
    " אני מאשר/ת פנייה בנוגע לאספקה סיטונאית.</label>\n"
    '    <div class="pf-hp" aria-hidden="true"><label for="pf-web">אתר</label>'
    '<input id="pf-web" name="company_website" type="text" tabindex="-1"'
    ' autocomplete="off"></div>',
)

# The old thank-you described a mail client opening. Nothing opens one now, and
# the promise is the one the form's own header makes.
sub(
    "honest success + a failure state",
    '<div class="pf-done" id="pf-done"><b>תודה — הבקשה בדרך אלינו.</b>'
    "<span>אפליקציית המייל שלכם נפתחה עם המכתב המוכן. "
    "אם לא — כתבו ל־info@gteveryday.com</span></div>",
    '<div class="pf-done" id="pf-done"><b>תודה — הפנייה נקלטה.</b>'
    "<span>נחזור אליכם תוך יום עסקים אחד, לרוב מוקדם יותר.</span></div>\n"
    '    <div class="pf-err" id="pf-err"><b>הפנייה לא נשלחה.</b>'
    "<span>משהו אצלנו לא הגיב. נסו שוב, או פנו ישירות ב"
    '<a href="https://wa.me/972543982444" target="_blank" rel="noopener">וואטסאפ</a>'
    ' או בטלפון <a href="tel:+972543982444">054-398-2444</a>.</span></div>',
)

# ── the handler ─────────────────────────────────────────────────────────
OLD_HANDLER = """function pSend(e){e.preventDefault();
 var g=function(id){var el=document.getElementById(id);return el?el.value.trim():'';};
 var f=document.getElementById('pform');
 if(!document.getElementById('pf-agree').checked)return false;
 var L=['שם העסק:'+g('pf-venue'),'שם:'+g('pf-name'),'תפקיד:'+(g('pf-role')||'—'),
        'עיר:'+g('pf-city'),'טלפון:'+g('pf-phone'),'אימייל:'+(g('pf-mail')||'—'),
        'מתעניין ב:'+(g('pf-int')||'—'),'','הודעה:',g('pf-msg')||'—'];
 var subj='GT Everyday — בקשת שיתוף פעולה —'+(g('pf-venue')||g('pf-name'));
 window.location.href='mailto:info@gteveryday.com?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(L.join('\\n'));
 f.classList.add('sent');
 return false;}"""

NEW_HANDLER = """/* The enquiry form.
 *
 * This used to open a `mailto:` and then add the "sent" class unconditionally.
 * On a phone with no mail client configured — which is most phones — the
 * visitor read "תודה — הבקשה בדרך אלינו" and nothing had left the device.
 *
 * So the success message is now shown ONLY when the server says it stored the
 * lead. A failure says so, and points at WhatsApp, which works.
 *
 * The endpoint is the `website_lead_intake` Edge Function. It is public on
 * purpose: a browser cannot be trusted with the ingest token, so the token
 * lives there and this page holds nothing secret. That function validates,
 * limits one lead per phone per day, and hands the enquiry to sales-leads-poll
 * /ingest, which alerts the desk.
 *
 * Generated by tools/patch_form_intake.py — edit that, not this.
 */
var PF_ENDPOINT='%ENDPOINT%';
var PF_LOADED=Date.now();

function pSend(e){e.preventDefault();
 var g=function(id){var el=document.getElementById(id);return el?el.value.trim():'';};
 var f=document.getElementById('pform');
 var btn=f.querySelector('button');
 if(!document.getElementById('pf-agree').checked)return false;
 if(f.classList.contains('sending')||f.classList.contains('sent'))return false;

 f.classList.remove('failed');
 f.classList.add('sending');
 var label=btn?btn.innerHTML:'';
 if(btn){btn.disabled=true;btn.textContent='שולח…';}

 var settled=false;
 var give=function(ok){
  if(settled)return; settled=true;
  f.classList.remove('sending');
  if(ok){f.classList.add('sent');return;}
  f.classList.add('failed');
  if(btn){btn.disabled=false;btn.innerHTML=label;}
 };
 /* A request that never comes back must not leave the button spinning for
    ever — after 15s we say so, rather than let it look like it worked. */
 setTimeout(function(){give(false);},15000);

 fetch(PF_ENDPOINT,{method:'POST',headers:{'content-type':'application/json'},
  body:JSON.stringify({
   contact_name:g('pf-name'), venue:g('pf-venue'), city:g('pf-city'),
   role:g('pf-role'), phone:g('pf-phone'), email:g('pf-mail'),
   interest:g('pf-int'), message:g('pf-msg'),
   company_website:g('pf-web'),        /* honeypot — a person leaves it empty */
   elapsed_ms:Date.now()-PF_LOADED,    /* a person cannot fill nine fields in 3s */
   page:location.href, referrer:document.referrer})})
 .then(function(r){return r.json().then(
    function(j){return {ok:r.ok,body:j};},
    function(){return {ok:false,body:{}};});})
 .then(function(res){give(res.ok&&res.body&&res.body.ok===true);})
 .catch(function(){give(false);});

 return false;}""".replace("%ENDPOINT%", ENDPOINT)

sub("form posts to the sales system", OLD_HANDLER, NEW_HANDLER)

# The old handler was the page's only `mailto:` script. The contact list still
# shows the address as text, which is right — this asserts no code path can
# quietly go back to opening a mail client.
if "window.location.href='mailto:" in text:
    sys.exit("FAIL: a mailto: handler survives — the silent-loss path is back")

SRC.write_text(text, encoding="utf-8")
for line in applied:
    print(f"  ✓ {line}")
print("  ✓ no mailto: handler remains")
