# Klaudiusz

Asystent AI firmy **FUDALI Sp. z o.o.** (Głogów Małopolski, Podkarpacie) – nowoczesne stolarstwo i naturalne
konstrukcje drewniane: drewutnie, domki ogrodowe i nowoczesne domki, altany, pergole, wiaty, meble ogrodowe
(m.in. składany leżak z jodły), drewno konstrukcyjne i deski, akcesoria z drewna. Strona: https://fudali.com.pl,
Instagram: [@fudali_nowoczesne_stolarstwo](https://www.instagram.com/fudali_nowoczesne_stolarstwo/).

## Zadania automatyczne

Zespół nie pracuje 24/7 – każdy pracownik budzi się na swoje **zmiany** (rano ok. 5:00 i w południe ok. 12:00).
Godziny: **`zespol/godziny.json`** (jedyne miejsce), obowiązki: `zespol/zadania/`, opis: `AGENTS.md` („Zmiany pracy”).

| Zadanie | Kiedy | Procedura | Wynik |
|---|---|---|---|
| Raport konkurencji (główny rywal: Bogateco / Płoty Ogrodowe) | poranna zmiana (+ powiadomienie Telegram) | `konkurencja/instrukcja-raportu.md` | `raporty/RRRR-MM-DD-konkurencja.md` |
| Monitoring IG/TikTok konkurencji + słowa kluczowe | każda zmiana | `konkurencja/instrukcja-monitoringu.md` | `monitoring/social/RRRR-MM-DD.md`, `slowa-kluczowe/podsumowania/RRRR-MM-DD.md` |

## Struktura
- `AGENTS.md` – główne instrukcje dla agentów (zasady pracy, narzędzia/API); `CLAUDE.md` tylko go importuje
- `zespol/` – **7 wirtualnych pracowników** (karty `<id>.md` + statusy) – Klaudiusz jest mózgiem, oni wykonują role
- `biuro/` – **wirtualne biuro** na Vercel (pikselowa mapa: kto pracuje, kto czeka na szefa) – instrukcja `biuro/README.md`
- `konkurencja/firmy/*.md` – **źródło prawdy o konkurencji** (jeden plik = jedna firma, konta IG/TikTok w nagłówku)
- `konkurencja/konkurenci.md` – indeks (generowany)
- `slowa-kluczowe/` – lista fraz (`slowa-kluczowe.csv`), historia pomiarów, kandydaci, podsumowania z każdej zmiany
- `monitoring/` – logi z każdej zmiany i stan scrapera (`monitoring/media/` – wideo/klatki, poza gitem)
- `raporty/` – codzienne raporty
- `scripts/` – scraper (Apify), analiza wideo (ffmpeg + Gemini 4 przez OpenRouter), metryki słów, powiadomienia Telegram

## Sekrety (zmienne środowiskowe środowiska chmurowego)
Pełna, aktualna lista narzędzi, kluczy i ich statusów: **`AGENTS.md`** (sekcja „Narzędzia i klucze API”).

| Zmienna | Do czego |
|---|---|
| `APIFY_API_KEY` | scraping Instagram/TikTok (aktorzy `apify/instagram-scraper`, `clockworks/tiktok-scraper`) |
| `OPENROUTER_API_KEY` | analiza wideo klatka po klatce z dźwiękiem (Gemini 4, `google/gemini-4-argon`) |
| `TELEGRAM_BOT_TOKEN` (+ opcjonalnie `TELEGRAM_CHAT_ID`) | powiadomienia na Telegram |
