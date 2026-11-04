"use strict";
// Wirtualne biuro FUDALI – pikselowa mapa (canvas), dane z dane.json (budowane z repozytorium).

/* ============================ stałe ============================ */
const T = 16, MW = 32, MH = 20;
const OUT = "#2b1d16";
const STANY = {
  pracuje: { nazwa: "Pracuje", kolor: "#3fb950" },
  gotowe: { nazwa: "Gotowe", kolor: "#58a6ff" },
  czeka: { nazwa: "Czeka na Ciebie", kolor: "#ff6b4a" },
  wolne: { nazwa: "Wolne", kolor: "#9aa4b2" },
  blad: { nazwa: "Błąd", kolor: "#ff2d55" },
  cisza: { nazwa: "Cisza – brak sygnału", kolor: "#c9a227" },
};
const MIEJSCA = {
  konkurencja: [3, 12], "slowa-kluczowe": [10, 12], pozycjonowanie: [17, 12], "rynki-zagraniczne": [24, 12],
  marketing: [6, 16], grafika: [13, 16], sprzedaz: [20, 16],
};
const ZAPASOWE = [[28, 12], [2, 16], [23, 16]];
const SKORY = ["#f1c27d", "#e0ac69", "#ffdbac", "#f5cba7", "#d8a37a"];
const DRZWI = [4, 5, 15, 16, 26, 27];
const KLAUDIUSZ = { cx: 16 * T, by: 6 * T };
const TABLICA = { x: 19, w: 5 };

/* ============================ dane ============================ */
let DANE = { zespol: [], zapisy: [] };
let osoby = [];         // pracownicy na mapie (bez Klaudiusza)
let klaudiusz = null;   // osoba Klaudiusz
let wybrany = null;     // id otwartego panelu

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const hash = (s) => { let h = 7; for (const ch of String(s)) h = (h * 31 + ch.charCodeAt(0)) >>> 0; return h; };

