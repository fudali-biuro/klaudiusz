# Procedura: codzienny raport konkurencji

Kontekst firmy: `README.md`. Język raportu: polski. Ton: konkretny, biznesowy, bez lania wody.

## Kroki
1. Wczytaj **wszystkie pliki `konkurencja/firmy/*.md`** (źródło prawdy o konkurentach) oraz 2–3 ostatnie raporty z `raporty/`.
2. Wczytaj wyniki godzinnego monitoringu z ostatnich 24 h:
   `monitoring/social/<wczoraj>.md`, `monitoring/social/<dziś>.md` oraz `slowa-kluczowe/podsumowania/<wczoraj>.md`.
   Najważniejsze posty i pomysły „możemy zrobić podobnie” przenieś do raportu (sekcja Marketing i social media).
3. Research (WebSearch/WebFetch), skup się na ostatnich 24–72 h i zmianach względem poprzednich raportów:
   - nowe produkty, promocje, zmiany cen (altany, domki, pergole, drewutnie, meble ogrodowe, drewno),
   - aktywność marketingowa (FB/Instagram/TikTok, kampanie, konkursy), opinie klientów,
   - nowi gracze na Podkarpaciu i w sprzedaży wysyłkowej w PL,
   - sygnały rynkowe: ceny drewna (Lasy Państwowe, tarcica), sezonowość, dotacje, przepisy.
4. Nie wymyślaj danych. Każdy fakt z linkiem do źródła. Jeśli czegoś nie da się sprawdzić – napisz to wprost.
5. Zapisz raport jako `raporty/RRRR-MM-DD-konkurencja.md` wg szablonu poniżej.
6. Nowego istotnego konkurenta dodaj jako nowy plik w `konkurencja/firmy/` (skopiuj szablon z istniejącego pliku),
   a istotne zmiany u istniejących dopisz w ich „Dzienniku obserwacji”. Potem `python3 scripts/indeks_konkurencji.py`.

## Szablon raportu
```
# Raport konkurencji – RRRR-MM-DD

## TL;DR (max 5 punktów)
## Co się zmieniło u konkurencji
(tabela: Firma | Zmiana | Źródło)
## Ceny – obserwacje
## Marketing i social media (w tym: najlepsze posty z monitoringu godzinnego i pomysły dla FUDALI)
## Słowa kluczowe – co zyskuje, co traci
## Rynek i surowiec
## Szanse dla FUDALI (2–3 konkretne rekomendacje na dziś/ten tydzień)
## Źródła
```
W dni bez istotnych zmian raport może być krótki – napisz to uczciwie zamiast zapychać treść.

## Powiadomienie
Po zapisaniu raportu: `scripts/powiadom-whatsapp.sh "<TL;DR + link do pliku na GitHubie>"`.
