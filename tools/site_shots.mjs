// Render-grade evidence for the brand site, read-only: the home page and the four category
// landing pages at phone and desktop widths, plus the states a visitor actually reaches (nav,
// recipe card, matrix, pricing, FAQ, the enquiry form in its error and sent states, keyboard
// focus), with facts.json beside the shots. iPad widths stay in
// gt-factory-os/api/scripts/site_ipad_shots.mjs; /site-gate runs both.
//
//   node tools/site_shots.mjs
//
// Env: UX_OUT (default /tmp/site-ux; writes site/shots/*.png and site/facts.json)
// · SITE_URL (default https://gteveryday.com/; a ?preview_theme_id= URL audits an unpublished copy)
// · SITE_VPS (e.g. p390,d1366: only these; facts.json is merged, so one width can be re-run)
// · UX_LP=0 skips the landing pages · UX_PERF=0 skips the slow-4G run · UX_PERF_RUNS (default 1)
// · AXE_JS (a local axe.min.js; otherwise fetched once from jsdelivr into UX_OUT)
// · PW_CHROME_PATH · PLAYWRIGHT_DIR · HTTPS_PROXY (honoured).
//
// The enquiry form is exercised against an intercepted endpoint: the POST to website_lead_intake
// never leaves the browser, so no lead is created and no alert is sent. Chromium only: Safari-only
// behaviour still needs a real device, and Linux has no Apple fonts.
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';

const { chromium } = createRequire(process.env.PLAYWRIGHT_DIR ?? '/opt/node22/lib/node_modules/')('playwright');
const ROOT = `${process.env.UX_OUT ?? '/tmp/site-ux'}/site`;
const OUT = `${ROOT}/shots`;
mkdirSync(OUT, { recursive: true });
const SITE = process.env.SITE_URL ?? 'https://gteveryday.com/';
const at = (q = '') => { const u = new URL(SITE); new URLSearchParams(q).forEach((v, k) => u.searchParams.set(k, v)); return u.href; };
const FACTS = `${ROOT}/facts.json`;
const ONLY = process.env.SITE_VPS ? new Set(process.env.SITE_VPS.split(',')) : null;
const facts = ONLY && existsSync(FACTS) ? JSON.parse(readFileSync(FACTS, 'utf8')) : {};
facts.site = SITE; facts.takenAt = new Date().toISOString();

// Phones are the cheapest Android in a kitchen; desktops are a laptop and a large office screen.
const ANDROID = 'Mozilla/5.0 (Linux; Android 13; SM-A135F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36';
const VPS = {
  p360: { w: 360, h: 780, mobile: true },
  p390: { w: 390, h: 844, mobile: true },
  d1366: { w: 1366, h: 768, mobile: false },
  d1920: { w: 1920, h: 1080, mobile: false },
};
const LEAD = '**/functions/v1/website_lead_intake';

// axe-core: a local copy if given, else fetched once and cached beside the evidence.
async function loadAxe() {
  const local = [process.env.AXE_JS, `${ROOT}/axe.min.js`].find((p) => p && existsSync(p));
  if (local) return readFileSync(local, 'utf8');
  try {
    const r = await fetch('https://cdn.jsdelivr.net/npm/axe-core@4.10.3/axe.min.js');
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const js = await r.text(); writeFileSync(`${ROOT}/axe.min.js`, js); return js;
  } catch (e) { facts.axeUnavailable = String(e.message); return null; }
}
const AXE = await loadAxe();

const browser = await chromium.launch({
  executablePath: process.env.PW_CHROME_PATH ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  ...(process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {}),
});

