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

const zespol = [];
const pliki = fs.readdirSync(ZESPOL).filter((f) => f.endsWith(".md") && f !== "README.md").map((f) => f.slice(0, -3));
pliki.sort((a, b) => (KOLEJNOSC.indexOf(a) + 1 || 99) - (KOLEJNOSC.indexOf(b) + 1 || 99));
for (const id of pliki) {
  const [meta, tresc] = naglowek(fs.readFileSync(path.join(ZESPOL, id + ".md"), "utf8"));
  const status = czytajJson(path.join(ZESPOL, "status", id + ".json"), { stan: "wolne", zadanie: "", prosby: [], dziennik: [] });
  const wyniki = [];
  for (const w of (meta.wyniki || "").split(";")) for (const rel of znajdz(w)) wyniki.push(kopiuj(rel));
  zespol.push({ id, ...meta, karta: tresc, status });
  zespol.at(-1).wyniki = wyniki;
}

let zapisy = [];
try {
  zapisy = execSync("git log -25 --pretty=format:%cI%x09%s", { cwd: ROOT, encoding: "utf8" })
    .split("\n").filter(Boolean).map((l) => { const [czas, tekst] = l.split("\t"); return { czas, tekst }; });
} catch { /* brak historii w środowisku budowania – trudno */ }

const dane = {
  zbudowano: new Date().toISOString(),
  wersja: (process.env.VERCEL_GIT_COMMIT_SHA || "").slice(0, 7),
  zespol,
  zapisy,
};
fs.writeFileSync(path.join(DIST, "dane.json"), JSON.stringify(dane));
console.log(`Biuro zbudowane: ${zespol.length} osób, ${zespol.reduce((s, z) => s + z.wyniki.length, 0)} plików wyników -> ${path.relative(ROOT, DIST)}`);
