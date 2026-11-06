#!/usr/bin/env python3
"""Zosia: filmy TikTok koparki wg tabeli z marketing/kampanie/koparka/posty.md (zdjęcia wg numerów z ogłoszenia: 1 = plik bez sufiksu, 2–10 = „--n”).
Haczyk (1,4 s) → napisy na kolejnych ujęciach → CTA. Bez ceny (posty z ceną dopiero po akceptacji Marka).
Użycie: python3 scripts/grafika/koparka_posty.py 1 2 3   → media/post-N.mp4 + post-N.txt"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import koparka_film as K
from PIL import Image
W, H, FPS = K.W, K.H, K.FPS
POSTY = {  # nr: (haczyk, [(zdjęcie, napis, ruch0, ruch1)], opis)
 1: ("Jedna łyżka. Sześć zadań.", [(4, "Łyżka 6w1"), (2, "Nowa koparko-ładowarka 2026"), (10, "Od ręki – Rzeszów")],
     "Nowa koparko-ładowarka Shanmon Fuji 388 z łyżką 6w1. Dostępna od ręki w Rzeszowie. Oględziny i jazda próbna po umówieniu. Pisz w wiadomości."),
 2: ("Nowa. Rocznik 2026. Stoi w Rzeszowie.", [(2, "Fabrycznie nowa"), (7, "Rocznik 2026 (lipiec)"), (6, "Od ręki")],
     "Fabrycznie nowa koparko-ładowarka, rok produkcji 2026. Nie czeka się miesiącami – jest od ręki. Pisz w wiadomości."),
 3: ("5,5 metra w dół.", [(5, "Kopie do 5,5 m"), (9, "Ramię teleskopowe"), (3, "4,1 m bez wysuwu")],
     "Ramię teleskopowe: głębokość kopania do 5,5 m (4,1 m bez wysuwu). Shanmon Fuji 388, nowa, Rzeszów."),
 5: ("Zanim kupisz używaną – zobacz tę.", [(7, "Używana czy nowa?"), (2, "Nowa 2026"), (5, "Jazda próbna po umówieniu")],
     "Zanim kupisz używaną, zobacz nową. Oględziny i jazda próbna w Rzeszowie."),
 6: ("Obchód maszyny – 10 sekund", [(1, "Z każdej strony"), (7, "Z każdej strony"), (8, "Z każdej strony"), (3, "Z każdej strony"), (10, "Nowa · od ręki")],
     "Cała maszyna z każdej strony. Shanmon Fuji 388 – nowa, od ręki."),
 8: ("Szukasz koparko-ładowarki na już?", [(10, "Od ręki"), (6, "Rzeszów"), (2, "Jazda próbna")],
     "Maszyna jest od ręki, w Rzeszowie. Umów oględziny i jazdę próbną."),
 9: ("Łyżka 6w1 – po co?", [(4, "1 łyżka = wiele zadań"), (9, "Nowa maszyna"), (2, "Zapytaj o szczegóły")],
     "Łyżka przednia 6w1 – jedna maszyna do kilku zadań na budowie. Zapytaj o szczegóły w wiadomości."),
}
def idx(n): return 9 if n == 1 else 0 if n == 10 else n - 1
MOVES = [((0.5, 0.58, 0.95), (0.5, 0.55, 0.62)), ((0.55, 0.55, 0.9), (0.5, 0.58, 0.6)), ((0.5, 0.6, 0.85), (0.45, 0.55, 0.58))]
def build(nr):
    hak, sc, opis = POSTY[nr]; srcs = {}; n_sc = len(sc); durs = [3.0] + [2.4] * (n_sc - 1) if n_sc <= 3 else [2.4] + [1.6] * (n_sc - 1)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", f"{K.OUT}post-{nr}.mp4"], stdin=subprocess.PIPE)
    for i, ((foto, napis), dur) in enumerate(zip(sc, durs)):
        a0, a1 = MOVES[i % 3]
        if idx(foto) not in srcs: srcs[idx(foto)] = Image.open(K.FOTO[idx(foto)]).convert("RGB")
        for n in range(int(dur * FPS)):
            t = n / FPS
            txt = [hak] if (i == 0 and t < 1.4) else [napis]
            tt = t if not (i == 0 and t >= 1.4) else t - 1.4
            fr = K.photo_frame(srcs[idx(foto)], t, dur, a0, a1, txt) if not (i == 0 and t >= 1.4) else K.photo_frame(srcs[idx(foto)], t, dur, a0, a1, txt)
            ff.stdin.write(fr.convert("RGB").tobytes())
    for n in range(int(1.6 * FPS)): ff.stdin.write(K.card("cta", ["Pisz w", "wiadomości"], n / FPS).convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    open(f"{K.OUT}post-{nr}.txt", "w", encoding="utf-8").write(f"Post TikTok nr {nr} (posty.md)\nHaczyk: {hak}\nNapisy: " + " → ".join(n for _, n in sc) + f"\nOpis: {opis}\n(bez ceny, bez logo FUDALI, bez etykiety AI)\n")
    print("OK post", nr)
for a in (sys.argv[1:] or ["1", "2", "3"]): build(int(a))
