#!/usr/bin/env python3
"""Zosia: filmy TikTok 9:16 – koparko-ładowarka Shanmon Fuji 388 (PRAWDZIWE zdjęcia, ruchomy kadr, duże napisy; bez logo FUDALI, bez etykiety AI).
Cena = zmienny napis: marketing/kampanie/koparka/media/cena.txt (edytuj plik i uruchom skrypt ponownie).
Użycie: python3 scripts/grafika/koparka_film.py [nowa|glebokosc|szybkie]"""
import subprocess, sys, os, glob
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
OUT = "marketing/kampanie/koparka/media/"; os.makedirs(OUT, exist_ok=True)
CENA = open(OUT + "cena.txt", encoding="utf-8").read().strip()
FOTO = sorted(glob.glob("marketing/biblioteka-zdjec/produkty/*shanmon-fuji-388*"))  # 0:'--10' 1:'--2' … 9:'' (po nazwie)
FD = "/usr/share/fonts/truetype/dejavu/"
F = lambda sz: ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", sz)
YEL = (255, 196, 0); WHITE = (255, 255, 255); BLACK = (16, 16, 16)
# indeksy zdjęć: 4=cała maszyna z daleka, 3=łyżka, 6=bok, 5=ramię z tyłu, 9=ramię+kabina, 1=przód łyżka, 2=tył+ramię, 8=las, 0=bok z ramieniem, 7=kabina z przodu
FILMY = {
 "nowa": ("koparka-nowa-2026", [
    (4, ["NOWA", "KOPARKO-ŁADOWARKA"], 2.2, (0.66, 0.62, 0.9), (0.66, 0.6, 0.62)),
    (7, ["Rok produkcji 2026"], 1.8, (0.5, 0.5, 0.9), (0.5, 0.48, 0.7)),
    (3, ["Łyżka przednia 6w1"], 2.0, (0.5, 0.62, 0.8), (0.55, 0.62, 0.6)),
    (5, ["Kopie do 5,5 m"], 2.0, (0.65, 0.5, 0.95), (0.62, 0.45, 0.65)),
    ("cena", ["{CENA}", "od ręki · Rzeszów"], 2.4),
    ("cta", ["Oględziny", "i jazda próbna", "po umówieniu"], 2.0)]),
 "glebokosc": ("koparka-5-5-m", [
    (5, ["KOPIE DO 5,5 m"], 2.2, (0.65, 0.5, 0.95), (0.62, 0.45, 0.6)),
    (9, ["Ramię teleskopowe"], 2.0, (0.45, 0.5, 0.9), (0.45, 0.45, 0.65)),
    (3, ["Łyżka 6w1"], 1.8, (0.5, 0.6, 0.8), (0.5, 0.6, 0.55)),
    (0, ["Nowa · 2026"], 1.8, (0.5, 0.55, 0.9), (0.5, 0.55, 0.65)),
    ("cena", ["{CENA}", "od ręki · Rzeszów"], 2.4),
    ("cta", ["Pisz w wiadomości", "– umówimy oględziny"], 2.0)]),
 "szybkie": ("koparka-szybkie-ciecia", [
    (4, ["NOWA 2026"], 1.0, (0.66, 0.62, 0.9), (0.66, 0.6, 0.75)),
    (3, ["ŁYŻKA 6w1"], 1.0, (0.5, 0.6, 0.85), (0.5, 0.6, 0.7)),
    (5, ["5,5 m"], 1.0, (0.65, 0.5, 0.95), (0.62, 0.46, 0.75)),
    (6, ["OD RĘKI"], 1.0, (0.5, 0.6, 0.95), (0.45, 0.58, 0.8)),
    (8, ["RZESZÓW"], 1.0, (0.55, 0.55, 0.95), (0.55, 0.55, 0.8)),
    ("cena", ["{CENA}"], 2.2),
    ("cta", ["Oględziny", "i jazda próbna"], 1.8)]),
}
def stroke_text(d, xy, t, f, fill):
    x, y = xy
    for dx in (-4, 0, 4):
        for dy in (-4, 0, 4): d.text((x + dx, y + dy), t, font=f, fill=BLACK + (255,))
    d.text((x, y), t, font=f, fill=fill + (255,))
def centered(img, lines, y, a, size=120, color=WHITE, last_color=None):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    if len(lines) == 1 and d.textlength(lines[0], font=F(size)) > W - 120 and " " in lines[0]:
        w_ = lines[0].split(); best = min(range(1, len(w_)), key=lambda k: abs(len(" ".join(w_[:k])) - len(" ".join(w_[k:]))))
        lines = [" ".join(w_[:best]), " ".join(w_[best:])]
    sz = size
    while sz > 48 and max(d.textlength(l, font=F(sz)) for l in lines) > W - 120: sz -= 4
    f = F(sz)
    for i, l in enumerate(lines):
        c = YEL if (i == 0 and len(lines) > 1 and color == WHITE and last_color == "first") else color
        stroke_text(d, (W / 2 - d.textlength(l, font=f) / 2, y), l, f, c); y += int(sz * 1.2)
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a))); return Image.alpha_composite(img, layer)
def photo_frame(src, t, dur, a0, a1, lines):
    k = t / dur; k = k * k * (3 - 2 * k); cx, cy, h = [a0[i] + (a1[i] - a0[i]) * k for i in range(3)]
    ch = h * src.height; cw = ch * W / H
    if cw > src.width: cw = src.width; ch = cw * H / W
    x0 = min(max(cx * src.width - cw / 2, 0), src.width - cw); y0 = min(max(cy * src.height - ch / 2, 0), src.height - ch)
    fr = src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(H - 700, H): d.line((0, y, W, y), fill=(0, 0, 0, int(215 * (y - (H - 700)) / 700)))
    fr = Image.alpha_composite(fr, ov); a = min(1, t / 0.2)
    nl = len(lines) if not (len(lines) == 1 and ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(lines[0], font=F(130)) > W - 120 and ' ' in lines[0]) else 2
    return centered(fr, lines, H - 160 - 135 * nl + int((1 - a) * 40), a, size=130, last_color="first")
def card(kind, lines, t):
    a = min(1, t / 0.25); fr = Image.new("RGBA", (W, H), BLACK + (255,)); d = ImageDraw.Draw(fr)
    d.rectangle((0, 0, W, 40), fill=YEL + (255,)); d.rectangle((0, H - 40, W, H), fill=YEL + (255,))
    lines = [l.replace("{CENA}", CENA) for l in lines]
    if kind == "cena":
        fr = centered(fr, lines[:1], 700, a, size=150, color=YEL)
        if len(lines) > 1: fr = centered(fr, lines[1:], 980, a, size=96, color=WHITE)
        return fr
    return centered(fr, lines, 640, a, size=110, color=WHITE)
def build(klucz):
    nazwa, sceny = FILMY[klucz]; srcs = {}
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", f"{OUT}{nazwa}.mp4"], stdin=subprocess.PIPE)
    for s in sceny:
        for n in range(int(s[2] * FPS)):
            t = n / FPS
            if isinstance(s[0], str): fr = card(s[0], s[1], t)
            else:
                if s[0] not in srcs:
                    im = Image.open(FOTO[s[0]]).convert("RGB"); srcs[s[0]] = im
                fr = photo_frame(srcs[s[0]], t, s[2], s[3], s[4], s[1])
            ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait(); print("OK", nazwa, round(sum(s[2] for s in sceny), 1), "s")
if __name__ == "__main__":
    for k in (sys.argv[1:] or list(FILMY)): build(k)
