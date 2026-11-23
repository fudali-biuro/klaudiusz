# Nowe logo FUDALI – warianty (Zosia, 23.11.2026) – tylko propozycja, nic nie wdrożone
**Plansza porównawcza:** `plansza.png` (4000×2000; źródło `plansza.html`) – obecne logo vs A / B / C, każdy na jasnym `#F7F5EF` i ciemnozielonym `#34442F`, w rozmiarach: logo pełne, nagłówek 40 px (bez opisu), favicon 32 px, awatar w kole.
**Pliki SVG** (tekst zamieniony na krzywe, bez zależności od fontów; wektorowo, bez generatora AI) – `svg/`:
- `logo-{A,B,C}-{jasne,ciemne}.svg` (z tłem), `…-przezroczyste.svg` (do nakładania), `…-naglowek.svg` (wersja bez opisu na nagłówek ≤40 px), `znak-{A,B,C}-{jasne,ciemne}-awatar.svg` (koło 100×100; favicon = ten sam znak 32 px).
**Generator:** `python3 scripts/grafika/logo_fudali.py` (opis do zmiany: zmienna środowiskowa `FUDALI_OPIS`, np. `FUDALI_OPIS="DREWNO I STOLARSTWO" python3 scripts/grafika/logo_fudali.py`; potem zrobić ponownie plansza.png – zrzut `plansza.html` w przeglądarce).
**Fonty:** Zilla Slab Bold (napis), Zilla Slab Medium (opis) – Google Fonts, licencja OFL, kopie w `fonty/`.

## Warianty
- **A** – mocna płytka „FUDALI” + rdzawa linia + opis rozciągnięty na szerokość napisu. Znak: litera F w kole.
- **B** – jak A, ale w linii prosty jednokolorowy liść dębu (okrągłe płaty, żyłki) – zintegrowany w środku linii (nie „wiszący”). Znak: liść w kole. Uwaga: w 32 px liść jest bardzo drobny (w favicon lepiej wyglądałoby samo F).
- **C** – monogram F w zaokrąglonym kwadracie + napis i opis po prawej. Znak do awatara: F w kole.

## Kolory (bez czerni)
zieleń `#34442F` (tekst/tło ciemne) · zieleń 2 `#475638` · oliwka `#737D4F` (opis na jasnym) · parchment `#F7F5EF` · akcent rdzawy `#B4552A` na jasnym tle, `#DB8453` na ciemnozielonym (jaśniejszy wariant, żeby linia była widoczna) · opis na ciemnym `#C9CDB5`.

## Opis pod nazwą
Robocza wersja: „STOLARSTWO I DREWNO OGRODOWE” (z uwag Pablo). Propozycje Oli i sprawdzenie Bartka (SEO) – do podmiany przez `FUDALI_OPIS`.
Uwagi z briefu zaadresowane: mocniejszy krój (płytka zamiast cienkiego szeryfa), opis zostaje, wersje czytelne w 40/32 px (nagłówek bez opisu, favicon = znak), awatar dla social mediów, zero czerni.
