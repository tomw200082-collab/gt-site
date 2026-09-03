# -*- coding: utf-8 -*-
"""One generator, four sections. If a page needs a hand edit, this file is wrong.

Design note — the drink is the signature.
Each card carries the photograph of the drink it names: 48 cut-out glasses shot for
GT, one per drink, all trimmed to the same 520px height so the whole grid reads as
one set. They replaced a CSS-drawn glass that sized its bands from the millilitres
in the recipe — an honest diagram, but a diagram, on a page whose job is to make a
buyer want the cup. `photos.json` holds the drink-to-photo map and its provenance.
"""
import json, html, os

D = json.load(open('drinks.json'))
P = json.load(open('photos.json'))
A = json.load(open('assets.json'))['size']
B = json.load(open('bottles.json'))

def dim(asset):
    """width/height attributes for a theme asset, measured not guessed.

    These exist so the browser can reserve the right box before the bytes land. All
    thirteen were wrong by hand -- the plate shot claimed 720x720 against a real
    700x1585, so the page reserved a square and jumped 567px when the file arrived.
    measure_assets.py refreshes assets.json whenever an asset is replaced."""
    w, h = A[asset]
    return f'width="{w}" height="{h}"'
esc = lambda s: html.escape(s, quote=True)
WA = "972543982444"

