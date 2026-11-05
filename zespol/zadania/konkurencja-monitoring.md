---
nazwa: "Monitoring IG/TikTok konkurencji"
kiedy: "kazda"
kolejnosc: 10
---
# Monitoring Instagram/TikTok konkurencji (na każdej zmianie)

Procedura szczegółowa: `konkurencja/instrukcja-monitoringu.md` – wykonujesz sekcje **1, 2, 3, 5, 5a i 6** (sekcję 4 – słowa kluczowe – robi Kuba na swojej zmianie, kilkanaście minut po Tobie).

1. Dane: `bash scripts/godzinny.sh konkurencja` (scraper Apify → klatki + Gemini 4; sam ustawia Twój status „pracuje”).
2. Analiza nowych postów (wideo: arkusz klatek narzędziem Read ORAZ analiza Gemini z `monitoring/stan/wideo-analizy/`), werdykt „czy FUDALI może zrobić podobne” z konkretnym pomysłem; przy Bogateco – „jak ich przebić”.
3. Dopisz sekcję `## HH:MM` (godzina zmiany) w `monitoring/social/RRRR-MM-DD.md`, dziennik obserwacji w `konkurencja/firmy/<slug>.md`. Brak nowości → jedna linia.
4. Zapis na main (bez `monitoring/media/`), status: `python3 scripts/status.py konkurencja gotowe "HH:MM – N nowych postów (M z werdyktem TAK)"`.
5. Werdykt TAK → pomysł zostaje w logu (wyraźnie: „💡 TAK”, link + pomysł w 1–2 zdaniach) – Ola przegląda go na swojej zmianie (kilkanaście minut po Tobie), nie musisz do niej pisać. send_message do Oli tylko w sprawie pilnej na dziś (np. Bogateco rusza z promocją, na którą trzeba odpowiedzieć). Telegram tylko przy czymś naprawdę ważnym (sekcja 6).
6. Brak nowości = żadnych wiadomości, tylko linia w logu i status.
