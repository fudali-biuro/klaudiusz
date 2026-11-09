#!/usr/bin/env python3
"""Kuba: pomiar ZASIĘGU fraz BEZ Apify (pytrends, za darmo) – ta sama logika co zasieg.py (kotwica = 100).
Paczki: slowa-kluczowe/zasieg/paczki.json. Wynik: monitoring/stan/zasieg.json (jak zasieg.py), potem zasieg_raport.py.
Google bywa wolny (429) – czekamy między paczkami. Wymaga: pip install pytrends."""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from wspolne import ROOT, teraz  # noqa: E402
from pytrends.request import TrendReq  # noqa: E402

def sredn(xs): return round(sum(xs) / len(xs), 1) if xs else 0.0

def paczka(frazy, geo):
    for proba in range(4):
        try:
            tr = TrendReq(hl="pl-PL", tz=-60, timeout=(10, 30))
            tr.build_payload(frazy, timeframe="today 12-m", geo=geo)
            df = tr.interest_over_time()
            if df is not None and len(df):
                return df
        except Exception as e:
            print("  429/błąd:", str(e)[:80])
        time.sleep(30 * (proba + 1))
    return None

def main():
    cfg = json.loads((ROOT / "slowa-kluczowe" / "zasieg" / "paczki.json").read_text(encoding="utf-8"))
    kot, geo = cfg["kotwica"], cfg["geo"]
    wyniki = {}
    for p in cfg["paczki"]:
        frazy = [kot] + p
        df = paczka(frazy, geo)
        if df is None:
            print("brak danych:", frazy); continue
        for f in frazy:
            if f == kot and f in wyniki: continue
            seria = [float(x) for x in df[f].tolist()]
            wyniki[f] = {"s12": sredn(seria), "s4": sredn(seria[-4:]), "p4": sredn(seria[-8:-4]),
                         "szczyt": str(df[f].idxmax().date()), "szczyt_wartosc": float(df[f].max())}
        print("ok:", frazy); time.sleep(20)
    k = wyniki[kot]["s12"] or 0.1; k4 = wyniki[kot]["s4"] or 0.1
    out = {}
    for f, v in wyniki.items():
        zm = None if not v["p4"] else round((v["s4"] - v["p4"]) / v["p4"] * 100)
        out[f] = {"zasieg_12m": round(v["s12"] / k * 100, 1), "zasieg_teraz": round(v["s4"] / k4 * 100, 1),
                  "srednia_12m_surowa": v["s12"], "ost_4tyg_surowa": v["s4"], "zmiana_proc": zm, "szczyt": v["szczyt"],
                  "teraz_vs_szczyt_proc": round(v["s4"] / v["szczyt_wartosc"] * 100) if v["szczyt_wartosc"] else 0}
    res = {"czas": teraz().isoformat(timespec="minutes"), "kotwica": kot, "geo": geo, "zbiory": ["pytrends"], "frazy": out}
    (ROOT / "monitoring" / "stan" / "zasieg.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({f: (v["zasieg_12m"], v["zasieg_teraz"]) for f, v in out.items()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
