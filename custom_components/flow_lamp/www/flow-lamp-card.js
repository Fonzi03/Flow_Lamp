/*!
 * Flow Lamp card for Home Assistant (custom:flow-lamp-card)
 * Ships with the Flow Lamp integration.
 * Embedded font: Shrikhand, SIL Open Font License 1.1 (see LICENSE-Shrikhand.txt).
 */
const FLOW_LAMP_CARD_VERSION = "1.0.3";
const FLOW_FONT = "FlowLampShrikhand";

// The font has to be registered on the document; @font-face inside a shadow root is ignored.
(() => {
  if (document.getElementById("flow-lamp-card-font")) return;
  const style = document.createElement("style");
  style.id = "flow-lamp-card-font";
  style.textContent =
    `@font-face{font-family:'${FLOW_FONT}';font-style:normal;font-weight:400;font-display:swap;` +
    `src:url(data:font/woff2;base64,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) format('woff2');}`;
  document.head.appendChild(style);
})();

/* ---------- colour helpers (RGB as 0..1 triples) ---------- */
const clamp01 = (v) => Math.min(1, Math.max(0, v));
const clampC = (a) => a.map(clamp01);
const mix = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
const mul = (a, b) => a.map((v, i) => v * b[i]);
const scale = (a, k) => a.map((v) => v * k);
const add = (a, b) => a.map((v, i) => v + b[i]);
const rgba = (c, a = 1) =>
  `rgba(${Math.round(clamp01(c[0]) * 255)},${Math.round(clamp01(c[1]) * 255)},${Math.round(clamp01(c[2]) * 255)},${a})`;
const rgbList = (c) => `${Math.round(clamp01(c[0]) * 255)}, ${Math.round(clamp01(c[1]) * 255)}, ${Math.round(clamp01(c[2]) * 255)}`;
// Rescale a colour so its brightest channel sits near `target` (keeps hue, restores vividness).
const normalize = (c, target = 0.96, lo = 0.9, hi = 4) => {
  const m = Math.max(c[0], c[1], c[2], 0.001);
  return clampC(scale(c, Math.min(hi, Math.max(lo, target / m))));
};

const DEFAULT_WAX = [255, 214, 51]; // yellow wax
const DEFAULT_LIQUID = [122, 43, 191]; // purple liquid
const WHITE = [1, 1, 1];
const BULB = [1.0, 0.95, 0.86]; // the lamp's own warm-white bulb; everything else is derived from the colours

function parseColor(value, fallback) {
  try {
    if (Array.isArray(value) && value.length >= 3) {
      return value.slice(0, 3).map((v) => clamp01(Number(v) / 255));
    }
    if (typeof value === "string" && value.trim()) {
      const ctx = parseColor._ctx || (parseColor._ctx = document.createElement("canvas").getContext("2d"));
      ctx.fillStyle = "#010203";
      ctx.fillStyle = value; // invalid colours are ignored by the canvas
      const out = ctx.fillStyle;
      if (out === "#010203" && value.replace(/\s/g, "").toLowerCase() !== "#010203") return fallback;
      if (out.startsWith("#")) return [1, 3, 5].map((i) => parseInt(out.slice(i, i + 2), 16) / 255);
      const m = out.match(/[\d.]+/g);
      if (m && m.length >= 3) return m.slice(0, 3).map((v) => Number(v) / 255);
    }
  } catch (e) {
    /* fall through */
  }
  return fallback;
}

