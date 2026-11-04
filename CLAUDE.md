# Klaudiusz

Asystent AI firmy **FUDALI Sp. z o.o.** (Głogów Małopolski) – nowoczesne stolarstwo i naturalne konstrukcje drewniane
(domki ogrodowe, altany, pergole, wiaty, drewutnie, meble ogrodowe, tarcica, drewno opałowe, drobne akcesoria).

## Zadania automatyczne

| Zadanie | Kiedy | Wynik |
|---|---|---|
| Raport konkurencji | codziennie, gotowy ok. 8:00 (Europe/Warsaw) | `raporty/RRRR-MM-DD-konkurencja.md` + powiadomienie (aplikacja Claude, Telegram) |

## Struktura

- `konkurencja/konkurenci.md` – lista obserwowanych konkurentów (edytuj śmiało – dopisz/usuń firmy)
- `konkurencja/instrukcja-raportu.md` – procedura, którą wykonuje codzienne zadanie
- `raporty/` – archiwum raportów
- `scripts/powiadom-telegram.sh` – wysyłka powiadomienia na Telegram (bot)
