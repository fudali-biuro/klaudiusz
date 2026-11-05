# Obowiązki zespołu – każdy pracownik ma swoje

Jeden plik = jeden obowiązek jednego pracownika: `<id-pracownika>-<klucz>.md`.
Nagłówek: `nazwa`, `kiedy` (na której zmianie), opcjonalnie `kolejnosc` (kolejność na zmianie, domyślnie 50) i `wylaczone: tak`.

**Godzin tu nie ma** – pracownik budzi się na swoje zmiany wg **`zespol/godziny.json`** (jedyne miejsce z godzinami).
Na zmianie uruchamia `python3 scripts/godziny.py zmiana <id>`, a skrypt wybiera obowiązki wg pola `kiedy`:

| `kiedy` | Znaczenie |
|---|---|
| `kazda` | na każdej zmianie |
| `rano` | na pierwszej (porannej) zmianie dnia |
| `ostatnia` | na ostatniej zmianie dnia |
| `pozniej` | na każdej zmianie oprócz pierwszej |
| `wezwanie` | bez zegarka – osobne zadanie budzone z zewnątrz (np. czat z biura) |
| `rano pon` | jak wyżej, ale tylko w podane dni (`pon`, `wt`, `śr`, `czw`, `pt`, `sob`, `nd`, zakresy `pon-pt`) |

| Plik | Pracownik | `kiedy` |
|---|---|---|
| `klaudiusz-czat.md` | 🧠 Klaudiusz | wezwanie – wiadomość z czatu w biurze |
| `konkurencja-monitoring.md` | 🔭 Mietek | kazda |
| `konkurencja-raport.md` | 🔭 Mietek | rano (Pablo ma raport gotowy rano) |
| `pozycjonowanie-trendy.md` | 🧭 Bartek | rano pon |
| `slowa-kluczowe-pomiar.md` | 🔑 Kuba | kazda (na ostatniej zmianie dnia + podsumowanie dnia) |
| `marketing-plan-tygodnia.md` | 📣 Ola | rano pon (po trendach Bartka) |
| `marketing-buffer-posty.md` | 📣 Ola | kazda (rano nowy post, w ciągu dnia odpowiedzi szefa) |
| `marketing-pinterest.md` | 📣 Ola | rano |

Przegląd: `python3 scripts/godziny.py pokaz`. Zosia, Marek i Greta nie mają stałych godzin – pracują na zlecenie
(Klaudiusz, Ola, Pablo z czatu). Gdy dostaną godziny (`godziny.py ustaw`), dopisz im tu obowiązki – inaczej obudzą się na darmo.
