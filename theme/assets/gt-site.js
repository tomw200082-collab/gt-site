/* This file is served as a static asset, so Liquid never runs over it.
   Image references below are written as GT_ASSET_BASE + "<filename>"; the
   section sets window.GT_ASSET_BASE before this script loads. */
var GT_ASSET_BASE = (typeof window !== 'undefined' && window.GT_ASSET_BASE) || '';


document.addEventListener('keydown',function(e){var t=e.target;if(!t||!t.matches||!t.matches('[role="button"][onclick]'))return;if(e.key!=='Enter'&&e.key!==' ')return;e.preventDefault();t.click();});
function navToggle(b){var n=b.closest('nav');var open=n.classList.toggle('open');
 b.setAttribute('aria-expanded',open?'true':'false');
 document.body.style.overflow=open?'hidden':'';}
document.addEventListener('click',function(e){var a=e.target.closest('.nav-links a');
 if(!a)return;var n=a.closest('nav');if(!n||!n.classList.contains('open'))return;
 n.classList.remove('open');document.body.style.overflow='';
 var b=n.querySelector('.nav-burger');if(b)b.setAttribute('aria-expanded','false');});
document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;
 var n=document.querySelector('nav.open');if(!n)return;
 n.classList.remove('open');document.body.style.overflow='';
 var b=n.querySelector('.nav-burger');if(b)b.setAttribute('aria-expanded','false');});
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));

;

var FSCENE={"f-matcha":(GT_ASSET_BASE+"gt-7e97065cdf.webp"),"f-hojicha":(GT_ASSET_BASE+"gt-942aaf2e7c.webp"),"f-ube":(GT_ASSET_BASE+"gt-868e993bce.webp"),"f-detox":(GT_ASSET_BASE+"gt-4cc755499d.webp"),"f-energy":(GT_ASSET_BASE+"gt-ef4d3102be.webp"),"f-revive":(GT_ASSET_BASE+"gt-2939fe0ed9.webp"),"f-fresh":(GT_ASSET_BASE+"gt-d3abd65414.webp"),"f-consciousness":(GT_ASSET_BASE+"gt-398ddc71c5.webp"),"f-namastea":(GT_ASSET_BASE+"gt-74108519a7.webp"),"f-desertea":(GT_ASSET_BASE+"gt-d7c1e8617c.webp"),"f-calm":(GT_ASSET_BASE+"gt-6a21be6289.webp"),"f-american":(GT_ASSET_BASE+"gt-f88debdd2a.webp")};

const FL={
 "Detox":"הדגל של התפריט היומיומי. פרופיל קליל ומרענן שאורחים בכל גיל מבינים מיד — סיפור בריאות ברור וישר שלא צריך להסביר. עובד מצוין כחליטה קרה, כבסיס ללימונדה או כגזוז.",
 "Revive":"סנצ׳ה מדרגה גבוהה, מיובא ישירות מיפן, מורם עם פסיפלורה טרופית. כוס מפתיעה עם סיפור שהצוות שלכם יאהב לספר — וטעם שאורחים לא שוכחים.",
 "Energy":"קפאין טבעי עם נוכחות וארומה אמיתיות: תה ירוק, למון גראס, נענע ולימון. האלטרנטיבה הירוקה שמרחיבה את התפריט מעבר לקפה — בהיר, ארומטי, ער.",
 "Consciousness":"פרחוניות עדינה עם ליצ׳י טבעי — כוס אלגנטית ומדויקת. בנויה על 70% תה יסמין, עם ארומה רכה שנשארת הרבה אחרי הלגימה האחרונה.",
 "American":"הקלאסיקה האמריקאית עם חוצפה ישראלית. תה מיושן ועמוק שמורם ביוזו, ברגמוט והדרים — ובן זוג מושלם למחית אפרסק או מנגו מקו הסמוזי שלנו.",
 "Fresh":"קריאת השכמה בלי קפאין. אדום נועז ומסקרן שעוצר את הגלילה, עם חמיצות עדינה שמחזירה אורחים שוב ושוב.",
 "Desertea":"מוצר ישראלי ייחודי בלי מתחרים: חמישה צמחי בר מקומיים — לואיזה, נענע, אזוב, מליסה, מרווה וזוטה לבנה — בכוס אחת. בלי קפאין, בטעם של מדבר אחרי גשם.",
 "Calm":"עדין ואלגנטי, לכל גיל. קמומיל, תפוח וציפורן: מתוק בטבעיות, בלי קפאין — הכוס המושלמת לאחר הצהריים ולערב.",
 "Namastea":"רב מכר אדיר בקהל הישראלי. שני סוגי תה שחור וחמישה תבלינים — מבריק קר או עם מי קוקוס, ונהדר חם כצ׳אי לאטה עם כל חלב."
};

const T={
 tea:["ממלאים כוס בקרח","מוסיפים 50 מ״ל תרכיז GT","משלימים ל־⅔ במים קרים — או בסודה לגרסה מוגזת","קישוט: פרוסת לימון + עשבי תיבול טריים"],
 lem:["ממלאים כוס בקרח","מוסיפים 50 מ״ל תרכיז GT","ממלאים עד למעלה בלימונדה","מערבבים קלות ומגישים"],
 sig:(x)=>["ממלאים כוס בקרח","מוסיפים 40 מ״ל"+x,"מוסיפים 40 מ״ל תרכיז GT","משלימים ל־⅔ במים","מקשטים לפי הטעם"],
 gaz:(x)=>["ממלאים כוס בקרח","מוסיפים 40 מ״ל"+x,"מוסיפים 40 מ״ל תרכיז GT","משלימים בסודה (כ־150 מ״ל)","מקשטים"]
};
const MK={
 "Detox":[
  {t:"חליטת Detox קרה — רגילה או מוגזת",p:20,m:81,fc:"3.25",st:T.tea},
  {t:"משקה דגל תות־לואיזה",p:31,m:82,fc:"4.80",st:T.sig("מחית תות")}],
 "Revive":[
  {t:"חליטת Revive קרה — רגילה או מוגזת",p:20,m:81,fc:"3.25",st:T.tea},
  {t:"משקה דגל מנגו־סנצ׳ה",p:31,m:82,fc:"4.80",st:T.sig("מחית מנגו")}],
 "Energy":[
  {t:"חליטת Energy קרה — רגילה או מוגזת",p:20,m:81,fc:"3.25",st:T.tea}],
 "Consciousness":[
  {t:"חליטת יסמין־ליצ׳י",p:20,m:81,fc:"3.25",st:T.tea},
  {t:"גזוז ליצ׳י",p:25,m:85,fc:"3.08",st:["ממלאים כוס בקרח","מוסיפים 40 מ״ל מי ליצ׳י","מוסיפים 40 מ״ל תרכיז GT","משלימים בסודה (כ־150 מ״ל)","קישוט: 2 ליצ׳י טריים"]}],
 "American":[
  {t:"חליטת American קרה — רגילה או מוגזת",p:20,m:81,fc:"3.25",st:T.tea}],
 "Fresh":[
  {t:"חליטת Fresh",p:20,m:81,fc:"3.25",st:T.tea},
  {t:"לימונדת היביסקוס־ליים",p:22,m:79,fc:"3.95",st:T.lem},
  {t:"משקה דגל תפוח־היביסקוס",p:24,m:86,fc:"2.88",st:T.sig("מיץ תפוחים")},
  {t:"גזוז היביסקוס־תפוח",p:22,m:85,fc:"2.88",st:T.gaz("מיץ תפוחים")}],
 "Desertea":[
  {t:"חליטה מדברית",p:20,m:81,fc:"3.25",st:T.tea},
  {t:"לימונדה מדברית",p:22,m:79,fc:"3.95",st:T.lem},
  {t:"משקה דגל מדברי־אפרסק",p:31,m:82,fc:"4.80",st:T.sig("מחית אפרסק")},
  {t:"גזוז מדברי־אפרסק",p:33,m:83,fc:"4.80",st:T.gaz("מחית אפרסק")}],
 "Calm":[
  {t:"חליטת קמומיל־תפוח — רגילה או מוגזת",p:20,m:81,fc:"3.25",st:T.tea}],
 "Namastea":[
  {t:"אייס צ׳אי מסאלה קלאסי",p:28,m:77,fc:"5.57",st:["ממלאים כוס בקרח","משלימים ל־⅔ בחלב (כל חלב מתאים)","מוזגים 50 מ״ל תרכיז מסאלה GT","מכתירים בקצף חלב","מפזרים קינמון"]},
  {t:"צ׳אי מסאלה על קרח",p:24,m:82,fc:"3.70",st:["ממלאים כוס בקרח","משלימים ל־⅔ במים","מוזגים 50 מ״ל תרכיז מסאלה GT","מכתירים בקצף חלב נדיב"]},
  {t:"דירטי צ׳אי (עם אספרסו)",p:32,m:76,fc:"6.57",st:["מוציאים שוט אספרסו","ממלאים כוס בקרח","משלימים ל־⅔ בחלב","מוזגים 50 מ״ל מסאלה + האספרסו","מכתירים בקצף חלב"]},
  {t:"צ׳אי וטוניק תפוז מיובש",p:26,m:78,fc:"4.75",st:["ממלאים כוס בקרח","מוזגים 50 מ״ל תרכיז מסאלה GT","ממלאים בטוניק (כ־150 מ״ל)","מקשטים בפרוסת תפוז מיובש"]},
  {t:"טוניק ורדים ורוד",p:24,m:77,fc:"4.75",st:["ממלאים כוס בקרח","מוזגים 50 מ״ל תרכיז מסאלה GT","ממלאים בטוניק ורדים או אשכוליות (כ־150 מ״ל)"]},
  {t:"צ׳אי קולד פואם וניל",p:28,m:83,fc:"4.00",st:["ממלאים כוס בקרח","משלימים ל־⅔ במים","מוזגים 50 מ״ל תרכיז מסאלה GT","מכתירים בקצף קר וניל","מקשטים במקל וניל"]}]
};
const MKMORE={"Hojicha":"מוגש בשתי הדרכים — הוג׳יצ׳ה לאטה חם עם כל חלב, או קר על חלב. נימות קלויות של אגוזי לוז וקקאו.","American":"משתלב מושלם עם מחיות אפרסק ומנגו של ODK — הבסיס למשקאות הדגל.","Energy":"כל חליטה קרה היא גם גזוז: אותו מתכון, סודה במקום מים.","Calm":"כל חליטה קרה היא גם גזוז: אותו מתכון, סודה במקום מים."};
window.POUCH=['f-matcha','f-hojicha','f-ube'];
var POUCHCH={"Matcha":"אייס מאצ׳ה","Ube":"אובה"};
function renderMakesPouch(n){
 const box=document.getElementById('fm-makes');
 const ch=(typeof COLS!=='undefined')?COLS.find(x=>x.t===POUCHCH[n]):null;
 if(!ch){box.innerHTML=(typeof MKMORE!=='undefined'&&MKMORE[n])?('<div class="mkmore">'+MKMORE[n]+'</div>'):'';return;}
 let h='<h6>Menu drinks it makes \u2014 tap for recipe</h6>';
 ch.drinks.forEach(d=>{
  h+='<details class="mk"><summary><span>'+dn(d)+'</span><i>\u20aa'+d.p+' \u00b7 <b>'+d.m+'%</b></i></summary>';
  h+='<div class="rec"><ol>';
  d.st.forEach(x=>{h+='<li>'+x+'</li>'});
  h+='</ol><div class="fc">Food cost \u20aa'+d.fc+' ex-VAT \u00b7 recommended price \u20aa'+d.p+' incl. VAT \u00b7 margin '+d.m+'%</div></div></details>';
 });
 box.innerHTML=h;
}
function renderMakes(n){
 const box=document.getElementById('fm-makes');
 const list=MK[n]||[]; let h='';
 if(list.length){h+='<h6>Menu drinks it makes \u2014 tap for recipe</h6>';
  list.forEach(d=>{
   h+='<details class="mk"><summary><span>'+d.t+'</span><i>\u20aa'+d.p+' \u00b7 <b>'+d.m+'%</b></i></summary>';
   h+='<div class="rec"><ol>';
   d.st.forEach(x=>{h+='<li>'+x+'</li>'});
   h+='</ol><div class="fc">Food cost \u20aa'+d.fc+' ex-VAT \u00b7 recommended price \u20aa'+d.p+' incl. VAT \u00b7 margin '+d.m+'%</div></div></details>';
  });}
 if(MKMORE[n])h+='<div class="mkmore">'+MKMORE[n]+'</div>';
 box.innerHTML=h;
}

