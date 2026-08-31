# -*- coding: utf-8 -*-
"""One generator, four sections. If a page needs a hand edit, this file is wrong."""
import json, html, os
D = json.load(open('drinks.json'))
esc = lambda s: html.escape(s, quote=True)

PAGES = {
 "chai": dict(
   key="צ'אי", slug="chai", accent="#C98A2D", tint="#F0E2CC", deep="#8A5A18",
   hero="gt-74108519a7.webp", eyebrow="צ׳אי מסאלה",
   h1=("אחת שקית. ", "אחת־עשרה כוסות."),
   promise="NAMASTEA הוא תרכיז אחד שנכנס לתפריט בלי ציוד חדש ובלי הכשרה — ופותח אחת־עשרה כוסות שהצוות שלכם כבר יודע להכין.",
   need="שום דבר. קרח, חלב או מים, וכוס. כל אחד־עשר המשקאות נבנים מאותו תרכיז.",
   prod=dict(name="NAMASTEA", origin="תערובת הודית",
     comp="שני סוגי תה שחור · קינמון · הל · ג׳ינג׳ר · פלפל שחור · ציפורן",
     liner="רב מכר אדיר בקהל הישראלי. שני סוגי תה שחור וחמישה תבלינים — מבריק קר או עם מי קוקוס, ונהדר חם כצ׳אי לאטה עם כל חלב.",
     sizes=[("500 מ״ל","₪33"),("1 ליטר","₪65")],
     imgs=["gt-0ae37a139e.webp","gt-c3376fa322.webp","gt-51eff11d95.webp"]),
   extra=None),
 "matcha": dict(
   key="מאצ'ה", slug="matcha", accent="#4A8A38", tint="#E6F0DC", deep="#2B4F24",
   hero="gt-7e97065cdf.webp", eyebrow="מאצ׳ה",
   h1=("המאצ׳ה היפנית ", "האיכותית בישראל."),
   promise="להכנת מגוון משקאות שכל אחד מהם הוא חוויה מסעירה.",
   need="מקציף או מטרפה, וחלב. הבסיס נבנה פעם אחת ומשרת את כל הכוסות במשמרת.",
   prod=dict(name="מאצ׳ה שיזואוקה", origin="שיזואוקה · יפן",
     comp="דרגה טקסית · מיובא ישירות מהחקלאים",
     liner="אבקת מאצ׳ה טקסית יפנית ממחוז שיזואוקה, בהטסה ישירה מהחקלאים ביפן לשמירת טריות מירבית — כי את ההבדל הלקוחות מרגישים בטעם.",
     yields=[("50 גרם","27"),("500 גרם","277")], dose="1.8 גרם לכוס",
     sizes=[("50 גרם","₪65"),("500 גרם","₪590")],
     imgs=["gt-b701af91e0.webp","gt-ead606c1cb.webp"]),
   extra=dict(kind="hojicha", name="הוג׳יצ׳ה", tagline="קלוי · ״מאצ׳ה שחורה״",
     liner="כל שש־עשרה הכוסות בעמוד הזה אפשר להכין גם עם הוג׳יצ׳ה — מאצ׳ה שחורה קלויה, עם נימות אגוז לוז וקקאו. אותה הכנה, אותה עלות מנה, פרופיל טעם אחר לגמרי.",
     comp="מאצ׳ה מובחר קלוי · נימות אגוז לוז וקקאו",
     sizes=[("500 גרם","₪375")], img="gt-a06eb940fc.webp")),
 "iced-tea": dict(
   key="תה קר", slug="iced-tea", accent="#A31F34", tint="#F3D9DD", deep="#6E1223",
   hero="gt-d3abd65414.webp", eyebrow="חליטות קרות",
   h1=("שש־עשרה כוסות. ", "בלי מכונה אחת."),
   promise="תרכיזי תה מוכנים למזיגה. פותחים, מוזגים חמישים מיליליטר, משלימים במים או בסודה — והמשקה על הבר.",
   need="שום דבר. קרח, מים או סודה, וכוס. בקבוק סגור לא צריך מקרר.",
   prod=dict(name="אחד עשר תרכיזים", origin="הקו",
     comp="Fresh · Detox · Revive · Energy · Consciousness · Calm · Desertea · Namastea · American",
     liner="אחד עשר תרכיזים מכל עולם התה, כל אחד עם פרופיל משלו. בקבוק סגור לא צריך מקרר, ובקבוק פתוח מחזיק במקרר.",
     sizes=[("500 מ״ל","₪33"),("1 ליטר","₪65")],
     imgs=["gt-682cbb70f5.webp","gt-a5c7d099eb.webp","gt-e24c680e39.webp"]),
   extra=None),
 "ube": dict(
   key="אובה", slug="ube", accent="#7B5CC6", tint="#EAE3F7", deep="#4E3690",
   hero="gt-868e993bce.webp", eyebrow="אובה",
   h1=("UBE — הטרנד הסגול ", "שכובש את העולם."),
   promise="אבקת שורש יאם באיכות מעולה, עם מרקם קרמי ומתיקות עדינה בין וניל לאגוז.",
   need="מקציף או מטרפה, וחלב. כל כוס בעמוד הזה מחברת אובה למוצר GT שני — מחית פרי, מאצ׳ה או צ׳אי.",
   prod=dict(name="אובה", origin="שורש בטטה סגולה",
     comp="אבקת בטטה סגולה · צבע טבעי",
     liner="אבקת שורש יאם (בטטה סגולה) באיכות מעולה, בעלת מרקם קרמי ומתיקות עדינה בין וניל לאגוז. הצבע הסגול טבעי ומגיע מצבעה של הבטטה, והיא משתלבת באופן מושלם במשקאות לאטה, שייק או סודה.",
     yields=[("500 גרם","250"),("1 ק״ג","500")], dose="2 גרם לכוס",
     sizes=[("500 גרם","₪175"),("1 ק״ג","₪340")],
     imgs=["gt-cda710c642.webp","gt-c6647d2155.webp"]),
   extra=None),
}
WA = "972543982444"

