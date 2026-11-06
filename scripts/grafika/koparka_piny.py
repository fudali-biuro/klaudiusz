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
PINY = {  # nr: (zdjęcie, kicker, tytuł)
 1: (5, "BRAND NEW 2026", "Backhoe Loader – Available Now in Rzeszów, Poland"),
 2: (4, "SHANMON FUJI 388", "6-in-1 Front Bucket Backhoe Loader"),
 3: (6, "TELESCOPIC ARM", "Dig up to 5.5 m (18 ft)"),
 4: (8, "FOR SALE IN POLAND", "New Backhoe Loader – " + CENA.split(" (")[0] + ", 12-Month Warranty"),
 5: (7, "4x4 · NEW 2026", "6-in-1 Bucket, Dig to 5.5 m – Test Drive in Rzeszów"),
}
def wrap(d, t, f, mw):
    out, cur = [], ""
    for w in t.split():
        x = (cur + " " + w).strip()
        if d.textlength(x, font=f) <= mw: cur = x
        else: out.append(cur); cur = w
    return out + [cur]
for nr, (foto, kick, tytul) in PINY.items():
    ph = Image.open(FOTO[idx(foto)]).convert("RGB"); W, H = 1000, 1500
    r = max(W / ph.width, H / ph.height); ph = ph.resize((round(ph.width * r), round(ph.height * r)), Image.LANCZOS)
    x0 = (ph.width - W) // 2; y0 = int((ph.height - H) * 0.4); im = ph.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d0 = ImageDraw.Draw(ov)
    for y in range(H - 620, H): d0.line((0, y, W, y), fill=(0, 0, 0, int(225 * (y - (H - 620)) / 620)))
    im = Image.alpha_composite(im, ov); d = ImageDraw.Draw(im)
    f = F(76); lines = wrap(d, tytul, f, W - 100); y = H - 70 - len(lines) * 90
    d.text((50, y - 70), kick, font=F(40), fill=YEL + (255,))
    for l in lines: d.text((50, y), l, font=f, fill=WHITE + (255,)); y += 90
    d.rectangle((0, 0, W, 16), fill=YEL + (255,))
    im.convert("RGB").save(f"{OUT}pin-{nr}.jpg", quality=93)
print("OK", len(PINY))