const DP={     "Chai & dry-orange tonic": (GT_ASSET_BASE+"gt-8150b6d37e.webp"), "Chai cold foam vanilla": (GT_ASSET_BASE+"gt-5211366790.webp")};

let baseImg='';
var fmPre={};
function fmPreload(u){ if(!u||fmPre[u])return; var i=new Image(); i.src=u; fmPre[u]=1; }
function swapImg(src){
 var im=document.getElementById('fm-img'); if(!im||!src)return;
 if(im.getAttribute('src')===src)return;
 var host=im.parentNode; if(!host)return;
 if(!im.getAttribute('src')){ im.setAttribute('src',src); im.style.opacity=1; return; }
 var prev=host.querySelector('.fm-ghost');
 if(prev&&prev.parentNode)prev.parentNode.removeChild(prev);
 var mount=function(){
  var g=document.createElement('img');
  g.className='fm-ghost'; g.alt='';
  g.setAttribute('src',src);
  host.appendChild(g);
  requestAnimationFrame(function(){
   g.classList.add('in');
   setTimeout(function(){
    im.setAttribute('src',src); im.style.opacity=1;
    requestAnimationFrame(function(){ if(g.parentNode)g.parentNode.removeChild(g); });
   },340);
  });
 };
 var done=false, run=function(){ if(done)return; done=true; mount(); };
 var pic=new Image(); pic.src=src;
 if(pic.complete){run();}
 else if(pic.decode){ pic.decode().then(run).catch(run); setTimeout(run,700); }
 else { pic.onload=run; pic.onerror=run; setTimeout(run,700); }
}
document.addEventListener('toggle',function(e){
 const d=e.target;
 if(!d.matches||!d.matches('#fm-makes details.mk'))return;
 if(d.open){
  document.querySelectorAll('#fm-makes details.mk').forEach(x=>{if(x!==d)x.open=false});
  const t=d.querySelector('summary span').textContent.trim();
  swapImg(DP[t]||baseImg);
 } else {
  const anyOpen=[...document.querySelectorAll('#fm-makes details.mk')].some(x=>x.open);
  if(!anyOpen)swapImg(baseImg);
 }
},true);

