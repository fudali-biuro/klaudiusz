# Antigravity CLI (`agy`) – obrazy z konta Google zamiast płatnego API

Oficjalne narzędzie Google (następca Gemini CLI). Zalogowane kontem **biuro@fudali.com.pl** (Workspace) –
Google przydzielił mu **„Antigravity Starter Quota”** (darmowy limit odnawiany co tydzień; Workspace nie liczy się jako Pro/Ultra).
Ma wbudowane generowanie obrazów (Nano Banana) – także edycję zdjęcia produktu w nowej scenie. Wynik ~1K (np. 896×1200).

## Na co dzień
- **Sceny produktów:** `python3 scripts/grafika/scena.py --zdjecie <plik/URL> --opis "<scena EN>" --wyjscie <plik.jpg>`
  (najpierw agy, płatny zapas OpenRouter tylko gdy agy zawiedzie; `--bez-api` = bez zapasu). ~1 min na obrazek.
- **Ręcznie:** `scripts/antigravity/start.sh`, potem w folderze `~/.cache/fudali-agy`:
  `agy -p "<polecenie>" --sandbox --mode accept-edits --output-format json` → obraz ląduje w
  `~/.gemini/antigravity-cli/brain/<conversation_id>/*.jpg`. **Nie używać `--dangerously-skip-permissions`.**

## Po restarcie maszyny
Maszyna jest czyszczona, więc `start.sh` (wołany sam przez `scena.py`) instaluje agy i odtwarza logowanie
ze zmiennej środowiskowej **`AGY_AUTH`** (ustawienia środowiska → Edit → zmienne). Nic nie trzeba klikać.

## Gdy logowanie wygaśnie (błąd „brak logowania” / „AGY_AUTH uszkodzony”)
Tylko w rozmowie z Pablo na żywo (nie w zadaniu automatycznym) i **w jednej turze** – maszyna gubi okno logowania między wiadomościami:
1. `tmux new-session -d -s agy "agy"` → Enter (Google OAuth) → wyciągnij link z `tmux capture-pane`.
2. Link do Pablo przez **AskUserQuestion** (kod wkleja w pole „Other”) – nie kończ tury, nie zamykaj tmux.
3. `tmux send-keys -t agy -l '<kod>'` + Enter → ekrany powitalne: **odznacz zgodę na zbieranie danych**, zaufaj folderowi.
4. `scripts/antigravity/zapisz-logowanie.sh` → Pablo kopiuje zawartość `AGY_AUTH-do-skopiowania.txt` do zmiennej `AGY_AUTH`
   → potem `rm AGY_AUTH-do-skopiowania.txt` (plik jest poza archiwum, ale nie zostawiamy go).
