#!/usr/bin/env bash
# Po zalogowaniu (README.md, krok 1) – przygotowuje wartość zmiennej AGY_AUTH do wklejenia w ustawieniach środowiska.
# Plik trafia do AGY_AUTH-do-skopiowania.txt w katalogu repozytorium (ignorowany – nie idzie do archiwum).
# Po wklejeniu w ustawienia: rm AGY_AUTH-do-skopiowania.txt
set -euo pipefail
TOKEN="$HOME/.gemini/antigravity-cli/antigravity-oauth-token"
[ -s "$TOKEN" ] || { echo "Brak logowania – najpierw zaloguj (README.md)." >&2; exit 1; }
CEL="$(cd "$(dirname "$0")/../.." && pwd)/AGY_AUTH-do-skopiowania.txt"
base64 -w0 "$TOKEN" > "$CEL"; chmod 600 "$CEL"
echo "Gotowe: $CEL ($(wc -c < "$CEL") znaków) – całą zawartość wkleić jako zmienną AGY_AUTH."
