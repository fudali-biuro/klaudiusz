// Wspólne funkcje serwera czatu biura (Vercel Functions). Pliki z „_” na początku nie są adresami API.
import { put, list, del } from "@vercel/blob";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

export const ZESPOL = ["klaudiusz", "konkurencja", "marketing", "pozycjonowanie", "grafika", "slowa-kluczowe", "sprzedaz", "rynki-zagraniczne"];
export const MAX_PLIK = 4_400_000; // limit ciała żądania funkcji Vercel to 4,5 MB
const FIRE = (zadanie) => `https://api.anthropic.com/v1/claude_code/routines/${zadanie}/fire`;
const PREFIKS_USTAWIEN = "ustawienia/polaczenie";

export function odpowiedz(dane, status = 200) {
  return Response.json(dane, { status, headers: { "cache-control": "no-store" } });
}

// Żądania tylko z naszej strony (nagłówek x-biuro wymusza sprawdzenie CORS przez przeglądarkę).
export function zNaszejStrony(request) {
  if (request.headers.get("x-biuro") !== "1") return false;
  const origin = request.headers.get("origin");
  if (!origin) return true;
  try { return new URL(origin).host === request.headers.get("host"); } catch { return false; }
}

// Rejestr sesji i zadań (zespol/sesje.json – dołączany do funkcji przez vercel.json → includeFiles)
export function sesje() {
  for (const p of [path.join(process.cwd(), "zespol", "sesje.json"), new URL("../zespol/sesje.json", import.meta.url)]) {
    try { return JSON.parse(fs.readFileSync(p, "utf8")).sesje || {}; } catch { /* następna ścieżka */ }
  }
  return {};
}

// ---------- ustawienia połączenia (token zadania „📨 Czat z biura”) – zaszyfrowane w magazynie Blob ----------
function klucz() {
  const sekret = process.env.BLOB_READ_WRITE_TOKEN || "";
  if (!sekret) throw new Error("Brak magazynu Blob (BLOB_READ_WRITE_TOKEN)");
  return crypto.createHash("sha256").update("biuro-fudali|czat|" + sekret).digest();
}
function szyfruj(obj) {
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv("aes-256-gcm", klucz(), iv);
  const dane = Buffer.concat([c.update(JSON.stringify(obj), "utf8"), c.final()]);
  return JSON.stringify({ v: 1, iv: iv.toString("base64"), tag: c.getAuthTag().toString("base64"), dane: dane.toString("base64") });
}
function odszyfruj(tekst) {
  const o = JSON.parse(tekst);
  const d = crypto.createDecipheriv("aes-256-gcm", klucz(), Buffer.from(o.iv, "base64"));
  d.setAuthTag(Buffer.from(o.tag, "base64"));
  return JSON.parse(Buffer.concat([d.update(Buffer.from(o.dane, "base64")), d.final()]).toString("utf8"));
}

let pamiec = null, pamiecCzas = 0;
export async function ustawienia() {
  if (pamiec && Date.now() - pamiecCzas < 20_000) return pamiec;
  let wynik = { tokeny: {} };
  try {
    const { blobs } = await list({ prefix: PREFIKS_USTAWIEN });
    const najnowszy = blobs.sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt))[0];
    if (najnowszy) {
      const r = await fetch(najnowszy.url, { cache: "no-store" });
      if (r.ok) wynik = odszyfruj(await r.text());
    }
  } catch (e) { console.error("ustawienia:", e.message); }
  wynik.tokeny ||= {};
  pamiec = wynik; pamiecCzas = Date.now();
  return wynik;
}
export async function zapiszUstawienia(obj) {
  const nowy = await put(`${PREFIKS_USTAWIEN}.json`, szyfruj(obj), {
    access: "public", addRandomSuffix: true, contentType: "application/json", cacheControlMaxAge: 60,
  });
  const { blobs } = await list({ prefix: PREFIKS_USTAWIEN });
  const stare = blobs.filter((b) => b.url !== nowy.url).map((b) => b.url);
  if (stare.length) await del(stare);
  pamiec = obj; pamiecCzas = Date.now();
}

// Dokąd wysłać wiadomość: bezpośrednio do pracownika (jeśli ma własne zadanie czatu i token) albo przez Klaudiusza.
export function cel(doKogo, ust, s = sesje()) {
  const bezposrednio = s[doKogo]?.zadania?.czat && ust.tokeny?.[doKogo];
  if (bezposrednio) return { zadanie: s[doKogo].zadania.czat, token: ust.tokeny[doKogo], przez: doKogo };
  if (s.klaudiusz?.zadania?.czat && ust.tokeny?.klaudiusz) return { zadanie: s.klaudiusz.zadania.czat, token: ust.tokeny.klaudiusz, przez: "klaudiusz" };
  return null;
}

// Obudzenie sesji: POST /fire zadania z tekstem (trafia do sesji jako blok routine-fire-payload).
export async function obudz(zadanie, token, tekst) {
  const r = await fetch(FIRE(zadanie), {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "anthropic-beta": "experimental-cc-routine-2026-04-01",
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({ text: tekst }),
  });
  const surowe = await r.text();
  let dane = null;
  try { dane = JSON.parse(surowe); } catch { /* nie-JSON */ }
  return { ok: r.ok, status: r.status, dane, blad: r.ok ? null : (dane?.error?.message || surowe.slice(0, 300)) };
}

export function czasPL(d = new Date()) {
  // ISO z przesunięciem Europe/Warsaw, np. 2026-11-04T15:12:05+01:00
  const p = Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Warsaw", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23",
  }).formatToParts(d).map((x) => [x.type, x.value]));
  const lokalnie = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second);
  const off = Math.round((lokalnie - Math.floor(d.getTime() / 1000) * 1000) / 60000);
  const zn = off >= 0 ? "+" : "-", a = Math.abs(off);
  return `${p.year}-${p.month}-${p.day}T${p.hour}:${p.minute}:${p.second}${zn}${String(Math.floor(a / 60)).padStart(2, "0")}:${String(a % 60).padStart(2, "0")}`;
}

export function noweId() {
  const t = czasPL().slice(0, 19).replace(/\D/g, "");
  return `m_${t}_${crypto.randomBytes(3).toString("hex")}`;
}
