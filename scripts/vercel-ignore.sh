#!/bin/sh
# Czy Vercel ma przebudować biuro? exit 1 = buduj, exit 0 = pomiń.
# Limit Vercel (plan darmowy) to ok. 100 przebudów na dobę, a zespół zapisuje setki zmian dziennie.
# Kod strony (biuro/, api/, konfiguracja) → zawsze buduj. Same dane → buduj najwyżej co 20 minut
# (czat i biblioteka akceptacji i tak biorą świeże dane na żywo z /api/na-zywo).
P="$VERCEL_GIT_PREVIOUS_SHA"
[ -z "$P" ] && exit 1
git cat-file -e "$P^{commit}" 2>/dev/null || git fetch -q --deepen=500 origin 2>/dev/null
git cat-file -e "$P^{commit}" 2>/dev/null || exit 1
git diff --quiet "$P" HEAD -- biuro api package.json package-lock.json vercel.json scripts/vercel-ignore.sh || exit 1
git diff --quiet "$P" HEAD -- zespol marketing raporty monitoring/social slowa-kluczowe konkurencja seo grafika sprzedaz rynki-zagraniczne AGENTS.md && exit 0
T0=$(git log -1 --format=%ct "$P"); T1=$(git log -1 --format=%ct HEAD)
[ $((T1 - T0)) -ge 1200 ] && exit 1
echo "Pomijam: dane zmienione, ale ostatnia przebudowa < 20 min temu"
exit 0
