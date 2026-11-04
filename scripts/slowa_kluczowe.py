#!/usr/bin/env python3
"""Godzinne metryki słów kluczowych: Google Autocomplete (PL) + wzmianki w postach konkurencji.

Wynik: monitoring/stan/slowa-metryki.json (bieżący pomiar z oceną 0–100),
       slowa-kluczowe/historia.csv (dopisywany), slowa-kluczowe/kandydaci.md (nowe frazy).
"""
import csv, json, re, sys, time, unicodedata, urllib.parse, urllib.request, datetime as dt, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wspolne import ROOT, STAN, teraz, json_wczytaj, json_zapisz

KAT = ROOT / "slowa-kluczowe"
# kandydaci zawierający te słowa są pomijani (marketplace'y, sieciówki, krzyżówki itp.)
STOP = ["krzyzowk", "castorama", "obi", "leroy", "allegro", "olx", "ikea", "jysk", "lidl", "biedronka",
        "action", "bricomarche", "pepco", "kaufland", "aldi", "minecraft", "sims", "chomik", "pdf"]
MAX_KANDYDATOW = 30
WAGA_BIZ = {"wysokie": 1.0, "srednie": 0.65, "niskie": 0.35}

def bez_ogonkow(s):
    s = s.lower().replace("ł", "l")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def podpowiedzi(fraza):
    url = "https://suggestqueries.google.com/complete/search?client=firefox&hl=pl&gl=pl&q=" + urllib.parse.quote(fraza)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (klaudiusz-fudali)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))[1]
    except Exception as e:  # sieć/limit – nie przerywamy całego pomiaru
        print(f"autocomplete '{fraza}': {e}", file=sys.stderr)
        return None

def main():
    t = teraz()
    frazy = list(csv.DictReader((KAT / "slowa-kluczowe.csv").open(encoding="utf-8")))
    posty = json_wczytaj(STAN / "posty-30dni.json", [])
    g24 = (t - dt.timedelta(hours=24)).isoformat()[:16]
    g7 = (t - dt.timedelta(days=7)).isoformat()[:10]
    teksty = []
    for p in posty:
        txt = bez_ogonkow((p.get("opis") or "") + " " + " ".join("#" + h for h in p.get("hashtagi") or []))
        teksty.append((p.get("data") or p.get("pobrano") or "", txt,
                       (p.get("polubienia") or 0) + (p.get("komentarze") or 0), p.get("firma")))
    wyniki, znane, kandydaci = [], {bez_ogonkow(f["fraza"]) for f in frazy}, {}
    for f in frazy:
        fr = f["fraza"].strip()
        n = bez_ogonkow(fr)
        wzorce = [re.escape(n), re.escape(n.replace(" ", ""))]  # "altana drewniana" i "#altanadrewniana"
        rx = re.compile("|".join(wzorce))
        traf = [x for x in teksty if rx.search(x[1])]
        w24 = sum(1 for x in traf if x[0][:16] >= g24)
        w7 = sum(1 for x in traf if x[0][:10] >= g7)
        zaang = round(sum(x[2] for x in traf) / len(traf), 1) if traf else 0
        firmy = sorted({x[3] for x in traf if x[3]})
        sug = podpowiedzi(fr)
        time.sleep(0.4)
        # pozycja frazy w podpowiedziach dla jej skróconej wersji (np. "altana drewn" -> "altana drewniana")
        prefiks = fr[:max(3, len(fr) - 4)]
        sug_pref = podpowiedzi(prefiks)
        time.sleep(0.4)
        pozycja = None
        if sug_pref:
            for i, s_ in enumerate(sug_pref):
                if bez_ogonkow(s_) == n:
                    pozycja = i + 1
                    break
        if sug is not None:
            for s_ in sug:
                b = bez_ogonkow(s_)
                if b not in znane and b != n and not any(x in b for x in STOP):
                    kandydaci.setdefault(s_, fr)
        if sug is None and sug_pref is None:
            popyt = None
        else:
            szer = min(len(sug or []), 10) / 10                      # ile rozwinięć ma fraza
            poz = (11 - pozycja) / 10 if pozycja else 0.1            # jak wysoko jest wśród podpowiedzi
            popyt = 0.6 * poz + 0.4 * szer
        # ocena: popyt 45%, konkurencja 25%, zaangażowanie 10%, dopasowanie do oferty 20%
        ocena = 100 * (0.45 * (popyt if popyt is not None else 0.5)
                       + 0.25 * min(w7 / 5, 1) + 0.10 * min(zaang / 200, 1)
                       + 0.20 * WAGA_BIZ.get(f.get("znaczenie_biznesowe", "srednie"), 0.65))
        wyniki.append({"fraza": fr, "grupa": f.get("grupa"), "znaczenie_biznesowe": f.get("znaczenie_biznesowe"),
                       "podpowiedzi_google": sug, "pozycja_w_podpowiedziach": pozycja,
                       "popyt_0_1": None if popyt is None else round(popyt, 2), "liczba_podpowiedzi": None if sug is None else len(sug),
                       "wzmianki_konkurencji_24h": w24, "wzmianki_konkurencji_7d": w7,
                       "srednie_zaangazowanie": zaang, "firmy": firmy, "ocena": round(ocena)})
    # trend względem poprzedniego pomiaru
    poprz = {w["fraza"]: w["ocena"] for w in json_wczytaj(STAN / "slowa-metryki.json", {}).get("frazy", [])}
    for w in wyniki:
        w["zmiana_oceny"] = None if w["fraza"] not in poprz else w["ocena"] - poprz[w["fraza"]]
    wyniki.sort(key=lambda w: w["ocena"], reverse=True)
    json_zapisz(STAN / "slowa-metryki.json", {"czas": t.isoformat(timespec="minutes"),
                                              "postow_w_bazie": len(posty), "frazy": wyniki,
                                              "kandydaci": [{"fraza": k, "z_frazy": v} for k, v in kandydaci.items()]})
    hist = KAT / "historia.csv"
    nowy = not hist.exists()
    with hist.open("a", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        if nowy:
            wr.writerow(["czas", "fraza", "ocena", "popyt", "pozycja_w_podpowiedziach", "liczba_podpowiedzi", "wzmianki_24h", "wzmianki_7d", "srednie_zaangazowanie"])
        for w in wyniki:
            wr.writerow([t.isoformat(timespec="minutes"), w["fraza"], w["ocena"], w["popyt_0_1"], w["pozycja_w_podpowiedziach"], w["liczba_podpowiedzi"],
                         w["wzmianki_konkurencji_24h"], w["wzmianki_konkurencji_7d"], w["srednie_zaangazowanie"]])
    # kandydaci – dopisz tylko nowe
    kp = KAT / "kandydaci.md"
    istn = kp.read_text(encoding="utf-8") if kp.exists() else "# Kandydaci na nowe słowa kluczowe\n\nWykryte automatycznie (podpowiedzi Google). Dodaj wartościowe do `slowa-kluczowe.csv`.\n\n| Fraza | Wykryto przy | Data |\n|---|---|---|\n"
    dop = [f"| {k} | {v} | {t:%Y-%m-%d} |" for k, v in kandydaci.items() if f"| {k} |" not in istn][:MAX_KANDYDATOW]
    kp.write_text(istn + ("\n".join(dop) + "\n" if dop else ""), encoding="utf-8")
    print(f"Zmierzono {len(wyniki)} fraz, nowych kandydatów: {len(dop)}. TOP5: " +
          ", ".join(f"{w['fraza']} ({w['ocena']})" for w in wyniki[:5]))

if __name__ == "__main__":
    main()
