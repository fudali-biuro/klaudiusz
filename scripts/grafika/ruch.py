#!/usr/bin/env python3
"""Zosia: „żywe ujęcia” – krótki film z realistycznych zbliżeń (prawdziwe zdjęcia albo sceny z Nano Banana).
Powolny, płynny ruch kamery (najazd / przesuw / odjazd) na każdym kadrze, miękkie przejścia, delikatne ziarno filmowe.
Bez płatnych API – produkt zostaje dokładnie taki jak na zdjęciu (ruszy się kamera, nie produkt).

Użycie:
  python3 scripts/grafika/ruch.py --zdjecia a.jpg b.jpg c.jpg --wyjscie marketing/zdjecia/x/film.mp4
      [--format 4:5|9:16|1:1] [--sek 3.2] [--logo]
Wynik: MP4 (H.264, 30 kl/s, bez dźwięku) gotowy na IG/TikTok/Pinterest.
"""
import argparse, subprocess
from PIL import Image, ImageDraw

FORMATY = {"4:5": (1080, 1350), "9:16": (1080, 1920), "1:1": (1080, 1080)}
RUCHY = [  # (zoom od, zoom do, przesuw x od→do, przesuw y od→do) – przesuw w ułamkach wolnego marginesu
    (1.00, 1.13, (0.0, 0.25), (0.0, 0.15)),    # najazd
    (1.08, 1.08, (-0.8, 0.8), (0.0, 0.0)),     # przesuw w prawo
    (1.14, 1.02, (0.2, -0.1), (0.3, 0.0)),     # odjazd
    (1.08, 1.08, (0.0, 0.0), (0.8, -0.8)),     # przesuw w górę
]
FPS, PRZEJSCIE = 30, 14  # klatki przenikania


def wygladz(t):
    return t * t * (3 - 2 * t)


def ujecie(sciezka, W, H, n, ruch):
    src = Image.open(sciezka).convert("RGB")
    s = max(W / src.width, H / src.height)          # „cover” – kadr wypełnia ekran
    z0, z1, (px0, px1), (py0, py1) = ruch
    for i in range(n):
        t = wygladz(i / max(n - 1, 1))
        z = z0 + (z1 - z0) * t
        okno_w, okno_h = W / (s * z), H / (s * z)    # wycinek źródła (w pikselach źródła)
        mx, my = (src.width - okno_w) / 2, (src.height - okno_h) / 2
        x0 = mx + mx * (px0 + (px1 - px0) * t)
        y0 = my + my * (py0 + (py1 - py0) * t)
        k = okno_w / W                              # subpikselowa transformacja = płynny ruch bez drgań
        yield src.transform((W, H), Image.AFFINE, (k, 0, x0, 0, k, y0), resample=Image.BICUBIC)


def logo_naklejka(W):
    lg = Image.open("marketing/logo/fudali-logo.png").convert("RGBA"); lw = round(W * 0.2)
    lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
    pl = Image.new("RGBA", (lw + 32, lg.height + 26), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=16, fill=(250, 245, 234, 235))
    pl.alpha_composite(lg, (16, 13))
    return pl


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zdjecia", nargs="+", required=True)
    ap.add_argument("--wyjscie", required=True)
    ap.add_argument("--format", default="4:5", choices=FORMATY)
    ap.add_argument("--sek", type=float, default=3.2, help="długość jednego ujęcia")
    ap.add_argument("--logo", action="store_true", help="logo FUDALI w rogu")
    a = ap.parse_args()
    W, H = FORMATY[a.format]
    n = round(a.sek * FPS) + PRZEJSCIE
    logo = logo_naklejka(W) if a.logo else None
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-vf", "noise=alls=3:allf=t", "-c:v", "libx264", "-preset", "slow",
                           "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.wyjscie], stdin=subprocess.PIPE)
    ogon = []  # ostatnie klatki poprzedniego ujęcia – przenikają się z początkiem następnego
    for nr, sciezka in enumerate(a.zdjecia):
        ostatnie, nowy_ogon = nr == len(a.zdjecia) - 1, []
        for i, kl in enumerate(ujecie(sciezka, W, H, n, RUCHY[nr % len(RUCHY)])):
            if i < len(ogon):
                kl = Image.blend(ogon[i], kl, wygladz((i + 1) / (len(ogon) + 1)))
            elif not ostatnie and i >= n - PRZEJSCIE:
                nowy_ogon.append(kl); continue
            if logo:
                kl = kl.convert("RGBA"); kl.alpha_composite(logo, (36, 36)); kl = kl.convert("RGB")
            ff.stdin.write(kl.tobytes())
        ogon = nowy_ogon
    ff.stdin.close()
    if ff.wait():
        raise SystemExit("ffmpeg: nie wyszło")
    print(f"OK {a.wyjscie} ({len(a.zdjecia)} ujęć, {W}x{H})")


if __name__ == "__main__":
    main()