/* ---------- wax blobs ---------- */
// x: horizontal centre (0..1), r: radius (fraction of a 200-unit width), T: seconds per rise-and-fall,
// ph: phase, H: how high the blob climbs (fraction of tank height), wT: sideways drift period.
// Most blobs are slow and flowy; two (T: 13 and 19) are the occasional quicker ones.
const BLOBS = [
  { x: 0.3, r: 0.105, T: 36, ph: 0.0, H: 0.78, wT: 15 },
  { x: 0.62, r: 0.14, T: 46, ph: 1.3, H: 0.62, wT: 18 },
  { x: 0.45, r: 0.088, T: 29, ph: 2.4, H: 0.88, wT: 13 },
  { x: 0.72, r: 0.075, T: 26, ph: 3.7, H: 0.7, wT: 16 },
  { x: 0.25, r: 0.13, T: 52, ph: 4.6, H: 0.5, wT: 22 },
  { x: 0.55, r: 0.062, T: 13, ph: 5.4, H: 0.92, wT: 10 },
  { x: 0.4, r: 0.115, T: 41, ph: 2.0, H: 0.4, wT: 17 },
  { x: 0.12, r: 0.09, T: 39, ph: 1.0, H: 0.6, wT: 16 },
  { x: 0.84, r: 0.1, T: 49, ph: 3.0, H: 0.75, wT: 20 },
  { x: 0.92, r: 0.07, T: 19, ph: 0.6, H: 0.5, wT: 14 },
];
const RIPPLES = 8;
const VB_W = 300; // tank is 6:5
const VB_H = 250;
const BASE_W = 200; // blob sizes were designed against a 200-unit width

const STATE_LABELS = { off: "Off", warm_up: "Warm Up", flowing: "Flowing", cool_down: "Cool Down" };

const STYLE = `
  :host { display: block; }
  ha-card {
    display: block;
    position: relative;
    overflow: hidden;
    isolation: isolate;
    color: #fff;
    background:
      linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03) 45%, rgba(255,255,255,0.07)),
      rgba(18, 14, 30, 0.62);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
    backdrop-filter: blur(22px) saturate(150%);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 28px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.2);
  }
  .orbs { position: absolute; inset: 0; z-index: -1; pointer-events: none; }
  .orbs::before, .orbs::after {
    content: ""; position: absolute; border-radius: 50%; filter: blur(46px);
  }
  .orbs::before { width: 60%; height: 38%; left: -14%; top: -6%; background: var(--orb1); }
  .orbs::after { width: 66%; height: 40%; right: -18%; bottom: 14%; background: var(--orb2); }
  .content { padding: 16px 16px 14px; }
  .title {
    font-family: '${FLOW_FONT}', 'Shrikhand', cursive;
    font-size: 1.35rem; text-align: center; margin: 0 0 12px;
    letter-spacing: 0.02em; text-shadow: 0 2px 10px rgba(0,0,0,0.4);
  }
  .tank {
    position: relative;
    width: min(100%, 495px);
    aspect-ratio: 6 / 5;
    margin: 0 auto;
    border-radius: 30px;
    overflow: hidden;
    background: #08080c;
    -webkit-tap-highlight-color: transparent;
    transition: transform 0.18s ease, filter 0.18s ease;
    box-shadow:
      0 0 calc(var(--glow-k) * 46px) calc(var(--glow-k) * 6px) rgba(var(--glow-rgb), calc(var(--glow-k) * 0.42)),
      0 10px 26px rgba(0,0,0,0.5);
  }
  .tank.clickable { cursor: pointer; }
  .tank.clickable:hover { filter: brightness(1.06); }
  .tank.clickable:active { transform: scale(0.992); }
  .tank:focus-visible { outline: 2px solid rgba(255,255,255,0.65); outline-offset: 3px; }
  .tank svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .glass {
    position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0) 22%, rgba(0,0,0,0) 78%, rgba(0,0,0,0.22));
    box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.22), inset 0 1px 0 2px rgba(255,255,255,0.05), inset 0 0 26px rgba(255,255,255,0.06);
  }
  .info {
    margin-top: 16px; padding: 4px 14px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 20px;
    -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
    font-family: '${FLOW_FONT}', 'Shrikhand', cursive;
  }
  /* A row that doesn't fit on one line drops its value onto a second line (right-aligned). */
  .row { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 1px 12px; padding: 9px 0; }
  .row[hidden] { display: none; }
  .row + .row { border-top: 1px solid rgba(255,255,255,0.09); }
  .k { font-size: 0.82rem; white-space: nowrap; color: rgba(255,255,255,0.62); letter-spacing: 0.02em; }
  .v { font-size: 1.05rem; white-space: nowrap; margin-left: auto; text-align: right; color: #fff; text-shadow: 0 1px 8px rgba(0,0,0,0.35); }
  .msg { padding: 28px 12px; text-align: center; font-family: '${FLOW_FONT}', 'Shrikhand', cursive; color: rgba(255,255,255,0.75); }
`;

