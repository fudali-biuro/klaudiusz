#!/usr/bin/env python3
"""Zosia: próbne grafiki Instagram 4:5 (1080×1350) w jednym stylu serii – prawdziwe zdjęcia z biblioteki, montaż (bez AI, bez napisu „AI”).
Styl serii: pełny kadr zdjęcia, małe logo FUDALI (jasna plakietka) w lewym górnym rogu, mała kremowa „etykieta” tematu w prawym górnym rogu, minimum tekstu.
Użycie: python3 scripts/grafika/ig_proba.py → marketing/instagram/proby/"""
import glob, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W, H = 1080, 1350
B = "marketing/biblioteka-zdjec/"; OUT = "marketing/instagram/proby/"; os.makedirs(OUT, exist_ok=True)
CREAM = (250, 245, 234); GREEN = (24, 52, 38); GOLD = (214, 170, 80)
F = lambda sz, bold=True: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), sz)
FS = lambda sz: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", sz)
LOGO = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
g = lambda k: sorted(glob.glob(B + f"*/*{k}*"))[0]
def cover(im, w, h, fx=0.5, fy=0.5):
    r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r) + 1, round(im.height * r) + 1), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def chrome(img, tag, caption=None, bottom_grad=True):
    img = img.convert("RGBA"); d = ImageDraw.Draw(img)
    if bottom_grad and caption:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d0 = ImageDraw.Draw(ov)
        for y in range(H - 300, H): d0.line((0, y, W, y), fill=GREEN + (int(215 * ((y - (H - 300)) / 300) ** 1.2),))
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img)
    lg = LOGO.resize((200, round(LOGO.height * 200 / LOGO.width)), Image.LANCZOS); pl = Image.new("RGBA", (lg.width + 28, lg.height + 22), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=14, fill=CREAM + (235,)); img.alpha_composite(pl, (36, 36)); img.alpha_composite(lg, (50, 47))
    f = F(24); tw = d.textlength(tag, font=f) + 44; x0 = W - 36 - tw
    d.rounded_rectangle((x0, 40, W - 36, 40 + 52), radius=26, fill=CREAM + (235,)); d.text((x0 + 22, 52), tag, font=f, fill=GREEN + (255,))
    if caption:
        d.rectangle((50, H - 130, 120, H - 124), fill=GOLD + (255,)); d.text((50, H - 108), caption, font=FS(46), fill=CREAM + (255,))
    return img.convert("RGB")
# 1. Realizacja – prawdziwe zdjęcie z werandy klienta
im = cover(Image.open(g("image-20260904-110937-616")).convert("RGB"), W, H, 0.5, 0.55)
chrome(im, "REALIZACJA", "Leżaki na werandzie").save(OUT + "proba-1-realizacja.jpg", quality=94)
# 2. Detal – zbliżenie na listwy (zdjęcie studyjne)
d_ = Image.open(g("detal-siedziska-lezaka-w-ciemnym")).convert("RGB"); d_ = d_.crop((330, 420, 330 + 1000, 420 + 1250 if 420 + 1250 <= 1600 else 1600)).resize((1000, min(1250, 1180)), Image.LANCZOS) if False else d_.crop((420, 250, 1500, 1600)); im = cover(d_, W, H, 0.5, 0.5)
chrome(im, "DETAL", "Każda listwa na swoim miejscu").save(OUT + "proba-2-detal.jpg", quality=94)
# 3. 5 kolorów – montaż packshotów (białe tło wycięte flood-fillem, cienie pod nogami)
def sprite(path):
    im = Image.open(path).convert("RGB"); L = ImageChops.darker(ImageChops.darker(*im.split()[:2]), im.split()[2]); ImageDraw.floodfill(L, (0, 0), 0, thresh=26)
    a = L.point(lambda v: 255 if v else 0).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.1))
    s = im.convert("RGBA"); s.putalpha(a); return s.crop(s.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())
pw = lambda n: sorted(glob.glob(B + f"produkty/*produktywniej*fud-{n}.jpg"))[0]
natural = sorted(glob.glob(B + "produkty/*packshot-lezaka-w-kolorze-naturalnym*"))[0]
chairs = [natural, pw(13), pw(2), pw(5), pw(4)]  # jasny · brąz · ciemny brąz · grafit · czerń
bg = Image.new("RGB", (W, H)); px = ImageDraw.Draw(bg)
for y in range(H): c = tuple(int(a + (b - a) * y / H) for a, b in zip((242, 235, 223), (222, 210, 192))); px.line((0, y, W, y), fill=c)
img = bg.convert("RGBA"); TH = 400
sp = []
for p in chairs:
    s_ = sprite(p); sp.append(s_.resize((round(s_.width * TH / s_.height), TH), Image.LANCZOS))
def put(img, s_, x, base):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((x + s_.width * 0.12, base - 12, x + s_.width * 0.92, base + 18), fill=(60, 45, 30, 115))
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(12))); img.alpha_composite(s_, (x, base - TH)); return img
w0 = sp[0].width; gap = (W - 80 - 3 * w0) / 2   # górny rząd: 3 leżaki
for i in range(3): img = put(img, sp[i], int(40 + i * (w0 + gap)), 640)
w1 = sp[3].width; tot = sp[3].width + sp[4].width + 30   # dolny rząd: 2 leżaki, wyśrodkowane
x1 = int((W - tot) / 2); img = put(img, sp[3], x1, 1010); img = put(img, sp[4], x1 + sp[3].width + 30, 1010)
d_ = ImageDraw.Draw(img); d_.rectangle((50, H - 190, 120, H - 184), fill=GOLD + (255,)); d_.text((50, H - 168), "Jedna jodła, pięć charakterów", font=FS(46), fill=GREEN + (255,))
chrome(img, "5 KOLORÓW", None).save(OUT + "proba-3-kolory.jpg", quality=94)
print("OK")
