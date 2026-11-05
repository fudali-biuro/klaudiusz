#!/usr/bin/env bash
# Antigravity CLI (agy) – instalacja + przywrócenie logowania na świeżej maszynie.
# Maszyna sesji jest czyszczona po każdym wyłączeniu, więc ten skrypt odpala się sam
# (scripts/grafika/scena.py) albo ręcznie przed użyciem agy:  scripts/antigravity/start.sh
# Trwa kilkanaście sekund przy pierwszym razie w sesji, potem ~0 s.
# Logowanie: zmienna środowiskowa AGY_AUTH (base64 pliku antigravity-oauth-token), tworzona przez
# scripts/antigravity/zapisz-logowanie.sh. Nigdy nie zapisujemy jej do repozytorium.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
KAT="$HOME/.gemini/antigravity-cli"
PRACA="${AGY_PRACA:-$HOME/.cache/fudali-agy}"   # folder roboczy agy (zdjęcia referencyjne)
mkdir -p "$HOME/.cache" "$KAT/cache" "$PRACA"

# 1) Program
if ! command -v agy >/dev/null 2>&1; then
  tmp=$(mktemp -d)
  curl -fsSL https://antigravity.google/cli/install.sh -o "$tmp/install.sh" && bash "$tmp/install.sh" >/dev/null 2>&1
  rm -rf "$tmp"
  command -v agy >/dev/null 2>&1 || { echo "agy: instalacja nie wyszła" >&2; exit 1; }
fi

# 2) Logowanie z AGY_AUTH (tylko gdy maszyna nie ma własnego, świeższego)
if [ ! -s "$KAT/antigravity-oauth-token" ]; then
  if [ -n "${AGY_AUTH:-}" ]; then
    if echo "$AGY_AUTH" | base64 -d > "$KAT/antigravity-oauth-token.tmp" 2>/dev/null \
       && python3 -c "import json,sys; json.load(open(sys.argv[1]))['token']['refresh_token']" "$KAT/antigravity-oauth-token.tmp" 2>/dev/null; then
      mv "$KAT/antigravity-oauth-token.tmp" "$KAT/antigravity-oauth-token"; chmod 600 "$KAT/antigravity-oauth-token"
    else
      rm -f "$KAT/antigravity-oauth-token.tmp"; echo "agy: AGY_AUTH uszkodzony – trzeba zalogować się ponownie (scripts/antigravity/README.md)" >&2; exit 2
    fi
  else
    echo "agy: brak logowania – brak zmiennej AGY_AUTH (scripts/antigravity/README.md)" >&2; exit 2
  fi
fi

# 3) Bez ekranów powitalnych + zaufany folder roboczy
[ -s "$KAT/cache/onboarding.json" ] || echo '{"consumerOnboardingComplete": true, "enterpriseOnboardingComplete": false, "onboardingComplete": true}' > "$KAT/cache/onboarding.json"
python3 - "$KAT/settings.json" "$PRACA" <<'PY'
import json, os, sys
p, praca = sys.argv[1], sys.argv[2]
s = json.load(open(p)) if os.path.exists(p) else {}
t = s.setdefault("trustedWorkspaces", [])
if praca not in t:
    t.append(praca); json.dump(s, open(p, "w"), indent=2)
PY
echo "agy: gotowe ($(agy --version 2>/dev/null), folder roboczy $PRACA)"