var FLMAP={
 "Detox":[[0,4],[2,1]],
 "Revive":[[0,3],[2,2]],
 "Energy":[[0,5]],
 "Consciousness":[[0,6],[3,0]],
 "Fresh":[[0,0],[1,0],[2,3],[3,2]],
 "Desertea":[[0,2],[1,1],[2,0],[3,1]],
 "Calm":[[0,1]],
 "Namastea":[[1,2],[4,4],[7,0],[7,1],[7,2],[7,3],[7,4],[7,5],[8,0],[8,1],[8,2],[8,3],[9,3]],
 "Matcha":[[4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[5,0],[5,1],[5,2],[5,3],[5,4],[6,0],[6,1],[6,2],[6,3],[6,4],[9,4]],
 "Ube":[[9,0],[9,1],[9,2],[9,3],[9,4]]
};
function fmDrinkImg(ci,di){
 try{ var k=ci+':'+di;
  if(typeof DPHOTO!=='undefined'&&DPHOTO[k])return DPHOTO[k];
  var sc=(typeof CHAPTER_SCENES!=='undefined')?CHAPTER_SCENES[ci]:null;
  return sc?sc.url:'';
 }catch(e){return ''}
}
function renderMakesCols(n){
 var box=document.getElementById('fm-makes'), map=FLMAP[n];
 if(!map||typeof COLS==='undefined')return false;
 var h='<h6>Menu drinks it makes \u2014 tap to open the recipe</h6><div class="mkgo-list">';
 var cnt=0;
 map.forEach(function(pair){
  var c=COLS[pair[0]]; if(!c)return; var d=c.drinks[pair[1]]; if(!d)return; cnt++;
  h+='<a class="mkgo" href="#!" data-ci="'+pair[0]+'" data-di="'+pair[1]+'">'
   + '<span class="nm">'+dn(d)+'<em>'+c.t+'</em></span>'
   + '<i>\u20aa'+d.p+' \u00b7 <b>'+d.m+'%</b><u>\u2192</u></i></a>';
 });
 if(!cnt)return false;
 h+='</div>';
 if(typeof MKMORE!=='undefined'&&MKMORE[n])h+='<div class="mkmore">'+MKMORE[n]+'</div>';
 box.innerHTML=h;
 box.querySelectorAll('a.mkgo').forEach(function(a){
  var ci=+a.getAttribute('data-ci'), di=+a.getAttribute('data-di');
  var pu=fmDrinkImg(ci,di); if(pu)fmPreload(pu);
  a.addEventListener('mouseenter',function(){ if(pu)swapImg(pu);});
  a.addEventListener('click',function(e){e.preventDefault();
   document.getElementById('fmodal').classList.remove('open');
   cmOpen(ci); cmI=di; cmRender();});
 });
 box.addEventListener('mouseleave',function(){swapImg(baseImg);});
 return true;
}
function openF(c){
 try{
  const n=c.querySelector('h4').textContent.trim();
  baseImg=(FSCENE[c.id]||c.querySelector('.ph img').src);document.getElementById('fm-img').src=baseImg;document.getElementById('fm-img').style.opacity=1;
  const o=c.querySelector('.origin');document.getElementById('fm-origin').textContent=o?o.textContent:'';
  document.getElementById('fm-name').textContent=n;
  const cp=c.querySelector('.comp');document.getElementById('fm-comp').textContent=cp?cp.textContent:'';
  const ln=c.querySelector('.liner');
  document.getElementById('fm-text').textContent=FL[n]||(ln?ln.textContent:'');
  const pr=c.querySelector('.prow'),mp=document.querySelector('#fmodal .prow');
  if(pr&&mp)mp.innerHTML=pr.innerHTML;
  const POUCH=window.POUCH;
  const fa=document.querySelector('#fmodal .facts');
  if(fa)fa.style.display=POUCH.indexOf(c.id)>-1?'none':'flex';
  try{if(!renderMakesCols(n)){POUCH.indexOf(c.id)>-1?renderMakesPouch(n):renderMakes(n);}}catch(e){try{POUCH.indexOf(c.id)>-1?renderMakesPouch(n):renderMakes(n);}catch(e2){}}
 }catch(e){}
 document.getElementById('fmodal').classList.add('open');
}
window.openF=openF;

function ddGo(e,id){e.preventDefault();const el=document.getElementById(id);if(!el)return;
 if(el.scrollIntoView)el.scrollIntoView({behavior:'smooth',block:'center'});
 setTimeout(()=>{try{openF(el)}catch(_){}},650);}
window.ddGo=ddGo;

document.addEventListener('click',function(e){
 const c=e.target.closest?e.target.closest('.fcard'):null;
 if(c && !c.id.startsWith('p-')){e.preventDefault();openF(c);}
});
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.getElementById('fmodal').classList.remove('open')});
const COLS=[{"n": "01", "t": "חליטות קרות", "he": "חליטות קרות", "p": "₪20", "drinks": [{"en": "Fresh", "he": "חליטת היביסקוס וליים", "d": "חליטת היביסקוס וליים, רגילה או מוגזת, עם לימון ונענע", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים ל־⅔ במים קרים (או סודה)", "קישוט: פרוסת לימון · נענע טרייה"], "ing": ["קרח", "50 מ״ל תרכיז GT", "פרוסת לימון", "עשבי קישוט"], "fc": "3.25", "p": 20, "m": 81, "pr": "13.70"}, {"en": "Calm", "he": "חליטת קמומיל ותפוח", "d": "קמומיל, תפוח וציפורן · בלי קפאין, מרגיע", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים ל־⅔ במים קרים (או סודה)", "קישוט: פרוסת לימון · אזוב או נענע"], "ing": ["קרח", "50 מ״ל תרכיז GT", "פרוסת לימון", "עשבי קישוט"], "fc": "3.25", "p": 20, "m": 81, "pr": "13.70"}, {"en": "Desertea", "he": "חליטה מדברית", "d": "לואיזה, נענע, אזוב, מרווה וזוטה לבנה · בלי קפאין", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים ל־⅔ במים קרים (או סודה)", "קישוט: פרוסת לימון · תערובת תבלינים"], "ing": ["קרח", "50 מ״ל תרכיז GT", "פרוסת לימון", "עשבי קישוט"], "fc": "3.25", "p": 20, "m": 81, "pr": "13.70"}, {"en": "Revive", "he": "חליטת סנצ'ה ופסיפלורה", "d": "סנצ׳ה יפני ופסיפלורה · עם קפאין, מרענן", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים ל־⅔ במים קרים (או סודה)", "קישוט: פרוסת לימון · רוזמרין"], "ing": ["קרח", "50 מ״ל תרכיז GT", "פרוסת לימון", "עשבי קישוט"], "fc": "3.25", "p": 20, "m": 81, "pr": "13.70"}, {"en": "Detox", "he": "חליטת תה ירוק לואיזה וליים", "d": "תה ירוק, לואיזה, נענע וליים", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים ל־⅔ במים קרים (או סודה)", "קישוט: פרוסת לימון · נענע טרייה"], "ing": ["קרח", "50 מ״ל תרכיז GT", "פרוסת לימון", "עשבי קישוט"], "fc": "3.25", "p": 20, "m": 81, "pr": "13.70"}, {"en": "Energy", "he": "חליטת תה ירוק ולמון גראס", "d": "תה ירוק, למון גראס, נענע ולימון", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים ל־⅔ במים קרים (או סודה)", "קישוט: פרוסת לימון · בזיליקום"], "ing": ["קרח", "50 מ״ל תרכיז GT", "פרוסת לימון", "עשבי קישוט"], "fc": "3.25", "p": 20, "m": 81, "pr": "13.70"}, {"en": "Consciousness", "he": "חליטת יסמין וליצ'י", "d": "תה יסמין וליצ׳י — רגיל או מוגז, ארומטי ועדין", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים ל־⅔ במים קרים (או סודה)", "קישוט: פרוסת לימון · נענע טרייה"], "ing": ["קרח", "50 מ״ל תרכיז GT", "פרוסת לימון", "עשבי קישוט"], "fc": "3.25", "p": 20, "m": 81, "pr": "13.70"}], "ac": "var(--terra)"}, {"n": "02", "t": "לימונדות", "he": "לימונדות", "p": "₪22", "drinks": [{"en": "לימונדת Fresh", "he": "לימונדת היביסקוס וליים", "d": "לימונדת היביסקוס וליים מרעננת", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים עד למעלה בלימונדה", "מערבבים בעדינות ומגישים"], "ing": ["קרח", "50 מ״ל תרכיז GT", "~250 מ״ל לימונדה"], "fc": "3.95", "p": 22, "m": 79, "pr": "14.69"}, {"en": "לימונדה מדברית", "he": "לימונדה מדברית", "d": "לימונדה על צמחי בר ישראליים", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים עד למעלה בלימונדה", "מערבבים בעדינות ומגישים"], "ing": ["קרח", "50 מ״ל תרכיז GT", "~250 מ״ל לימונדה"], "fc": "3.95", "p": 22, "m": 79, "pr": "14.69"}, {"en": "לימונדת Namastea", "he": "לימונדת צ'אי מסאלה", "d": "לימונדה על צ׳אי מסאלה", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז GT", "משלימים עד למעלה בלימונדה", "מערבבים בעדינות ומגישים"], "ing": ["קרח", "50 מ״ל תרכיז GT", "~250 מ״ל לימונדה"], "fc": "3.95", "p": 22, "m": 79, "pr": "14.69"}], "ac": "var(--energy)"}, {"n": "03", "t": "משקאות הדגל", "he": "משקאות הדגל", "p": "₪24–31", "drinks": [{"en": "מדברי אפרסק", "he": "חליטת אפרסק מדברית", "d": "משקה דגל על מחית אפרסק", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית אפרסק", "מוסיפים 40 מ״ל תרכיז GT", "מוסיפים מים", "מקשטים לפי הטעם"], "ing": ["קרח", "40 מ״ל מחית אפרסק", "40 מ״ל תרכיז GT", "קישוט"], "fc": "4.80", "p": 31, "m": 82, "pr": "21.47"}, {"en": "Detox תות", "he": "חליטת תות לואיזה", "d": "משקה דגל על מחית תות", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית תות", "מוסיפים 40 מ״ל תרכיז GT", "משלימים ל־⅔ במים", "מקשטים לפי הטעם"], "ing": ["קרח", "40 מ״ל מחית תות", "40 מ״ל תרכיז GT", "קישוט"], "fc": "4.80", "p": 31, "m": 82, "pr": "21.47"}, {"en": "Revive מנגו", "he": "חליטת מנגו סנצ'ה", "d": "משקה דגל על מנגו", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית מנגו", "מוסיפים 40 מ״ל תרכיז GT", "משלימים ל־⅔ במים", "מקשטים לפי הטעם"], "ing": ["קרח", "40 מ״ל מחית מנגו", "40 מ״ל תרכיז GT", "קישוט"], "fc": "4.80", "p": 31, "m": 82, "pr": "21.47"}, {"en": "Fresh תפוח", "he": "חליטת תפוח היביסקוס", "d": "משקה דגל על מיץ תפוחים", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מיץ תפוחים", "מוסיפים 40 מ״ל תרכיז GT", "משלימים ל־⅔ במים", "מקשטים לפי הטעם"], "ing": ["קרח", "40 מ״ל מיץ תפוחים", "40 מ״ל תרכיז GT", "קישוט"], "fc": "2.88", "p": 24, "m": 86, "pr": "17.46"}], "ac": "var(--revive)"}, {"n": "04", "t": "גזוז", "he": "גזוז", "p": "₪22–33", "drinks": [{"en": "Consciousness ליצ׳י", "he": "גזוז יסמין וליצ'י", "d": "גזוז תה יסמין וליצ׳י עם ליצ׳י טרי", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מי ליצ׳י", "מוסיפים 40 מ״ל תרכיז GT", "משלימים ל־⅔ בסודה (כ־150 מ״ל)", "קישוט: 2 ליצ׳י"], "ing": ["קרח", "40 מ״ל מי ליצ׳י", "40 מ״ל תרכיז GT", "~150 מ״ל סודה", "2 ליצ׳י"], "fc": "3.08", "p": 25, "m": 85, "pr": "18.11"}, {"en": "גזוז מדברי אפרסק", "he": "גזוז מדברי ואפרסק", "d": "גזוז צמחי בר ואפרסק", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית אפרסק", "מוסיפים 40 מ״ל תרכיז GT", "משלימים ל־⅔ בסודה (כ־150 מ״ל)", "מקשטים לפי הטעם"], "ing": ["קרח", "40 מ״ל מחית אפרסק", "40 מ״ל תרכיז GT", "~150 מ״ל סודה"], "fc": "4.80", "p": 33, "m": 83, "pr": "23.17"}, {"en": "גזוז Fresh תפוח", "he": "גזוז היביסקוס ותפוח", "d": "גזוז היביסקוס עם מיץ תפוחים", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מיץ תפוחים", "מוסיפים 40 מ״ל תרכיז GT", "משלימים ל־⅔ בסודה (כ־150 מ״ל)", "מקשטים לפי הטעם"], "ing": ["קרח", "40 מ״ל מיץ תפוחים", "40 מ״ל תרכיז GT", "~150 מ״ל סודה"], "fc": "2.88", "p": 22, "m": 85, "pr": "15.76"}], "ac": "#7FA8B8"}, {"n": "05", "t": "אייס מאצ׳ה", "he": "אייס מאצ'ה", "p": "₪26–39", "drinks": [{"en": "Classic", "he": "אייס מאצ'ה קלאסי", "d": "אייס מאצ׳ה קלאסי", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "70 מ״ל קצף חלב"], "fc": "4.26", "p": 26, "m": 81, "pr": "17.77"}, {"en": "Mango", "he": "אייס מאצ'ה מנגו", "d": "אייס מאצ׳ה מנגו", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית מנגו", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "40 מ״ל מחית מנגו", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "70 מ״ל קצף חלב"], "fc": "6.46", "p": 39, "m": 80, "pr": "26.59"}, {"en": "Strawberry", "he": "אייס מאצ'ה תות", "d": "אייס מאצ׳ה מחית תות", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית תות", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "40 מ״ל מחית תות", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "70 מ״ל קצף חלב"], "fc": "6.46", "p": 39, "m": 80, "pr": "26.59"}, {"en": "Peach", "he": "אייס מאצ'ה אפרסק", "d": "אייס מאצ׳ה מחית אפרסק", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית אפרסק", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "40 מ״ל מחית אפרסק", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "70 מ״ל קצף חלב"], "fc": "6.46", "p": 39, "m": 80, "pr": "26.59"}, {"en": "Massala", "he": "אייס מאצ'ה מסאלה", "d": "אייס מאצ׳ה עם תרכיז מסאלה GT", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל תרכיז מסאלה GT", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "40 מ״ל תרכיז מסאלה GT", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "70 מ״ל קצף חלב"], "fc": "6.86", "p": 37, "m": 78, "pr": "24.50"}, {"en": "אגבה על קרח", "he": "מאצ'ה אגבה על הקרח", "d": "אייס מאצ׳ה קליל עם אגבה על קרח", "st": ["ממלאים את הכוס בקרח", "מוסיפים 15 מ״ל סירופ אגבה", "משלימים ל־⅔ במים", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "⅔ כוס מים", "15 מ״ל סירופ אגבה", "50 מ״ל מאצ׳ה (1.8 גרם)", "70 מ״ל קצף חלב"], "fc": "2.85", "p": 26, "m": 87, "pr": "19.18"}], "ac": "var(--matcha)"}, {"n": "06", "t": "מאצ׳ה ספיישל", "he": "מאצ'ה — טעמים מיוחדים", "p": "₪28–29", "drinks": [{"en": "Vanilla", "he": "אייס מאצ'ה וניל", "d": "אייס מאצ׳ה וניל", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים מקל וניל", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "מקל וניל", "70 מ״ל קצף חלב"], "fc": "4.56", "p": 28, "m": 81, "pr": "19.17"}, {"en": "Pistachio", "he": "אייס מאצ'ה פיסטוק", "d": "אייס מאצ׳ה פיסטוק", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים פיסטוק גרוס", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "פיסטוק גרוס", "70 מ״ל קצף חלב"], "fc": "5.46", "p": 28, "m": 77, "pr": "18.27"}, {"en": "שומשום שחור", "he": "אייס מאצ'ה שומשום שחור", "d": "אייס מאצ׳ה שומשום שחור", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים שומשום שחור", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "שומשום שחור", "70 מ״ל קצף חלב"], "fc": "5.06", "p": 28, "m": 79, "pr": "18.67"}, {"en": "Coffee", "he": "אייס מאצ'ה קפה", "d": "אייס מאצ׳ה קפה", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים שוט אספרסו", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "שוט אספרסו", "70 מ״ל קצף חלב"], "fc": "5.26", "p": 29, "m": 79, "pr": "19.32"}, {"en": "Banana", "he": "אייס מאצ'ה בננה", "d": "אייס מאצ׳ה בננה", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "מוסיפים מחית בננה", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מאצ׳ה (1.8 גרם)", "מחית בננה", "70 מ״ל קצף חלב"], "fc": "4.76", "p": 28, "m": 80, "pr": "18.97"}], "ac": "#8C8C7A"}, {"n": "07", "t": "מאצ׳ה קוקוס", "he": "מאצ'ה קוקוס", "p": "₪32–44", "drinks": [{"en": "אגבה קלאסי", "he": "מאצ'ה קוקוס אגבה", "d": "מאצ׳ה קוקוס אגבה קלאסי", "st": ["ממלאים את הכוס בקרח", "מוסיפים 15 מ״ל סירופ אגבה", "משלימים ל־⅔ במי קוקוס (כ־150 מ״ל)", "מוסיפים קרם קוקוס (70 מ״ל)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)"], "ing": ["קרח", "15 מ״ל סירופ אגבה", "~150 מ״ל מי קוקוס", "70 מ״ל קרם קוקוס", "50 מ״ל מאצ׳ה (1.8 גרם)"], "fc": "4.04", "p": 34, "m": 86, "pr": "24.77"}, {"en": "Lychee", "he": "מאצ'ה קוקוס ליצ'י", "d": "מאצ׳ה קוקוס ליצ׳י", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מי ליצ׳י", "משלימים ל־⅔ במי קוקוס (כ־150 מ״ל)", "מוסיפים קרם קוקוס (70 מ״ל)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)"], "ing": ["קרח", "40 מ״ל מי ליצ׳י", "~150 מ״ל מי קוקוס", "70 מ״ל קרם קוקוס", "50 מ״ל מאצ׳ה (1.8 גרם)"], "fc": "4.07", "p": 32, "m": 85, "pr": "23.05"}, {"en": "Strawberry", "he": "מאצ'ה קוקוס תות", "d": "מאצ׳ה קוקוס תות", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית תות", "משלימים ל־⅔ במי קוקוס (כ־150 מ״ל)", "מוסיפים קרם קוקוס (70 מ״ל)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)"], "ing": ["קרח", "40 מ״ל מחית תות", "~150 מ״ל מי קוקוס", "70 מ״ל קרם קוקוס", "50 מ״ל מאצ׳ה (1.8 גרם)"], "fc": "5.79", "p": 44, "m": 84, "pr": "31.50"}, {"en": "Mango", "he": "מאצ'ה קוקוס מנגו", "d": "מאצ׳ה קוקוס מנגו", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית מנגו", "משלימים ל־⅔ במי קוקוס (כ־150 מ״ל)", "מוסיפים קרם קוקוס (70 מ״ל)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)"], "ing": ["קרח", "40 מ״ל מחית מנגו", "~150 מ״ל מי קוקוס", "70 מ״ל קרם קוקוס", "50 מ״ל מאצ׳ה (1.8 גרם)"], "fc": "5.79", "p": 44, "m": 84, "pr": "31.50"}, {"en": "Peach", "he": "מאצ'ה קוקוס אפרסק", "d": "מאצ׳ה קוקוס אפרסק", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית אפרסק", "משלימים ל־⅔ במי קוקוס (כ־150 מ״ל)", "מוסיפים קרם קוקוס (70 מ״ל)", "מוזגים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)"], "ing": ["קרח", "40 מ״ל מחית אפרסק", "~150 מ״ל מי קוקוס", "70 מ״ל קרם קוקוס", "50 מ״ל מאצ׳ה (1.8 גרם)"], "fc": "5.79", "p": 44, "m": 84, "pr": "31.50"}], "ac": "#5FA89B"}, {"n": "08", "t": "צ׳אי מסאלה", "he": "צ'אי מסאלה", "p": "₪24–32", "drinks": [{"en": "אייס מסאלה קלאסי", "he": "אייס צ'אי מסאלה קלאסי", "d": "צ׳אי מסאלה עשיר עם קצף חלב וקינמון", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל תרכיז מסאלה GT", "מוסיפים קצף חלב", "מפזרים קינמון"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מסאלה GT", "70 מ״ל קצף חלב", "קינמון"], "fc": "5.57", "p": 28, "m": 77, "pr": "18.16"}, {"en": "על קרח", "he": "צ'אי מסאלה על הקרח", "d": "צ׳אי מסאלה קליל ומרענן על מים", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ במים", "מוזגים 50 מ״ל תרכיז מסאלה GT", "מוסיפים קצף חלב נדיב"], "ing": ["קרח", "⅔ כוס מים", "50 מ״ל מסאלה GT", "70 מ״ל קצף חלב"], "fc": "3.70", "p": 24, "m": 82, "pr": "16.64"}, {"en": "דירטי צ׳אי", "he": "דירטי צ'אי", "d": "צ׳אי מסאלה עם שוט אספרסו וקצף חלב עשיר", "st": ["מכינים שוט אספרסו", "ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב", "מוזגים 50 מ״ל מסאלה GT + האספרסו", "מוסיפים קצף חלב נדיב"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מסאלה GT", "שוט אספרסו", "70 מ״ל קצף חלב"], "fc": "6.57", "p": 32, "m": 76, "pr": "20.55"}, {"en": "טוניק תפוז מיובש", "he": "צ'אי מסאלה תפוז וטוניק", "d": "צ׳אי מסאלה מוגז עם טוניק ותפוז מיובש", "st": ["ממלאים את הכוס בקרח", "מוזגים 50 מ״ל תרכיז מסאלה GT", "משלימים בטוניק (כ־150 מ״ל)", "מקשטים בפרוסת תפוז מיובש"], "ing": ["קרח", "50 מ״ל מסאלה GT", "~150 מ״ל טוניק", "תפוז מיובש"], "fc": "4.75", "p": 26, "m": 78, "pr": "17.28"}, {"en": "טוניק ורדים ורוד", "he": "צ'אי מסאלה פינק טוניק", "d": "צ׳אי מסאלה עם טוניק ורדים או אשכוליות", "st": ["ממלאים את הכוס בקרח", "מוזגים 50 מ״ל תרכיז מסאלה GT", "משלימים בטוניק ורדים או אשכוליות (כ־150 מ״ל)"], "ing": ["קרח", "50 מ״ל מסאלה GT", "~150 מ״ל טוניק ורדים"], "fc": "4.75", "p": 24, "m": 77, "pr": "15.59"}, {"en": "מיץ תפוזים", "he": "צ'אי מסאלה ומיץ תפוזים", "d": "צ׳אי מסאלה עם מיץ תפוזים סחוט", "st": ["ממלאים את הכוס בקרח", "מוזגים 50 מ״ל תרכיז מסאלה GT", "משלימים במיץ תפוזים סחוט (כ־150 מ״ל)"], "ing": ["קרח", "50 מ״ל מסאלה GT", "~150 מ״ל מיץ תפוזים"], "fc": "5.25", "p": 28, "m": 78, "pr": "18.48"}], "ac": "var(--nama)"}, {"n": "09", "t": "קולד פואם", "he": "צ'אי מסאלה קולד פואם", "p": "₪28–32", "drinks": [{"en": "Vanilla", "he": "צ'אי מסאלה קולד פואם וניל", "d": "צ׳אי מסאלה עם קצף קר וניל", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ במים", "מוזגים 50 מ״ל תרכיז מסאלה GT", "מכתירים בקצף קר וניל", "מקשטים במקל וניל"], "ing": ["קרח", "⅔ כוס מים", "50 מ״ל מסאלה GT", "70 מ״ל קצף קר", "תמצית וניל"], "fc": "4.00", "p": 28, "m": 83, "pr": "19.73"}, {"en": "Pistachio", "he": "צ'אי מסאלה קולד פואם פיסטוק", "d": "צ׳אי מסאלה עם קצף קר ופיסטוק גרוס", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב", "מוזגים 50 מ״ל תרכיז מסאלה GT", "מכתירים בקצף קר חלבי", "מפזרים פיסטוק גרוס"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מסאלה GT", "70 מ״ל קצף קר", "פיסטוק גרוס"], "fc": "4.90", "p": 30, "m": 81, "pr": "20.52"}, {"en": "קוקוס תאילנדי", "he": "צ'אי תאילנדי קוקוס קולד פואם", "d": "צ׳אי מסאלה עם קצף קר קוקוס, בסגנון תאילנדי", "st": ["ממלאים את הכוס בקרח", "משלימים במי קוקוס (כ־150 מ״ל)", "מוזגים 50 מ״ל תרכיז מסאלה GT", "מכתירים בקצף קר קוקוס (70 מ״ל)"], "ing": ["קרח", "~150 מ״ל מי קוקוס", "50 מ״ל מסאלה GT", "70 מ״ל קרם קוקוס"], "fc": "4.90", "p": 32, "m": 82, "pr": "22.22"}, {"en": "Banana", "he": "צ'אי מסאלה קולד פואם בננה", "d": "צ׳אי מסאלה עם קצף קר בננה", "st": ["ממלאים את הכוס בקרח", "משלימים ל־⅔ בחלב", "מוזגים 50 מ״ל מסאלה GT + מחית בננה", "מכתירים בקצף קר חלבי"], "ing": ["קרח", "⅔ כוס חלב", "50 מ״ל מסאלה GT", "מחית בננה", "70 מ״ל קצף קר"], "fc": "4.20", "p": 31, "m": 84, "pr": "22.07"}], "ac": "#B0793B"}, {"n": "10", "t": "אובה", "he": "אובה", "p": "₪28–31", "drinks": [{"en": "Strawberry", "he": "אייס אובה תות", "d": "אייס אובה תות", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית תות", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל אובה מוכן (2 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "40 מ״ל מחית תות", "⅔ כוס חלב", "50 מ״ל אובה (2 גרם)", "70 מ״ל קצף חלב"], "fc": "5.22", "p": 30, "m": 79, "pr": "20.20"}, {"en": "Mango", "he": "אייס אובה מנגו", "d": "אייס אובה מנגו", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית מנגו", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל אובה מוכן (2 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "40 מ״ל מחית מנגו", "⅔ כוס חלב", "50 מ״ל אובה (2 גרם)", "70 מ״ל קצף חלב"], "fc": "5.22", "p": 30, "m": 79, "pr": "20.20"}, {"en": "Peach", "he": "אייס אובה אפרסק", "d": "אייס אובה אפרסק", "st": ["ממלאים את הכוס בקרח", "מוסיפים 40 מ״ל מחית אפרסק", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל אובה מוכן (2 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "40 מ״ל מחית אפרסק", "⅔ כוס חלב", "50 מ״ל אובה (2 גרם)", "70 מ״ל קצף חלב"], "fc": "5.22", "p": 30, "m": 79, "pr": "20.20"}, {"en": "Massala", "he": "אייס אובה מסאלה", "d": "אייס אובה מסאלה", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל תרכיז מסאלה GT", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל אובה מוכן (2 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "50 מ״ל מסאלה GT", "⅔ כוס חלב", "50 מ״ל אובה (2 גרם)", "70 מ״ל קצף חלב"], "fc": "6.27", "p": 31, "m": 76, "pr": "20.00"}, {"en": "Matcha", "he": "אייס אובה מאצ'ה", "d": "אייס אובה מאצ׳ה", "st": ["ממלאים את הכוס בקרח", "מוסיפים 50 מ״ל מאצ׳ה מוכן (1.8 גרם אבקה)", "משלימים ל־⅔ בחלב (או חלב צמחי)", "מוזגים 50 מ״ל אובה מוכן (2 גרם אבקה)", "מוסיפים קצף חלב מלמעלה"], "ing": ["קרח", "50 מ״ל מאצ׳ה (1.8 גרם)", "⅔ כוס חלב", "50 מ״ל אובה (2 גרם)", "70 מ״ל קצף חלב"], "fc": "4.96", "p": 28, "m": 79, "pr": "18.77"}], "ac": "var(--ube)"}];

