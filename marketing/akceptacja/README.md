# ✅ Biuro akceptacji – biblioteka postów do zatwierdzenia (polecenie Pablo, 06.11.2026)

**Strona:** https://biuro-fudali.vercel.app/akceptacja.html (w biurze przycisk „✅ Akceptacja postów”).
**Zasada:** KAŻDY gotowy post (IG, FB, Pinterest, TikTok, relacje) trafia tutaj – nie do czatu, nie jako prośba w statusie.
Pablo przegląda bibliotekę w swoim tempie i przy każdym poście klika **✅ OK / ✏️ Popraw (+komentarz) / ❌ Odrzuć**,
potem „📨 Wyślij decyzje” → jedna wiadomość do Oli.

## Obieg
1. **Ola (+ Zosia)** przygotowuje post pod klucz: osobno na każdy kanał, finalna grafika, gotowy tekst, hashtagi →
   `python3 scripts/akceptacja.py dodaj --kanal instagram --data RRRR-MM-DD --godzina HH:MM --tytul "…" --produkt "…" --tekst-plik marketing/posty/….md --hashtagi "…" --obraz marketing/zdjecia/….jpg [--obraz …] [--wideo …]`
   (jeden plik = `marketing/akceptacja/<id>.json`; karuzela = kilka `--obraz` w kolejności slajdów).
2. **Klaudiusz** pilnuje: gdy czeka ≥ 3 posty → `python3 scripts/akceptacja.py przypomnij` (wiadomość do Pablo: „biblioteka pełna – przejrzyj”).
   Nikt inny nie zasypuje Pablo prośbami o akceptację.
3. **Pablo** klika decyzje i „Wyślij decyzje” → Ola dostaje listę (czat → jej skrzynka).
4. **Ola** wpisuje każdą decyzję: `python3 scripts/akceptacja.py ustaw <id> ok|popraw|odrzucone --komentarz "…" --kto pablo`, potem:
   - **OK** → szkic w Buffer (`saveToDraft: true`, właściwy kanał) → `ustaw <id> w-bufferze --kto marketing`;
     FB/IG, których nie ma w Bufferze → gotowy pakiet w `marketing/posty/` i stan `ok`.
   - **POPRAW** → poprawka wg komentarza (grafika → Zosia) → `python3 scripts/akceptacja.py popraw <id> [--tekst-plik …] [--obraz …]` – wraca do biblioteki jako nowa wersja.
   - **ODRZUĆ** → nic więcej (zostaje w historii, uczymy się z komentarza).
5. Publikacja dopiero, gdy Pablo sam zatwierdzi szkic w Bufferze (🔒 święta zasada).

`python3 scripts/akceptacja.py lista [--stan czeka]` – co jest w bibliotece.
