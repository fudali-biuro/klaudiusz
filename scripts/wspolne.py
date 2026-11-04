"""Wspólne funkcje skryptów Klaudiusza (bez zależności zewnętrznych)."""
import json, pathlib, datetime as dt
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
TZ = ZoneInfo("Europe/Warsaw")
STAN = ROOT / "monitoring" / "stan"

def teraz():
    return dt.datetime.now(TZ)

def wczytaj_konkurentow():
    """Zwraca listę słowników z front matter plików konkurencja/firmy/*.md."""
    wynik = []
    for p in sorted((ROOT / "konkurencja" / "firmy").glob("*.md")):
        tekst = p.read_text(encoding="utf-8")
        dane = {"slug": p.stem, "plik": str(p.relative_to(ROOT))}
        if tekst.startswith("---"):
            naglowek = tekst.split("---", 2)[1]
            for linia in naglowek.strip().splitlines():
                if ":" in linia:
                    k, v = linia.split(":", 1)
                    dane[k.strip()] = v.strip().strip('"').lstrip("@")
        wynik.append(dane)
    return wynik

def json_wczytaj(p, domyslnie):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return domyslnie

def json_zapisz(p, dane):
    p = pathlib.Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(dane, ensure_ascii=False, indent=1), encoding="utf-8")
