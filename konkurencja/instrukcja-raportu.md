# Procedura: codzienny raport konkurencji

Kontekst firmy: patrz `README.md`. Język raportu: polski. Ton: konkretny, biznesowy, bez lania wody.

## Kroki
1. Wczytaj `konkurencja/konkurenci.md` oraz 2–3 ostatnie raporty z `raporty/` (żeby nie powtarzać tych samych informacji i móc pokazać zmiany).
2. Research (WebSearch/WebFetch), skup się na ostatnich 24–72 h i zmianach względem poprzednich raportów:
   - nowe produkty, promocje, zmiany cen (szczególnie altany, domki, pergole, drewutnie, drewno opałowe),
   - aktywność marketingowa (FB/Instagram, nowe kampanie, konkursy), opinie klientów,
   - nowi gracze na Podkarpaciu i w sprzedaży wysyłkowej w PL,
   - sygnały rynkowe: ceny drewna (Lasy Państwowe, tarcica), sezonowość, dotacje, przepisy (np. budowa bez pozwolenia).
3. Nie wymyślaj danych. Każdy fakt z linkiem do źródła. Jeśli czegoś nie da się sprawdzić – napisz to wprost.
4. Zapisz raport jako `raporty/RRRR-MM-DD-konkurencja.md` wg szablonu poniżej.
5. Jeśli znalazłeś nowego istotnego konkurenta – dopisz go w sekcji „Nowo wykryci” w `konkurencja/konkurenci.md`.

## Szablon raportu
```
# Raport konkurencji – RRRR-MM-DD

## TL;DR (max 5 punktów)
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
`scripts/powiadom-whatsapp.sh "<tekst>"` – jeśli zmienne CallMeBot nie są ustawione, skrypt kończy się bez błędu i tylko to zgłasza.
