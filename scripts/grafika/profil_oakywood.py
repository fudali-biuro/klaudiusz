#!/usr/bin/env python3
"""Profil IG w duchu wzoru (Zosia, 09.11.2026): 6 okładek wyróżnionych, 3 karty-cytaty, makieta profilu."""
import glob, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(R, "marketing/instagram/profil-oakywood")
FD = "/usr/share/fonts/truetype/dejavu/"
SB = lambda s: ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", s)
SN = lambda s, b=False: ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf"), s)
GREEN, CREAM, GOLD, INK = (24, 52, 38), (246, 240, 226), (214, 170, 80), (28, 28, 28)
LOGO = Image.open(os.path.join(R, "marketing/logo/fudali-logo.png")).convert("RGBA")

def logo(w):
    return LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS)

def spaced(d, xy, txt, font, fill, sp=6, anchor_center=True):
    ws = [d.textlength(c, font=font) for c in txt]
    tot = sum(ws) + sp * (len(txt) - 1)
    x, y = xy
    if anchor_center: x -= tot / 2
    for c, w in zip(txt, ws):
        d.text((x, y), c, font=font, fill=fill); x += w + sp

def disc_img(d_px, fill):
    s = 4; m = Image.new("L", (d_px * s, d_px * s), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d_px * s - 1, d_px * s - 1), fill=255)
    return m.resize((d_px, d_px), Image.LANCZOS)

