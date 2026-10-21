#!/usr/bin/env node
// Runs the ppc-reporting dashboard script against a small DOM stub and checks
// which currency each money cell is printed in. No browser, no network.
//
//   node tests/dashboard_probe.cjs fixture <case>      print the case's DATA.json
//   node tests/dashboard_probe.cjs check <html> <case> run the page, assert, exit 0/1
//   node tests/dashboard_probe.cjs dump <html>         print every element's rendered state
//
// Cases: mixed (Google EUR, TikTok JPY), tiktok-only (TikTok JPY, no Google
// currency), tiktok-unknown (TikTok without a currency), google-only (no
// TikTok block), hostile (markup in the TikTok currency and advertiser).
'use strict';
const fs = require('fs');
const vm = require('vm');

const period = { label: 'Last 7 days', start: '2026-10-14', end: '2026-10-20' };
const previous = { label: 'Previous 7 days', start: '2026-10-07', end: '2026-10-13' };
const meta = (extra) => Object.assign({ account: 'Probe account', period, previous, generated_at: '2026-10-21T00:00:00Z' }, extra);
const ads = {
  current: { cost: 500, impressions: 10000, clicks: 250, conversions: 10, conversion_value: 2000 },
  previous: { cost: 400, impressions: 9000, clicks: 200, conversions: 8, conversion_value: 1500 },
  daily: { dates: ['10-19', '10-20'], cost: [200, 300], conversions: [4, 6], clicks: [100, 150] },
  campaigns: [{ name: 'Search', status: 'ENABLED', cost: 500, impressions: 10000, clicks: 250, conversions: 10, conversion_value: 2000 }],
  wasted_spend: [{ search_term: 'free stuff', campaign: 'Search', cost: 25, clicks: 9, conversions: 0 }],
};
const tiktok = (extra) => Object.assign({
  advertiser: 'Probe advertiser',
  current: { cost: 120, impressions: 1000, clicks: 40, conversions: 4 },
  campaigns: [{ name: 'Spark', status: 'ENABLE', cost: 120, impressions: 1000, clicks: 40, conversions: 4 }],
}, extra);

const FIXTURES = {
  mixed: { meta: meta({ currency: 'EUR' }), ads, tiktok: tiktok({ currency: 'JPY' }) },
  'tiktok-only': { meta: meta({}), tiktok: tiktok({ currency: 'JPY' }) },
  'tiktok-unknown': { meta: meta({ currency: 'EUR' }), ads, tiktok: tiktok({}) },
  'google-only': { meta: meta({ currency: 'EUR' }), ads },
  hostile: { meta: meta({ currency: 'EUR' }), ads, tiktok: tiktok({ currency: '<img src=x onerror=alert(1)>', advertiser: '</script><b>x</b>' }) },
};