function stanEf(o) {
  const s = o.status || {};
  let st = STANY[s.stan] ? s.stan : "wolne";
  if (st === "pracuje" && s.aktualizacja && Date.now() - Date.parse(s.aktualizacja) > 3 * 3600e3) st = "cisza";
  return st;
}
function kiedy(iso) {
  if (!iso) return "—";
  const d = new Date(iso); if (isNaN(d)) return iso;
  const min = Math.round((Date.now() - d) / 60000);
  if (min < 1) return "przed chwilą";
  if (min < 60) return `${min} min temu`;
  const fmt = (o) => new Intl.DateTimeFormat("pl-PL", { timeZone: "Europe/Warsaw", ...o }).format(d);
  if (min < 12 * 60) return `${Math.round(min / 60)} godz. temu (${fmt({ hour: "2-digit", minute: "2-digit" })})`;
  return fmt({ day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
}
function godzinaPL() {
  const p = new Intl.DateTimeFormat("pl-PL", { timeZone: "Europe/Warsaw", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date());
  return { h: +p.find((x) => x.type === "hour").value % 24, m: +p.find((x) => x.type === "minute").value };
}
function shade(hex, f) {
  const n = parseInt(hex.slice(1), 16);
  let r = n >> 16, g = (n >> 8) & 255, b = n & 255;
  const t = f < 0 ? 0 : 255, p = Math.abs(f);
  r = Math.round((t - r) * p + r); g = Math.round((t - g) * p + g); b = Math.round((t - b) * p + b);
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

/* ============================ mapa / kolizje ============================ */
const solid = Array.from({ length: MH }, () => Array(MW).fill(false));
const blok = (x, y, w = 1, h = 1) => { for (let j = y; j < y + h; j++) for (let i = x; i < x + w; i++) if (solid[j]) solid[j][i] = true; };
blok(0, 0, MW, 2); blok(0, 0, 1, MH); blok(MW - 1, 0, 1, MH); blok(0, MH - 1, MW, 1);
for (let x = 1; x < MW - 1; x++) if (!DRZWI.includes(x)) blok(x, 9);
blok(10, 2, 1, 7); blok(21, 2, 1, 7);

const R = (c, x, y, w, h, k) => { c.fillStyle = k; c.fillRect(x, y, w, h); };
const OR = (c, x, y, w, h, k, o = OUT) => { R(c, x - 1, y - 1, w + 2, h + 2, o); R(c, x, y, w, h, k); };

function region(x, y) {
  if (y <= 8) { if (x <= 10) return "gabinet"; if (x >= 22) return "kuchnia"; return "mozg"; }
  return "open";
}

// ---- meble (stałe obiekty z kolizją i sortowaniem po głębokości) ----
const meble = [];
function mebel(x, y, w, h, rysuj, kolizja = true) {
  if (kolizja) blok(x, y, w, h);
  meble.push({ baseY: (y + h) * T, rysuj: (c, t) => rysuj(c, x * T, y * T, t) });
}
function roslina(x, y) {
  mebel(x, y, 1, 1, (c, x0, y0) => {
    OR(c, x0 + 4, y0 + 9, 8, 6, "#b5562b"); R(c, x0 + 4, y0 + 9, 8, 1, "#cf6d3d");
    OR(c, x0 + 3, y0 - 2, 10, 11, "#3f8f3f"); R(c, x0 + 1, y0 + 2, 4, 5, "#3f8f3f"); R(c, x0 + 11, y0 + 1, 4, 5, "#3f8f3f");
    R(c, x0 + 5, y0, 3, 3, "#5fb55f"); R(c, x0 + 9, y0 + 3, 2, 3, "#5fb55f"); R(c, x0 + 2, y0 + 3, 2, 2, "#5fb55f"); R(c, x0 + 12, y0 + 2, 2, 2, "#5fb55f");
  });
}
// gabinet szefa
mebel(1, 2, 2, 1, (c, x0, y0) => {
  OR(c, x0 + 1, y0 - 12, 30, 27, "#6e4420");
  const kolory = ["#c0392b", "#2980b9", "#27ae60", "#f1c40f", "#8e44ad", "#e67e22", "#ecf0f1"];
  for (let p = 0; p < 3; p++) {
    const py = y0 - 10 + p * 8;
    R(c, x0 + 2, py + 6, 28, 2, "#4a2e16");
    for (let i = 0; i < 7; i++) R(c, x0 + 3 + i * 4, py + (i % 3 === 0 ? 1 : 0), 3, 6 - (i % 3 === 0 ? 1 : 0), kolory[(i + p * 2) % kolory.length]);
  }
});
mebel(4, 4, 3, 1, (c, x0, y0) => {           // biurko szefa
  OR(c, x0 + 1, y0 + 4, 46, 7, "#4a2e16"); OR(c, x0 + 1, y0 - 6, 46, 10, "#6b4423"); R(c, x0 + 1, y0 - 6, 46, 1, "#8a5a30");
  R(c, x0 + 3, y0 + 11, 3, 4, "#2e1c0d"); R(c, x0 + 42, y0 + 11, 3, 4, "#2e1c0d");
  OR(c, x0 + 14, y0 - 16, 20, 11, "#2d3436"); R(c, x0 + 15, y0 - 15, 18, 1, "#636e72"); R(c, x0 + 22, y0 - 5, 4, 2, "#2d3436");
  OR(c, x0 + 18, y0 + 5, 12, 4, "#d4af37"); R(c, x0 + 20, y0 + 6, 8, 2, "#8a6d1d");   // tabliczka SZEF
  OR(c, x0 + 4, y0 - 4, 7, 4, "#fbfaf5"); OR(c, x0 + 38, y0 - 6, 4, 5, "#f4f1ea"); R(c, x0 + 38, y0 - 5, 4, 1, "#b03a2e");
});
mebel(5, 3, 1, 1, (c, x0, y0) => { OR(c, x0 + 1, y0 - 2, 14, 12, "#3b2a20"); R(c, x0 + 2, y0 - 1, 12, 2, "#5a4030"); }, true);
roslina(9, 2); roslina(1, 8);
mebel(8, 6, 1, 1, (c, x0, y0) => {           // makieta domku ogrodowego
  OR(c, x0 + 1, y0 + 8, 14, 6, "#5b3a1e");
  OR(c, x0 + 3, y0 + 1, 10, 8, "#deb887"); R(c, x0 + 3, y0 + 3, 10, 1, "#c9a06a"); R(c, x0 + 3, y0 + 6, 10, 1, "#c9a06a");
  OR(c, x0 + 7, y0 + 4, 3, 5, "#8b5a2b");
  OR(c, x0 + 2, y0 - 2, 12, 3, "#6e2c1a"); R(c, x0 + 4, y0 - 4, 8, 2, "#6e2c1a");
});
// mózg operacji
for (const x of [11, 12, 19, 20]) mebel(x, 2, 1, 1, (c, x0, y0, t) => {
  OR(c, x0 + 1, y0 - 13, 14, 28, "#1b1f2a"); R(c, x0 + 2, y0 - 12, 12, 1, "#2f3647");
  for (let i = 0; i < 6; i++) {
    R(c, x0 + 3, y0 - 10 + i * 4, 10, 3, "#252b3a");
    const on = (hash(x * 13 + i) + Math.floor(t / (180 + i * 40))) % 3;
    R(c, x0 + 4, y0 - 9 + i * 4, 1, 1, on ? "#3fb950" : "#0f3d1a");
    R(c, x0 + 6, y0 - 9 + i * 4, 1, 1, on === 2 ? "#58a6ff" : "#123050");
  }
});
roslina(11, 8); roslina(20, 8);
blok(15, 4, 2, 2);  // piedestał Klaudiusza
// kuchnia
mebel(22, 2, 5, 1, (c, x0, y0, t) => {
  OR(c, x0, y0 - 8, 80, 23, "#cfc4b2"); R(c, x0, y0 - 8, 80, 8, "#e6ddd0"); R(c, x0, y0 - 1, 80, 1, "#a99d8a");
  for (let i = 1; i < 5; i++) R(c, x0 + i * 16, y0, 1, 14, "#a99d8a");
  for (let i = 0; i < 5; i++) R(c, x0 + i * 16 + 7, y0 + 4, 2, 1, "#7d7262");
  OR(c, x0 + 19, y0 - 18, 11, 13, "#2e2e33"); R(c, x0 + 21, y0 - 16, 7, 3, "#55555e");
  R(c, x0 + 27, y0 - 10, 1, 1, Math.floor(t / 700) % 2 ? "#ff4d4d" : "#7a1f1f"); OR(c, x0 + 23, y0 - 8, 4, 3, "#f4f1ea");
  OR(c, x0 + 50, y0 - 6, 12, 5, "#9aa4ad"); R(c, x0 + 55, y0 - 11, 2, 5, "#7f8c8d");
});
mebel(30, 2, 1, 1, (c, x0, y0) => {
  OR(c, x0 + 1, y0 - 15, 14, 30, "#eef1f4"); R(c, x0 + 1, y0 - 4, 14, 1, "#b9c2cc"); R(c, x0 + 3, y0 - 12, 1, 5, "#95a5a6"); R(c, x0 + 3, y0, 1, 8, "#95a5a6");
});
mebel(25, 5, 2, 1, (c, x0, y0) => {
  OR(c, x0 + 2, y0 - 4, 28, 12, "#c08a50"); R(c, x0 + 2, y0 - 4, 28, 1, "#d6a066"); R(c, x0 + 5, y0 + 8, 2, 6, "#6e4420"); R(c, x0 + 25, y0 + 8, 2, 6, "#6e4420");
  OR(c, x0 + 6, y0 - 2, 4, 4, "#f4f1ea"); OR(c, x0 + 20, y0 - 1, 6, 3, "#e8b04a");
});
for (const x of [24, 27]) mebel(x, 5, 1, 1, (c, x0, y0) => { OR(c, x0 + 4, y0 + 2, 8, 6, "#7a5230"); R(c, x0 + 7, y0 + 8, 2, 6, "#4a2e16"); });
mebel(28, 7, 3, 1, (c, x0, y0) => {
  OR(c, x0 + 1, y0 - 4, 46, 19, "#4f6f8a"); R(c, x0 + 1, y0 - 4, 46, 7, "#5a7d9a");
  R(c, x0 + 16, y0 + 3, 1, 10, "#3f5a70"); R(c, x0 + 31, y0 + 3, 1, 10, "#3f5a70");
  OR(c, x0 + 1, y0 - 4, 4, 19, "#3f5a70"); OR(c, x0 + 43, y0 - 4, 4, 19, "#3f5a70");
});
roslina(22, 8);
// open space
mebel(27, 15, 3, 2, (c, x0, y0) => {          // mini drewutnia – firmowy znak rozpoznawczy :)
  OR(c, x0 + 1, y0 + 2, 3, 28, "#5b3a1e"); OR(c, x0 + 44, y0 + 2, 3, 28, "#5b3a1e");
  OR(c, x0 + 4, y0 + 6, 40, 24, "#3a2616");
  for (let r = 0; r < 4; r++) for (let k = 0; k < 6; k++) {
    const lx = x0 + 5 + k * 6 + (r % 2) * 3, ly = y0 + 7 + r * 6;
    if (lx + 5 > x0 + 44) continue;
    R(c, lx, ly, 5, 5, "#8b5a2b"); R(c, lx + 1, ly + 1, 3, 3, "#deb887"); R(c, lx + 2, ly + 2, 1, 1, "#a0703f");
  }
  OR(c, x0 - 1, y0 - 4, 50, 7, "#6e2c1a"); R(c, x0 - 1, y0 - 4, 50, 2, "#8e3b24");
});
mebel(12, 10, 1, 1, (c, x0, y0, t) => {        // dystrybutor wody
  OR(c, x0 + 4, y0 + 3, 8, 12, "#ecf0f1"); OR(c, x0 + 5, y0 - 5, 6, 8, "#7ec8f0"); R(c, x0 + 6, y0 - 4, 2, 6, "#b8e4fa");
  R(c, x0 + 6, y0 + 6 + (Math.floor(t / 900) % 2), 4, 1, "#3498db");
});
roslina(1, 10); roslina(30, 10); roslina(1, 18); roslina(30, 18); roslina(9, 18);

/* ============================ tło (podłogi i ściany) ============================ */
function zbudujTlo() {
  const g = document.createElement("canvas"); g.width = MW * T; g.height = MH * T;
  const c = g.getContext("2d");
  const deski = ["#c8955a", "#bf8a50", "#d09d63", "#c38f55"];
  for (let y = 0; y < MH; y++) for (let x = 0; x < MW; x++) {
    const x0 = x * T, y0 = y * T, r = region(x, y);
    if (r === "open") {
      for (let s = 0; s < 4; s++) {
        const rz = y * 4 + s, off = (rz * 23) % 48;
        for (let i = 0; i < T; i++) {
          const gx = x0 + i + off, nr = Math.floor(gx / 48);
          R(c, x0 + i, y0 + s * 4, 1, 3, gx % 48 === 0 ? "#a87440" : deski[hash(nr * 7 + rz) % 4]);
          R(c, x0 + i, y0 + s * 4 + 3, 1, 1, "#ad7845");
        }
      }
    } else if (r === "gabinet") {
      R(c, x0, y0, T, T, "#3e6b4f");
      for (let i = 0; i < 4; i++) R(c, x0 + (hash(x * 3 + y * 7 + i) % 16), y0 + (hash(x * 11 + y * 5 + i) % 16), 1, 1, "#4a7a5c");
    } else if (r === "mozg") {
      R(c, x0, y0, T, T, "#1c2541"); R(c, x0, y0, T, 1, "#26335a"); R(c, x0, y0, 1, T, "#26335a");
      if (hash(x * 17 + y) % 5 === 0) R(c, x0 + 7, y0 + 7, 2, 2, "#2f4a7a");
    } else {
      for (let j = 0; j < 2; j++) for (let i = 0; i < 2; i++) R(c, x0 + i * 8, y0 + j * 8, 8, 8, (i + j + x + y) % 2 ? "#e9e4da" : "#cfc6b6");
    }
  }
  // dywan w gabinecie
  OR(c, 3 * T, 6 * T, 4 * T, 2 * T + 8, "#7b2d26");
  R(c, 3 * T + 3, 6 * T + 3, 4 * T - 6, 2 * T + 2, "#9c3b31");
  for (let i = 0; i < 4 * T - 10; i += 4) { R(c, 3 * T + 5 + i, 6 * T + 5, 2, 2, "#d4a85a"); R(c, 3 * T + 5 + i, 8 * T + 1, 2, 2, "#d4a85a"); }
  // pierścień pod Klaudiuszem
  OR(c, 14 * T + 4, 4 * T + 2, 3 * T - 8, 2 * T + 6, "#24305a", "#121a33");
  // ściana górna
  const tynk = (x) => (x <= 10 ? "#efe3cf" : x >= 21 ? "#dfe9d8" : "#2d3a5a");
  for (let x = 0; x < MW; x++) {
    const x0 = x * T;
    R(c, x0, 0, T, 4, "#4a3426");
    R(c, x0, 4, T, 16, tynk(x));
    R(c, x0, 20, T, 9, x > 10 && x < 21 ? "#1f2944" : "#8a6a4f");
    R(c, x0 + 7, 20, 1, 9, x > 10 && x < 21 ? "#18203a" : "#765a42");
    R(c, x0, 29, T, 3, x > 10 && x < 21 ? "#121a33" : "#5a4030");
  }
  // ścianki działowe pionowe
  for (const x of [10, 21]) for (let y = 2; y <= 8; y++) { R(c, x * T + 5, y * T, 6, T, "#4a3426"); R(c, x * T + 5, y * T, 1, T, "#6b4f3a"); }
  // ściana pozioma (y = 9) – widać jej front od strony open space
  for (let x = 1; x < MW - 1; x++) {
    const x0 = x * T, y0 = 9 * T;
    if (DRZWI.includes(x)) { R(c, x0 + 2, y0 + 10, 12, 4, "#6e5a3e"); continue; }
    R(c, x0, y0, T, 4, "#4a3426"); R(c, x0, y0 + 4, T, 8, "#efe3cf"); R(c, x0, y0 + 12, T, 3, "#8a6a4f"); R(c, x0, y0 + 15, T, 1, "#5a4030");
  }
  for (const x of [4, 15, 26]) { R(c, x * T - 2, 9 * T, 2, T, "#4a3426"); R(c, (x + 2) * T, 9 * T, 2, T, "#4a3426"); }
  // szyld FUDALI
  OR(c, 8 * T + 2, 9 * T + 4, 5 * T - 4, 8, "#8b5a2b"); R(c, 8 * T + 2, 9 * T + 4, 5 * T - 4, 1, "#a87440");
  // ściany zewnętrzne
  for (let y = 0; y < MH; y++) { R(c, 0, y * T, T, T, "#3a281c"); R(c, (MW - 1) * T, y * T, T, T, "#3a281c"); }
  R(c, T - 1, 2 * T, 1, (MH - 3) * T, "#5a4030"); R(c, (MW - 1) * T, 2 * T, 1, (MH - 3) * T, "#5a4030");
  R(c, 0, (MH - 1) * T, MW * T, T, "#3a281c"); R(c, T, (MH - 1) * T, (MW - 2) * T, 1, "#5a4030");
  return g;
}

/* ============================ postacie ============================ */
function rysujOsobe(c, cx, by, o) {
  const skora = o.skora || "#f1c27d", wl = o.wlosy || "#3b2a1a", ko = o.kolor || "#888888";
  const ciemny = shade(ko, -0.3), spodnie = o.spodnie || "#34495e", kier = o.kier || "d";
  if (!o.siedzi) {
    const a = o.krok === 1 ? 1 : 0, b = o.krok === 2 ? 1 : 0;
    OR(c, cx - 4, by - 6, 3, 6 - a, spodnie); OR(c, cx + 1, by - 6, 3, 6 - b, spodnie);
    R(c, cx - 4, by - 1 - a, 3, 1, "#2b2b2b"); R(c, cx + 1, by - 1 - b, 3, 1, "#2b2b2b");
  }
  // ręce
  if (o.reka) { OR(c, cx + 5, by - 26, 2, 13, ciemny); R(c, cx + 5, by - 27, 2, 2, skora); }
  else if (!o.siedzi) { OR(c, cx + 5, by - 13, 2, 6, ciemny); R(c, cx + 5, by - 8, 2, 2, skora); }
  else OR(c, cx + 5, by - 13, 2, 5, ciemny);
  if (!o.siedzi) { OR(c, cx - 7, by - 13, 2, 6, ciemny); R(c, cx - 7, by - 8, 2, 2, skora); }
  else OR(c, cx - 7, by - 13, 2, 5, ciemny);
  // tułów
  OR(c, cx - 5, by - 13, 10, 8, ko); R(c, cx - 5, by - 13, 10, 1, shade(ko, 0.2));
  if (o.krata) { R(c, cx - 5, by - 10, 10, 1, ciemny); R(c, cx - 2, by - 13, 1, 8, ciemny); R(c, cx + 2, by - 13, 1, 8, ciemny); }
  if (kier === "d") { R(c, cx - 1, by - 13, 2, 2, skora); }
  // głowa + fryzura
  const fr = o.fryzura || "krotkie";
  const extra = [];
  if (fr === "dlugie") extra.push([cx - 7, by - 21, 2, 10], [cx + 5, by - 21, 2, 10]);
  if (fr === "kok") extra.push([cx - 2, by - 26, 4, 3]);
  if (fr === "kucyk") extra.push(kier === "l" ? [cx - 7, by - 21, 2, 8] : [cx + 5, by - 21, 2, 8]);
  if (fr === "czapka") extra.push([cx - 6, by - 26, 12, 5], [cx - 1, by - 28, 2, 2]);
  for (const [x, y, w, h] of extra) R(c, x - 1, y - 1, w + 2, h + 2, OUT);
  OR(c, cx - 5, by - 23, 10, 10, skora);
  for (const [x, y, w, h] of extra) R(c, x, y, w, h, fr === "czapka" ? (h === 2 ? "#f4f1ea" : shade(ko, -0.15)) : wl);
  if (kier === "u") {
    R(c, cx - 5, by - 23, 10, fr === "lysy" ? 6 : 10, fr === "lysy" ? skora : wl);
    if (fr === "lysy") R(c, cx - 5, by - 17, 10, 4, wl);
    if (fr === "czapka") R(c, cx - 5, by - 23, 10, 3, shade(ko, -0.15));
    return;
  }
  if (fr !== "lysy" && fr !== "czapka") {
    R(c, cx - 5, by - 23, 10, 3, wl);
    if (kier === "d") { R(c, cx - 5, by - 20, 1, 2, wl); R(c, cx + 4, by - 20, 1, 2, wl); }
    if (fr === "dlugie" && kier === "d") { R(c, cx - 5, by - 20, 2, 6, wl); R(c, cx + 3, by - 20, 2, 6, wl); }
  }
  if (fr === "czapka") { R(c, cx - 5, by - 21, 10, 1, shade(ko, -0.4)); R(c, cx - 5, by - 20, 1, 2, wl); R(c, cx + 4, by - 20, 1, 2, wl); }
  if (fr === "lysy") { R(c, cx - 5, by - 20, 1, 3, wl); R(c, cx + 4, by - 20, 1, 3, wl); R(c, cx - 4, by - 16, 8, 3, wl); R(c, cx - 2, by - 16, 4, 1, shade(skora, -0.2)); R(c, cx - 2, by - 22, 2, 1, shade(skora, 0.35)); }
  if (kier === "l") R(c, cx + 1, by - 22, 4, 6, wl);
  if (kier === "r") R(c, cx - 5, by - 22, 4, 6, wl);
  const oko = o.mrug ? 1 : 2, oy = by - 18 + (o.mrug ? 1 : 0);
  if (kier === "d") { R(c, cx - 3, oy, 1, oko, OUT); R(c, cx + 2, oy, 1, oko, OUT); R(c, cx - 4, by - 16, 1, 1, "#f19a8e"); R(c, cx + 3, by - 16, 1, 1, "#f19a8e"); }
  if (kier === "l") R(c, cx - 4, oy, 1, oko, OUT);
  if (kier === "r") R(c, cx + 3, oy, 1, oko, OUT);
}

function rysujRobota(c, cx, by, t, kolor) {
  const f = Math.round(Math.sin(t / 500) * 1.5);
  const y = by - 30 + f;
  // piedestał
  OR(c, cx - 15, by - 10, 30, 8, "#3d4660"); R(c, cx - 15, by - 10, 30, 2, "#56627f");
  const p = 0.5 + 0.5 * Math.sin(t / 400);
  c.globalAlpha = 0.35 + 0.35 * p; R(c, cx - 12, by - 12, 24, 2, kolor); c.globalAlpha = 1;
  // dysze
  if (Math.floor(t / 120) % 2) { R(c, cx - 4, y + 22, 2, 2, "#ffd166"); R(c, cx + 2, y + 22, 2, 2, "#ffd166"); }
  // korpus
  OR(c, cx - 6, y + 13, 12, 9, "#e8e8ec"); R(c, cx - 6, y + 13, 12, 1, "#ffffff");
  R(c, cx - 2, y + 16, 4, 3, kolor); R(c, cx - 1, y + 17, 2, 1, "#ffffff");
  OR(c, cx - 9, y + 14, 2, 5, "#c9ccd1"); OR(c, cx + 7, y + 14, 2, 5, "#c9ccd1");
  // twarz
  OR(c, cx - 8, y + 6, 16, 7, "#d97742"); R(c, cx - 8, y + 6, 16, 1, "#f0a070");
  const mr = Math.floor(t / 2600) % 7 === 0 && (t % 2600) < 160;
  R(c, cx - 5, y + 8 + (mr ? 1 : 0), 3, mr ? 1 : 3, "#bff6ff"); R(c, cx + 2, y + 8 + (mr ? 1 : 0), 3, mr ? 1 : 3, "#bff6ff");
  // szklana kopuła z mózgiem
  OR(c, cx - 7, y - 4, 14, 10, "#9fd8ef"); R(c, cx - 6, y - 5, 12, 1, "#9fd8ef");
  R(c, cx - 5, y - 2, 10, 7, "#ff8fb1"); R(c, cx - 4, y - 3, 8, 1, "#ff8fb1");
  R(c, cx - 1, y - 3, 1, 8, "#e0628a"); R(c, cx - 4, y, 3, 1, "#e0628a"); R(c, cx + 1, y + 2, 3, 1, "#e0628a"); R(c, cx - 3, y + 3, 2, 1, "#e0628a");
  R(c, cx - 6, y - 3, 1, 3, "#e8f8ff"); R(c, cx - 5, y - 4, 2, 1, "#e8f8ff");
}

/* ============================ dymki ============================ */
const GLIFY = {
  czeka: ["..#..", "..#..", "..#..", ".....", "..#.."],
  gotowe: [".....", "....#", "...#.", "#.#..", ".#..."],
  blad: ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
  wolne: ["####.", "..#..", ".#...", "####.", "....."],
  cisza: [".###.", "#...#", "..##.", ".....", "..#.."],
};
function rysujDymek(c, cx, top, st, t) {
  const kolor = STANY[st].kolor;
  const bob = st === "czeka" ? Math.round(Math.abs(Math.sin(t / 250)) * -2) : Math.round(Math.sin(t / 700));
  const x = cx - 6, y = top - 11 + bob;
  OR(c, x, y, 13, 9, st === "czeka" ? "#fff2d6" : "#ffffff");
  R(c, cx - 1, y + 9, 3, 1, OUT); R(c, cx, y + 9, 1, 1, "#ffffff"); R(c, cx, y + 10, 1, 1, OUT);
  if (st === "pracuje") {
    const n = Math.floor(t / 300) % 4;
    for (let i = 0; i < 3; i++) R(c, x + 3 + i * 3, y + 4, 2, 2, i < n ? kolor : "#d0d0d0");
    return;
  }
  const g = GLIFY[st]; if (!g) return;
  const dy = st === "wolne" ? Math.floor(t / 600) % 2 : 0;
  g.forEach((w, j) => [...w].forEach((ch, i) => { if (ch === "#") R(c, x + 4 + i, y + 2 + j - dy, 1, 1, kolor); }));
}

/* ============================ gracz (Pablo) ============================ */
const pablo = { tx: 5, ty: 6, x: 5 * T + 8, y: 7 * T, kier: "d", sciezka: [], cel: null, krok: 0, dystans: 0 };
const klawisze = new Set();
const PREDKOSC = 84; // px/s

function wolne(x, y) { return x >= 0 && y >= 0 && x < MW && y < MH && !solid[y][x]; }
function bfs(sx, sy, czyCel) {
  const prev = new Map(), k = (x, y) => y * MW + x, q = [[sx, sy]];
  prev.set(k(sx, sy), null);
  while (q.length) {
    const [x, y] = q.shift();
    if (czyCel(x, y)) { const sc = []; let n = k(x, y); while (n !== null && n !== k(sx, sy)) { sc.unshift([n % MW, Math.floor(n / MW)]); n = prev.get(n); } return sc; }
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, ny = y + dy;
      if (wolne(nx, ny) && !prev.has(k(nx, ny))) { prev.set(k(nx, ny), k(x, y)); q.push([nx, ny]); }
    }
  }
  return null;
}
function idzDoKafla(tx, ty) {
  const s = bfs(pablo.tx, pablo.ty, (x, y) => x === tx && y === ty) ||
    bfs(pablo.tx, pablo.ty, (x, y) => Math.abs(x - tx) + Math.abs(y - ty) <= 1);
  if (s) pablo.sciezka = s;
}
function idzDo(kafle) {
  const s = bfs(pablo.tx, pablo.ty, (x, y) => kafle.some(([a, b]) => Math.abs(a - x) + Math.abs(b - y) === 1));
  if (s) pablo.sciezka = s;
}
function aktualizujPablo(dt) {
  if (!pablo.cel) {
    let nast = null;
    if (pablo.sciezka.length) nast = pablo.sciezka.shift();
    else {
      const d = kierunekZKlawiszy();
      if (d) {
        pablo.kier = d[2];
        if (wolne(pablo.tx + d[0], pablo.ty + d[1])) nast = [pablo.tx + d[0], pablo.ty + d[1]];
      }
    }
    if (nast) {
      const [nx, ny] = nast;
      pablo.kier = nx > pablo.tx ? "r" : nx < pablo.tx ? "l" : ny > pablo.ty ? "d" : "u";
      pablo.cel = nast;
    }
  }
  if (pablo.cel) {
    const cx = pablo.cel[0] * T + 8, cy = (pablo.cel[1] + 1) * T;
    const dx = cx - pablo.x, dy = cy - pablo.y, d = Math.hypot(dx, dy), s = PREDKOSC * dt;
    pablo.dystans += s;
    if (d <= s) { pablo.x = cx; pablo.y = cy; pablo.tx = pablo.cel[0]; pablo.ty = pablo.cel[1]; pablo.cel = null; }
    else { pablo.x += dx / d * s; pablo.y += dy / d * s; }
    pablo.krok = Math.floor(pablo.dystans / 6) % 4 === 1 ? 1 : Math.floor(pablo.dystans / 6) % 4 === 3 ? 2 : 0;
  } else pablo.krok = 0;
}
function kierunekZKlawiszy() {
  if (klawisze.has("ArrowUp") || klawisze.has("w")) return [0, -1, "u"];
  if (klawisze.has("ArrowDown") || klawisze.has("s")) return [0, 1, "d"];
  if (klawisze.has("ArrowLeft") || klawisze.has("a")) return [-1, 0, "l"];
  if (klawisze.has("ArrowRight") || klawisze.has("d")) return [1, 0, "r"];
  return null;
}

/* ============================ rozmieszczenie zespołu ============================ */
function rozmiesc() {
  let z = 0;
  osoby = [];
  for (const o of DANE.zespol) {
    if (o.id === "klaudiusz") { klaudiusz = o; continue; }
    const m = MIEJSCA[o.id] || ZAPASOWE[z++];
    if (!m) continue;
    o.dx = m[0]; o.dy = m[1];
    o.skora = SKORY[hash(o.id) % SKORY.length];
    o.kafle = [[o.dx, o.dy - 1], [o.dx + 1, o.dy - 1], [o.dx, o.dy], [o.dx + 1, o.dy]];
    blok(o.dx, o.dy - 1, 2, 2);
    osoby.push(o);
  }
}
function rysujStanowisko(c, o, t) {
  const x0 = o.dx * T, y0 = o.dy * T, cx = x0 + 16, by = y0 + 1, st = stanEf(o), kol = STANY[st].kolor;
  OR(c, cx - 7, by - 18, 14, 11, "#3d3f4a"); R(c, cx - 6, by - 17, 12, 2, "#555869");
  const odd = Math.sin(t / 900 + hash(o.id)) > 0.85 ? -1 : 0;
  rysujOsobe(c, cx, by + odd, { ...o, siedzi: true, reka: st === "czeka", mrug: (t + hash(o.id) * 37) % 3200 < 140 });
  // biurko
  OR(c, x0 + 1, y0 + 4, 30, 6, "#6e4420");
  OR(c, x0 + 1, y0 - 6, 30, 10, "#a06a35"); R(c, x0 + 1, y0 - 6, 30, 1, "#b97c42");
  R(c, x0 + 2, y0 + 10, 2, 5, "#4a2e16"); R(c, x0 + 28, y0 + 10, 2, 5, "#4a2e16");
  // laptop (tył klapy), kubek, kartka w kolorze roli
  OR(c, x0 + 3, y0 - 13, 10, 8, "#c9ccd1"); R(c, x0 + 4, y0 - 12, 8, 1, "#e1e4e8");
  c.globalAlpha = st === "pracuje" ? 0.6 + 0.4 * Math.sin(t / 200) : 1; R(c, x0 + 7, y0 - 10, 2, 2, kol); c.globalAlpha = 1;
  OR(c, x0 + 2, y0 - 5, 12, 2, "#9ea3aa");
  OR(c, x0 + 25, y0 - 6, 3, 4, "#f4f1ea"); R(c, x0 + 25, y0 - 5, 3, 1, o.kolor || "#888");
  OR(c, x0 + 18, y0 - 4, 5, 4, shade(o.kolor || "#888888", 0.55));
  // dłonie na blacie
  const pis = st === "pracuje" ? Math.floor(t / 140) % 2 : 0;
  if (st !== "czeka") OR(c, cx + 3, y0 - 7 - pis, 3, 2, o.skora);
  OR(c, cx - 6, y0 - 7 - (st === "pracuje" ? 1 - pis : 0), 3, 2, o.skora);
}

/* ============================ render ============================ */
const canvas = $("#mapa"), ctx = canvas.getContext("2d");
let tlo = null, S = 3, VW = MW, VH = MH, camX = 0, camY = 0, cssW = 0;
let najechany = null, blisko = null;

function rozmiar() {
  const ramka = $("#mapa-ramka");
  cssW = ramka.clientWidth;
  const waski = cssW < 640;
  VW = waski ? 17 : MW; VH = waski ? 15 : MH;
  const dpr = window.devicePixelRatio || 1;
  S = Math.max(1, Math.ceil((cssW * dpr) / (VW * T)));
  canvas.width = VW * T * S; canvas.height = VH * T * S;
  canvas.style.height = (cssW * VH / VW) + "px";
}
function kamera(natychmiast) {
  const vw = VW * T, vh = VH * T;
  const tx = Math.max(0, Math.min(MW * T - vw, pablo.x - vw / 2));
  const ty = Math.max(0, Math.min(MH * T - vh, pablo.y - 10 - vh / 2));
  if (natychmiast) { camX = tx; camY = ty; } else { camX += (tx - camX) * 0.12; camY += (ty - camY) * 0.12; }
}
function niebo(h) {
  if (h >= 8 && h < 15) return ["#7ec8f0", "#bde6ff"];
  if (h >= 6 && h < 8) return ["#f5b971", "#ffd9a8"];
  if (h >= 15 && h < 17) return ["#f08a5d", "#f7c59f"];
  return ["#0f1b3d", "#1d2b5a"];
}
function rysujScianyDynamiczne(c, t) {
  const { h, m } = godzinaPL(), [n1, n2] = niebo(h), noc = n1 === "#0f1b3d";
  for (const x of [3, 6, 24, 27]) {
    const x0 = x * T + 2, w = 2 * T - 4;
    OR(c, x0, 6, w, 13, n1, "#5a4030"); R(c, x0, 6, w, 5, n2);
    if (noc) { R(c, x0 + 4, 9, 1, 1, "#fff"); R(c, x0 + 17, 8, 1, 1, "#fff"); R(c, x0 + 11, 13, 1, 1, "#ffe9a8"); }
    else { R(c, x0 + 5 + (Math.floor(t / 4000) % 10), 9, 6, 2, "#ffffff"); }
    R(c, x0 + w / 2 - 1, 6, 2, 13, "#5a4030"); R(c, x0, 12, w, 1, "#5a4030");
  }
  // zegar
  const zx = 8 * T + 8, zy = 12;
  OR(c, zx - 5, zy - 5, 10, 10, "#f4f1ea");
  const kat = (v) => v * Math.PI * 2 - Math.PI / 2;
  const hk = kat(((h % 12) + m / 60) / 12), mk = kat(m / 60);
  for (let i = 1; i <= 3; i++) R(c, Math.round(zx + Math.cos(mk) * i), Math.round(zy + Math.sin(mk) * i), 1, 1, OUT);
  for (let i = 1; i <= 2; i++) R(c, Math.round(zx + Math.cos(hk) * i), Math.round(zy + Math.sin(hk) * i), 1, 1, "#c0392b");
  // neon nad mózgiem
  c.globalAlpha = 0.75 + 0.25 * Math.sin(t / 300);
  R(c, 13 * T + 8, 7, 5 * T, 1, "#ff8fb1"); R(c, 13 * T + 8, 18, 5 * T, 1, "#ff8fb1");
  c.globalAlpha = 1;
  // tablica z karteczkami (stany pracowników)
  const bx = TABLICA.x * T + 2, byy = 9 * T + 3;
  OR(c, bx, byy, TABLICA.w * T - 4, 10, "#f7f7f2", "#7f8c8d");
  osoby.forEach((o, i) => R(c, bx + 3 + i * 10, byy + 2 + (i % 2), 7, 6, STANY[stanEf(o)].kolor));
}
function rysujCzastki(c, t) {
  for (const o of osoby) {
    if (stanEf(o) !== "pracuje") continue;
    const sx = o.dx * T + 16, sy = o.dy * T - 14, ex = KLAUDIUSZ.cx, ey = KLAUDIUSZ.by - 24;
    for (let i = 0; i < 3; i++) {
      const p = ((t / 2600) + i / 3 + (hash(o.id) % 100) / 100) % 1;
      const x = sx + (ex - sx) * p, y = sy + (ey - sy) * p - Math.sin(p * Math.PI) * 24;
      c.globalAlpha = Math.sin(p * Math.PI); R(c, Math.round(x), Math.round(y), 2, 2, o.kolor || "#fff"); c.globalAlpha = 1;
    }
  }
}
function etykieta(tekst, wx, wy, opcje = {}) {
  const k = canvas.width / cssW;
  const sx = (wx - camX) * S, sy = (wy - camY) * S;
  const fs = Math.round((opcje.rozmiar || 12) * k);
  ctx.font = `${opcje.gruby ? 600 : 400} ${fs}px "Pixelify Sans", ui-monospace, monospace`;
  const w = ctx.measureText(tekst).width + fs * 0.9, h = fs * 1.45;
  if (opcje.tlo !== false) {
    ctx.fillStyle = opcje.tlo || "rgba(18,13,9,.82)"; ctx.fillRect(Math.round(sx - w / 2), Math.round(sy), Math.round(w), Math.round(h));
    if (opcje.ramka) { ctx.strokeStyle = opcje.ramka; ctx.lineWidth = Math.max(1, k * 1.5); ctx.strokeRect(Math.round(sx - w / 2), Math.round(sy), Math.round(w), Math.round(h)); }
  }
  ctx.fillStyle = opcje.kolor || "#f3eadf"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillText(tekst, sx, sy + h / 2 + k * 0.5);
}
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = "#0d0a07"; ctx.fillRect(0, 0, canvas.width, canvas.height);
  const ox = Math.round(camX * S), oy = Math.round(camY * S);
  ctx.setTransform(S, 0, 0, S, -ox, -oy);
  ctx.drawImage(tlo, 0, 0);
  rysujScianyDynamiczne(ctx, t);
  const kSt = klaudiusz ? stanEf(klaudiusz) : "wolne";
  const lista = [
    ...meble.map((m) => ({ y: m.baseY, f: () => m.rysuj(ctx, t) })),
    ...osoby.map((o) => ({ y: (o.dy + 1) * T, f: () => rysujStanowisko(ctx, o, t) })),
    { y: KLAUDIUSZ.by, f: () => rysujRobota(ctx, KLAUDIUSZ.cx, KLAUDIUSZ.by, t, STANY[kSt].kolor) },
    { y: pablo.y, f: () => rysujOsobe(ctx, Math.round(pablo.x), Math.round(pablo.y), { skora: "#f1c27d", wlosy: "#2b1d16", fryzura: "krotkie", kolor: "#b03a2e", krata: true, spodnie: "#2f4a6d", kier: pablo.kier, krok: pablo.krok, mrug: t % 4100 < 140 }) },
  ].sort((a, b) => a.y - b.y);
  for (const e of lista) e.f();
  rysujCzastki(ctx, t);
  for (const o of osoby) rysujDymek(ctx, o.dx * T + 16, o.dy * T - 26, stanEf(o), t + hash(o.id));
  if (klaudiusz) rysujDymek(ctx, KLAUDIUSZ.cx, KLAUDIUSZ.by - 36, kSt, t);

  // napisy (w pikselach ekranu – ostre)
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const pok = [["GABINET SZEFA", 5.5, 2.2], ["MÓZG OPERACJI", 16, 2.2], ["KUCHNIA", 26.5, 3.5], ["OPEN SPACE", 6.5, 10.25]];
  for (const [n, x, y] of pok) etykieta(n, x * T, y * T, { tlo: false, kolor: "rgba(255,255,255,.55)", rozmiar: 10 });
  ctx.globalAlpha = 0.8 + 0.2 * Math.sin(t / 300);
  etykieta("KLAUDIUSZ", 16 * T, 8.6, { tlo: false, kolor: "#ff8fb1", rozmiar: 10, gruby: true });
  ctx.globalAlpha = 1;
  etykieta("FUDALI", 10.5 * T - 2, 9 * T + 3.5, { tlo: false, kolor: "#fbe3c0", rozmiar: 9, gruby: true });
  etykieta(`📋 Prośby: ${liczProsby()}`, (TABLICA.x + TABLICA.w / 2) * T, 10 * T + 1, { rozmiar: 10, ramka: liczProsby() ? STANY.czeka.kolor : null });
  for (const o of osoby) {
    const st = stanEf(o), hov = najechany && najechany.id === o.id;
    etykieta(`${o.emoji || ""} ${o.imie || o.id}`, o.dx * T + 16, (o.dy + 1) * T + 1, { ramka: hov || wybrany === o.id ? "#ffd166" : STANY[st].kolor, kolor: o.wdrozenie === "makieta" ? "#d8ccbc" : "#ffffff", rozmiar: 11 });
  }
  etykieta("🧠 Klaudiusz", KLAUDIUSZ.cx, KLAUDIUSZ.by + 1, { ramka: najechany && najechany.id === "klaudiusz" ? "#ffd166" : STANY[kSt].kolor, rozmiar: 11, gruby: true });
  etykieta("👑 Pablo (Ty)", pablo.x, pablo.y + 2, { rozmiar: 10, kolor: "#ffd166" });
}

/* ============================ interakcja ============================ */
function trafienie(wx, wy) {
  for (const o of osoby) {
    const cx = o.dx * T + 16, by = o.dy * T;
    if (wx >= cx - 14 && wx <= cx + 14 && wy >= by - 34 && wy <= by + 24) return { id: o.id, kafle: o.kafle };
  }
  if (Math.abs(wx - KLAUDIUSZ.cx) <= 16 && wy >= KLAUDIUSZ.by - 48 && wy <= KLAUDIUSZ.by + 12) return { id: "klaudiusz", kafle: [[15, 4], [16, 4], [15, 5], [16, 5]] };
  if (wx >= TABLICA.x * T && wx <= (TABLICA.x + TABLICA.w) * T && wy >= 9 * T && wy <= 11 * T) return { id: "@prosby", kafle: [[19, 9], [20, 9], [21, 9], [22, 9], [23, 9]] };
  return null;
}
function doSwiata(e) {
  const r = canvas.getBoundingClientRect();
  return [(e.clientX - r.left) / r.width * VW * T + camX, (e.clientY - r.top) / r.height * VH * T + camY];
}
function obokPablo() {
  const cele = [...osoby.map((o) => ({ id: o.id, kafle: o.kafle, nazwa: o.imie })),
    { id: "klaudiusz", kafle: [[15, 4], [16, 4], [15, 5], [16, 5]], nazwa: "Klaudiuszem" },
    { id: "@prosby", kafle: [[19, 9], [20, 9], [21, 9], [22, 9], [23, 9]], nazwa: "tablicą próśb" }];
  for (const c of cele) if (c.kafle.some(([x, y]) => Math.max(Math.abs(x - pablo.tx), Math.abs(y - pablo.ty)) <= 1)) return c;
  return null;
}
canvas.addEventListener("mousemove", (e) => {
  const [wx, wy] = doSwiata(e);
  najechany = trafienie(wx, wy);
  canvas.classList.toggle("klik", !!najechany);
});
canvas.addEventListener("mouseleave", () => { najechany = null; });
canvas.addEventListener("click", (e) => {
  canvas.focus({ preventScroll: true });
  const [wx, wy] = doSwiata(e);
  const traf = trafienie(wx, wy);
  if (traf) { idzDo(traf.kafle); otworz(traf.id); }
  else idzDoKafla(Math.floor(wx / T), Math.floor(wy / T));
});
const KLAWISZE_RUCHU = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "w", "a", "s", "d"];
window.addEventListener("keydown", (e) => {
  if ($("#podglad").open) return;
  const ae = document.activeElement;
  const naMapie = !ae || ae === document.body || ae === canvas;
  const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
  if (k === "Escape") { zamknijPanel(); return; }
  if (!naMapie || e.ctrlKey || e.metaKey || e.altKey) return;
  if (KLAWISZE_RUCHU.includes(k)) { klawisze.add(k); pablo.sciezka = []; e.preventDefault(); }
  if (k === "e" || k === "Enter" || k === " ") { const b = obokPablo(); if (b) { otworz(b.id); e.preventDefault(); } }
});
window.addEventListener("keyup", (e) => klawisze.delete(e.key.length === 1 ? e.key.toLowerCase() : e.key));
window.addEventListener("blur", () => klawisze.clear());

/* ============================ panel ============================ */
function liczProsby() { return DANE.zespol.reduce((s, o) => s + ((o.status && o.status.prosby) || []).length, 0); }
function znajdz(id) { return DANE.zespol.find((o) => o.id === id); }
function chipStanu(st) { return `<span class="stan ${st}" style="--k:${STANY[st].kolor}">${STANY[st].nazwa}</span>`; }

function avatar(o, skala = 4) {
  const c = document.createElement("canvas"); c.width = 24 * skala; c.height = 30 * skala;
  const g = c.getContext("2d"); g.imageSmoothingEnabled = false; g.scale(skala, skala);
  if (o.id === "klaudiusz") rysujRobota(g, 12, 36, 0, STANY[stanEf(o)].kolor);
  else rysujOsobe(g, 12, 29, { ...o, skora: o.skora || SKORY[hash(o.id) % SKORY.length] });
  return c;
}
function htmlProsby(o, zNazwa) {
  const p = (o.status && o.status.prosby) || [];
  if (!p.length) return "";
  return `<ul class="prosby">${p.map((x) => `<li>${zNazwa ? `<span class="kto">${esc(o.emoji || "")} ${esc(o.imie)} · ${esc(o.rola || "")}</span>` : ""}${x.pilne ? "⚠️ " : ""}${esc(x.tresc)}<div class="male">${esc(kiedy(x.czas))}</div>${zNazwa ? `<button class="przycisk" data-idz="${esc(o.id)}" type="button">Przejdź do biurka →</button>` : ""}</li>`).join("")}</ul>`;
}
function otworz(id) {
  wybrany = id;
  const panel = $("#panel"), tresc = $("#panel-tresc");
  if (id === "@prosby") {
    const z = DANE.zespol.filter((o) => (o.status?.prosby || []).length);
    tresc.innerHTML = `<div class="p-glowa"><div><h2>🙋 Prośby do Ciebie</h2><div class="rola">${liczProsby()} – czego zespół potrzebuje od szefa</div></div></div>
      <div class="sekcja">${z.length ? z.map((o) => htmlProsby(o, true)).join("") : "<p>Nikt niczego nie potrzebuje. 🎉</p>"}
      <p class="wskazowka">Odpowiedz Klaudiuszowi w czacie (albo na Telegramie) – np. „cennik jest w załączniku”. Po załatwieniu prośba zniknie z tablicy.</p></div>`;
  } else {
    const o = znajdz(id); if (!o) return;
    const s = o.status || {}, st = stanEf(o);
    const postep = typeof s.postep === "number" && st === "pracuje" ? `<div class="pasek"><div style="width:${Math.max(0, Math.min(100, s.postep))}%"></div></div>` : "";
    const wyniki = (o.wyniki || []).map((w) => `<button class="plik" type="button" data-plik="${esc(w.url)}" data-tytul="${esc(w.sciezka)}">📄 ${esc(w.sciezka.split("/").pop())}<small>${esc(w.sciezka)}</small></button>`).join("");
    const dziennik = (s.dziennik || []).slice(0, 12).map((d) => `<li><i style="--k:${(STANY[d.stan] || STANY.wolne).kolor}"></i><time>${esc(kiedy(d.czas))}</time><span>${esc(d.tekst)}</span></li>`).join("");
    const zapisy = id === "klaudiusz" && DANE.zapisy?.length ? `<div class="sekcja"><h3>💾 Ostatnie zapisy w archiwum</h3><ul class="dziennik">${DANE.zapisy.slice(0, 10).map((z) => `<li><i style="--k:#d97742"></i><time>${esc(kiedy(z.czas))}</time><span>${esc(z.tekst)}</span></li>`).join("")}</ul></div>` : "";
    tresc.innerHTML = `<div class="p-glowa"><span id="p-avatar"></span><div>
        <h2>${esc(o.emoji || "")} ${esc(o.imie || o.id)}${o.przydomek ? ` <small>„${esc(o.przydomek)}”</small>` : ""}</h2>
        <div class="rola">${esc(o.rola || "")}</div>${chipStanu(st)}${o.wdrozenie === "makieta" ? `<span class="makieta" title="Rola zaprojektowana – automaty jeszcze nie działają">🧩 makieta</span>` : ""}</div></div>
      <div class="sekcja"><h3>⌨️ Teraz</h3><p>${esc(s.zadanie || "—")}</p>${postep}<div class="male">Ostatni sygnał: ${esc(kiedy(s.aktualizacja))}${s.makieta ? " · przykładowe dane (makieta)" : ""}</div></div>
      ${(s.prosby || []).length ? `<div class="sekcja"><h3>🙋 Potrzebuje od Ciebie</h3>${htmlProsby(o, false)}<p class="wskazowka">Odpowiedz Klaudiuszowi w czacie – on przekaże dalej.</p></div>` : ""}
      <div class="sekcja"><h3>📂 Ostatnie wyniki</h3><div class="pliki">${wyniki || `<p class="male">Jeszcze nic – ${o.wdrozenie === "makieta" ? "rola czeka na wdrożenie." : "pierwsze wyniki pojawią się po najbliższym przebiegu."}</p>`}</div></div>
      ${dziennik ? `<div class="sekcja"><h3>🗒️ Dziennik</h3><ul class="dziennik">${dziennik}</ul></div>` : ""}
      ${zapisy}
      <details class="karta-prac"><summary>🪪 Karta pracownika (co robi, jakich narzędzi używa)</summary><div class="md">${renderMd(o.karta || "")}</div></details>`;
    $("#p-avatar").replaceWith(avatar(o));
  }
  panel.hidden = false;
  $(".uklad").classList.add("z-panelem");
  requestAnimationFrame(() => { rozmiar(); kamera(true); });
  panel.scrollTop = 0;
}
function zamknijPanel() {
  if ($("#podglad").open) return;
  wybrany = null; $("#panel").hidden = true; $(".uklad").classList.remove("z-panelem");
  requestAnimationFrame(() => { rozmiar(); kamera(true); });
}
$("#panel-zamknij").addEventListener("click", zamknijPanel);
$("#chip-prosby").addEventListener("click", () => otworz("@prosby"));
document.addEventListener("click", async (e) => {
  const idz = e.target.closest("[data-idz]");
  if (idz) { const o = znajdz(idz.dataset.idz); if (o?.kafle) idzDo(o.kafle); otworz(idz.dataset.idz); return; }
  const p = e.target.closest("[data-plik]");
  if (p) {
    $("#podglad-tytul").textContent = p.dataset.tytul;
    $("#podglad-tresc").innerHTML = "<p>Wczytuję…</p>";
    $("#podglad").showModal();
    try {
      const r = await fetch(p.dataset.plik, { cache: "no-cache" });
      if (!r.ok) throw new Error(r.status);
      const txt = await r.text();
      MD_BAZA = p.dataset.plik.replace(/[^/]*$/, "");
      $("#podglad-tresc").innerHTML = p.dataset.plik.endsWith(".md") ? renderMd(txt) : `<pre><code>${esc(txt)}</code></pre>`;
      MD_BAZA = "";
    } catch (err) { $("#podglad-tresc").innerHTML = `<p>Nie udało się wczytać pliku (${esc(err.message)}).</p>`; }
  }
});
$("#podglad-zamknij").addEventListener("click", () => $("#podglad").close());

/* ============================ karty zespołu ============================ */
function odswiezUI(panelTez = true) {
  const karty = $("#karty"); karty.innerHTML = "";
  for (const o of DANE.zespol) {
    const st = stanEf(o), n = (o.status?.prosby || []).length;
    const b = document.createElement("button"); b.type = "button"; b.className = "karta";
    b.innerHTML = `<span></span><span><b>${esc(o.emoji || "")} ${esc(o.imie || o.id)}</b><span class="rola">${esc(o.rola || "")}</span>${chipStanu(st)}${o.wdrozenie === "makieta" ? `<span class="makieta">🧩 makieta</span>` : ""}<span class="zad">${esc(o.status?.zadanie || "")}</span>${n ? `<span class="ile-prosb">🙋 ${n} ${n === 1 ? "prośba" : n < 5 ? "prośby" : "próśb"} do Ciebie</span>` : ""}</span>`;
    b.firstChild.replaceWith(avatar(o, 2));
    b.addEventListener("click", () => { if (o.kafle) idzDo(o.kafle); otworz(o.id); window.scrollTo({ top: 0, behavior: "smooth" }); });
    karty.appendChild(b);
  }
  const ile = liczProsby();
  $("#licz-prosby").textContent = ile;
  $("#chip-prosby").classList.toggle("sa", ile > 0);
  $("#licz-pracuje").textContent = DANE.zespol.filter((o) => stanEf(o) === "pracuje").length;
  $("#aktualizacja").textContent = `Dane: ${kiedy(DANE.zbudowano)}`;
  $("#aktualizacja").title = `Zbudowano: ${DANE.zbudowano || "—"} ${DANE.wersja || ""}`;
  if (panelTez && wybrany && !$("#podglad").open) { const sc = $("#panel").scrollTop; otworz(wybrany); $("#panel").scrollTop = sc; }
}

/* ============================ markdown (prosty, bezpieczny) ============================ */
let MD_BAZA = "";
function obrazek(alt, src) {
  const u = /^https?:\/\//i.test(src) ? src : new URL(src, location.origin + "/" + MD_BAZA).pathname;
  return `<img src="${esc(u)}" alt="${esc(alt)}" loading="lazy">`;
}
function inline(s) {
  return s.split(/(`[^`]+`)/g).map((cz) => {
    if (cz.startsWith("`") && cz.endsWith("`") && cz.length > 1) return `<code>${esc(cz.slice(1, -1))}</code>`;
    const obr = [];
    cz = cz.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (_, alt, src) => { obr.push(obrazek(alt, src)); return `\u0000${obr.length - 1}\u0000`; });
    let h = esc(cz);
    h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (_, t, u) => `<a href="${u}" target="_blank" rel="noopener noreferrer">${t}</a>`);
    h = h.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, t) => t);
    h = h.replace(/(^|[\s(])(https?:\/\/[^\s<)]+)/g, (_, p, u) => `${p}<a href="${u}" target="_blank" rel="noopener noreferrer">${u}</a>`);
    h = h.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>").replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>");
    return h.replace(/\u0000(\d+)\u0000/g, (_, n) => obr[+n]);
  }).join("");
}
function renderMd(md) {
  const linie = md.replace(/\r/g, "").split("\n"), out = [];
  let i = 0;
  const lista = (typ) => { const el = []; const re = typ === "ol" ? /^\s*\d+[.)]\s+(.*)$/ : /^\s*[-*+]\s+(.*)$/; while (i < linie.length && re.test(linie[i])) { el.push(`<li>${inline(linie[i].match(re)[1])}</li>`); i++; } out.push(`<${typ}>${el.join("")}</${typ}>`); };
  while (i < linie.length) {
    const l = linie[i];
    if (/^```/.test(l)) { const kod = []; i++; while (i < linie.length && !/^```/.test(linie[i])) kod.push(linie[i++]); i++; out.push(`<pre><code>${esc(kod.join("\n"))}</code></pre>`); continue; }
    if (/^\s*$/.test(l)) { i++; continue; }
    const hm = l.match(/^(#{1,6})\s+(.*)$/); if (hm) { const n = Math.min(hm[1].length, 4); out.push(`<h${n}>${inline(hm[2])}</h${n}>`); i++; continue; }
    if (/^\s*([-*_])\s*\1\s*\1[-*_\s]*$/.test(l)) { out.push("<hr>"); i++; continue; }
    if (/^\s*\|/.test(l)) {
      const wiersze = []; while (i < linie.length && /^\s*\|/.test(linie[i])) wiersze.push(linie[i++]);
      const kom = (w) => w.trim().replace(/^\||\|$/g, "").split("|").map((x) => x.trim());
      const sep = wiersze.length > 1 && /^[\s|:-]+$/.test(wiersze[1]);
      const nag = sep ? `<thead><tr>${kom(wiersze[0]).map((x) => `<th>${inline(x)}</th>`).join("")}</tr></thead>` : "";
      const ciało = (sep ? wiersze.slice(2) : wiersze).map((w) => `<tr>${kom(w).map((x) => `<td>${inline(x)}</td>`).join("")}</tr>`).join("");
      out.push(`<div class="tabela"><table>${nag}<tbody>${ciało}</tbody></table></div>`); continue;
    }
    if (/^>\s?/.test(l)) { const q = []; while (i < linie.length && /^>\s?/.test(linie[i])) q.push(linie[i++].replace(/^>\s?/, "")); out.push(`<blockquote>${renderMd(q.join("\n"))}</blockquote>`); continue; }
    if (/^\s*[-*+]\s+/.test(l)) { lista("ul"); continue; }
    if (/^\s*\d+[.)]\s+/.test(l)) { lista("ol"); continue; }
    const p = []; while (i < linie.length && linie[i].trim() && !/^(#{1,6}\s|```|\s*\||>|\s*[-*+]\s|\s*\d+[.)]\s)/.test(linie[i])) p.push(linie[i++]);
    if (!p.length) p.push(linie[i++]);
    out.push(`<p>${p.map(inline).join("<br>")}</p>`);
  }
  return out.join("\n");
}

