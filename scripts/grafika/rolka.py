#!/usr/bin/env python3
"""Zosia: krótka pionowa rolka 1080x1920 z jednego zdjęcia (ruchomy kadr, bez fal.ai): powolny najazd + efekt (snow|ogien).
Użycie: rolka.py wej.jpg wyj.mp4 --efekt snow|ogien [--sek 7]"""
import argparse, random, subprocess, math
from PIL import Image, ImageDraw, ImageEnhance
ap = argparse.ArgumentParser(); ap.add_argument("wej"); ap.add_argument("wyj"); ap.add_argument("--efekt", default="snow"); ap.add_argument("--sek", type=float, default=7)
a = ap.parse_args()
W, H, FPS = 1080, 1920, 30; N = int(a.sek * FPS)
src = Image.open(a.wej).convert("RGB")
r = max(W / src.width, H / src.height) * 1.0
base = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
bx, by = (base.width - W) // 2, (base.height - H) // 2
logo = Image.open("marketing/logo/fudali-logo.png").convert("RGBA"); lw = 230
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
pl = Image.new("RGBA", (lw + 32, logo.height + 26), (0, 0, 0, 0))
ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=16, fill=(250, 245, 234, 235))
random.seed(7)
flakes = [[random.uniform(0, W), random.uniform(0, H), random.uniform(2, 6), random.uniform(1.5, 4)] for _ in range(140)]
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", a.wyj], stdin=subprocess.PIPE)
for i in range(N):
    t = i / (N - 1); z = 1.0 + 0.16 * (t * t * (3 - 2 * t))  # łagodny najazd
    cw, ch = W / z, H / z
    x0 = bx + (W - cw) / 2 + 20 * t; y0 = by + (H - ch) / 2 + 30 * t
    fr = base.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)
    if a.efekt == "ogien":
        fr = ImageEnhance.Brightness(fr).enhance(1.0 + 0.05 * math.sin(i * 0.55) + 0.03 * math.sin(i * 1.7))
        fr = ImageEnhance.Color(fr).enhance(1.08)
    fr = fr.convert("RGBA")
    if a.efekt == "snow":
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for f in flakes:
            f[1] = (f[1] + f[3] * 2.2) % H; f[0] = (f[0] + math.sin((f[1] + i) / 60) * 1.2) % W
            d.ellipse((f[0] - f[2], f[1] - f[2], f[0] + f[2], f[1] + f[2]), fill=(255, 255, 255, 190))
        fr = Image.alpha_composite(fr, ov)
    fr.alpha_composite(pl, (40, 60)); fr.alpha_composite(logo, (56, 73))
    ff.stdin.write(fr.convert("RGB").tobytes())
ff.stdin.close(); ff.wait(); print("OK", a.wyj)
