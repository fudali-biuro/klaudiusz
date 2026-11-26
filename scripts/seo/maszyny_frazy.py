#!/usr/bin/env python3
"""Kuba: frazy SEO „maszyny budowlane” (priorytet Pablo 25.11.2026).
Etap 1: podpowiedzi Google (autocomplete) dla fraz + rozszerzenie a–z -> kandydaci long-tail.
Etap 2: Google Trends (pytrends, za darmo) – zasięg względny, kotwica 'koparko ładowarka', kalibracja do 'koparka'=100.
Wyniki: monitoring/stan/maszyny-auto.json, maszyny-trends.json; potem maszyny_csv.py składa slowa-kluczowe/maszyny.csv."""
import json, sys, time, urllib.parse, urllib.request, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from wspolne import ROOT  # noqa

FRAZY = {
 "głowa": ["koparka","koparko-ładowarka","koparko ładowarka","ładowarka","ładowarka kołowa","maszyny budowlane","sprzęt budowlany","minikoparka","koparka kołowa","koparka gąsienicowa","ładowarka teleskopowa","ładowarka przegubowa"],
 "intencja zakupowa": ["koparko-ładowarka na sprzedaż","koparko-ładowarka nowa","nowa koparko-ładowarka","koparko-ładowarka od ręki","koparka na sprzedaż","koparka nowa","ładowarka na sprzedaż","maszyny budowlane na sprzedaż","maszyny budowlane nowe","sprzęt budowlany sprzedaż","koparko-ładowarka dealer","koparko-ładowarka sklep","koparko-ładowarka olx","koparko-ładowarka otomoto","koparko-ładowarka allegro","koparko-ładowarka używana"],
 "cena i finansowanie": ["koparko-ładowarka cena","ile kosztuje koparko-ładowarka","koparko-ładowarka cennik","koparko-ładowarka leasing","leasing koparki","leasing maszyn budowlanych","koparko-ładowarka rata","koparko-ładowarka kredyt","koparko-ładowarka netto","tania koparko-ładowarka","koparka cena","ładowarka cena"],
 "chińskie i marki": ["chińska koparko-ładowarka","chińska koparka","chińskie maszyny budowlane","chińska ładowarka","koparko-ładowarka chińska opinie","chińska koparko-ładowarka czy warto","shanmon","shanmon koparko-ładowarka","shanmon opinie","shanmon fuji","shanmon fuji 388","fuji 388"],
 "modele Shanmon": ["shanmon 377","shanmon 388","shanmon 388-ii","shanmon 388t","shanmon 388h","shanmon 398h","shanmon 378h","shanmon wz30-25","shanmon wz30-25 koparko-ładowarka","shanmon 388 cena","shanmon 388h cena","shanmon 398h cena","shanmon 377 cena"],
 "porównania": ["jcb 3cx","jcb 3cx cena","jcb 3cx alternatywa","alternatywa dla jcb","tańsza alternatywa jcb","cat 432","cat 428","koparko-ładowarka jcb","koparko-ładowarka cat","koparko-ładowarka case","koparko-ładowarka volvo","koparko-ładowarka komatsu","chińska koparko-ładowarka vs jcb","jcb czy chińska koparka","koparko-ładowarka ranking","najlepsza koparko-ładowarka"],
 "serwis i gwarancja": ["koparko-ładowarka serwis","koparko-ładowarka gwarancja","koparko-ładowarka części","koparko-ładowarka osprzęt","koparko-ładowarka łyżka","koparko-ładowarka jazda próbna","serwis maszyn budowlanych","części do koparek"],
 "miasta i regiony": ["koparko-ładowarka rzeszów","koparka rzeszów","maszyny budowlane rzeszów","koparko-ładowarka podkarpacie","koparko-ładowarka kraków","koparko-ładowarka małopolska","koparko-ładowarka warszawa","koparko-ładowarka lublin","koparko-ładowarka katowice","koparko-ładowarka tarnów","koparko-ładowarka przemyśl","koparko-ładowarka krosno","koparko-ładowarka mielec","koparko-ładowarka stalowa wola","koparko-ładowarka sprzedaż polska","sprzęt budowlany podkarpacie","wynajem koparko-ładowarki rzeszów"],
}
SEEDY_ROZSZ = ["koparko-ładowarka","koparka","ładowarka","maszyny budowlane","chińska koparka","shanmon","jcb 3cx","koparko-ładowarka cena","koparko-ładowarka nowa","koparko-ładowarka leasing","koparka kołowa","minikoparka"]

