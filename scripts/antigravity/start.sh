#!/usr/bin/env bash
# Antigravity CLI (agy) – instalacja + przywrócenie logowania na świeżej maszynie.
# Maszyna sesji jest czyszczona po każdym wyłączeniu, więc ten skrypt odpala się sam
# (scripts/grafika/scena.py) albo ręcznie przed użyciem agy:  scripts/antigravity/start.sh
# Trwa kilkanaście sekund przy pierwszym razie w sesji, potem ~0 s.
# Logowanie trzymamy w zmiennej środowiskowej AGY_AUTH (base64 z tar.gz plików logowania),
# którą tworzy scripts/antigravity/zapisz-logowanie.sh. Nigdy nie zapisujemy jej do repozytorium.
set -uo pipefail
mkdir -p "$HOME/.cache"
export PATH="$HOME/.local/bin:$PATH"

# 1) Program
if ! command -v agy >/dev/null 2>&1; then
  tmp=$(mktemp -d)
  curl -fsSL https://antigravity.google/cli/install.sh -o "$tmp/install.sh" && bash "$tmp/install.sh" >/dev/null 2>&1
  rm -rf "$tmp"
  command -v agy >/dev/null 2>&1 || { echo "agy: instalacja nie wyszła"; exit 1; }
fi

# 2) Logowanie (z AGY_AUTH, jeśli maszyna jeszcze go nie ma)
if [ -n "${AGY_AUTH:-}" ] && [ ! -f "$HOME/.cache/antigravity-auth-ok" ]; then
  if echo "$AGY_AUTH" | base64 -d 2>/dev/null | tar -xzf - -C "$HOME" 2>/dev/null; then
    touch "$HOME/.cache/antigravity-auth-ok"
  else
    echo "agy: AGY_AUTH uszkodzony – trzeba zalogować się ponownie"
  fi
fi
echo "agy: gotowe ($(agy --version 2>/dev/null))"
