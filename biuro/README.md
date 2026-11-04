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

## Uruchomienie na Vercel (jednorazowo)
Najlepiej: Klaudiusz robi to sam przez konektor Vercel (w sesji, która go widzi). Gdyby trzeba było ręcznie – gotowe linki:
1. **Utworzenie projektu z archiwum:** https://vercel.com/new/import?s=https://github.com/fudali-biuro/klaudiusz → „Deploy”
   (ustawienia są w `vercel.json`, nic nie trzeba zmieniać).
2. **Zabezpieczenie (ważne):** https://vercel.com/d?to=%2F%5Bteam%5D%2F%5Bproject%5D%2Fsettings%2Fdeployment-protection
   → Vercel Authentication **włączone**, zakres **All Deployments** (działa też na darmowym planie).
   Stronę zobaczy tylko ktoś zalogowany na Vercel z dostępem do projektu.
3. Link do biura: https://vercel.com/d?to=%2F%5Bteam%5D%2F%5Bproject%5D%2Fsettings%2Fdomains (np. `klaudiusz-xxx.vercel.app`).

Dostęp dla współpracownika = zaproszenie do zespołu na Vercel: https://vercel.com/d?to=%2Fteams%2F%5Bteam%5D%2Fsettings%2Fmembers

## Sterowanie
- myszka / palec: klik w podłogę – Pablo idzie; klik w osobę – rozmowa (panel),
- klawiatura: WASD / strzałki – chodzenie, **E** – rozmowa z osobą obok, **Esc** – zamknij panel,
- tablica w open space i przycisk „🙋 Prośby do Ciebie” – wszystkie prośby zespołu w jednym miejscu.

## Podgląd lokalny (dla Klaudiusza)
```bash
node biuro/build.mjs && python3 -m http.server 8765 -d biuro/dist
```
