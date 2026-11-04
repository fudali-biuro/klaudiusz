---
nazwa: "🔭 Mietek – raport konkurencji (8:00)"
cron: "CRON_TZ=Europe/Warsaw 41 7 * * *"
---
# Dzienny raport konkurencji (gotowy ok. 8:00 czasu polskiego)

Główni rywale do przebicia: **Bogateco / Płoty Ogrodowe** (bogateco.eu, plotyogrodowe.pl) i **Ecofurn / EcoChair**.

1. `python3 scripts/status.py konkurencja pracuje "Raport konkurencji na dziś"`.
2. Przeczytaj `konkurencja/instrukcja-raportu.md` i `konkurencja/konkurenci.md` – postępuj DOKŁADNIE wg nich.
3. Research w sieci (WebSearch/WebFetch). Nie wymyślaj faktów – każdy fakt z linkiem. Porównaj z ostatnimi raportami w `raporty/` i pokaż zmiany.
4. Zapisz `raporty/RRRR-MM-DD-konkurencja.md` (data wg Europe/Warsaw) + ewentualne zmiany w plikach `konkurencja/firmy/`; zapis na main (pull --rebase, push HEAD:main, bez force). Sprawdź `git ls-remote origin main`.
5. Telegram: `scripts/powiadom-telegram.sh "<wiadomość>"` – samowystarczalna, bez linków do GitHuba: „📊 Raport konkurencji DD.MM”, 🎯 Bogateco/Płoty Ogrodowe (3–4 punkty), 📌 reszta rynku (2–3), 💪 Jak ich przebić (2–3), na końcu „Pełny raport w biurze: https://biuro-fudali.vercel.app”. Max ~3500 znaków.
6. `python3 scripts/status.py konkurencja gotowe "Raport DD.MM gotowy – <1 zdanie>"` i meldunek do Klaudiusza (send_message): najważniejsze 2 punkty + pomysły dla Oli.
Jeśli coś nie działa i nie da się naprawić – `status.py konkurencja czeka "…" --prosba "<prosto, czego potrzebujesz>"`.
