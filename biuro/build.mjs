// Buduje wirtualne biuro (statyczna strona) z danych w repozytorium.
// Uruchamiane przez Vercel przy każdym zapisie na main: node biuro/build.mjs  ->  biuro/dist/
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SRC = path.join(ROOT, "biuro", "src");
const DIST = path.join(ROOT, "biuro", "dist");
const ZESPOL = path.join(ROOT, "zespol");
const KOLEJNOSC = ["klaudiusz", "konkurencja", "marketing", "pozycjonowanie", "grafika", "slowa-kluczowe", "sprzedaz", "rynki-zagraniczne"];
const PLIKOW_NA_WZORZEC = 6;
const MAX_ROZMIAR = 400_000;

fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(DIST, { recursive: true });
for (const f of fs.readdirSync(SRC)) fs.copyFileSync(path.join(SRC, f), path.join(DIST, f));

function naglowek(tekst) {
  const dane = {};
  if (!tekst.startsWith("---")) return [dane, tekst];
  const [, nag, ...reszta] = tekst.split(/^---\s*$/m);
  for (const linia of nag.split("\n")) {
    const m = linia.match(/^([\w-]+):\s*(.*?)(\s+#.*)?\s*$/);
    if (m) dane[m[1]] = m[2].replace(/^"(.*)"$/, "$1");
  }
  return [dane, reszta.join("---").trim()];
}

// "raporty/*-konkurencja.md" -> najnowsze pliki (sortowanie po nazwie malejąco – nazwy zaczynają się od daty)
function znajdz(wzorzec) {
  const rel = wzorzec.trim();
  if (!rel) return [];
  const katalog = path.join(ROOT, path.dirname(rel));
  const re = new RegExp("^" + path.basename(rel).replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*") + "$");
  if (!fs.existsSync(katalog) || !fs.statSync(katalog).isDirectory()) return [];
  return fs.readdirSync(katalog)
    .filter((f) => re.test(f) && !f.startsWith(".") && f.toLowerCase() !== "readme.md")
    .filter((f) => fs.statSync(path.join(katalog, f)).isFile())
    .sort().reverse().slice(0, PLIKOW_NA_WZORZEC)
    .map((f) => path.posix.join(path.dirname(rel), f));
}

function kopiuj(rel) {
  const zrodlo = path.join(ROOT, rel);
  const cel = path.join(DIST, "pliki", rel);
  fs.mkdirSync(path.dirname(cel), { recursive: true });
  let tresc = fs.readFileSync(zrodlo, "utf8");
  if (tresc.length > MAX_ROZMIAR) tresc = tresc.slice(0, MAX_ROZMIAR) + "\n\n… (plik ucięty – pełna wersja w archiwum)";
  fs.writeFileSync(cel, tresc);
  // obrazki wskazane w markdown (![opis](../zdjecia/x.jpg)) – kopiujemy, żeby było je widać w biurze
  for (const [, src] of tresc.matchAll(/!\[[^\]]*\]\(([^)\s]+)\)/g)) {
    if (/^https?:/i.test(src)) continue;
    const obr = path.posix.normalize(path.posix.join(path.posix.dirname(rel), src));
    const z = path.join(ROOT, obr);
    if (obr.startsWith("..") || !fs.existsSync(z)) continue;
    const c = path.join(DIST, "pliki", obr);
    fs.mkdirSync(path.dirname(c), { recursive: true });
    fs.copyFileSync(z, c);
  }
  return { sciezka: rel, url: "pliki/" + rel, rozmiar: tresc.length };
}

function czytajJson(p, domyslnie) {
  try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return domyslnie; }
}

// godziny pracy (zmiany) – jedyne miejsce: zespol/godziny.json
const godzinyRej = czytajJson(path.join(ZESPOL, "godziny.json"), {}).pracownicy || {};

