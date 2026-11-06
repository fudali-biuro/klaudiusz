---
nazwa: "Nowe zdjęcia od Pablo → biblioteka"
kiedy: "kazda"
kolejnosc: 5
---
# Nowe prawdziwe zdjęcia od Pablo (strona 📸 Zdjęcia w biurze)

1. `python3 scripts/zdjecia.py pobierz --z-sieci` – pobiera do `marketing/biblioteka-zdjec/` wszystko, co Pablo wgrał od ostatniego razu
   (gdy brak `zrodlo.txt`: JSON z https://biuro-fudali.vercel.app/api/zdjecia przez konektor Vercel `web_fetch_vercel_url` → na wejście skryptu).
2. Każde nowe zdjęcie obejrzyj (Read) i opisz: `python3 scripts/zdjecia.py opisz <plik> --opis "…" --tagi a,b,c [--produkt lezak]`
   (tagi: miejsce, pora roku, kolor, światło – po nich dobieramy tło do produktu).
3. Jeśli nic nowego – nic nie rób, nie meldujesz się.
