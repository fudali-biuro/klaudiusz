# Procedura: codzienny raport konkurencji

Kontekst firmy: `AGENTS.md`. Język raportu: polski. Ton: konkretny, biznesowy, bez lania wody.

## Kroki
1. Wczytaj **wszystkie pliki `konkurencja/firmy/*.md`** (źródło prawdy o konkurentach; indeks: `konkurencja/konkurenci.md`)
   oraz 2–3 ostatnie raporty z `raporty/` (żeby nie powtarzać tych samych informacji i móc pokazać zmiany).
2. Wczytaj wyniki monitoringu (logi ze zmian) z ostatnich 24 h: `monitoring/social/<wczoraj>.md`, `monitoring/social/<dziś>.md`
   oraz `slowa-kluczowe/podsumowania/<wczoraj>.md`. Najważniejsze posty i pomysły „możemy zrobić podobnie” przenieś do raportu.
3. **Główny rywal – Bogateco / Płoty Ogrodowe (`konkurencja/firmy/bogateco.md`) – sprawdzaj ZAWSZE i najdokładniej**
   (obie strony, FB, IG, marketplace’y): nowe produkty, ceny kluczowych produktów (i zmiany vs poprzedni raport), promocje,
   darmowa dostawa, kampanie, posty, opinie, nagrody/PR, ruchy w B2B/eksporcie. Właściciel chce ich **przebić** –
   szukaj ich słabych punktów i luk w ofercie.
3a. **Drugi kluczowy rywal – Ecofurn / EcoChair (`konkurencja/firmy/ecofurn.md`)** – ten sam produkt co nasz leżak, konkurują za granicą.
   Co dzień: ceny EcoChair u partnerów (Bloomling, Galaxus, Folk Interiors…), nowe kolory/gatunki, czy weszli na Etsy/Amazon/Instagram,
   promocje. Ich strona blokuje automaty – korzystaj z wyszukiwarki i sklepów partnerskich (nie obchodź zabezpieczeń).
   W raporcie dodaj sekcję „🎯 Ecofurn – co robią i jak ich wyprzedzić” zaraz po Bogateco.
4. Research pozostałych (WebSearch/WebFetch), skup się na ostatnich 24–72 h i zmianach względem poprzednich raportów:
   - nowe produkty, promocje, zmiany cen (szczególnie altany, domki, pergole, drewutnie, meble ogrodowe, drewno),
   - aktywność marketingowa (FB/Instagram/TikTok, nowe kampanie, konkursy), opinie klientów,
   - nowi gracze na Podkarpaciu i w sprzedaży wysyłkowej w PL,
   - sygnały rynkowe: ceny drewna (Lasy Państwowe, tarcica), sezonowość, dotacje, przepisy (np. budowa bez pozwolenia).
5. Nie wymyślaj danych. Każdy fakt z linkiem do źródła. Jeśli czegoś nie da się sprawdzić – napisz to wprost.
6. Zapisz raport jako `raporty/RRRR-MM-DD-konkurencja.md` wg szablonu poniżej.
7. Nowego istotnego konkurenta dodaj jako nowy plik w `konkurencja/firmy/` (skopiuj dowolny istniejący jako szablon),
   istotne zmiany u istniejących dopisz w ich „Dzienniku obserwacji”, potem `python3 scripts/indeks_konkurencji.py`.

8. Status w biurze: na start `python3 scripts/status.py konkurencja pracuje "Raport konkurencji RRRR-MM-DD"`,
   po zapisie `python3 scripts/status.py konkurencja gotowe "Raport RRRR-MM-DD: <najważniejsza rzecz w 1 zdaniu>"`.

9. **Sezon świąteczny (polecenie Pablo, od 6.11 do 24.12.2026; brief `marketing/kampanie/2026-11-sezon-swiateczny-brief.md`)**:
   w raporcie dodaj sekcję „🎄 Święta – co robi konkurencja” (Bogateco, Ecofurn, Altanka): oferty/kolekcje świąteczne, prezenty, terminy zamówień
   i dostaw przed świętami, kampanie/posty, ceny. Pod spodem 2–4 konkretne pomysły „jak ich przebić” dla Oli (kanał FB/IG/Pinterest,
   produkt FUDALI, hook, CTA). Pomysły z werdyktem TAK od razu zgłoś Oli (send_message). Nic nie publikujemy bez zgody Pabla.

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
## Marketing i social media (w tym najlepsze posty z monitoringu i pomysły dla FUDALI)
## Słowa kluczowe – co zyskuje, co traci
## Rynek i surowiec
## Szanse dla FUDALI (2–3 konkretne rekomendacje na dziś/ten tydzień)
## Źródła
```
W dni bez istotnych zmian raport może być krótki – wtedy napisz to uczciwie zamiast zapychać treść.

## Powiadomienie
Po zapisaniu raportu wyślij krótkie podsumowanie (TL;DR + link do pliku):
`scripts/powiadom-telegram.sh "<tekst>"` – jeśli TELEGRAM_BOT_TOKEN nie jest ustawiony, skrypt kończy się bez błędu i tylko to zgłasza.
