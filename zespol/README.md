# Zespół Klaudiusza – wirtualni pracownicy FUDALI

**Klaudiusz (`AGENTS.md`) jest mózgiem operacji**: zna całą firmę, rozdziela pracę, pilnuje jakości i rozmawia z Pablo.
Pracownicy to wyspecjalizowane role. Każdy ma swoją **kartę** (`zespol/<id>.md`) – kim jest, za co odpowiada,
jakich skryptów używa, co oddaje – i swój **status** (`zespol/status/<id>.json`), który widać w wirtualnym biurze (`biuro/`).

Gdy sesja Claude wykonuje pracę danej roli, **wciela się w tego pracownika**: czyta jego kartę i trzyma się jej zasad,
a na początku i końcu pracy aktualizuje jego status.

| # | Pracownik | Rola | Karta | Stan wdrożenia |
|---|---|---|---|---|
| 🧠 | **Klaudiusz** | mózg operacji, koordynator | `AGENTS.md`, `zespol/klaudiusz.md` | ✅ aktywny |
| 1 | 🔭 **Mietek „Lornetka”** | śledzenie konkurencji | `zespol/konkurencja.md` | ✅ aktywny (raport dzienny + monitoring godzinny) |
| 2 | 📣 **Ola „Megafon”** | marketing (+ Pinterest/Etsy) | `zespol/marketing.md` | ✅ aktywna (posty, kampanie, szkice w Metricool) |
| 3 | 🧭 **Bartek „Kompas”** | pozycjonowanie (SEO) + Google Trends | `zespol/pozycjonowanie.md` | ✅ aktywny (trendy co tydzień) |
| 4 | 🎨 **Zosia „Pędzel”** | grafika | `zespol/grafika.md` | ✅ aktywna (produkty w nowych scenach) |
| 5 | 🔑 **Kuba „Klucznik”** | słowa kluczowe | `zespol/slowa-kluczowe.md` | ✅ aktywny (pomiar co godzinę) |
| 6 | 🤝 **Marek „Domykacz”** | sprzedaż | `zespol/sprzedaz.md` | 🧩 makieta |
| 7 | 🌍 **Greta „Paszport”** | rynki zagraniczne | `zespol/rynki-zagraniczne.md` | 🧩 makieta |

**Makieta** = rola jest zaprojektowana (zadania, planowane skrypty, potrzebne dostępy), ale nie ma jeszcze
automatów. Wdrożenie = napisanie skryptów z sekcji „Planowane narzędzia”, dopisanie zadania automatycznego
w `AGENTS.md` i zmiana `wdrozenie: makieta` → `aktywny` w nagłówku karty.

## Jak przepływa praca
```
            Pablo (szef)
                │  polecenia, odpowiedzi na prośby
                ▼
        🧠 Klaudiusz (mózg) ──────────────► raporty, powiadomienia Telegram
   ┌──────┬──────┼──────┬──────┬──────┬──────┐
Mietek   Kuba   Ola   Bartek  Zosia  Marek  Greta
(rywale) (frazy)(posty) (SEO) (grafika)(oferty)(eksport)
   └──► pomysły ──► Ola ──► zlecenia ──► Zosia
        frazy ─────► Bartek, Ola, Greta
```

## Statusy (`zespol/status/<id>.json`)
Aktualizuje je **wyłącznie** skrypt `scripts/status.py` (nie edytuj ręcznie):

```bash
python3 scripts/status.py <id> pracuje "Co teraz robię"           # zaczynam
python3 scripts/status.py <id> gotowe  "Co zrobiłem (1 zdanie)"    # skończyłem
python3 scripts/status.py <id> czeka   "Na co czekam" --prosba "Pablo, potrzebuję …"   # potrzebuję szefa
python3 scripts/status.py <id> --zalatwione                        # Pablo odpowiedział – usuń prośby
python3 scripts/status.py <id> blad    "Co nie działa"
```

| Stan | Znaczenie | W biurze |
|---|---|---|
| `pracuje` | coś teraz robi | stuka w klawiaturę, dymek „…” |
| `gotowe` | skończył zadanie, wynik w archiwum | zielony ✓ |
| `czeka` | potrzebuje czegoś od Pablo (prośba) | czerwony „!” |
| `wolne` | nic do roboty / czeka na zlecenie | „zZ” |
| `blad` | coś się wysypało | czerwony ✗ |

`pracuje` dłużej niż 3 h bez aktualizacji biuro pokazuje jako „cisza” (sesja mogła się urwać).
Identyfikatory: `klaudiusz`, `konkurencja`, `marketing`, `pozycjonowanie`, `grafika`, `slowa-kluczowe`, `sprzedaz`, `rynki-zagraniczne`.

## Nagłówek karty (czyta go biuro)
```
---
id: konkurencja            # = nazwa pliku i statusu
imie: Mietek
przydomek: Lornetka
rola: Śledzenie konkurencji
emoji: 🔭
kolor: "#c0392b"           # kolor koszulki w biurze
wlosy: "#3b2a1a"           # kolor włosów
fryzura: krotkie           # krotkie | dlugie | kok | czapka | lysy | kucyk
wdrozenie: aktywny         # aktywny | makieta
wyniki: raporty/*-konkurencja.md; monitoring/social/*.md   # pliki pokazywane w biurze (najnowsze)
---
```
