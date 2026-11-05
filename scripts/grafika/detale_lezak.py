#!/usr/bin/env python3
"""Zosia: 3 slajdy „detal wykonania” 1080x1350 z PRAWDZIWYCH zdjęć (kadr + logo + krótkie hasło, bez AI)."""
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
Z = "marketing/zdjecia/lezak/"; O = "marketing/zdjecia/paczka-listopad/"
LOGO = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
CREAM = (250, 245, 234)
FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 64)
def crop(f, box):  # box w ułamkach (x0,y0,x1,y1) – proporcje 4:5 wymuszone
    im = Image.open(Z + f).convert("RGB"); w, h = im.size
    x0, y0, x1, y1 = box[0]*w, box[1]*h, box[2]*w, box[3]*h
    return im.crop((int(x0), int(y0), int(x1), int(y1))).resize((W, H), Image.LANCZOS)
def finish(im, haslo, out):
    im = im.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(H - 330, H): d.line((0, y, W, y), fill=(20, 26, 20, int(200 * (y - (H - 330)) / 330)))
    im = Image.alpha_composite(im, ov); d = ImageDraw.Draw(im)
    d.text((56, H - 120), haslo, font=FS, fill=CREAM + (255,))
    lw = 210; lg = LOGO.resize((lw, round(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    pl = Image.new("RGBA", (lw + 32, lg.height + 26), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=16, fill=CREAM + (235,))
    im.alpha_composite(pl, (36, 36)); im.alpha_composite(lg, (52, 49))
    im.convert("RGB").save(O + out, quality=93)
finish(crop("05-detal-ciemny-braz-lina.jpg", (0.10, 0.0, 0.90, 1.0)), "Jodła z certyfikatem FSC", "detal-1-listwy-4x5.jpg")
finish(crop("06-czarny-i-brazowy-poduszki.jpg", (0.35, 0.28, 1.0, 0.90)), "Lina jutowa", "detal-2-lina-4x5.jpg")
finish(crop("02-dwa-lezaki-ogrod.jpg", (0.03, 0.50, 0.58, 1.0)), "Zrobione w Głogowie Młp.", "detal-3-siedzisko-4x5.jpg")
