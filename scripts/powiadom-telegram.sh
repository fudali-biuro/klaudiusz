#!/usr/bin/env bash
# Wysyła wiadomość na Telegram przez Bot API.
# Wymaga zmiennej TELEGRAM_BOT_TOKEN. TELEGRAM_CHAT_ID jest opcjonalne – jeśli go brak,
# skrypt sam odczyta ID z ostatniej wiadomości wysłanej do bota (działa, gdy ktoś napisał
# do bota w ciągu ostatnich 24 h). Najpewniej: ID z @userinfobot wpisane jako TELEGRAM_CHAT_ID.
# Użycie: scripts/powiadom-telegram.sh "treść wiadomości"
set -euo pipefail
MSG="${1:?Podaj treść wiadomości}"
# Domyślny odbiorca: właściciel (chat ID bez tokenu bota nic nie daje, więc może być w repo)
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-6330814720}"
if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]]; then
  echo "Telegram: brak TELEGRAM_BOT_TOKEN – pomijam wysyłkę." >&2
  exit 0
fi
if [[ -z "${TELEGRAM_CHAT_ID:-}" ]]; then
  TELEGRAM_CHAT_ID=$(curl -sS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" \
    | python3 -c 'import sys,json; r=json.load(sys.stdin).get("result",[]); ids=[u.get("message",{}).get("chat",{}).get("id") for u in r]; ids=[i for i in ids if i]; print(ids[-1] if ids else "")')
  if [[ -z "$TELEGRAM_CHAT_ID" ]]; then
    echo "Telegram: brak TELEGRAM_CHAT_ID i nikt nie pisał do bota w ostatnich 24 h – napisz do bota cokolwiek albo ustaw TELEGRAM_CHAT_ID." >&2
    exit 0
  fi
  echo "Telegram: wykryty chat ID = ${TELEGRAM_CHAT_ID} (wpisz go jako TELEGRAM_CHAT_ID, żeby nie zależeć od wykrywania)"
fi
MSG="${MSG:0:4000}"   # limit Telegrama to 4096 znaków
RESP=$(curl -sS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
  --data-urlencode "text=${MSG}" \
  --data-urlencode "disable_web_page_preview=true")
if [[ "$RESP" == *'"ok":true'* ]]; then echo "Telegram: wysłano"; else echo "Telegram: błąd: ${RESP:0:300}" >&2; exit 1; fi
