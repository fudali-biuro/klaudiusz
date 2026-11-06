# 📸 Biblioteka prawdziwych zdjęć (polecenie Pablo, 06.11.2026)

**Strona:** https://biuro-fudali.vercel.app/zdjecia.html (w biurze przycisk „📸 Zdjęcia”) – Pablo wgrywa zdjęcia z telefonu/komputera
do jednej z sekcji. Zdjęcia przysłane w czacie albo w sesji Klaudiusza też trafiają tutaj.

| Sekcja | Co | Do czego |
|---|---|---|
| `tla/` | prawdziwe tła: salon, taras, ogród, wnętrza | miejsca, w które wstawiamy produkty |
| `produkty/` | prawdziwe zdjęcia produktów (leżak itd.) | produkt do wstawienia w tło |
| `gotowe/` | prawdziwe zdjęcia gotowe do użycia | posty bez obróbki albo z drobną (świąteczne dodatki, kadr) |

## Zasady pracy (Zosia, Ola – pilnuje Klaudiusz)
1. **Najpierw prawdziwe zdjęcia.** Grafika powstaje tak: wybierz tło + produkt, które do siebie pasują (światło, perspektywa, styl)
   → wstaw produkt w tło (`scripts/grafika/scena.py` albo montaż) → ewentualnie sezonowe dodatki (prezenty, choinka, światełka) → logo i napisy w stylu serii.
   To montaż prawdziwych zdjęć – **bez etykiety „AI”**. Czysta grafika AI tylko wyjątkowo i z etykietą.
2. **Rotacja:** `python3 scripts/zdjecia.py nastepne --sekcja tla` (najrzadziej używane) i po użyciu `python3 scripts/zdjecia.py uzyj <plik> --gdzie <id posta>`.
   Nie używamy tego samego tła/ujęcia w dwóch postach z rzędu na tym samym kanale.
3. Nowe zdjęcia od Pablo: `python3 scripts/zdjecia.py dodaj --sekcja <tla|produkty|gotowe> <pliki> --opis "…" [--tagi …] [--produkt lezak]`,
   potem obejrzyj każde i uzupełnij opis/tagi (`zdjecia.py opisz`) – po tagach zespół szuka pasujących par.
4. Gotowe grafiki idą do biblioteki akceptacji (`marketing/akceptacja/README.md`).
