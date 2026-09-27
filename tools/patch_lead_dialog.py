#!/usr/bin/env python3
"""Every lead call-to-action opens the enquiry form in a dialog, instead of throwing the page
to its bottom (Tom, 2026-09-27).

Nineteen links on the served page point at #contact: the nav, the hero, the ten hero slides,
the catalogue, the economics card, the closing call-to-action, the add-to-menu link in the
product window, and three flavour cards (retargeted by strip_prices.py, which open the product
window first). A click used to scroll the visitor to the form at the bottom of the page. Now:

  One form, borrowed.
      The dialog holds no form of its own. On open, #pform moves into it, and on close it goes
      back into #pf-slot, which keeps the form's height meanwhile so the page below does not
      shrink and move. So there is one form, one sender (pSend) and one sent state. Without
      this script, or without <dialog> support, the links still scroll to #contact.

  The page stays where it was.
      A native modal dialog is in the top layer and makes the rest of the page inert. The page
      is locked with html.cm-lock, the class the recipe card uses; body is never position:fixed,
      which jumps the page on iOS. Opening pushes a history entry, so the phone's back button
      closes the dialog instead of leaving the site. Closing steps back over that entry and
      returns focus to what opened the dialog, without scrolling.

  Businesses only, then the details, then a line (Tom, 2026-09-27).
      GT sells wholesale. The form first asks whether the visitor has a business. A private buyer
      is sent to the shop that sells GT to the public, Elita Ofek, and nothing is sent to sales.
      A business fills in the four details. After a send the form asks which line interests them
      most, and each line is a link to the lead number's WhatsApp with a message already written.
      The answer to the first question stays for the visit, so a second link opens the form.

  The thank-you is earned, and the dialog leaves when the visitor has picked.
      A send is held until 3 s after navigation start, because the intake answers ok and stores
      nothing when elapsed_ms is under 3000. Success is res.ok, body.ok and a was_new key: the
      intake's two silent drops (honeypot, too fast) answer {ok:true} without was_new. After a
      success the dialog shows a check, the thanks and the lines. Picking one opens WhatsApp, and
      the dialog closes when the visitor comes back to the page. It does not close on a timer:
      two seconds cut the thanks off for a screen reader (UX gate, 2026-09-27).

  The dialog wears the drink it was opened from.
      A hero slide lends its photo and colour, the product window its product, and every other
      link the hero's bottles: the colour on the phone sheet's rim, the photo beside the form
      from 880px. On a mouse-and-keyboard screen the first field is focused on open.

  Intent travels with the lead.
      data-price links (the slides, the catalogue, the economics card) preselect the first
      interest option, the full price list, when nothing is chosen, and closing without
      sending undoes it, so a later link starts clean. The product window's
      add-to-menu link sends the product's name as the interest when the visitor leaves it
      empty. generate_lead carries lead_cta.

The form also gets visible labels. The four required fields come first, and role, email,
interest and message sit behind one disclosure. No new form_name, no intake change.

Every edit asserts its anchor, so a silent no-op is impossible. Runs last, after patch_ipad.py.
"""
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"

