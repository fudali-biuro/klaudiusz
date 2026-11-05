#!/usr/bin/env bash
# Przebieg danych na zmianie (godziny: zespol/godziny.json): scraping IG/TikTok -> analiza wideo (klatki + Gemini) -> metryki słów -> indeks.
# Każdy krok jest niezależny: błąd jednego nie zatrzymuje kolejnych.
# Statusy w wirtualnym biurze: Mietek (konkurencja) i Kuba (słowa kluczowe) – zespol/status/*.json
# Użycie:  bash scripts/godzinny.sh konkurencja   # część Mietka (jego zmiana)
#          bash scripts/godzinny.sh slowa         # część Kuby (jego zmiana, kilkanaście minut po Mietku)
#          bash scripts/godzinny.sh               # obie (test / ręcznie)
cd "$(dirname "$0")/.."
CO="${1:-wszystko}"
status() { python3 scripts/status.py "$@" --bez-zapisu >/dev/null 2>&1 || true; }

if [[ "$CO" == "konkurencja" || "$CO" == "wszystko" ]]; then
  status konkurencja pracuje "Zbieram nowe posty IG/TikTok konkurencji (Apify)"
  python3 scripts/monitoring_social.py  || { echo "UWAGA: monitoring_social.py zakończył się błędem"; status konkurencja blad "Scraper IG/TikTok zwrócił błąd"; }
  status konkurencja pracuje "Oglądam wideo konkurencji (klatki + Gemini 4)"
  python3 scripts/analiza_wideo.py      || echo "UWAGA: analiza_wideo.py zakończył się błędem"
  status konkurencja pracuje "Dane zebrane – analizuję posty i piszę log"
  python3 scripts/indeks_konkurencji.py || true
fi

if [[ "$CO" == "slowa" || "$CO" == "wszystko" ]]; then
  status slowa-kluczowe pracuje "Mierzę ważność fraz (Google + konkurencja)"
  if python3 scripts/slowa_kluczowe.py; then
    status slowa-kluczowe pracuje "Pomiar gotowy – piszę podsumowanie"
  else
    echo "UWAGA: slowa_kluczowe.py zakończył się błędem"; status slowa-kluczowe blad "Pomiar fraz zwrócił błąd"
  fi
fi
