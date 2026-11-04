// POST /api/plik?nazwa=…&do=… – załącznik z czatu (obrazek, nagranie, plik) → Vercel Blob → link dla pracownika.
import { put } from "@vercel/blob";
import { ZESPOL, MAX_PLIK, odpowiedz, zNaszejStrony, czasPL } from "./_wspolne.js";

export async function POST(request) {
  if (!zNaszejStrony(request)) return odpowiedz({ blad: "Niedozwolone źródło żądania" }, 403);
  const u = new URL(request.url);
  const doKogo = ZESPOL.includes(u.searchParams.get("do")) ? u.searchParams.get("do") : "klaudiusz";
  const nazwa = (u.searchParams.get("nazwa") || "plik").normalize("NFKD").replace(/[̀-ͯ]/g, "")
    .replace(/[^\w.\-]+/g, "-").replace(/^[-.]+|[-.]+$/g, "").slice(-80) || "plik";
  const typ = (request.headers.get("content-type") || "application/octet-stream").split(";")[0].slice(0, 80);
  const dlugosc = Number(request.headers.get("content-length") || 0);
  if (dlugosc > MAX_PLIK) return odpowiedz({ blad: "Plik za duży (max 4 MB)" }, 413);
  const dane = Buffer.from(await request.arrayBuffer());
  if (!dane.length) return odpowiedz({ blad: "Pusty plik" }, 400);
  if (dane.length > MAX_PLIK) return odpowiedz({ blad: "Plik za duży (max 4 MB)" }, 413);
  const blob = await put(`czat/${doKogo}/${czasPL().slice(0, 10)}/${nazwa}`, dane, {
    access: "public", addRandomSuffix: true, contentType: typ,
  });
  return odpowiedz({ url: blob.url, nazwa, typ, rozmiar: dane.length });
}
