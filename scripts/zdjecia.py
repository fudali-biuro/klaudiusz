#!/usr/bin/env python3
"""📸 Biblioteka prawdziwych zdjęć Pablo – marketing/biblioteka-zdjec/ (strona w biurze: 📸 Zdjęcia).

Sekcje:  tla      – prawdziwe tła: salon, taras, ogród, wnętrza (bez produktu albo do podmiany)
         produkty – prawdziwe zdjęcia produktów (leżak, stolik, …) – do wstawiania w tła
         gotowe   – prawdziwe zdjęcia gotowe do użycia od razu (produkt w realnym miejscu)
Zasada: najpierw prawdziwe zdjęcia; łączymy produkt + tło (montaż, ewentualnie świąteczne dodatki) – to NIE jest „grafika AI”.
Rotacja: bierz zdjęcia najrzadziej używane (`nastepne`), po użyciu zapisz (`uzyj`) – żeby posty się nie powtarzały.

  python3 scripts/zdjecia.py dodaj --sekcja tla plik1.jpg [plik2.jpg …] [--opis "salon z kominkiem"] [--tagi salon,zima] [--produkt lezak]
  python3 scripts/zdjecia.py lista [--sekcja tla]
  python3 scripts/zdjecia.py nastepne --sekcja tla [--tag taras] [-n 3]       # najrzadziej używane
  python3 scripts/zdjecia.py uzyj <plik> [<plik> …] --gdzie <id posta>          # zapis użycia (rotacja)
  python3 scripts/zdjecia.py opisz <plik> --opis "…" [--tagi a,b] [--produkt lezak]
"""
import argparse, datetime, json, pathlib, re, shutil, subprocess, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIB = ROOT / "marketing" / "biblioteka-zdjec"
INDEKS = BIB / "indeks.json"
SEKCJE = {"tla": "🏡 Tła", "produkty": "🪑 Produkty", "gotowe": "✨ Gotowe ujęcia"}
ROZSZ = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".mp4", ".mov"}


def teraz():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")


def wczytaj():
    try:
        return json.loads(INDEKS.read_text())
    except Exception:
        return {"zdjecia": {}}


def zapisz_indeks(d):
    BIB.mkdir(parents=True, exist_ok=True)
    INDEKS.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def archiwum(opis, bez):
    if bez:
        return
    git("add", str(BIB))
    if git("diff", "--cached", "--quiet").returncode == 0:
        return
    git("commit", "-q", "-m", f"Biblioteka zdjęć: {opis}")
    for _ in range(4):
        git("pull", "-q", "--rebase", "origin", "main")
        if git("push", "-q", "origin", "HEAD:main").returncode == 0:
            print("💾 Zapisane w archiwum – w biurze widać za ok. 1 min.")
            return
    print("⚠️ Nie udało się zapisać w archiwum.", file=sys.stderr)


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:50] or "zdjecie"


def klucz(plik):
    p = pathlib.Path(plik)
    if p.is_absolute() or (ROOT / p).exists():
        p = (ROOT / p).resolve() if not p.is_absolute() else p.resolve()
        try:
            return str(p.relative_to(ROOT))
        except ValueError:
            pass
    return str(plik)


def dodaj(a):
    d = wczytaj()
    kat = BIB / a.sekcja
    kat.mkdir(parents=True, exist_ok=True)
    dzis = datetime.date.today().isoformat()
    for f in a.pliki:
        src = pathlib.Path(f)
        if not src.exists() or src.suffix.lower() not in ROZSZ:
            print(f"pomijam: {f}")
            continue
        baza = slug(a.opis or re.sub(r"^\d{8}-\d{6}-", "", src.stem))
        cel = kat / f"{dzis}-{baza}{src.suffix.lower()}"
        i = 2
        while cel.exists():
            cel = kat / f"{dzis}-{baza}-{i}{src.suffix.lower()}"
            i += 1
        shutil.copy2(src, cel)
        rel = str(cel.relative_to(ROOT))
        d["zdjecia"][rel] = {"sekcja": a.sekcja, "opis": a.opis or "", "tagi": [t.strip() for t in (a.tagi or "").split(",") if t.strip()],
                             "produkt": a.produkt or "", "dodano": teraz(), "od": "pablo", "uzycia": []}
        print(f"+ {rel}")
    zapisz_indeks(d)
    archiwum(f"nowe zdjęcia ({SEKCJE[a.sekcja]})", a.bez_zapisu)