let cmC=0,cmI=0;

var DFCOL={"Detox":"#D8492B","Revive":"#0FA3A3","Energy":"#4B3B8F","Consciousness":"#C2185B","American":"#C62828",
"Fresh":"#A31F34","Desertea":"#D9A413","Calm":"#8E7CC3","Namastea":"#C98A2D","Matcha":"#5F8F4E","Ube":"#7C5CBF","Hojicha":"#A9752E"};
function buildMatrix(){
 var box=document.getElementById('mx'); if(!box||typeof FLMAP==='undefined')return;
 var NOTE={"American":"בסיס למשקה דגל — משתלב עם מחיות אפרסק ומנגו של ODK.",
           "Hojicha":"מוגש חם או קר כלאטה. עדיין בלי מתכוני תפריט."};
 var h='';
 Object.keys(FLCARD).forEach(function(p){
  var pairs=FLMAP[p]||[];
  var muted=pairs.length?'':' muted';
  h+='<div class="mxc'+muted+'"><div class="hd"><i class="pd" style="background:'+(DFCOL[p]||'#ccc')+'"></i>'
    +'<span class="pn">'+p+'</span><span class="pc">'+(pairs.length?pairs.length+(pairs.length===1?' drink':' drinks'):'\u2014')+'</span></div>';
  if(!pairs.length){ h+='<div class="note">'+(NOTE[p]||'No menu drinks yet.')+'</div></div>'; return; }
  var byCh={},order=[];
  pairs.forEach(function(pr){ if(!byCh[pr[0]]){byCh[pr[0]]=[];order.push(pr[0]);} byCh[pr[0]].push(pr[1]); });
  order.forEach(function(ci){
   h+='<div class="grp"><span class="gl">'+COLS[ci].t+'</span><div class="chips">';
   byCh[ci].forEach(function(di){
    h+='<button class="mxd" data-ci="'+ci+'" data-di="'+di+'">'+dn(COLS[ci].drinks[di])+'</button>';
   });
   h+='</div></div>';
  });
  h+='</div>';
 });
 box.innerHTML=h;
 box.querySelectorAll('.mxd').forEach(function(b){
  b.addEventListener('click',function(){cmOpen(+b.getAttribute('data-ci'));cmI=+b.getAttribute('data-di');cmRender();});
 });
}
function heroSwipe(){
 var el=document.querySelector('.hs')||document.querySelector('#hero'); if(!el)return;
 var x0=null;
 el.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
 el.addEventListener('touchend',function(e){
  if(x0===null)return; var dx=e.changedTouches[0].clientX-x0; x0=null;
  if(Math.abs(dx)<45)return;
  if(typeof hsGo==='function'){hsGo(dx<0?hsI+1:hsI-1); if(typeof hsRestart==='function')hsRestart();}
 },{passive:true});
}
function cmOpen(ci){cmC=ci;cmI=0;cmRender();document.getElementById('cmodal').classList.add('open');}
function cmClose(){document.getElementById('cmodal').classList.remove('open');}
function cmGo(d){const n=COLS[cmC].drinks.length;cmI=Math.min(n-1,Math.max(0,cmI+d));cmRender();}

