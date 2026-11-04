# Zadania automatyczne – każdy pracownik ma swoje

Jeden plik = jedno zadanie automatyczne jednego pracownika: `<id-pracownika>-<klucz>.md`.
Nagłówek: `nazwa` (tak nazywa się zadanie w Claude), `cron` (kiedy – pusty = tylko na wezwanie).
Zadanie budzi **stałą sesję pracownika** (subczat nazwany jego imieniem) i każe mu wykonać procedurę z tego pliku.
Utworzenie / przeniesienie zadań: `zespol/sesje.md`. Lista: `python3 scripts/sesje.py pokaz`.

| Plik | Pracownik | Kiedy |
|---|---|---|
| `klaudiusz-czat.md` | 🧠 Klaudiusz | na wezwanie – wiadomość z czatu w biurze |
| `konkurencja-raport.md` | 🔭 Mietek | codziennie 7:41 (raport gotowy ok. 8:00) |
| `konkurencja-monitoring.md` | 🔭 Mietek | co godzinę o :37 |
| `slowa-kluczowe-godzinne.md` | 🔑 Kuba | co godzinę o :52 (po danych Mietka) |
| `pozycjonowanie-trendy.md` | 🧭 Bartek | poniedziałek 7:17 |
| `marketing-plan-tygodnia.md` | 📣 Ola | poniedziałek 7:47 (po trendach Bartka) |
| `marketing-pinterest.md` | 📣 Ola | codziennie 9:00 |

Zosia, Marek i Greta nie mają zadań na zegarek – pracują na zlecenie (Klaudiusz, Ola, Pablo z czatu).
