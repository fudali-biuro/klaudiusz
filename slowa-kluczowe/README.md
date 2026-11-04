# Słowa kluczowe FUDALI

- `slowa-kluczowe.csv` – **lista śledzonych fraz** (źródło prawdy). Kolumny: `fraza`, `grupa`,
  `znaczenie_biznesowe` (wysokie/srednie/niskie – jak bardzo fraza pasuje do oferty FUDALI). Edytuj śmiało.
- `historia.csv` – godzinne pomiary (dopisywane automatycznie przez `scripts/slowa_kluczowe.py`).
- `kandydaci.md` – nowe frazy wykryte w podpowiedziach Google i postach konkurencji, do decyzji czy dodać.
- `podsumowania/RRRR-MM-DD.md` – godzinne podsumowania: które frazy są ważne, a które nie, i dlaczego.

## Skąd ocena ważności (0–100)
Skrypt liczy sygnały, a Claude je interpretuje:
1. **Popyt (Google Autocomplete, PL)** – czy fraza i jej rozwinięcia pojawiają się w podpowiedziach
   (podpowiedzi = realne, częste wyszukiwania). Darmowe, bez klucza.
2. **Aktywność konkurencji** – ile razy fraza / jej hashtag pojawia się w postach konkurencji (24 h i 7 dni)
   z monitoringu Instagram/TikTok.
3. **Zaangażowanie** – średnie polubienia+komentarze postów konkurencji z daną frazą.
4. **Dopasowanie do oferty** – kolumna `znaczenie_biznesowe`.

Gdy podłączysz Ahrefs/Google Search Console, dojdą wolumeny wyszukiwań i pozycje fudali.com.pl.
