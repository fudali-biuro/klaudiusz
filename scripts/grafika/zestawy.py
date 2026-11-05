#!/usr/bin/env python3
"""Zosia: zdjęcia z 2–3 produktami FUDALI w jednej scenie (zlecenie Pablo 05.11.2026).
Najpierw składa kolaż-referencję z oryginalnych zdjęć produktów (z zachowaniem względnych rozmiarów), potem scena.py.
Użycie: ZRODLA=<katalog ze zdjęciami ze strony> python3 scripts/grafika/zestawy.py"""
import os, subprocess, sys
from PIL import Image
Z = os.environ["ZRODLA"]; P = "marketing/zdjecia/packshoty/surowe/"; O = "marketing/zdjecia/zestawy/surowe/"
SRC = {"lezak": P + "lezak-c-bialy.jpg", "stolik": P + "stolik-c-bialy.jpg" if os.path.exists(P + "stolik-c-bialy.jpg") else f"{Z}/2144-0.jpg",
       "stolki": P + "stolki-c-bialy.jpg", "podkladka": P + "podkladka-c-bialy.jpg", "otwieracz": f"{Z}/2146-0.jpg"}
OPIS = {"lezak": "the folding lounge chair with white pillow", "stolik": "the flower-shaped side table with black vase and white roses",
        "stolki": "the round stool set on castors", "podkladka": "the round walnut flower coaster", "otwieracz": "the two wooden cat bottle openers"}
ZESTAWY = {  # nazwa: ([(produkt, wysokość względna)], scena)
 "lezak-stolik": ([("lezak", 1.0), ("stolik", 0.6)], "on a light blonde oak floor next to each other, the side table placed right beside the lounge chair, cream wall, soft daylight"),
 "lezak-stolik-stolki": ([("lezak", 1.0), ("stolik", 0.55), ("stolki", 0.55)], "arranged together as a calm interior corner on a light blonde oak floor, cream wall, soft daylight"),
 "stolik-stolki": ([("stolik", 1.0), ("stolki", 1.0)], "side by side on a light blonde oak floor, cream wall, soft daylight, catalog look"),
 "drobiazgi": ([("podkladka", 0.8), ("otwieracz", 1.0)], "arranged together on a light oak wooden tabletop, the coaster lying flat and the two cat openers standing next to it, blurred cream wall, soft daylight"),
}
def kolaz(skladniki, out):
    H = 900; ims = []
    for p, h in skladniki:
        im = Image.open(SRC[p]).convert("RGB"); im.thumbnail((2000, 2000)); r = int(H * h) / im.height
        ims.append(im.resize((int(im.width * r), int(H * h))))
    W = sum(i.width for i in ims) + 40 * (len(ims) + 1)
    c = Image.new("RGB", (W, H + 80), "white"); x = 40
    for i in ims: c.paste(i, (x, H + 40 - i.height)); x += i.width + 40
    c.save(out)
os.makedirs(O, exist_ok=True)
for nazwa, (skl, scena) in ZESTAWY.items():
    out = f"{O}{nazwa}.jpg"
    if os.path.exists(out): continue
    ref = f"/tmp/kolaz-{nazwa}.jpg"; kolaz(skl, ref)
    opis = ("Square studio packshot with multiple products together: " + ", ".join(OPIS[p] for p, _ in skl) +
            ". The reference image shows the products side by side on white – keep EACH product exactly as in the reference, never merge or redesign them, "
            "keep their relative sizes, remove any text or captions. Place them " + scena + ". Gentle natural shadows, nothing else in the scene.")
    r = subprocess.run([sys.executable, "scripts/grafika/scena.py", "--proporcje", "1:1", "--zdjecie", ref, "--opis", opis, "--wyjscie", out], capture_output=True, text=True)
    print("OK" if r.returncode == 0 else "BŁĄD", out, r.stderr[-200:] if r.returncode else "", flush=True)