class FlowLampCard extends HTMLElement {
  static getConfigElement() {
    return document.createElement("flow-lamp-card-editor");
  }

  static getStubConfig(hass) {
    const stub = {};
    try {
      // Prefer the entity registry: group Flow's entities by device and map by translation key.
      const groups = {};
      for (const e of Object.values((hass && hass.entities) || {})) {
        if (e.platform !== "flow_lamp" || !e.device_id) continue;
        (groups[e.device_id] = groups[e.device_id] || {})[e.translation_key] = e.entity_id;
      }
      const g = Object.values(groups).find((x) => x.state);
      if (g) return { ...stub, state_entity: g.state };
      // Fallback: entity-id naming (<lamp>_flow_lamp_state).
      const ids = Object.keys((hass && hass.states) || {});
      const st = ids.find((id) => /^sensor\..+_flow_lamp_state$/.test(id));
      if (st) return { ...stub, state_entity: st };
    } catch (e) {
      /* ignore */
    }
    return { ...stub, state_entity: "" };
  }

  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    FlowLampCard._n = (FlowLampCard._n || 0) + 1;
    this._uid = `fc${FlowLampCard._n}`;
    this._t = 0;
    this._F = 0; // flow amount (0 = wax resting, 1 = fully moving)
    this._I = 0; // light level (0 = dark, 1 = full backlight)
    this._Ft = 0;
    this._It = 0;
    this._snap = true;
    this._raf = null;
    this._last = 0;
    this._config = {};
    this._sib = {};
    this._tankW = 330;
    this._wax = scale(DEFAULT_WAX, 1 / 255);
    this._liq = scale(DEFAULT_LIQUID, 1 / 255);
    this._clear = false;
    this._reduced = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  }

  setConfig(config) {
    if (!config || typeof config !== "object") throw new Error("Invalid configuration");
    this._config = { ...config };
    this._sib = {};
    this._regRef = null;
    this._colorKey = null;
    this._build();
    this._update();
  }

  set hass(hass) {
    this._hass = hass;
    this._update();
  }

  getCardSize() {
    return 7;
  }

  getGridOptions() {
    return { columns: 7, rows: "auto", min_columns: 4 };
  }

  connectedCallback() {
    this._observe();
    this._ensureLoop();
  }

  disconnectedCallback() {
    if (this._raf) cancelAnimationFrame(this._raf);
    this._raf = null;
    if (this._ro) this._ro.disconnect();
  }

  /* ---------- sibling entities (found automatically on the same Flow device) ---------- */
  _entity(kind) {
    const c = this._config;
    const explicit = kind === "dimming_level" ? c.dimming_entity : kind === "time_remaining" ? c.time_entity : undefined;
    if (explicit) return explicit;
    const st = c.state_entity;
    if (!st || !this._hass) return undefined;
    const reg = this._hass.entities || {};
    if (this._regRef !== reg) {
      // The registry changed (or first look): forget earlier misses and look again.
      this._regRef = reg;
      this._sib = {};
    }
    if (kind in this._sib) return this._sib[kind] || undefined;
    let found;
    const dev = reg[st] && reg[st].device_id;
    if (dev) {
      const hit = Object.values(reg).find((e) => e.device_id === dev && e.platform === "flow_lamp" && e.translation_key === kind);
      if (hit) found = hit.entity_id;
    }
    if (!found) {
      const domain = kind === "power" ? "switch" : "sensor";
      const base = st.replace(/^sensor\./, `${domain}.`).replace(/_state$/, "");
      const guesses = kind === "power" ? [`${base}_lamp_power`, `${base}_light_power`, `${base}_power`] : [`${base}_${kind}`];
      found = guesses.find((g) => this._hass.states[g]);
    }
    this._sib[kind] = found || null;
    return found;
  }

  // Colours come from the integration (Configure on the Flow Lamp entry); defaults if unavailable.
  _syncColors() {
    const c = this._config;
    const st = this._hass && c.state_entity ? this._hass.states[c.state_entity] : undefined;
    const attrs = (st && st.attributes) || {};
    const clear = attrs.liquid_clear === true;
    const key = JSON.stringify([attrs.wax_color, attrs.liquid_color, clear]);
    if (key === this._colorKey) return;
    this._colorKey = key;
    this._wax = parseColor(attrs.wax_color, scale(DEFAULT_WAX, 1 / 255));
    this._clear = clear;
    this._liq = clear ? WHITE : parseColor(attrs.liquid_color, scale(DEFAULT_LIQUID, 1 / 255));
    this._renderFrame();
  }

  /* ---------- DOM ---------- */
  _build() {
    const id = this._uid;
    const ripples = Array.from({ length: RIPPLES }, () => `<circle class="rip" r="20"/>`).join("");
    const blobs = BLOBS.map(() => `<ellipse class="blob"/>`).join("");
    const title = this._config.name ? `<div class="title">${this._esc(this._config.name)}</div>` : "";
    this.shadowRoot.innerHTML = `
      <style>${STYLE}</style>
      <ha-card>
        <div class="orbs"></div>
        <div class="content">
          ${title}
          <div class="tank" role="button" tabindex="0" aria-label="Toggle the lamp">
            <svg viewBox="0 0 ${VB_W} ${VB_H}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <filter id="goo-${id}" filterUnits="userSpaceOnUse" x="0" y="0" width="${VB_W}" height="${VB_H}" color-interpolation-filters="sRGB">
                  <feGaussianBlur in="SourceGraphic" stdDeviation="5"/>
                  <feColorMatrix mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 24 -10"/>
                </filter>
                <linearGradient id="liq-${id}" x1="0" y1="1" x2="0" y2="0">
                  <stop offset="0" style="stop-color:var(--liq-hi)"/>
                  <stop offset="1" style="stop-color:var(--liq-lo)"/>
                </linearGradient>
                <linearGradient id="wax-${id}" x1="0" y1="1" x2="0" y2="0">
                  <stop offset="0" style="stop-color:var(--wax-bot)"/>
                  <stop offset="0.25" style="stop-color:var(--wax-hi)"/>
                  <stop offset="1" style="stop-color:var(--wax-lo)"/>
                </linearGradient>
                <radialGradient id="glow-${id}" cx="50%" cy="104%" r="86%">
                  <stop offset="0" style="stop-color:var(--glow);stop-opacity:var(--glow-a)"/>
                  <stop offset="0.5" style="stop-color:var(--glow);stop-opacity:var(--glow-b)"/>
                  <stop offset="1" style="stop-color:var(--glow);stop-opacity:0"/>
                </radialGradient>
                <filter id="shade-${id}" filterUnits="userSpaceOnUse" x="0" y="0" width="${VB_W}" height="${VB_H}" color-interpolation-filters="sRGB">
                  <feGaussianBlur in="SourceAlpha" stdDeviation="3.2" result="bump"/>
                  <feSpecularLighting in="bump" surfaceScale="6" specularConstant="0.9" specularExponent="24" style="lighting-color:var(--spec)" result="spec">
                    <fePointLight x="80" y="-40" z="110"/>
                  </feSpecularLighting>
                  <feComposite in="spec" in2="SourceAlpha" operator="in" result="specIn"/>
                  <feComposite in="SourceGraphic" in2="specIn" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/>
                </filter>
                <mask id="wm-${id}" maskUnits="userSpaceOnUse" x="0" y="0" width="${VB_W}" height="${VB_H}">
                  <g filter="url(#goo-${id})" fill="#fff">
                    <rect class="pool" x="-10" width="${VB_W + 20}"/>
                    ${ripples}
                    ${blobs}
                  </g>
                </mask>
              </defs>
              <rect width="${VB_W}" height="${VB_H}" fill="#08080c"/>
              <rect width="${VB_W}" height="${VB_H}" fill="url(#glow-${id})"/>
              <rect width="${VB_W}" height="${VB_H}" fill="url(#liq-${id})" style="opacity:var(--liq-op)"/>
              <g filter="url(#shade-${id})"><rect width="${VB_W}" height="${VB_H}" fill="url(#wax-${id})" mask="url(#wm-${id})" opacity="0.97"/></g>
            </svg>
            <div class="glass"></div>
          </div>
          <div class="info">
            <div class="row"><span class="k">State</span><span class="v st">—</span></div>
            <div class="row dlrow"><span class="k">Dimming Level</span><span class="v dl">—</span></div>
            <div class="row"><span class="k">Time Remaining</span><span class="v tr">—</span></div>
          </div>
        </div>
      </ha-card>`;
    const $ = (s) => this.shadowRoot.querySelector(s);
    const $$ = (s) => Array.from(this.shadowRoot.querySelectorAll(s));
    this._host = $("ha-card");
    this._els = {
      tank: $(".tank"),
      pool: $(".pool"),
      rips: $$(".rip"),
      blobs: $$(".blob"),
      st: $(".st"),
      dl: $(".dl"),
      dlrow: $(".dlrow"),
      tr: $(".tr"),
    };
    this._els.tank.addEventListener("click", () => this._toggle());
    this._els.tank.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" || ev.key === " ") {
        ev.preventDefault();
        this._toggle();
      }
    });
    this._snap = true;
    this._observe();
    this._renderFrame();
  }

  _observe() {
    if (this._ro) this._ro.disconnect();
    if (typeof ResizeObserver === "undefined" || !this._els || !this.isConnected) return;
    this._ro = new ResizeObserver((entries) => {
      const w = entries[0] && entries[0].contentRect && entries[0].contentRect.width;
      if (w) this._tankW = w;
    });
    this._ro.observe(this._els.tank);
  }

  _esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }

  /* ---------- interaction ---------- */
  async _toggle() {
    if (!this._hass) return;
    const power = this._entity("power");
    let domain = "switch";
    let target = power;
    if (!target) {
      // Fall back to the lamp itself (named on the state sensor).
      const st = this._hass.states[this._config.state_entity];
      target = st && st.attributes && st.attributes.light;
      domain = target ? target.split(".")[0] : "";
    }
    if (!target) return;
    try {
      await this._hass.callService(domain, "toggle", { entity_id: target });
    } catch (err) {
      // Home Assistant shows its own message when a call is refused (e.g. while the lamp cools down).
    }
  }

  /* ---------- data ---------- */
  _read(entityId) {
    if (!entityId || !this._hass) return undefined;
    const s = this._hass.states[entityId];
    return s ? s.state : undefined;
  }

  _update() {
    if (!this._els) return;
    const c = this._config;
    const st = this._read(c.state_entity);
    const dimId = this._entity("dimming_level"); // none for lamps that can't dim
    const dl = dimId ? this._read(dimId) : undefined;
    const tr = this._read(this._entity("time_remaining"));
    this._syncColors();
    const bad = (v) => v === undefined || v === "unknown" || v === "unavailable";

    const label = bad(st) ? (st === undefined ? "—" : "Unavailable") : STATE_LABELS[st] || st;
    this._els.st.textContent = label;

    this._els.dlrow.hidden = !dimId;
    const pct = bad(dl) || isNaN(Number(dl)) ? null : Math.max(0, Math.min(100, Number(dl)));
    this._els.dl.textContent = pct === null ? (dl === undefined ? "—" : "Unavailable") : `${Math.round(pct)}%`;
    this._els.tr.textContent = bad(tr) ? (tr === undefined ? "—" : "Unavailable") : tr;

    // Light follows the dimmer output (still visibly lit when dimmed low). A lamp without
    // dimming is simply lit whenever it is on (warm-up and flowing).
    if (dimId) this._It = pct && pct > 0 ? 0.18 + 0.82 * (pct / 100) : 0;
    else this._It = st === "warm_up" || st === "flowing" ? 1 : 0;
    this._Ft = st === "flowing" || st === "cool_down" ? 1 : 0;

    const stateObj = this._hass && this._hass.states[c.state_entity];
    const clickable = !!(this._entity("power") || (stateObj && stateObj.attributes && stateObj.attributes.light));
    this._els.tank.classList.toggle("clickable", clickable);

    if (this._snap && this._hass) {
      this._F = this._Ft;
      this._I = this._It;
      this._snap = false;
      this._renderFrame();
    }
    this._ensureLoop();
  }

  /* ---------- animation ---------- */
  _settled() {
    const eps = 0.002;
    const still = this._Ft === 0 && this._It === 0 && this._F < eps && this._I < eps;
    const steady = Math.abs(this._F - this._Ft) < eps && Math.abs(this._I - this._It) < eps;
    return still && steady;
  }

  _ensureLoop() {
    if (this._raf || !this.isConnected || !this._els) return;
    if (this._settled()) {
      this._F = 0;
      this._I = 0;
      this._renderFrame();
      return;
    }
    this._last = 0;
    this._raf = requestAnimationFrame((t) => this._tick(t));
  }

  _tick(now) {
    this._raf = null;
    if (!this.isConnected) return;
    if (!this._last) this._last = now;
    const dt = Math.min(0.1, (now - this._last) / 1000);
    if (dt < 1 / 32) {
      // ~30 fps is plenty for slow wax and is kinder to wall tablets
      this._raf = requestAnimationFrame((t) => this._tick(t));
      return;
    }
    this._last = now;
    this._advance(dt);
    this._renderFrame();
    if (this._settled()) {
      this._F = 0;
      this._I = 0;
      this._renderFrame();
      return;
    }
    this._raf = requestAnimationFrame((t) => this._tick(t));
  }

  _advance(dt) {
    // Smaller tanks (phones) get a calmer pace so the motion reads the same.
    const speed = (this._reduced ? 0.35 : 1) * (this._tankW < 420 ? 0.75 : 1);
    this._t += dt * speed;
    const ease = (cur, target, tauUp, tauDown) => {
      const tau = target > cur ? tauUp : tauDown;
      return cur + (target - cur) * (1 - Math.exp(-dt / tau));
    };
    this._F = ease(this._F, this._Ft, 4.5, 7); // starts moving gently, sinks back slowly
    this._I = ease(this._I, this._It, 0.9, 0.9);
  }

  _renderFrame() {
    const e = this._els;
    if (!e) return;
    const W = VB_W;
    const H = VB_H;
    const F = this._F;
    const I = this._I;
    const t = this._t;
    const TAU = Math.PI * 2;

    // Pool of wax at the bottom; it sits a little lower while blobs are aloft.
    const h0 = H * 0.19;
    const poolTop = H - h0 * (1 - 0.38 * F);
    e.pool.setAttribute("y", poolTop.toFixed(2));
    e.pool.setAttribute("height", (H - poolTop + 30).toFixed(2));

    const ripAmp = 0.9 + 2.6 * I * (1 - F) + 1.6 * F;
    e.rips.forEach((c, i) => {
      const x = W * (0.02 + (0.96 * i) / (RIPPLES - 1)) + Math.sin(t * 0.2 + i * 1.7) * 5 * F;
      const y = poolTop + 15 + Math.sin(t * 0.35 + i * 2.1) * ripAmp;
      c.setAttribute("cx", x.toFixed(2));
      c.setAttribute("cy", y.toFixed(2));
      c.setAttribute("r", (21 + 2 * Math.sin(t * 0.25 + i)).toFixed(2));
    });

    const yRest = H - h0 * 0.5;
    BLOBS.forEach((p, i) => {
      const s0 = (Math.sin((t / p.T) * TAU + p.ph) + 1) / 2;
      const s = s0 * s0 * (3 - 2 * s0);
      const k = F * s;
      const yPeak = H * (1 - p.H);
      const cy = yRest + (yPeak - yRest) * k;
      const cx = W * p.x + Math.sin((t / p.wT) * TAU + p.ph * 2) * W * 0.045 * F;
      const r = p.r * BASE_W * (0.5 + 0.5 * Math.min(1, F * 1.6));
      const rx = r * (1 + 0.07 * Math.sin(t * 0.6 + p.ph)) * (1 - 0.1 * k);
      const ry = r * (1 + 0.12 * k);
      const b = e.blobs[i];
      b.setAttribute("cx", cx.toFixed(2));
      b.setAttribute("cy", cy.toFixed(2));
      b.setAttribute("rx", rx.toFixed(2));
      b.setAttribute("ry", ry.toFixed(2));
    });

    this._applyLook(I);
  }

  /*
   * Colour model. The backlight passes through the liquid, so the liquid tints everything behind
   * it: the wax you see is the wax colour multiplied by the liquid's transmission (yellow wax in
   * purple liquid reads red-orange, in blue liquid it reads green). Clear liquid lets the wax keep
   * its own colour. The glow is the bulb's light after the liquid, so it follows the liquid too.
   */
  _applyLook(I) {
    const clear = this._clear;
    const liq = this._liq;
    const T = clear ? WHITE : mix(WHITE, liq, 0.92);
    const waxF = normalize(mul(this._wax, T));
    const glow = normalize(mul(BULB, T), 1.0, 1, 4);

    const own = normalize(this._wax); // the wax's own colour, before the liquid tints it
    const bot = mix(waxF, own, 0.8); // right by the bulb the wax still shows mostly its own colour
    const waxBot = mix(scale(bot, 0.3), clampC(add(bot, [0.04, 0.04, 0.04])), I);
    const waxLitHi = clampC(add(waxF, [0.04, 0.04, 0.04]));
    const waxHi = mix(scale(waxF, 0.3), waxLitHi, I);
    const waxLo = mix(scale(waxF, 0.2), scale(waxF, 0.72), I);

    let liqHi;
    let liqLo;
    let liqLitHi;
    if (clear) {
      liqHi = glow;
      liqLo = glow;
      liqLitHi = scale(glow, 0.85);
    } else {
      liqLitHi = clampC(add(scale(liq, 1.25), [0.05, 0.05, 0.05]));
      liqHi = mix(scale(liq, 0.3), liqLitHi, I);
      liqLo = mix(scale(liq, 0.2), clampC(scale(liq, 0.85)), I);
    }
    const orbLiq = clear ? scale(glow, 0.45) : scale(liq, 0.45);

    const s = this._host.style;
    s.setProperty("--wax-bot", rgba(waxBot));
    s.setProperty("--wax-hi", rgba(waxHi));
    s.setProperty("--wax-lo", rgba(waxLo));
    s.setProperty("--liq-hi", rgba(liqHi));
    s.setProperty("--liq-lo", rgba(liqLo));
    s.setProperty("--liq-op", clear ? "0" : "0.84");
    s.setProperty("--glow", rgba(glow));
    s.setProperty("--glow-rgb", rgbList(glow));
    s.setProperty("--glow-a", (0.9 * I).toFixed(3));
    s.setProperty("--glow-b", (0.34 * I).toFixed(3));
    s.setProperty("--glow-k", I.toFixed(3));
    s.setProperty("--spec", rgba(scale([1.0, 0.97, 0.92], 0.55 * I)));
    s.setProperty("--orb1", rgba(mix(orbLiq, liqLitHi, I), 0.5));
    s.setProperty("--orb2", rgba(mix(scale(waxF, 0.35), waxLitHi, I), 0.42));
  }
}

