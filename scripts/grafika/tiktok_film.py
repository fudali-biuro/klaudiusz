#!/usr/bin/env python3
"""Zosia: krótkie pionowe filmy TikTok 1080×1920 z PRAWDZIWYCH zdjęć (ruchomy kadr, cięcia, napisy, logo, plansza CTA). Montaż – bez etykiety AI.
Użycie: python3 scripts/grafika/tiktok_film.py [kolory|material]   → marketing/zdjecia/tiktok-filmy/<nazwa>.mp4
Scena: (plik, podpis[], sekundy, (cx0,cy0,h0), (cx1,cy1,h1), mały_znacznik) – cx,cy = środek kadru (ułamek zdjęcia), h = wysokość kadru (ułamek wysokości)."""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
Z = "marketing/zdjecia/lezak/"; OUT = "marketing/zdjecia/tiktok-filmy/"; os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu/"
F = lambda sz, serif=True: ImageFont.truetype(FD + ("DejaVuSerif-Bold.ttf" if serif else "DejaVuSans-Bold.ttf"), sz)
CREAM = (250, 245, 234); GREEN = (24, 52, 38); GOLD = (214, 170, 80); RED = (178, 36, 44)
LOGO = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
FILMY = {
 "kolory": ("lezak-5-kolorow", [  # „5 kolorów” – cięcia co ~0,8 s
    ("hook", ["Który Twój?"], 1.1),
    ("03-packshot-naturalny.jpg", ["1 / 5"], 0.85, (0.5, 0.55, 0.92), (0.5, 0.5, 0.84), None),
    ("02-dwa-lezaki-ogrod.jpg", ["2 / 5"], 0.85, (0.30, 0.62, 0.55), (0.30, 0.58, 0.48), None),
    ("05-detal-ciemny-braz-lina.jpg", ["3 / 5"], 0.85, (0.5, 0.5, 1.0), (0.5, 0.5, 0.86), None),
    ("04-szary-kwitnaca-wisnia.jpg", ["4 / 5"], 0.85, (0.5, 0.6, 0.85), (0.5, 0.58, 0.75), None),
    ("06-czarny-i-brazowy-poduszki.jpg", ["5 / 5"], 0.85, (0.45, 0.55, 0.9), (0.45, 0.52, 0.8), None),
    ("cena", ["5 kolorów", "299 zł"], 1.3),
    ("end", ["fudali.com.pl", "link w bio"], 1.3)]),
 "material": ("lezak-z-czego", [  # „Z czego jest leżak?”
    ("02-dwa-lezaki-ogrod.jpg", ["Z czego jest leżak?"], 1.3, (0.5, 0.6, 0.9), (0.5, 0.62, 0.78), None),
    ("05-detal-ciemny-braz-lina.jpg", ["Jodła z certyfikatem FSC"], 1.5, (0.5, 0.5, 1.0), (0.5, 0.5, 0.82), None),
    ("04-szary-kwitnaca-wisnia.jpg", ["Lina jutowa"], 1.4, (0.28, 0.82, 0.42), (0.30, 0.78, 0.32), None),
    ("06-czarny-i-brazowy-poduszki.jpg", ["Poduszka", "w zestawie"], 1.4, (0.7, 0.55, 0.55), (0.62, 0.52, 0.48), None),
    ("cena", ["299 zł", "darmowa wysyłka"], 1.2),
    ("end", ["fudali.com.pl", "link w bio"], 1.4)]),
}
def plaque(img, w, x, y):
    lg = LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS)
    pl = Image.new("RGBA", (w + 36, lg.height + 28), (0, 0, 0, 0)); ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=18, fill=CREAM + (238,))
    img.alpha_composite(pl, (x, y)); img.alpha_composite(lg, (x + 18, y + 14))
def fit(d, lines, maxsz):
    sz = maxsz
    while sz > 44 and max(d.textlength(l, font=F(sz)) for l in lines) > W - 140: sz -= 4
    return F(sz)
def centered(fr, lines, y, a, color=CREAM, size=110, accent_last=False):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer); f = fit(dl, lines, size)
    for i, l in enumerate(lines):
        c = GOLD if accent_last and i == len(lines) - 1 else color
        dl.text((W / 2 - dl.textlength(l, font=f) / 2, y), l, font=f, fill=c + (255,)); y += int(f.size * 1.2)
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a))); return Image.alpha_composite(fr, layer)
def photo_frame(src, t, dur, a0, a1, lines):
    k = t / dur; k = k * k * (3 - 2 * k)
    cx, cy, h = [a0[i] + (a1[i] - a0[i]) * k for i in range(3)]
    ch = h * src.height; cw = ch * W / H
    if cw > src.width: cw = src.width; ch = cw * H / W
    x0 = min(max(cx * src.width - cw / 2, 0), src.width - cw); y0 = min(max(cy * src.height - ch / 2, 0), src.height - ch)
    fr = src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(H - 560, H): d.line((0, y, W, y), fill=GREEN + (int(235 * (y - (H - 560)) / 560),))
    fr = Image.alpha_composite(fr, ov); a = min(1, t / 0.25)
    fr = centered(fr, lines, H - 150 - 125 * len(lines) + int((1 - a) * 30), a, size=112 if len(lines[0]) < 12 else 92)
    plaque(fr, 260, 44, 70); return fr
def card(kind, lines, t, dur):
    a = min(1, t / 0.3); fr = Image.new("RGBA", (W, H), GREEN + (255,)); d = ImageDraw.Draw(fr)
    if kind == "hook":
        fr = centered(fr, lines, 800, a, size=130); plaque(fr, 520, W // 2 - 278, 420); return fr
    if kind == "cena":
        fr = centered(fr, lines, 700, a, size=150, accent_last=True); plaque(fr, 520, W // 2 - 278, 360)
        l2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(l2); dl.rounded_rectangle((W // 2 - 300, 1200, W // 2 + 300, 1290), radius=46, fill=RED + (255,)); dl.text((W / 2 - dl.textlength("poduszka w zestawie", font=F(42, False)) / 2, 1218), "poduszka w zestawie", font=F(42, False), fill=CREAM + (255,))
        l2.putalpha(l2.getchannel("A").point(lambda v: int(v * a))); return Image.alpha_composite(fr, l2)
    lg = LOGO.resize((760, round(LOGO.height * 760 / LOGO.width)), Image.LANCZOS); pl = Image.new("RGBA", (lg.width + 80, lg.height + 70), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=36, fill=CREAM + (255,)); fr.alpha_composite(pl, (W // 2 - pl.width // 2, 520)); fr.alpha_composite(lg, (W // 2 - lg.width // 2, 555))
    return centered(fr, lines, 960, a, size=104, accent_last=False)
def build(klucz):
    nazwa, sceny = FILMY[klucz]; srcs = {}
    tl = []
    for s in sceny:
        for k in range(int(s[2] * FPS)): tl.append((s, k / FPS))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", f"{OUT}{nazwa}.mp4"], stdin=subprocess.PIPE)
    for s, t in tl:
        if s[0] in ("hook", "cena", "end"): fr = card(s[0], s[1], t, s[2])
        else:
            if s[0] not in srcs:
                im = Image.open(Z + s[0]).convert("RGB"); r = max(1.0, 2600 / max(im.size)); srcs[s[0]] = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
            fr = photo_frame(srcs[s[0]], t, s[2], s[3], s[4], s[1])
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait(); print("OK", nazwa, sum(s[2] for s in sceny), "s")
for k in (sys.argv[1:] or list(FILMY)): build(k)