def card(d, n, cfg):
    steps = "".join(f"<li>{esc(s)}</li>" for s in d['steps'])
    note = f'<p class="lp-note">{esc(d["note"])}</p>' if d['note'] else ""
    return f"""
      <article class="lp-drink rv">
        <header>
          <span class="lp-n">{n:02d}</span>
          <div>
            <h3>{esc(d['he'])}</h3>
            <span class="lp-en">{esc(d['en'])}</span>
          </div>
        </header>
        <dl class="lp-fig">
          <div><dt>עלות מנה<small>ללא מע״מ</small></dt><dd class="num">₪{d['cost']}</dd></div>
          <div><dt>מחיר מומלץ<small>כולל מע״מ</small></dt><dd class="num">₪{d['price']}</dd></div>
          <div class="lp-marg"><dt>רווחיות</dt><dd class="num">{d['marg']}%</dd></div>
        </dl>
        <details>
          <summary>אופן ההכנה</summary>
          <ol>{steps}</ol>
          {note}
        </details>
      </article>"""

def build(slug, cfg):
    ds = [d for d in D if d['page'] == cfg['key']]
    cards = "".join(card(d, i+1, cfg) for i, d in enumerate(ds))
    p = cfg['prod']
    chip = lambda l, v: f'<span>{esc(l)}<b dir="ltr">{esc(v)}</b></span>'
    sizes = "".join(chip(l, v) for l, v in p['sizes'])
    yield_line = ""
    if p.get('yields'):
        ys = " · ".join(f"{esc(g)} ≈ {esc(n)} כוסות" for g, n in p['yields'])
        yield_line = f'<p class="lp-yield">{ys} — לפי מנת ההכנה שבמתכונים ({esc(p["dose"])}).</p>' 
    from urllib.parse import quote
    wa_txt = quote(f"היי, הגעתי מדף ה{cfg['key']} באתר ואשמח לשמוע פרטים")

    extra = ""
    if cfg['extra']:
        e = cfg['extra']
        extra = f"""
    <aside class="lp-alt rv">
      <img src="{{{{ '{e['img']}' | asset_url }}}}" alt="{esc(e['name'])}" loading="lazy" decoding="async" width="420" height="420">
      <div>
        <span class="lp-eyebrow">{esc(e['tagline'])}</span>
        <h3>{esc(e['name'])}</h3>
        <p>{esc(e['liner'])}</p>
        <p class="lp-comp">{esc(e['comp'])}</p>
        <div class="lp-sizes">{"".join(chip(l, v) for l, v in e['sizes'])}</div>
      </div>
    </aside>"""

    return f"""{{{{ 'gt-lp.css' | asset_url | stylesheet_tag }}}}
{{{{ 'gt-lp.js' | asset_url | script_tag }}}}
{{%- comment -%}}
  gt-lp-{slug} — landing page section, generated by gen.py. Do not hand-edit:
  regenerate. Figures transcribed from Canva DAHTYkRvEnM (קטלוג משקאות סופי 26)
  and proven equal to drinks_final_figures.json 2026-08-27 — 48/48 names,
  0 deviations, margin re-derived 0/48 mismatches.
{{%- endcomment -%}}
<div class="lp lp-{slug}" style="--a:{cfg['accent']};--tint:{cfg['tint']};--deep:{cfg['deep']}">

  <header class="lp-hero">
    <img class="lp-hero-img" src="{{{{ '{cfg['hero']}' | asset_url }}}}" alt="{esc(cfg['eyebrow'])}" width="1400" height="900" fetchpriority="high" decoding="async">
    <div class="lp-hero-in">
      <img class="lp-logo" src="{{{{ 'gt-71e14890dd.png' | asset_url }}}}" alt="GT Everyday" width="120" height="34" decoding="async">
      <span class="lp-eyebrow">{esc(cfg['eyebrow'])}</span>
      <h1 class="lp-display">{esc(cfg['h1'][0])}<em>{esc(cfg['h1'][1])}</em></h1>
      <p class="lp-promise">{esc(cfg['promise'])}</p>
      <div class="lp-ctas">
        <a class="lp-btn" href="#lp-form">קבלו את המחירון המלא <span aria-hidden="true">←</span></a>
        <a class="lp-btn lp-wa" href="https://wa.me/{WA}?text={wa_txt}" target="_blank" rel="noopener">וואטסאפ <span aria-hidden="true">←</span></a>
      </div>
    </div>
  </header>

  <section class="lp-strip">
    <div class="lp-wrap">
      <div><b class="num">{len(ds)}</b><i>משקאות מהעמוד הזה</i></div>
      <div><b class="num">{min(int(d['marg']) for d in ds)}–{max(int(d['marg']) for d in ds)}<span>%</span></b><i>רווחיות לכוס</i></div>
      <div><b class="num">₪{min(float(d['cost']) for d in ds):.2f}</b><i>עלות המנה הנמוכה בעמוד</i></div>
    </div>
  </section>

  <section class="lp-sec">
    <div class="lp-wrap">
      <div class="lp-head rv">
        <span class="lp-eyebrow">התפריט</span>
        <h2 class="lp-display">זה יכול להיות <em>התפריט שלך.</em></h2>
        <p>עלות המנה היא עלות הרכיבים שלכם לכוס, ללא מע״מ. המחיר המומלץ כולל מע״מ. הרווחיות מחושבת על ההכנסה נטו — מה שנשאר אצלכם.</p>
      </div>
      <div class="lp-grid">{cards}</div>
      <p class="lp-fine">עלות = ללא מע״מ · מחיר מומלץ = כולל מע״מ 18% · רווח מחושב על ההכנסה נטו · עלות רכיבי המשקה בלבד · ללא גרניש</p>
    </div>
  </section>

  <section class="lp-sec lp-tinted">
    <div class="lp-wrap">
      <div class="lp-head rv">
        <span class="lp-eyebrow">מה צריך להחזיק</span>
        <h2 class="lp-display">{esc(cfg['need'])}</h2>
      </div>
      <ol class="lp-steps rv">
        <li><b>01</b><span>פותחים ומודדים</span></li>
        <li><b>02</b><span>מוסיפים קרח ונוזל</span></li>
        <li><b>03</b><span>מקשטים</span></li>
        <li><b>04</b><span>מגישים</span></li>
      </ol>
    </div>
  </section>

  <section class="lp-sec">
    <div class="lp-wrap">
      <div class="lp-head rv"><span class="lp-eyebrow">המוצר</span><h2 class="lp-display">{esc(p['name'])}</h2></div>
      <article class="lp-prod rv">
        <div class="lp-prod-ph">
          <img src="{{{{ '{p['imgs'][0]}' | asset_url }}}}" alt="{esc(p['name'])}" loading="lazy" decoding="async" width="640" height="640">
        </div>
        <div class="lp-prod-tx">
          <span class="lp-origin">{esc(p['origin'])}</span>
          <p class="lp-liner">{esc(p['liner'])}</p>
          <p class="lp-comp">{esc(p['comp'])}</p>
          <div class="lp-sizes">{sizes}</div>
          {yield_line}
        </div>
      </article>{extra}
    </div>
  </section>

  <section class="lp-sec lp-story">
    <div class="lp-wrap">
      <div class="rv">
        <span class="lp-eyebrow">מי אנחנו</span>
        <h2 class="lp-display">יצרנית בוטיק <em>ישראלית.</em></h2>
        <p>אנחנו חולטים עלי תה וצמחי מאכל באיכות מעולה מכל העולם ויוצרים מהם תמציות טבעיות ללא חומרים משמרים, להכנת מגוון אדיר של משקאות שמעניקים חוויה ולא רק שתייה.</p>
        <p class="lp-punch">אלו יהיו המשקאות הכי רווחיים שלך.</p>
      </div>
      <div class="rv">
        <ul>
          <li>נוצר במיוחד עבור בעלי בתי קפה ומסעדות.</li>
          <li>קל מאוד לתפעול ולהטמעה.</li>
          <li>באחסון סגור אינו מצריך קירור ואינו תופס מקום במקרר.</li>
        </ul>
        <p class="lp-punch">ברוכים הבאים לעולם חדש של משקאות GT.</p>
      </div>
    </div>
  </section>

  <section class="lp-sec lp-capture" id="lp-form">
    <div class="lp-wrap lp-cap-in">
      <div class="rv">
        <span class="lp-eyebrow">צור קשר</span>
        <h2 class="lp-display">נשלח לכם את <em>המחירון המלא.</em></h2>
        <p>השאירו פרטים ונחזור אליכם תוך יום עסקים אחד — עם המחירון, ההתאמה לתפריט שלכם, ותיאום טעימה.</p>
        <ul class="lp-contact">
          <li><a href="https://wa.me/{WA}?text={wa_txt}" target="_blank" rel="noopener">וואטסאפ · 054-398-2444</a></li>
          <li><a href="tel:+{WA}">חייגו · 054-398-2444</a></li>
          <li>הלהב 15, חולון · info@gteveryday.com</li>
        </ul>
      </div>
      <form class="lp-form rv" data-endpoint="{{{{ section.settings.lead_webhook | escape }}}}" data-source="site-{slug}" data-wa="{WA}" novalidate>
        <div class="lp-f-head"><b>קבלת מחירון</b><span>עונים תוך יום עסקים אחד</span></div>
        <div class="lp-f-row">
          <label><span>שם העסק *</span><input name="display_name" required autocomplete="organization"></label>
          <label><span>השם שלך *</span><input name="contact_name" required autocomplete="name"></label>
        </div>
        <div class="lp-f-row">
          <label><span>טלפון *</span><input name="phone" type="tel" required autocomplete="tel" inputmode="tel"></label>
          <label><span>עיר</span><input name="city" autocomplete="address-level2"></label>
        </div>
        <label class="lp-f-full"><span>אימייל</span><input name="email" type="email" autocomplete="email"></label>
        <label class="lp-f-ok"><input type="checkbox" name="consent" required> אני מאשר/ת פנייה בנוגע לאספקה סיטונאית.</label>
        <button type="submit" class="lp-btn lp-btn-full">שליחה <span aria-hidden="true">←</span></button>
        <p class="lp-f-msg" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>

  <footer class="lp-foot">
    <div class="lp-wrap">
      <span>© 2026 גרין טי אוורידיי בע״מ</span>
      <span class="lp-serif">Don't Drink Boring.</span>
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
    n = len([d for d in D if d['page']==cfg['key']])
    print(f"gt-lp-{slug}.liquid  {len(src):>6} B  · {n} drinks")
