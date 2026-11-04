# Konkurencja – źródło prawdy

**Ten folder jest jedynym źródłem prawdy o konkurencji** dla wszystkich automatyzacji:
codziennego raportu (`instrukcja-raportu.md`) i godzinnego monitoringu social media
(`instrukcja-monitoringu.md`).

- `firmy/<slug>.md` – **jeden plik na konkurenta**. Nagłówek (front matter) zawiera dane, z których
  korzystają skrypty: `www`, `instagram`, `tiktok` (same nazwy kont, bez @), `facebook`, `priorytet`
  (A – bezpośredni, B – częściowy, C – rynek/ceny referencyjne), `aktywny_monitoring` (tak/nie).
  Poniżej: notatki i „Dziennik obserwacji” dopisywany automatycznie.
- `konkurenci.md` – tabela-indeks (generowana: `python3 scripts/indeks_konkurencji.py`).

**Dodanie konkurenta:** skopiuj dowolny plik z `firmy/`, zmień nazwę i dane. Tyle – od następnej godziny
monitoring go obejmie, a raport dzienny weźmie go pod uwagę.
