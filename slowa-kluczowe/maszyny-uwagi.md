# 🚜 Frazy SEO – maszyny budowlane (Kuba, 26.11.2026) – wnioski i metoda
Plik z frazami: `slowa-kluczowe/maszyny.csv` (134 frazy: 106 z listy + 28 kandydatów long-tail z rozszerzenia a–z). Historia pozycji: `seo/pozycje/historia.csv`. Skrypty: `scripts/seo/maszyny_frazy.py`, `maszyny_kandydaci.py`, `maszyny_csv.py`.

## Skąd dane i ich granice (czytaj najpierw)
- **Podpowiedzi Google PL** (autocomplete, 0–10): czy ktoś w ogóle to wpisuje i jak. Brak podpowiedzi = prawie nikt.
- **Google Trends** (12 mies., Polska): zasięg **względny**, kotwica = „koparko ładowarka” = 100. To NIE jest liczba wyszukań. Trends zaokrągla do liczb całkowitych, więc wartości <1 = „brak sygnału”.
- **Trudność = oszacowanie** z podpowiedzi (portale OLX/Otomoto/Allegro, dealerzy marek) – nie mam danych SERP ani Search Console, więc to nie jest pomiar.
- **Pozycje FUDALI: brak** (pole puste w `historia.csv`) – bez Google Search Console nie da się ich zmierzyć. Do uzupełnienia po podpięciu GSC.
- **Prawdziwy wolumen (wyszukań/mies.) wymaga Google Ads Keyword Planner** – dostęp od Pablo (jest na liście próśb w briefie).

## Najważniejsze wnioski
1. **Mierzalny ruch ma tylko kilka fraz:** „koparko-ładowarka” (100), „jcb 3cx” (75), „koparko-ładowarka olx” (ok. 20). Wszystkie frazy kupujących z długiego ogona („nowa”, „cena”, „leasing”, „chińska”) mają w Trends ≈0 względem głowy, chociaż Google je podpowiada. Czyli: **ruch jest wąski – jedna mocna podstrona „koparko-ładowarka” (+ strona produktu Shanmon Fuji 388) wygra więcej niż wiele cienkich stron.**
2. **Wejście przez JCB 3CX:** „jcb 3cx” (75) i „jcb 3cx cena” – ludzie myślą marką; „alternatywa dla JCB” = puste (0 wyszukań) → w tytule dawać „JCB 3CX cena i alternatywa”, nie samo „alternatywa”.
3. **OLX/Otomoto/Allegro:** „koparko-ładowarka olx” (20) – kupujący szukają na portalach; ogłoszenia FUDALI (OLX/Otomoto) są tak samo ważne jak strona.
4. **Shanmon w Polsce = 0** (podpowiedzi tylko ru/en, „shanmon” myli się z Shannon) – markę budujemy od zera: zawsze „Shanmon Fuji 388” + „koparko-ładowarka”, nie „Shanmon” samo.
5. **Frazy z miastami** („koparko-ładowarka Rzeszów/Kraków/Warszawa…”) to prawie wyłącznie **usługi, wynajem, kurs, praca** – nie kupujący. Lokalność załatwia Google Business Profile + „Rzeszów” w treści, nie strony miejskie (zgodnie z decyzją Bartka).
6. **„Cena” bywa „za godzinę”** (usługi koparką) – frazy „koparka cena”, „koparko-ładowarka cena” trzeba pisać z „nowa” lub „netto”.
7. **Frazy z cudzymi markami** (jcb, cat, case, volvo, komatsu, hidromek, new holland, terex, waryński) – dealerzy w TOP10; wejście przez porównania z cenami z ogłoszeń (bez twierdzenia, że jesteśmy dealerem).
8. **Segment inny niż nasza maszyna:** minikoparka, ładowarka teleskopowa, koparka kołowa/gąsienicowa – duży zasięg, ale kupujący szuka innej maszyny; „ładowarka” to głównie telefon. W CSV mają priorytet C.

## Priorytet A w CSV (do treści i reklam)
koparko-ładowarka · koparko-ładowarka nowa / nowa koparko-ładowarka · koparko-ładowarka cena (z „nowa/netto”) · koparko-ładowarka leasing · chińska koparko-ładowarka (+cena) · jcb 3cx (+cena) · koparko-ładowarka olx/otomoto · shanmon fuji 388 (+ modele 388H/388T/388-II jako brand-building).
Ostrzeżenie dla reklam płatnych: te frazy mają niski wolumen – budżet Google Ads liczyć dopiero po Keyword Plannerze.
