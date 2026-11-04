# Procedura: godzinny monitoring konkurencji (Instagram + TikTok) i słów kluczowych

Kontekst firmy i zasady zapisu: `AGENTS.md`. Konkurenci: **wyłącznie** `konkurencja/firmy/*.md` (źródło prawdy).
Język: polski, konkretnie, bez lania wody. Nie wymyślaj faktów – każdy post z linkiem.

## 1. Zbierz dane
```bash
bash scripts/godzinny.sh
```
Powstają: `monitoring/stan/nowe-posty.json`, `monitoring/stan/wideo-analizy/*.json`,
`monitoring/stan/slowa-metryki.json`, dopisek w `slowa-kluczowe/historia.csv`.
Status `brak_tokenu` / `brak_klucza_openrouter` = brak klucza (APIFY_API_KEY / OPENROUTER_API_KEY) – zanotuj to raz w podsumowaniu, to nie błąd.
Status `pierwsze_uruchomienie` = zapamiętano stan bazowy, analizy postów jeszcze nie ma.
Test / pełny pierwszy raport: `ANALIZUJ_PIERWSZE=2 bash scripts/godzinny.sh` – analizuje 2 najnowsze posty z każdego konta
(gdy stan bazowy już istnieje, najpierw usuń `monitoring/stan/widziane.json`).

## 2. Analiza nowych postów (tylko jeśli są)
Dla każdego nowego posta:
- **Wideo – dwa niezależne spojrzenia:**
  1. *Twoje (Claude):* obejrzyj narzędziem Read arkusz klatek `monitoring/media/<id>/arkusz.jpg`
     (klatki z timestampami), a przy ciekawych momentach pojedyncze klatki z `.../klatki/`. Oceń: hook w 1–3 s,
     kadrowanie, światło, tekst na ekranie, tempo, jak pokazano produkt.
  2. *Gemini 4 (obraz + dźwięk):* `monitoring/stan/wideo-analizy/<id>.json` → pole `gemini.analiza`
     (sceny z timestampami, transkrypcja, muzyka, hook, pomysł dla FUDALI).
  Porównaj oba – jeśli się różnią, napisz to (Ty nie słyszysz dźwięku; Gemini może się mylić w szczegółach obrazu).
- **Zdjęcia/karuzele:** oceń opis, hashtagi, zaangażowanie względem typowych wyników tego konta (`posty-30dni.json`).
- **Bogateco / Płoty Ogrodowe (priorytet A+, główny rywal)** – ich posty analizuj zawsze najdokładniej i dodaj punkt
  „jak ich przebić” (co zrobić lepiej/inaczej niż oni).
- **Werdykt:** „Czy FUDALI może zrobić coś podobnego?” – TAK / CZĘŚCIOWO / NIE + dlaczego.
  Przy TAK: konkretny pomysł (produkt FUDALI, hook, 3–6 ujęć, audio, tekst na ekranie, CTA, ile pracy).

## 3. Zapisz wyniki
- `monitoring/social/RRRR-MM-DD.md` – **dopisz** sekcję `## HH:00` (data i godzina Europe/Warsaw):
  tabela `Firma | Platforma | Post (link) | Co to jest | Zaangażowanie | Werdykt`, potem przy TAK pomysły.
  Brak nowości → jedna linia „HH:00 – brak nowych postów (sprawdzono N kont)”.
- Najciekawsze posty (werdykt TAK lub wyraźnie ponadprzeciętne zaangażowanie) dopisz na górze sekcji
  „Dziennik obserwacji” w pliku firmy `konkurencja/firmy/<slug>.md` (data, link, 1–2 zdania).
- Brakujące konta IG/TikTok konkurentów: jeśli przy okazji znajdziesz pewny link (np. na ich stronie www),
  uzupełnij front matter w pliku firmy. Nowego konkurenta dodaj jako nowy plik w `konkurencja/firmy/`.

## 4. Słowa kluczowe – podsumowanie godzinowe
Na podstawie `monitoring/stan/slowa-metryki.json` (ocena 0–100, popyt z podpowiedzi Google, wzmianki
konkurencji 24 h/7 d, zaangażowanie, zmiana względem poprzedniego pomiaru) i `slowa-kluczowe/historia.csv`
**dopisz** sekcję `## HH:00` w `slowa-kluczowe/podsumowania/RRRR-MM-DD.md`:
- **Ważne teraz (TOP 5)** – fraza, ocena, dlaczego (który sygnał), co z tym zrobić (post / opis produktu / strona).
- **Rośnie / spada** – frazy ze zmianą oceny lub nowymi wzmiankami u konkurencji.
- **Nieistotne** – frazy z niską oceną; zaproponuj usunięcie, jeśli są niskie od kilku dni.
- **Kandydaci** – max 3 najlepsze nowe frazy z `slowa-kluczowe/kandydaci.md` pasujące do oferty FUDALI.
Jeśli nic się nie zmieniło od poprzedniej godziny, napisz krótko „bez zmian” + TOP 3 – nie powtarzaj całej analizy.
Raz dziennie (pierwszy przebieg po 20:00) dodaj sekcję `## Podsumowanie dnia`.

## 5. Zapis (archiwum = gałąź `main`, zasady w `AGENTS.md`)
Zacommituj zmiany (bez `monitoring/media/`) i wypchnij na `main`: `git pull --rebase origin main`, potem
`git push origin HEAD:main`. Przy konflikcie zachowaj zmiany obu stron (w `historia.csv` – wszystkie wiersze;
w `monitoring/stan/*.json` – wersję bieżącą). Nigdy `push --force`.
**Statusy kluczy:** jeśli w `AGENTS.md` Apify/OpenRouter mają status 🔑, a w tym przebiegu zadziałały (scraping zwrócił
posty / Gemini zwrócił analizę) – zmień na ✅; jeśli zwróciły błąd autoryzacji – ❌ z krótkim opisem.

## 5a. Status w biurze (Mietek i Kuba)
`godzinny.sh` ustawia „pracuje”. Na koniec (po zapisie wyników) ustaw:
```bash
python3 scripts/status.py konkurencja gotowe "HH:00 – N nowych postów (M z werdyktem TAK)"   # albo "brak nowych postów"
python3 scripts/status.py slowa-kluczowe gotowe "HH:00 – TOP: <fraza> (<ocena>)"
```
Brak klucza / błąd API → `... blad "krótko co"`. Statusy zapisz razem z wynikami (przy konflikcie – wersja bieżąca).

## 6. Powiadomienie
Tylko gdy jest coś wartego uwagi (werdykt TAK, wiral u konkurencji, mocny skok frazy):
`scripts/powiadom-telegram.sh "<max 3 punkty + link do pliku na GitHubie>"`. W pozostałych przypadkach nie wysyłaj.
