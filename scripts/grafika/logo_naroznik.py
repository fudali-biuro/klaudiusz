#!/usr/bin/env python3
"""Zosia: dokłada stałe logo FUDALI w lewym górnym rogu kwadratowych packshotów (1080x1080 lub 4:5 = 1080x1350). Użycie: logo_naroznik.py wej.jpg wyj.jpg"""
import sys
from PIL import Image, ImageDraw
src = Image.open(sys.argv[1]).convert("RGB")
size = (1080, 1350) if abs(src.width / src.height - 0.8) < 0.05 else (1080, 1080)
im = src.resize(size, Image.LANCZOS).convert("RGBA")
logo = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
lw = 210; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
pl = Image.new("RGBA", (lw + 32, logo.height + 26), (0, 0, 0, 0))
ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=16, fill=(250, 245, 234, 235))
im.alpha_composite(pl, (36, 36)); im.alpha_composite(logo, (52, 49))
im.convert("RGB").save(sys.argv[2], quality=93)
