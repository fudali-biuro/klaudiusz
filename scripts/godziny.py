#!/usr/bin/env python3
"""Godziny pracy zespołu – JEDNO miejsce: zespol/godziny.json (czas polski).

Pracownicy nie pracują 24/7 (oszczędzamy kredyty): każdy budzi się sam tylko na swoje „zmiany” (np. 5:05 i 12:05)
i wtedy robi obowiązki z plików zespol/zadania/<id>-*.md (pole `kiedy` w nagłówku: kazda | rano | ostatnia | pozniej
| wezwanie, opcjonalnie z dniem, np. "rano pon"). Każdy pracownik ma JEDNO zadanie automatyczne „zmiany” (klucz `zmiana`
w zespol/sesje.json) – zmiana godzin = jedna linia w godziny.json + jedno update_trigger.

  python3 scripts/godziny.py pokaz                                   # godziny i obowiązki wszystkich
  python3 scripts/godziny.py ustaw <id> 6:00 14:00 [--dni pon-pt]    # nowe godziny pracownika
  python3 scripts/godziny.py ustaw <id> brak                         # bez stałych godzin (tylko na zlecenie)
  python3 scripts/godziny.py ustaw wszyscy 6:00 14:00                # wszyscy naraz (kolejność i odstępy zostają)
  python3 scripts/godziny.py plan [<id>]                             # JSON: co wywołać (update_trigger / create_trigger / wyłączenie)
  python3 scripts/godziny.py zmiana <id> [--czas HH:MM] [--data RRRR-MM-DD]   # co robić NA TEJ zmianie (czyta pracownik)
"""
import argparse, datetime as dt, json, re, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wspolne import ROOT, TZ, teraz
from czat import karta, znane_id
from sesje import ZADANIA, naglowek_zadania, wczytaj as wczytaj_sesje

PLIK = ROOT / "zespol" / "godziny.json"
DNI = {"nd": 0, "ndz": 0, "niedz": 0, "pon": 1, "pn": 1, "wt": 2, "sr": 3, "śr": 3, "czw": 4, "cz": 4, "pt": 5, "sob": 6, "sb": 6}
NAZWA_DNIA = ["nd", "pon", "wt", "śr", "czw", "pt", "sob"]          # numeracja jak w cron: 0 = niedziela
KIEDY = {"kazda": "na każdej zmianie", "rano": "na pierwszej zmianie dnia", "ostatnia": "na ostatniej zmianie dnia",
         "pozniej": "na zmianach po pierwszej", "wezwanie": "na wezwanie (bez zegarka)"}
TOLERANCJA = dt.timedelta(minutes=15)   # zadanie może odpalić chwilę przed/po czasie


