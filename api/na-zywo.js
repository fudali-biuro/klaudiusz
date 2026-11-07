// /api/na-zywo – świeże dane biura prosto z archiwum (bez czekania na przebudowę strony).
// Powód: strona na Vercel ma limit ok. 100 przebudów na dobę, a zespół zapisuje setki zmian – dane ze strony statycznej się starzeją.
//   GET ?co=akceptacja        → { zbudowano, posty:[…] }   (marketing/akceptacja/*.json)
//   GET ?co=czat&id=<osoba>   → { zbudowano, wiadomosci:[…] } (zespol/czat/<osoba>/*.json, ostatnie 300)
// Obrazy/pliki wskazują na kopie w archiwum (raw.githubusercontent.com). Gdy archiwum nie odpowiada – 502, strona bierze dane statyczne.
const ZESPOL = ["klaudiusz", "konkurencja", "marketing", "pozycjonowanie", "grafika", "slowa-kluczowe", "sprzedaz", "rynki-zagraniczne"];

const REPO = "fudali-biuro/klaudiusz", GALAZ = "main";
const RAW = `https://raw.githubusercontent.com/${REPO}/${GALAZ}/`;
const naRaw = (rel) => RAW + String(rel).replace(/^\/+/, "").split("/").map(encodeURIComponent).join("/");
const pamiec = new Map(); // prosta pamięć w ciepłej funkcji: klucz → { czas, dane }

async function katalog(sciezka) {
  const h = { accept: "application/vnd.github+json", "user-agent": "biuro-fudali" };
  if (process.env.GITHUB_TOKEN) h.authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  const r = await fetch(`https://api.github.com/repos/${REPO}/contents/${sciezka}?ref=${GALAZ}`, { headers: h, cache: "no-store" });
  if (r.status === 404) return [];
  if (!r.ok) throw new Error(`archiwum ${r.status}`);
  return (await r.json()).filter((f) => f.type === "file" && f.name.endsWith(".json"))
    .map((f) => ({ nazwa: f.name, sha: f.sha, url: naRaw(f.path) }));
}
const plikiJson = (pliki) => Promise.all(pliki.map(async (f) => {
  try { const r = await fetch(`${f.url}?sha=${f.sha}`, { cache: "no-store" }); return r.ok ? await r.json() : null; } catch { return null; }
}));

async function akceptacja() {
  const pliki = (await katalog("marketing/akceptacja")).sort((a, b) => a.nazwa.localeCompare(b.nazwa));
  const posty = (await plikiJson(pliki)).filter((p) => p && p.id);
  for (const p of posty) for (const k of ["obrazy", "wideo"]) p[k] = (p[k] || []).map(naRaw);
  return { posty };
}

async function czat(id) {
  const pliki = (await katalog(`zespol/czat/${id}`)).sort((a, b) => a.nazwa.localeCompare(b.nazwa)).slice(-300);
  const wiadomosci = (await plikiJson(pliki)).filter((w) => w && w.id);
  for (const w of wiadomosci) for (const p of w.pliki || []) if (!p.url && p.sciezka) p.url = naRaw(p.sciezka);
  return { wiadomosci };
}

export async function GET(request) {
  const u = new URL(request.url);
  const co = u.searchParams.get("co"), id = u.searchParams.get("id") || "";
  let klucz, fn;
  if (co === "akceptacja") { klucz = co; fn = akceptacja; }
  else if (co === "czat" && ZESPOL.includes(id)) { klucz = `czat/${id}`; fn = () => czat(id); }
  else return Response.json({ blad: "Nieznane dane" }, { status: 400 });
  const teraz = Date.now(), zapas = pamiec.get(klucz);
  try {
    const dane = zapas && teraz - zapas.czas < 45_000 ? zapas.dane : { zbudowano: new Date().toISOString(), ...(await fn()) };
    pamiec.set(klucz, { czas: zapas && dane === zapas.dane ? zapas.czas : teraz, dane });
    return Response.json(dane, { headers: { "cache-control": "no-store", "vercel-cdn-cache-control": "max-age=60, stale-while-revalidate=600" } });
  } catch (e) {
    if (zapas) return Response.json(zapas.dane, { headers: { "cache-control": "no-store" } });
    return Response.json({ blad: e.message }, { status: 502, headers: { "cache-control": "no-store" } });
  }
}
