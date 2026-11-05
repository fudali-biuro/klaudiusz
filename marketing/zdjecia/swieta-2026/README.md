# Święta 2026 – grafiki (Zosia, pierwsza paczka 05.11.2026)
7 motywów × 4 formaty = 28 plików: `<motyw>-ig-4x5.jpg` (1080×1350), `-ig-1x1.jpg` (1080), `-fb-191x1.jpg` (1200×628), `-pin-2x3.jpg` (1000×1500, **napisy EN** pod Pinterest/Etsy). Logo FUDALI w rogu; kadr z gotowych zdjęć.
**Oznaczenie AI:** wszystkie zdjęcia bazowe to obrazy AI (zdjęcia produktów w scenach) – na kwadratach/pionach jest dopisek „grafika AI”, w opisach postów też oznaczać.
Motywy: `lezak-prezent` (299 zł, darmowa wysyłka), `lezak-kokarda`, `lezak-choinka`, `zestaw-wnetrze`, `stolki` (1200 zł), `podkladka` (99 zł), `otwieracz-kot` (49 zł). Ceny z fudali.com.pl (05.11.2026) – Ola, sprawdź przed publikacją.
Skrypt: `python3 scripts/grafika/swieta.py` (teksty/motywy w słowniku `KARTY`; nowe zdjęcia → dopisać wpis). Nowe sceny AI dopiero po odnowieniu limitu.

## Paczka 2 (05.11.2026) – zlecenie Oli
- **Kolaż startowy „Prezenty z drewna od 49 zł”** (post pon 9.11): `kolaz-start-ig-4x5.jpg`, `kolaz-start-fb-191x1.jpg` – 6 produktów z cenami (49/99/229/299/850/1200 zł), z `kampania-swieta/`.
- **Pinterest 2:3 (EN), 3 warianty leżaka:** `pin-lezak-gift-under-the-tree.jpg` (kokarda), `pin-lezak-cushion-included.jpg`, `pin-lezak-gift-idea.jpg`.
- **Podkładka 99 zł:** `podkladka-ig-4x5.jpg`, `podkladka-ig-1x1.jpg` (FB 1:1), `podkladka-fb-191x1.jpg` – z paczki 1.
Skrypt: `python3 scripts/grafika/swieta_kolaz.py`. Wszystko AI (dopisek „grafika AI”). Ceny sprawdzić przed publikacją.

## ✨ Poprawka świątecznego klimatu (05.11.2026, na uwagę Klaudiusza)
Nadpisane pliki: wszystkie packshotowe motywy – `lezak-prezent-*`, `zestaw-wnetrze-*`, `stolki-*`, `podkladka-*` (4 formaty) – oraz `kolaz-start-*` i `pin-lezak-cushion-included.jpg`.
Dołożony montaż (bez nowego AI): cieplejsza kolorystyka, światełka bokeh, delikatny śnieg, gałązki świerku z bombkami i czerwonymi jagodami w rogach, czerwono-złote akcenty. Wzorce bez zmian: `lezak-choinka-*`, `lezak-kokarda-*`, `otwieracz-kot-*`.

## ❌ Nie używać – czekają na scenę AI (decyzja Klaudiusza, 05.11.2026)
Rysowane gałązki i bokeh na jasnym pustym wnętrzu nie robią świąt. **Nie używać:** `zestaw-wnetrze-*`, `lezak-prezent-*`, `stolki-*`, `podkladka-*` (wszystkie formaty) oraz `pin-lezak-cushion-included.jpg`.
**Do używania:** `kolaz-start-*`, `lezak-choinka-*`, `lezak-kokarda-*`, `otwieracz-kot-*`, `pin-lezak-gift-under-the-tree.jpg`, `pin-lezak-gift-idea.jpg` oraz sceny z `marketing/zdjecia/kampania-swieta/`.

### Kolejka na nowe sceny AI (gdy wróci limit Antigravity)
1. Wnętrze z choinką/kominkiem jak w `lezak-choinka` – zestaw: leżak + stolik Płatek + stołki (zamiast `zestaw-wnetrze`).
2. Stołki z wózkiem w świątecznym wnętrzu (zamiast `stolki-*`).
3. Podkładka z orzecha w świątecznej scenie (kubek, światełka) – zamiast `podkladka-*`.
4. Leżak „cushion included” w ciepłej scenie świątecznej (pin 2:3, EN).
Po nowych scenach: ponowne złożenie 4 formatów przez `scripts/grafika/swieta.py` (bez gałązek/bokeh na packshotach).