PAGES = {
 "chai": dict(
   key="צ'אי", unit="מבקבוק אחד", accent="#D96B3F", atext="#B85B36", tint="#F6E4D9", deep="#412013",
   hero="gt-74108519a7.webp", eyebrow="צ׳אי מסאלה · NAMASTEA",
   h1=("בקבוק אחד. ", "אחת־עשרה כוסות."),
   promise="שני סוגי תה שחור וחמישה תבלינים, מוכנים למזיגה. אחד־עשר משקאות שהבר שלכם יודע להכין כבר עכשיו — בלי ציוד, בלי הכשרה, בלי פריט חדש במקרר.",
   need=("צריך רק מה שכבר יש לכם", "קרח, חלב או מים, וכוס. כל אחד־עשר המשקאות יוצאים מאותו בקבוק."),
   prod=dict(name="NAMASTEA", origin="תערובת הודית",
     comp="שני סוגי תה שחור · קינמון · הל · ג׳ינג׳ר · פלפל שחור · ציפורן",
     liner="רב־המכר של GT בקהל הישראלי. מבריק קר, נהדר עם מי קוקוס, ועובד חם כצ׳אי לאטה עם כל חלב.",
     sizes=[("500 מ״ל","₪33"),("1 ליטר","₪65")],
     img="gt-0ae37a139e.webp"),
   extra=None),
 "matcha": dict(
   key="מאצ'ה", unit="מאבקה אחת", accent="#5FA34C", atext="#4C823D", tint="#E5ECDB", deep="#1C3117",
   hero="gt-7e97065cdf.webp", eyebrow="מאצ׳ה · שיזואוקה",
   h1=("המאצ׳ה היפנית ", "האיכותית בישראל."),
   promise="להכנת מגוון משקאות שכל אחד מהם הוא חוויה מסעירה. בסיס אחד נבנה בתחילת המשמרת ומשרת את כל שש־עשרה הכוסות.",
   need=("צריך מקציף וחלב", "הבסיס נבנה פעם אחת — 1.8 גרם על 50 מ״ל מים — ומחזיק לכל המשמרת."),
   prod=dict(name="מאצ׳ה שיזואוקה", origin="שיזואוקה · יפן",
     comp="דרגה טקסית · מיובא ישירות מהחקלאים",
     liner="אבקת מאצ׳ה טקסית יפנית ממחוז שיזואוקה, בהטסה ישירה מהחקלאים ביפן לשמירת טריות מירבית — כי את ההבדל הלקוחות מרגישים בטעם.",
     sizes=[("50 גרם","₪65"),("500 גרם","₪590")],
     yields=[("50 גרם","27"),("500 גרם","277")], dose="1.8 גרם לכוס",
     img="gt-b701af91e0.webp"),
   extra=dict(name="הוג׳יצ׳ה", tagline="קלוי · ״מאצ׳ה שחורה״",
     liner="כל שש־עשרה הכוסות בעמוד הזה אפשר להכין גם עם הוג׳יצ׳ה — מאצ׳ה שחורה קלויה, עם נימות אגוז לוז וקקאו. אותה הכנה, אותה עלות מנה, פרופיל טעם אחר לגמרי.",
     comp="מאצ׳ה מובחר קלוי · נימות אגוז לוז וקקאו",
     sizes=[("500 גרם","₪375")], img="gt-a06eb940fc.webp")),
 "iced-tea": dict(
   key="תה קר", unit="מאותו קו תרכיזים", accent="#E63950", atext="#DA364C", tint="#F8DDDB", deep="#451118",
   hero="gt-d3abd65414.webp", eyebrow="חליטות קרות · אחד עשר תרכיזים",
   h1=("שש־עשרה כוסות. ", "בלי מכונה אחת."),
   promise="תרכיזי תה מוכנים למזיגה. חמישים מיליליטר, קרח, ומים או סודה — והמשקה על הבר. בקבוק סגור לא צריך מקום במקרר.",
   need=("צריך רק מה שכבר יש לכם", "קרח, מים או סודה, וכוס. בקבוק סגור לא צריך קירור."),
   line=True,
   prod=dict(name="אחד עשר תרכיזים", origin="הקו",
     comp="Fresh · Detox · Revive · Energy · Consciousness · Calm · Desertea · Namastea · American",
     liner="אחד עשר תרכיזים מכל עולם התה, כל אחד עם פרופיל משלו. בקבוק סגור לא צריך מקרר, ופתוח מחזיק בקירור.",
     sizes=[("500 מ״ל","₪33"),("1 ליטר","₪65")],
     img="gt-682cbb70f5.webp"),
   extra=None),
 "ube": dict(
   key="אובה", unit="מאבקה אחת", accent="#7B5CC6", atext="#7B5CC6", tint="#E9E2EC", deep="#251C3B",
   hero="gt-868e993bce.webp", eyebrow="אובה · שורש בטטה סגולה",
   h1=("הטרנד הסגול ", "שכובש את העולם."),
   promise="אבקת שורש יאם באיכות מעולה — מרקם קרמי ומתיקות עדינה בין וניל לאגוז. הצבע מגיע מהשורש עצמו, וזה בדיוק מה שמצלם.",
   need=("צריך מקציף וחלב", "כל כוס כאן מחברת אובה למוצר GT שני — מחית פרי, מאצ׳ה או צ׳אי."),
   prod=dict(name="אובה", origin="שורש בטטה סגולה",
     comp="אבקת בטטה סגולה · צבע טבעי",
     liner="אבקת שורש יאם (בטטה סגולה) באיכות מעולה, בעלת מרקם קרמי ומתיקות עדינה בין וניל לאגוז. הצבע הסגול טבעי ומגיע מצבעה של הבטטה, והיא משתלבת באופן מושלם במשקאות לאטה, שייק או סודה.",
     sizes=[("500 גרם","₪175"),("1 ק״ג","₪340")],
     yields=[("500 גרם","250"),("1 ק״ג","500")], dose="2 גרם לכוס",
     img="gt-cda710c642.webp"),
   extra=None),
}

def shot(d):
    """The drink's own photograph. alt is empty on purpose: the h3 beside it already
    names the drink, so a duplicate would only make a screen reader say it twice.

    All 48 sit on one shared canvas, so one width/height serves every card and the
    glasses align without the CSS doing any work — see photos.json and cut_shots.py.

    Delivered at the height the card actually paints (200 CSS px), not the 1052 the
    master is stored at. Shopify keeps a transparent master as PNG and only hands
    back WebP when the browser asks for it in Accept, so the numbers that matter are
    the WebP ones; at 200 a shot is an order of magnitude smaller than its master.
    width/height stay the master's so the aspect ratio is known before the CSS
    lands."""
    did = P['map'][d['he']]
    w, h = P['size']
    u = f'{P["cdn"]}gtd-{did}.webp?height='
    return (f'<img class="g-shot" src="{u}400"'
            f' srcset="{u}200 1x, {u}400 2x" alt=""'
            f' width="{w}" height="{h}" loading="lazy" decoding="async">')