def cover(lines, name):
    im = Image.new("RGB", (1080, 1920), GREEN); d = ImageDraw.Draw(im)
    D = 780; cx, cy = 540, 960
    im.paste(Image.new("RGB", (D, D), CREAM), (cx - D // 2, cy - D // 2), disc_img(D, 1))
    fs = 84 if max(len(l) for l in lines) <= 8 else 68
    lh = fs + 22; y0 = cy - (len(lines) * lh) / 2 - 40
    for i, l in enumerate(lines):
        spaced(d, (cx, y0 + i * lh), l, SB(fs), GREEN, sp=8)
    yl = y0 + len(lines) * lh + 18
    d.rectangle((cx - 40, yl, cx + 40, yl + 4), fill=GOLD)
    lg = logo(210); im.paste(lg, (cx - lg.width // 2, int(yl + 34)), lg)
    im.save(os.path.join(OUT, f"okladka-{name}.png"))
    return im

COVERS = [("LEZAKI", ["LEŻAKI"]), ("MEBLE", ["MEBLE"]), ("ALTANY", ["ALTANY", "I DOMKI"]),
          ("WARSZTAT", ["WARSZTAT"]), ("OPINIE", ["OPINIE"]), ("PYTANIA", ["PYTANIA"])]

def avatar(d_px):
    a = Image.new("RGB", (d_px, d_px), CREAM)
    lg = logo(int(d_px * 0.8)); a.paste(lg, ((d_px - lg.width) // 2, (d_px - lg.height) // 2), lg)
    out = Image.new("RGBA", (d_px, d_px), (0, 0, 0, 0)); out.paste(a, (0, 0), disc_img(d_px, 1)); return out

def quote(txt, name):
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), (251, 249, 244)); d = ImageDraw.Draw(im)
    av = avatar(120); im.paste(av, (90, 120), av)
    d.text((240, 132), "FUDALI", font=SN(46, True), fill=INK)
    d.text((240, 190), "@fudali_nowoczesne_stolarstwo", font=SN(30), fill=(120, 120, 120))
    f = SN(58); lines = []
    for p in txt.split("\n"): lines += textwrap.wrap(p, 30) or [""]
    lh = 84; y = 330
    for l in lines:
        d.text((90, y), l, font=f, fill=INK); y += lh
    d.rectangle((90, H - 190, 170, H - 186), fill=GOLD)
    d.text((90, H - 160), "Drewno, które zostaje.", font=SB(36), fill=GREEN)
    d.text((90, H - 105), "fudali.com.pl", font=SN(30), fill=(120, 120, 120))
    im.save(os.path.join(OUT, f"cytat-{name}.jpg"), quality=94)

QUOTES = [
 ("leżak-10kg", "Leżak waży 10 kg i składa się na płasko.\nZmieści się w bagażniku, pod łóżkiem i w każdej wymówce, że nie ma miejsca."),
 ("zima", "Czy drewno przetrwa zimę?\nTak – jeśli stoi sucho i przewiewnie.\nReszta to jodła bieszczadzka z certyfikatem FSC."),
 ("zaufanie", "Reklamacja po 20 latach? Nie – to zaufanie.\nRobimy rzeczy, do których nikt nie musi wracać."),
]

def crop(path, w, h):
    im = Image.open(path).convert("RGB"); r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))

def lib(sub):
    return glob.glob(os.path.join(R, "marketing/biblioteka-zdjec", sub))[0]

def mockup(covers):
    W, H = 1080, 2330
    im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
    d.text((W // 2, 70), "fudali_nowoczesne_stolarstwo", font=SN(38, True), fill=INK, anchor="mm")
    # awatar z pierścieniem
    ring = Image.new("RGB", (260, 260)); g = ImageDraw.Draw(ring)
    for i in range(260): g.line((0, i, 260, i), fill=(int(GOLD[0] + (GREEN[0] - GOLD[0]) * i / 260), int(GOLD[1] + (GREEN[1] - GOLD[1]) * i / 260), int(GOLD[2] + (GREEN[2] - GOLD[2]) * i / 260)))
    im.paste(ring, (40, 150), disc_img(260, 1)); im.paste(Image.new("RGB", (240, 240), (255, 255, 255)), (50, 160), disc_img(240, 1))
    av = avatar(224); im.paste(av, (58, 168), av)
    d.text((340, 190), "Drewno, które zostaje.", font=SN(40, True), fill=INK)
    for x, lab in [(340, "posty"), (560, "obserwujący"), (860, "obserwowani")]:
        d.text((x, 270), "–", font=SN(46, True), fill=INK); d.text((x, 325), lab, font=SN(30), fill=INK)
    bio = ["Produkt / usługa", "Drewno, które zostaje.", "Made in Poland · rodzinna pracownia z Głogowa Młp.", "Leżaki · meble · altany z litego drewna", "↓ sklep · wycena · współpraca"]
    y = 450
    for i, b in enumerate(bio):
        d.text((44, y), b, font=SN(34), fill=(120, 120, 120) if i == 0 else INK); y += 50
    d.text((44, y + 6), "fudali.com.pl/sklep", font=SN(34, True), fill=(0, 90, 200)); y += 90
    for x, w, t, pr in [(44, 300, "Obserwuj", True), (364, 300, "Wiadomość", False), (684, 220, "Kontakt", False)]:
        d.rounded_rectangle((x, y, x + w, y + 80), 16, fill=(30, 100, 220) if pr else (236, 236, 236))
        d.text((x + w / 2, y + 40), t, font=SN(32, True), fill=(255, 255, 255) if pr else INK, anchor="mm")
    y += 130
    labs = ["Leżaki", "Meble", "Altany i domki", "Warsztat", "Opinie", "Pytania"]
    for i, (c, lab) in enumerate(zip(covers, labs)):
        cx = 40 + i * 176
        c2 = c.crop((140, 560, 940, 1360)).resize((140, 140), Image.LANCZOS)
        d.ellipse((cx - 4, y - 4, cx + 148, y + 148), outline=(200, 200, 200), width=3)
        im.paste(c2, (cx + 2, y + 2), disc_img(140, 1))
        d.text((cx + 72, y + 170), lab if len(lab) < 11 else "Altany", font=SN(24), fill=INK, anchor="mm")
    y += 220
    d.line((0, y, W, y), fill=(220, 220, 220), width=2)
    d.rectangle((140, y - 3, 220, y), fill=INK)
    for i, x in enumerate([180, 540, 900]):
        col = INK if i == 0 else (150, 150, 150)
        if i == 0:
            for a in range(3):
                for b in range(3): d.rectangle((x - 27 + a * 20, y + 20 + b * 20, x - 15 + a * 20, y + 32 + b * 20), fill=col)
        elif i == 1:
            d.rounded_rectangle((x - 28, y + 20, x + 28, y + 70), 10, outline=col, width=4); d.polygon([(x - 7, y + 33), (x - 7, y + 57), (x + 14, y + 45)], fill=col)
        else:
            d.ellipse((x - 12, y + 18, x + 12, y + 42), outline=col, width=4); d.arc((x - 26, y + 40, x + 26, y + 90), 180, 360, fill=col, width=4)
    y += 90
    cw, ch = 360, 480
    pins = [crop(lib("gotowe/*taras-z-palenisko*"), cw, ch), None, crop(lib("gotowe/*stolik-patek*"), cw, ch)]
    fill = [crop(p, cw, ch) for p in sorted(glob.glob(os.path.join(R, "marketing/instagram/inspiracje/insp-1[0-9]-*-4x5.jpg")))[:3]]
    for i in range(6):
        x, yy = (i % 3) * cw, y + (i // 3) * ch
        if i < 3:
            p = pins[i]
            if p is None:
                p = Image.new("RGB", (cw, ch), GREEN); pd = ImageDraw.Draw(p)
                pd.polygon([(150, 190), (150, 270), (225, 230)], fill=CREAM)
                pd.text((cw / 2, 330), "miejsce na rolkę", font=SN(26), fill=CREAM, anchor="mm")
                pd.text((cw / 2, 365), "z twarzą firmy", font=SN(22), fill=(200, 200, 200), anchor="mm")
            im.paste(p, (x, yy))
            d.ellipse((x + cw - 56, yy + 14, x + cw - 14, yy + 56), fill=(255, 255, 255))
            d.polygon([(x + cw - 42, yy + 22), (x + cw - 28, yy + 22), (x + cw - 22, yy + 36), (x + cw - 48, yy + 36)], fill=INK)
            d.rectangle((x + cw - 36, yy + 36, x + cw - 34, yy + 48), fill=INK)
        else:
            im.paste(fill[i - 3], (x, yy))
        d.line((x, yy, x, yy + ch), fill=(255, 255, 255), width=2)
    im.crop((0, 0, W, y + 2 * ch)).save(os.path.join(OUT, "podglad-profilu.jpg"), quality=93)

if __name__ == "__main__":
    covs = [cover(l, n.lower()) for n, l in COVERS]
    for n, t in QUOTES: quote(t, n)
    mockup(covs)
    print("OK")
