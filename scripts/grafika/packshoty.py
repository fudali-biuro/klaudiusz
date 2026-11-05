#!/usr/bin/env python3
"""Zosia: seria czystych packshotów 1:1 (styl zatwierdzony przez Pablo 05.11.2026) – produkty ze strony fudali.com.pl na jasnym dębie.
Użycie: ZRODLA=<katalog ze zdjęciami> python3 scripts/grafika/packshoty.py   (istniejące pliki pomija)"""
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
Z = os.environ["ZRODLA"]; O = "marketing/zdjecia/packshoty/surowe/"
LEZAK = "marketing/zdjecia/lezak/03-packshot-naturalny.jpg"
PRODUKTY = {  # id: (zdjęcie źródłowe, opis produktu)
 "lezak": (LEZAK, "the folding lounge chair with its white pillow"),
 "stolki": (f"{Z}/2149-1.jpg", "the stool set with a castor trolley, exactly as in the reference"),
 "podkladka": (f"{Z}/2148-1.jpg", "the round dark walnut coaster with flower-shaped cut-outs, lying flat"),
 "otwieracz": (f"{Z}/2146-0.jpg", "the two wooden cat bottle openers (front and back), standing upright side by side, exactly as in the reference"),
 "taboret": (f"{Z}/2145-0.jpg", "the folding wooden stool with rope"),
 "stolik": (f"{Z}/2144-0.jpg", "the side table with flower-shaped wooden top, black vase and white roses"),
}
TLA = {
 "a-dab": "on a light blonde oak floor, soft daylight from the left, softly blurred warm cream wall behind, gentle natural shadow.",
 "b-blat": "on a light oak wooden tabletop with fine visible grain, slightly closer view, soft diffused daylight, blurred pale cream wall behind, gentle natural shadow.",
 "c-bialy": "on a seamless warm off-white studio background with a soft natural shadow beneath, clean minimal catalog look.",
}
BASE = "Square studio packshot of {p}. Product centered and fully visible with generous margin, remove any text, captions or labels from the reference, calm craft style, photorealistic, no extra objects or props. Place it {t}"
jobs = [(src, BASE.format(p=opis, t=TLA[k]), f"{O}{pid}-{k}.jpg") for pid, (src, opis) in PRODUKTY.items() for k in TLA]
def run(j):
    src, opis, out = j
    if os.path.exists(out): return out, 0
    r = subprocess.run([sys.executable, "scripts/grafika/scena.py", "--proporcje", "1:1", "--zdjecie", src, "--opis", opis, "--wyjscie", out], capture_output=True, text=True)
    return out, r.returncode
os.makedirs(O, exist_ok=True)
with ThreadPoolExecutor(3) as ex:
    for out, rc in ex.map(run, jobs): print("OK" if rc == 0 else "BŁĄD", out, flush=True)