applied: list[str] = []


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        sys.exit(f"FAIL [patch_lead_dialog]: {label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new)


FIELDS_OLD = (
    '    <div class="pf-row">\n'
    '      <input id="pf-name" name="name" autocomplete="name" placeholder="שם מלא *" required>\n'
    '      <input id="pf-venue" name="venue" autocomplete="organization" placeholder="שם העסק *" required>\n'
    '    </div>\n'
    '    <div class="pf-row">\n'
    '      <input id="pf-city" name="city" autocomplete="address-level2" placeholder="עיר *" required>\n'
    '      <select id="pf-role" name="role" aria-label="תפקיד">\n'
    '        <option value="">תפקיד</option><option>בעלים</option><option>מנהל/ת</option>\n'
    '        <option>אחראי/ת בר</option><option>בריסטה</option><option>אחר</option>\n'
    '      </select>\n'
    '    </div>\n'
    '    <div class="pf-row">\n'
    '      <input id="pf-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="טלפון *" required>\n'
    '      <input id="pf-mail" name="email" type="email" inputmode="email" autocomplete="email" placeholder="אימייל">\n'
    '    </div>\n'
    '    <select id="pf-int" name="interest" aria-label="מה מעניין אתכם">\n'
    '      <option value="">מה מעניין אתכם…</option><option>המחירון המלא</option><option>טעימה במקום</option>\n'
    '      <option>תמציות תה</option><option>מאצ׳ה ואבקות</option><option>מחיות פרי</option>\n'
    '      <option>כלי בר ואביזרים</option><option>כל תפריט הקיץ</option>\n'
    '    </select>\n'
    '    <textarea id="pf-msg" name="message" rows="3" placeholder="משהו שכדאי שנדע? (לא חובה)"></textarea>\n'
)
# Labels, not placeholders: a placeholder disappears as the visitor types. The words are the old
# placeholders'. The optional four sit behind one disclosure; the full price list stays the first
# interest option, because the data-price links select option 1.
FIELDS_NEW = (
    '    <div class="pf-req">\n'
    '      <label class="pf-f"><span>שם מלא</span><input id="pf-name" name="name" autocomplete="name" required></label>\n'
    '      <label class="pf-f"><span>שם העסק</span><input id="pf-venue" name="venue" autocomplete="organization" required></label>\n'
    '      <label class="pf-f"><span>עיר</span><input id="pf-city" name="city" autocomplete="address-level2" required></label>\n'
    '      <label class="pf-f"><span>טלפון</span><input id="pf-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required></label>\n'
    '    </div>\n'
    '    <details class="pf-more"><summary>עוד פרטים (לא חובה)</summary><div>\n'
    '      <label class="pf-f"><span>תפקיד</span><select id="pf-role" name="role">\n'
    '        <option value=""></option><option>בעלים</option><option>מנהל/ת</option>\n'
    '        <option>אחראי/ת בר</option><option>בריסטה</option><option>אחר</option>\n'
    '      </select></label>\n'
    '      <label class="pf-f"><span>אימייל</span><input id="pf-mail" name="email" type="email" inputmode="email" autocomplete="email"></label>\n'
    '      <label class="pf-f"><span>מה מעניין אתכם</span><select id="pf-int" name="interest">\n'
    '        <option value=""></option><option>המחירון המלא</option><option>תמציות תה</option>\n'
    '        <option>מאצ׳ה ואבקות</option><option>מחיות פרי</option>\n'
    '        <option>כלי בר ואביזרים</option><option>כל תפריט הקיץ</option>\n'
    '      </select></label>\n'
    '      <label class="pf-f"><span>משהו שכדאי שנדע?</span><textarea id="pf-msg" name="message" rows="3"></textarea></label>\n'
    '    </div></details>\n'
)

# The steps around the form. The first asks whether the visitor has a business; its two answers
# are buttons, not links, so nothing leaves the page. A private buyer gets the shop that sells GT
# to the public. After a send, each line is a link to the lead number's WhatsApp (054-758-8132,
# Sales-Machine D-014) with the visitor's message already written, in Tom's words. The last line
# is not a product: it is help building a drinks menu (Tom, 2026-09-27).
ASK = (
    '    <div class="pf-ask"><p class="pf-q" id="pf-ask-q" tabindex="-1"><b>יש לכם עסק?</b>'
    '<span>אנחנו עובדים רק עם עסקים, בסיטונאות.</span></p>\n'
    '      <button class="btn" type="button" data-biz="1">כן, יש לי עסק</button>'
    '<button class="btn" type="button" data-biz="0">לא, לשימוש פרטי</button></div>\n'
    '    <div class="pf-priv"><p class="pf-q" id="pf-priv-q" tabindex="-1">'
    '<span>ללקוחות פרטיים, המוצרים שלנו נמכרים באתר של אליטה אופק.</span></p>\n'
    '      <a class="btn" href="https://elitaofek.co.il/product-category/gt/" target="_blank" rel="noopener">'
    'למוצרי GT אצל אליטה אופק <span class="arr" aria-hidden="true">←</span></a>'
    '<button class="pf-back" type="button" data-biz="">חזרה</button></div>\n'
)
WA_LEAD = "https://wa.me/972547588132?text="
LINES = ["מאצ׳ה", "אובה", "צ׳אי מסאלה", "תמציות תה", "בניית תפריט משקאות בעסק שלי"]


def line(name: str) -> str:
    wide = ' class="pf-wide"' if name == LINES[-1] else ""
    return (f'<a{wide} href="{WA_LEAD}{quote("היי, אני מעוניין ב" + name)}" target="_blank" rel="noopener">'
            f'{name}</a>')


PICK = (
    '    <div class="pf-pick" role="group" aria-labelledby="pf-pick-q"><p class="pf-q" id="pf-pick-q" tabindex="-1">'
    '<b>מה הכי מעניין אתכם?</b><span>נשלח לכם את התפריט בוואטסאפ.</span></p>\n'
    '      <div class="pf-lines">' + "".join(line(n) for n in LINES) + '</div></div>\n'
)

# The dialog is a shell: the form moves in on open. The <style media="all"> is deliberate:
# build_theme.py lifts every bare <style> into gt-site.css, and this one must stay in the page,
# inside <noscript>, so that without JavaScript the revealed-on-scroll blocks (.rv) are visible,
# #contact's phone, WhatsApp and mail links among them.
SHELL = (
    '<dialog id="ldlg" aria-labelledby="ld-h"><div class="ld-pic" aria-hidden="true"></div><div class="ld-main">'
    '<button class="ld-x" type="button" aria-label="סגירה">✕</button>'
    '</div></dialog>\n'
    '<noscript><style media="all">.rv{opacity:1;transform:none}</style></noscript>\n'
)

CSS = """
/* ====================================================================
   The lead dialog (tools/patch_lead_dialog.py). Appended last.
   ==================================================================== */
/* the closing call-to-action: the decorative GT behind it was painted over the button and took its taps */
.bigcta .ghost{pointer-events:none}
/* the form: visible labels; the four required fields first, the rest behind one disclosure */
.partner .pf-req{display:grid;gap:14px}
@media(min-width:640px){.partner .pf-req{grid-template-columns:1fr 1fr}}
.partner .pf-f{display:grid;gap:6px;min-width:0}
.partner .pf-f>span{font-size:13.5px;font-weight:700;color:var(--ink-soft)}
.partner .pf-more summary{display:flex;align-items:center;gap:8px;min-height:44px;cursor:pointer;list-style:none;font-size:14px;font-weight:700;color:var(--gt)}
.partner .pf-more summary::-webkit-details-marker{display:none}
.partner .pf-more summary::before{content:'+';width:14px;text-align:center}
.partner .pf-more[open] summary::before{content:'\\2212'}
.partner .pf-more>div{display:grid;gap:14px;padding-top:4px}
/* the steps: whether the visitor has a business, the answer for a private buyer, and after a send
   the line that interests them; each step shows the heading and itself only */
.partner .pf-ask,.partner .pf-priv,.partner .pf-pick{display:none}
.partner.ask>*:not(.pf-head):not(.pf-ask),.partner.priv>*:not(.pf-head):not(.pf-priv){display:none}
.partner.ask .pf-ask,.partner.priv .pf-priv,.partner.sent .pf-pick{display:grid;gap:12px}
.partner .pf-q{margin:0 0 4px}
.partner .pf-q b{display:block;font-size:20px;font-weight:800;line-height:1.3}
.partner .pf-q span{display:block;margin-top:4px;font-size:15px;line-height:1.5;color:var(--ink-soft)}
.partner .pf-q:focus,#ld-h:focus{outline:none}
.partner .pf-ask .btn,.partner .pf-priv .btn{justify-content:center;min-height:52px;font-size:15px}
.partner .pf-ask .btn+.btn,.partner .pf-ask .btn+.btn:hover{background:none;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--line)}
.partner .pf-ask .btn+.btn:hover{box-shadow:inset 0 0 0 1.5px var(--ink)}
.partner .pf-back{justify-self:center;min-height:44px;padding:0 18px;border:0;background:none;font:inherit;font-size:14px;font-weight:700;color:var(--gt);cursor:pointer}
.partner .pf-lines{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.partner .pf-lines a{display:flex;align-items:center;justify-content:center;min-height:52px;padding:8px 14px;border-radius:999px;background:var(--white);box-shadow:inset 0 0 0 1.5px var(--line);color:var(--ink);font-size:15px;font-weight:700;line-height:1.25;text-align:center;text-decoration:none;transition:box-shadow .2s}
.partner .pf-lines a:hover,.partner .pf-lines a:focus-visible{box-shadow:inset 0 0 0 2px var(--gt);outline:none}
.partner .pf-lines .pf-wide{grid-column:1/-1}
/* the dialog: a bottom sheet on phones, a centred card from 640px */
#ldlg{border:0;padding:0 0 env(safe-area-inset-bottom,0);margin:auto auto 0;width:100%;max-width:100%;max-height:92vh;max-height:92dvh;
 background:var(--paper);color:var(--ink);border-radius:26px 26px 0 0;box-shadow:0 -18px 60px -20px rgba(24,26,22,.45);overflow:auto;overscroll-behavior:contain}
#ldlg::backdrop{background:rgba(24,26,22,.55);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
@media(min-width:640px){#ldlg{margin:auto;max-width:480px;border-radius:26px;box-shadow:0 40px 90px -30px rgba(24,26,22,.55)}}
/* the dialog wears the drink it was opened from: its colour on the sheet's rim, and from 880px its
   photo beside the form, the way the product window pairs photo and text */
#ldlg{border-top:6px solid var(--ld-tint,var(--gt))}
#ldlg .ld-pic{display:none}
@media(min-width:880px){
 #ldlg{max-width:820px;border-top:0}
 #ldlg[open]{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr)}
 #ldlg .ld-pic{display:block;background:var(--ld-tint,var(--gt)) center/cover no-repeat}
}
#ldlg .btn:active{transform:scale(.98)}
/* short phones (iPhone SE, 320x640): a tighter rhythm, so the consent and the button are on the first screen */
@media(max-width:639px) and (max-height:760px){
 #ldlg form.partner{padding:12px 18px 16px;gap:9px}
 #ldlg .pf-head b{font-size:24px}
 #ldlg .pf-req{gap:9px}
 #ldlg .pf-f{gap:4px}
 #ldlg input:not([type=checkbox]),#ldlg select{padding:10px 14px}
 #ldlg .pf-more summary{min-height:40px}
 #ldlg form.partner>button.btn{min-height:50px}
}
#ldlg[open]{animation:ld-up .32s cubic-bezier(.2,.8,.25,1)}
#ldlg[open]::backdrop{animation:ld-fade .32s ease}
@keyframes ld-up{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}
@keyframes ld-fade{from{opacity:0}}
#ldlg .ld-x{position:absolute;top:12px;left:12px;z-index:1;width:44px;height:44px;border:0;border-radius:50%;background:var(--card);color:var(--ink);font-size:18px;cursor:pointer}
#ldlg .ld-x:focus-visible{outline:2px solid var(--gt);outline-offset:2px}
#ldlg form.partner{border:0;border-radius:0;box-shadow:none;background:none;padding:20px 22px 24px;gap:14px;opacity:1;transform:none;transition:none}
#ldlg .pf-head{padding-left:52px}
#ldlg .pf-head b{font-size:28px;line-height:1.15}
#ldlg input:not([type=checkbox]),#ldlg select,#ldlg textarea{background:#fff}
#ldlg form.partner>button.btn{width:100%;min-height:54px;font-size:16px;letter-spacing:.02em}
/* sent: a check and the thanks, then the lines */
.partner .ld-check{display:none}
#ldlg .partner.sent>*:not(.pf-done):not(.ld-check):not(.pf-pick){display:none}
#ldlg .partner.sent .ld-check{display:block;width:64px;height:64px;margin:8px auto 0}
.ld-check circle{fill:#EEF4EA;stroke:var(--gt);stroke-width:2}
.ld-check path{fill:none;stroke:var(--gt);stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:40;stroke-dashoffset:40;animation:ld-draw .45s .1s ease-out forwards}
@keyframes ld-draw{to{stroke-dashoffset:0}}
#ldlg .partner.sent .pf-done{background:none;padding:6px 0 0;text-align:center;font-size:15px}
#ldlg .partner.sent .pf-done b{margin:6px 0 4px;font-family:'Roca One','Heebo',serif;font-weight:400;font-size:28px}
#ldlg .partner.sent .pf-pick{margin-top:6px;padding-top:18px;border-top:1px solid var(--line);text-align:center}
@media(prefers-reduced-motion:reduce){#ldlg[open],#ldlg[open]::backdrop,.ld-check path{animation:none}.ld-check path{stroke-dashoffset:0}}
"""

JS = """<script>
/* The lead dialog (tools/patch_lead_dialog.py). Every a[href="#contact"] opens #pform in a modal
   dialog; the form moves in and back, so there is one form, one sender and one state. */
var ldInv=null,ldCard=null,ldCta='contact',ldCtx='',ldAuto=0,ldDoc=Math.random();
(function(){var o=window.openF;if(o)window.openF=function(c){ldCard=c;return o.apply(this,arguments);};})();
function ldIn(){var d=document.getElementById('ldlg');return !!(d&&d.open);}
/* focus what the step starts with: its question; in the form, the first field on a mouse-and-
   keyboard screen, else the heading, so a touch keyboard does not open by itself */
function ldStep(f){
 var q=f.classList.contains('sent')?'pf-pick-q':f.classList.contains('ask')?'pf-ask-q':f.classList.contains('priv')?'pf-priv-q'
  :matchMedia('(pointer:fine)').matches?'pf-name':'ld-h';
 document.getElementById(q).focus({preventScroll:true});}
function ldOpen(a){
 var d=document.getElementById('ldlg'),f=document.getElementById('pform'),s=document.getElementById('pf-slot'),i=document.getElementById('pf-int');
 if(!d||!d.showModal||d.open)return false;
 var fm=a.closest('#fmodal'),sl=a.closest('.hs-slide');
 ldInv=fm?(ldCard||a):a;
 ldCta=(a.getAttribute('data-cta')||'link')+(sl?'-'+([].indexOf.call(sl.parentNode.children,sl)+1):'');
 ldCtx=fm?document.getElementById('fm-name').textContent.trim():'';
 if(a.hasAttribute('data-price')&&!i.value){i.selectedIndex=1;ldAuto=1;}
 var h=document.querySelector('img[fetchpriority="high"]');
 d.querySelector('.ld-pic').style.backgroundImage=sl?(sl.dataset.hsbg?'url("'+sl.dataset.hsbg+'")':sl.style.getPropertyValue('--hsbg'))
  :'url("'+(fm?document.getElementById('fm-img').currentSrc:h?h.currentSrc:'')+'")';
 d.style.setProperty('--ld-tint',(sl&&sl.getAttribute('data-bg'))||(fm&&ldCard&&ldCard.style.backgroundColor)||'var(--gt)');
 s.style.height=f.offsetHeight+'px';
 f.classList.add('on');
 d.querySelector('.ld-main').appendChild(f);
 if(document.activeElement&&document.activeElement.blur)document.activeElement.blur();
 document.documentElement.classList.add('cm-lock');
 history.pushState({gtLead:1,doc:ldDoc},'');
 d.showModal();d.scrollTop=0;ldStep(f);
 return true;}
function ldClose(){var d=document.getElementById('ldlg');if(d&&d.open)d.close();}
(function(){var f=document.getElementById('pform');if(!f)return;
 if(!f.classList.contains('sent'))f.classList.add('ask');
 f.addEventListener('click',function(e){
  var b=e.target.closest('[data-biz]'),v=b&&b.getAttribute('data-biz');
  if(b){f.classList.remove('ask','priv');if(v)f.classList.toggle('priv',v==='0');else f.classList.add('ask');ldStep(f);return;}
  /* a line picked: WhatsApp opens in its own tab or app, and the dialog is done when the visitor
     comes back. Closing at once would step history back while an in-app browser, which opens the
     link in the same tab, is still on its way to WhatsApp, and would cancel it. */
  if(e.target.closest('.pf-lines a')&&ldIn())document.addEventListener('visibilitychange',function w(){
   if(document.hidden)return;document.removeEventListener('visibilitychange',w);ldClose();});});
})();
(function(){var d=document.getElementById('ldlg');if(!d||!d.showModal)return;
 d.addEventListener('close',function(){
  var f=document.getElementById('pform'),s=document.getElementById('pf-slot'),i=document.getElementById('pf-int'),h=history.state;
  if(ldAuto&&i.selectedIndex===1&&!f.classList.contains('sent'))i.selectedIndex=0;ldAuto=0;
  s.appendChild(f);s.style.height='';
  document.documentElement.classList.remove('cm-lock');
  if(h&&h.gtLead&&h.doc===ldDoc)history.back();
  if(ldInv&&ldInv.focus)ldInv.focus({preventScroll:true});
  ldCta='contact';ldCtx='';});
 d.querySelector('.ld-x').addEventListener('click',ldClose);
 d.addEventListener('click',function(e){if(e.target!==d)return;var r=d.getBoundingClientRect();
  if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)ldClose();});
 window.addEventListener('popstate',function(){if(d.open)d.close();});
 document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href="#contact"]');
  if(!a||a.classList.contains('fcard')||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
  if(ldOpen(a))e.preventDefault();});
})();
/* the product window: its title takes focus when it opens, and the card that opened it takes it
   back when it closes, unless the lead dialog or a recipe card has it by then */
(function(){var fm=document.getElementById('fmodal'),on=false;if(!fm||!window.MutationObserver)return;
 new MutationObserver(function(){var o=fm.classList.contains('open');if(o===on)return;on=o;
  if(o)document.getElementById('fm-name').focus({preventScroll:true});
  else if(ldCard&&!ldIn()&&!document.querySelector('#cmodal.open'))ldCard.focus({preventScroll:true});
 }).observe(fm,{attributes:true,attributeFilter:['class']});})();
</script>
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ── the calls-to-action: a name for lead_cta, and which ones ask for the price list ──
    text = sub("cta: nav", '<a class="btn" href="#contact">רוצים להתחיל',
               '<a class="btn" href="#contact" data-cta="nav">רוצים להתחיל', text)
    text = sub("cta: hero", '<a class="btn" href="#contact">אני מעוניין',
               '<a class="btn" href="#contact" data-cta="hero">אני מעוניין', text)
    text = sub("cta: the ten slides", '<a class="sub-cta" href="#contact">רוצה מחירון</a>',
               '<a class="sub-cta" href="#contact" data-cta="slide" data-price>רוצה מחירון</a>', text, 10)
    text = sub("cta: catalogue", '<a class="btn" href="#contact">לקבלת הקטלוג המלא',
               '<a class="btn" href="#contact" data-cta="catalogue" data-price>לקבלת הקטלוג המלא', text)
    text = sub("cta: economics", '<a class="btn light" style="margin-top:24px" href="#contact">רוצה מחירון ותמחירים',
               '<a class="btn light" style="margin-top:24px" href="#contact" data-cta="economics" data-price>רוצה מחירון ותמחירים', text)
    text = sub("cta: closing", '<a class="btn light" href="#contact">רוצים להתחיל',
               '<a class="btn light" href="#contact" data-cta="closing">רוצים להתחיל', text)
    text = sub("cta: product window", '<a class="cta" href="#contact" onclick=',
               '<a class="cta" href="#contact" data-cta="product" onclick=', text)

    # ── the form: labels, required first, the slot it returns to, the check ──
    text = sub("form fields", FIELDS_OLD, FIELDS_NEW, text)
    text = sub("form heading names the dialog, then the business question",
               '<div class="pf-head"><b>בקשת מחירון</b><span>עונים תוך יום עסקים אחד</span></div>\n',
               '<div class="pf-head"><b id="ld-h" tabindex="-1">בקשת מחירון</b><span>עונים תוך יום עסקים אחד</span></div>\n' + ASK, text)
    text = sub("form slot opens", '<form class="rv partner" id="pform"', '<div id="pf-slot"><form class="rv partner" id="pform"', text)
    text = sub("form slot closes, after the lines", '  </form>\n</div></section>', PICK + '  </form></div>\n</div></section>', text)
    text = sub("sent check", '<div class="pf-done" id="pf-done"',
               '<svg class="ld-check" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="30"/>'
               '<path d="M20 33l8 8 16-17"/></svg>\n    <div class="pf-done" id="pf-done"', text)
    text = sub("dialog stylesheet", "</style>", CSS + "</style>", text)  # before the shell: it adds a </style>
    text = sub("dialog shell", '<footer class="site wrap">', SHELL + '<footer class="site wrap">', text)

    # ── the sender: held to 3 s, success only with was_new, the page never scrolled from the dialog ──
    text = sub("send: remember where it started", " btn.disabled=true;btn.innerHTML=",
               " var viaDlg=ldIn();btn.disabled=true;btn.innerHTML=", text)
    text = sub("send: an error scrolls only the form it is in", "  err.scrollIntoView({block:'nearest',behavior:'smooth'});};",
               "  if(!viaDlg||ldIn())err.scrollIntoView({block:'nearest',behavior:'smooth'});};", text)
    # The intake answers {ok:true} and stores nothing when elapsed_ms < 3000, so a fast,
    # autofilled person would be thanked for a lead that never landed. Hold the send until 3 s
    # after navigation start; the button already says it is sending.
    text = sub("send: held to 3 s from navigation start", " var body={contact_name:g('pf-name')",
               " setTimeout(function(){var body={contact_name:g('pf-name')", text)
    text = sub("send: the hold ends", " .catch(function(){clearTimeout(to);fail(PF_ERR);});\n return false;}",
               " .catch(function(){clearTimeout(to);fail(PF_ERR);});\n },Math.max(0,3050-performance.now()));\n return false;}", text)
    text = sub("send: the product is the interest when none is chosen", "interest:g('pf-int'),",
               "interest:g('pf-int')||ldCtx,", text)
    # Coupled to website_lead_intake: it answers {ok:true} without was_new for its two silent
    # drops (a filled honeypot, elapsed_ms < 3000). Only the real path carries was_new.
    text = sub("send: success means stored", "   if(res.ok&&res.j&&res.j.ok){pfTrack(g('pf-int'),g('pf-role'));",
               "   if(res.ok&&res.j&&res.j.ok&&'was_new' in res.j){pfTrack(g('pf-int')||ldCtx,g('pf-role'),ldCta);", text)
    text = sub("send: the thanks, then the lines",
               "    document.getElementById('pf-done').scrollIntoView({block:'nearest',behavior:'smooth'});return;}",
               "    if(ldIn())document.getElementById('ldlg').scrollTop=0;\n"
               "    else if(!viaDlg)document.getElementById('pf-done').scrollIntoView({block:'nearest',behavior:'smooth'});\n"
               "    if(!viaDlg||ldIn())ldStep(f);return;}", text)
    text = sub("lead_cta", "function pfTrack(interest,role){", "function pfTrack(interest,role,cta){", text)
    text = sub("lead_cta field", "  lead_interest:interest||'',lead_role:role||''});",
               "  lead_interest:interest||'',lead_role:role||'',lead_cta:cta||'contact'});", text)

    text = sub("dialog script", "</body>", JS + "</body>", text)

    SRC.write_text(text, encoding="utf-8")
    print(f"lead dialog: {len(applied)} changes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
