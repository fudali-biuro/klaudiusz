// GET  /api/ustawienia – czy czat jest połączony z Klaudiuszem
// POST /api/ustawienia {token} – wklejony token zadania „📨 Czat z biura” → test (budzi Klaudiusza) → zapis zaszyfrowany
// DELETE /api/ustawienia – rozłącz
import { odpowiedz, zNaszejStrony, sesje, ustawienia, zapiszUstawienia, obudz, czasPL, noweId, przesylka } from "./_wspolne.js";

function zadanieCzatu() { return sesje().klaudiusz?.zadania?.czat || null; }

export async function GET() {
  const ust = await ustawienia();
  const zadanie = zadanieCzatu();
  return odpowiedz({
    polaczony: Boolean(zadanie && ust.tokeny?.klaudiusz),
    zadanie,
    link: zadanie ? `https://claude.ai/code/routines/${zadanie}` : "https://claude.ai/code/routines",
    polaczono: ust.zapisano || null,
    magazyn: Boolean(process.env.BLOB_READ_WRITE_TOKEN),
  });
}

export async function POST(request) {
  if (!zNaszejStrony(request)) return odpowiedz({ blad: "Niedozwolone źródło żądania" }, 403);
  let b;
  try { b = await request.json(); } catch { return odpowiedz({ blad: "Niepoprawne dane" }, 400); }
  const token = String(b.token || "").trim().replace(/^Bearer\s+/i, "");
  if (!/^sk-ant-[\w-]{20,}$/.test(token)) return odpowiedz({ blad: "To nie wygląda na token (powinien zaczynać się od „sk-ant-”)." }, 400);
  const zadanie = zadanieCzatu();
  if (!zadanie) return odpowiedz({ blad: "Klaudiusz nie ma jeszcze zadania „📨 Czat z biura”." }, 409);
  const test = { id: noweId(), czas: czasPL(), od: "pablo", do: "klaudiusz", typ: "test",
    tekst: "TEST POŁĄCZENIA – czat w biurze został właśnie połączony. Odpisz Pablo jednym zdaniem, że wszystko działa.", zalaczniki: [] };
  const wynik = await obudz(zadanie, token, JSON.stringify(przesylka(test)));
  if (!wynik.ok) {
    return odpowiedz({ blad: wynik.status === 401 || wynik.status === 403
      ? "Ten token nie pasuje do zadania „📨 Czat z biura – listonosz” (albo został już zmieniony). Wygeneruj nowy i wklej jeszcze raz."
      : `Nie udało się sprawdzić tokenu (kod ${wynik.status}). Spróbuj za chwilę.` }, 400);
  }
  const ust = await ustawienia();
  await zapiszUstawienia({ ...ust, tokeny: { ...(ust.tokeny || {}), klaudiusz: token }, zapisano: czasPL() });
  return odpowiedz({ ok: true, id: test.id });
}

export async function DELETE(request) {
  if (!zNaszejStrony(request)) return odpowiedz({ blad: "Niedozwolone źródło żądania" }, 403);
  const ust = await ustawienia();
  await zapiszUstawienia({ ...ust, tokeny: {}, zapisano: czasPL() });
  return odpowiedz({ ok: true });
}
