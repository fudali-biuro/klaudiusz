#!/usr/bin/env python3
"""Zosia: 5 pinów Pinterest 2:3 (1000×1500, EN) z prawdziwych zdjęć koparki – bez logo FUDALI, bez etykiety AI. Tytuły z posty.md; cena z media/cena-en.txt.
Użycie: python3 scripts/grafika/koparka_piny.py → marketing/kampanie/koparka/piny/pin-N.jpg"""
import glob, os
from PIL import Image, ImageDraw, ImageFont
OUT = "marketing/kampanie/koparka/piny/"; os.makedirs(OUT, exist_ok=True)
FOTO = sorted(glob.glob("marketing/biblioteka-zdjec/produkty/*shanmon-fuji-388*"))
idx = lambda n: 9 if n == 1 else 0 if n == 10 else n - 1
CENA = open("marketing/kampanie/koparka/media/cena-en.txt", encoding="utf-8").read().strip()
YEL = (255, 196, 0); WHITE = (255, 255, 255); BLK = (16, 16, 16)
F = lambda sz: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
PINY = {  # nr: (zdjęcie, kicker, tytuł, zoom, cx, cy) – ciasny kadr: maszyna wypełnia kadr (min. 60%)
 1: (3, "BRAND NEW 2026", "Brand New Backhoe Loader 2026 – Available Now in Rzeszów, Poland", 1.0, 0.5, 0.62),
 2: (4, "SHANMON FUJI 388", "6-in-1 Front Bucket Backhoe Loader – Shanmon Fuji 388", 1.0, 0.5, 0.6),
 3: (1, "TELESCOPIC ARM", "Telescopic Backhoe Arm – Dig Up to 5.5 m (18 ft)", 1.0, 0.5, 0.55),
 4: (9, "FOR SALE IN POLAND", "Backhoe Loader for Sale in Poland – " + CENA.split(" (")[0] + ", 2026, Warranty 12 Months", 1.0, 0.5, 0.62),
 5: (7, "4x4 · NEW 2026", "New Backhoe Loader 4x4 Stage V – 6-in-1 Bucket, Dig to 5.5 m, Test Drive in Rzeszów", 1.0, 0.5, 0.58),
}
def wrap(d, t, f, mw):
    out, cur = [], ""
    for w in t.split():
        x = (cur + " " + w).strip()
        if d.textlength(x, font=f) <= mw: cur = x
        else: out.append(cur); cur = w
    return out + [cur]
for nr, (foto, kick, tytul, zoom, cxf, cyf) in PINY.items():
    ph = Image.open(FOTO[idx(foto)]).convert("RGB"); W, H = 1000, 1500
    r = max(W / ph.width, H / ph.height) * zoom; ph = ph.resize((round(ph.width * r), round(ph.height * r)), Image.LANCZOS)
    x0 = int((ph.width - W) * cxf); y0 = int((ph.height - H) * cyf); im = ph.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d0 = ImageDraw.Draw(ov)
    for y in range(H - 430, H): d0.line((0, y, W, y), fill=(0, 0, 0, int(225 * (y - (H - 430)) / 430)))
    im = Image.alpha_composite(im, ov); d = ImageDraw.Draw(im)
    f = F(64); lines = wrap(d, tytul, f, W - 100); y = H - 70 - len(lines) * 78
    kw = d.textlength(kick, font=F(40)); d.rounded_rectangle((40, y - 84, 60 + kw + 20, y - 18), radius=14, fill=BLK + (235,))
    d.text((50, y - 74), kick, font=F(40), fill=YEL + (255,))
    for l in lines: d.text((50, y), l, font=f, fill=WHITE + (255,)); y += 78
    d.rectangle((0, 0, W, 16), fill=YEL + (255,))
    im.convert("RGB").save(f"{OUT}pin-{nr}.jpg", quality=93)
print("OK", len(PINY))
