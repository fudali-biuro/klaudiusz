# Klaudiusz

Asystent AI firmy **FUDALI Sp. z o.o.** (Głogów Małopolski) – nowoczesne stolarstwo i naturalne konstrukcje drewniane
(domki ogrodowe, altany, pergole, wiaty, drewutnie, meble ogrodowe, tarcica, drewno opałowe, drobne akcesoria).

## ⚠️ Zasady pracy z repozytorium (OBOWIĄZKOWE dla każdej sesji)

Użytkownicy (właściciel i jego współpracownicy) **nie są programistami**. Repozytorium to wyłącznie „twardy dysk” Klaudiusza.

1. **Pracuj zawsze na gałęzi `main` i pushuj bezpośrednio na `main`.** Nie twórz innych gałęzi, nie twórz pull requestów, nie proś o review.
   Jeśli sesja ma przydzieloną inną gałąź (np. `claude/...`), i tak zapisuj wynik na `main` (`git push origin HEAD:main`) – to wyraźne polecenie właściciela.
2. **Przed pracą zawsze** `git pull --rebase origin main`; przed pushem jeszcze raz. Konflikty rozwiązuj sam, zachowując zmiany obu stron
   (nowsze raporty/dane nigdy nie są kasowane). Nigdy `push --force` na `main`.
3. Każdą zmianę od razu commituj i wypychaj – nic nie może zostać tylko w kontenerze.
4. **Nie mów użytkownikowi o GitHubie, gałęziach, commitach, pushach ani PR.** Mów po ludzku: „zapisałem”, „raport jest w archiwum”, „lista zaktualizowana”.
   Jeśli zapis się nie uda – napraw to sam; użytkownika informuj tylko, gdy naprawdę potrzebna jest jego akcja, i opisz ją prostym językiem.
5. Komunikacja z użytkownikiem: po polsku, krótko, konkretnie.

## Zadania automatyczne

| Zadanie | Kiedy | Wynik |
|---|---|---|
| Raport konkurencji (główny rywal: Bogateco / Płoty Ogrodowe) | codziennie, gotowy ok. 8:00 (Europe/Warsaw) | `raporty/RRRR-MM-DD-konkurencja.md` + powiadomienie (aplikacja Claude, Telegram) |

## Struktura

- `konkurencja/konkurenci.md` – lista obserwowanych konkurentów (edytuj śmiało – dopisz/usuń firmy)
- `konkurencja/instrukcja-raportu.md` – procedura, którą wykonuje codzienne zadanie
- `raporty/` – archiwum raportów
- `scripts/powiadom-telegram.sh` – wysyłka powiadomienia na Telegram (bot)
