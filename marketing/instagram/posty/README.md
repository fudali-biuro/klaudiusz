# Grafiki Instagram – pierwsza siatka (Zosia, 06.11.2026)
Prawdziwe zdjęcia z `marketing/biblioteka-zdjec/` (w tym profesjonalne „Produktywniej – Maciej Banasik”), montaż – **bez etykiety AI**. Styl serii: krem + ciemna zieleń + drewno, logo FUDALI lewy górny róg, etykieta tematu prawy górny, nagłówek serif, złota kreska. 4:5 (1080×1350), reelsy 9:16.
| Post | Pliki | Uwagi |
|---|---|---|
| P1 5 kolorów | `P1/slajd-1…6.jpg` | 1 slajd = 1 kolor (jasny brąz, brąz, ciemny brąz, grafit, czerń; zbliżenia fotografa -18/-17/-15/-16/-14) + slajd końcowy z montażem 5 leżaków |
| P2 przechowywanie | `P2/slajd-1…4.jpg` | sucho · przewiewnie · z dala od wilgoci i dużego ciepła (fakty z `produkty.md`) |
| P3 reel | `P3-reel.mp4` (10,5 s) + okładka `P3/okladka.jpg` | wycięte blaty → stolik Płatek (prawdziwe zdjęcia, ruchomy kadr) |
| P4 z czego leżak | `P4/slajd-1…5.jpg` | 30 mm/50 mm/10 kg, wymiary 100×55×90, złożony 125×55×25 (z infografik fotografa), poduszka, lina |
| P5 | `P5/slajd-1.jpg` | taras z paleniskiem |
| P6 prezent dla taty | `P6/slajd-1…4.jpg` | 49 / 99 / 229 / 299 zł (+ darmowa wysyłka przy leżaku) |
| P7 reel | `P7-reel.mp4` (9,2 s) + okładka `P7/okladka.jpg` | animacja 3D składania z biblioteki, napisy „Składa się na płasko · 10 kg” |
| P8 realizacja | `P8/slajd-1…3.jpg` | tylko prawdziwa realizacja (weranda klienta, image-20260904-110937-616): pełny kadr + 2 zbliżenia tego samego zdjęcia |
| P9 dąb czy jodła | `P9/slajd-1…5.jpg` | tylko fakty: leżak – jodła FSC; stołki i Płatek – dąb czerwony |
Siatka: `../siatka-3x3.jpg` (P9 P8 P7 / P6 P5 P4 / P3 P2 P1). Okładki wyróżnionych (1080×1920): `../wyroznione/okladka-{lezak,gear,dom,kropla,prezent,pytanie}.png` = Leżak, Jak to robimy, Realizacje, Pielęgnacja, Prezenty, Pytania; podgląd w kółku: `../wyroznione/podglad-kolka.png`.
Skrypt: `python3 scripts/grafika/ig_serie.py [posty|reelsy|siatka|okladki]` (zmiany tekstów w funkcji `posty()`).
Nie zrobione: P8 „realizacje” z nazwą miejscowości (brak danych), prawdziwy proces z warsztatu (czekamy na filmy od Pablo).

## ✨ Wersja 2 (06.11, poprawki Klaudiusza/Oli)
- Okładki (slajd 1): tekst tylko w P1 „5 kolorów. Który Twój?”, P4 „10 kg · 30 mm”, P6 „Prezent dla taty · od 49 zł”; reszta (P2, P3, P5, P7, P8, P9) = **czyste zdjęcie**, bez plakietek i bez logo (logo małe tylko na slajdach 2+). Plakietki tematu usunięte z całej serii.
- P2 okładka = prawdziwe zdjęcie leżaków przy białej bramie (karuzela ma teraz 5 slajdów); P4 okładka = cały leżak (nie kolejne listwy); P8 = „Lato na tarasie” (bez „klienta”); P7 = reel z prawdziwych zdjęć (leżak złożony → rozłożony → w ogrodzie), okładka = leżak pod kwitnącą wiśnią.
- Jedna korekta barwna całej serii (ciepło, lekko złoty, kontrast +5%) – w funkcji `save()`.
- **Stories D1–D7** (9–15.11): `../stories/D1…D7/klatka-N.jpg` (1080×1920, 3–4 klatki/dzień, mało tekstu; ankiety/quizy/pytania = puste miejsce na naklejki w aplikacji): D1 jodła czy dąb · D2 ile waży leżak (odp. 10 kg) · D3 z czego to zrobione · D4 wybierz kolor · D5 zadaj pytanie stolarzowi · D6 taras o zmierzchu · D7 zapowiedź tygodnia. Odtworzenie: `python3 scripts/grafika/ig_serie.py stories`.
