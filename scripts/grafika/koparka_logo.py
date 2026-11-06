#!/usr/bin/env python3
"""Zosia: logo / awatar konta (TikTok, Pinterest) do sprzedaży koparki – 3 warianty PNG 1080×1080 + podgląd w kółku 200 px.
(a) sam znak, (b) znak + napis (NAPIS poniżej – nazwę konta poda Pablo), (c) zdjęcie maszyny w kółku z żółtą ramką. Żółty + czarny jak maszyna. Bez logo FUDALI."""
import glob
from PIL import Image, ImageDraw, ImageFont
NAPIS = "MASZYNY RZESZÓW"
OUT = "marketing/kampanie/koparka/logo/"
YEL = (255, 196, 0); BLK = (16, 16, 16); S = 2  # supersampling
def znak(size, color=YEL, bg=BLK):
    """sylwetka koparko-ładowarki (boczny widok), rysowana w układzie 640×440"""
    k = size / 640 * S; W_ = int(640 * k); H_ = int(440 * k)
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    c = color + (255,); b = bg + (255,)
    d.polygon(P([(120, 262), (130, 222), (250, 212), (262, 262)]), fill=c)                       # maska silnika
    d.polygon(P([(250, 262), (252, 138), (276, 112), (406, 112), (430, 138), (434, 262)]), fill=c)  # kabina
    d.polygon(P([(284, 150), (284, 232), (400, 232), (394, 150)]), fill=b)                        # szyba
    d.rectangle(P([(110, 262), (480, 300)])[0] + P([(110, 262), (480, 300)])[1], fill=c)        # rama
    # ładowacz (przód, lewa strona)
    d.line(P([(135, 235), (50, 212)]), fill=c, width=int(30 * k)); d.line(P([(135, 258), (60, 250)]), fill=c, width=int(18 * k))
    d.polygon(P([(14, 195), (64, 190), (60, 292), (6, 300)]), fill=c)                             # łyżka
    for tx in (10, 24, 38, 52): d.polygon(P([(tx, 298), (tx + 8, 298), (tx + 4, 318)]), fill=c)  # zęby
    # koparka (tył, prawa strona) – wysięgnik i ramię
    d.line(P([(470, 262), (525, 130), (588, 205)]), fill=c, width=int(26 * k), joint="curve")
    d.line(P([(588, 205), (566, 262)]), fill=c, width=int(20 * k))
    d.polygon(P([(540, 262), (596, 262), (580, 300), (545, 300)]), fill=c)                        # łyżka tylna
    d.rectangle(P([(470, 262), (500, 330)])[0] + P([(470, 262), (500, 330)])[1], fill=c)        # stabilizator
    # koła
    for cx, cy, r in ((388, 322, 86), (168, 334, 66)):
        d.ellipse(((cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k), fill=c)
        d.ellipse(((cx - r * .55) * k, (cy - r * .55) * k, (cx + r * .55) * k, (cy + r * .55) * k), fill=b)
        d.ellipse(((cx - r * .22) * k, (cy - r * .22) * k, (cx + r * .22) * k, (cy + r * .22) * k), fill=c)
    return im.resize((int(640 * size / 640), int(440 * size / 640)), Image.LANCZOS)
def kolko_maska(n): m = Image.new("L", (n * 4, n * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, n * 4 - 1, n * 4 - 1), fill=255); return m.resize((n, n), Image.LANCZOS)
def wariant_a():
    im = Image.new("RGBA", (1080, 1080), BLK + (255,)); d = ImageDraw.Draw(im)
    d.ellipse((40, 40, 1040, 1040), outline=YEL + (255,), width=18)
    z = znak(840); im.alpha_composite(z, ((1080 - z.width) // 2, 300)); return im
def wariant_b():
    im = Image.new("RGBA", (1080, 1080), BLK + (255,)); d = ImageDraw.Draw(im)
    d.ellipse((40, 40, 1040, 1040), outline=YEL + (255,), width=18)
    z = znak(640); im.alpha_composite(z, ((1080 - z.width) // 2, 200))
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 92); words = NAPIS.split(" ")
    y = 690
    for w in words: d.text((540 - d.textlength(w, font=f) / 2, y), w, font=f, fill=YEL + (255,)); y += 112
    return im
def wariant_c():
    im = Image.new("RGBA", (1080, 1080), BLK + (255,)); d = ImageDraw.Draw(im)
    f = sorted(glob.glob("marketing/biblioteka-zdjec/produkty/*shanmon-fuji-388*"))[4]  # '--5' – cała maszyna z daleka
    ph = Image.open(f).convert("RGB"); w, h = ph.size; cw = int(w * 0.95); cx0 = int(w * 0.62 - cw / 2); cx0 = min(max(cx0, 0), w - cw); cy0 = int(h * 0.55 - cw / 2)
    ph = ph.crop((cx0, cy0, cx0 + cw, cy0 + cw)).resize((960, 960), Image.LANCZOS).convert("RGBA")
    ph.putalpha(kolko_maska(960)); d.ellipse((40, 40, 1040, 1040), fill=YEL + (255,)); im.alpha_composite(ph, (60, 60)); return im
def podglad(files):
    m = Image.new("RGB", (len(files) * 260 + 20, 240), (60, 60, 60))
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGBA").resize((200, 200), Image.LANCZOS); im.putalpha(kolko_maska(200)); m.paste(im, (20 + i * 260, 20), im)
    m.save(OUT + "podglad-kolko-200px.png")
fs = []
for n, fn in (("a-sam-znak", wariant_a), ("b-znak-z-napisem", wariant_b), ("c-zdjecie-w-kolku", wariant_c)):
    fn().save(f"{OUT}logo-koparka-{n}.png"); fs.append(f"{OUT}logo-koparka-{n}.png")
podglad(fs); print("OK")
