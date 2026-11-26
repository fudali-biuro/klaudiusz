#!/usr/bin/env python3
"""Kuba: dopełnienie – kandydaci long-tail (z rozszerzenia a–z) mierzeni w Trends (kotwica 'koparko ładowarka'). Wynik: maszyny-trends-kand.json"""
import json, sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from wspolne import ROOT
from pytrends.request import TrendReq
KAND = ["chińska koparko ładowarka cena","koparko ładowarka sany","koparko ładowarka hidromek","koparko ładowarka waryński","koparko ładowarka terex","koparko ładowarka new holland","koparko ładowarka hydrema","koparko ładowarka mecalac","mini koparko ładowarka","koparko ładowarka do 100 tys","koparko ładowarka do 150 tys","koparko ładowarka cena za godzinę","koparko ładowarka jcb 4cx","koparko ładowarka case 580","koparko ładowarka volvo bl71","koparko ładowarka aliexpress","koparko ładowarka elektryczna","koparko ładowarka cesja leasingu","chińska koparka opinie","chińska koparka sany","shanmon backhoe loader","shanmon loader","shanmon 388h carraro","shanmon wheel loader","jcb 3cx czy 4cx","jcb 3cx eco opinie","koparko ładowarka egzamin","koparko ładowarka kurs"]
def sr(xs): return round(sum(xs)/len(xs),1) if xs else 0.0
def paczka(fr):
    for p in range(4):
        try:
            tr=TrendReq(hl="pl-PL",tz=-60,timeout=(10,30)); tr.build_payload(fr,timeframe="today 12-m",geo="PL")
            df=tr.interest_over_time()
            if df is not None and len(df): return df
        except Exception as e: print("błąd",str(e)[:50],flush=True)
        time.sleep(30*(p+1))
kot="koparko ładowarka"; w={}
for i in range(0,len(KAND),4):
    fr=[kot]+KAND[i:i+4]; df=paczka(fr)
    if df is None: continue
    for f in fr:
        if f==kot: continue
        s=[float(x) for x in df[f].tolist()]
        w[f]={"s12":sr(s),"s4":sr(s[-4:]),"p4":sr(s[-8:-4]),"szczyt":str(df[f].idxmax().date())}
    print("ok",fr,flush=True); time.sleep(15)
    (ROOT/"monitoring"/"stan"/"maszyny-trends-kand.json").write_text(json.dumps(w,ensure_ascii=False,indent=1),encoding="utf-8")
print("KAND KONIEC",flush=True)