def auto(q):
    u = "https://suggestqueries.google.com/complete/search?client=firefox&hl=pl&gl=pl&q=" + urllib.parse.quote(q)
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(u, timeout=15))[1]
        except Exception:
            time.sleep(2)
    return []

def etap1():
    wszystkie = [f for g in FRAZY.values() for f in g]
    out = {"podpowiedzi": {}, "rozszerzenie": {}}
    for f in wszystkie:
        out["podpowiedzi"][f] = auto(f); time.sleep(0.25)
    for s in SEEDY_ROZSZ:
        zbior = []
        for lit in "abcdefghijklmnoprstuwyz":
            for x in auto(s + " " + lit):
                if x not in zbior: zbior.append(x)
            time.sleep(0.2)
        out["rozszerzenie"][s] = zbior
    (ROOT / "monitoring" / "stan" / "maszyny-auto.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("etap1: frazy", len(wszystkie), "rozszerzeń", sum(len(v) for v in out["rozszerzenie"].values()))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "etap1": etap1()

def etap2():
    from pytrends.request import TrendReq
    kot = "koparko ładowarka"
    wszystkie = [f for g in FRAZY.values() for f in g]
    # Trends nie rozróżnia myślnika – normalizuj, deduplikuj
    def norm(s): return s.replace("-", " ")
    uniq = []
    for f in wszystkie:
        n = norm(f)
        if n not in uniq and n != kot and n != "koparka": uniq.append(n)
    wyn = {}
    def paczka(frazy):
        for proba in range(4):
            try:
                tr = TrendReq(hl="pl-PL", tz=-60, timeout=(10, 30))
                tr.build_payload(frazy, timeframe="today 12-m", geo="PL")
                df = tr.interest_over_time()
                if df is not None and len(df): return df
            except Exception as e:
                print("  błąd:", str(e)[:60])
            time.sleep(30 * (proba + 1))
        return None
    def sr(xs): return round(sum(xs)/len(xs), 1) if xs else 0.0
    # kalibracja koparka vs koparko ładowarka
    df = paczka(["koparka", kot, "maszyny budowlane", "ładowarka", "minikoparka"])
    if df is not None:
        for f in ["koparka", kot, "maszyny budowlane", "ładowarka", "minikoparka"]:
            s = [float(x) for x in df[f].tolist()]
            wyn[f] = {"s12": sr(s), "s4": sr(s[-4:]), "p4": sr(s[-8:-4]), "szczyt": str(df[f].idxmax().date())}
        print("kalibracja ok", flush=True)
    time.sleep(15)
    for i in range(0, len(uniq), 4):
        paczka_f = [kot] + uniq[i:i+4]
        df = paczka(paczka_f)
        if df is None: print("brak:", paczka_f, flush=True); continue
        for f in paczka_f:
            if f == kot: continue
            s = [float(x) for x in df[f].tolist()]
            wyn[f] = {"s12": sr(s), "s4": sr(s[-4:]), "p4": sr(s[-8:-4]), "szczyt": str(df[f].idxmax().date()), "wzgl_kot": True}
        print("ok", paczka_f, flush=True); time.sleep(15)
        (ROOT / "monitoring" / "stan" / "maszyny-trends.json").write_text(json.dumps(wyn, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "monitoring" / "stan" / "maszyny-trends.json").write_text(json.dumps(wyn, ensure_ascii=False, indent=1), encoding="utf-8")
    print("etap2 KONIEC", len(wyn), flush=True)

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "etap2": etap2()
