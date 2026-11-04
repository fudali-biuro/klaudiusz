#!/usr/bin/env python3
"""Status pracownika w wirtualnym biurze (zespol/status/<id>.json).

Użycie:
  python3 scripts/status.py <id> <stan> "tekst" [--prosba "..."] [--postep 40]
  python3 scripts/status.py <id> --zalatwione          # usuń wszystkie prośby do Pablo
  python3 scripts/status.py <id> --pokaz                # wypisz status
Stany: pracuje | gotowe | czeka | wolne | blad

Status od razu zapisuje się w archiwum (biuro pokazuje go po ~15 s). --bez-zapisu = tylko lokalnie (np. w środku skryptu).
Każda --prosba trafia też do czatu z Pablo w biurze i na Telegram (--bez-telegramu, żeby pominąć Telegram).
"""
import argparse, json, sys
from wspolne import ROOT, teraz
import czat

STANY = ("pracuje", "gotowe", "czeka", "wolne", "blad")
KATALOG = ROOT / "zespol" / "status"
MAX_DZIENNIK = 40


def znane_id():
    return czat.znane_id()


def wczytaj(pid):
    p = KATALOG / f"{pid}.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"id": pid, "stan": "wolne", "zadanie": "", "postep": None,
                "aktualizacja": None, "prosby": [], "dziennik": [], "makieta": False}


def zapisz(pid, dane):
    KATALOG.mkdir(parents=True, exist_ok=True)
    (KATALOG / f"{pid}.json").write_text(json.dumps(dane, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id")
    ap.add_argument("stan", nargs="?", choices=STANY)
    ap.add_argument("tekst", nargs="?", default="")
    ap.add_argument("--prosba", action="append", default=[], help="prośba do Pablo (można kilka razy)")
    ap.add_argument("--pilne", action="store_true", help="oznacz prośbę jako pilną")
    ap.add_argument("--postep", type=int, help="postęp 0–100")
    ap.add_argument("--zalatwione", action="store_true", help="usuń prośby do Pablo")
    ap.add_argument("--pokaz", action="store_true")
    ap.add_argument("--bez-zapisu", action="store_true", help="nie zapisuj od razu w archiwum")
    ap.add_argument("--bez-telegramu", action="store_true", help="prośba bez powiadomienia na Telegramie")
    a = ap.parse_args()

    if a.id not in znane_id():
        sys.exit(f"Nieznany pracownik '{a.id}'. Dostępni: {', '.join(znane_id())}")
    dane = wczytaj(a.id)
    if a.pokaz:
        print(json.dumps(dane, ensure_ascii=False, indent=1))
        return
    if not (a.stan or a.zalatwione or a.prosba):
        sys.exit("Podaj stan (pracuje/gotowe/czeka/wolne/blad), --prosba albo --zalatwione.")

    czas = teraz().isoformat(timespec="minutes")
    dane["aktualizacja"] = czas
    dane["makieta"] = False  # prawdziwa aktualizacja = już nie makieta
    if a.zalatwione:
        if dane.get("prosby"):
            dane["dziennik"].insert(0, {"czas": czas, "stan": "gotowe", "tekst": "Prośby do Pablo załatwione"})
        dane["prosby"] = []
    if a.stan:
        dane["stan"] = a.stan
        if a.tekst:
            dane["zadanie"] = a.tekst
        dane["postep"] = a.postep if a.postep is not None else (100 if a.stan == "gotowe" else None)
        dane.setdefault("dziennik", []).insert(0, {"czas": czas, "stan": a.stan, "tekst": a.tekst})
    elif a.postep is not None:
        dane["postep"] = a.postep
    for t in a.prosba:
        dane.setdefault("prosby", []).append({"czas": czas, "tresc": t, "pilne": a.pilne})
        if not a.stan:
            dane["stan"] = "czeka"
    dane["dziennik"] = dane.get("dziennik", [])[:MAX_DZIENNIK]
    zapisz(a.id, dane)
    print(f"Status {a.id}: {dane['stan']} – {dane.get('zadanie', '')}")

    # prośby do Pablo → także wiadomość w czacie (Pablo odpowiada w tym samym oknie) i Telegram
    pliki = [KATALOG / f"{a.id}.json"]
    for t in a.prosba:
        w = {"id": czat.nowe_id("o"), "czas": teraz().isoformat(timespec="seconds"), "od": a.id, "do": "pablo",
             "typ": "prosba", "tekst": t, "pliki": [], "pilne": a.pilne}
        pliki.append(czat.zapisz_wiadomosc(a.id, w))
    if not a.bez_zapisu:
        imie = czat.karta(a.id).get("imie", a.id)
        czat.zapisz_w_archiwum(pliki, f"Status: {imie} – {dane['stan']}" + (" (prośba do Pablo)" if a.prosba else ""))
    if a.prosba and not a.bez_telegramu:
        lista = "\n".join(f"• {t}" for t in a.prosba)
        czat.telegram(f"🙋 {czat.kto(a.id)} potrzebuje Twojej decyzji:\n{lista}\n\nOdpowiedz w czacie w biurze: {czat.BIURO}/#czat-{a.id}")


if __name__ == "__main__":
    main()
