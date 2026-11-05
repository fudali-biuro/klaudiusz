#!/usr/bin/env python3
"""Karuzela „Leżak – prezent na maj”: 5 slajdów 1080x1350 z prawdziwych zdjęć + nakładki graficzne (produkt nieprzerabiany)."""
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
import os
W, H = 1080, 1350
Z = "marketing/zdjecia/lezak/"
OUT = "marketing/zdjecia/karuzela-prezent/"
CREAM = (248, 241, 227); GREEN = (31, 58, 44); WOOD = (201, 141, 74); DARK = (28, 22, 16)
FD = "/usr/share/fonts/truetype/dejavu/"
def F(sz, bold=True, serif=True):
    n = ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf") if serif else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(FD + n, sz)

def cover(img, focus=(0.5, 0.5)):
    r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = int((img.width - W) * focus[0]); y = int((img.height - H) * focus[1])
    return img.crop((x, y, x + W, y + H))

def gradient(img, y0, y1, color, a0, a1):
    ov = Image.new("RGBA", (W, H), color + (0,))
    px = ov.load()
    for y in range(H):
        t = 0 if y <= y0 else 1 if y >= y1 else (y - y0) / (y1 - y0)
        a = int(a0 + (a1 - a0) * t)
        for x in range(W): px[x, y] = color + (a,)
    return Image.alpha_composite(img.convert("RGBA"), ov)

def wrap(d, text, font, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= maxw: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
    return lines

def text_block(d, text, font, x, y, maxw, fill, lh=1.18, shadow=True, anchor_bottom=False, align="left"):
    lines = wrap(d, text, font, maxw)
    h = int(font.size * lh)
    if anchor_bottom: y = y - h * len(lines)
    for i, l in enumerate(lines):
        xx = x if align == "left" else x + (maxw - d.textlength(l, font=font)) / 2
        if shadow: d.text((xx + 3, y + i * h + 3), l, font=font, fill=(0, 0, 0, 150))
        d.text((xx, y + i * h), l, font=font, fill=fill)
    return y + h * len(lines)

LOGO = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
def brand(d, dark=False, y=44):
    """Logo FUDALI w lewym górnym rogu; na zdjęciach na jasnej plakietce (czytelność)."""
    lw = 230; lh = round(LOGO.height * lw / LOGO.width)
    logo = LOGO.resize((lw, lh), Image.LANCZOS)
    im = d._image
    if not dark:
        pl = Image.new("RGBA", (lw + 36, lh + 28), (0, 0, 0, 0))
        ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=18, fill=CREAM + (238,))
        im.alpha_composite(pl, (40, y - 6))
    im.alpha_composite(logo, (58, y + 8))

def dots(d, n, total=5):
    r = 7; gap = 24; x0 = W - 56 - (total - 1) * gap
    for i in range(total):
        c = CREAM + (255,) if i == n else CREAM + (110,)
        d.ellipse((x0 + i * gap - r, 70 - r, x0 + i * gap + r, 70 + r), fill=c)

def pill(d, x, y, text, font, bg, fg, padx=26, pady=14):
    w = d.textlength(text, font=font)
    d.rounded_rectangle((x, y, x + w + 2 * padx, y + font.size + 2 * pady), radius=40, fill=bg)
    d.text((x + padx, y + pady - 2), text, font=font, fill=fg)
    return x + w + 2 * padx

def slide_photo(n, file, focus, headline, sub=None, small=None, hsize=84, grad_from=720, tag=None):
    img = cover(Image.open(Z + file).convert("RGB"), focus)
    img = gradient(img, grad_from, H, (22, 30, 24), 0, 235)
    img = gradient(img, 0, 220, (0, 0, 0), 110, 0)
    d = ImageDraw.Draw(img)
    brand(d); dots(d, n)
    if tag: pill(d, 56, 170, tag, F(28, True, False), WOOD + (255,), DARK + (255,))
    y = H - 70
    if small:
        y = text_block(d, small, F(30, False, False), 56, y, W - 112, CREAM + (230,), lh=1.3, shadow=False, anchor_bottom=True) if False else y
    lines = wrap(d, headline, F(hsize), W - 112)
    total = len(lines) * int(hsize * 1.14)
    sub_h = 0
    if sub:
        sl = wrap(d, sub, F(36, False, False), W - 112); sub_h = len(sl) * 50 + 22
    ytop = H - 80 - total - sub_h
    d.rectangle((56, ytop - 28, 56 + 90, ytop - 20), fill=WOOD + (255,))
    yy = text_block(d, headline, F(hsize), 56, ytop, W - 112, CREAM + (255,), lh=1.14)
    if sub: text_block(d, sub, F(36, False, False), 56, yy + 14, W - 112, CREAM + (235,), lh=1.38, shadow=True)
    return img.convert("RGB")

def slide_last():
    bg = Image.new("RGB", (W, H), CREAM)
    p = Image.open(Z + "03-packshot-naturalny.jpg").convert("RGB")
    p = p.resize((940, 940), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), CREAM)
    canvas.paste(Image.new("RGB", (940, 940), CREAM), (70, 130))
    layer = Image.new("RGB", (W, H), (255, 255, 255)); layer.paste(p, (70, 130))
    bg = ImageChops.multiply(canvas.copy(), layer)  # białe tło packshotu -> kremowe
    img = bg.convert("RGBA")
    d = ImageDraw.Draw(img)
    # dolny panel ciemnozielony
    d.rounded_rectangle((0, 960, W, H), radius=0, fill=GREEN + (255,))
    brand(d, dark=True); dots_dark(d)
    d.text((56, 1000), "299 zł", font=F(128), fill=CREAM + (255,))
    pill(d, 56, 1160, "poduszka w zestawie", F(32, True, False), WOOD + (255,), DARK + (255,))
    d.text((56, 1250), "🚚" if False else "Darmowa wysyłka w Polsce  ·  link w bio", font=F(34, True, False), fill=CREAM + (255,))
    d.text((56, 1298), "5 kolorów: jasny brąz · brąz · ciemny brąz · grafit · czerń", font=F(22, False, False), fill=CREAM + (170,))
    return img.convert("RGB")

def dots_dark(d):
    r = 7; gap = 24; x0 = W - 56 - 4 * gap
    for i in range(5):
        c = DARK + (255,) if i == 4 else DARK + (90,)
        d.ellipse((x0 + i * gap - r, 70 - r, x0 + i * gap + r, 70 + r), fill=c)

slides = [
    slide_photo(0, "02-dwa-lezaki-ogrod.jpg", (0.5, 0.35), "Prezent, który rozłożysz w maju", "Składany leżak z jodły. Czeka do wiosny.", tag="🎁 NA ŚWIĘTA".replace("🎁 ", "")),
    slide_photo(1, "01-taras-ognisko-drewno.jpg", (0.5, 0.6), "…a w chłodne wieczory przy ognisku", "Prezent, którego używa się cały rok.", hsize=78),
    slide_photo(2, "06-czarny-i-brazowy-poduszki.jpg", (0.5, 0.5), "Poduszka w zestawie", "Miękka, bawełniana – już w komplecie.", hsize=80),
    slide_photo(3, "05-detal-ciemny-braz-lina.jpg", (0.5, 0.5), "Jodła bieszczadzka z certyfikatem FSC", "Lina jutowa. Bez plastiku, bez śrubek do zgubienia.", hsize=70, grad_from=640),
    slide_last(),
]
os.makedirs(OUT, exist_ok=True)
for i, s in enumerate(slides, 1):
    s.save(f"{OUT}slajd-{i}.jpg", quality=93)
print("OK", len(slides))
