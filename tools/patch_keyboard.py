#!/usr/bin/env python3
"""Keyboard, focus and motion: what the 2026-09-28 site gate found (INTER, A11Y, CRO, COPY).

  The three windows (recipe card, product window, purée gallery)
      Focus never entered the recipe card or the gallery and never came back: 48 Tab presses
      under the backdrop to reach the card's ×, and Esc dropped focus to the page (A11Y-01, P0).
      Now each window's title takes focus on open, Tab and Shift+Tab stay inside the window, and
      focus returns to what opened it. The gallery closes on Esc. The product window and the
      gallery lock the page like the recipe card, and the phone's back gesture closes them
      instead of leaving the site (INTER-03): each pushes one history entry, and a hand-over to
      the recipe card replaces it, so closing the card steps back to the page, not to a window.

  The recipe card
      Chips were rebuilt on every drink change, so the focused chip vanished; the end buttons were
      disabled under the focus. Chips are rebuilt only when the collection changes, the current one
      carries aria-current, the end buttons say aria-disabled (cmGo already clamps), and the drink
      name is announced. The header's colour is darkened just enough for white text (A11Y-03),
      the body scrolls from the keyboard, and the × no longer covers a long title on a phone.

  The hero carousel
      Autoplay held for nobody (INTER-02, A11Y-04). Now a mouse over it holds it, a finger on it
      holds it until 5 s after the finger lifts, and keyboard focus or a click inside it stops it
      for the visit, as the WAI-ARIA carousel pattern does. It never turns under an open window.
      Only the current slide is reachable: the other nine are inert. It is a section, not the
      page's banner.

  The form's edges
      A required field left blank (spaces pass the browser's check) or a phone under 9 digits (the
      intake's own rule) is caught before the 3-second hold, with the approved messages, and the
      field is marked and focused; so are the fields the intake names. A late reply after the 15-s
      timeout is aborted, so it can no longer show the error and the thanks together or count a lead
      twice. A reply that lands after the dialog was closed during «שולח…» reopens the dialog, and
      the lead keeps the slide or product it came from. After a send, focus lands on the thanks.
      Sent inline, the used form folds to the heading, the check, the thanks and the lines.

  The rest
      FAQ answers that say "leave your details below" open the form (no words change); a white
      focus ring on the green and magenta bands; the FAQ group headings at 4.9:1; room above a
      focused control for the sticky nav; the products menu no longer puts 15 links in the Tab
      path on desktop, and a first tap on it on a touch screen does not leave it open over the
      grid; the burger closes on Esc (focus back on it), on rotation past 980 px and when focus
      leaves it; glyphs out of accessible names; a <main> landmark; reduced motion stops the
      reveal and the marquees pause under the pointer; the page is readable before its script
      runs (CRO-10), so a lead sent to /#faq lands on text.

Every edit asserts its anchor, so a silent no-op is impossible. Runs last, after patch_lead_dialog.py.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"

applied: list[str] = []


def sub(label: str, old: str, new: str, text: str, count: int = 1) -> str:
    n = text.count(old)
    if n != count:
        sys.exit(f"FAIL [patch_keyboard]: {label}: expected {count} occurrence(s), found {n}")
    applied.append(label)
    return text.replace(old, new)


# The recipe card's header colour, per collection: the smallest darkening that gives white text
# 4.5:1 (the kicker is 11 px and the English name 15 px). Ube already passes. #4C823D and
# #B85B36 are the landing pages' own accent-text colours.
CM_HEAD = ('var CM_HEAD={"var(--terra)":"#A96440","var(--energy)":"#9C6C26","var(--revive)":"#C05440",'
           '"#7FA8B8":"#5D7B86","var(--matcha)":"#4C823D","#8C8C7A":"#777768","#5FA89B":"#488076",'
           '"var(--nama)":"#B85B36","#B0793B":"#9D6C35"};\n')

CHIPS_OLD = (
    " document.getElementById('cm-prev').disabled=(cmI===0);\n"
    " document.getElementById('cm-next').disabled=(cmI===c.drinks.length-1);\n"
    " const dots=document.getElementById('cm-dots');dots.innerHTML='';\n"
    " c.drinks.forEach((dd,i)=>{const sp=document.createElement('button');sp.type='button';\n"
    "  sp.className='cm-chip'+(i===cmI?' on':'');sp.textContent=dn(dd);\n"
    "  sp.onclick=()=>{cmI=i;cmRender();};dots.appendChild(sp);});\n"
)
CHIPS_NEW = (
    " document.getElementById('cm-prev').setAttribute('aria-disabled',cmI===0?'true':'false');\n"
    " document.getElementById('cm-next').setAttribute('aria-disabled',cmI===c.drinks.length-1?'true':'false');\n"
    " const dots=document.getElementById('cm-dots');\n"
    " if(dots.dataset.c!==String(cmC)){dots.dataset.c=cmC;dots.innerHTML='';\n"
    " c.drinks.forEach((dd,i)=>{const sp=document.createElement('button');sp.type='button';\n"
    "  sp.className='cm-chip';sp.textContent=dn(dd);\n"
    "  sp.onclick=()=>{cmI=i;cmRender();};dots.appendChild(sp);});}\n"
    " [].forEach.call(dots.children,(sp,i)=>{sp.classList.toggle('on',i===cmI);"
    "if(i===cmI)sp.setAttribute('aria-current','true');else sp.removeAttribute('aria-current');});\n"
)

FAIL_OLD = (
    " var fail=function(msg){err.innerHTML=msg;err.hidden=false;\n"
    "  btn.disabled=false;btn.innerHTML=PF_LABEL;\n"
    "  if(!viaDlg||ldIn())err.scrollIntoView({block:'nearest',behavior:'smooth'});};\n"
    " err.hidden=true;\n"
    " var viaDlg=ldIn();btn.disabled=true;btn.innerHTML='שולח\\u2026';\n"
)
FAIL_NEW = (
    " var fail=function(msg,ids){err.innerHTML=msg;err.hidden=false;\n"
    "  btn.disabled=false;btn.innerHTML=PF_LABEL;\n"
    "  if(viaDlg&&!ldIn())ldBack();\n"
    "  if(!viaDlg||ldIn())err.scrollIntoView({block:'nearest',behavior:'smooth'});\n"
    "  pfMark(ids,btn);};\n"
    # before the hold: blanks (spaces pass `required`) and the intake's own phone rule
    " var miss=['pf-name','pf-venue','pf-city','pf-phone'].filter(function(id){return !g(id);});\n"
    " if(miss.length){err.innerHTML='חסרים פרטי חובה. בדקו שם מלא, שם העסק, עיר וטלפון.';err.hidden=false;pfMark(miss);return false;}\n"
    " if(g('pf-phone').replace(/\\D/g,'').length<9){err.innerHTML='מספר הטלפון לא נראה תקין. בדקו אותו ונסו שוב.';err.hidden=false;pfMark(['pf-phone']);return false;}\n"
    " err.hidden=true;\n"
    # the lead keeps where it came from, even if the dialog is closed during the send
    " var viaDlg=ldIn(),cta=ldCta,ctx=ldCtx;btn.disabled=true;btn.innerHTML='שולח\\u2026';\n"
)

TIMEOUT_OLD = (
    " var to=setTimeout(function(){fail(PF_ERR);},15000);\n"
    " fetch(PF_ENDPOINT,{method:'POST',headers:{'content-type':'application/json'},\n"
    "  body:JSON.stringify(body)})"
)
TIMEOUT_NEW = (
    " var ac=window.AbortController?new AbortController():null,to=setTimeout(function(){if(ac)ac.abort();else fail(PF_ERR);},15000);\n"
    " fetch(PF_ENDPOINT,{method:'POST',headers:{'content-type':'application/json'},signal:ac?ac.signal:undefined,\n"
    "  body:JSON.stringify(body)})"
)

CSS = """
/* ====================================================================
   Keyboard, focus and motion (tools/patch_keyboard.py, site gate 2026-09-28). Appended last.
   ==================================================================== */
