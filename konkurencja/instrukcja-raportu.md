# Procedura: codzienny raport konkurencji

Kontekst firmy: patrz `README.md`. Język raportu: polski. Ton: konkretny, biznesowy, bez lania wody.

## Kroki
1. Wczytaj `konkurencja/konkurenci.md` oraz 2–3 ostatnie raporty z `raporty/` (żeby nie powtarzać tych samych informacji i móc pokazać zmiany).
2. **Główny rywal – Bogateco / Płoty Ogrodowe – sprawdzaj ZAWSZE i najdokładniej** (obie strony, FB, IG, marketplace’y):
   nowe produkty, ceny kluczowych produktów (i zmiany vs poprzedni raport), promocje, darmowa dostawa, kampanie, posty, opinie,
   nagrody/PR, ruchy w B2B/eksporcie. Właściciel chce ich **przebić** – szukaj ich słabych punktów i luk w ofercie.
3. Research pozostałych (WebSearch/WebFetch), skup się na ostatnich 24–72 h i zmianach względem poprzednich raportów:
   - nowe produkty, promocje, zmiany cen (szczególnie altany, domki, pergole, drewutnie, drewno opałowe),
   - aktywność marketingowa (FB/Instagram, nowe kampanie, konkursy), opinie klientów,
   - nowi gracze na Podkarpaciu i w sprzedaży wysyłkowej w PL,
   - sygnały rynkowe: ceny drewna (Lasy Państwowe, tarcica), sezonowość, dotacje, przepisy (np. budowa bez pozwolenia).
4. Nie wymyślaj danych. Każdy fakt z linkiem do źródła. Jeśli czegoś nie da się sprawdzić – napisz to wprost.
5. Zapisz raport jako `raporty/RRRR-MM-DD-konkurencja.md` wg szablonu poniżej.
6. Jeśli znalazłeś nowego istotnego konkurenta – dopisz go w sekcji „Nowo wykryci” w `konkurencja/konkurenci.md`.

## Szablon raportu
```
# Raport konkurencji – RRRR-MM-DD

## TL;DR (max 5 punktów)
## 🎯 Bogateco / Płoty Ogrodowe – co dziś robią
(nowości, ceny, promocje, social media, opinie; zmiany vs poprzedni raport)
## Jak ich przebić (2–3 konkretne ruchy dla FUDALI: produkt, cena, marketing, SEO, marketplace)
## Co się zmieniło u konkurencji
(tabela: Firma | Zmiana | Źródło)
## Ceny – obserwacje
## Marketing i social media
## Rynek i surowiec
## Szanse dla FUDALI (2–3 konkretne rekomendacje na dziś/ten tydzień)
## Źródła
```
W dni bez istotnych zmian raport może być krótki – wtedy napisz to uczciwie zamiast zapychać treść.

## Powiadomienie
Po zapisaniu raportu wyślij krótkie podsumowanie (TL;DR + link do pliku na GitHubie):
`scripts/powiadom-telegram.sh "<tekst>"` – jeśli TELEGRAM_BOT_TOKEN nie jest ustawiony (TELEGRAM_CHAT_ID jest opcjonalny – skrypt wykrywa go sam), skrypt kończy się bez błędu i tylko to zgłasza.