// Behind the agent proxy Chromium's trust store may lack the proxy CA while Node's has it: fetch
// on the Node side and hand the response to the page. TLS is still verified, by Node.
async function wire(ctx) {
  if (process.env.HTTPS_PROXY) await ctx.route('**/*', async (r) => { try { r.fulfill({ response: await r.fetch() }); } catch { r.abort(); } });
  // Registered last, so it wins: the lead endpoint answers from here and is never reached.
  await ctx.route(LEAD, async (r) => {
    const reply = await r.request().frame().page().evaluate(() => window.__leadReply ?? 'ok').catch(() => 'ok');
    // as the intake answers a stored lead: the page thanks only a reply that carries was_new
    const body = reply === 'ok' ? { ok: true, id: 'shot-fake', was_new: true } : { ok: false, error: reply };
    await sleep(600);
    r.fulfill({ status: reply === 'ok' ? 200 : 400, contentType: 'application/json', body: JSON.stringify(body) });
  });
}
const context = (vp, extra = {}) => browser.newContext({
  viewport: { width: vp.w, height: vp.h }, isMobile: vp.mobile, hasTouch: vp.mobile,
  deviceScaleFactor: vp.mobile ? 2 : 1, locale: 'he-IL', ...(vp.mobile ? { userAgent: ANDROID } : {}), ...extra,
});
const shot = (p, name, opts = {}) => p.screenshot({ path: `${OUT}/${name}.png`, ...opts });
const press = (el, vp) => (vp.mobile ? el.tap() : el.click());
const challenged = (p) => p.evaluate(() => /just a moment|cf-chl|attention required/i.test(document.title + ' ' + (document.body?.innerText.slice(0, 400) ?? '')));

