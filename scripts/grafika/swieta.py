#!/usr/bin/env python3
"""Zosia: świąteczne grafiki w formatach IG 4:5, IG 1:1, FB 1.91:1, Pinterest 2:3 – z GOTOWYCH zdjęć (kadr + napisy + logo + oznaczenie AI).
Użycie: python3 scripts/grafika/swieta.py   → marketing/zdjecia/swieta-2026/<id>-<format>.jpg"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Z = "marketing/zdjecia/"; O = Z + "swieta-2026/"
FD = "/usr/share/fonts/truetype/dejavu/"
def F(sz, serif=True, bold=True): return ImageFont.truetype(FD + ("DejaVuSerif-Bold.ttf" if serif and bold else "DejaVuSerif.ttf" if serif else "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), sz)
CREAM = (250, 245, 234); GREEN = (24, 52, 38); RED = (178, 36, 44); GOLD = (214, 170, 80)
LOGO = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
FORMATY = {"ig-4x5": (1080, 1350), "ig-1x1": (1080, 1080), "fb-191x1": (1200, 628), "pin-2x3": (1000, 1500)}
# id: (źródło, AI?, fokus, {kanał: (plakietka, nagłówek, podpis)})
PACK = {"lezak-prezent", "stolki", "podkladka", "zestaw-wnetrze"}  # packshoty: produkt w całości (bez przycinania), tło = rozmyta kopia zdjęcia
KARTY = {
 "lezak-prezent": (Z + "packshoty/surowe/lezak-a-dab.jpg", True, (0.5, 0.45), {
    "pl": ("NA ŚWIĘTA", "Prezent, który zostaje na lata", "Składany leżak z jodły · 299 zł · darmowa wysyłka"),
    "en": ("CHRISTMAS GIFT", "A gift they will use for years", "Handmade folding lounge chair · cushion included")}),
 "lezak-kokarda": (Z + "paczka-listopad/surowe/lezak-6-prezent-kokarda-1x1.jpg", True, (0.5, 0.5), {
    "pl": ("POD CHOINKĘ", "Leżak z kokardą", "Prezent na święta · 299 zł · darmowa wysyłka"),
    "en": ("UNDER THE TREE", "Wrap it. Gift it. Unfold it in May.", "Folding fir lounge chair · cushion included")}),
 "lezak-choinka": (Z + "kampania-swieta/lezak-pod-choinka.jpg", True, (0.5, 0.5), {
    "pl": ("WESOŁYCH ŚWIĄT", "Pod choinkę – na lata", "Leżak FUDALI z poduszką w zestawie"),
    "en": ("MERRY CHRISTMAS", "Under the tree – for years", "FUDALI folding lounge chair with cushion")}),
 "zestaw-wnetrze": (Z + "zestawy/surowe/lezak-stolik-stolki.jpg", True, (0.5, 0.5), {
    "pl": ("ŚWIĘTA W DREWNIE", "Naturalne drewno w Twoim domu", "Leżak · stolik Płatek · stołki"),
    "en": ("WOODEN GIFTS", "Natural wood for a cosy home", "Lounge chair · side table · stools")}),
 "stolki": (Z + "packshoty/surowe/stolki-a-dab.jpg", True, (0.5, 0.5), {
    "pl": ("POMYSŁ NA PREZENT", "Zestaw stołków z wózkiem", "Dąb czerwony · 1200 zł"),
    "en": ("GIFT IDEA", "Stackable stool set on wheels", "Solid red oak")}),
 "podkladka": (Z + "packshoty/surowe/podkladka-a-dab.jpg", True, (0.5, 0.5), {
    "pl": ("MAŁY PREZENT", "Podkładka z orzecha czarnego", "Ręcznie wycinany kwiat · 99 zł"),
    "en": ("STOCKING FILLER", "Black walnut flower coaster", "Hollow-cut, heat-resistant")}),
 "podkladka-kakao": (Z + "kampania-swieta/podkladka.jpg", True, (0.5, 0.5), {
    "pl": ("MAŁY PREZENT", "Podkładka z orzecha czarnego", "Ręcznie wycinany kwiat · 99 zł"),
    "en": ("STOCKING FILLER", "Black walnut flower coaster", "Hollow-cut, heat-resistant")}),
 "otwieracz-kot": (Z + "kampania-swieta/otwieracz-kot.jpg", True, (0.5, 0.5), {
    "pl": ("MAŁY PREZENT", "Drewniany otwieracz Kot", "Szczęśliwy kot na święta · 49 zł"),
    "en": ("STOCKING FILLER", "Wooden cat bottle opener", "A lucky cat for the holidays")}),
}
import random, math
from PIL import ImageEnhance, ImageChops
def warm(im):
    """cieplejsza kolorystyka (miękkie pomarańczowe światło) + lekkie podbicie nasycenia"""
    rgb = im.convert("RGB"); ov = Image.new("RGB", rgb.size, (255, 170, 90))
    rgb = Image.blend(rgb, ImageChops.multiply(rgb, ov), 0.22); rgb = ImageEnhance.Color(rgb).enhance(1.08); return rgb.convert("RGBA")
def bokeh(img, box, n=22, seed=3):
    """ciepłe światełka bokeh (złote/ciepłe białe, rozmyte) w obszarze box=(x0,y0,x1,y1)"""
    r = random.Random(seed); W, H = img.size; ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for _ in range(n):
        x = r.uniform(box[0], box[2]); y = r.uniform(box[1], box[3]); rad = r.uniform(6, 20) * W / 1080
        c = r.choice([(255, 214, 140), (255, 236, 190), (255, 190, 110), (255, 245, 220)])
        d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=c + (r.randint(45, 105),))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(6 * W / 1080)))
def snow(img, box, n=45, seed=5):
    r = random.Random(seed); W, H = img.size; ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for _ in range(n):
        x = r.uniform(box[0], box[2]); y = r.uniform(box[1], box[3]); rad = r.uniform(1.2, 3.2) * W / 1080
        d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=(255, 255, 255, r.randint(110, 200)))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.8)))
def gałązka(size=560, seed=1):
    """gałązka świerku z bombkami i czerwonymi jagodami (rysowana, RGBA), korzeń w prawym górnym rogu, rośnie w lewo-dół"""
    r = random.Random(seed); S = size * 2; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(S * (1 - t * 0.92), S * (0.02 + 0.8 * t ** 1.35 * 0.55 + 0.06 * math.sin(t * 5))) for t in [i / 60 for i in range(61)]]
    for i in range(len(pts) - 1): d.line((pts[i], pts[i + 1]), fill=(70, 46, 28, 255), width=int(10 * (1 - i / 80)))
    for i in range(2, 60):
        (x, y), (x2, y2) = pts[i], pts[i + 1]; a = math.atan2(y2 - y, x2 - x); L = S * 0.2 * (1 - i / 78)
        for side in (-1, 1):
            for k in range(7):
                aa = a + side * (0.9 + 0.15 * k) + r.uniform(-0.08, 0.08); ln = L * (1 - 0.1 * k) * r.uniform(0.7, 1.05)
                col = r.choice([(24, 74, 46, 255), (34, 98, 60, 255), (18, 58, 38, 255)])
                d.line((x, y, x + math.cos(aa) * ln, y + math.sin(aa) * ln), fill=col, width=int(S * 0.012))
    for i in (22, 34, 45):
        x, y = pts[i]; rad = S * 0.034; col = r.choice([(176, 36, 44), (214, 170, 80)])
        d.ellipse((x - rad, y - rad + 10, x + rad, y + rad + 10), fill=col + (255,)); d.ellipse((x - rad * .45, y - rad * .55, x - rad * .1, y - rad * .2), fill=(255, 255, 255, 170))
    for i in (28, 40, 52):
        x, y = pts[i]; rad = S * 0.012
        for dx, dy in ((0, 0), (rad * 2, rad), (-rad * 1.5, rad * 1.6)): d.ellipse((x + dx - rad, y + dy + S * .04 - rad, x + dx + rad, y + dy + S * .04 + rad), fill=(190, 30, 40, 255))
    return im.resize((size, size), Image.LANCZOS)
def festive(img, W, H, photo_box):
    """świąteczny montaż: ciepłe barwy, bokeh, śnieg, gałązki w rogach"""
    img = warm(img) if photo_box is None else img
    bokeh(img, (photo_box[0], photo_box[1], photo_box[2], photo_box[1] + (photo_box[3] - photo_box[1]) * 0.45), n=int(14 * W / 1080) + 5); snow(img, photo_box, n=int(34 * W / 1080) + 8)
    g = gałązka(int(min(W, H) * 0.30)); img.alpha_composite(g, (photo_box[2] - g.width + 6, photo_box[1] - 6))
    g2 = gałązka(int(min(W, H) * 0.22), seed=4).transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
    img.alpha_composite(g2, (photo_box[0] - 10, photo_box[3] - g2.height + 10))
    return img
def cover(im, w, h, focus):
    r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r) + 1, round(im.height * r) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1]); return im.crop((x, y, x + w, y + h))
def wrap(d, t, f, mw):
    out, cur = [], ""
    for w_ in t.split():
        x = (cur + " " + w_).strip()
        if d.textlength(x, font=f) <= mw: cur = x
        else: out.append(cur); cur = w_
    return out + [cur]
def plaque_logo(img, w, x, y):
    lg = LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS)
    pl = Image.new("RGBA", (w + 28, lg.height + 22), (0, 0, 0, 0)); ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=14, fill=CREAM + (238,))
    img.alpha_composite(pl, (x, y)); img.alpha_composite(lg, (x + 14, y + 11))
def render(src, ai, focus, tekst, fmt, out, pack=False):
    W, H = FORMATY[fmt]; plak, head, sub = tekst; wide = W / H > 1.5
    ph = Image.open(src).convert("RGB")
    def blurbg(w, h): return cover(ph, w, h, (0.5, 0.5)).filter(ImageFilter.GaussianBlur(38))
    def feather(base, c, xy, f=44):
        m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rectangle((f, f, c.width - f, c.height - f), fill=255)
        base.paste(c, xy, m.filter(ImageFilter.GaussianBlur(f * 0.6)))
    def contain(im, w, h):
        r = min(w / im.width, h / im.height); return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    if wide:
        pw = int(W * 0.5); img = Image.new("RGBA", (W, H), GREEN + (255,)); tx, tw = 48, W - pw - 96
        if pack:
            bg = blurbg(pw, H); c = contain(ph, pw, H); feather(bg, c, ((pw - c.width) // 2, (H - c.height) // 2)); img.paste(bg, (W - pw, 0))
        else: img.paste(cover(ph, pw, H, focus), (W - pw, 0))
    elif pack:
        tb = int(H * {"ig-4x5": 0.27, "ig-1x1": 0.33, "pin-2x3": 0.27}[fmt])
        img = blurbg(W, H); c = contain(ph, W, H - tb + 30); feather(img, c, ((W - c.width) // 2, 0)); img = img.convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d0 = ImageDraw.Draw(ov); gh = tb + 40
        for y in range(H - gh, H): d0.line((0, y, W, y), fill=GREEN + (int(250 * min(1, 1.5 * (y - (H - gh)) / gh)),))
        img = Image.alpha_composite(img, ov); tx, tw = 56, W - 112
    else:
        img = cover(ph, W, H, focus).convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d0 = ImageDraw.Draw(ov); gh = int(H * 0.42)
        for y in range(H - gh, H): d0.line((0, y, W, y), fill=GREEN + (int(245 * ((y - (H - gh)) / gh) ** 0.8),))
        img = Image.alpha_composite(img, ov); tx, tw = 56, W - 112
    if pack:
        box = (W - int(W * 0.5), 0, W, H) if wide else (0, 0, W, int(H * 0.7))
        img = festive(warm(img.convert("RGBA")) if not wide else img, W, H, box)
    d = ImageDraw.Draw(img)
    hs = int({"ig-4x5": 70, "ig-1x1": 64, "fb-191x1": 44, "pin-2x3": 72}[fmt]); ss = max(24, int(hs * 0.42)); ps = max(20, int(hs * 0.34))
    hl = wrap(d, head, F(hs), tw); sl = wrap(d, sub, F(ss, False, False), tw)
    hh = int(hs * 1.16); sh = int(ss * 1.4); block = len(hl) * hh + len(sl) * sh + ps * 2 + 60
    y = (H - block) // 2 if wide else H - block - 48
    pw_ = d.textlength(plak, font=F(ps, False, True)) + 2 * 22
    d.rounded_rectangle((tx, y, tx + pw_, y + ps + 22), radius=30, fill=RED + (255,)); d.text((tx + 22, y + 9), plak, font=F(ps, False, True), fill=CREAM + (255,)); y += ps + 22 + 20
    d.rectangle((tx, y, tx + 70, y + 5), fill=GOLD + (255,)); y += 18
    for l in hl: d.text((tx, y), l, font=F(hs), fill=CREAM + (255,)); y += hh
    y += 6
    for l in sl: d.text((tx, y), l, font=F(ss, False, False), fill=CREAM + (235,)); y += sh
    plaque_logo(img, 150 if wide else 210, 28 if wide else 36, 24 if wide else 36)
    if ai: d.text((W - 24 - d.textlength("grafika AI", font=F(18, False, False)), H - 34), "grafika AI", font=F(18, False, False), fill=CREAM + (200,)) if not wide else None
    img.convert("RGB").save(out, quality=93)
def main():
  os.makedirs(O, exist_ok=True)
  for kid, (src, ai, focus, tt) in KARTY.items():
    for fmt in FORMATY:
        lang = "en" if fmt.startswith("pin") else "pl"
        render(src, ai, focus, tt[lang], fmt, f"{O}{kid}-{fmt}.jpg", kid in PACK)
  print("OK", len(KARTY) * len(FORMATY))
if __name__ == "__main__": main()
