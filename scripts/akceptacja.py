#!/usr/bin/env python3
"""Biuro akceptacji – biblioteka postów do zatwierdzenia przez Pablo (strona: biuro → ✅ Akceptacja).

Każdy post = jeden plik marketing/akceptacja/<id>.json. Pablo w biurze klika: ✅ OK / ✏️ Popraw (+komentarz) / ❌ Odrzuć,
potem „Wyślij decyzje” → jedna wiadomość do Oli (czat). Ola/Zosia wpisują decyzje do plików i działają dalej.

  python3 scripts/akceptacja.py dodaj --kanal instagram --data 2026-11-09 --godzina 18:00 --tytul "Start sezonu" \
      --tekst-plik marketing/posty/x.md --obraz marketing/zdjecia/swieta-2026/kolaz-start-ig-4x5.jpg --autor marketing
  python3 scripts/akceptacja.py lista [--stan czeka]
  python3 scripts/akceptacja.py ustaw <id> ok|popraw|odrzucone|w-bufferze|opublikowane [--komentarz "…"] [--kto pablo]
  python3 scripts/akceptacja.py popraw <id> [--tekst-plik …] [--obraz …]     # nowa wersja po poprawkach → znów „czeka”
  python3 scripts/akceptacja.py przypomnij [--min 3]                          # Klaudiusz: „Pablo, biblioteka pełna – przejrzyj”
Zapis w archiwum robi sam (git), chyba że --bez-zapisu.
"""
import argparse, datetime, json, pathlib, re, secrets, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KAT = ROOT / "marketing" / "akceptacja"
KANALY = ["instagram", "facebook", "pinterest", "tiktok", "instagram-relacja", "etsy"]
STANY = ["czeka", "ok", "popraw", "odrzucone", "w-bufferze", "opublikowane"]
ADRES = "https://biuro-fudali.vercel.app/akceptacja.html"


def teraz():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def zapisz(sciezki, opis, bez_zapisu):
    if bez_zapisu:
        return
    git("add", *[str(p) for p in sciezki])
    if git("diff", "--cached", "--quiet").returncode == 0:
        return
    git("commit", "-q", "-m", f"Akceptacja: {opis}")
    for _ in range(4):
        git("pull", "-q", "--rebase", "origin", "main")
        if git("push", "-q", "origin", "HEAD:main").returncode == 0:
            print("💾 Zapisane w archiwum – w biurze widać za ok. 1 min.")
            return
    print("⚠️ Nie udało się zapisać w archiwum – spróbuj ponownie.", file=sys.stderr)


def wczytaj(pid):
    p = KAT / f"{pid}.json"
    if not p.exists():
        sys.exit(f"Brak posta {pid}")
    return p, json.loads(p.read_text())


def rel(sciezka):
    p = (ROOT / sciezka).resolve() if not pathlib.Path(sciezka).is_absolute() else pathlib.Path(sciezka).resolve()
    if not p.exists():
        sys.exit(f"Brak pliku: {sciezka}")
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        sys.exit(f"Plik musi być w archiwum (repozytorium): {sciezka}")


def tekst_z(a):
    if a.tekst_plik:
        return (ROOT / a.tekst_plik).read_text().strip()
    return (a.tekst or "").strip()


def dodaj(a):
    KAT.mkdir(parents=True, exist_ok=True)
    pid = f"{(a.data or datetime.date.today().isoformat())}-{a.kanal}-{secrets.token_hex(2)}"
    post = {
        "id": pid, "kanal": a.kanal, "data": a.data, "godzina": a.godzina, "tytul": a.tytul,
        "produkt": a.produkt, "tekst": tekst_z(a), "hashtagi": a.hashtagi or "",
        "obrazy": [rel(o) for o in a.obraz], "wideo": [rel(w) for w in a.wideo],
        "autor": a.autor, "kampania": a.kampania or "", "stan": "czeka", "komentarz": "", "wersja": 1,
        "utworzono": teraz(), "zmieniono": teraz(), "historia": [{"czas": teraz(), "kto": a.autor, "stan": "czeka"}],
    }
    p = KAT / f"{pid}.json"
    p.write_text(json.dumps(post, ensure_ascii=False, indent=1) + "\n")
    print(f"Dodano do biblioteki: {pid} ({a.kanal}, {a.tytul})")
    zapisz([p], f"nowy post {pid}", a.bez_zapisu)


