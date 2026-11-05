# Sesje zespołu – Klaudiusz + 7 subczatów

**Zasada (polecenie Pablo, 04.11.2026):** nie ma jednego wielkiego procesu. Klaudiusz ma swoją sesję główną
(„🧠 Klaudiusz”), a **każdy pracownik ma własną, stałą sesję nazwaną jego imieniem** – tam przychodzą jego zmiany
(budzenie o stałych godzinach z `zespol/godziny.json` – jedyne miejsce z godzinami) i wiadomości. Wszystkie sesje: **średni wysiłek (medium)**. Rejestr: `zespol/sesje.json`
(`python3 scripts/sesje.py pokaz`). Biuro pokazuje przy każdym pracowniku link do jego sesji (do poprawek).

```
Pablo ── czat w biurze (biuro-fudali.vercel.app) ──► 📨 listonosz (zapis + budzik) ──► 📥 Skrzynka ──► stała sesja adresata
                                                     (zespol/zadania/klaudiusz-czat.md)                (pracownik albo Klaudiusz)
                                   🧠 Klaudiusz (sesja główna) – zleca pracę, zbiera meldunki
                                                                           │ send_message
          ┌──────────┬──────────┬──────────┬──────────┬──────────┬────────┴─┐
       🔭 Mietek  🔑 Kuba   🧭 Bartek   📣 Ola    🎨 Zosia  🤝 Marek  🌍 Greta     ← każdy we własnej sesji,
          │ ⏰ zmiany wg zespol/godziny.json (rano ~5:00, w południe ~12:00)      każdy budzi się tylko na swoje zmiany
          └── odpowiedzi do Pablo: scripts/czat.py napisz <id> "…"  → okno czatu w biurze
              koniec pracy: meldunek do Klaudiusza (send_message)    → Klaudiusz decyduje, co dalej
```

## Uruchomienie zespołu (robi Klaudiusz w swojej sesji – raz; potem tylko gdy czegoś brakuje)

1. `git pull --rebase origin main`. Zarejestruj siebie: `mcp__claude-code-remote__get_session` (bez session_id) → Twoje ID →
   `python3 scripts/sesje.py zapisz klaudiusz <Twoje session_id>` (zanim utworzysz pracowników – ich prompty zawierają Twoje ID).
   `python3 scripts/sesje.py pokaz` – sprawdź, kto już ma sesję (nie twórz duplikatów).
2. Dla każdego pracownika bez sesji (`konkurencja`, `slowa-kluczowe`, `pozycjonowanie`, `marketing`, `grafika`,
   `sprzedaz`, `rynki-zagraniczne`):
   - `python3 scripts/sesje.py parametry <id>` → JSON;
   - `mcp__claude-code-remote__create_session` z polami z JSON-a: `title`, `source_url`, `outcome_branch` (`main`),
     `append_system_prompt`, `prompt`, `tags` (bez `environment_id` – ta sama chmura; bez `model` – ten sam model);
   - `python3 scripts/sesje.py zapisz <id> <session_id>`.
3. Zadania automatyczne każdego pracownika: `python3 scripts/godziny.py plan` → każdą pozycję wykonaj narzędziem z planu
   (`create_trigger` / `update_trigger` z podanymi argumentami), potem komendę z „potem” (`python3 scripts/sesje.py zadanie <id> <klucz> <trig_id>`).
   Pracownik z godzinami w `zespol/godziny.json` dostaje JEDNO zadanie „zmiany” (klucz `zmiana`). Czatu („📨 listonosz”, `zespol/zadania/klaudiusz-czat.md`)
   i „📥 Skrzynek” (`scripts/sesje.py skrzynka <id>`) plan nie dotyka – mają własną procedurę; zadania czatu nie twórz ponownie.
4. **Stare wspólne zadania – wyłącz** (`update_trigger enabled=false`, NIE kasuj – skasowanie usuwa historię przebiegów),
   dopiero gdy nowe zadania pracowników są utworzone:
   - `trig_01PkJMYcfanpMvD8Yo8L4vHx` – „Monitoring konkurencji IG/TikTok + słowa kluczowe (co godzinę)” → Mietek + Kuba,
   - `trig_01HuWfV746T2VFYdA5NSw42c` – „Raport konkurencji FUDALI (8:00)” (była przypięta do zarchiwizowanej sesji) → Mietek,
   - `trig_018KMyuLw6yaTP2LSwz12KMj` – „Marketing i SEO FUDALI – plan tygodnia (Ola + Bartek)” → Bartek + Ola,
   - `trig_01CzM5g59fBgRH7dczzB9nzV` – „Pinterest FUDALI: codzienny research zasięgu” → Ola.
5. Zapisz `zespol/sesje.json` na main; `python3 scripts/status.py klaudiusz gotowe "Zespół na stanowiskach: 7 sesji, N zadań"`.
6. Poczekaj na meldunki pracowników (każdy odpisze jednym zdaniem). Napisz Pablo w czacie
   (`python3 scripts/czat.py napisz klaudiusz "…"`): kto jest na stanowisku i jakie ma zadania – krótko, po ludzku.

## Na co dzień
- **Zlecenie dla pracownika:** `send_message(session_id=<z sesje.json>, message="…")` – konkretnie: co, na kiedy, gdzie wynik.
- **Wiadomość od Pablo z czatu:** listonosz zapisuje ją i budzi „📥 Skrzynkę” adresata; adresat robi `scripts/czat.py skrzynka <id>`
  i odpowiada (`zespol/zadania/klaudiusz-czat.md`). Nowa sesja pracownika = utwórz też jego skrzynkę (`scripts/sesje.py skrzynka <id>`).
- **Pracownik skończył:** melduje się Tobie (send_message). Ty decydujesz, co dalej (np. pomysły Mietka → Ola → Zosia).
- **Sesja pracownika padła / zarchiwizowana:** `get_session`; w razie potrzeby `unarchive_session` albo nowa sesja
  (pkt 2), `sesje.py zapisz` i **przepnij jego zadania** (`update_trigger` nie zmienia sesji → stare wyłącz, `sesje.py usun-zadanie`,
  potem `godziny.py plan <id>` utworzy nowe).
- **Nowy obowiązek:** nowy plik `zespol/zadania/<id>-<klucz>.md` (nagłówek `nazwa`, `kiedy`) – pracownik zrobi go na najbliższej zmianie,
  nowe zadanie automatyczne nie jest potrzebne (chyba że pracownik nie ma godzin – wtedy `godziny.py ustaw` + `plan`).
- **Zmiana godzin (prośba Pablo):** `python3 scripts/godziny.py ustaw <id> 6:00 14:00` → `python3 scripts/godziny.py plan <id>` →
  wykonaj kroki → zapis na main → jedno zdanie do Pablo w czacie. Szczegóły: AGENTS.md, „Zmiany pracy”.
- Nazwy sesji = imiona pracowników (`scripts/sesje.py tytul <id>`) – nie zmieniaj ich, Pablo po nich nawiguje.

## Wysiłek (effort)
Wszystkie sesje zespołu działają na **medium**. Ustawienie domyślne jest w `.claude/settings.json` (`"effortLevel": "medium"`).
Po utworzeniu sesji sprawdź `get_session` → `external_metadata.effort_level`; jeśli jest inny niż `medium`, zgłoś to w czacie Pablo
jedną prośbą (sam nie przełączysz – robi się to jednym kliknięciem w sesji: wybór modelu → Effort → Medium).