/* the page is readable before its script runs: .rv hides only once gt-site.js has marked what is on screen */
.rv-on .rv{opacity:0;transform:translateY(26px);transition:opacity .7s ease,transform .7s ease}
.rv-on .rv.on{opacity:1;transform:none}
/* the recipe card: white text at 4.5:1 on its header, a × that reads on every colour, a keyboard-scrollable body */
#cmodal .cm-head .ch,#cmodal .cm-head .heh{opacity:1}
#cmodal .cm-x{background:rgba(20,22,18,.32)}
#cmodal .cm-num{opacity:.8}
#cm-en:focus,#pm-title:focus,.partner .pf-done:focus{outline:none}
#cmodal .cm-body:focus-visible{outline:2px solid var(--gt);outline-offset:-2px}
.cm-nav>button[aria-disabled="true"]{opacity:.25;cursor:default}
@media(max-width:700px){#cmodal .cm-head{padding-left:78px}}
/* the product window and the gallery keep a flick inside them */
.fmodal .box,.pm-card{overscroll-behavior:contain}
/* the hero: a finger's 44 px arrows; focus never scrolls the clipped track */
.hs{overflow:clip}
.hs-arr{width:44px;height:44px}
/* on colour and on photos the focus ring is white (on the paper it stays green) */
.econ :focus-visible,.bigcta :focus-visible,.hs .hs-copy :focus-visible{outline-color:#fff}
.hs-arr:focus-visible{outline-color:var(--ink)}
/* small terra text is #9C5C3C on the paper (4.9:1), as the eyebrows have been since 2026-09-27 */
#faq .faq-group{color:#9C5C3C}
@media(max-width:980px){.nav-links .dd-head{color:#9C5C3C}}
/* a focused control is never under the sticky nav (80 px on phones, 108 on desktop) */
html{scroll-padding-top:124px}
@media(max-width:640px){html{scroll-padding-top:96px}}
/* glyphs are not part of a name */
#faq summary::after{content:"+";content:"+" / ""}
#faq details[open] summary::after{content:"\\2013";content:"\\2013" / ""}
.partner .pf-more summary::before{content:'+';content:'+' / ''}
.partner .pf-more[open] summary::before{content:'\\2212';content:'\\2212' / ''}
/* desktop: focus on «מוצרים» does not open its 15 links into the Tab path; the pointer still opens it */
@media(min-width:981px){.nav-dd:focus-within:not(:hover) .dd-menu{opacity:0;visibility:hidden}}
/* the form: a field the send found wanting is marked; sent inline, the used form folds like the dialog's */
.partner [aria-invalid="true"]{border-color:#7A2E1E;box-shadow:0 0 0 1px #7A2E1E}
.partner.sent>*:not(.pf-head):not(.pf-done):not(.ld-check):not(.pf-pick){display:none}
.partner.sent .ld-check{display:block;width:64px;height:64px;margin:8px auto 0}
/* the lines wrap: the page keeps WhatsApp links on one line for phone numbers, and at 390 px the
   fifth line ran past its pill */
.partner .pf-lines a{white-space:normal}
/* motion: nothing slides in for a visitor who asked for less; the marquees stop under the pointer */
@media(prefers-reduced-motion:reduce){.rv-on .rv,.rv{opacity:1;transform:none;transition:none}html{scroll-behavior:auto}}
.ticker:hover .track,.pmarquee:hover .ptrack,.pmarquee:focus-within .ptrack{animation-play-state:paused}
"""

JS = """<script>
/* Keyboard, focus and motion (tools/patch_keyboard.py, site gate 2026-09-28). */
/* the form: mark the fields a send found wanting and focus the first; typing clears the mark */
function pfMark(ids,btn){ids=(ids||[]).filter(Boolean);
 ids.forEach(function(id){var el=document.getElementById(id);if(!el)return;var d=el.closest('details');if(d)d.open=true;
  el.setAttribute('aria-invalid','true');el.setAttribute('aria-describedby','pf-err');});
 var el=ids.length&&document.getElementById(ids[0]);
 if(el)el.focus();else if(btn&&(!document.activeElement||document.activeElement===document.body))btn.focus({preventScroll:true});}
/* a reply that lands after the dialog was closed during the send reopens it, unless a window is open */
function ldBack(){if(!document.querySelector('#cmodal.open,#fmodal.open,#pmodal.open'))ldOpen(document.querySelector('a[data-cta="nav"]'));}
(function(){var f=document.getElementById('pform');if(!f)return;
 f.addEventListener('input',function(e){var t=e.target;if(t.getAttribute&&t.getAttribute('aria-invalid')){t.removeAttribute('aria-invalid');t.removeAttribute('aria-describedby');}});})();
/* the three windows: focus in, Tab stays, focus back; Esc; the page locked; back closes them */
var pmCard=null;
(function(){var o=window.pmOpen;if(o)window.pmOpen=function(id){pmCard=document.getElementById('p-'+id);return o.apply(this,arguments);};})();
(function(){
 if(!window.MutationObserver)return;
 var root=document.documentElement,fromPop={},last=null,cmOpener=null;
 function isOpen(id){var el=document.getElementById(id);return !!(el&&el.classList.contains('open'));}
 function anyOpen(){return isOpen('cmodal')||isOpen('fmodal')||isOpen('pmodal');}
 function shown(x){return !!(x&&x.isConnected&&x.getClientRects().length&&!(x.closest&&x.closest('[inert]')));}
 function unlock(){if(!anyOpen()&&!ldIn())root.classList.remove('cm-lock');}
 /* what opened the recipe card: the focused control, or for a row in the product window or the
    gallery, the card that opened that window */
 function opener(){var a=document.activeElement,w=a&&a.closest&&a.closest('#fmodal,#pmodal');
  if(w)return w.id==='fmodal'?ldCard:pmCard;
  if(a&&a!==document.body&&a!==root)return a;
  return last&&Date.now()-last.t<800?last.el:null;}
 function watch(id,on,off){var el=document.getElementById(id);if(!el)return;var was=el.classList.contains('open');
  new MutationObserver(function(){var o=el.classList.contains('open');if(o===was)return;was=o;(o?on:off)();})
   .observe(el,{attributes:true,attributeFilter:['class']});}
 /* the product window and the gallery: one history entry each, the page locked while open */
 ['fmodal','pmodal'].forEach(function(id){
  watch(id,function(){root.classList.add('cm-lock');
    if(!(history.state&&history.state.gtWin))history.pushState({gtWin:id,doc:cmDoc},'');
    if(id==='pmodal')document.getElementById('pm-title').focus({preventScroll:true});},
   function(){last={el:id==='fmodal'?ldCard:pmCard,t:Date.now()};unlock();
    var s=history.state;
    if(fromPop[id])fromPop[id]=0;else if(s&&s.gtWin===id&&s.doc===cmDoc)history.back();
    if(id==='pmodal'&&!anyOpen()&&!ldIn()&&shown(pmCard))pmCard.focus({preventScroll:true});});});
 window.addEventListener('popstate',function(){['fmodal','pmodal'].forEach(function(id){var s=history.state;
  if(isOpen(id)&&!(s&&s.gtWin===id)){fromPop[id]=1;document.getElementById(id).classList.remove('open');}});});
 /* the recipe card: its title takes focus; on close, what opened it takes it back */
 watch('cmodal',function(){cmOpener=opener();document.getElementById('cm-en').focus({preventScroll:true});},
  function(){var o=cmOpener;cmOpener=null;if(!o||anyOpen()||ldIn())return;
   var sl=o.closest&&o.closest('.hs-slide');
   if(sl){var i=[].indexOf.call(sl.parentNode.children,sl);if(i!==hsI)hsGo(i);}
   if(shown(o))o.focus({preventScroll:true});
   else{var c=document.querySelector('.ccard[data-ci="'+cmC+'"]');if(c)c.focus({preventScroll:true});}});
 if(isOpen('cmodal'))document.getElementById('cm-en').focus({preventScroll:true});
 var SEL='a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex="0"]';
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&isOpen('pmodal')&&!ldIn()){document.getElementById('pmodal').classList.remove('open');return;}
  if(e.key!=='Tab'||ldIn())return;
  var id=isOpen('cmodal')?'cmodal':isOpen('pmodal')?'pmodal':isOpen('fmodal')?'fmodal':null;if(!id)return;
  var w=document.getElementById(id),f=[].filter.call(w.querySelectorAll(SEL),shown);if(!f.length)return;
  var a=document.activeElement,i=f.indexOf(a);
  if(!w.contains(a)){e.preventDefault();(e.shiftKey?f[f.length-1]:f[0]).focus();return;}
  if(e.shiftKey){if(i===0||(i<0&&!f.some(function(x){return x.compareDocumentPosition(a)&4;}))){e.preventDefault();f[f.length-1].focus();}}
  else if(i===f.length-1||(i<0&&!f.some(function(x){return a.compareDocumentPosition(x)&4;}))){e.preventDefault();f[0].focus();}});
})();
/* the recipe chips scroll sideways under a mouse wheel (RTL: scrollLeft runs negative) */
(function(){var d=document.getElementById('cm-dots');if(!d||!matchMedia('(hover:hover) and (pointer:fine)').matches)return;
 d.addEventListener('wheel',function(e){if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){d.scrollLeft-=e.deltaY;e.preventDefault();}},{passive:false});})();
/* the hero carousel: a mouse over it holds it, a finger holds it until 5 s after it lifts, focus or a
   click inside it stops it for the visit; only the current slide is reachable */
(function(){var hs=document.getElementById('hs');if(!hs)return;
 var stop=function(){hsStop=1;clearInterval(hsTimer);};
 hs.addEventListener('focusin',stop);
 hs.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse')stop();else hsHold=1;});
 var lift=function(e){if(e.pointerType!=='mouse'&&hsHold){hsHold=0;hsRestart();}};
 hs.addEventListener('pointerup',lift);hs.addEventListener('pointercancel',lift);
 hs.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')hsHold=1;});
 hs.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse')hsHold=0;});
 document.querySelectorAll('.hs-slide').forEach(function(s,j){s.inert=j!==hsI;});})();
/* the products menu: on a touch screen from 981 px, the first tap on «מוצרים» goes to the grid and leaves the menu shut */
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.nav-dd>a');
 if(!a||!matchMedia('(min-width:981px) and (hover:none)').matches)return;var dd=a.parentNode;dd.classList.add('dd-shut');
 document.addEventListener('pointerdown',function(){dd.classList.remove('dd-shut')},{once:true,capture:true});});