// ---- DOM stub: just enough of the DOM for the page script ----
class El {
  constructor(tag, id) {
    this.tagName = tag; this.id = id || ''; this.children = []; this._text = ''; this._html = '';
    this.className = ''; this.hidden = false; this.style = {}; this.dataset = {}; this.attrs = {};
    this._q = new Map(); this.ths = [];
    this.classList = { contains: (c) => this.className.split(/\s+/).includes(c) };
  }
  get textContent() { return this._text + this.children.map((c) => c.textContent).join(''); }
  set textContent(v) { this._text = String(v); this.children = []; }
  get innerHTML() { return this._html; }
  set innerHTML(v) { this._html = String(v); this._text = ''; this.children = []; if (this._html) this.children.push(new El('svg')); }
  get firstChild() { return this.children[0] || null; }
  appendChild(c) { this.children.push(c); return c; }
  insertAdjacentHTML(pos, s) { this._html += s; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  addEventListener() {}
  querySelector(sel) { if (!this._q.has(sel)) this._q.set(sel, new El(sel)); return this._q.get(sel); }
  querySelectorAll(sel) { return sel === 'th' ? this.ths : []; }
}

function run(html) {
  const dataM = html.match(/<script id="ppc-data" type="application\/json">([\s\S]*?)<\/script>/);
  if (!dataM) throw new Error('no ppc-data block');
  const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
  const els = new Map();
  const byId = (id) => {
    if (!els.has(id)) {
      const e = new El('div', id);
      if (id === 'ppc-data') e._text = dataM[1];
      if (new RegExp('<[a-z0-9]+ [^>]*id="' + id + '"[^>]*\\shidden[\\s>]').test(html)) e.hidden = true;
      const t = html.match(new RegExp('<table id="' + id + '"><thead><tr>([\\s\\S]*?)</tr></thead>'));
      if (t) e.ths = [...t[1].matchAll(/<th([^>]*)>([^<]*)<\/th>/g)].map((m) => {
        const th = new El('th'); const k = m[1].match(/data-k="([^"]*)"/); const c = m[1].match(/class="([^"]*)"/);
        if (k) th.dataset.k = k[1]; if (c) th.className = c[1]; th.textContent = m[2]; return th;
      });
      els.set(id, e);
    }
    return els.get(id);
  };
  const document = {
    getElementById: byId,
    createElement: (tag) => new El(tag),
    createTextNode: (v) => ({ textContent: String(v) }),
  };
  vm.runInNewContext(code, { document, Intl, Math, JSON, String, Number, Object, Array, RegExp, console });
  return { byId, els };
}

const fmt = (code, frac) => (v) => new Intl.NumberFormat(undefined, { style: 'currency', currency: code, maximumFractionDigits: frac }).format(v);
const plain = (frac) => (v) => new Intl.NumberFormat(undefined, { maximumFractionDigits: frac }).format(v);
const sym = (code) => new Intl.NumberFormat(undefined, { style: 'currency', currency: code }).formatToParts(1).find((p) => p.type === 'currency').value;

function kpis(r, id) { return r.byId(id).children.map((k) => ({ label: k.children[0].textContent, value: k.children[1].textContent })); }
function kpi(r, id, label) { const k = kpis(r, id).find((x) => x.label.replace(/ \(currency unknown\)$/, '') === label); return k ? k.value : undefined; }
function rows(r, id) { return r.byId(id).querySelector('tbody').children.map((tr) => tr.children.map((td) => td.textContent)); }
function ttText(r) { return [r.byId('tt-sub'), r.byId('tt-kpis'), r.byId('tt-campaigns').querySelector('tbody')].map((e) => e.textContent).join(' | ') + ' | ' + r.byId('tt-campaigns').ths.map((t) => t.textContent).join(' '); }

function check(html, name) {
  const errs = [];
  const eq = (what, got, want) => { if (got !== want) errs.push(`${what}: got ${JSON.stringify(got)}, want ${JSON.stringify(want)}`); };
  const no = (what, hay, needle) => { if (hay.includes(needle)) errs.push(`${what}: found ${JSON.stringify(needle)} in ${JSON.stringify(hay)}`); };
  const has = (what, hay, needle) => { if (!hay.includes(needle)) errs.push(`${what}: missing ${JSON.stringify(needle)} in ${JSON.stringify(hay)}`); };
  const r = run(html);
  const tt = () => ttText(r);
  // TikTok campaign row: name, status, cost, impr, clicks, ctr, cpc, conv, cpa
  const ttMoneyCells = (money0, money2) => {
    eq('tiktok kpi Cost', kpi(r, 'tt-kpis', 'Cost'), money0(120));
    eq('tiktok kpi Avg. CPC', kpi(r, 'tt-kpis', 'Avg. CPC'), money2(3));
    eq('tiktok kpi Cost per conversion', kpi(r, 'tt-kpis', 'Cost per conversion'), money2(30));
    const row = rows(r, 'tt-campaigns')[0] || [];
    eq('tiktok campaign cost', row[2], money0(120));
    eq('tiktok campaign cpc', row[6], money2(3));
    eq('tiktok campaign cpa', row[8], money2(30));
  };
  const googleMoney = () => {
    eq('google kpi Cost', kpi(r, 'kpis', 'Cost'), fmt('EUR', 0)(500));
    eq('google kpi Avg. CPC', kpi(r, 'kpis', 'Avg. CPC'), fmt('EUR', 2)(2));
    eq('google campaign cost', (rows(r, 'campaigns')[0] || [])[2], fmt('EUR', 0)(500));
    eq('sec-ads hidden', r.byId('sec-ads').hidden, false);
  };
  if (name === 'mixed') {
    googleMoney();
    eq('sec-tt hidden', r.byId('sec-tt').hidden, false);
    ttMoneyCells(fmt('JPY', 0), fmt('JPY', 2));
    no('sec-tt', tt(), 'EUR'); no('sec-tt', tt(), sym('EUR')); has('tt-sub', r.byId('tt-sub').textContent, 'JPY');
    has('currency chip', r.byId('currency-chip').textContent, 'EUR'); has('currency chip', r.byId('currency-chip').textContent, 'JPY');
  } else if (name === 'tiktok-only') {
    eq('sec-ads hidden', r.byId('sec-ads').hidden, true);
    ttMoneyCells(fmt('JPY', 0), fmt('JPY', 2));
    no('sec-tt', tt(), 'USD'); no('sec-tt', tt(), sym('USD')); has('tt-sub', r.byId('tt-sub').textContent, 'JPY');
    eq('currency chip', r.byId('currency-chip').textContent, 'JPY');
  } else if (name === 'tiktok-unknown' || name === 'hostile') {
    googleMoney();
    ttMoneyCells(plain(0), plain(2));
    for (const l of ['Cost', 'Cost per conversion', 'Avg. CPC']) has('tiktok kpi label', (kpis(r, 'tt-kpis').find((k) => k.label.startsWith(l + ' (')) || { label: l }).label, 'currency unknown');
    has('tt-sub', r.byId('tt-sub').textContent, 'currency unknown');
    for (const s of ['EUR', sym('EUR'), 'USD', sym('USD'), 'JPY', sym('JPY')]) no('sec-tt', tt(), s);
    has('currency chip', r.byId('currency-chip').textContent, 'EUR'); has('currency chip', r.byId('currency-chip').textContent, 'unknown');
    if (name === 'hostile') {
      const block = html.match(/<script id="ppc-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
      no('ppc-data block', block, '<');
      has('tt-sub', r.byId('tt-sub').textContent, '</script><b>x</b>');
      no('sec-tt', tt(), '<img');
    }
  } else if (name === 'google-only') {
    googleMoney();
    eq('sec-tt hidden', r.byId('sec-tt').hidden, true);
    eq('currency chip', r.byId('currency-chip').textContent, 'EUR');
    eq('waste total', r.byId('waste-total').textContent, fmt('EUR', 2)(25) + ' spent on 1 zero-conversion terms (5.0% of period cost)');
  } else {
    errs.push('unknown case ' + name);
  }
  return errs;
}

function dump(html) {
  const r = run(html);
  const ser = (e) => (e instanceof El ? { tag: e.tagName, cls: e.className, hidden: e.hidden, text: e._text, html: e._html, style: e.style, attrs: e.attrs,
    kids: e.children.map(ser), q: [...e._q].map(([k, v]) => [k, ser(v)]), ths: e.ths.map(ser) } : { node: e.textContent });
  return JSON.stringify([...r.els].filter(([id]) => id !== 'ppc-data').map(([id, e]) => [id, ser(e)]), null, 1);
}

const [mode, a, b] = process.argv.slice(2);
if (mode === 'fixture' && FIXTURES[a]) { process.stdout.write(JSON.stringify(FIXTURES[a], null, 2) + '\n'); }
else if (mode === 'check' && a && b) {
  let errs;
  try { errs = check(fs.readFileSync(a, 'utf8'), b); } catch (e) { errs = ['page script threw: ' + (e && e.stack || e)]; }
  if (errs.length) { errs.forEach((e) => console.log(`FAIL ${b}: ${e}`)); process.exit(1); }
  console.log(`OK ${b}`);
} else if (mode === 'dump' && a) { process.stdout.write(dump(fs.readFileSync(a, 'utf8')) + '\n'); }
else { console.error('usage: dashboard_probe.cjs fixture <case> | check <html> <case> | dump <html>\ncases: ' + Object.keys(FIXTURES).join(', ')); process.exit(2); }
