# Grafika – ściąga do promptów (Zosia, od 17.11.2026; wytyczne: `marketing/wiedza/lumor-ai.md`, lekcje Pablo 18–25)

Generator scen: `python3 scripts/grafika/scena.py --model openrouter:google/gemini-3-pro-image --proporcje 4:5|2:3 --zdjecie <referencja> --opis "<prompt>" --wyjscie <plik>`
(maszyny/tła tańszy model: `openrouter:google/gemini-3.1-flash-image`). Zero wideo AI. Jedna sztuka produktu w kadrze, 1:1 z referencją.

## 1. Zanim napiszesz prompt – 3 pytania
1. **Typ ujęcia:** PACKSHOT (sprzedaje produkt – prawdziwe zdjęcie Pablo, ewent. oczyszczone) · TEKSTURA (makro: słoje, węzeł liny, krawędź listewki) · LIFESTYLE (rytuał: kawa, książka, wieczór przy ogniu).
2. **Spójność kampanii:** ten sam produkt 1:1 (bryła, liczba listewek, lina, poduszka, kolor) w każdej scenie.
3. **Światło:** skąd pada i co podkreśla.

## 2. Szablon promptu
```
[FID]  Exactly ONE <produkt> in the whole frame, shown completely. Reproduce it EXACTLY as in the reference: <opis bryły: listewki, nogi, lina, poduszka, kolor> – no redesign, no duplicated or bent parts.
[KARTA SESJI]
  Typ: packshot | tekstura (macro) | lifestyle-rytuał
  Miejsce / rytuał: <np. kącik czytelniczy, kawa i książka>
  Światło: <skąd i jakie: twardy promień z boku / chmurne dzienne / lampa z lewej / flesz bezpośredni> – podkreśla <detal: słoje, linę>
  Pora: <świt / południe / zmierzch / noc>   Paleta: <3 kolory>   Flesz: tak/nie
  Niedoskonałość: <lekko krzywy kadr z ręki, twardy cień, drobny kurz> (mieszamy; nie złota godzina w każdym kadrze)
[KONIEC]  Candid editorial photograph, real unedited look, generous negative space, no people (chyba że zlecono), no text, no logos.
```
## 3. Zasady
- Na obrazku co najwyżej 2–4 słowa albo nic; zero odznak/ikonek/list zalet (lekcja 25). Test „super / okej / źle” – oddajemy tylko „super”.
- Sesja produktu = 3 typy ujęć (packshot / tekstura / lifestyle). Mieszać światło: flesz, twardy cień, chmurne dzienne, złota godzina tylko czasem.
- Sprawdzać wierność: dwa oparcia, wygięte siedzisko, zlane części = powtórka raz, potem odpuścić i dać znać Oli.
- Formaty: 4:5 (IG 1080×1350), 2:3 (Pinterest 1000×1500); po generacji powiększyć (Lanczos + UnsharpMask).