def lista(a):
    posty = sorted((json.loads(p.read_text()) for p in KAT.glob("*.json")), key=lambda x: (x.get("data") or "", x["id"]))
    for x in posty:
        if a.stan and x["stan"] != a.stan:
            continue
        kom = f" – „{x['komentarz']}”" if x.get("komentarz") else ""
        print(f"{x['stan']:<12} {x['id']:<36} {x.get('data') or '':<10} {x['kanal']:<18} {x.get('tytul') or ''}{kom}")
    ile = sum(1 for x in posty if x["stan"] == "czeka")
    print(f"\nCzeka na Pablo: {ile} · strona: {ADRES}")


def ustaw(a):
    p, x = wczytaj(a.id)
    x["stan"] = a.stan
    if a.komentarz is not None:
        x["komentarz"] = a.komentarz
    x["zmieniono"] = teraz()
    x.setdefault("historia", []).append({"czas": teraz(), "kto": a.kto, "stan": a.stan, **({"komentarz": a.komentarz} if a.komentarz else {})})
    p.write_text(json.dumps(x, ensure_ascii=False, indent=1) + "\n")
    print(f"{a.id} → {a.stan}")
    zapisz([p], f"{a.id} → {a.stan}", a.bez_zapisu)


def popraw(a):
    p, x = wczytaj(a.id)
    if a.tekst_plik or a.tekst:
        x["tekst"] = tekst_z(a)
    if a.obraz:
        x["obrazy"] = [rel(o) for o in a.obraz]
    if a.hashtagi is not None:
        x["hashtagi"] = a.hashtagi
    x["wersja"] = x.get("wersja", 1) + 1
    x["stan"] = "czeka"
    x["zmieniono"] = teraz()
    x.setdefault("historia", []).append({"czas": teraz(), "kto": a.kto, "stan": "czeka", "komentarz": f"poprawiona wersja {x['wersja']}"})
    p.write_text(json.dumps(x, ensure_ascii=False, indent=1) + "\n")
    print(f"{a.id} – wersja {x['wersja']} czeka na Pablo")
    zapisz([p], f"{a.id} poprawiony (v{x['wersja']})", a.bez_zapisu)


def przypomnij(a):
    ile = sum(1 for p in KAT.glob("*.json") if json.loads(p.read_text())["stan"] == "czeka")
    if ile < a.min:
        print(f"Czeka {ile} – za mało, nie przypominam (próg {a.min}).")
        return
    tekst = (f"Paweł, biblioteka akceptacji jest pełna – czeka {ile} postów. Wejdź w „✅ Akceptacja” w biurze ({ADRES}), "
             f"przy każdym kliknij ✅ OK, ✏️ Popraw (z komentarzem, co zmienić) albo ❌ Odrzuć, a na końcu „Wyślij decyzje”. "
             f"Resztę (szkice w Bufferze) zrobią Ola i Zosia.")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "czat.py"), "napisz", "klaudiusz", tekst, "--typ", "prosba"], cwd=ROOT)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dodaj")
    d.add_argument("--kanal", choices=KANALY, required=True)
    d.add_argument("--data"); d.add_argument("--godzina"); d.add_argument("--tytul", required=True)
    d.add_argument("--produkt"); d.add_argument("--tekst"); d.add_argument("--tekst-plik"); d.add_argument("--hashtagi")
    d.add_argument("--obraz", action="append", default=[]); d.add_argument("--wideo", action="append", default=[])
    d.add_argument("--autor", default="marketing"); d.add_argument("--kampania")
    l = sub.add_parser("lista"); l.add_argument("--stan", choices=STANY)
    u = sub.add_parser("ustaw"); u.add_argument("id"); u.add_argument("stan", choices=STANY)
    u.add_argument("--komentarz"); u.add_argument("--kto", default="pablo")
    p = sub.add_parser("popraw"); p.add_argument("id"); p.add_argument("--tekst"); p.add_argument("--tekst-plik")
    p.add_argument("--obraz", action="append", default=[]); p.add_argument("--hashtagi"); p.add_argument("--kto", default="marketing")
    r = sub.add_parser("przypomnij"); r.add_argument("--min", type=int, default=3)
    for s in (d, u, p):
        s.add_argument("--bez-zapisu", action="store_true")
    a = ap.parse_args()
    {"dodaj": dodaj, "lista": lista, "ustaw": ustaw, "popraw": popraw, "przypomnij": przypomnij}[a.cmd](a)


if __name__ == "__main__":
    main()
