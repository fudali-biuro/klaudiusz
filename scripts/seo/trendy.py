#!/usr/bin/env python3
"""Bartek: Google Trends przez Apify (aktor apify/google-trends-scraper).

Porównuje grupy fraz z seo/trendy-grupy.json (max 5 fraz w grupie, jedna wspólna skala 0–100 w grupie).
Wynik: monitoring/stan/trendy.json (surowe dane) + seo/trendy/RRRR-MM-DD.md (tabele; wnioski dopisuje Claude).

Użycie:
  python3 scripts/seo/trendy.py                 # nowy pomiar (każda grupa osobno, równolegle; koszt Apify ok. 0,1 USD za grupę)
  python3 scripts/seo/trendy.py --dataset ID    # użyj gotowych wyników (bez nowego scrapowania), można kilka po przecinku
"""
import argparse, json, os, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from wspolne import ROOT, teraz  # noqa: E402

AKTOR = "apify~google-trends-scraper"
API = "https://api.apify.com/v2"


def api(sciezka, dane=None, metoda=None):
    tok = os.environ["APIFY_API_KEY"]
    url = f"{API}{sciezka}{'&' if '?' in sciezka else '?'}token={tok}"
    req = urllib.request.Request(url, data=json.dumps(dane).encode() if dane is not None else None,
                                 headers={"Content-Type": "application/json"}, method=metoda)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def start(geo, frazy):
    wejscie = {"searchTerms": [",".join(frazy)], "isMultiple": True, "geo": geo,
               "skipDebugScreen": True, "timeRange": "", "maxRequestRetries": 4}
    if geo:
        wejscie["viewedFrom"] = geo.lower()
    for proba in range(40):  # plan FREE: max 16 GB pamięci naraz – przy braku miejsca (402) czekamy
        try:
            run = api(f"/acts/{AKTOR}/runs?timeout=900&memory=2048", wejscie)["data"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 402 or proba == 39:
                raise
            time.sleep(15)
    print(f"Apify: start {run['id']} – {', '.join(frazy)} ({geo or 'świat'})")
    return run["id"]


def czekaj(ids):
    """Czeka na wszystkie przebiegi (równolegle); zwraca listę ID zbiorów danych."""
    zbiory, koszt = {}, 0.0
    for _ in range(170):
        for rid in [r for r in ids if r not in zbiory]:
            run = api(f"/actor-runs/{rid}")["data"]
            if run["status"] not in ("READY", "RUNNING"):
                zbiory[rid] = run["defaultDatasetId"]; koszt += run.get("usageTotalUsd", 0) or 0
                print(f"Apify: {rid} -> {run['status']}")
        if len(zbiory) == len(ids):
            break
        time.sleep(6)
    print(f"Apify: łączny koszt ~{koszt:.2f} USD")
    return list(zbiory.values())


def pobierz(dataset):
    return api(f"/datasets/{dataset}/items?clean=true")


def sredn(xs):
    return round(sum(xs) / len(xs), 1) if xs else 0


def analiza(item, frazy):
    tl = [t for t in item.get("interestOverTime_timelineData", []) if t.get("value")]
    wiersze = []
    for i, f in enumerate(frazy):
        seria = [t["value"][i] if i < len(t["value"]) else 0 for t in tl]
        ost, poprz = seria[-4:], seria[-8:-4]
        szczyt = max(range(len(seria)), key=lambda k: seria[k]) if seria else 0
        zmiana = None if not sredn(poprz) else round((sredn(ost) - sredn(poprz)) / sredn(poprz) * 100)
        wiersze.append({"fraza": f, "srednia_12m": sredn(seria), "ost_4tyg": sredn(ost), "poprz_4tyg": sredn(poprz),
                        "zmiana_proc": zmiana, "szczyt_tydzien": tl[szczyt]["formattedAxisTime"] if tl else "",
                        "szczyt_wartosc": seria[szczyt] if seria else 0,
                        "teraz_vs_szczyt_proc": round(sredn(ost) / seria[szczyt] * 100) if seria and seria[szczyt] else 0})
    podk = next((r["value"][0] for r in item.get("interestBySubregion", []) if r.get("geoCode") == "PL-PK"), None)
    return {"wiersze": wiersze, "powiazane_top": [q["query"] for q in item.get("relatedQueries_top", [])[:8]],
            "powiazane_rosnace": [f"{q['query']} ({q.get('formattedValue', '')})" for q in item.get("relatedQueries_rising", [])[:8]],
            "podkarpackie_1sza_fraza": podk}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", help="ID gotowych zbiorów Apify, po przecinku")
    a = ap.parse_args()
    if not os.environ.get("APIFY_API_KEY"):
        sys.exit("Brak APIFY_API_KEY – trzeba dodać klucz w ustawieniach środowiska.")
    grupy = json.loads((ROOT / "seo" / "trendy-grupy.json").read_text(encoding="utf-8"))["grupy"]
    if a.dataset:
        zbiory = a.dataset.split(",")
    else:
        zbiory = czekaj([start(g["geo"], g["frazy"]) for g in grupy])
    items = [it for d in zbiory for it in pobierz(d)]
    po_kluczu = {it.get("searchTerm", ""): it for it in items}
    wynik = {"czas": teraz().isoformat(timespec="minutes"), "zbiory": zbiory, "grupy": []}
    for g in grupy:
        it = po_kluczu.get(",".join(g["frazy"]))
        wynik["grupy"].append({**g, **(analiza(it, g["frazy"]) if it else {"brak_danych": True})})
    (ROOT / "monitoring" / "stan").mkdir(parents=True, exist_ok=True)
    (ROOT / "monitoring" / "stan" / "trendy.json").write_text(json.dumps(wynik, ensure_ascii=False, indent=1), encoding="utf-8")

    dzis = teraz().strftime("%Y-%m-%d")
    md = [f"# Google Trends – {dzis} (Bartek)", "",
          "Skala 0–100 **wewnątrz grupy** (100 = najwyższe zainteresowanie którejkolwiek frazy w grupie w ciągu 12 mies.). "
          "Dane tygodniowe, ostatnie 12 miesięcy. Źródło: Google Trends przez Apify.", ""]
    for g in wynik["grupy"]:
        md += [f"## {g['nazwa']} ({g['geo'] or 'świat'})", ""]
        if g.get("brak_danych"):
            md += ["_Brak danych w tym przebiegu (Google nie oddał wyników) – spróbuj ponownie za tydzień._", ""]
            continue
        md += ["| Fraza | Średnio 12 mies. | Ostatnie 4 tyg. | Poprzednie 4 tyg. | Zmiana | Szczyt (tydzień) | Teraz vs szczyt |",
               "|---|---|---|---|---|---|---|"]
        for w in sorted(g["wiersze"], key=lambda w: -w["srednia_12m"]):
            zm = "—" if w["zmiana_proc"] is None else f"{w['zmiana_proc']:+d}%"
            md.append(f"| {w['fraza']} | {w['srednia_12m']} | {w['ost_4tyg']} | {w['poprz_4tyg']} | {zm} | "
                      f"{w['szczyt_tydzien']} ({w['szczyt_wartosc']}) | {w['teraz_vs_szczyt_proc']}% |")
        if g["powiazane_top"]:
            md += ["", "**Powiązane wyszukiwania (top):** " + ", ".join(g["powiazane_top"])]
        if g["powiazane_rosnace"]:
            md += ["", "**Rosnące:** " + ", ".join(g["powiazane_rosnace"])]
        if g.get("podkarpackie_1sza_fraza") is not None:
            md += ["", f"Podkarpackie (fraza „{g['frazy'][0]}”): {g['podkarpackie_1sza_fraza']}/100 względem najmocniejszego województwa."]
        md.append("")
    md += ["## Wnioski i rekomendacje", "", "_(uzupełnia Bartek: co rośnie, sezonowość, TOP 3 na tydzień, co dla Oli, co na stronę)_", ""]
    out = ROOT / "seo" / "trendy" / f"{dzis}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"Zapisano {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
