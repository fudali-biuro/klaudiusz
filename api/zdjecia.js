// /api/zdjecia – zgłoszenia nowych zdjęć do biblioteki (działa bez połączenia czatu).
// POST { sekcja, opis, pliki:[{url,nazwa,typ,rozmiar}] } → zapis zgłoszenia w Vercel Blob
// GET  → { zgloszenia:[{id, czas, sekcja, opis, pliki}] } – Klaudiusz/Zosia pobierają je do archiwum (scripts/zdjecia.py pobierz)
import { put, list } from "@vercel/blob";
import { odpowiedz, zNaszejStrony, czasPL, noweId, ustawienia, cel, obudz, przesylka } from "./_wspolne.js";

const PREFIKS = "biblioteka/zgloszenia/";
const SEKCJE = ["tla", "produkty", "gotowe"];

const INDEKS = "biblioteka/zgloszenia-indeks.json";

async function zgloszenia() {
  const { blobs } = await list({ prefix: PREFIKS, limit: 1000 });
  return (await Promise.all(blobs.map(async (b) => {
    try { const r = await fetch(`${b.url}?v=${encodeURIComponent(b.uploadedAt)}`, { cache: "no-store" }); return r.ok ? await r.json() : null; } catch { return null; }
  }))).filter(Boolean).sort((a, b) => a.czas.localeCompare(b.czas));
}

export async function GET() {
  try {
    const { blobs } = await list({ prefix: INDEKS });
    return odpowiedz({ zgloszenia: await zgloszenia(), indeks_url: blobs[0]?.url || null });
  } catch (e) { return odpowiedz({ blad: e.message, zgloszenia: [] }, 500); }
}

export async function POST(request) {
  if (!zNaszejStrony(request)) return odpowiedz({ blad: "Niedozwolone źródło żądania" }, 403);
  let w;
  try { w = await request.json(); } catch { return odpowiedz({ blad: "Niepoprawne dane" }, 400); }
  const sekcja = SEKCJE.includes(w.sekcja) ? w.sekcja : null;
  if (!sekcja) return odpowiedz({ blad: "Zła sekcja" }, 400);
  const pliki = (Array.isArray(w.pliki) ? w.pliki : []).slice(0, 60)
    .filter((z) => /^https:\/\/[\w.-]+\.blob\.vercel-storage\.com\//.test(String(z?.url || "")))
    .map((z) => ({ url: String(z.url), nazwa: String(z.nazwa || "zdjecie.jpg").slice(0, 120), typ: String(z.typ || "").slice(0, 80), rozmiar: Number(z.rozmiar) || null }));
  if (!pliki.length) return odpowiedz({ blad: "Brak plików" }, 400);
  const z = { id: noweId().replace(/^m_/, "z_"), czas: czasPL(), sekcja, opis: String(w.opis || "").slice(0, 4000).trim(), pliki };
  await put(`${PREFIKS}${z.id}.json`, JSON.stringify(z), { access: "public", addRandomSuffix: false, contentType: "application/json" });
  // stały, publiczny spis wszystkich zgłoszeń – zespół pobiera go bez logowania (scripts/zdjecia.py pobierz)
  let indeksUrl = null;
  try {
    const wszystkie = await zgloszenia();
    indeksUrl = (await put(INDEKS, JSON.stringify({ zgloszenia: wszystkie }), {
      access: "public", addRandomSuffix: false, allowOverwrite: true, contentType: "application/json", cacheControlMaxAge: 60 })).url;
  } catch (e) { console.error("indeks:", e.message); }

  // jeśli czat jest połączony – od razu obudź Zosię (nieobowiązkowe; bez tego zdjęcia odbierze Klaudiusz)
  let powiadomiono = false;
  try {
    const c = cel("grafika", await ustawienia());
    if (c) {
      const tekst = `📸 NOWE ZDJĘCIA DO BIBLIOTEKI – sekcja ${sekcja}, ${pliki.length} szt.${z.opis ? `, opis: ${z.opis}` : ""}. ` +
        `Pobierz: python3 scripts/zdjecia.py pobierz (zgłoszenie ${z.id}), potem opisz każde zdjęcie.`;
      const wiad = { id: noweId(), czas: czasPL(), od: "pablo", do: "grafika", typ: "wiadomosc", tekst, zalaczniki: [] };
      powiadomiono = (await obudz(c.zadanie, c.token, JSON.stringify(przesylka(wiad)))).ok;
    }
  } catch { /* trudno – zgłoszenie i tak jest zapisane */ }
  return odpowiedz({ ok: true, id: z.id, powiadomiono, indeks_url: indeksUrl });
}