/* ============================ start ============================ */
function toast(t) { const el = $("#toast"); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => (el.hidden = true), 3500); }
async function wczytaj(pierwszy) {
  try {
    const r = await fetch("dane.json", { cache: "no-cache" });
    if (!r.ok) throw new Error(r.status);
    const d = await r.json();
    if (!pierwszy && d.zbudowano === DANE.zbudowano) { odswiezUI(false); return; }
    // nowe dane: zdejmij stare kolizje pracowników i rozmieść ponownie
    for (const o of osoby) for (const [x, y] of o.kafle) solid[y][x] = false;
    DANE = d; rozmiesc(); odswiezUI();
    if (!pierwszy) toast("🔄 Nowe dane z biura");
  } catch (e) { if (pierwszy) toast("Nie udało się wczytać danych biura"); }
}
let ostatni = 0;
function petla(t) {
  const dt = Math.min(0.05, (t - ostatni) / 1000 || 0); ostatni = t;
  aktualizujPablo(dt); kamera(false);
  const b = obokPablo();
  const pp = $("#podpowiedz");
  if (b && b.id !== wybrany) { pp.hidden = false; pp.textContent = `E – porozmawiaj z: ${b.nazwa}`; } else pp.hidden = true;
  blisko = b;
  render(t);
  requestAnimationFrame(petla);
}
tlo = zbudujTlo();
rozmiar(); kamera(true);
window.addEventListener("resize", () => { rozmiar(); kamera(true); });
wczytaj(true).then(() => requestAnimationFrame(petla));
setInterval(() => wczytaj(false), 5 * 60 * 1000);
