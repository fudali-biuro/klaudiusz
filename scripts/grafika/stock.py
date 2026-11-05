#!/usr/bin/env python3
"""Zosia: pobiera darmowe zdjęcia tła (salony, tarasy, ogrody, zima…) z Openverse – tylko licencje CC0 / domena publiczna
(użycie komercyjne, bez obowiązku podpisu). NIE Getty / NIE zdjęcia konkurencji.
Użycie: python3 scripts/grafika/stock.py <temat-folder> "<zapytanie EN>" [ile=6]
Wynik: marketing/zdjecia/tla/<temat>/<id>.jpg + <id>.json (tytuł, autor, licencja, źródło) + podglad.jpg"""
import json, os, sys, urllib.request, urllib.parse, io
from PIL import Image
temat, q = sys.argv[1], sys.argv[2]; ile = int(sys.argv[3]) if len(sys.argv) > 3 else 6
O = f"marketing/zdjecia/tla/{temat}/"; os.makedirs(O, exist_ok=True)
UA = {"User-Agent": "FudaliBot/1.0 (biuro@fudali.com.pl)"}
url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "cc0", "page_size": 20})
import time
for proba in range(4):
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()); break
    except Exception as e:
        print("Openverse:", str(e)[:60], "– ponawiam"); time.sleep(5)
else:
    sys.exit("Openverse nie odpowiada")
n = 0; tiles = []
for r in d.get("results", []):
    if n >= ile: break
    if (r.get("width") or 0) < 1400 or (r.get("height") or 0) < 1000: continue
    f = O + r["id"][:8] + ".jpg"
    if os.path.exists(f): continue
    try:
        raw = urllib.request.urlopen(urllib.request.Request(r["url"], headers=UA), timeout=60).read()
        im = Image.open(io.BytesIO(raw)).convert("RGB"); im.thumbnail((2400, 2400)); im.save(f, quality=92)
    except Exception as e:
        print("pominięto", r["url"][:70], str(e)[:60]); continue
    json.dump({"tytul": r.get("title"), "autor": r.get("creator"), "licencja": r.get("license"), "zrodlo": r.get("foreign_landing_url"), "plik_url": r["url"]},
              open(f[:-4] + ".json", "w"), ensure_ascii=False, indent=1)
    print("OK", f, r.get("license"), r.get("source"), (r.get("title") or "")[:50]); n += 1
