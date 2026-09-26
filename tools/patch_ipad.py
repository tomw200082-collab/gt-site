#!/usr/bin/env python3
"""The recipe card on iPad, and the other touch findings of the 2026-09-25 UX gate.

Tom, 2026-09-25: the drink recipe pages do not work well on an iPad. The gate
(gt-factory-os docs/superpowers/plans/2026-09-25-customer-portal-ux-gate.md, §9 and
reports/IPAD-S.md) found the card breaking for three mechanical reasons, all in the
delivered English source, so every fix here is either an anchored `sub()` on the
script or CSS appended last, where it wins.

  The card scrolled as one block (G-59)
      "Hard-guard" rules made the whole card the scroller; header, prev/next
      and chips were never pinned. `.cm-body` is now the only scroller.

  The renderer scrolled the card to the chip row (G-57)
      `scrollIntoView` on the active chip moved every scrollable ancestor, about
      620 px, on open and on every next-drink tap. The chip strip scrolls itself now, the
      body resets to the top, and a collection card opens once (the second
      listener is gone).

  Invisible product links over the portrait screen (G-58)
      `visibility:inherit` on the folded dropdown (patch_rtl_shell.py), and here
      `-webkit-backdrop-filter` beside each unprefixed rule so Safari paints the
      same containing blocks.

  The photo filled the portrait card (G-60), the chips clipped their first row
  (G-61), step 1 of the icon strip sat off the card (G-62), the page scrolled
  behind the open card (G-63), one hero swipe moved two slides (G-64), hover
  reveals stuck on touch (G-65), and the small targets (G-70), the flavour
  modal's × (G-70), the hover-cycle downloads on touch (G-71) and the missing
  tap cue on collection cards (G-70).

  Upgrades: a swipe between drinks inside the card (U8: a finger moving right
  means next, it fires only when |dx| > 60 and |dx| > 1.5·|dy|), and deep links
  with the back gesture (U9: pushState on open, replaceState on a drink change,
  popstate closes, `#recipe-<collection>-<drink>` opens the card on load).
  Closing steps back only over an entry this page load pushed; a deep link the
  visitor arrived on keeps its entry and just loses the hash, because back()
  from there would take them off the site.

Every edit asserts its anchor, so a silent no-op is impossible. Runs last.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "index.html"

applied: list[str] = []


def sub(label: str, old: str, new: str, text: str) -> str:
    n = text.count(old)
    if n != 1:
        sys.exit(f"FAIL [patch_ipad]: {label}: expected 1 occurrence, found {n}")
    applied.append(label)
    return text.replace(old, new, 1)


# G-64: the hero slider's second swipe listener, removed whole (its call and its body).
HERO_SWIPE = """function heroSwipe(){
 var el=document.querySelector('.hs')||document.querySelector('#hero'); if(!el)return;
 var x0=null;
 el.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
 el.addEventListener('touchend',function(e){
  if(x0===null)return; var dx=e.changedTouches[0].clientX-x0; x0=null;
  if(Math.abs(dx)<45)return;
  if(typeof hsGo==='function'){hsGo(dx<0?hsI+1:hsI-1); if(typeof hsRestart==='function')hsRestart();}
 },{passive:true});
}
"""


CSS = """
/* ====================================================================
   iPad and touch (tools/patch_ipad.py, UX gate 2026-09-25). Appended last.
   ==================================================================== */
