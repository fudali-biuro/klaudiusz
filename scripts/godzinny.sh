#!/usr/bin/env bash
# Godzinny przebieg danych: scraping IG/TikTok -> analiza wideo (klatki + Gemini) -> metryki słów -> indeks.
# Każdy krok jest niezależny: błąd jednego nie zatrzymuje kolejnych.
# Statusy w wirtualnym biurze: Mietek (konkurencja) i Kuba (słowa kluczowe) – zespol/status/*.json
# Użycie:  bash scripts/godzinny.sh konkurencja   # część Mietka (jego sesja, o :37)
#          bash scripts/godzinny.sh slowa         # część Kuby (jego sesja, o :52)
#          bash scripts/godzinny.sh               # obie (test / ręcznie)
cd "$(dirname "$0")/.."
CO="${1:-wszystko}"
status() { python3 scripts/status.py "$@" --bez-zapisu >/dev/null 2>&1 || true; }

if [[ "$CO" == "konkurencja" || "$CO" == "wszystko" ]]; then
  status konkurencja pracuje "Zbieram nowe posty IG/TikTok konkurencji (Apify)"
  python3 scripts/monitoring_social.py  || { echo "UWAGA: monitoring_social.py zakończył się błędem"; status konkurencja blad "Scraper IG/TikTok zwrócił błąd"; }
  status konkurencja pracuje "Oglądam wideo konkurencji (klatki + Gemini 4)"
  python3 scripts/analiza_wideo.py      || echo "UWAGA: analiza_wideo.py zakończył się błędem"
  status konkurencja pracuje "Dane zebrane – analizuję posty i piszę log godzinny"
  python3 scripts/indeks_konkurencji.py || true
fi

if [[ "$CO" == "slowa" || "$CO" == "wszystko" ]]; then
  status slowa-kluczowe pracuje "Mierzę ważność fraz (Google + konkurencja)"
  if python3 scripts/slowa_kluczowe.py; then
    status slowa-kluczowe pracuje "Pomiar gotowy – piszę podsumowanie godzinowe"
  else
    echo "UWAGA: slowa_kluczowe.py zakończył się błędem"; status slowa-kluczowe blad "Pomiar fraz zwrócił błąd"
  fi
fi