def card(d):
    steps = "".join(f"<li>{esc(s)}</li>" for s in d['steps'])
    note = f'<p class="g-note">{esc(d["note"])}</p>' if d['note'] else ""
    return f"""
      <article class="g-drink">
        {shot(d)}
        <div class="g-drink-tx">
          <h3>{esc(d['he'])}</h3>
          <span class="g-en">{esc(d['en'])}</span>
          <dl class="g-fig">
            <div><dt>עלות מנה</dt><dd>₪{d['cost']}</dd></div>
            <div><dt>מחיר מומלץ</dt><dd>₪{d['price']}</dd></div>
            <div class="g-keep"><dt>נשאר אצלכם</dt><dd>{d['marg']}%</dd></div>
          </dl>
          <details>
            <summary>איך מכינים</summary>
            <ol>{steps}</ol>
            {note}
          </details>
        </div>
      </article>"""

def sizes_html(pairs):
    return "".join(f'<span>{esc(l)}<b dir="ltr">{esc(v)}</b></span>' for l, v in pairs)

def build(slug, cfg):
    ds = [d for d in D if d['page'] == cfg['key']]
    cards = "".join(card(d) for d in ds)
    p = cfg['prod']
    wa = f"https://wa.me/{WA}?text=" + __import__('urllib.parse', fromlist=['quote']).quote(
        f"היי, הגעתי מדף ה{cfg['key']} באתר ואשמח לקבל את המחירון")
    lo = min(float(d['cost']) for d in ds)
    mn, mx = min(int(d['marg']) for d in ds), max(int(d['marg']) for d in ds)

    yield_line = ""
    if p.get('yields'):
        ys = " · ".join(f"{esc(g)} ≈ {esc(n)} כוסות" for g, n in p['yields'])
        yield_line = f'<p class="g-yield">{ys} — לפי המנה שבמתכונים ({esc(p["dose"])}).</p>'

    # The whole concentrate line, eleven bottles, which is exactly the number this
    # section's heading claims. Each carries its index for the arrival stagger and its
    # own label colour for the glow behind it; gt-lp.js arms and triggers the arrival.
    line = ""
    if cfg.get('line'):
        items = "".join(
            f'<li class="g-btl" style="--i:{i};--c:{B["glow"][k]}">'
            f'<img src="{{{{ \'gt-btl-{k}.webp\' | asset_url }}}}" alt="{esc(B["name"][k])}"'
            f' loading="lazy" decoding="async" {dim(f"gt-btl-{k}.webp")}></li>'
            for i, k in enumerate(B['order']))
        line = f"""
    <div class="g-wrap">
      <ul class="g-line">{items}</ul>
    </div>
"""

    siblings = "".join(
        f'<a href="/pages/{o}">{esc(PAGES[o]["key"])}</a>'
        for o in PAGES if o != slug)

    extra = ""
    if cfg['extra']:
        e = cfg['extra']
        extra = f"""
    <div class="g-wrap">
      <aside class="g-alt">
        <img src="{{{{ '{e['img']}' | asset_url }}}}" alt="{esc(e['name'])}" loading="lazy" decoding="async" {dim(e['img'])}>
        <div>
          <span class="g-eyebrow">{esc(e['tagline'])}</span>
          <h3>{esc(e['name'])}</h3>
          <p>{esc(e['liner'])}</p>
          <p class="g-comp">{esc(e['comp'])}</p>
          <div class="g-sizes">{sizes_html(e['sizes'])}</div>
        </div>
      </aside>
    </div>"""

    return f"""{{{{ 'gt-lp.css' | asset_url | stylesheet_tag }}}}
{{{{ 'gt-lp.js' | asset_url | script_tag }}}}
{{%- comment -%}}
  gt-lp-{slug} — generated by tools/landing-pages/gen.py. Do not hand-edit: regenerate.
  Figures transcribed from Canva DAHTYkRvEnM (קטלוג משקאות סופי 26) and proven equal
  to drinks_final_figures.json 2026-08-27 — 48/48 names, 0 deviations, margin
  re-derived 0/48 mismatches. Each card carries the photograph of the drink it names,
  cut out and trimmed by tools/landing-pages/photos.json.
{{%- endcomment -%}}
<div class="g-lp g-lp-{slug}" style="--a:{cfg['accent']};--at:{cfg['atext']};--tint:{cfg['tint']};--deep:{cfg['deep']}">

  <header class="g-hero">
    <img class="g-hero-img" src="{{{{ '{cfg['hero']}' | asset_url }}}}" alt="" {dim(cfg['hero'])} fetchpriority="high" decoding="async">
    <div class="g-hero-in">
      <img class="g-logo" src="{{{{ 'gt-71e14890dd.png' | asset_url }}}}" alt="GT Everyday" {dim('gt-71e14890dd.png')} decoding="async">
      <span class="g-eyebrow">{esc(cfg['eyebrow'])}</span>
      <h1 class="g-display">{esc(cfg['h1'][0])}<em>{esc(cfg['h1'][1])}</em></h1>
      <p class="g-promise">{esc(cfg['promise'])}</p>
      <div class="g-ctas">
        <a class="g-btn" href="#g-lp-form">להצטרף כשותפים <span class="g-arr" aria-hidden="true">←</span></a>
        <a class="g-btn g-ghost" href="{wa}" target="_blank" rel="noopener">וואטסאפ <span class="g-arr" aria-hidden="true">←</span></a>
      </div>
    </div>
    <div class="g-ledger">
      <div><b dir="ltr">{len(ds)}</b><i>משקאות {esc(cfg["unit"])}</i></div>
      <div><b dir="ltr">{mn}–{mx}%</b><i>נשאר אצלכם על כל כוס</i></div>
      <div><b dir="ltr">₪{lo:.2f}</b><i>עלות המנה הנמוכה כאן</i></div>
    </div>
  </header>

  <section class="g-menu">
    <div class="g-wrap">
      <div class="g-head">
        <span class="g-eyebrow">התפריט</span>
        <h2 class="g-display">זה יכול להיות <em>התפריט שלך.</em></h2>
        <p>כל כוס בתמונה היא הכוס שיוצאת מהמתכון הזה. עלות המנה ללא מע״מ, המחיר המומלץ כולל, והאחוז הוא מה שנשאר אצלכם מההכנסה נטו.</p>
      </div>
      <div class="g-grid">{cards}</div>
      <p class="g-fine">עלות = ללא מע״מ · מחיר מומלץ = כולל מע״מ 18% · הרווח מחושב על ההכנסה נטו · עלות רכיבי המשקה בלבד, ללא גרניש</p>
    </div>
  </section>

  <section class="g-plate">
    <div class="g-wrap g-plate-in">
      <figure><img src="{{{{ '{p['img']}' | asset_url }}}}" alt="{esc(p['name'])}" loading="lazy" decoding="async" {dim(p['img'])}></figure>
      <div>
        <span class="g-eyebrow">{esc(p['origin'])}</span>
        <h2 class="g-display">{esc(p['name'])}</h2>
        <p class="g-liner">{esc(p['liner'])}</p>
        <p class="g-comp">{esc(p['comp'])}</p>
        <div class="g-sizes">{sizes_html(p['sizes'])}</div>
        {yield_line}
        <div class="g-need">
          <b>{esc(cfg['need'][0])}</b>
          <span>{esc(cfg['need'][1])}</span>
        </div>
      </div>
    </div>
{extra}{line}  </section>

  <section class="g-story">
    <span class="g-ghostword" aria-hidden="true">{esc(cfg['key'])}</span>
    <div class="g-wrap g-story-in">
      <div>
        <span class="g-eyebrow">מי אנחנו</span>
        <h2 class="g-display">יצרנית בוטיק <em>ישראלית.</em></h2>
        <p>אנחנו חולטים עלי תה וצמחי מאכל באיכות מעולה מכל העולם ויוצרים מהם תמציות טבעיות ללא חומרים משמרים, להכנת מגוון אדיר של משקאות שמעניקים חוויה ולא רק שתייה.</p>
      </div>
      <div>
        <p class="g-punch">אלו יהיו המשקאות הכי רווחיים שלך.</p>
        <ul>
          <li>נוצר במיוחד עבור בעלי בתי קפה ומסעדות.</li>
          <li>קל מאוד לתפעול ולהטמעה.</li>
          <li>באחסון סגור אינו מצריך קירור ואינו תופס מקום במקרר.</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="g-capture" id="g-lp-form">
    <div class="g-wrap g-capture-in">
      <div>
        <span class="g-eyebrow">נדבר</span>
        <h2 class="g-display">בואו נהיה <em>שותפים.</em></h2>
        <p>המחירון הסיטונאי, המתכונים המתומחרים, והתאמה לתפריט שלכם. חוזרים תוך יום עסקים אחד.</p>
        <ul class="g-contact">
          <li><a href="{wa}" target="_blank" rel="noopener">וואטסאפ · 054-398-2444</a></li>
          <li><a href="tel:+{WA}">חייגו · 054-398-2444</a></li>
          <li>הלהב 15, חולון · info@gteveryday.com</li>
        </ul>
      </div>
      <form data-endpoint="{{{{ section.settings.lead_webhook | escape }}}}" data-source="site-{slug}" data-wa="{WA}" novalidate>
        <div class="g-f-row">
          <label><span>שם העסק</span><input name="display_name" required autocomplete="organization"></label>
          <label><span>השם שלך</span><input name="contact_name" required autocomplete="name"></label>
        </div>
        <div class="g-f-row">
          <label><span>טלפון</span><input name="phone" type="tel" required autocomplete="tel" inputmode="tel"></label>
          <label><span>עיר</span><input name="city" autocomplete="address-level2"></label>
        </div>
        <label><span>אימייל · לא חובה</span><input name="email" type="email" autocomplete="email"></label>
        <label class="g-ok"><input type="checkbox" name="consent" required> אני מאשר/ת פנייה בנוגע לאספקה סיטונאית.</label>
        <button type="submit" class="g-btn g-solid">להצטרף כשותפים <span class="g-arr" aria-hidden="true">←</span></button>
        <p class="g-msg" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>

  <nav class="g-siblings" aria-label="קווים נוספים">
    <span>עוד קווים</span>
    {siblings}
  </nav>

  <a class="g-sticky" href="#g-lp-form">להצטרף כשותפים <span class="g-arr" aria-hidden="true">←</span></a>

  <footer class="g-foot">
    <div class="g-wrap">
      <span>© 2026 גרין טי אוורידיי בע״מ</span>
      <span class="g-serif" dir="ltr">Don't Drink Boring.</span>
    </div>
  </footer>
</div>

{{% schema %}}
{{
  "name": "GT LP · {slug}",
  "settings": [
    {{
      "type": "text",
      "id": "lead_webhook",
      "label": "Lead webhook (Make)",
      "info": "POST target for the form. Leave empty and the form falls back to WhatsApp with the details prefilled."
    }}
  ]
}}
{{% endschema %}}
"""

os.makedirs('out', exist_ok=True)
for slug, cfg in PAGES.items():
    src = build(slug, cfg)
    open(f'out/gt-lp-{slug}.liquid','w').write(src)
    tpl = {"layout":"gt","sections":{"main":{"type":f"gt-lp-{slug}","settings":{}}},"order":["main"]}
    open(f'out/page.{slug}.json','w').write(json.dumps(tpl, indent=2)+"\n")
    print(f"gt-lp-{slug}.liquid  {len(src):>6} chars · {len([d for d in D if d['page']==cfg['key']])} drinks")
