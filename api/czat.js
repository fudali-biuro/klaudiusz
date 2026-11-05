// POST /api/czat – Pablo wysyła wiadomość z okna czatu w biurze → budzi sesję (zadanie „📨 Czat z biura”).
import { ZESPOL, odpowiedz, zNaszejStrony, ustawienia, cel, obudz, czasPL, noweId, przesylka } from "./_wspolne.js";

const MAX_TEKST = 15_000;

export async function POST(request) {
  if (!zNaszejStrony(request)) return odpowiedz({ blad: "Niedozwolone źródło żądania" }, 403);
  let w;
  try { w = await request.json(); } catch { return odpowiedz({ blad: "Niepoprawne dane" }, 400); }
  const doKogo = String(w.do || "");
  if (!ZESPOL.includes(doKogo)) return odpowiedz({ blad: "Nieznany adresat" }, 400);
  const tekst = String(w.tekst || "").slice(0, MAX_TEKST).trim();
  const zalaczniki = (Array.isArray(w.zalaczniki) ? w.zalaczniki : []).slice(0, 12)
    .filter((z) => /^https:\/\/[\w.-]+\.blob\.vercel-storage\.com\//.test(String(z?.url || "")))
    .map((z) => ({ url: String(z.url), nazwa: String(z.nazwa || "plik").slice(0, 120), typ: String(z.typ || "").slice(0, 80), rozmiar: Number(z.rozmiar) || null }));
  const typ = w.typ === "test" ? "test" : "wiadomosc";
  if (!tekst && !zalaczniki.length && typ !== "test") return odpowiedz({ blad: "Pusta wiadomość" }, 400);

  const ust = await ustawienia();
  const c = cel(doKogo, ust);
  if (!c) return odpowiedz({ blad: "brak_polaczenia", opis: "Czat nie jest jeszcze połączony z Klaudiuszem." }, 409);

  const wiadomosc = {
    id: /^m_[\w]{6,40}$/.test(String(w.id || "")) ? String(w.id) : noweId(),
    czas: czasPL(), od: "pablo", do: doKogo, typ, tekst, zalaczniki,
    ...(w.re ? { re: String(w.re).slice(0, 80) } : {}),
    ...(w.re_tekst ? { re_tekst: String(w.re_tekst).slice(0, 500) } : {}),
  };
  const paczka = przesylka(wiadomosc);
  if (!paczka.skrzynka) return odpowiedz({ blad: "brak_sesji", opis: "Ten pracownik nie ma jeszcze swojej skrzynki – napisz do Klaudiusza." }, 409);
  const wynik = await obudz(c.zadanie, c.token, JSON.stringify(paczka));
  if (!wynik.ok) {
    console.error("fire:", wynik.status, wynik.blad);
    const opis = wynik.status === 401 || wynik.status === 403
      ? "Połączenie z Klaudiuszem wygasło – trzeba wkleić nowy token (instrukcja w czacie)."
      : `Nie udało się obudzić Klaudiusza (kod ${wynik.status}). Spróbuj za chwilę.`;
    return odpowiedz({ blad: wynik.status === 401 || wynik.status === 403 ? "brak_polaczenia" : "blad_wysylki", opis }, 502);
  }
  return odpowiedz({ ok: true, id: wiadomosc.id, czas: wiadomosc.czas, przez: c.przez, sesja: wynik.dane?.claude_code_session_id || null });
}
