#!/usr/bin/env bash
# Godzinny przebieg danych: scraping IG/TikTok -> analiza wideo (klatki + Gemini) -> metryki słów -> indeks.
# Każdy krok jest niezależny: błąd jednego nie zatrzymuje kolejnych.
cd "$(dirname "$0")/.."
python3 scripts/monitoring_social.py  || echo "UWAGA: monitoring_social.py zakończył się błędem"
python3 scripts/analiza_wideo.py      || echo "UWAGA: analiza_wideo.py zakończył się błędem"
python3 scripts/slowa_kluczowe.py     || echo "UWAGA: slowa_kluczowe.py zakończył się błędem"
python3 scripts/indeks_konkurencji.py || true
