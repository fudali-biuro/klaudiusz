#!/usr/bin/env python3
"""Kuba: porównanie ZASIĘGU fraz na jednej skali.

Google Trends porównuje max 5 fraz naraz (skala 0-100 w grupie). Żeby porównać wszystkie, każda paczka dostaje tę samą
frazę-kotwicę; wartości przeliczamy na skalę kotwicy (kotwica = 100 średniego zainteresowania z 12 mies.).
Wynik: monitoring/stan/zasieg.json (surowe), slowa-kluczowe/zasieg/RRRR-MM-DD.md (tabela rankingowa).

  python3 scripts/seo/zasieg.py                     # paczki z slowa-kluczowe/zasieg/paczki.json (koszt ok. 0,07 USD / paczka)
  python3 scripts/seo/zasieg.py --dataset ID,ID     # gotowe zbiory Apify
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from wspolne import ROOT, teraz  # noqa: E402
import trendy  # noqa: E402

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dataset")
    a = ap.parse_args()
    if not os.environ.get("APIFY_API_KEY"):
        sys.exit("Brak APIFY_API_KEY")
    cfg = json.loads((ROOT / "slowa-kluczowe" / "zasieg" / "paczki.json").read_text(encoding="utf-8"))
    kot, geo, paczki = cfg["kotwica"], cfg["geo"], cfg["paczki"]
    zbiory = a.dataset.split(",") if a.dataset else trendy.czekaj([trendy.start(geo, [kot] + p) for p in paczki])
    items = {it.get("searchTerm", ""): it for d in zbiory for it in trendy.pobierz(d)}
    wyniki = {}
    for p in paczki:
        frazy = [kot] + p
        it = items.get(",".join(frazy))
        if not it:
            print("brak danych:", frazy); continue
        w = {r["fraza"]: r for r in trendy.analiza(it, frazy)["wiersze"]}
        k = w[kot]["srednia_12m"] or 0.1
        k4 = w[kot]["ost_4tyg"] or 0.1
        for f in frazy:
            if f == kot and f in wyniki: continue
            wyniki[f] = {"zasieg_12m": round(w[f]["srednia_12m"] / k * 100, 1),
                         "zasieg_teraz": round(w[f]["ost_4tyg"] / k4 * 100, 1) if w[f]["ost_4tyg"] else 0.0,
                         "srednia_12m_surowa": w[f]["srednia_12m"], "ost_4tyg_surowa": w[f]["ost_4tyg"],
                         "zmiana_proc": w[f]["zmiana_proc"], "szczyt": w[f]["szczyt_tydzien"],
                         "teraz_vs_szczyt_proc": w[f]["teraz_vs_szczyt_proc"]}
    out = {"czas": teraz().isoformat(timespec="minutes"), "kotwica": kot, "geo": geo, "zbiory": zbiory, "frazy": wyniki}
    (ROOT / "monitoring" / "stan" / "zasieg.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({f: (v["zasieg_12m"], v["zasieg_teraz"]) for f, v in wyniki.items()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
