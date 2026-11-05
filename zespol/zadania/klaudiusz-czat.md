---
nazwa: "📨 Czat z biura – listonosz"
kiedy: "wezwanie"
wylaczone: tak
---
# 📨 Czat z biura – jak wiadomość od Pablo dociera do pracownika

```
okno czatu w biurze ─► api/czat.js ─► 📨 listonosz (krótka sesja, bez powiadomień) ─► archiwum (zespol/czat/<id>/)
                                              │ nastawia budzik (+90 s)
                                              ▼
                                   📥 Skrzynka adresata ─► budzi STAŁĄ sesję pracownika ─► czat.py skrzynka <id> ─► praca
                                                                                         └► czat.py napisz <id> "…" ─► okno czatu
```

1. **Listonosz** – zadanie `📨 Czat z biura – listonosz` (`zespol/sesje.json` → `klaudiusz.zadania.czat`). Serwer biura budzi je
   przy każdej wiadomości (tokenem API wklejonym raz w biurze). Każde wywołanie to osobna, krótka sesja (widać ją tylko w historii
   zadania, nie na liście sesji). Robi dwie rzeczy: `scripts/czat.py przyjmij` (zapis wiadomości + pobranie załączników + transkrypcja
   nagrań) i `update_trigger(<skrzynka adresata>, run_once_at=+90 s)`. Sesje odpalane z zewnątrz nie mogą pisać do innych sesji –
   dlatego budzik, a nie send_message.
2. **Skrzynka** – zadanie `📥 Skrzynka – <pracownik>` przypięte do stałej sesji każdego pracownika i Klaudiusza
   (`zespol/sesje.json` → `<id>.zadania.skrzynka`, prompt: `python3 scripts/sesje.py skrzynka <id>`). Bez stałej godziny –
   dzwoni tylko, gdy listonosz nastawi budzik. Pracownik robi `python3 scripts/czat.py skrzynka <id>` (wiadomości od Pablo po jego
   ostatniej odpowiedzi), wykonuje i odpisuje `python3 scripts/czat.py napisz <id> "…"`.

Czas: wiadomość widać w archiwum po ~1 min, pracownik zaczyna po ~2–3 min. Kilka wiadomości naraz = jedno obudzenie (skrzynka pokaże wszystkie).

Odtworzenie skrzynki pracownika (np. nowa sesja): `python3 scripts/sesje.py skrzynka <id>` → `create_trigger(name, prompt,
persistent_session_id)` bez cron → `python3 scripts/sesje.py zadanie <id> skrzynka <trig_id>`.
Odtworzenie listonosza: `create_trigger(create_new_session_on_fire=true, notifications={})` z promptem jak w obecnym zadaniu →
`python3 scripts/sesje.py zadanie klaudiusz czat <trig_id>` → Pablo wkleja w biurze nowy token API.