def lista(a):
    d = wczytaj()
    for rel, z in sorted(d["zdjecia"].items(), key=lambda kv: (kv[1]["sekcja"], len(kv[1]["uzycia"]), kv[0])):
        if a.sekcja and z["sekcja"] != a.sekcja:
            continue
        print(f"{z['sekcja']:<9} użyte {len(z['uzycia'])}×  {rel}  {z.get('opis', '')}  {','.join(z.get('tagi', []))}")
    print(f"\nRazem: {len(d['zdjecia'])} · strona: https://biuro-fudali.vercel.app/zdjecia.html")


def nastepne(a):
    d = wczytaj()
    kand = [(rel, z) for rel, z in d["zdjecia"].items() if z["sekcja"] == a.sekcja
            and (not a.tag or a.tag in z.get("tagi", []) or a.tag in z.get("opis", "")) and (not a.produkt or z.get("produkt") == a.produkt)]
    kand.sort(key=lambda kv: (len(kv[1]["uzycia"]), (kv[1]["uzycia"] or [{"czas": ""}])[-1]["czas"]))
    if not kand:
        print("Brak zdjęć w tej sekcji – poproś Klaudiusza, żeby przypomniał Pablo o wgraniu.")
    for rel, z in kand[:a.n]:
        print(f"{rel}  (użyte {len(z['uzycia'])}×) {z.get('opis', '')}")


def uzyj(a):
    d = wczytaj()
    for f in a.pliki:
        k = klucz(f)
        if k not in d["zdjecia"]:
            print(f"nie ma w bibliotece: {f}")
            continue
        d["zdjecia"][k]["uzycia"].append({"czas": teraz(), "gdzie": a.gdzie})
        print(f"✓ {k} – użycie nr {len(d['zdjecia'][k]['uzycia'])}")
    zapisz_indeks(d)
    archiwum("rotacja (użycia)", a.bez_zapisu)


def opisz(a):
    d = wczytaj()
    k = klucz(a.plik)
    z = d["zdjecia"].get(k) or sys.exit(f"nie ma w bibliotece: {a.plik}")
    if a.opis is not None:
        z["opis"] = a.opis
    if a.tagi is not None:
        z["tagi"] = [t.strip() for t in a.tagi.split(",") if t.strip()]
    if a.produkt is not None:
        z["produkt"] = a.produkt
    zapisz_indeks(d)
    archiwum("opis zdjęcia", a.bez_zapisu)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = ap.add_subparsers(dest="cmd", required=True)
    p = s.add_parser("dodaj"); p.add_argument("--sekcja", choices=SEKCJE, required=True); p.add_argument("pliki", nargs="+")
    p.add_argument("--opis"); p.add_argument("--tagi"); p.add_argument("--produkt")
    l = s.add_parser("lista"); l.add_argument("--sekcja", choices=SEKCJE)
    n = s.add_parser("nastepne"); n.add_argument("--sekcja", choices=SEKCJE, required=True); n.add_argument("--tag"); n.add_argument("--produkt"); n.add_argument("-n", type=int, default=3)
    u = s.add_parser("uzyj"); u.add_argument("pliki", nargs="+"); u.add_argument("--gdzie", required=True)
    o = s.add_parser("opisz"); o.add_argument("plik"); o.add_argument("--opis"); o.add_argument("--tagi"); o.add_argument("--produkt")
    for x in (p, u, o):
        x.add_argument("--bez-zapisu", action="store_true")
    a = ap.parse_args()
    {"dodaj": dodaj, "lista": lista, "nastepne": nastepne, "uzyj": uzyj, "opisz": opisz}[a.cmd](a)


if __name__ == "__main__":
    main()