// ==== SVG-инфографика стакана со слоями состава ====
const LAYER_MAP=[
 [/\u05e7\u05e6\u05e3|cold foam|\u05e7\u05e8\u05dd \u05e7\u05d5\u05e7\u05d5\u05e1/, '#FFF6EA', 'foam'],   // קצף / крем кокос -> пена
 [/\u05de\u05d0\u05e6['\u05f3]?\u05d4/, '#5FA34C', 'top'],        // מאצ'ה
 [/\u05d0\u05d5\u05d1\u05d4/, '#7B5CC6', 'top'],                    // אובה
 [/\u05de\u05e1\u05d0\u05dc\u05d4/, '#9A6633', 'mid'],             // מסאלה
 [/\u05ea\u05e8\u05db\u05d9\u05d6 GT|\u05ea\u05de\u05e6\u05d9\u05ea GT/, '#C98A2D', 'mid'], // тмицит GT
 [/\u05de\u05e0\u05d2\u05d5/, '#F0A63A', 'bottom'],                 // מנגו
 [/\u05ea\u05d5\u05ea/, '#D8203F', 'bottom'],                        // תות
 [/\u05d0\u05e4\u05e8\u05e1\u05e7/, '#F2A57C', 'bottom'],          // אפרסק
 [/\u05dc\u05d9\u05e6['\u05f3]?\u05d9/, '#F3E3E9', 'bottom'],      // ליצ'י
 [/\u05d0\u05d2\u05d1\u05d4/, '#E5C55A', 'bottom'],                 // אגבה
 [/\u05d0\u05e1\u05e4\u05e8\u05e1\u05d5/, '#4A2E1E', 'mid'],      // אספרסו
 [/\u05de\u05d9\u05e5 \u05ea\u05e4\u05d5\u05d6\u05d9\u05dd/, '#F08A24', 'fill'], // מיץ תפוזים
 [/\u05dc\u05d9\u05de\u05d5\u05e0\u05d3\u05d4/, '#F5E27A', 'fill'], // לימונדה
 [/\u05d8\u05d5\u05e0\u05d9\u05e7/, '#EAF2F0', 'fill'],            // טוניק
 [/\u05e1\u05d5\u05d3\u05d4/, '#E8F1F5', 'fill'],                   // סודה
 [/\u05de\u05d9 \u05e7\u05d5\u05e7\u05d5\u05e1/, '#F4F0E4', 'fill'], // מי קוקוס
 [/\u05d7\u05dc\u05d1/, '#F6EFE2', 'fill'],                          // חלב
 [/\u05de\u05d9\u05dd/, '#E8F1F5', 'fill'],                          // מים
];
function glassSVG(ing, accent){
 // раскладка: fill-слои снизу вверх, bottom-слои у дна, mid середина, top сверху, foam шапка
 const layers=[];
 ing.forEach(t=>{ if(/\u05e7\u05e8\u05d7/.test(t)) return; // лёд отдельно
   for(const [re,color,kind] of LAYER_MAP){ if(re.test(t)){ layers.push({color,kind}); return; } } });
 const order={bottom:0,fill:1,mid:2,top:3};
 const body=layers.filter(l=>l.kind!=='foam').sort((a,b)=>order[a.kind]-order[b.kind]);
 const foam=layers.find(l=>l.kind==='foam');
 const X=18,W=60,BOT=118,TOPY=30, H=BOT-TOPY;
 let svg='<svg viewBox="0 0 96 132" xmlns="http://www.w3.org/2000/svg">';
 // жидкости
 if(body.length){ const lh=H/body.length;
   body.forEach((l,i)=>{ const y=BOT-lh*(i+1);
     svg+=`<rect x="${X+3}" y="${y.toFixed(1)}" width="${W-6}" height="${(lh+0.6).toFixed(1)}" fill="${l.color}" opacity="0.92"/>`; });
 } else { svg+=`<rect x="${X+3}" y="${TOPY}" width="${W-6}" height="${H}" fill="${accent}" opacity="0.35"/>`; }
 if(foam){ svg+=`<path d="M${X+3} ${TOPY+6} Q${X+13} ${TOPY-8} ${X+W/2} ${TOPY-2} Q${X+W-13} ${TOPY-9} ${X+W-3} ${TOPY+6} Z" fill="${foam.color}" stroke="#E8E0D0" stroke-width="1"/>`; }
 // кубики льда
 svg+=`<g fill="rgba(255,255,255,.5)" stroke="rgba(255,255,255,.85)" stroke-width="1.4">
 <rect x="${X+9}" y="${TOPY+14}" width="15" height="15" rx="3" transform="rotate(-12 ${X+16} ${TOPY+21})"/>
 <rect x="${X+32}" y="${TOPY+30}" width="15" height="15" rx="3" transform="rotate(9 ${X+39} ${TOPY+37})"/>
 <rect x="${X+15}" y="${TOPY+52}" width="14" height="14" rx="3" transform="rotate(-6 ${X+22} ${TOPY+59})"/></g>`;
 // контур стакана поверх
 svg+=`<path d="M${X} ${TOPY-10} L${X} ${BOT-6} Q${X} ${BOT} ${X+6} ${BOT} L${X+W-6} ${BOT} Q${X+W} ${BOT} ${X+W} ${BOT-6} L${X+W} ${TOPY-10}" fill="none" stroke="#20241F" stroke-width="2.4" stroke-linecap="round"/>`;
 svg+='</svg>';
 return svg;
}


// ==== реальные напитки: кроп своего стакана из сцены главы ====
const CHAPTER_SCENES={
 
 9:{url:(GT_ASSET_BASE+'gt-130f595fbd.webp'),n:5}
};


// одиночные сгенерированные стаканы напитков (пилот; заполняется волной)
const DPHOTO={"0:0":(GT_ASSET_BASE+"gt-2057456452.webp"),"0:1":(GT_ASSET_BASE+"gt-dbb6f70ab8.webp"),"0:2":(GT_ASSET_BASE+"gt-f2b0bded99.webp"),"0:3":(GT_ASSET_BASE+"gt-a8d86ef209.webp"),"0:4":(GT_ASSET_BASE+"gt-1b1a5fe6f0.webp"),"0:5":(GT_ASSET_BASE+"gt-1ef5ba754c.webp"),"0:6":(GT_ASSET_BASE+"gt-0a9c7c969a.webp"),"1:0":(GT_ASSET_BASE+"gt-c942631391.webp"),"1:1":(GT_ASSET_BASE+"gt-bf31374321.webp"),"1:2":(GT_ASSET_BASE+"gt-4445c6ab4a.webp"),"2:0":(GT_ASSET_BASE+"gt-39a9e89014.webp"),"2:1":(GT_ASSET_BASE+"gt-c30af31427.webp"),"2:2":(GT_ASSET_BASE+"gt-d1ca1a3dd5.webp"),"2:3":(GT_ASSET_BASE+"gt-a72027a9c6.webp"),"3:0":(GT_ASSET_BASE+"gt-2a0820440f.webp"),"3:1":(GT_ASSET_BASE+"gt-9a20a715c3.webp"),"3:2":(GT_ASSET_BASE+"gt-732cf0c401.webp"),"4:0":(GT_ASSET_BASE+"gt-8728800f85.webp"),"4:1":(GT_ASSET_BASE+"gt-c3872fdce0.webp"),"4:2":(GT_ASSET_BASE+"gt-cc4193ac56.webp"),"4:3":(GT_ASSET_BASE+"gt-de4bdcef66.webp"),"4:4":(GT_ASSET_BASE+"gt-9b5c14e199.webp"),"4:5":(GT_ASSET_BASE+"gt-f59f059ff2.webp"),"5:0":(GT_ASSET_BASE+"gt-d6a15a37c6.webp"),"5:1":(GT_ASSET_BASE+"gt-29868b6d41.webp"),"5:2":(GT_ASSET_BASE+"gt-fe76b1afa1.webp"),"5:3":(GT_ASSET_BASE+"gt-7565afcb24.webp"),"5:4":(GT_ASSET_BASE+"gt-5752efa538.webp"),"6:0":(GT_ASSET_BASE+"gt-e9f4e7fc38.webp"),"6:1":(GT_ASSET_BASE+"gt-63eac43d2d.webp"),"6:2":(GT_ASSET_BASE+"gt-b843ae6fca.webp"),"6:3":(GT_ASSET_BASE+"gt-ba6967c907.webp"),"6:4":(GT_ASSET_BASE+"gt-e7bf263165.webp"),"7:0":(GT_ASSET_BASE+"gt-7a2b44891b.webp"),"7:1":(GT_ASSET_BASE+"gt-8d26f09d17.webp"),"7:2":(GT_ASSET_BASE+"gt-36f43500ad.webp"),"7:3":(GT_ASSET_BASE+"gt-af10238dca.webp"),"7:4":(GT_ASSET_BASE+"gt-690f2e7dec.webp"),"7:5":(GT_ASSET_BASE+"gt-c6c2dd8d6b.webp"),"8:0":(GT_ASSET_BASE+"gt-676ae5224b.webp"),"8:1":(GT_ASSET_BASE+"gt-d35192636a.webp"),"8:2":(GT_ASSET_BASE+"gt-2b1babb40e.webp"),"8:3":(GT_ASSET_BASE+"gt-6e94247f32.webp"),"9:0":(GT_ASSET_BASE+"gt-7281b3e7a6.webp"),"9:1":(GT_ASSET_BASE+"gt-83ff7d7c09.webp"),"9:2":(GT_ASSET_BASE+"gt-9c1a90ccd8.webp"),"9:3":(GT_ASSET_BASE+"gt-e048d3f32b.webp"),"9:4":(GT_ASSET_BASE+"gt-ec3523c940.webp")};
const STEP_ICONS=[
 [/\u05e7\u05e8\u05d7|ice/i,'\ud83e\uddca','\u05e7\u05e8\u05d7'],
 [/\u05de\u05d0\u05e6['\u05f3]?\u05d4|matcha/i,'\ud83c\udf75','\u05de\u05d0\u05e6\u05f3\u05d4'],
 [/\u05d0\u05d5\u05d1\u05d4|ube/i,'\ud83c\udf60','\u05d0\u05d5\u05d1\u05d4'],
 [/\u05ea\u05e8\u05db\u05d9\u05d6 (\u05de\u05e1\u05d0\u05dc\u05d4 )?GT|\u05de\u05e1\u05d0\u05dc\u05d4 GT|GT (massala )?(concentrate|essence)|GT massala/i,'\ud83e\uddc9','GT 50 \u05de\u05f4\u05dc'],
 [/\u05e7\u05e6\u05e3|\u05e7\u05e8\u05dd \u05e7\u05d5\u05e7\u05d5\u05e1|milk foam|cold foam|foam|coconut cream/i,'\u2601\ufe0f','\u05e7\u05e6\u05e3'],
 [/\u05d7\u05dc\u05d1|milk/i,'\ud83e\udd5b','\u05d7\u05dc\u05d1'],
 [/\u05e1\u05d5\u05d3\u05d4|\u05d8\u05d5\u05e0\u05d9\u05e7|soda|tonic|sparkl/i,'\ud83e\udd64','\u05e1\u05d5\u05d3\u05d4'],
 [/\u05de\u05d9\u05dd|water/i,'\ud83d\udca7','\u05de\u05d9\u05dd'],
 [/\u05d0\u05e1\u05e4\u05e8\u05e1\u05d5|espresso|coffee/i,'\u2615','\u05d0\u05e1\u05e4\u05e8\u05e1\u05d5'],
 [/\u05d0\u05d2\u05d1\u05d4|agave/i,'\ud83c\udf6f','\u05d0\u05d2\u05d1\u05d4'],
 [/\u05de\u05e0\u05d2\u05d5|\u05ea\u05d5\u05ea|\u05d0\u05e4\u05e8\u05e1\u05e7|\u05dc\u05d9\u05e6['\u05f3]?\u05d9|\u05ea\u05e4\u05d5\u05d7|\u05d1\u05e0\u05e0\u05d4|\u05ea\u05e4\u05d5\u05d6|\u05dc\u05d9\u05de\u05d5\u05e0\u05d3\u05d4|\u05de\u05d9\u05e5|\u05e4\u05d9\u05e8\u05d4|mango|strawberry|peach|lychee|apple|banana|orange|lemonade|juice|pur\u00e9e/i,'\ud83c\udf53','\u05e4\u05e8\u05d9'],
 [/\u05de\u05e7\u05e9\u05d8|\u05e7\u05d9\u05e9\u05d5\u05d8|\u05de\u05e4\u05d6\u05e8|\u05de\u05db\u05ea\u05d9\u05e8|\u05de\u05e2\u05e8\u05d1|\u05d5\u05e0\u05d9\u05dc|\u05e4\u05d9\u05e1\u05d8\u05d5\u05e7|\u05e9\u05d5\u05de\u05e9\u05d5\u05dd|garnish|dust|sprinkle|crown|stir|vanilla|pistachio|sesame/i,'\ud83c\udf3f','\u05e1\u05d9\u05d5\u05dd'],
];
function buildRow(steps){
 const parts=[];
 steps.forEach(t=>{ for(const [re,ic,lb] of STEP_ICONS){ if(re.test(t)){ parts.push({ic,lb}); return; } } parts.push({ic:'\u2022',lb:''}); });
 return '<div class="cm-build">'+parts.map((p,i)=>(i?'<span class="sep">\u2192</span>':'')+'<span class="st"><i>'+p.ic+'</i><b>'+(i+1)+'. '+p.lb+'</b></span>').join('')+'</div>';
}


var FLCARD={"Detox":"f-detox","Revive":"f-revive","Energy":"f-energy","Consciousness":"f-consciousness",
 "American":"f-american","Fresh":"f-fresh","Desertea":"f-desertea","Calm":"f-calm","Namastea":"f-namastea",
 "Matcha":"f-matcha","Ube":"f-ube","Hojicha":"f-hojicha"};
function cmSources(ci,di){
 var out=[]; if(typeof FLMAP==='undefined')return out;
 for(var k in FLMAP){ (FLMAP[k]||[]).forEach(function(pr){
   if(pr[0]===ci&&pr[1]===di&&out.indexOf(k)<0)out.push(k); }); }
 return out;
}
function cmSrcRender(ci,di){
 var host=document.getElementById('cm-src');
 if(!host){ var dsc=document.getElementById('cm-desc'); if(!dsc)return;
  host=document.createElement('div'); host.id='cm-src'; host.className='cm-src';
  dsc.parentNode.insertBefore(host,dsc.nextSibling); }
 var srcs=cmSources(ci,di);
 if(!srcs.length){host.innerHTML='';host.style.display='none';return;}
 host.style.display='flex';
 host.innerHTML='<span class="lbl">על בסיס</span>'+srcs.map(function(n){
   return '<a href="#!" data-card="'+(FLCARD[n]||'')+'">'+n+' \u2190</a>'; }).join('');
 host.querySelectorAll('a').forEach(function(a){
  a.addEventListener('click',function(e){e.preventDefault();
   var el=document.getElementById(a.getAttribute('data-card')); if(!el)return;
   cmClose(); openF(el); });
 });
}

var cmPre={};
function cmPreload(u){ if(!u||cmPre[u])return; var i=new Image(); i.decoding='async'; i.src=u; cmPre[u]=1; }
function cmShow(cv,html,url){
 var apply=function(){
  cv.innerHTML=html;
  var rec=document.querySelector('#cmodal .cm-rec');
  if(rec){rec.classList.remove('cmrise'); void rec.offsetWidth; rec.classList.add('cmrise');}
 };
 if(!url){apply();return;}
 var done=false, run=function(){ if(done)return; done=true; apply(); };
 var im=new Image(); im.src=url;
 if(im.complete){run();return;}
 if(im.decode){ im.decode().then(run).catch(run); } else { im.onload=run; im.onerror=run; }
 setTimeout(run,700);
}
function cmPrefetchNear(){
 try{ var c=COLS[cmC], sc=CHAPTER_SCENES[cmC];
  [cmI-1,cmI+1,cmI+2].forEach(function(k){
   if(k<0||k>=c.drinks.length)return;
   cmPreload(DPHOTO[cmC+':'+k]||(sc?sc.url:''));
  });
 }catch(e){}
}
// Hebrew name when the drink has one; the English name becomes the kicker.
function dn(d){return (d && d.he) || (d && d.en) || '';}
function cmRender(){
 const c=COLS[cmC],d=c.drinks[cmI];
 document.getElementById('cm-head').style.background=c.ac;document.getElementById('cm-visual').style.setProperty('--cmbg',c.ac);
 document.getElementById('cm-col').textContent='GT '+c.t.toUpperCase()+' \u00b7 '+c.n;
 document.getElementById('cm-en').textContent=dn(d);
 document.getElementById('cm-he').textContent=d.en||'';
 document.getElementById('cm-num').textContent=(cmI+1)+' / '+c.drinks.length;
 document.getElementById('cm-desc').textContent=d.d;
 const ol=document.getElementById('cm-steps');ol.innerHTML='';
 d.st.forEach(t=>{const li=document.createElement('li');li.textContent=t;ol.appendChild(li);});
 ol.querySelectorAll('li').forEach(li=>{li.style.setProperty('--a',c.ac)});
 document.querySelectorAll('.cm-steps li').forEach(li=>{li.firstChild;});
 const style=document.getElementById('cm-dyn')||(()=>{const st=document.createElement('style');st.id='cm-dyn';document.head.appendChild(st);return st;})();
 style.textContent='.cm-steps li:before{background:'+c.ac+'}';
 const key=cmC+':'+cmI, scene=CHAPTER_SCENES[cmC];
 let vis='';
 if(DPHOTO[key]) vis='<img loading="lazy" decoding="async" src="'+DPHOTO[key]+'" alt="'+dn(d)+'">';
 else if(scene){const pos=scene.n>1?(cmI/(scene.n-1))*100:50; vis='<div class="cm-shot" style="background-image:url(\''+scene.url+'\');background-position:'+pos+'% 100%"></div>';}
 const cv=document.getElementById('cm-visual');cmShow(cv,vis,DPHOTO[key]||(scene?scene.url:''));
 const vurl=DPHOTO[key]||(scene?scene.url:'');
 cv.style.setProperty('--hov',vurl?"url('"+vurl+"')":'none');
 document.getElementById('cm-glass').innerHTML=buildRow(d.st);
 const ing=document.getElementById('cm-ing');ing.innerHTML='';
 d.ing.forEach(t=>{const sp=document.createElement('span');sp.textContent=t;ing.appendChild(sp);});
 document.getElementById('cm-fc').textContent='\u20aa'+d.fc;
 document.getElementById('cm-p').textContent='\u20aa'+d.p;
 document.getElementById('cm-m').textContent=d.m+'%';
 document.getElementById('cm-pr').textContent='\u20aa'+d.pr;
 document.getElementById('cm-prev').disabled=(cmI===0);
 document.getElementById('cm-next').disabled=(cmI===c.drinks.length-1);
 const dots=document.getElementById('cm-dots');dots.innerHTML='';
 c.drinks.forEach((dd,i)=>{const sp=document.createElement('button');sp.type='button';
  sp.className='cm-chip'+(i===cmI?' on':'');sp.textContent=dn(dd);
  sp.onclick=()=>{cmI=i;cmRender();};dots.appendChild(sp);});
 const act=dots.querySelector('.on');
 if(act&&act.scrollIntoView)try{act.scrollIntoView({block:'nearest',inline:'center'})}catch(e){}
 cmSrcRender(cmC,cmI);
 cmPrefetchNear();
}
document.querySelectorAll('.ccard').forEach((el,i)=>{el.style.cursor='pointer';el.addEventListener('click',()=>cmOpen(i));});
try{
 var mxt=document.getElementById('mxtog'), mxb=document.getElementById('mxbox'), mxBuilt=false;
 if(mxt&&mxb){ mxt.addEventListener('click',function(){
  var open=mxt.getAttribute('aria-expanded')==='true';
  if(open){ mxb.hidden=true; mxt.setAttribute('aria-expanded','false'); }
  else{ if(!mxBuilt){ buildMatrix(); mxBuilt=true; }
        mxb.hidden=false; mxt.setAttribute('aria-expanded','true'); }
 }); }
}catch(e){}
try{heroSwipe()}catch(e){}
document.addEventListener('keydown',e=>{const o=document.getElementById('cmodal').classList.contains('open');if(!o)return;
 if(e.key==='Escape')cmClose();if(e.key==='ArrowRight')cmGo(1);if(e.key==='ArrowLeft')cmGo(-1);});
document.getElementById('cmodal').addEventListener('click',e=>{if(e.target.id==='cmodal')cmClose();});
const PUREES={"mango": {"t": "Mango", "d": "מחית מנגו בסגנון אלפונסו זהוב — שכבת השמש למשקאות הדגל, למאצ׳ה, לקוקוס ולאובה.", "drinks": [["משקה דגל Revive מנגו", 2, 2], ["אייס מאצ׳ה מנגו", 4, 1], ["מאצ׳ה קוקוס מנגו", 6, 3], ["אייס אובה מנגו", 9, 1]]}, "strawberry": {"t": "Strawberry", "d": "מחית תות אדום ובשל — שכבת רב המכר לאורך כל תפריט הקיץ.", "drinks": [["משקה דגל Detox תות", 2, 1], ["אייס מאצ׳ה תות", 4, 2], ["מאצ׳ה קוקוס תות", 6, 2], ["אייס אובה תות", 9, 0]]}, "peach": {"t": "Peach", "d": "מחית אפרסק קטיפתי — הכוכב של המדברי־אפרסק: משקה דגל, גזוז, מאצ׳ה ואובה.", "drinks": [["משקה דגל מדברי אפרסק", 2, 0], ["גזוז מדברי אפרסק", 3, 1], ["אייס מאצ׳ה אפרסק", 4, 3], ["אייס אובה אפרסק", 9, 2]]}};
let PIMG={"mango": (GT_ASSET_BASE+"gt-a4039bc6a8.webp"), "strawberry": (GT_ASSET_BASE+"gt-b422ab404b.webp"), "peach": (GT_ASSET_BASE+"gt-c1c67d9c51.webp")};


var PEXTRA={"peach":[(GT_ASSET_BASE+"gt-d66ba5f239.webp")],"strawberry":[(GT_ASSET_BASE+"gt-3fdd230b8c.webp")],"mango":[(GT_ASSET_BASE+"gt-4478816d4f.webp")]};
var pmShots=[],pmI=0;
function pmRender(){var g=document.getElementById("pm-gal");
 var pim=document.getElementById("pm-img");
 pim.src=pmShots[pmI]||"";
 pim.style.cssText='position:static;inset:auto;width:100%;height:auto;max-width:none;max-height:none;'
   +'aspect-ratio:auto;object-fit:fill;display:block;border-radius:0;'
 var pg=document.getElementById("pm-gal");
 if(pg)pg.style.setProperty('--hov',pmShots[pmI]?"url('"+pmShots[pmI]+"')":'none');
 g.classList.toggle("single",pmShots.length<2);
 document.getElementById("pm-dots").innerHTML=pmShots.map(function(_,k){
   return "<i class=\""+(k===pmI?"on":"")+"\"></i>";}).join("");}
function pmSlide(d){if(!pmShots.length)return;pmI=(pmI+d+pmShots.length)%pmShots.length;pmRender();}
function pmOpen(id){
 const p=PUREES[id];
 pmShots=((PEXTRA[id]&&PEXTRA[id].length)?PEXTRA[id]:[PIMG[id]||'']).filter(Boolean);pmI=0;pmRender();
 document.getElementById('pm-title').textContent=p.t+'מחית · לאן זה הולך';
 document.getElementById('pm-sub').textContent=p.d;
 const L=document.getElementById('pm-list');L.innerHTML='';
 p.drinks.forEach(([name,ci,si])=>{
   const a=document.createElement('a');a.href='#!';
   a.innerHTML='<span>'+name+'</span><span class="tag">'+COLS[ci].n+' \u00b7 '+COLS[ci].t+' \u2192</span>';
   a.style.cssText+='color:#20241F;text-decoration:none;';
   a.firstChild.style.cssText='font-family:Assistant,sans-serif;font-weight:600;font-size:16px;color:#20241F;text-decoration:none;';
   a.lastChild.style.cssText='font-size:10.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#9A9F93;text-decoration:none;white-space:nowrap;';
   a.onclick=(e)=>{e.preventDefault();document.getElementById('pmodal').classList.remove('open');cmOpen(ci);cmI=si;cmRender();};
   L.appendChild(a);
 });
 document.getElementById('pmodal').classList.add('open');
}
document.getElementById('pmodal').addEventListener('click',e=>{if(e.target.id==='pmodal')e.target.classList.remove('open')});


let hsI=0,hsTimer=null;
function hsLoad(j){const sl=document.querySelectorAll('.hs-slide');const el=sl[(j+sl.length)%sl.length];if(el&&el.dataset.hsbg){el.style.setProperty("--hsbg","url('"+el.dataset.hsbg+"')");delete el.dataset.hsbg;}}
function hsGo(i){const N=document.querySelectorAll('.hs-slide').length;hsI=(i+N)%N;hsLoad(hsI);hsLoad(hsI+1);hsLoad(hsI-1);
 document.getElementById('hs-track').style.transform='translateX(-'+(hsI*100)+'%)';
 document.getElementById('hs').style.background=document.querySelectorAll('.hs-slide')[hsI].dataset.bg;
 
 document.querySelectorAll('#hs-dots span').forEach((d,j)=>d.classList.toggle('on',j===hsI));
 hsRestart();}
function hsRestart(){clearInterval(hsTimer);if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;hsTimer=setInterval(()=>hsGo(hsI+1),5000);}
(function(){const dd=document.getElementById('hs-dots');
 document.querySelectorAll('.hs-slide').forEach((_,i)=>{const sp=document.createElement('span');sp.onclick=()=>hsGo(i);dd.appendChild(sp);});
 const hs=document.getElementById('hs');
 
 let tx=null;
 hs.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;},{passive:true});
 hs.addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;tx=null;
  if(Math.abs(dx)>50)hsGo(hsI+(dx<0?1:-1));},{passive:true});
 hsGo(0);})();


;
(function(){var M={"417fcc70":(GT_ASSET_BASE+"gt-3ec9267141.webp"),"3a32c397":(GT_ASSET_BASE+"gt-1d3b85270b.webp"),"5c1a5972":(GT_ASSET_BASE+"gt-0043a3441c.webp")};document.querySelectorAll("img").forEach(function(im){var src=im.getAttribute("src")||"";Object.keys(M).forEach(function(k){if(src.indexOf(k)>-1&&!im.closest("#pmodal")){var o=im.src;im.parentElement.addEventListener("mouseenter",function(){im.src=M[k];});im.parentElement.addEventListener("mouseleave",function(){im.src=o;});}});});})();

;

try{
var CYCSHOTS={"0": [(GT_ASSET_BASE+"gt-2057456452.webp"), (GT_ASSET_BASE+"gt-dbb6f70ab8.webp"), (GT_ASSET_BASE+"gt-f2b0bded99.webp"), (GT_ASSET_BASE+"gt-a8d86ef209.webp"), (GT_ASSET_BASE+"gt-1b1a5fe6f0.webp"), (GT_ASSET_BASE+"gt-1ef5ba754c.webp"), (GT_ASSET_BASE+"gt-0a9c7c969a.webp")], "1": [(GT_ASSET_BASE+"gt-c942631391.webp"), (GT_ASSET_BASE+"gt-bf31374321.webp"), (GT_ASSET_BASE+"gt-4445c6ab4a.webp")], "2": [(GT_ASSET_BASE+"gt-39a9e89014.webp"), (GT_ASSET_BASE+"gt-c30af31427.webp"), (GT_ASSET_BASE+"gt-d1ca1a3dd5.webp"), (GT_ASSET_BASE+"gt-a72027a9c6.webp")], "3": [(GT_ASSET_BASE+"gt-2a0820440f.webp"), (GT_ASSET_BASE+"gt-9a20a715c3.webp"), (GT_ASSET_BASE+"gt-732cf0c401.webp")], "4": [(GT_ASSET_BASE+"gt-8728800f85.webp"), (GT_ASSET_BASE+"gt-c3872fdce0.webp"), (GT_ASSET_BASE+"gt-cc4193ac56.webp"), (GT_ASSET_BASE+"gt-de4bdcef66.webp"), (GT_ASSET_BASE+"gt-9b5c14e199.webp"), (GT_ASSET_BASE+"gt-f59f059ff2.webp")], "5": [(GT_ASSET_BASE+"gt-d6a15a37c6.webp"), (GT_ASSET_BASE+"gt-29868b6d41.webp"), (GT_ASSET_BASE+"gt-fe76b1afa1.webp"), (GT_ASSET_BASE+"gt-7565afcb24.webp"), (GT_ASSET_BASE+"gt-5752efa538.webp")], "6": [(GT_ASSET_BASE+"gt-e9f4e7fc38.webp"), (GT_ASSET_BASE+"gt-63eac43d2d.webp"), (GT_ASSET_BASE+"gt-b843ae6fca.webp"), (GT_ASSET_BASE+"gt-ba6967c907.webp"), (GT_ASSET_BASE+"gt-e7bf263165.webp")], "7": [(GT_ASSET_BASE+"gt-7a2b44891b.webp"), (GT_ASSET_BASE+"gt-8d26f09d17.webp"), (GT_ASSET_BASE+"gt-36f43500ad.webp"), (GT_ASSET_BASE+"gt-af10238dca.webp"), (GT_ASSET_BASE+"gt-690f2e7dec.webp"), (GT_ASSET_BASE+"gt-c6c2dd8d6b.webp")], "8": [(GT_ASSET_BASE+"gt-676ae5224b.webp"), (GT_ASSET_BASE+"gt-d35192636a.webp"), (GT_ASSET_BASE+"gt-2b1babb40e.webp"), (GT_ASSET_BASE+"gt-6e94247f32.webp")], "9": [(GT_ASSET_BASE+"gt-7281b3e7a6.webp"), (GT_ASSET_BASE+"gt-83ff7d7c09.webp"), (GT_ASSET_BASE+"gt-9c1a90ccd8.webp"), (GT_ASSET_BASE+"gt-e048d3f32b.webp"), (GT_ASSET_BASE+"gt-ec3523c940.webp")]};
// ── листание напитков главы при наведении на карточку коллекции ──
(function(){
  function build(){
    document.querySelectorAll('.ccard[data-ci]').forEach(function(card){
      if(card.querySelector('.cyc')) return;
      var ci=card.getAttribute('data-ci');
      var shots=(CYCSHOTS[ci]||[]);
      if(shots.length<2) return;
      var box=document.createElement('div'); box.className='cyc';
      box.style.cssText+='position:absolute;inset:0;z-index:2;pointer-events:none;overflow:hidden;opacity:0;';
      shots.forEach(function(u,i){
        var im=document.createElement('img');
        im.decoding='async'; im.alt='';
        im.style.cssText+='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;'
          +'object-position:50% 100%;opacity:0;';
        im.src=u;
        if(i===0){ im.className='on'; im.style.opacity='1'; }
        box.appendChild(im);
      });
      var tag=document.createElement('div'); tag.className='cyc-tag';
      tag.textContent=shots.length+'מתכונים ←';
      /* позиция задаётся инлайном — её не перебьёт ни одно правило в стилях */
      tag.style.cssText+='position:absolute;top:14px;right:14px;left:auto;bottom:auto;'
        +'max-width:calc(100% - 28px);box-sizing:border-box;z-index:6;';
      var dots=document.createElement('div'); dots.className='cyc-dots';
      dots.style.cssText+='position:absolute;top:52px;right:16px;left:auto;bottom:auto;z-index:6;';
      shots.forEach(function(_,k){var d=document.createElement('i'); if(k===0)d.className='on'; dots.appendChild(d);});
      card.appendChild(box); card.appendChild(tag); card.appendChild(dots);

      var imgs=box.querySelectorAll('img'), ds=dots.querySelectorAll('i'), i=0, t=null;
      var HOLD=900;
      function show(n){
        imgs=box.querySelectorAll('img');
        if(!imgs.length) return;
        i=n%imgs.length;
        [].forEach.call(imgs,function(x,k){
          if(k===i){ x.classList.add('on'); x.style.opacity='1'; }
          else { x.classList.remove('on'); x.style.opacity='0'; }
        });
        [].forEach.call(ds,function(x,k){ x.className = (k===i?'on':''); });
      }
      function step(){ show((i+1)%imgs.length); }
      var warmed=false;
      function play(){
        imgs=box.querySelectorAll('img');
        if(imgs.length<2) return;
        if(!warmed){ warmed=true;
          [].forEach.call(imgs,function(x){ if(x.decode) x.decode().catch(function(){}); }); }
        if(t)clearInterval(t);
        box.style.opacity='1';
        show(0);
        t=setInterval(step,HOLD);
      }
      function stop(){ clearInterval(t); t=null; show(0); box.style.opacity='0'; }
      card.addEventListener('mouseenter',play);
      card.addEventListener('pointerenter',play);
      card.addEventListener('mouseleave',stop);
      card.addEventListener('pointerleave',stop);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',build);
  else build();
})();
}catch(e){console.warn('cyc:',e)}

;

function pAll(b){var ds=document.querySelectorAll('#pricing .ptable');
 var open=[].every.call(ds,function(d){return d.open});
 [].forEach.call(ds,function(d){d.open=!open});
 b.textContent=open?'Expand all':'סגרו הכול';}

;

function pfTrack(interest,role){try{
 window.dataLayer=window.dataLayer||[];
 window.dataLayer.push({event:'generate_lead',form:'partner_enquiry',
  lead_interest:interest||'',lead_role:role||''});
 if(typeof gtag==='function')gtag('event','generate_lead',{form:'partner_enquiry'});
}catch(e){}}
var PF_LABEL='שליחה <span class="arr">\u2190</span>';
var PF_ERR='לא הצלחנו לשלוח את הפנייה. נסו שוב, או דברו איתנו ישירות: <a href="https://wa.me/972543982444">וואטסאפ</a> \u00b7 <a href="tel:+972543982444">054-398-2444</a>.';
var PF_ENDPOINT="https://rvadsozabmxkkrktwgnv.supabase.co/functions/v1/website_lead_intake";
var PF_SHOWN=Date.now();
function pSend(e){e.preventDefault();
 var g=function(id){var el=document.getElementById(id);return el?el.value.trim():'';};
 var f=document.getElementById('pform');
 var err=document.getElementById('pf-err');
 var btn=f.querySelector('button');
 if(!document.getElementById('pf-agree').checked)return false;
 var fail=function(msg){err.innerHTML=msg;err.hidden=false;
  btn.disabled=false;btn.innerHTML=PF_LABEL;
  err.scrollIntoView({block:'nearest',behavior:'smooth'});};
 err.hidden=true;
 btn.disabled=true;btn.innerHTML='שולח\u2026';
 var body={contact_name:g('pf-name'),venue:g('pf-venue'),city:g('pf-city'),
  role:g('pf-role'),phone:g('pf-phone'),email:g('pf-mail'),interest:g('pf-int'),
  message:g('pf-msg'),company_website:g('pf-cw'),
  elapsed_ms:Date.now()-PF_SHOWN,page:location.href,referrer:document.referrer};
 var to=setTimeout(function(){fail(PF_ERR);},15000);
 fetch(PF_ENDPOINT,{method:'POST',headers:{'content-type':'application/json'},
  body:JSON.stringify(body)})
  .then(function(r){return r.json().catch(function(){return {};})
   .then(function(j){return {ok:r.ok,j:j};});})
  .then(function(res){clearTimeout(to);
   if(res.ok&&res.j&&res.j.ok){pfTrack(g('pf-int'),g('pf-role'));
    f.classList.add('sent');btn.innerHTML='נשלח \u2713';
    document.getElementById('pf-done').scrollIntoView({block:'nearest',behavior:'smooth'});return;}
   if(res.j&&res.j.error==='missing_fields'){fail('חסרים פרטים חובה. בדקו שם, שם העסק, עיר וטלפון.');return;}
   if(res.j&&res.j.error==='bad_phone'){fail('מספר הטלפון לא נראה תקין. בדקו אותו ונסו שוב.');return;}
   if(res.j&&res.j.error==='bad_email'){fail('כתובת המייל לא נראית תקינה. בדקו אותה ונסו שוב.');return;}
   fail(PF_ERR);})
  .catch(function(){clearTimeout(to);fail(PF_ERR);});
 return false;}
