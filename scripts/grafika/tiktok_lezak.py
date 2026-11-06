#!/usr/bin/env python3
"""Zosia: krótki film 9:16 na TikTok z PRAWDZIWYCH zdjęć leżaka (ruchomy kadr + napisy + logo + plansza końcowa z zaproszeniem na stronę).
To montaż prawdziwych zdjęć – BEZ etykiety AI. Muzykę/dźwięk dodaje się w aplikacji TikTok.
Użycie: python3 scripts/grafika/tiktok_lezak.py → marketing/zdjecia/tiktok/lezak-zaproszenie.mp4"""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
Z = "marketing/zdjecia/lezak/"; OUT = "marketing/zdjecia/tiktok/"; os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu/"
F = lambda sz, serif=True: ImageFont.truetype(FD + ("DejaVuSerif-Bold.ttf" if serif else "DejaVuSans-Bold.ttf"), sz)
CREAM = (250, 245, 234); GREEN = (24, 52, 38); GOLD = (214, 170, 80); RED = (178, 36, 44)
LOGO = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
SC = [  # zdjęcie, podpis, sekundy, fokus startowy
 ("02-dwa-lezaki-ogrod.jpg", ["Prezent, który", "rozłożysz w maju"], 3.0, (0.5, 0.75)),
 ("01-taras-ognisko-drewno.jpg", ["…a w chłodne wieczory", "przy ognisku"], 2.8, (0.5, 0.7)),
 ("06-czarny-i-brazowy-poduszki.jpg", ["Poduszka", "w zestawie"], 2.6, (0.5, 0.5)),
 ("05-detal-ciemny-braz-lina.jpg", ["Jodła z certyfikatem FSC"], 2.6, (0.5, 0.5)),
 ("03-packshot-naturalny.jpg", ["299 zł", "darmowa wysyłka"], 2.8, (0.5, 0.45)),
]
END = 3.0; XF = 0.4
def plaque(img, w, x, y):
    lg = LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS)
    pl = Image.new("RGBA", (w + 36, lg.height + 28), (0, 0, 0, 0)); ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=18, fill=CREAM + (238,))
    img.alpha_composite(pl, (x, y)); img.alpha_composite(lg, (x + 18, y + 14))
def scene_frame(base, t, dur, fokus, tekst, last):
    z = 1.0 + 0.12 * (t / dur); cw, ch = W / z, H / z
    x0 = (base.width - W) * fokus[0] + (W - cw) / 2; y0 = (base.height - H) * fokus[1] + (H - ch) / 2
    fr = base.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(H - 620, H): d.line((0, y, W, y), fill=GREEN + (int(235 * (y - (H - 620)) / 620),))
    fr = Image.alpha_composite(fr, ov); d = ImageDraw.Draw(fr)
    a = min(1, t / 0.5); off = int((1 - a) * 40)  # napis wjeżdża i się pojawia
    sz = 92
    while sz > 48 and max(d.textlength(l, font=F(sz)) for l in tekst) > W - 140: sz -= 4
    f = F(sz); yy = H - 330 - 110 * (len(tekst) - 1) + off
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
    if last: dl.rounded_rectangle((70, yy - 90, 70 + 0.001, yy - 90), radius=1)
    dl.rectangle((70, yy - 36, 160, yy - 28), fill=GOLD + (255,))
    for l in tekst: dl.text((70, yy), l, font=f, fill=CREAM + (255,)); yy += 112
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a))); fr = Image.alpha_composite(fr, layer)
    plaque(fr, 260, 44, 70); return fr
def end_frame(t):
    fr = Image.new("RGBA", (W, H), GREEN + (255,)); d = ImageDraw.Draw(fr); a = min(1, t / 0.5)
    lg = LOGO.resize((760, round(LOGO.height * 760 / LOGO.width)), Image.LANCZOS); pl = Image.new("RGBA", (lg.width + 80, lg.height + 70), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=36, fill=CREAM + (255,)); fr.alpha_composite(pl, (W // 2 - pl.width // 2, 520)); fr.alpha_composite(lg, (W // 2 - lg.width // 2, 555))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
    for txt, f, y, c in (("Składany leżak z jodły", F(64), 900, CREAM), ("Zobacz na", F(54, False), 1060, CREAM), ("fudali.com.pl", F(96), 1130, GOLD)):
        dl.text((W // 2 - dl.textlength(txt, font=f) / 2, y), txt, font=f, fill=c + (255,))
    dl.rounded_rectangle((W // 2 - 250, 1330, W // 2 + 250, 1410), radius=44, fill=RED + (255,)); dl.text((W // 2 - dl.textlength("darmowa wysyłka", font=F(40, False)) / 2, 1348), "darmowa wysyłka", font=F(40, False), fill=CREAM + (255,))
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a))); return Image.alpha_composite(fr, layer)
bases = []
for f, *_ in SC:
    im = Image.open(Z + f).convert("RGB"); r = max(W / im.width, H / im.height) * 1.0; bases.append(im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", OUT + "lezak-zaproszenie.mp4"], stdin=subprocess.PIPE)
frames_total = sum(int(s[2] * FPS) for s in SC) + int(END * FPS)
timeline = []  # (typ, indeks, t, dur)
for i, (f, tekst, dur, fok) in enumerate(SC):
    for k in range(int(dur * FPS)): timeline.append(("s", i, k / FPS, dur))
for k in range(int(END * FPS)): timeline.append(("e", 0, k / FPS, END))
def render(item):
    typ, i, t, dur = item
    if typ == "e": return end_frame(t)
    return scene_frame(bases[i], t, dur, SC[i][3], SC[i][1], i == len(SC) - 1)
prev = None
for n, item in enumerate(timeline):
    fr = render(item)
    typ, i, t, dur = item
    if t < XF and n > 0:  # przenikanie z poprzedniej sceny
        pf = render(timeline[n - 1]); fr = Image.blend(pf.convert("RGB"), fr.convert("RGB"), min(1, (t + 1 / FPS) / XF)).convert("RGBA") if False else Image.blend(prev.convert("RGB"), fr.convert("RGB"), (t + 1 / FPS) / XF).convert("RGBA") if prev is not None and timeline[n - 1][0:2] != item[0:2] else fr
    prev = fr if t >= XF else (prev if prev is not None else fr)
    ff.stdin.write(fr.convert("RGB").tobytes())
ff.stdin.close(); ff.wait(); print("OK", frames_total / FPS, "s")
