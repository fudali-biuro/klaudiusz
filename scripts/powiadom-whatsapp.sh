#!/usr/bin/env bash
# Wysyła wiadomość WhatsApp przez CallMeBot (https://www.callmebot.com/blog/free-api-whatsapp-messages/).
# Wymaga zmiennych środowiskowych: WHATSAPP_PHONE (np. +48600111222) i CALLMEBOT_APIKEY.
# Użycie: scripts/powiadom-whatsapp.sh "treść wiadomości"
set -euo pipefail
MSG="${1:?Podaj treść wiadomości}"
if [[ -z "${WHATSAPP_PHONE:-}" || -z "${CALLMEBOT_APIKEY:-}" ]]; then
  echo "WhatsApp: brak WHATSAPP_PHONE/CALLMEBOT_APIKEY – pomijam wysyłkę." >&2
  exit 0
fi
# CallMeBot ma limit długości – przycinamy do ~1500 znaków
MSG="${MSG:0:1500}"
HTTP=$(curl -sS -o /tmp/callmebot.out -w "%{http_code}" -G "https://api.callmebot.com/whatsapp.php" \
  --data-urlencode "phone=${WHATSAPP_PHONE}" \
  --data-urlencode "text=${MSG}" \
  --data-urlencode "apikey=${CALLMEBOT_APIKEY}")
echo "WhatsApp: HTTP ${HTTP}"; cat /tmp/callmebot.out | head -c 300; echo
[[ "$HTTP" == "200" ]]
