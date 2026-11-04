# Klaudiusz

Asystent AI firmy **FUDALI Sp. z o.o.** (Głogów Małopolski, Podkarpacie) – nowoczesne stolarstwo i naturalne
konstrukcje drewniane: drewutnie, domki ogrodowe i nowoczesne domki, altany, pergole, wiaty, meble ogrodowe
(m.in. składany leżak z jodły), drewno konstrukcyjne i deski, akcesoria z drewna. Strona: https://fudali.com.pl,
Instagram: [@fudali_nowoczesne_stolarstwo](https://www.instagram.com/fudali_nowoczesne_stolarstwo/).

## Zadania automatyczne

| Zadanie | Kiedy | Procedura | Wynik |
|---|---|---|---|
| Raport konkurencji (główny rywal: Bogateco / Płoty Ogrodowe) | codziennie ok. 8:00 (+ powiadomienie Telegram) | `konkurencja/instrukcja-raportu.md` | `raporty/RRRR-MM-DD-konkurencja.md` |
| Monitoring IG/TikTok konkurencji + słowa kluczowe | co godzinę | `konkurencja/instrukcja-monitoringu.md` | `monitoring/social/RRRR-MM-DD.md`, `slowa-kluczowe/podsumowania/RRRR-MM-DD.md` |

## Struktura
- `konkurencja/firmy/*.md` – **źródło prawdy o konkurencji** (jeden plik = jedna firma, konta IG/TikTok w nagłówku)
- `konkurencja/konkurenci.md` – indeks (generowany)
- `slowa-kluczowe/` – lista fraz (`slowa-kluczowe.csv`), historia pomiarów, kandydaci, podsumowania godzinowe
- `monitoring/` – logi godzinne i stan scrapera (`monitoring/media/` – wideo/klatki, poza gitem)
- `raporty/` – codzienne raporty
- `scripts/` – scraper (Apify), analiza wideo (ffmpeg + Gemini 4 przez OpenRouter), metryki słów, powiadomienia Telegram

## Sekrety (zmienne środowiskowe środowiska chmurowego)
| Zmienna | Do czego |
|---|---|
| `APIFY_API_KEY` | scraping Instagram/TikTok (aktorzy `apify/instagram-scraper`, `clockworks/tiktok-scraper`) |
| `OPENROUTER_API_KEY` | analiza wideo klatka po klatce z dźwiękiem (Gemini 4, `google/gemini-4-argon`) |
| `TELEGRAM_BOT_TOKEN` (+ opcjonalnie `TELEGRAM_CHAT_ID`) | powiadomienia na Telegram |
- `AGENTS.md` – instrukcje dla agentów + lista narzędzi/API
