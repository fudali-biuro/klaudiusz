---
nazwa: "Post pod klucz → akceptacja szefa → Buffer"
kiedy: "kazda"
kolejnosc: 20
---
# Gotowy post pod klucz → akceptacja szefa → publikacja przez Buffer

Masz podpięty **Buffer** (konektor `mcp__Buffer__*`), organizacja „My organization” `6aeb3d2cc85b7740a1571069`, strefa Europe/Warsaw.
Kanały: Pinterest `FudaliNowoczesneStolarstwo` (`6aeb3db8e29c69a1715d6f02`), TikTok `nowoczesne_stolarstwo` (`6aeb3da5e29c69a1715d6de6`).
Instagram jeszcze niepodpięty w Bufferze – sprawdź `list_channels`; jeśli dalej go nie ma, przygotuj wersję IG w pliku i dopisz w prośbie, że trzeba go podpiąć.
Plan darmowy: max 10 zaplanowanych postów – pilnuj limitu.

**Która zmiana?** Na porannej: punkty 1–6 (odpowiedzi szefa + nowy post). Na zmianie w ciągu dnia (np. południe): przede wszystkim
punkt 2 – reaguj na odpowiedzi szefa (publikacja po „tak”, poprawki), przejrzyj nowe „💡 TAK” Mietka; nowy post przygotuj tylko,
jeśli dziś jeszcze żadnego nie było. Brak odpowiedzi i nic nowego → status i koniec zmiany.

1. `python3 scripts/status.py marketing pracuje "Post pod klucz do akceptacji"`.
2. Najpierw sprawdź czat (`python3 scripts/czat.py pokaz marketing`): czy szef odpowiedział na wcześniejsze propozycje.
   - **„tak / zielone światło”** → dopiero wtedy publikuj/zaplanuj w Buffer (`edit_post` szkicu albo `create_post`, `mode: addToQueue`
     lub `customScheduled` na godzinę wskazaną przez szefa), potem `status.py marketing ... --zalatwione` i krótka odpowiedź w czacie.
   - **poprawki** → popraw szkic, wyślij jeszcze raz do akceptacji.
   - brak odpowiedzi → nic nie publikuj, najwyżej przypomnij raz w czacie.
3. Przygotuj **kompletny post pod klucz** (wg karty, `marketing/produkty.md`, kalendarza i trendów Bartka): grafika (od Zosi, publiczny link – patrz „🔒 Linki do zdjęć” niżej),
   tekst PL na Instagram, tekst EN + tytuł + tablica + link (Etsy) na Pinterest, hashtagi, proponowany dzień i godzina.
   Zapisz w `marketing/posty/RRRR-MM-DD-<temat>.md`.
4. W Buffer wrzuć go **tylko jako szkic** (`create_post` z `saveToDraft: true`). Grafiki z AI → `isAiGenerated` tam, gdzie się da.
5. Zapytaj szefa: `python3 scripts/status.py marketing czeka "akceptacja posta" --prosba "Szefie, gotowy post: <temat>, <kanały>, <termin>. Publikujemy czy coś zmienić?"`
   (+ `scripts/czat.py napisz marketing "…" --plik <grafika>`).
6. Zapis na main.

🔒 **ŚWIĘTA ZASADA:** bez wyraźnej zgody szefa w czacie NIC nie publikujesz ani nie planujesz do publikacji. Tylko szkice.


## 🔒 Linki do zdjęć/filmów dla Buffera (od 26.11.2026 – archiwum będzie prywatne)
Archiwum przestaje być publiczne (polecenie Pablo), więc **nie używaj linków raw.githubusercontent.com** – Buffer ich nie pobierze.
Plik wgraj do schowka biura (Vercel Blob) i w Bufferze podaj zwrócony link:
1. Konektor Vercel: `update_project_protection_bypass` (projekt `biuro-fudali`, team `team_4EPn15A90m2RP26RoJNuWg1e`, `generate`) → jednorazowy klucz.
2. `curl -X POST "https://biuro-fudali.vercel.app/api/plik?do=marketing&nazwa=<nazwa>" -H "x-biuro: 1" -H "x-vercel-protection-bypass: <klucz>" -H "content-type: image/jpeg" --data-binary @<plik>` → `url` (max 4 MB).
3. Po wgraniu odwołaj klucz (`revoke`, `regenerate: false`). Klucza nigdy nie zapisuj w plikach ani w czacie.
Mapa przeniesionych 26.11 plików (Buffer): `marketing/buffer-linki-blob.tsv`.