# ---------- plik godziny.json ----------
def wczytaj():
    try:
        d = json.loads(PLIK.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        d = {}
    d.setdefault("strefa", "Europe/Warsaw")
    d.setdefault("pracownicy", {})
    return d


def zapisz(d):
    """Jedna linia na pracownika – czytelnie dla człowieka."""
    linie = ["{", f' "_opis": {json.dumps(d.get("_opis", ""), ensure_ascii=False)},',
             f' "strefa": {json.dumps(d["strefa"], ensure_ascii=False)},', ' "pracownicy": {']
    prac = list(d["pracownicy"].items())
    for i, (pid, v) in enumerate(prac):
        linie.append(f'  {json.dumps(pid)}: {json.dumps(v, ensure_ascii=False)}' + ("," if i < len(prac) - 1 else ""))
    linie += [" }", "}"]
    PLIK.write_text("\n".join(linie) + "\n", encoding="utf-8")


def godzina(tekst):
    m = re.fullmatch(r"\s*(\d{1,2})(?:[:.](\d{2}))?\s*", tekst)
    if not m or int(m.group(1)) > 23 or int(m.group(2) or 0) > 59:
        sys.exit(f"Zła godzina: {tekst!r} (np. 5:05, 12:00, 6)")
    return f"{int(m.group(1)):02d}:{int(m.group(2) or 0):02d}"


def minuty(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def ladnie(hhmm):
    return f"{int(hhmm[:2])}:{hhmm[3:]}"


def dni_zbior(tekst):
    """'codziennie' | 'pon-pt' | 'pon' | 'pon,śr,pt' | 'sob-nd' -> zbiór numerów dni jak w cron (0 = nd)."""
    t = (tekst or "codziennie").strip().lower().replace(" ", "")
    if t in ("", "codziennie", "*", "wszystkie"):
        return set(range(7))
    wynik = set()
    for kawalek in t.split(","):
        if "-" in kawalek:
            a, b = kawalek.split("-", 1)
            if a not in DNI or b not in DNI:
                sys.exit(f"Nie znam dnia w {kawalek!r} (pon, wt, śr, czw, pt, sob, nd)")
            i = DNI[a]
            while True:
                wynik.add(i)
                if i == DNI[b]:
                    break
                i = (i + 1) % 7
        elif kawalek in DNI:
            wynik.add(DNI[kawalek])
        else:
            sys.exit(f"Nie znam dnia {kawalek!r} (pon, wt, śr, czw, pt, sob, nd)")
    return wynik


def dzien_cron(data):
    return (data.weekday() + 1) % 7      # Python: pon = 0 → cron: pon = 1, nd = 0


def pracownik(pid, d=None):
    p = (d or wczytaj())["pracownicy"].get(pid) or {}
    return sorted({godzina(g) for g in p.get("godziny", [])}, key=minuty), p.get("dni", "codziennie")


def opis_godzin(pid, d=None):
    g, dni = pracownik(pid, d)
    if not g:
        return "bez stałych godzin – tylko na zlecenie"
    return " i ".join(ladnie(x) for x in g) + ("" if dni_zbior(dni) == set(range(7)) else f" ({dni})")


# ---------- obowiązki (zespol/zadania/<id>-*.md) ----------
def obowiazki(pid):
    wynik = []
    for p in sorted(ZADANIA.glob(f"{pid}-*.md")):
        n = naglowek_zadania(p)
        if n.get("wylaczone") == "tak":
            continue
        czesci = (n.get("kiedy") or "kazda").split()
        ktora = czesci[0].lower()
        if ktora not in KIEDY:
            sys.exit(f"{p.relative_to(ROOT)}: nieznane `kiedy: {ktora}` (dozwolone: {', '.join(KIEDY)})")
        wynik.append({"klucz": p.stem[len(pid) + 1:], "plik": str(p.relative_to(ROOT)), "nazwa": n.get("nazwa", p.stem),
                      "ktora": ktora, "dni": dni_zbior(",".join(czesci[1:])) if len(czesci) > 1 else None,
                      "kiedy": n.get("kiedy") or "kazda", "kolejnosc": int(n.get("kolejnosc") or 50)})
    return sorted(wynik, key=lambda o: (o["kolejnosc"], o["plik"]))


def zmiany_dnia(pid, data, d=None):
    g, dni = pracownik(pid, d)
    return g if dzien_cron(data) in dni_zbior(dni) else []


def na_zmiane(pid, data, nr, d=None):
    """Obowiązki na zmianę nr (0 = pierwsza) danego dnia."""
    n = len(zmiany_dnia(pid, data, d))
    wynik = []
    for o in obowiazki(pid):
        if o["ktora"] == "wezwanie" or (o["dni"] is not None and dzien_cron(data) not in o["dni"]):
            continue
        if (o["ktora"] == "kazda" or (o["ktora"] == "rano" and nr == 0)
                or (o["ktora"] == "ostatnia" and nr == n - 1) or (o["ktora"] == "pozniej" and nr > 0)):
            wynik.append(o)
    return wynik


def puste_zmiany(pid, d=None):
    """Zmiany w tygodniu, na których pracownik nie miałby nic do roboty (= kredyty za darmo)."""
    dzis = teraz().date()
    pon = dzis - dt.timedelta(days=dzis.weekday())
    braki = []
    for i in range(7):
        data = pon + dt.timedelta(days=i)
        for nr, g in enumerate(zmiany_dnia(pid, data, d)):
            if not na_zmiane(pid, data, nr, d):
                braki.append(f"{NAZWA_DNIA[dzien_cron(data)]} {ladnie(g)}")
    return braki


# ---------- zadania automatyczne (triggery) ----------
def krotki_tytul(pid):
    k = karta(pid)
    return f"{k.get('emoji', '')} {k.get('imie', pid)}".strip()


def prompt_zmiany(pid):
    return (f"⏰ Zmiana pracy – {krotki_tytul(pid)} (zespol/{pid}.md). Godziny zmian ustawia zespol/godziny.json – nie zmieniaj ich sam.\n"
            "1. `cd` do repozytorium klaudiusz, `git pull --rebase origin main` (jeśli repo nie jest sklonowane – wywołaj "
            "mcp__claude-code-remote__add_repo owner=fudali-biuro repo=klaudiusz access=push i sklonuj).\n"
            f"2. `python3 scripts/godziny.py zmiana {pid}` – wypisze, co masz zrobić NA TEJ zmianie (zależy od godziny i dnia) "
            "i które pliki przeczytać (AGENTS.md, Twoja karta, procedury).\n"
            "3. Wykonaj DOKŁADNIE procedury z wypisanych plików, po kolei. Nic ponad listę.\n"
            f"4. Zapisz wyniki na main, ustaw status w biurze (python3 scripts/status.py {pid} …) i zakończ zmianę.\n"
            "OSZCZĘDZAJ KREDYTY: przekazania dla kolegów zostawiaj w plikach (przeczytają je na swojej zmianie); send_message "
            "do innej sesji tylko w sprawie pilnej na dziś. Meldunek do Klaudiusza tylko, gdy coś wymaga jego decyzji – status "
            "w biurze wystarczy. Prośby do Pablo jak zwykle (status.py … czeka --prosba).")


def wyzwalacze(pid, d=None):
    """Docelowe zadania automatyczne pracownika: zmiany (po jednym na każdą minutę godziny) + zadania na wezwanie."""
    g, dni = pracownik(pid, d)
    zbior = dni_zbior(dni)
    dow = "*" if zbior == set(range(7)) else ",".join(str(x) for x in sorted(zbior))
    grupy = {}
    for x in g:
        grupy.setdefault(int(x[3:]), []).append(int(x[:2]))
    wynik = []
    for i, (m, godz) in enumerate(sorted(grupy.items(), key=lambda kv: min(kv[1]) * 60 + kv[0])):
        czasy = " i ".join(f"{h}:{m:02d}" for h in godz)
        wynik.append({"klucz": "zmiana" if i == 0 else f"zmiana-{i + 1}",
                      "name": f"{krotki_tytul(pid)} – {'zmiana' if len(godz) == 1 else 'zmiany'} {czasy}" + ("" if dow == "*" else f" ({dni})"),
                      "cron_expression": f"CRON_TZ={(d or wczytaj())['strefa']} {m} {','.join(str(h) for h in godz)} * * {dow}",
                      "prompt": prompt_zmiany(pid)})
    for o in obowiazki(pid):
        if o["ktora"] == "wezwanie":
            tresc = (ROOT / o["plik"]).read_text(encoding="utf-8").split("---", 2)[2].strip()
            wynik.append({"klucz": o["klucz"], "name": o["nazwa"], "cron_expression": "", "prompt": tresc})
    return wynik


def plan(pids):
    d, s = wczytaj(), wczytaj_sesje()["sesje"]
    akcje = []
    for pid in pids:
        sesja = (s.get(pid) or {}).get("sesja")
        mam = dict((s.get(pid) or {}).get("zadania") or {})
        chce = wyzwalacze(pid, d)
        if not sesja:
            if any(w["cron_expression"] for w in chce):
                akcje.append({"pracownik": pid, "uwaga": "brak sesji – najpierw utwórz ją wg zespol/sesje.md (pkt 2), potem uruchom plan jeszcze raz"})
            continue
        for w in chce:
            if w["klucz"] in mam:
                if w["cron_expression"]:
                    akcje.append({"pracownik": pid, "narzedzie": "update_trigger",
                                  "argumenty": {"trigger_id": mam[w["klucz"]], "name": w["name"], "cron_expression": w["cron_expression"],
                                                "prompt": w["prompt"], "enabled": True}})
            else:
                arg = {"name": w["name"], "prompt": w["prompt"], "persistent_session_id": sesja, "initiation": "human_request"}
                if w["cron_expression"]:
                    arg["cron_expression"] = w["cron_expression"]
                akcje.append({"pracownik": pid, "narzedzie": "create_trigger", "argumenty": arg,
                              "potem": f"python3 scripts/sesje.py zadanie {pid} {w['klucz']} <trig_id z odpowiedzi>"})
        for klucz, trig in mam.items():     # plan zarządza TYLKO swoimi zadaniami „zmiana*” (czat/skrzynki mają własną procedurę)
            if (klucz == "zmiana" or klucz.startswith("zmiana-")) and klucz not in {w["klucz"] for w in chce}:
                akcje.append({"pracownik": pid, "narzedzie": "update_trigger", "argumenty": {"trigger_id": trig, "enabled": False},
                              "potem": f"python3 scripts/sesje.py usun-zadanie {pid} {klucz}",
                              "uwaga": f"„{klucz}” nie jest już potrzebne – WYŁĄCZ (nie kasuj)"})
        for b in puste_zmiany(pid, d):
            akcje.append({"pracownik": pid, "uwaga": f"zmiana {b} – brak obowiązków (pracownik obudzi się na darmo; popraw godziny/dni)"})
    return akcje


# ---------- zmiana: co robić teraz ----------
def biezaca(pid, chwila, d=None):
    """(nr zmiany, godzina) dla chwili; None, gdy to nie pora zmiany tego dnia."""
    z = zmiany_dnia(pid, chwila.date(), d)
    pasujace = [i for i, g in enumerate(z)
                if dt.datetime.combine(chwila.date(), dt.time(int(g[:2]), int(g[3:])), TZ) <= chwila + TOLERANCJA]
    if pasujace:
        return pasujace[-1], z[pasujace[-1]]
    return (0, z[0]) if z else None


def poprzednia(pid, chwila, nr, d=None):
    data = chwila.date()
    z = zmiany_dnia(pid, data, d)
    if nr > 0:
        g = z[nr - 1]
        return dt.datetime.combine(data, dt.time(int(g[:2]), int(g[3:])), TZ)
    for i in range(1, 9):
        dd = data - dt.timedelta(days=i)
        z = zmiany_dnia(pid, dd, d)
        if z:
            return dt.datetime.combine(dd, dt.time(int(z[-1][:2]), int(z[-1][3:])), TZ)
    return None


def zmienione_od(pliki, od):
    if od is None:
        return set(pliki)
    try:
        wynik = set()
        for p in pliki:
            if subprocess.run(["git", "log", "-1", "--format=%H", f"--since={od.isoformat()}", "--", p],
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip():
                wynik.add(p)
        return wynik
    except Exception:
        return set(pliki)


def zmiana(pid, chwila):
    d = wczytaj()
    b = biezaca(pid, chwila, d)
    dzien = f"{NAZWA_DNIA[dzien_cron(chwila.date())]} {chwila:%d.%m.%Y %H:%M}"
    if b is None:
        print(f"⏸️  {krotki_tytul(pid)}: dziś ({dzien}) nie masz zmiany – godziny: {opis_godzin(pid, d)}.\n"
              "Nic nie rób (chyba że ktoś zlecił Ci coś wprost w tej wiadomości). Zakończ.")
        return
    nr, g = b
    z = zmiany_dnia(pid, chwila.date(), d)
    rodzaj = ("jedyna zmiana dnia" if len(z) == 1 else "poranna – pierwsza zmiana dnia" if nr == 0
              else "ostatnia zmiana dnia" if nr == len(z) - 1 else f"zmiana {nr + 1} z {len(z)}")
    lista = na_zmiane(pid, chwila.date(), nr, d)
    print(f"⏰ {krotki_tytul(pid)} – zmiana {ladnie(g)} ({rodzaj}), teraz: {dzien} (czas polski).")
    if not lista:
        print("Na tej zmianie nie masz obowiązków. Ustaw status i zakończ:\n"
              f"  python3 scripts/status.py {pid} wolne \"Zmiana {ladnie(g)} – nic do zrobienia\"")
        return
    print("\nDO ZROBIENIA TERAZ (po kolei):")
    for i, o in enumerate(lista, 1):
        print(f"  {i}. {o['plik']} – {o['nazwa']}")
    if len(z) > 1 and nr > 0:
        print("  (zmiana w ciągu dnia: reaguj na to, co przyszło od rana – odpowiedzi Pablo w czacie, nowe dane kolegów)")
    pliki = ["AGENTS.md", f"zespol/{pid}.md"] + [o["plik"] for o in lista]
    od = poprzednia(pid, chwila, nr, d)
    zm = zmienione_od(pliki, od)
    if zm:
        print(f"\nPRZECZYTAJ (zmieniły się od poprzedniej zmiany{f' – {od:%d.%m %H:%M}' if od else ''}): " + ", ".join(p for p in pliki if p in zm))
    reszta = [p for p in pliki if p not in zm]
    if reszta:
        print("Bez zmian (czytaj tylko, jeśli nie masz ich w pamięci tej rozmowy): " + ", ".join(reszta))
    nast = [x for x in z if minuty(x) > minuty(g)]
    print(f"\nNastępna zmiana: {ladnie(nast[0]) + ' dziś' if nast else 'jutro lub później – wg zespol/godziny.json'}.")


# ---------- pokaz / ustaw ----------
def pokaz():
    d = wczytaj()
    s = wczytaj_sesje()["sesje"]
    print(f"Godziny pracy zespołu ({d['strefa']}) – zespol/godziny.json\n")
    for pid in list(d["pracownicy"]) + [x for x in znane_id() if x not in d["pracownicy"]]:
        ob = obowiazki(pid)
        if pid not in d["pracownicy"] and not ob:
            continue
        print(f"{krotki_tytul(pid):14} ⏰ {opis_godzin(pid, d)}")
        for o in ob:
            dni = f" ({','.join(NAZWA_DNIA[x] for x in sorted(o['dni']))})" if o["dni"] is not None else ""
            print(f"{'':17}- {o['nazwa']} – {KIEDY[o['ktora']]}{dni}  [{o['plik']}]")
        zad = (s.get(pid) or {}).get("zadania") or {}
        if zad:
            print(f"{'':17}zadania automatyczne: " + ", ".join(f"{k}={v}" for k, v in zad.items()))
        for b in puste_zmiany(pid, d):
            print(f"{'':17}⚠️  zmiana {b} bez obowiązków")


def ustaw(kto, czasy, dni):
    d = wczytaj()
    P = d["pracownicy"]
    brak = len(czasy) == 1 and czasy[0].lower() in ("brak", "nic", "-", "zlecenie")
    nowe = [] if brak else sorted({godzina(c) for c in czasy}, key=minuty)
    if dni:
        dni_zbior(dni)   # walidacja
    if kto == "wszyscy":
        aktywni = [p for p, v in P.items() if v.get("godziny")]
        if not aktywni:
            sys.exit("Nikt nie ma jeszcze godzin – ustaw każdego osobno.")
        baza = min(minuty(pracownik(p, d)[0][0]) for p in aktywni)
        for p in aktywni:
            g, _ = pracownik(p, d)
            przes = minuty(g[0]) - baza            # zachowaj kolejność i odstępy (Mietek → Bartek → Kuba → Ola)
            lista = nowe[:1] if len(g) == 1 else nowe   # kto ma 1 zmianę (np. Bartek – raz w tygodniu), dostaje tylko pierwszą
            P[p]["godziny"] = [f"{(minuty(x) + przes) // 60 % 24:02d}:{(minuty(x) + przes) % 60:02d}" for x in lista]
            if dni:
                P[p]["dni"] = dni
    else:
        if kto not in znane_id():
            sys.exit(f"Nie znam pracownika {kto!r}: {', '.join(znane_id())}")
        P.setdefault(kto, {"godziny": [], "dni": "codziennie"})["godziny"] = nowe
        if dni:
            P[kto]["dni"] = dni
    zapisz(d)
    for p in (P if kto == "wszyscy" else [kto]):
        print(f"{krotki_tytul(p):14} ⏰ {opis_godzin(p, d)}")
    print(f"\nTeraz: python3 scripts/godziny.py plan{'' if kto == 'wszyscy' else ' ' + kto}  → wykonaj wypisane kroki i zapisz na main.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komenda", choices=["pokaz", "ustaw", "plan", "zmiana"])
    ap.add_argument("argumenty", nargs="*")
    ap.add_argument("--dni", help="np. codziennie, pon-pt, pon, pon,śr,pt")
    ap.add_argument("--czas", help="HH:MM (test komendy zmiana)")
    ap.add_argument("--data", help="RRRR-MM-DD (test komendy zmiana)")
    a = ap.parse_args()
    arg = a.argumenty
    if a.komenda == "pokaz":
        pokaz()
    elif a.komenda == "ustaw":
        if len(arg) < 2:
            sys.exit("Użycie: ustaw <id|wszyscy> 5:05 12:05 [--dni pon-pt]   albo   ustaw <id> brak")
        ustaw(arg[0], arg[1:], a.dni)
    elif a.komenda == "plan":
        d = wczytaj()
        pids = arg or sorted(set(d["pracownicy"]) | {p for p in znane_id() if obowiazki(p)})
        print(json.dumps(plan(pids), ensure_ascii=False, indent=1))
    elif a.komenda == "zmiana":
        if not arg or arg[0] not in znane_id():
            sys.exit(f"Podaj id pracownika: {', '.join(znane_id())}")
        chwila = teraz()
        if a.data or a.czas:
            data = dt.date.fromisoformat(a.data) if a.data else chwila.date()
            g = godzina(a.czas) if a.czas else chwila.strftime("%H:%M")
            chwila = dt.datetime.combine(data, dt.time(int(g[:2]), int(g[3:])), TZ)
        zmiana(arg[0], chwila)


if __name__ == "__main__":
    main()
