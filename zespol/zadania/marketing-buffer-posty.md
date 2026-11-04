---
nazwa: "📣 Ola – gotowy post pod klucz w Buffer (10:13)"
cron: "CRON_TZ=Europe/Warsaw 13 10 * * *"
---
# Gotowy post pod klucz → akceptacja szefa → publikacja przez Buffer

Masz podpięty **Buffer** (konektor `mcp__Buffer__*`), organizacja „My organization” `6aeb3d2cc85b7740a1571069`, strefa Europe/Warsaw.
Kanały: Pinterest `FudaliNowoczesneStolarstwo` (`6aeb3db8e29c69a1715d6f02`), TikTok `nowoczesne_stolarstwo` (`6aeb3da5e29c69a1715d6de6`).
Instagram jeszcze niepodpięty w Bufferze – sprawdź `list_channels`; jeśli dalej go nie ma, przygotuj wersję IG w pliku i dopisz w prośbie, że trzeba go podpiąć.
Plan darmowy: max 10 zaplanowanych postów – pilnuj limitu.

1. `python3 scripts/status.py marketing pracuje "Post pod klucz do akceptacji"`.
2. Najpierw sprawdź czat (`python3 scripts/czat.py pokaz marketing`): czy szef odpowiedział na wcześniejsze propozycje.
   - **„tak / zielone światło”** → dopiero wtedy publikuj/zaplanuj w Buffer (`edit_post` szkicu albo `create_post`, `mode: addToQueue`
     lub `customScheduled` na godzinę wskazaną przez szefa), potem `status.py marketing ... --zalatwione` i krótka odpowiedź w czacie.
   - **poprawki** → popraw szkic, wyślij jeszcze raz do akceptacji.
   - brak odpowiedzi → nic nie publikuj, najwyżej przypomnij raz w czacie.
3. Przygotuj **kompletny post pod klucz** (wg karty, `marketing/produkty.md`, kalendarza i trendów Bartka): grafika (od Zosi, publiczny link),
   tekst PL na Instagram, tekst EN + tytuł + tablica + link (Etsy) na Pinterest, hashtagi, proponowany dzień i godzina.
   Zapisz w `marketing/posty/RRRR-MM-DD-<temat>.md`.
4. W Buffer wrzuć go **tylko jako szkic** (`create_post` z `saveToDraft: true`). Grafiki z AI → `isAiGenerated` tam, gdzie się da.
5. Zapytaj szefa: `python3 scripts/status.py marketing czeka "akceptacja posta" --prosba "Szefie, gotowy post: <temat>, <kanały>, <termin>. Publikujemy czy coś zmienić?"`
   (+ `scripts/czat.py napisz marketing "…" --plik <grafika>`).
6. Zapis na main.

🔒 **ŚWIĘTA ZASADA:** bez wyraźnej zgody szefa w czacie NIC nie publikujesz ani nie planujesz do publikacji. Tylko szkice.
