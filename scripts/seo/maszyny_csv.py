#!/usr/bin/env python3
"""Kuba: składa slowa-kluczowe/maszyny.csv i dopisuje seo/pozycje/historia.csv z maszyny-auto.json + maszyny-trends*.json."""
import csv, json, re, sys, os, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from wspolne import ROOT
sys.path.insert(0, os.path.dirname(__file__))
from maszyny_frazy import FRAZY

auto = json.loads((ROOT/"monitoring/stan/maszyny-auto.json").read_text(encoding="utf-8"))
tr = json.loads((ROOT/"monitoring/stan/maszyny-trends.json").read_text(encoding="utf-8"))
trk = {}
p = ROOT/"monitoring/stan/maszyny-trends-kand.json"
if p.exists(): trk = json.loads(p.read_text(encoding="utf-8"))
norm = lambda s: s.replace("-", " ")
kop = tr.get("koparka", {}); kot = tr.get("koparko ładowarka", {})
# kalibracja: wartości w paczkach są względem 'koparko ładowarka' (=100). Przeliczenie na skalę koparka=100 przez kalibrację.
wsp = (kot.get("s12", 0) / kop.get("s12", 1)) if kop.get("s12") else None  # ile koparko ładowarka to w skali koparka=100
wsp4 = (kot.get("s4", 0) / kop.get("s4", 1)) if kop.get("s4") else None

def zas(f):
    """Skala: 'koparko ładowarka' = 100 (kotwica; ten sam zakres co handel maszynami). Wartość = średnia 12 mies. frazy / średnia kotwicy w TEJ SAMEJ paczce."""
    k = norm(f)
    d = tr.get(k) or trk.get(k)
    if k == "koparko ładowarka": return 100.0, kot.get("s4"), kot.get("p4"), kot.get("szczyt"), "kotwica"
    if not d: return None, None, None, None, "brak"
    if k in ("koparka", "maszyny budowlane", "ładowarka", "minikoparka"):
        base12, base4, basep = kot.get("s12"), kot.get("s4"), kot.get("p4")
        z = round(d["s12"] / base12 * 100, 1) if base12 else None
        return z, d["s4"], d["p4"], d["szczyt"], "kalibracja"
    k12 = d.get("k12")
    if not k12: return None, None, None, d.get("szczyt"), "brak kotwicy"
    z = round(d["s12"] / k12 * 100, 1)
    # trend: zmiana frazy w ostatnich 4 tyg. względem poprzednich 4 (surowo)
    return z, d["s4"], d["p4"], d.get("szczyt"), "paczka"

def trend(s4, p4):
    if s4 is None or p4 is None: return ""
    if p4 == 0: return "nowy" if s4 else "0"
    return f"{round((s4 - p4) / p4 * 100):+d}%"

# intencja / trudność (OSZACOWANIE – brak danych SERP/GSC; patrz README w pliku maszyny-uwagi)
def ocena(f, grupa, n_pod):
    s = f.lower()
    if s in ("koparka", "ładowarka", "ładowarka kołowa", "maszyny budowlane", "sprzęt budowlany"):
        return "informacyjna/mieszana", "wysoka", "A-zasięg: szeroka, zaśmiecona (zabawki, telefon, dzieci) – nie celować wprost, tylko wspierać"
    if any(x in s for x in ("olx", "otomoto", "allegro")):
        return "zakup (portale)", "wysoka", "dominują portale ogłoszeniowe – nasza droga: własne ogłoszenia + podstrona produktu"
    if grupa == "modele Shanmon" or "shanmon" in s or "fuji" in s:
        return "marka/model", "niska", "praktycznie brak polskiej konkurencji; w Google tylko ru/en – ruch ≈0, wartość = zbudowanie marki"
    if any(x in s for x in ("alternatywa", "vs jcb", "czy chińska", "tańsza")):
        return "porównanie", "niska", "pustka w podpowiedziach – okazja na poradnik/podstronę"
    if "leasing" in s or "rata" in s or "kredyt" in s:
        return "finansowanie", "średnia", "leasingowcy, dealerzy marek, porównywarki"
    if "chińsk" in s:
        return "zakup/porównanie", "średnia", "sklepy z minikoparkami, Allegro, OLX"
    if any(x in s for x in ("jcb", "cat ", "cat4", "case", "volvo", "komatsu", "bobcat")):
        return "porównanie/marka", "wysoka", "dealerzy i producenci marek w TOP10; wchodzimy przez porównania"
    if group_city(f):
        return "lokalna (miasto)", "niska-średnia", "w podpowiedziach przeważa „usługi/kurs/praca” (wynajem, nie zakup) – sprawdzać intencję"
    if any(x in s for x in ("cena", "ile kosztuje", "cennik", "netto", "tania")):
        return "cena", "średnia", "cena bywa „za godzinę” (usługi) – frazy kupujących: „nowa/cena nowa”"
    if any(x in s for x in ("nowa", "nowe", "od ręki", "sprzedaż", "na sprzedaż", "dealer", "sklep")):
        return "zakup", "średnia-wysoka", "portale + dealerzy"
    if any(x in s for x in ("serwis", "gwarancja", "części", "osprzęt", "łyżka", "jazda próbna")):
        return "serwis/obsługa", "średnia", "pojedyncze podpowiedzi – temat do FAQ/poradnika"
    return "mieszana", "średnia", ""

def group_city(f):
    return bool(re.search(r"rzesz|podkarp|krak|małopol|warszaw|lublin|katowic|tarnów|przemyś|kros|mielec|stalowa", f.lower()))