// ── in-page probes ──
// elements sticking out horizontally, and the document width against the viewport
const probe = (p) => p.evaluate(() => {
  const W = innerWidth, out = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    if (r.width && (r.right > W + 1 || r.left < -1) && cs.position !== 'fixed' && !el.closest('[hidden],.hs-track,.ticker,.ptrack,#cmodal,#pmodal,#fmodal')) out.push(`${el.tagName.toLowerCase()}.${String(el.className).slice(0, 40)} ${Math.round(r.left)}→${Math.round(r.right)}`);
    if (out.length > 12) break;
  }
  return { scrollW: document.documentElement.scrollWidth, innerW: W, overflowX: document.documentElement.scrollWidth > W, sticking: out };
});
// interactive targets under 44 px on either side (visible ones only)
const smallTargets = (p) => p.evaluate(() => {
  const out = [];
  for (const el of document.querySelectorAll('a,button,input,select,textarea,summary,[role=button],[onclick]')) {
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.visibility === 'hidden' || cs.display === 'none' || el.closest('[hidden]')) continue;
    if (el.tabIndex < 0 && el.type === 'text') continue; // the honeypot
    if (r.width < 44 || r.height < 44) out.push(`${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}.${String(el.className).split(' ')[0]} "${(el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 28)}" ${Math.round(r.width)}×${Math.round(r.height)}`);
    if (out.length >= 40) break;
  }
  return out;
});
// what is on the first screen, and how the nav presents itself
const firstScreen = (p) => p.evaluate(() => {
  const H = innerHeight, W = innerWidth, seen = [];
  for (const el of document.querySelectorAll('h1,h2,h3,p,a,button,[class*=eyebrow],[class*=kicker]')) {
    const r = el.getBoundingClientRect(); if (r.bottom <= 0 || r.top >= H || !r.height) continue;
    // actually visible: the point at its centre hits the element itself, not a folded menu's clip or an overlay
    const hit = document.elementFromPoint(Math.min(W - 1, Math.max(0, r.left + r.width / 2)), Math.min(H - 1, Math.max(0, r.top + r.height / 2)));
    if (!hit || !el.contains(hit)) continue;
    const t = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' '); if (t) seen.push(`${el.tagName.toLowerCase()}: ${t.slice(0, 120)}`);
    if (seen.length >= 24) break;
  }
  const nl = document.getElementById('nav-links'); const b = document.querySelector('.nav-burger');
  const entry = [...document.querySelectorAll('a')].find((a) => /כניס(ה|ת) (לעסקים|לקוחות)/.test(a.textContent) && a.getBoundingClientRect().height > 0);
  return {
    h1: document.querySelector('h1')?.textContent.trim().slice(0, 160) ?? null,
    h1Visible: !!document.querySelector('h1') && getComputedStyle(document.querySelector('h1')).clipPath === 'none' && document.querySelector('h1').getBoundingClientRect().height > 1,
    text: seen,
    nav: { linksVisible: !!nl && nl.getBoundingClientRect().width > 0 && getComputedStyle(nl).display !== 'none', burgerVisible: !!b && b.getBoundingClientRect().width > 0, entryText: entry?.textContent.trim() ?? null, entryHref: entry?.getAttribute('href') ?? null },
  };
});
// the recipe card's geometry (the checks the iPad gate settled, re-read at these widths)
const geo = (p) => p.evaluate(() => {
  const q = (s) => document.querySelector(s), R = (s) => q(s)?.getBoundingClientRect();
  const m = q('#cmodal'), card = q('#cmodal .cm-card'), body = q('#cmodal .cm-body'), c = R('#cmodal .cm-card'), head = R('#cmodal .cm-head'), next = R('#cm-next');
  if (!m || !card || !c) return { open: false };
  return { open: m.classList.contains('open'), card: { top: Math.round(c.top), bottom: Math.round(c.bottom), w: Math.round(c.width), h: Math.round(c.height) }, vh: innerHeight,
    cardScrollFits: card.scrollHeight === card.clientHeight, bodyScrollTop: body?.scrollTop ?? null, headInCard: !!head && head.top >= c.top - 1 && head.bottom <= innerHeight, nextInCard: !!next && next.bottom <= c.bottom + 1,
    pageLocked: getComputedStyle(document.documentElement).overflow === 'hidden', hash: location.hash, cmI: typeof cmI === 'undefined' ? null : cmI };
});
// per-section visible text, for the copy reviewers
const sections = (p) => p.evaluate(() => Object.fromEntries([...document.querySelectorAll('section[id],footer')].map((s) => [s.id || s.tagName.toLowerCase(), (s.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 700)])));
const media = (p) => p.evaluate(() => {
  const imgs = [...document.images];
  return { images: imgs.length, withoutSize: imgs.filter((i) => !i.getAttribute('width') || !i.getAttribute('height')).length, lazy: imgs.filter((i) => i.loading === 'lazy').length, broken: imgs.filter((i) => i.complete && i.naturalWidth === 0 && i.getBoundingClientRect().width > 0).length,
    fonts: [...document.fonts].map((f) => `${f.family} ${f.weight} ${f.status}`).filter((v, i, a) => a.indexOf(v) === i).slice(0, 20), lang: document.documentElement.lang, dir: document.documentElement.dir };
});
async function axe(p, name, store) {
  if (!AXE) return;
  try {
    await p.addScriptTag({ content: AXE });
    const res = await p.evaluate(async () => { const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } }); return r.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, first: v.nodes[0]?.target?.join(' ').slice(0, 90), help: v.help })); });
    store[name] = res;
  } catch (e) { store[name] = { FAILED: String(e.message).split('\n')[0] }; }
}
async function scrollThrough(p) {
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 600) { await p.evaluate((yy) => window.scrollTo(0, yy), y); await sleep(120); }
  await sleep(600);
}
const go = async (p, url) => { await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); await sleep(3500); if (await challenged(p)) throw new Error('Cloudflare challenge — re-run this width with SITE_VPS'); };

