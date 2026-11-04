#!/usr/bin/env bash
# Godzinny przebieg danych: scraping IG/TikTok -> analiza wideo (klatki + Gemini) -> metryki słów -> indeks.
# Każdy krok jest niezależny: błąd jednego nie zatrzymuje kolejnych.
# Statusy w wirtualnym biurze: Mietek (konkurencja) i Kuba (słowa kluczowe) – zespol/status/*.json
cd "$(dirname "$0")/.."
status() { python3 scripts/status.py "$@" >/dev/null 2>&1 || true; }

status konkurencja pracuje "Zbieram nowe posty IG/TikTok konkurencji (Apify)"
python3 scripts/monitoring_social.py  || { echo "UWAGA: monitoring_social.py zakończył się błędem"; status konkurencja blad "Scraper IG/TikTok zwrócił błąd"; }
status konkurencja pracuje "Oglądam wideo konkurencji (klatki + Gemini 4)"
python3 scripts/analiza_wideo.py      || echo "UWAGA: analiza_wideo.py zakończył się błędem"
status konkurencja pracuje "Dane zebrane – analizuję posty i piszę log godzinny"

status slowa-kluczowe pracuje "Mierzę ważność fraz (Google + konkurencja)"
if python3 scripts/slowa_kluczowe.py; then
  status slowa-kluczowe pracuje "Pomiar gotowy – piszę podsumowanie godzinowe"
else
  echo "UWAGA: slowa_kluczowe.py zakończył się błędem"; status slowa-kluczowe blad "Pomiar fraz zwrócił błąd"
fi
python3 scripts/indeks_konkurencji.py || true
