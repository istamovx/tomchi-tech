/**
 * Tomchi Tech — Shared API Client & Integration Config
 * =====================================================
 * Barcha sahifalarda ishlatiladigan markazlashgan konfiguratsiya.
 * Kalitlar localStorage da saqlanadi (settings.html orqali kiritiladi).
 *
 * Ishlatish:
 *   <script src="../js/tomchi-api.js"></script>
 *   const data = await TOMCHI.get('/recommendations/');
 */

const TOMCHI = (function () {

  /* ── Standart qiymatlar ──────────────────────────────────────── */
  const DEFAULTS = {
    api:     { base: 'https://tomchi-tech-api.onrender.com/api/v1', key: '' },
    myid:    { enabled: false, clientId: '', clientSecret: '', sandbox: 'true' },
    egov:    { enabled: false, apiKey: '', base: 'https://api.egov.uz/v1' },
    kadastr: { enabled: false, token: '', base: 'https://api.kadastr.uz/v1' },
    agro:    { enabled: false, token: '', base: 'https://api.agro.uz/v1' },
    soliq:   { enabled: false, tin: '', token: '' },
    payme:   { enabled: false, merchantId: '', key: '', testMode: 'true' },
    click:   { enabled: false, merchantId: '', serviceId: '', secretKey: '', testMode: 'true' },
    uzum:    { enabled: false, shopId: '', token: '', testMode: 'true' },
    bot:     { alertsApiUrl: 'http://localhost:8787', alertsSecret: '' },
  };

  const LS_KEY = 'tomchi_cfg_v1';

  /* ── Config yuklash / saqlash ────────────────────────────────── */
  function loadCfg() {
    try {
      const saved = JSON.parse(localStorage.getItem(LS_KEY) || '{}');
      return deepMerge(DEFAULTS, saved);
    } catch { return { ...DEFAULTS }; }
  }

  function saveCfg(cfg) {
    localStorage.setItem(LS_KEY, JSON.stringify(cfg));
  }

  function patchCfg(section, fields) {
    const cfg = loadCfg();
    cfg[section] = { ...cfg[section], ...fields };
    saveCfg(cfg);
    return cfg;
  }

  function deepMerge(base, over) {
    const r = { ...base };
    for (const k in over) {
      if (over[k] !== null && typeof over[k] === 'object' && !Array.isArray(over[k])) {
        r[k] = deepMerge(base[k] || {}, over[k]);
      } else {
        r[k] = over[k];
      }
    }
    return r;
  }

  /* ── Asosiy API fetch ────────────────────────────────────────── */
  async function apiFetch(path, options = {}) {
    const cfg = loadCfg();
    const url = cfg.api.base + path;
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
    if (cfg.api.key) headers['X-API-Key'] = cfg.api.key;
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
    return res.json();
  }

  const get  = (path)       => apiFetch(path);
  const post = (path, body) => apiFetch(path, { method: 'POST', body: JSON.stringify(body) });
  const put  = (path, body) => apiFetch(path, { method: 'PUT',  body: JSON.stringify(body) });
  const del  = (path)       => apiFetch(path, { method: 'DELETE' });

  /* ── MyID (my.gov.uz) ────────────────────────────────────────── */
  async function myidVerify(pinfl) {
    const { myid } = loadCfg();
    if (!myid.enabled) throw new Error('MyID faol emas — Sozlamalar > Davlat tizimlari');
    const base = myid.sandbox === 'true' ? 'https://sandbox.myid.uz' : 'https://api.myid.uz';
    const tok = await fetch(`${base}/oauth2/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `grant_type=client_credentials&client_id=${myid.clientId}&client_secret=${myid.clientSecret}`
    }).then(r => r.json());
    return fetch(`${base}/api/v1/identification?pinfl=${pinfl}`, {
      headers: { Authorization: `Bearer ${tok.access_token}` }
    }).then(r => r.json());
  }

  /* ── Kadastr (kadastr.uz) ────────────────────────────────────── */
  async function kadastrLookup(cadNumber) {
    const { kadastr } = loadCfg();
    if (!kadastr.enabled) throw new Error('Kadastr faol emas');
    const r = await fetch(`${kadastr.base}/parcel/${cadNumber}`, {
      headers: { Authorization: `Bearer ${kadastr.token}` }
    });
    return r.json();
  }

  /* ── Agro API (agro.uz) ──────────────────────────────────────── */
  async function agroFarm(inn) {
    const { agro } = loadCfg();
    if (!agro.enabled) throw new Error('Agro vazirligi faol emas');
    const r = await fetch(`${agro.base}/farms/${inn}`, {
      headers: { Authorization: `Bearer ${agro.token}` }
    });
    return r.json();
  }

  async function agroIrrigationNorms(crop, regionId) {
    const { agro } = loadCfg();
    if (!agro.enabled) throw new Error('Agro vazirligi faol emas');
    const r = await fetch(`${agro.base}/norms/irrigation?crop=${crop}&region=${regionId}`, {
      headers: { Authorization: `Bearer ${agro.token}` }
    });
    return r.json();
  }

  /* ── Payme checkout URL ───────────────────────────────────────── */
  function paymeUrl({ amount, orderId, description = '', returnUrl = '' }) {
    const { payme } = loadCfg();
    if (!payme.enabled) throw new Error('Payme faol emas');
    const base = payme.testMode === 'true'
      ? 'https://checkout.test.paycom.uz'
      : 'https://checkout.paycom.uz';
    const payload = btoa(JSON.stringify({
      m: payme.merchantId,
      ac: { order_id: orderId },
      a: Math.round(amount * 100), // tiyin
      l: 'uz',
      d: description,
      c: returnUrl,
    }));
    return `${base}/${payload}`;
  }

  /* ── Click checkout URL ──────────────────────────────────────── */
  function clickUrl({ amount, orderId, returnUrl = '' }) {
    const { click } = loadCfg();
    if (!click.enabled) throw new Error('Click faol emas');
    const p = new URLSearchParams({
      service_id: click.serviceId,
      merchant_id: click.merchantId,
      amount,
      transaction_param: orderId,
      return_url: returnUrl,
      card_type: 'uzcard',
    });
    return `https://my.click.uz/services/pay?${p}`;
  }

  /* ── Uzum Bank ───────────────────────────────────────────────── */
  async function uzumCreateOrder({ amount, orderId, description = '' }) {
    const { uzum } = loadCfg();
    if (!uzum.enabled) throw new Error('Uzum Bank faol emas');
    const base = uzum.testMode === 'true'
      ? 'https://sandbox-api.uzumbank.uz'
      : 'https://api.uzumbank.uz';
    const r = await fetch(`${base}/v1/checkout/create`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${uzum.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ shopId: uzum.shopId, amount: Math.round(amount * 100), orderId, description, currency: 'UZS' })
    });
    return r.json();
  }

  /* ── Integration status (barcha) ────────────────────────────── */
  function integrationStatus() {
    const cfg = loadCfg();
    return {
      myid:    { enabled: !!cfg.myid.enabled    && !!(cfg.myid.clientId    && cfg.myid.clientSecret) },
      egov:    { enabled: !!cfg.egov.enabled    && !!cfg.egov.apiKey },
      kadastr: { enabled: !!cfg.kadastr.enabled && !!cfg.kadastr.token },
      agro:    { enabled: !!cfg.agro.enabled    && !!cfg.agro.token },
      soliq:   { enabled: !!cfg.soliq.enabled   && !!(cfg.soliq.tin && cfg.soliq.token) },
      payme:   { enabled: !!cfg.payme.enabled   && !!(cfg.payme.merchantId && cfg.payme.key) },
      click:   { enabled: !!cfg.click.enabled   && !!(cfg.click.merchantId && cfg.click.secretKey) },
      uzum:    { enabled: !!cfg.uzum.enabled    && !!(cfg.uzum.shopId && cfg.uzum.token) },
    };
  }

  /* ── Public API ──────────────────────────────────────────────── */
  return {
    loadCfg, saveCfg, patchCfg,
    get, post, put, del,
    myidVerify, kadastrLookup, agroFarm, agroIrrigationNorms,
    paymeUrl, clickUrl, uzumCreateOrder,
    integrationStatus,
  };
})();

// Backward compat — eski sahifalar uchun global API o'zgaruvchisi
const API = TOMCHI.loadCfg().api.base;