// ── the walk ──
for (const [name, vp] of Object.entries(VPS).filter(([k]) => !ONLY || ONLY.has(k))) {
  const f = { vp: `${vp.w}×${vp.h}${vp.mobile ? ' touch @2x' : ''}` }; facts[name] = f; f.axe = {};
  const ctx = await context(vp); await wire(ctx);
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(e.message.slice(0, 120)));
  const runAxe = name === 'p390' || name === 'd1366';
  try {
    // 1. home: first screen, whole page, nav
    await go(p, at());
    await shot(p, `${name}-01-top`);
    f.first = await firstScreen(p); f.probe = await probe(p); f.media = await media(p);
    if (vp.mobile) f.smallTargets = await smallTargets(p);
    if (name === 'p390') f.sections = await sections(p);
    if (runAxe) await axe(p, 'home', f.axe);
    await shot(p, `${name}-02-full`, { fullPage: true });
    if (vp.mobile) {
      const b = await p.$('.nav-burger');
      if (b) { await b.tap(); await sleep(900); await shot(p, `${name}-03-nav-open`); f.navOpen = await p.evaluate(() => ({ open: !!document.querySelector('nav.open'), links: [...document.querySelectorAll('#nav-links a')].filter((a) => a.getBoundingClientRect().height > 0).map((a) => a.textContent.trim().slice(0, 30)) })); await b.tap(); await sleep(500); }
    } else {
      const dd = await p.$('.nav-dd > a');
      if (dd) { await dd.hover(); await sleep(800); await shot(p, `${name}-03-nav-products-hover`); f.ddMenuVisible = await p.evaluate(() => { const m = document.querySelector('.dd-menu'); return !!m && getComputedStyle(m).visibility !== 'hidden' && m.getBoundingClientRect().height > 0; }); await p.mouse.move(5, 5); }
    }
    // 2. drinks and the recipe card
    await p.evaluate(() => document.getElementById('drinks')?.scrollIntoView()); await sleep(1500);
    await shot(p, `${name}-04-drinks`);
    const cc = await p.$('.ccard');
    if (cc) {
      await cc.scrollIntoViewIfNeeded(); await press(cc, vp); await sleep(1500);
      await shot(p, `${name}-05-recipe`); f.recipe = await geo(p);
      if (runAxe) await axe(p, 'recipe', f.axe);
      const nx = await p.$('#cm-next'); if (nx) { await press(nx, vp); await sleep(900); await shot(p, `${name}-06-recipe-next`); f.recipeAfterNext = await geo(p); }
      await p.keyboard.press('Escape'); await sleep(600);
      f.recipeEscapeCloses = !(await geo(p)).open;
      if (!f.recipeEscapeCloses) { const x = await p.$('#cmodal .cm-x'); if (x) { await press(x, vp); await sleep(600); } }
    }
    // 3. the "one bottle, many cups" matrix, the price list, the FAQ
    const tog = await p.$('#mxtog');
    if (tog) { await tog.scrollIntoViewIfNeeded(); await press(tog, vp); await sleep(1200); await shot(p, `${name}-07-matrix-open`); f.matrixProbe = await probe(p); await press(tog, vp); await sleep(500); }
    if (await p.$('#pricing')) {
      await p.evaluate(() => document.getElementById('pricing')?.scrollIntoView()); await sleep(1200); await shot(p, `${name}-08-pricing`);
      f.pricing = await p.evaluate(() => { const s = document.getElementById('pricing'); const t = s?.innerText ?? ''; return { present: true, visible: !!s && s.getBoundingClientRect().height > 0, shekelTokens: (t.match(/₪\s?\d|\d\s?₪|ש"ח|שח\b/g) || []).length, chars: t.length }; });
    } else f.pricing = { present: false, note: 'no #pricing section on this page: the price list is off (show_pricing) or gone' };
    // a ₪ figure anywhere on the page, for the money check (BRIEF §4) whatever the switch says
    f.shekelOnPage = await p.evaluate(() => (document.body.innerText.match(/₪\s?\d[\d,.]*|\d[\d,.]*\s?₪/g) || []).slice(0, 12));
    if (await p.$('#faq details')) {
      await p.evaluate(() => document.getElementById('faq')?.scrollIntoView()); await sleep(800);
      const sm = await p.$('#faq details summary'); if (sm) { await press(sm, vp); await sleep(700); }
      await shot(p, `${name}-09-faq-open`);
    }
    // 4. the enquiry form: empty submit, a rejected send, a confirmed send — all intercepted
    const form = await p.$('#pform');
    if (form) {
      await p.evaluate(() => document.getElementById('contact')?.scrollIntoView()); await sleep(900);
      await shot(p, `${name}-10-form`);
      if (runAxe) await axe(p, 'form', f.axe);
      // the form asks first whether the visitor has a business (patch_lead_dialog.py); the send button is
      // the form's own child, not one of the answers
      const yes = await p.$('#pform [data-biz="1"]');
      if (yes && await yes.isVisible()) { await press(yes, vp); await sleep(700); }
      const btn = await p.$('#pform>button.btn');
      await press(btn, vp); await sleep(600);
      f.formEmptySubmit = await p.evaluate(() => ({ invalid: document.querySelectorAll('#pform :invalid').length, firstInvalid: document.querySelector('#pform :invalid')?.id ?? null, focused: document.activeElement?.id ?? null, sent: document.getElementById('pform').classList.contains('sent') }));
      const fill = async () => { await p.fill('#pf-name', 'בדיקה אוטומטית'); await p.fill('#pf-venue', 'קפה בדיקה'); await p.fill('#pf-city', 'תל אביב'); await p.fill('#pf-phone', '0501234567'); await p.check('#pf-agree'); };
      await fill(); await p.evaluate(() => { window.__leadReply = 'bad_phone'; });
      await press(btn, vp); await sleep(1600); await shot(p, `${name}-11-form-error`);
      f.formError = await p.evaluate(() => ({ shown: !document.getElementById('pf-err').hidden, text: document.getElementById('pf-err').innerText.trim().slice(0, 200), button: document.querySelector('#pform>button.btn').innerText.trim(), disabled: document.querySelector('#pform>button.btn').disabled }));
      await p.evaluate(() => { window.__leadReply = 'ok'; });
      await press(btn, vp); await sleep(1600); await shot(p, `${name}-12-form-sent`);
      f.formSent = await p.evaluate(() => ({ sent: document.getElementById('pform').classList.contains('sent'), button: document.querySelector('#pform>button.btn').innerText.trim(), done: document.getElementById('pf-done').innerText.replace(/\s+/g, ' ').trim().slice(0, 200), generateLead: (window.dataLayer || []).some((e) => e && e.event === 'generate_lead') }));
      await shot(p, `${name}-13-footer`);
    }
    // 5. keyboard: the first stops from the top of the page, and whether focus is visible
    await go(p, at());
    const stops = [];
    for (let i = 0; i < 10; i++) {
      await p.keyboard.press('Tab'); await sleep(120);
      stops.push(await p.evaluate(() => { const a = document.activeElement; if (!a || a === document.body) return 'body'; const cs = getComputedStyle(a); const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || cs.boxShadow !== 'none'; return `${a.tagName.toLowerCase()}${a.id ? '#' + a.id : ''}.${String(a.className).split(' ')[0]} "${(a.getAttribute('aria-label') || a.textContent || '').trim().slice(0, 24)}"${ring ? '' : ' NO-RING'}`; }));
    }
    f.tabOrder = stops; await shot(p, `${name}-20-focus`);
    await ctx.close();
    // 6. reduced motion (one width is enough): does the hero hold, does the ticker stand still
    if (name === 'p390') {
      const c2 = await context(vp, { reducedMotion: 'reduce' }); await wire(c2); const p2 = await c2.newPage();
      await go(p2, at()); const i0 = await p2.evaluate(() => (typeof hsI === 'undefined' ? null : hsI)); await sleep(6000);
      f.reducedMotion = await p2.evaluate((i0) => ({ heroAdvanced: typeof hsI !== 'undefined' && hsI !== i0, tickerAnimation: document.querySelector('.ticker *') ? getComputedStyle(document.querySelector('.ticker > *') || document.querySelector('.ticker')).animationName : null }), i0);
      await c2.close();
    }
    // 7. the four category landing pages
    if (process.env.UX_LP !== '0') {
      const c3 = await context(vp); await wire(c3); const p3 = await c3.newPage();
      for (const slug of ['chai', 'matcha', 'iced-tea', 'ube']) {
        const lp = {}; f[`lp-${slug}`] = lp;
        try {
          await go(p3, at(`view=${slug}`));
          await shot(p3, `${name}-lp-${slug}-01-top`);
          lp.first = await firstScreen(p3); lp.probe = await probe(p3);
          await scrollThrough(p3);
          lp.reveal = await p3.evaluate(() => { const cards = [...document.querySelectorAll('.g-lp .g-drink')]; return { cards: cards.length, stillHidden: cards.filter((c) => parseFloat(getComputedStyle(c).opacity) < 0.5).length, isLandingPage: !!document.querySelector('.g-lp') }; });
          const hs0 = await p3.evaluate(() => [...document.querySelectorAll('.g-lp .g-drink')].map((c) => c.offsetHeight));
          const sm = await p3.$('.g-lp .g-drink summary');
          if (sm) { await sm.scrollIntoViewIfNeeded(); await press(sm, vp).catch(() => {}); await sleep(700); await shot(p3, `${name}-lp-${slug}-02-card-open`); const hs1 = await p3.evaluate(() => [...document.querySelectorAll('.g-lp .g-drink')].map((c) => c.offsetHeight)); lp.otherCardsResized = hs1.filter((h, i) => i > 0 && Math.abs(h - hs0[i]) > 2).length; }
          if (name === 'p390' || name === 'd1366') await shot(p3, `${name}-lp-${slug}-03-full`, { fullPage: true });
          if (vp.mobile) lp.smallTargets = (await smallTargets(p3)).slice(0, 15);
        } catch (e) { lp.FAILED = String(e.message).split('\n')[0]; }
      }
      await c3.close();
    }
  } catch (e) { f.FAILED = String(e.message).split('\n')[0]; await ctx.close().catch(() => {}); }
  f.errors = errs;
}

// ── performance: a phone on slow 4G with a 4× slower CPU, cold cache, against the real CDN ──
if (process.env.UX_PERF !== '0' && (!ONLY || ONLY.has('p390') || ONLY.has('perf'))) {
  const runs = [];
  for (let i = 0; i < Number(process.env.UX_PERF_RUNS ?? 1); i++) {
    const ctx = await context(VPS.p390); await wire(ctx); const p = await ctx.newPage();
    try {
      const cdp = await ctx.newCDPSession(p);
      await cdp.send('Network.enable');
      await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: (1.6 * 1024 * 1024) / 8, uploadThroughput: (750 * 1024) / 8 });
      await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
      const bytes = {}, types = {};
      cdp.on('Network.loadingFinished', (e) => { bytes[e.requestId] = e.encodedDataLength; });
      cdp.on('Network.responseReceived', (e) => { types[e.requestId] = `${e.type} ${e.response.url.split('?')[0].slice(-60)}`; });
      await p.addInitScript(() => {
        window.__lcp = 0; window.__cls = 0; window.__clsSrc = [];
        new PerformanceObserver((l) => { for (const e of l.getEntries()) { window.__lcp = e.startTime; window.__lcpEl = e.element ? `${e.element.tagName.toLowerCase()}${e.element.id ? '#' + e.element.id : ''}.${String(e.element.className).split(' ')[0]}` : e.url; } }).observe({ type: 'largest-contentful-paint', buffered: true });
        new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) { window.__cls += e.value; window.__clsSrc.push({ t: Math.round(e.startTime), v: +e.value.toFixed(4), nodes: (e.sources ?? []).map((s) => s.node ? `${s.node.tagName?.toLowerCase()}${s.node.id ? '#' + s.node.id : ''}.${String(s.node.className).split(' ')[0]}` : '?') }); } }).observe({ type: 'layout-shift', buffered: true });
      });
      const t0 = Date.now();
      await p.goto(at(), { waitUntil: 'load', timeout: 120000 }); await sleep(4000);
      const m = await p.evaluate(() => ({ fcp: Math.round(performance.getEntriesByName('first-contentful-paint')[0]?.startTime ?? 0), lcp: Math.round(window.__lcp), lcpElement: window.__lcpEl ?? null, cls: +window.__cls.toFixed(4), clsSources: window.__clsSrc.sort((a, b) => b.v - a.v).slice(0, 6), load: performance.timing.loadEventEnd - performance.timing.navigationStart, dom: document.getElementsByTagName('*').length, fontsLoaded: [...document.fonts].filter((f) => f.status === 'loaded').length }));
      const byType = {}; for (const [id, b] of Object.entries(bytes)) { const k = (types[id] ?? '?').split(' ')[0]; byType[k] = (byType[k] ?? 0) + b; }
      const biggest = Object.entries(bytes).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([id, b]) => `${Math.round(b / 1024)} KB ${types[id] ?? '?'}`);
      runs.push({ ...m, kb: Math.round(Object.values(bytes).reduce((a, b) => a + b, 0) / 1024), requests: Object.keys(bytes).length, kbByType: Object.fromEntries(Object.entries(byType).map(([k, v]) => [k, Math.round(v / 1024)])), biggest, wallMs: Date.now() - t0 });
    } catch (e) { facts.perfFAILED = String(e.message).split('\n')[0]; }
    await ctx.close();
  }
  if (runs.length) {
    const med = (k) => { const v = runs.map((r) => r[k]).sort((a, b) => a - b); return v[Math.floor(v.length / 2)]; };
    facts.perf = { note: 'p390, Android UA, cold cache, slow 4G 1.6 Mbps / 150 ms RTT, CPU ×4; the real CDN, so this is close to what a visitor gets', runs: runs.length, lcp: med('lcp'), fcp: med('fcp'), cls: med('cls'), kb: med('kb'), requests: med('requests'), last: runs[runs.length - 1] };
    facts.perfBudget = { lcpGoodLe2500: facts.perf.lcp <= 2500, clsGoodLe0_1: facts.perf.cls <= 0.1, kbLe1500: facts.perf.kb <= 1500 };
  }
}

