# Koparka Shanmon Fuji 388 – media (Zosia, 06.11.2026)
Prawdziwe zdjęcia z placu, 9:16 (1080×1920), 30 kl./s, bez dźwięku (muzyka w TikToku), **bez logo FUDALI, bez etykiety AI**.
- `koparka-nowa-2026.mp4` (12,4 s): „NOWA KOPARKO-ŁADOWARKA” → „Rok produkcji 2026” → „Łyżka przednia 6w1” → „Kopie do 5,5 m” → cena + „od ręki · Rzeszów” → „Oględziny i jazda próbna po umówieniu”.
- `koparka-5-5-m.mp4` (12,2 s): hak „KOPIE DO 5,5 m” → ramię teleskopowe → łyżka 6w1 → „Nowa · 2026” → cena → „Pisz w wiadomości – umówimy oględziny”.
- `koparka-szybkie-ciecia.mp4` (9 s): szybkie cięcia 1 s: NOWA 2026 · ŁYŻKA 6w1 · 5,5 m · OD RĘKI · RZESZÓW → cena → oględziny i jazda próbna.
**Cena = zmienny napis:** plik `cena.txt` (teraz „250 000 zł netto”). Zmiana: edytuj `cena.txt` i uruchom `python3 scripts/grafika/koparka_film.py` (odtwarza wszystkie 3 filmy).
Tylko fakty z briefu (nowa 2026, od ręki Rzeszów, oględziny/jazda próbna po umówieniu, 5,5 m głębokości, łyżka 6w1). Porównań cenowych („w cenie używanej”) nie ma – czekają na weryfikację Marka.
Kolejne: karuzele 9:16 i piny 2:3 po scenariuszach Oli.

## Posty TikTok wg tabeli Oli (`posty.md`) – bez ceny
`post-1.mp4` „Jedna łyżka. Sześć zadań.” (9,4 s) · `post-2.mp4` „Nowa. Rocznik 2026. Stoi w Rzeszowie.” · `post-3.mp4` „5,5 metra w dół.” – plus `post-N.txt` (numer, haczyk, napisy, opis). Haczyk w 1,4 s, potem napisy na kolejnych zdjęciach, plansza „Pisz w wiadomości”.
Skrypt: `python3 scripts/grafika/koparka_posty.py 1 2 3` (w słowniku `POSTY` są też gotowe 5, 6, 8, 9 – bez ceny).
Filmy `koparka-nowa-2026`, `koparka-5-5-m`, `koparka-szybkie-ciecia` ZAWIERAJĄ CENĘ – do użycia dopiero po akceptacji ceny przez Marka (posty 4, 7).

## Aktualizacja (06.11, po `ceny.md`)
- Cena w napisach: `cena.txt` = „250 000 zł netto (307 500 zł brutto)” – filmy `koparka-nowa-2026`, `koparka-5-5-m`, `koparka-szybkie-ciecia` odtworzone z nowym napisem (netto + brutto w nawiasie). Zmiana ceny: edytuj `cena.txt` (PL) / `cena-en.txt` (piny) i uruchom `koparka_film.py` / `koparka_piny.py`.
- Nowe filmy bez ceny: `post-5.mp4`, `post-6.mp4` (walk-around), `post-8.mp4`, `post-9.mp4` (wg oryginalnej tabeli ujęć/napisów z posty.md).
- Posty 4 i 7 (z ceną/wyposażeniem – napisy tylko z tabeli „Aktualizacja po ceny.md”, bez „Stage V”) – po decyzji Pablo/Marka o cenie.
- Piny EN 2:3: `marketing/kampanie/koparka/piny/pin-1…5.jpg` (prawdziwe zdjęcia, bez logo FUDALI, bez etykiety AI).
