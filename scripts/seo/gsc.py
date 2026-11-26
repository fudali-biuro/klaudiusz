#!/usr/bin/env python3
"""Google Search Console – tylko odczyt (zakres webmasters.readonly).

Klucz konta usługi: zmienna środowiska GSC_KEY_B64 (plik .json zakodowany base64) albo GSC_KEY_JSON (treść pliku).
Nigdy nie zapisuj klucza w plikach ani w czacie.

  python3 scripts/seo/gsc.py test                 # czy klucz działa i jakie usługi widać
  python3 scripts/seo/gsc.py pozycje [--dni 28]   # frazy: kliknięcia, wyświetlenia, CTR, średnia pozycja → seo/pozycje/gsc/RRRR-MM-DD.csv
  python3 scripts/seo/gsc.py strony  [--dni 28]   # to samo w podziale na adresy stron
"""
import argparse, base64, csv, datetime as dt, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

WLASNOSC = "https://www.fudali.com.pl/"  # zweryfikowana 26.11.2026 (tag HTML)
ZAKRES = "https://www.googleapis.com/auth/webmasters.readonly"
REPO = Path(__file__).resolve().parents[2]


def klucz():
    b64, js = os.environ.get("GSC_KEY_B64", "").strip(), os.environ.get("GSC_KEY_JSON", "").strip()
    if b64:
        return json.loads(base64.b64decode(b64 + "=" * (-len(b64) % 4)))
    if js:
        return json.loads(js)
    sys.exit("Brak klucza Search Console: dodaj zmienną GSC_KEY_B64 w ustawieniach środowiska (procedura: seo/search-console-podlaczenie.md).")


def token(k):
    b = lambda d: base64.urlsafe_b64encode(json.dumps(d, separators=(",", ":")).encode()).rstrip(b"=")
    teraz = int(time.time())
    naglowek = b({"alg": "RS256", "typ": "JWT"})
    tresc = b({"iss": k["client_email"], "scope": ZAKRES, "aud": k["token_uri"], "iat": teraz, "exp": teraz + 3600})
    pk = serialization.load_pem_private_key(k["private_key"].encode(), password=None)
    podpis = base64.urlsafe_b64encode(pk.sign(naglowek + b"." + tresc, padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=")
    jwt = (naglowek + b"." + tresc + b"." + podpis).decode()
    dane = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    with urllib.request.urlopen(urllib.request.Request(k["token_uri"], data=dane)) as r:
        return json.load(r)["access_token"]


def api(tok, sciezka, cialo=None):
    url = "https://www.googleapis.com/webmasters/v3/" + sciezka
    req = urllib.request.Request(url, data=json.dumps(cialo).encode() if cialo else None,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Search Console {e.code}: {e.read().decode()[:300]}")


def zapytanie(tok, wymiar, dni):
    koniec = dt.date.today() - dt.timedelta(days=2)  # dane GSC mają ok. 2 dni opóźnienia
    start = koniec - dt.timedelta(days=dni - 1)
    cialo = {"startDate": str(start), "endDate": str(koniec), "dimensions": [wymiar], "rowLimit": 1000}
    wynik = api(tok, f"sites/{urllib.parse.quote(WLASNOSC, safe='')}/searchAnalytics/query", cialo)
    return start, koniec, wynik.get("rows", [])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("co", choices=["test", "pozycje", "strony"])
    p.add_argument("--dni", type=int, default=28)
    a = p.parse_args()
    k = klucz()
    tok = token(k)
    if a.co == "test":
        uslugi = api(tok, "sites").get("siteEntry", [])
        print(f"Konto: {k['client_email']}")
        for s in uslugi:
            print(f"  {s['siteUrl']}  ({s['permissionLevel']})")
        if not any(s["siteUrl"] == WLASNOSC for s in uslugi):
            sys.exit(f"Brak dostępu do {WLASNOSC} – dodaj konto usługi w Search Console (Użytkownicy i uprawnienia).")
        _, _, wiersze = zapytanie(tok, "query", a.dni)
        print(f"OK – {len(wiersze)} fraz z ostatnich {a.dni} dni.")
        return
    wymiar = "query" if a.co == "pozycje" else "page"
    start, koniec, wiersze = zapytanie(tok, wymiar, a.dni)
    out = REPO / "seo/pozycje/gsc" / f"{dt.date.today()}-{'frazy' if wymiar == 'query' else 'strony'}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["od", "do", "fraza" if wymiar == "query" else "strona", "klikniecia", "wyswietlenia", "ctr_proc", "srednia_pozycja"])
        for r in sorted(wiersze, key=lambda r: -r["impressions"]):
            w.writerow([start, koniec, r["keys"][0], int(r["clicks"]), int(r["impressions"]), round(r["ctr"] * 100, 1), round(r["position"], 1)])
    print(f"Zapisano {len(wiersze)} wierszy → {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