const zespol = [];
// karty pracowników = zespol/<id>.md z nagłówkiem „id: <id>” (pozostałe .md w zespol/ to dokumentacja, np. sesje.md)
const pliki = fs.readdirSync(ZESPOL).filter((f) => f.endsWith(".md"))
  .map((f) => f.slice(0, -3))
  .filter((id) => naglowek(fs.readFileSync(path.join(ZESPOL, id + ".md"), "utf8"))[0].id === id);
pliki.sort((a, b) => (KOLEJNOSC.indexOf(a) + 1 || 99) - (KOLEJNOSC.indexOf(b) + 1 || 99));
for (const id of pliki) {
  const [meta, tresc] = naglowek(fs.readFileSync(path.join(ZESPOL, id + ".md"), "utf8"));
  const status = czytajJson(path.join(ZESPOL, "status", id + ".json"), { stan: "wolne", zadanie: "", prosby: [], dziennik: [] });
  const wyniki = [];
  for (const w of (meta.wyniki || "").split(";")) for (const rel of znajdz(w)) wyniki.push(kopiuj(rel));
  const g = godzinyRej[id] || {};
  zespol.push({ id, ...meta, karta: tresc, status, godziny: { godziny: g.godziny || [], dni: g.dni || "codziennie" } });
  zespol.at(-1).wyniki = wyniki;
}

let zapisy = [];
try {
  zapisy = execSync("git log -25 --pretty=format:%cI%x09%s", { cwd: ROOT, encoding: "utf8" })
    .split("\n").filter(Boolean).map((l) => { const [czas, tekst] = l.split("\t"); return { czas, tekst }; });
} catch { /* brak historii w środowisku budowania – trudno */ }

const zbudowano = new Date().toISOString();

// ---------- czat z Pablo: zespol/czat/<id>/*.json → czat/<id>.json (osobny plik na osobę, odświeżany przez okno czatu) ----------
const CZAT = path.join(ZESPOL, "czat");
const MAX_WIADOMOSCI = 300, MAX_ZALACZNIK = 15_000_000;
fs.mkdirSync(path.join(DIST, "czat"), { recursive: true });
const czat = {};
for (const o of zespol) {
  const kat = path.join(CZAT, o.id);
  const wiadomosci = !fs.existsSync(kat) ? [] : fs.readdirSync(kat).filter((f) => f.endsWith(".json")).sort()
    .slice(-MAX_WIADOMOSCI).map((f) => czytajJson(path.join(kat, f), null)).filter((w) => w && w.id);
  for (const w of wiadomosci) for (const p of w.pliki || []) {
    if (p.url || !p.sciezka) continue;
    const zrodlo = path.resolve(ROOT, p.sciezka);
    if (!zrodlo.startsWith(ROOT + path.sep) || !fs.existsSync(zrodlo) || fs.statSync(zrodlo).size > MAX_ZALACZNIK) continue;
    const cel = path.join(DIST, "pliki", path.relative(ROOT, zrodlo));
    fs.mkdirSync(path.dirname(cel), { recursive: true });
    fs.copyFileSync(zrodlo, cel);
    p.url = "pliki/" + path.relative(ROOT, zrodlo).split(path.sep).map(encodeURIComponent).join("/");
  }
  fs.writeFileSync(path.join(DIST, "czat", o.id + ".json"), JSON.stringify({ zbudowano, wiadomosci }));
  const ost = wiadomosci.at(-1);
  czat[o.id] = { liczba: wiadomosci.length, ostatnia: ost ? { id: ost.id, czas: ost.czas, od: ost.od, typ: ost.typ, tekst: String(ost.tekst || "").slice(0, 160) } : null };
}

// ---------- sesje zespołu (link do subczatu każdego pracownika – do poprawek) ----------
const sesjeRej = czytajJson(path.join(ZESPOL, "sesje.json"), {}).sesje || {};
const sesje = Object.fromEntries(Object.entries(sesjeRej).map(([id, s]) => [id, {
  tytul: s.tytul || null, link: s.link || (s.sesja ? `https://claude.ai/code/${s.sesja}` : null), zadania: Object.keys(s.zadania || {}),
}]));