/* the burger: closes when the screen widens past 980 px and when focus leaves it */
(function(){var shut=function(){var n=document.querySelector('nav.open');if(!n)return;n.classList.remove('open');document.body.style.overflow='';
  var b=n.querySelector('.nav-burger');if(b)b.setAttribute('aria-expanded','false');};
 var mq=matchMedia('(max-width:980px)');if(mq.addEventListener)mq.addEventListener('change',function(){if(!mq.matches)shut();});
 document.addEventListener('focusin',function(e){var n=document.querySelector('nav.open');if(n&&!n.contains(e.target))shut();});})();
</script>
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ── markup: the windows' titles take focus, the card's body scrolls from the keyboard ──
    text = sub("recipe title takes focus, announces the drink", '<h3 id="cm-en"></h3>',
               '<h3 id="cm-en" tabindex="-1" aria-live="polite"></h3>', text)
    text = sub("gallery title takes focus", '<h3 id="pm-title"></h3>', '<h3 id="pm-title" tabindex="-1"></h3>', text)
    text = sub("recipe body scrolls from the keyboard", '<div class="cm-body"> <div class="cm-visual" id="cm-visual">',
               '<div class="cm-body" tabindex="0" role="region" aria-labelledby="cm-en"> <div class="cm-visual" id="cm-visual">', text)
    # ── the carousel is a section, not the page's banner ──
    text = sub("carousel: a section (opens)", '<header class="hs" id="hs">', '<section class="hs" id="hs">', text)
    text = sub("carousel: a section (closes)", '  <div class="hs-dots" id="hs-dots"></div>\n</header>',
               '  <div class="hs-dots" id="hs-dots"></div>\n</section>', text)
    # ── a <main> landmark: from the nav to the dialog shell (the windows stay after the footer) ──
    text = sub("main opens", '</div></nav>\n', '</div></nav>\n<main id="main">\n', text)
    text = sub("main closes", '<dialog id="ldlg"', '</main>\n<dialog id="ldlg"', text)
    # ── the FAQ's "leave your details below" opens the form; no word changes ──
    text = sub("faq: getting started opens the form", '<p>משאירים פרטים כאן למטה,',
               '<p><a href="#contact" data-cta="faq">משאירים פרטים כאן למטה</a>,', text)
    text = sub("faq: prices open the form", 'השאירו פרטים כאן למטה,',
               '<a href="#contact" data-cta="faq">השאירו פרטים כאן למטה</a>,', text)
    # ── after a send, focus lands on the thanks, so it is what a screen reader reads first ──
    text = sub("thanks takes focus instead of a live region", '<div class="pf-done" id="pf-done" role="status">',
               '<div class="pf-done" id="pf-done" tabindex="-1">', text)
    text = sub("the sent step focuses the thanks", "f.classList.contains('sent')?'pf-pick-q'",
               "f.classList.contains('sent')?'pf-done'", text)
    # ── glyphs out of accessible names ──
    text = sub("cta arrows hidden", '<span class="arr">←</span>', '<span class="arr" aria-hidden="true">←</span>', text, 15)
    text = sub("menu caret hidden", '<span class="car">▾</span>', '<span class="car" aria-hidden="true">▾</span>', text)
    text = sub("plus glyph hidden", '<span class="ico">+</span>', '<span class="ico" aria-hidden="true">+</span>', text)
    text = sub("recipe icon strip hidden (the steps say it)", "return '<div class=\"cm-build\">'",
               "return '<div class=\"cm-build\" aria-hidden=\"true\">'", text)
    text = sub("ticker hidden (the collections are named below)", '<div class="ticker"><div class="track">',
               '<div class="ticker" aria-hidden="true"><div class="track">', text)
    text = sub("hover-cycle tag hidden", "tag.className='cyc-tag';", "tag.className='cyc-tag';tag.setAttribute('aria-hidden','true');", text)
    n = len(re.findall(r'<img class="cimg"[^>]*? alt="[^"]*"', text))
    if n != 10:
        sys.exit(f"FAIL [patch_keyboard]: collection photos: expected 10, found {n}")
    text = re.sub(r'(<img class="cimg"[^>]*?) alt="[^"]*"', r'\1 alt=""', text)
    applied.append("collection photos: the card's heading names it")
    text = sub("the English tagline is English", '<span class="serif">Don\'t Drink Boring.</span>',
               '<span class="serif" lang="en">Don\'t Drink Boring.</span>', text)

    # ── the recipe card: chips kept, current marked, ends aria-disabled; the header's colour ──
    text = sub("recipe chips kept across drinks", CHIPS_OLD, CHIPS_NEW, text)
    text = sub("recipe header colour table", "function cmRender(){", CM_HEAD + "function cmRender(){", text)
    text = sub("recipe header colour", "document.getElementById('cm-head').style.background=c.ac;",
               "document.getElementById('cm-head').style.background=CM_HEAD[c.ac]||c.ac;", text)
    # a hand-over from the product window or the gallery replaces its history entry
    text = sub("recipe card takes over a window's entry", "history.pushState({gtRecipe:1,doc:cmDoc},",
               "history[history.state&&history.state.gtWin&&history.state.doc===cmDoc?'replaceState':'pushState']({gtRecipe:1,doc:cmDoc},", text)

    # ── the carousel: held, stopped, one reachable slide ──
    text = sub("carousel state", "let hsI=0,hsTimer=null;", "let hsI=0,hsTimer=null,hsHold=0,hsStop=0;", text)
    text = sub("carousel: only the current slide is reachable",
               "document.querySelectorAll('#hs-dots span').forEach((d,j)=>d.classList.toggle('on',j===hsI));",
               "document.querySelectorAll('#hs-dots span').forEach((d,j)=>d.classList.toggle('on',j===hsI));"
               "document.querySelectorAll('.hs-slide').forEach((s,j)=>{s.inert=j!==hsI;});", text)
    text = sub("carousel: autoplay yields",
               "function hsRestart(){clearInterval(hsTimer);if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;"
               "hsTimer=setInterval(()=>hsGo(hsI+1),5000);}",
               "function hsRestart(){clearInterval(hsTimer);if(hsStop||matchMedia('(prefers-reduced-motion:reduce)').matches)return;"
               "hsTimer=setInterval(()=>{if(!hsHold&&!document.hidden&&!document.documentElement.classList.contains('cm-lock'))hsGo(hsI+1);},5000);}", text)

    # ── the burger: Esc gives focus back to it; the logo and the nav's button close it too ──
    text = sub("burger: Esc returns focus",
               "var b=n.querySelector('.nav-burger');if(b)b.setAttribute('aria-expanded','false');});\nconst io=",
               "var b=n.querySelector('.nav-burger');if(b){b.setAttribute('aria-expanded','false');b.focus();}});\nconst io=", text)
    text = sub("burger: every nav link closes it", "var a=e.target.closest('.nav-links a');",
               "var a=e.target.closest('.nav-links a,nav .logo-gt,nav a.btn');", text)
    # ── the reveal: blocks on screen are shown before .rv can hide anything ──
    text = sub("reveal: hidden only once the script runs (CSS)",
               ".rv{opacity:0;transform:translateY(26px);transition:opacity .7s ease,transform .7s ease}\n.rv.on{opacity:1;transform:none}\n",
               "", text)
    text = sub("reveal: hidden only once the script runs (JS)",
               "document.querySelectorAll('.rv').forEach(el=>io.observe(el));",
               "document.querySelectorAll('.rv').forEach(el=>{var r=el.getBoundingClientRect();"
               "if(r.top<innerHeight&&r.bottom>0)el.classList.add('on');else io.observe(el);});"
               "document.documentElement.classList.add('rv-on');", text)

    # ── the form's edges ──
    text = sub("send: checked before the hold, marks what it rejects", FAIL_OLD, FAIL_NEW, text)
    text = sub("send: the interest kept from the tap", "interest:g('pf-int')||ldCtx,", "interest:g('pf-int')||ctx,", text)
    text = sub("send: a late reply is aborted", TIMEOUT_OLD, TIMEOUT_NEW, text)
    text = sub("send: success clears the error, counts the tap's cta",
               "if(res.ok&&res.j&&res.j.ok&&'was_new' in res.j){pfTrack(g('pf-int')||ldCtx,g('pf-role'),ldCta);",
               "if(res.ok&&res.j&&res.j.ok&&'was_new' in res.j){err.hidden=true;pfTrack(g('pf-int')||ctx,g('pf-role'),cta);", text)
    text = sub("send: a closed dialog reopens on the thanks; inline, the form comes into view",
               "    if(ldIn())document.getElementById('ldlg').scrollTop=0;\n"
               "    else if(!viaDlg)document.getElementById('pf-done').scrollIntoView({block:'nearest',behavior:'smooth'});",
               "    if(viaDlg&&!ldIn())ldBack();\n"
               "    if(ldIn())document.getElementById('ldlg').scrollTop=0;\n"
               "    else if(!viaDlg)f.scrollIntoView({block:'start',behavior:'smooth'});", text)
    text = sub("send: the fields the intake names are marked",
               "fail('חסרים פרטי חובה. בדקו שם מלא, שם העסק, עיר וטלפון.');return;}",
               "fail('חסרים פרטי חובה. בדקו שם מלא, שם העסק, עיר וטלפון.',(res.j.missing||[]).map(function(k){"
               "return {contact_name:'pf-name',venue:'pf-venue',city:'pf-city',phone:'pf-phone'}[k];}));return;}", text)
    text = sub("send: a bad phone is marked", "fail('מספר הטלפון לא נראה תקין. בדקו אותו ונסו שוב.');return;}",
               "fail('מספר הטלפון לא נראה תקין. בדקו אותו ונסו שוב.',['pf-phone']);return;}", text)
    text = sub("send: a bad email is marked", "fail('כתובת המייל לא נראית תקינה. בדקו אותה ונסו שוב.');return;}",
               "fail('כתובת המייל לא נראית תקינה. בדקו אותה ונסו שוב.',['pf-mail']);return;}", text)
    # the product window's add-to-menu hands over to the dialog: its entry is replaced, not stacked
    text = sub("dialog takes over a window's entry", "history.pushState({gtLead:1,doc:ldDoc},'');",
               "history[history.state&&history.state.gtWin&&history.state.doc===cmDoc?'replaceState':'pushState']({gtLead:1,doc:ldDoc},'');", text)
    # the dialog closing over a window leaves the page locked under it
    text = sub("dialog close keeps a window's lock",
               "  s.appendChild(f);s.style.height='';\n  document.documentElement.classList.remove('cm-lock');",
               "  s.appendChild(f);s.style.height='';\n"
               "  if(!document.querySelector('#fmodal.open,#pmodal.open,#cmodal.open'))document.documentElement.classList.remove('cm-lock');", text)

    text = sub("keyboard stylesheet",
               "@media(prefers-reduced-motion:reduce){#ldlg[open],#ldlg[open]::backdrop,.ld-check path{animation:none}"
               ".ld-check path{stroke-dashoffset:0}}\n</style>",
               "@media(prefers-reduced-motion:reduce){#ldlg[open],#ldlg[open]::backdrop,.ld-check path{animation:none}"
               ".ld-check path{stroke-dashoffset:0}}\n" + CSS + "</style>", text)
    text = sub("keyboard script", "</body>", JS + "</body>", text)

    SRC.write_text(text, encoding="utf-8")
    print(f"keyboard: {len(applied)} changes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
