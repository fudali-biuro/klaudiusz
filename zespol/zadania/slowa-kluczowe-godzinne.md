---
nazwa: "🔑 Kuba – pomiar słów kluczowych (co godzinę)"
cron: "52 * * * *"
---
# Godzinny pomiar słów kluczowych

Procedura: `konkurencja/instrukcja-monitoringu.md`, sekcja **4** (+ 5 zapis, 5a status). Dane konkurencji zbiera Mietek o :37 – Ty korzystasz z najnowszych (`monitoring/stan/`).

1. Pomiar: `bash scripts/godzinny.sh slowa` (Google Autocomplete + wzmianki u konkurencji; sam ustawia Twój status „pracuje”).
2. Dopisz sekcję `## HH:00` w `slowa-kluczowe/podsumowania/RRRR-MM-DD.md` (TOP 5, rośnie/spada, nieistotne, kandydaci). Bez zmian → krótko „bez zmian” + TOP 3. Pierwszy przebieg po 20:00 → `## Podsumowanie dnia`.
3. Zapis na main, status: `python3 scripts/status.py slowa-kluczowe gotowe "HH:00 – TOP: <fraza> (<ocena>)"`.
4. Mocny skok frazy → krótki meldunek do Bartka i Oli (send_message do ich sesji). W innych przypadkach nic nie wysyłaj.