/* G-59 / G-57: the body is the only scroller; header, stats and nav stay pinned */
#cmodal .cm-card{max-height:94vh!important;max-height:94dvh!important;overflow:hidden!important}
#cmodal .cm-card .cm-scroll{display:flex;flex-direction:column;flex:1 1 auto!important;min-height:0!important;overflow:hidden}
#cmodal .cm-card .cm-body{flex:1 1 auto!important;min-height:0!important;overflow-x:hidden!important;overflow-y:auto!important;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
#cmodal .cm-card .cm-rec{max-height:none!important;overflow:visible!important}
#cmodal .cm-stats{margin-top:0}
#cmodal .cm-stats>div{display:flex;justify-content:center;align-items:baseline;gap:10px;padding:8px 10px}
#cmodal .cm-stats b{display:inline;font-size:22px!important}
@media(min-width:600px){
  #cmodal #cm-visual{position:sticky;top:0}
  #cmodal #cm-visual img{max-height:calc(94vh - 250px)!important;max-height:calc(94dvh - 250px)!important;object-fit:cover!important;object-position:50% 100%}
}
/* G-60: the photo sits beside the method in portrait; capped on phones */
@media(min-width:600px) and (max-width:860px){#cmodal .cm-card .cm-body{grid-template-columns:minmax(220px,38%) 1fr!important}}
@media(max-width:599px){#cmodal #cm-visual img{max-height:38vh!important;object-fit:cover!important;object-position:50% 100%}}
/* G-61: one swipeable chip row */
.cm-dots{flex-wrap:nowrap;justify-content:flex-start;align-content:normal;max-height:none!important;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;scroll-snap-type:x proximity;scrollbar-width:none;padding:4px 2px}
.cm-dots::-webkit-scrollbar{display:none}
.cm-chip{flex:0 0 auto;scroll-snap-align:center;min-height:40px;padding:8px 14px;font-size:13.5px}
/* G-62: the icon strip grows from its own start, not from the physical left */
#cm-glass{transform:none!important;margin:12px 0 16px!important}
.cm-build .st i{width:40px;height:40px;font-size:19px}
.cm-build .st b{font-size:11px}
/* G-63: the page stays put while a card is open */
html.cm-lock,html.cm-lock body{overflow:hidden}
/* G-70: 44 px targets in the recipe and flavour modals; the matrix chips grow to 36 px */
#cmodal .cm-x{width:44px;height:44px;top:14px}
.cm-nav>button{min-height:44px}
.mxd{min-height:36px;padding:8px 12px}
.fmodal .x{width:44px;height:44px;border-radius:50%;background:rgba(32,36,31,.45);top:14px;left:14px}
@media(hover:none) and (min-width:761px){.fmodal .box{overflow:auto}.fmodal .mtxt{max-height:none;display:block}.fmodal .makes{overflow:visible}}
/* G-58 parity: Safari paints the same containing blocks as Chromium */
nav{-webkit-backdrop-filter:blur(10px)}
#cmodal,.fmodal,#pmodal{-webkit-backdrop-filter:blur(6px)}
/* G-65: hover is for pointers; on touch nothing lifts, pours or reveals on the first tap */
@media(hover:none){
 .fcard:hover .comp{opacity:0;max-height:0;padding-top:0}
 .fcard.v3:hover .ph.vis img.hovimg{opacity:0}
 .fcard.v3:hover{transform:none;box-shadow:0 6px 30px rgba(32,36,31,.08)}
 .fcard.v3:hover .circle,.fcard:hover .ph img,.ccard:hover,.ccard:hover .cimg{transform:none}
 .fmodal a.mkgo i u{opacity:1;transform:none}
 .ccard small:after{content:"  \\2190"} /* G-70: a tap cue on collection cards */
}
/* G-65: the products menu folds after a pick (ddGo adds .dd-shut until the next pointerdown) */
.nav-dd.dd-shut .dd-menu{opacity:0!important;visibility:hidden!important}
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ── G-57: the chip strip scrolls itself; the card never moves ──────────
    # (`act` goes too: the scrollIntoView below was its only reader.)
    text = sub("chip strip scrolls itself, not the card",
               "const act=dots.querySelector('.on');\n"
               " if(act&&act.scrollIntoView)try{act.scrollIntoView({block:'nearest',inline:'center'})}catch(e){}",
               "cmCenterChip();var cb=document.querySelector('#cmodal .cm-body');if(cb)cb.scrollTop=0;"
               # the entry's state is kept as it is, so a drink change never changes who owns it
               "if(history.state&&history.state.gtRecipe)history.replaceState(history.state,'','#recipe-'+cmC+'-'+cmI);", text)
    # ── open: centre the chip, lock the page (G-63), push a history entry (U9) ──
    text = sub("open: centre chip, lock page, deep link",
               "function cmOpen(ci){cmC=ci;cmI=0;cmRender();document.getElementById('cmodal').classList.add('open');}",
               "function cmCenterChip(){var d=document.getElementById('cm-dots'),a=d&&d.querySelector('.on');"
               "if(!a||!d.clientWidth)return;var dr=d.getBoundingClientRect(),ar=a.getBoundingClientRect();"
               "d.scrollLeft+=(ar.left+ar.width/2)-(dr.left+dr.width/2);}\n"
               # one value per page load; an entry pushed by this load carries it as `doc`
               "var cmDoc=Math.random();\n"
               "function cmOpen(ci,di,fromPop){cmC=ci;cmI=di||0;"
               "if(!fromPop&&!(history.state&&history.state.gtRecipe))history.pushState({gtRecipe:1,doc:cmDoc},'','#recipe-'+cmC+'-'+cmI);"
               "cmRender();document.getElementById('cmodal').classList.add('open');"
               "document.documentElement.classList.add('cm-lock');cmCenterChip();}", text)
    text = sub("close: unlock page, step back out of the deep link",
               "function cmClose(){document.getElementById('cmodal').classList.remove('open');}",
               "function cmClose(fromPop){document.getElementById('cmodal').classList.remove('open');"
               "document.documentElement.classList.remove('cm-lock');var s=history.state;"
               "if(fromPop||!(s&&s.gtRecipe))return;"
               # Step back only over an entry this page load pushed. A deep link the visitor
               # arrived on (search result, pasted URL, bookmark, reload) is their own entry:
               # back() from it leaves the site, so it keeps its place and loses the hash.
               "if(s.doc===cmDoc)history.back();else history.replaceState(null,'',location.pathname+location.search);}\n"
               # one reader of the deep link, for popstate and for the first load
               "function cmFromHash(){var m=/^#recipe-(\\d+)-(\\d+)$/.exec(location.hash);if(!m||typeof COLS==='undefined'||!COLS[+m[1]])return false;"
               "cmOpen(+m[1],Math.min(+m[2],COLS[+m[1]].drinks.length-1),true);return true;}\n"
               "window.addEventListener('popstate',function(){if(!cmFromHash()&&document.getElementById('cmodal').classList.contains('open'))cmClose(true);});", text)
    # ── a card opens once: its inline onclick already does ──────────────────
    text = sub("a card opens once (its inline onclick already does)",
               "document.querySelectorAll('.ccard').forEach((el,i)=>{el.style.cursor='pointer';el.addEventListener('click',()=>cmOpen(i));});",
               "document.querySelectorAll('.ccard').forEach((el)=>{el.style.cursor='pointer';});\n"
               # U8: swipe between drinks. RTL: a finger moving right means next.
               "(function(){var c=document.querySelector('#cmodal .cm-card');if(!c)return;var x0=null,y0=0;"
               "c.addEventListener('touchstart',function(e){var t=e.touches[0];x0=t.clientX;y0=t.clientY;},{passive:true});"
               "c.addEventListener('touchend',function(e){if(x0==null)return;var t=e.changedTouches[0],dx=t.clientX-x0,dy=t.clientY-y0;x0=null;"
               "if(e.target.closest('.cm-dots,button,a'))return;if(Math.abs(dx)>60&&Math.abs(dx)>1.5*Math.abs(dy))cmGo(dx>0?1:-1);},{passive:true});})();\n"
               # U9: a shared or reloaded deep link opens its card. Its entry is marked, so the hash
               # follows the drink, but carries no `doc`: closing drops the hash instead of going back.
               "if(cmFromHash())history.replaceState({gtRecipe:1},'','#recipe-'+cmC+'-'+cmI);", text)
    # ── G-64: one swipe, one slide. That was heroSwipe's only call, so it goes too ──
    text = sub("one swipe, one slide", "try{heroSwipe()}catch(e){}", "", text)
    text = sub("heroSwipe, now uncalled", HERO_SWIPE, "", text)
    # ── G-65: no hover preview on touch; the products menu closes after a pick ──
    text = sub("no hover preview on touch",
               "a.addEventListener('mouseenter',function(){ if(pu)swapImg(pu);});",
               "if(matchMedia('(hover:hover)').matches)a.addEventListener('mouseenter',function(){ if(pu)swapImg(pu);});", text)
    text = sub("products menu closes after a pick",
               "function ddGo(e,id){e.preventDefault();",
               "function ddGo(e,id){e.preventDefault();var dd=e.target.closest&&e.target.closest('.nav-dd');"
               "if(dd){dd.classList.add('dd-shut');document.addEventListener('pointerdown',function(){dd.classList.remove('dd-shut')},{once:true,capture:true});}", text)
    # ── G-71: the 48-photo hover cycle is display:none on touch; do not fetch it ──
    text = sub("no hover-cycle on touch", "  function build(){", "  function build(){if(!matchMedia('(hover:hover)').matches)return;", text)

    text = sub("ipad stylesheet", "</style>", CSS + "</style>", text)

    SRC.write_text(text, encoding="utf-8")
    print(f"ipad: {len(applied)} fixes — {', '.join(applied)}")


if __name__ == "__main__":
    main()