/* ---------- visual editor ---------- */
const FLOW_SCHEMA = [
  { name: "name", selector: { text: {} } },
  { name: "state_entity", required: true, selector: { entity: { integration: "flow_lamp", domain: "sensor" } } },
];
const FLOW_LABELS = {
  name: "Name (optional)",
  state_entity: "State sensor (the other sensors are found automatically)",
};

class FlowLampCardEditor extends HTMLElement {
  setConfig(config) {
    this._config = config;
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  _render() {
    if (!this._hass || !this._config) return;
    if (!this._form) {
      this._form = document.createElement("ha-form");
      this._form.computeLabel = (s) => FLOW_LABELS[s.name] || s.name;
      this._form.addEventListener("value-changed", (ev) => {
        ev.stopPropagation();
        const config = { ...this._config, ...ev.detail.value };
        this._config = config;
        this.dispatchEvent(new CustomEvent("config-changed", { detail: { config }, bubbles: true, composed: true }));
      });
      this.appendChild(this._form);
    }
    this._form.hass = this._hass;
    this._form.schema = FLOW_SCHEMA;
    this._form.data = { ...this._config };
  }
}

if (!customElements.get("flow-lamp-card")) customElements.define("flow-lamp-card", FlowLampCard);
if (!customElements.get("flow-lamp-card-editor")) customElements.define("flow-lamp-card-editor", FlowLampCardEditor);
window.customCards = window.customCards || [];
if (!window.customCards.some((c) => c.type === "flow-lamp-card")) {
  window.customCards.push({
    type: "flow-lamp-card",
    name: "Flow Lamp",
    description: "Animated lava lamp for a lamp managed by the Flow integration.",
    preview: true,
  });
}
console.info(`%c FLOW LAMP %c ${FLOW_LAMP_CARD_VERSION} `, "color:#fff;background:#6f4bd8;font-weight:700", "color:#6f4bd8");
