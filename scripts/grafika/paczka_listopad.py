#!/usr/bin/env python3
"""Zosia: paczka grafik listopad (leżak 6 teł x 2 formaty, stolik i stołki x3 teł). Generuje przez scena.py, równolegle."""
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
S = os.environ.get("ZRODLA", "/tmp/zrodla")
LEZAK = "marketing/zdjecia/lezak/03-packshot-naturalny.jpg"
STOLIK = f"{S}/Flower-side-table.jpg"; STOLKI = f"{S}/Projekt-bez-nazwy-1.jpg"
O = "marketing/zdjecia/paczka-listopad/surowe/"
KADR = "Product centered, fully visible with generous margin around it, remove any text or captions from the reference, calm craft style, no extra text. Scene: "
T = {
 "lezak": (LEZAK, "the folding lounge chair with its white pillow", {
   "1-jasny-dab": "on a light blonde oak floor, soft daylight, blurred warm cream wall behind.",
   "2-szary-snieg": "standing on a grey weathered wooden terrace with a light layer of fresh snow, soft snowflakes falling, pale grey winter sky behind.",
   "3-kominek": "in a cosy living room next to a lit fireplace, warm glow, wooden floor, soft blurred background.",
   "4-ogrod-jesien": "in a garden in autumn, fallen orange and yellow leaves on the lawn, golden low sun, blurred trees behind.",
   "5-taras-wieczor": "on a wooden terrace in the evening, warm string lights softly glowing in the blurred background, dusk blue sky.",
   "6-prezent-kokarda": "as a Christmas gift: a big red satin bow tied around the chair's backrest, a few wrapped presents on a light wooden floor, soft warm festive light, blurred decorated tree behind.",
 }),
 "stolik": (STOLIK, "the side table with flower-shaped wooden top, black vase and white roses (keep exactly as in reference)", {
   "1-jasny-dab": "on a light blonde oak floor, soft daylight, blurred warm cream wall behind.",
   "2-salon-zima": "in a cosy living room beside a sofa with a wool blanket, warm winter evening light, pine branches and a candle in the soft background.",
   "3-taras-wieczor": "on a wooden terrace in the evening, warm string lights softly glowing, dusk sky blurred behind.",
 }),
 "stolki": (STOLKI, "the wooden stool set on castors (keep exactly as in reference)", {
   "1-jasny-dab": "on a light blonde oak floor, soft daylight, blurred warm cream wall behind.",
   "2-przedpokoj": "in a bright hallway with a wooden bench and a coat rack softly blurred behind, natural daylight.",
   "3-taras-wieczor": "on a wooden terrace in the evening, warm string lights softly glowing, dusk sky blurred behind.",
 }),
}
jobs = []
for prod, (src, opis, tla) in T.items():
    for k, tlo in tla.items():
        for prop, nazwa in (("1:1", "1x1"), ("4:5", "4x5")):
            if prod != "lezak" and prop == "4:5": continue
            jobs.append((src, f"Studio product shot of {opis}. {KADR}{tlo}", prop, f"{O}{prod}-{k}-{nazwa}.jpg"))
def run(j):
    src, opis, prop, out = j
    if os.path.exists(out): return out, 0
    r = subprocess.run([sys.executable, "scripts/grafika/scena.py", "--proporcje", prop, "--zdjecie", src, "--opis", opis, "--wyjscie", out], capture_output=True, text=True)
    return out, r.returncode
os.makedirs(O, exist_ok=True)
with ThreadPoolExecutor(4) as ex:
    for out, rc in ex.map(run, jobs): print("OK" if rc == 0 else "BŁĄD", out, flush=True)