// ---------- biuro akceptacji: marketing/akceptacja/*.json → akceptacja.json (+ obrazy/filmy w pliki/) ----------
const AKC = path.join(ROOT, "marketing", "akceptacja");
const posty = !fs.existsSync(AKC) ? [] : fs.readdirSync(AKC).filter((f) => f.endsWith(".json")).sort()
  .map((f) => czytajJson(path.join(AKC, f), null)).filter((p) => p && p.id);
for (const p of posty) {
  for (const klucz of ["obrazy", "wideo"]) {
    p[klucz] = (p[klucz] || []).map((rel) => {
      const zrodlo = path.resolve(ROOT, rel);
      if (!zrodlo.startsWith(ROOT + path.sep) || !fs.existsSync(zrodlo)) return null;
      const cel = path.join(DIST, "pliki", path.relative(ROOT, zrodlo));
      fs.mkdirSync(path.dirname(cel), { recursive: true });
      fs.copyFileSync(zrodlo, cel);
      return "pliki/" + path.relative(ROOT, zrodlo).split(path.sep).map(encodeURIComponent).join("/");
    }).filter(Boolean);
  }
}
fs.writeFileSync(path.join(DIST, "akceptacja.json"), JSON.stringify({ zbudowano, posty }));
const akceptacja = { czeka: posty.filter((p) => p.stan === "czeka").length, razem: posty.length };

// ---------- biblioteka prawdziwych zdjęć: marketing/biblioteka-zdjec/indeks.json → zdjecia.json ----------
const BIBZ = path.join(ROOT, "marketing", "biblioteka-zdjec");
const indeksZ = czytajJson(path.join(BIBZ, "indeks.json"), { zdjecia: {} }).zdjecia || {};
const zdjecia = [];
for (const [rel, z] of Object.entries(indeksZ)) {
  const zrodlo = path.resolve(ROOT, rel);
  if (!zrodlo.startsWith(ROOT + path.sep) || !fs.existsSync(zrodlo)) continue;
  const cel = path.join(DIST, "pliki", rel);
  fs.mkdirSync(path.dirname(cel), { recursive: true });
  fs.copyFileSync(zrodlo, cel);
  zdjecia.push({ url: "pliki/" + rel.split("/").map(encodeURIComponent).join("/"), nazwa: path.basename(rel), sekcja: z.sekcja,
    opis: z.opis || "", tagi: z.tagi || [], produkt: z.produkt || "", dodano: z.dodano || "", uzycia: (z.uzycia || []).length });
}
zdjecia.sort((a, b) => (b.dodano || "").localeCompare(a.dodano || ""));
fs.writeFileSync(path.join(DIST, "zdjecia.json"), JSON.stringify({ zbudowano, zdjecia }));

const dane = {
  zbudowano,
  zdjecia: { razem: zdjecia.length },
  akceptacja,
  wersja: (process.env.VERCEL_GIT_COMMIT_SHA || "").slice(0, 7),
  zespol,
  zapisy,
  czat,
  sesje,
  czat_zadanie: sesjeRej.klaudiusz?.zadania?.czat || null,
  czat_prompt: (() => {
    try {
      const t = fs.readFileSync(path.join(ZESPOL, "zadania", "klaudiusz-czat.md"), "utf8");
      const m = t.match(/<!-- PROMPT-START -->\s*```text\n([\s\S]*?)\n```\s*<!-- PROMPT-END -->/);
      return m ? m[1] : null;
    } catch { return null; }
  })(),
};
fs.writeFileSync(path.join(DIST, "dane.json"), JSON.stringify(dane));
console.log(`Biuro zbudowane: ${zespol.length} osób, ${zespol.reduce((s, z) => s + z.wyniki.length, 0)} plików wyników, ${Object.values(czat).reduce((s, c) => s + c.liczba, 0)} wiadomości czatu -> ${path.relative(ROOT, DIST)}`);
