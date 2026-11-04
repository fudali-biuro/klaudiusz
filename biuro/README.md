# 🏢 Biuro FUDALI – wirtualne biuro Klaudiusza (Vercel)

Pikselowe biuro w stylu „Gather”: Klaudiusz (mózg) w środku, 7 pracowników przy biurkach, Pablo chodzi po biurze.
Widać, kto **pracuje** (stuka w klawiaturę), kto **skończył** (✓), a kto **czegoś chce od szefa** (podniesiona ręka i „!”).
Klik w pracownika → panel: co teraz robi, prośby do Pablo, dziennik, ostatnie wyniki (raporty do przeczytania), karta pracownika.

## Skąd dane
Strona jest budowana z repozytorium przy każdym zapisie na `main` (`node biuro/build.mjs` → `biuro/dist/`):
- `zespol/*.md` – karty pracowników (nagłówek: imię, rola, kolor, fryzura, które pliki pokazywać jako wyniki),
- `zespol/status/*.json` – statusy (aktualizuje `scripts/status.py`),
- pliki wyników (np. `raporty/*-konkurencja.md`) – 6 najnowszych na wzorzec, do podglądu w biurze.

Strona sama sprawdza nowe dane co 5 minut. Vercel pomija budowanie, gdy zmiana nie dotyczy biura ani wyników (`ignoreCommand` w `vercel.json`).

## Uruchomienie na Vercel (jednorazowo, robi Pablo – ok. 5 minut)
1. Wejdź na **vercel.com** i zaloguj się kontem GitHub (tym, które ma dostęp do archiwum Klaudiusza).
2. **Add New… → Project** → przy repozytorium **`fudali-biuro/klaudiusz`** kliknij **Import**.
   Ustawień nie zmieniaj (wszystko jest w `vercel.json`) → **Deploy**.
3. **Zabezpieczenie (ważne!)**: w projekcie **Settings → Deployment Protection** → **Vercel Authentication: włącz**,
   zakres ustaw na **All Deployments** (dostępne też na darmowym planie) → **Save**.
   Od teraz stronę zobaczy tylko ktoś zalogowany na Vercel z dostępem do tego projektu; reszta świata dostaje ekran logowania.
4. Link do biura: **Settings → Domains** (np. `klaudiusz-xxx.vercel.app`) – zapisz w zakładkach telefonu.

Chcesz dać dostęp współpracownikowi? Zaproś go do zespołu na Vercel (Settings → Members) – bez tego nie wejdzie.

## Sterowanie
- myszka / palec: klik w podłogę – Pablo idzie; klik w osobę – rozmowa (panel),
- klawiatura: WASD / strzałki – chodzenie, **E** – rozmowa z osobą obok, **Esc** – zamknij panel,
- tablica w open space i przycisk „🙋 Prośby do Ciebie” – wszystkie prośby zespołu w jednym miejscu.

## Podgląd lokalny (dla Klaudiusza)
```bash
node biuro/build.mjs && python3 -m http.server 8765 -d biuro/dist
```
