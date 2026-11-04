#!/usr/bin/env python3
"""Status pracownika w wirtualnym biurze (zespol/status/<id>.json).

Użycie:
  python3 scripts/status.py <id> <stan> "tekst" [--prosba "..."] [--postep 40]
  python3 scripts/status.py <id> --zalatwione          # usuń wszystkie prośby do Pablo
  python3 scripts/status.py <id> --pokaz                # wypisz status
Stany: pracuje | gotowe | czeka | wolne | blad
"""
import argparse, json, sys
from wspolne import ROOT, teraz

STANY = ("pracuje", "gotowe", "czeka", "wolne", "blad")
KATALOG = ROOT / "zespol" / "status"
MAX_DZIENNIK = 40


def znane_id():
    return sorted(p.stem for p in (ROOT / "zespol").glob("*.md") if p.stem != "README")


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


if __name__ == "__main__":
    main()