def prio(f, zasieg, n_pod, intent):
    s = f.lower()
    if intent.startswith("marka/model") or "alternatywa" in s or "vs jcb" in s: return "A"
    if any(x in s for x in ("nowa", "chińsk", "cena", "leasing")) and "koparko" in s: return "A"
    if intent in ("lokalna (miasto)",): return "B"
    if zasieg and zasieg >= 5: return "A"
    return "B" if n_pod >= 3 else "C"

wiersze = []
for g, lista in FRAZY.items():
    for f in lista:
        n_pod = len(auto["podpowiedzi"].get(f, []))
        z, s4, p4, szczyt, tryb = zas(f)
        intent, trud, uz = ocena(f, g, n_pod)
        wiersze.append({"fraza": f, "grupa": g, "intencja": intent, "podpowiedzi_google_0_10": n_pod,
                        "zasieg_wzgl_kopladowarka=100": z if z is not None else "", "trend_4tyg": trend(s4, p4),
                        "szczyt_roku": szczyt or "", "trudnosc_szac": trud, "uzasadnienie_trudnosci": uz,
                        "priorytet": prio(f, z, n_pod, intent), "zrodlo": "autocomplete+Trends 26.11" if z is not None else "autocomplete 26.11 (Trends: brak danych)"})
# kandydaci long-tail z pomiaru
for f, d in trk.items():
    z, s4, p4, szczyt, tryb = zas(f)
    n_pod = len(auto["podpowiedzi"].get(f, [])) if f in auto["podpowiedzi"] else ""
    intent, trud, uz = ocena(f, "kandydat", n_pod or 0)
    wiersze.append({"fraza": f, "grupa": "kandydat long-tail", "intencja": intent, "podpowiedzi_google_0_10": n_pod,
                    "zasieg_wzgl_kopladowarka=100": z if z is not None else "", "trend_4tyg": trend(s4, p4), "szczyt_roku": szczyt or "",
                    "trudnosc_szac": trud, "uzasadnienie_trudnosci": uz, "priorytet": prio(f, z, 3, intent),
                    "zrodlo": "rozszerzenie a–z + Trends 26.11"})
SZUM = {"ładowarka": "dominuje ładowarka do telefonu/samochodu – wartość bez znaczenia dla maszyn",
        "minikoparka": "inny segment (małe koparki, ogród/budowa) – nie nasza maszyna",
        "ładowarka teleskopowa": "inny segment (Manitou/JCB Loadall) – nie nasza maszyna",
        "ładowarka przegubowa": "inny segment", "koparka kołowa": "inny segment (koparki kołowe 8–20 t)",
        "koparka gąsienicowa": "inny segment", "ładowarka kołowa": "ładowarka kołowa – inny segment (ale pokrewna)",
        "koparka": "bardzo szeroka (zabawki, bitcoin, dzieci) – tylko tło sezonowe", "maszyny budowlane": "szeroka (dzieci, zabawki, firmy) – tło",
        "sprzęt budowlany": "szeroka (wynajem/wypożyczalnie) – inna intencja", "ładowarka cena": "głównie ładowarka do telefonu – ignorować",
        "koparka cena": "głównie „cena za godzinę” (usługi) – ignorować"}
for r in wiersze:
    k = r["fraza"]
    if k in SZUM:
        r["priorytet"] = "C" if k in ("ładowarka","minikoparka","ładowarka teleskopowa","ładowarka przegubowa","koparka kołowa","koparka gąsienicowa","ładowarka cena","koparka cena","sprzęt budowlany","ładowarka kołowa") else "B"
        r["uzasadnienie_trudnosci"] = (r["uzasadnienie_trudnosci"] + " | UWAGA: " + SZUM[k]).strip(" |")
    z = r["zasieg_wzgl_kopladowarka=100"]
    # wiarygodność: Trends zaokrągla do całych liczb – niskie wartości = szum
    r["wiarygodnosc_zasiegu"] = "" if z == "" else ("dobra" if float(z) >= 5 else ("słaba (≈0, Trends zaokrągla)" if float(z) >= 1 else "brak sygnału (<1)"))
    if z != "" and float(z) < 1: r["trend_4tyg"] = "n/d"
wiersze.sort(key=lambda r: ({"A": 0, "B": 1, "C": 2}[r["priorytet"]], -(r["zasieg_wzgl_kopladowarka=100"] or 0) if r["zasieg_wzgl_kopladowarka=100"] != "" else 0))
pol = list(wiersze[0].keys())
with open(ROOT/"slowa-kluczowe/maszyny.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=pol); w.writeheader(); w.writerows(wiersze)
# historia pozycji (dopisz; pozycje FUDALI = brak danych bez Search Console)
h = ROOT/"seo/pozycje/historia.csv"; h.parent.mkdir(parents=True, exist_ok=True)
nowy = not h.exists()
with open(h, "a", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    if nowy: w.writerow(["data", "fraza", "pozycja_fudali", "url", "zasieg_wzgl_kopladowarka=100", "trend_4tyg", "zrodlo", "uwagi"])
    dzis = datetime.date.today().isoformat()
    for r in wiersze:
        if r["priorytet"] == "A":
            w.writerow([dzis, r["fraza"], "", "", r["zasieg_wzgl_kopladowarka=100"], r["trend_4tyg"], "Kuba: Trends+autocomplete", "pozycja do uzupełnienia po podpięciu Google Search Console"])
print("wierszy:", len(wiersze), "A:", sum(r["priorytet"] == "A" for r in wiersze))
