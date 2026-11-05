#!/usr/bin/env python3
"""Zosia: kolaż startowy „Prezenty z drewna od 49 zł” (IG 4:5, FB 1.91:1) + 3 piny leżaka 2:3 (EN) – z gotowych zdjęć.
Użycie: python3 scripts/grafika/swieta_kolaz.py → marketing/zdjecia/swieta-2026/"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import swieta as S
from PIL import Image, ImageDraw
Z = S.Z; O = S.O
KAFLE = [  # (zdjęcie, nazwa, cena, fokus)
 ("kampania-swieta/otwieracz-kot.jpg", "Otwieracz Kot", "49 zł", (0.5, 0.5)),
 ("kampania-swieta/podkladka.jpg", "Podkładka z orzecha", "99 zł", (0.5, 0.5)),
 ("kampania-swieta/stolik-skladany.jpg", "Składany stolik", "229 zł", (0.5, 0.5)),
 ("kampania-swieta/lezak-pod-choinka.jpg", "Leżak składany", "299 zł", (0.5, 0.5)),
 ("kampania-swieta/stolik-platek.jpg", "Stolik Płatek", "850 zł", (0.5, 0.5)),
 ("kampania-swieta/stolki.jpg", "Stołki z wózkiem", "1200 zł", (0.5, 0.5)),
]
def kafel(w, h, k, ps):
    im = S.cover(Image.open(Z + k[0]).convert("RGB"), w, h, k[3]).convert("RGBA"); d = ImageDraw.Draw(im)
    for y in range(h - int(h * .32), h): d.line((0, y, w, y), fill=S.GREEN + (int(230 * (y - (h - h * .32)) / (h * .32)),))
    fn, fp = S.F(ps, False, True), S.F(int(ps * 1.25), True, True)
    d.text((14, h - ps * 2.7), k[1], font=fn, fill=S.CREAM + (255,)); d.text((14, h - ps * 1.65), k[2], font=fp, fill=S.GOLD + (255,))
    return im
def kolaz(fmt, out):
    W, H = S.FORMATY[fmt]; wide = W / H > 1.5
    img = Image.new("RGBA", (W, H), S.GREEN + (255,)); d = ImageDraw.Draw(img)
    if wide:
        pw = 400; cols, rows, gap = 3, 2, 8; gx = pw; gw, gh = W - pw - 16, H - 16
        tw, th = (gw - gap * (cols - 1)) // cols, (gh - gap * (rows - 1)) // rows
        for i, k in enumerate(KAFLE): img.alpha_composite(kafel(tw, th, k, 20), (gx + 8 + (i % cols) * (tw + gap), 8 + (i // cols) * (th + gap)))
        y = 130; pl = "SEZON ŚWIĄTECZNY"; pf = S.F(20, False, True)
        d.rounded_rectangle((36, y, 36 + d.textlength(pl, font=pf) + 40, y + 46), radius=26, fill=S.RED + (255,)); d.text((56, y + 11), pl, font=pf, fill=S.CREAM + (255,)); y += 74
        d.rectangle((36, y, 106, y + 5), fill=S.GOLD + (255,)); y += 20
        for l in ["Prezenty", "z drewna", "od 49 zł"]: d.text((36, y), l, font=S.F(58), fill=S.CREAM + (255,)); y += 68
        d.text((36, y + 12), "FUDALI · Głogów Małopolski", font=S.F(20, False, False), fill=S.CREAM + (210,))
        S.plaque_logo(img, 150, 28, 24)
    else:
        top = 330; gx, gy, gap = 14, top, 10; cols, rows = 2, 3
        tw = (W - 2 * gx - gap) // 2; th = (H - gy - 14 - gap * 2) // 3
        for i, k in enumerate(KAFLE): img.alpha_composite(kafel(tw, th, k, 30), (gx + (i % cols) * (tw + gap), gy + (i // cols) * (th + gap)))
        pl = "SEZON ŚWIĄTECZNY"; pf = S.F(24, False, True)
        d.rounded_rectangle((56, 138, 56 + d.textlength(pl, font=pf) + 44, 138 + 50), radius=28, fill=S.RED + (255,)); d.text((78, 150), pl, font=pf, fill=S.CREAM + (255,))
        d.rectangle((56, 210, 130, 216), fill=S.GOLD + (255,)); d.text((56, 228), "Prezenty z drewna od 49 zł", font=S.F(54), fill=S.CREAM + (255,))
        S.plaque_logo(img, 210, 36, 30)
    d.text((W - 24 - d.textlength("grafika AI", font=S.F(16, False, False)), H - 26), "grafika AI", font=S.F(16, False, False), fill=S.CREAM + (210,))
    img.convert("RGB").save(out, quality=93)
kolaz("ig-4x5", O + "kolaz-start-ig-4x5.jpg"); kolaz("fb-191x1", O + "kolaz-start-fb-191x1.jpg")
PINY = {  # nazwa: (źródło, pack?, plakietka, nagłówek, podpis)
 "pin-lezak-gift-under-the-tree": (Z + "paczka-listopad/surowe/lezak-6-prezent-kokarda-4x5.jpg", False, "CHRISTMAS GIFT", "A gift under the tree", "Folding fir lounge chair · cushion included"),
 "pin-lezak-cushion-included": (Z + "packshoty/surowe/lezak-b-blat.jpg", True, "CUSHION INCLUDED", "Handmade, with its own cushion", "Folding lounge chair from Polish fir"),
 "pin-lezak-gift-idea": (Z + "kampania-swieta/lezak-pod-choinka.jpg", False, "GIFT IDEA", "Folding wooden lounger", "A holiday gift they will use all summer"),
}
for n, (src, pack, a, b, c) in PINY.items(): S.render(src, True, (0.5, 0.5), (a, b, c), "pin-2x3", f"{O}{n}.jpg", pack)
print("OK")
