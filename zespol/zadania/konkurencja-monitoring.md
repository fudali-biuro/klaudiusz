---
nazwa: "🔭 Mietek – monitoring IG/TikTok (co godzinę)"
cron: "37 * * * *"
---
# Godzinny monitoring Instagram/TikTok konkurencji

Procedura szczegółowa: `konkurencja/instrukcja-monitoringu.md` – wykonujesz sekcje **1, 2, 3, 5, 5a i 6** (sekcję 4 – słowa kluczowe – robi Kuba w swojej sesji o :52).

1. Dane: `bash scripts/godzinny.sh konkurencja` (scraper Apify → klatki + Gemini 4; sam ustawia Twój status „pracuje”).
2. Analiza nowych postów (wideo: arkusz klatek narzędziem Read ORAZ analiza Gemini z `monitoring/stan/wideo-analizy/`), werdykt „czy FUDALI może zrobić podobne” z konkretnym pomysłem; przy Bogateco – „jak ich przebić”.
3. Dopisz sekcję `## HH:00` w `monitoring/social/RRRR-MM-DD.md`, dziennik obserwacji w `konkurencja/firmy/<slug>.md`. Brak nowości → jedna linia.
4. Zapis na main (bez `monitoring/media/`), status: `python3 scripts/status.py konkurencja gotowe "HH:00 – N nowych postów (M z werdyktem TAK)"`.
5. Werdykt TAK → krótki meldunek do Oli (send_message do jej sesji z zespol/sesje.json): link do posta + pomysł w 1–2 zdaniach. Telegram tylko przy czymś naprawdę ważnym (sekcja 6).
6. Brak nowości = żadnych wiadomości, tylko linia w logu i status.
