// /api/akceptacja – decyzje Pablo w bibliotece postów (biuro → ✅ Akceptacja).
// GET  → { decyzje: { <id>: {decyzja, komentarz, czas, wyslano} } }
// POST { id, decyzja: "ok"|"popraw"|"odrzucone"|"", komentarz }  → zapis decyzji (Vercel Blob)
// POST { wyslij: true }  → jedna wiadomość do Oli (czat → jej skrzynka) ze wszystkimi niewysłanymi decyzjami
import { put, list, del } from "@vercel/blob";
import { odpowiedz, zNaszejStrony, ustawienia, cel, obudz, czasPL, noweId, przesylka } from "./_wspolne.js";

const PREFIKS = "akceptacja/decyzje/";
const DECYZJE = ["ok", "popraw", "odrzucone"];
const NAZWY = { ok: "✅ OK", popraw: "✏️ POPRAW", odrzucone: "❌ ODRZUĆ" };

async function wszystkie() {
  const { blobs } = await list({ prefix: PREFIKS, limit: 1000 });
  const wynik = {};
  await Promise.all(blobs.map(async (b) => {
    try {
      const r = await fetch(`${b.url}?v=${encodeURIComponent(b.uploadedAt)}`, { cache: "no-store" });
      if (r.ok) { const d = await r.json(); if (d?.id) wynik[d.id] = d; }
    } catch { /* pomiń uszkodzony wpis */ }
  }));
  return wynik;
}

async function zapisz(d) {
  await put(`${PREFIKS}${d.id}.json`, JSON.stringify(d), {
    access: "public", addRandomSuffix: false, allowOverwrite: true, contentType: "application/json", cacheControlMaxAge: 60,
  });
}

export async function GET() {
  try { return odpowiedz({ decyzje: await wszystkie() }); }
  catch (e) { return odpowiedz({ blad: e.message, decyzje: {} }, 500); }
}

export async function POST(request) {
  if (!zNaszejStrony(request)) return odpowiedz({ blad: "Niedozwolone źródło żądania" }, 403);
  let w;
  try { w = await request.json(); } catch { return odpowiedz({ blad: "Niepoprawne dane" }, 400); }

  if (w.wyslij) {
    const wsz = await wszystkie();
    const doWyslania = Object.values(wsz).filter((d) => d.decyzja && !d.wyslano);
    if (!doWyslania.length) return odpowiedz({ ok: true, wyslano: 0 });
    const linie = doWyslania.sort((a, b) => a.id.localeCompare(b.id)).map((d) =>
      `• ${NAZWY[d.decyzja]} – ${d.id}${d.tytul ? ` („${d.tytul}”)` : ""}${d.komentarz ? `\n   komentarz Pablo: ${d.komentarz}` : ""}`);
    const tekst = `✅ DECYZJE PABLO z biblioteki akceptacji (${doWyslania.length}):\n${linie.join("\n")}\n\n` +
      `Co dalej (Ola + Zosia): wpisz każdą decyzję: python3 scripts/akceptacja.py ustaw <id> ok|popraw|odrzucone --komentarz "…" --kto pablo. ` +
      `OK → szkic w Buffer (saveToDraft) i stan w-bufferze. POPRAW → popraw wg komentarza (grafika → Zosia), potem akceptacja.py popraw <id> – wraca do biblioteki. ODRZUĆ → nic.`;
    const ust = await ustawienia();
    const c = cel("marketing", ust);
    if (!c) return odpowiedz({ blad: "brak_polaczenia", opis: "Czat nie jest połączony z zespołem." }, 409);
    const wiadomosc = { id: noweId(), czas: czasPL(), od: "pablo", do: "marketing", typ: "wiadomosc", tekst, zalaczniki: [] };
    const paczka = przesylka(wiadomosc);
    const r = await obudz(c.zadanie, c.token, JSON.stringify(paczka));
    if (!r.ok) return odpowiedz({ blad: "blad_wysylki", opis: `Nie udało się wysłać (kod ${r.status}). Spróbuj za chwilę.` }, 502);
    const czas = czasPL();
    await Promise.all(doWyslania.map((d) => zapisz({ ...d, wyslano: czas })));
    return odpowiedz({ ok: true, wyslano: doWyslania.length });
  }

  const id = String(w.id || "");
  if (!/^[\w.-]{6,80}$/.test(id)) return odpowiedz({ blad: "Złe id posta" }, 400);
  const decyzja = String(w.decyzja || "");
  if (decyzja && !DECYZJE.includes(decyzja)) return odpowiedz({ blad: "Zła decyzja" }, 400);
  if (!decyzja) {
    const { blobs } = await list({ prefix: `${PREFIKS}${id}.json` });
    if (blobs.length) await del(blobs.map((b) => b.url));
    return odpowiedz({ ok: true, usunieto: true });
  }
  const d = { id, decyzja, komentarz: String(w.komentarz || "").slice(0, 2000).trim(), tytul: String(w.tytul || "").slice(0, 200),
    wersja: Number(w.wersja) || 1, czas: czasPL(), wyslano: null };
  await zapisz(d);
  return odpowiedz({ ok: true, decyzja: d });
}
