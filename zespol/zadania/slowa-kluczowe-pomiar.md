---
nazwa: "Pomiar słów kluczowych"
kiedy: "kazda"
---
# Pomiar słów kluczowych (na każdej zmianie)

Procedura: `konkurencja/instrukcja-monitoringu.md`, sekcja **4** (+ 5 zapis, 5a status). Dane konkurencji zbiera Mietek na swojej zmianie (kilkanaście minut przed Tobą) – korzystasz z najnowszych (`monitoring/stan/`).

1. Pomiar: `bash scripts/godzinny.sh slowa` (Google Autocomplete + wzmianki u konkurencji; sam ustawia Twój status „pracuje”).
2. Dopisz sekcję `## HH:MM` (godzina zmiany) w `slowa-kluczowe/podsumowania/RRRR-MM-DD.md` (TOP 5, rośnie/spada, nieistotne, kandydaci). Bez zmian → krótko „bez zmian” + TOP 3. Na ostatniej zmianie dnia (`godziny.py zmiana` napisze „ostatnia zmiana dnia”) dodaj `## Podsumowanie dnia`.
3. Zapis na main, status: `python3 scripts/status.py slowa-kluczowe gotowe "HH:MM – TOP: <fraza> (<ocena>)"`.
4. Mocny skok frazy → zaznacz go w podsumowaniu („⚡ SKOK: fraza, o ile, dlaczego”) – Ola i Bartek czytają je na swojej zmianie. send_message tylko w sprawie pilnej na dziś. W innych przypadkach nic nie wysyłaj.


## Google Search Console – prawdziwe pozycje (od 27.11.2026, pierwsza zmiana dnia)
`python3 scripts/seo/gsc.py pozycje` i `python3 scripts/seo/gsc.py strony` → `seo/pozycje/gsc/RRRR-MM-DD-*.csv` (dane z ostatnich 28 dni, ok. 2 dni opóźnienia).
W podsumowaniu dnia: frazy maszyn i mebli – średnia pozycja, wyświetlenia, kliknięcia; uzupełnij kolumnę `pozycja_fudali` w `seo/pozycje/historia.csv`.
Pusty wynik w pierwszych dniach = normalne (usługa zweryfikowana 26.11). Klucza nigdy nie wypisuj.