await browser.close();
writeFileSync(FACTS, JSON.stringify(facts, null, 1));
const vps = Object.keys(VPS).filter((k) => facts[k]);
console.log(JSON.stringify({
  out: OUT, facts: FACTS, viewports: vps,
  failed: vps.filter((k) => facts[k].FAILED).map((k) => `${k}: ${facts[k].FAILED}`),
  overflowX: Object.fromEntries(vps.map((k) => [k, facts[k].probe?.overflowX ?? null])),
  smallTargets: Object.fromEntries(vps.filter((k) => facts[k].smallTargets).map((k) => [k, facts[k].smallTargets.length])),
  axeViolations: Object.fromEntries(vps.filter((k) => facts[k].axe && Object.keys(facts[k].axe).length).map((k) => [k, Object.fromEntries(Object.entries(facts[k].axe).map(([s, v]) => [s, Array.isArray(v) ? v.length : v]))])),
  form: Object.fromEntries(vps.filter((k) => facts[k].formSent).map((k) => [k, { emptyInvalid: facts[k].formEmptySubmit?.invalid, errorShown: facts[k].formError?.shown, sent: facts[k].formSent?.sent, generateLead: facts[k].formSent?.generateLead }])),
  perf: facts.perf && { lcp: facts.perf.lcp, cls: facts.perf.cls, kb: facts.perf.kb, requests: facts.perf.requests, budget: facts.perfBudget },
  axeUnavailable: facts.axeUnavailable, perfFAILED: facts.perfFAILED,
}, null, 1));
