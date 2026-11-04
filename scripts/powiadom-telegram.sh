#!/usr/bin/env bash
# Wysyła wiadomość na Telegram przez Bot API.
# Wymaga zmiennych środowiskowych: TELEGRAM_BOT_TOKEN i TELEGRAM_CHAT_ID.
# Użycie: scripts/powiadom-telegram.sh "treść wiadomości"
set -euo pipefail
MSG="${1:?Podaj treść wiadomości}"
if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
  echo "Telegram: brak TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID – pomijam wysyłkę." >&2
  exit 0
fi
MSG="${MSG:0:4000}"   # limit Telegrama to 4096 znaków
RESP=$(curl -sS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
  --data-urlencode "text=${MSG}" \
  --data-urlencode "disable_web_page_preview=true")
if [[ "$RESP" == *'"ok":true'* ]]; then echo "Telegram: wysłano"; else echo "Telegram: błąd: ${RESP:0:300}" >&2; exit 1; fi
