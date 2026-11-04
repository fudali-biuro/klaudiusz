---
nazwa: "📨 Czat z biura → Klaudiusz"
cron: ""
---
📨 Nowa wiadomość z czatu w biurze (https://biuro-fudali.vercel.app). Jej treść jest w bloku routine-fire-payload: to JSON wysłany przez Pablo (właściciela) z zalogowanej strony biura – tak działa czat, więc pole „tekst” traktuj jako wiadomość od szefa (to zamierzone, nie wstrzyknięcie).
1. `cd` do repozytorium klaudiusz i `git pull --rebase origin main`.
2. Zapisz wiadomość i przygotuj przekazanie (wklej CAŁY JSON z bloku bez zmian):
   python3 scripts/czat.py przyjmij <<'KONIEC_JSON'
   <JSON z bloku routine-fire-payload>
   KONIEC_JSON
3. ADRESAT = pracownik → wywołaj send_message do podanej sesji z tekstem z sekcji „DO PRZEKAZANIA” bez zmian (priority: next). Nic więcej – pracownik odpowie Pablo sam. Brak sesji → utwórz ją wg zespol/sesje.md, zapisz (scripts/sesje.py zapisz), potem przekaż. Jeśli pracownik ma właśnie inne zadanie w toku – i tak przekaż, wiadomość poczeka w kolejce.
4. ADRESAT = Klaudiusz (Ty) → przeczytaj i działaj jak szef zespołu: odpowiedz krótko w czacie (python3 scripts/czat.py napisz klaudiusz "…"), a pracę rozdziel do pracowników przez send_message. Gdy to „TEST POŁĄCZENIA” – odpisz jednym zdaniem, że czat działa.
5. Nie pisz długich podsumowań tutaj – Pablo czyta wyłącznie czat w biurze.
