#!/usr/bin/env python3
"""Zosia: pierwsza siatka Instagram FUDALI (strategia.md): grafiki 9 postów P1–P9, siatka 3×3, okładki wyróżnionych relacji. PRAWDZIWE zdjęcia z biblioteki + montaż (bez etykiety AI).
Styl serii: ciepły krem + ciemna zieleń + drewno; logo FUDALI (plakietka) lewy górny róg, etykieta tematu prawy górny, nagłówek serif, złota kreska.
Użycie: python3 scripts/grafika/ig_serie.py [posty|reelsy|siatka|okladki]  (domyślnie wszystko)  → marketing/instagram/…"""
import glob, os, sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W, H = 1080, 1350
B = "marketing/biblioteka-zdjec/"; OUT = "marketing/instagram/"
CREAM = (250, 245, 234); GREEN = (24, 52, 38); GOLD = (214, 170, 80); WOOD = (176, 120, 66)
FD = "/usr/share/fonts/truetype/dejavu/"
F = lambda sz, bold=True: ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), sz)
FS = lambda sz: ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", sz)
LOGO = Image.open("marketing/logo/fudali-logo.png").convert("RGBA")
def g(k, sek="*"): return sorted(glob.glob(B + f"{sek}/*{k}*"))[0]
def pro(n): return sorted(glob.glob(B + f"produkty/*produktywniej*fud-{n}.jpg"))[0] if n else sorted(glob.glob(B + "produkty/*produktywniej*fud.jpg"))[0]
def rd(p): return Image.open(p).convert("RGB")
def cover(im, w, h, fx=0.5, fy=0.5, zoom=1.0):
    r = max(w / im.width, h / im.height) * zoom; im = im.resize((round(im.width * r) + 1, round(im.height * r) + 1), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def cream_bg(w=W, h=H):
    bg = Image.new("RGB", (w, h)); d = ImageDraw.Draw(bg)
    for y in range(h): d.line((0, y, w, y), fill=tuple(int(a + (b - a) * y / h) for a, b in zip((246, 240, 228), (226, 214, 196))))
    return bg
def on_cream(path, width=1000, y=90, w=W, h=H):
    """zdjęcie studyjne na białym tle → multiply na kremowe tło (pełna jakość, bez wycinania)"""
    bg = cream_bg(w, h); im = rd(path); r = width / im.width; im = im.resize((width, round(im.height * r)), Image.LANCZOS)
    x = (w - width) // 2; region = bg.crop((x, y, x + im.width, y + im.height)); bg.paste(ImageChops.multiply(region, im), (x, y)); return bg
def wrap(d, t, f, mw):
    out, cur = [], ""
    for w_ in t.split():
        x = (cur + " " + w_).strip()
        if d.textlength(x, font=f) <= mw: cur = x
        else: out.append(cur); cur = w_
    return out + [cur]
def chrome(img, tag=None, head=None, sub=None, dark=False, hs=None, w=W, h=H, grad=True, rgba=False, logo=True, top=False, small=False):
    img = img.convert("RGBA"); d = ImageDraw.Draw(img)
    if head and top and not dark:
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d0 = ImageDraw.Draw(ov)
        for y in range(0, 620): d0.line((0, y, w, y), fill=GREEN + (int(225 * (1 - y / 620) ** 1.2),))
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img)
    if head and grad and not dark and not top:
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d0 = ImageDraw.Draw(ov); gh = int(h * 0.36)
        for y in range(h - gh, h): d0.line((0, y, w, y), fill=GREEN + (int(225 * ((y - (h - gh)) / gh) ** 1.15),))
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img)
    if logo:
        lg = LOGO.resize((150, round(LOGO.height * 150 / LOGO.width)), Image.LANCZOS); pl = Image.new("RGBA", (lg.width + 22, lg.height + 18), (0, 0, 0, 0))
        ImageDraw.Draw(pl).rounded_rectangle((0, 0, pl.width - 1, pl.height - 1), radius=12, fill=CREAM + (232,)); img.alpha_composite(pl, (32, 32)); img.alpha_composite(lg, (43, 41))
    if head:
        hs = hs or ((46 if len(head) < 34 else 40 if len(head) < 60 else 36) if small else (62 if len(head) < 34 else 54 if len(head) < 60 else 46)); f = FS(hs); lines = wrap(d, head, f, w - 110)
        SF = F(max(32, int(hs * 0.5)), False); sl = wrap(d, sub, SF, w - 110) if sub else []
        block = len(lines) * int(hs * 1.16) + (len(sl) * int(SF.size * 1.38) + 12 if sl else 0); y = 230 if top else h - 70 - block
        col = GREEN if dark else CREAM
        d.rectangle((56, y - 24, 126, y - 18), fill=GOLD + (255,))
        for l in lines: d.text((56, y), l, font=f, fill=col + (255,)); y += int(hs * 1.16)
        y += 12
        for l in sl: d.text((56, y), l, font=SF, fill=col + (235,)); y += int(SF.size * 1.38)
    return img if rgba else img.convert("RGB")
def grade(img):
    """jedna korekta barwna całej serii: ciepło (lekko złoty) + podobny kontrast"""
    from PIL import ImageEnhance
    img = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.05); r, g_, b = img.split()
    r = r.point(lambda v: min(255, int(v * 1.035))); b = b.point(lambda v: int(v * 0.95)); return Image.merge("RGB", (r, g_, b))
def save(img, path): os.makedirs(os.path.dirname(path), exist_ok=True); grade(img).save(path, quality=94)
def sprite(path):
    im = rd(path); L = ImageChops.darker(ImageChops.darker(*im.split()[:2]), im.split()[2]); ImageDraw.floodfill(L, (0, 0), 0, thresh=26)
    a = L.point(lambda v: 255 if v else 0).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.1))
    s = im.convert("RGBA"); s.putalpha(a); return s.crop(s.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())
def kolory5():
    img = cream_bg().convert("RGBA"); TH = 400; ch = [g("packshot-lezaka-w-kolorze-naturalnym"), pro(13), pro(2), pro(5), pro(4)]
    sp = []
    for p in ch: s = sprite(p); sp.append(s.resize((round(s.width * TH / s.height), TH), Image.LANCZOS))
    def put(img, s, x, base):
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((x + s.width * 0.12, base - 12, x + s.width * 0.92, base + 18), fill=(60, 45, 30, 105))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(12))); img.alpha_composite(s, (x, base - TH)); return img
    w0 = sp[0].width; gap = (W - 80 - 3 * w0) / 2
    for i in range(3): img = put(img, sp[i], int(40 + i * (w0 + gap)), 600)
    x1 = int((W - (sp[3].width + sp[4].width + 30)) / 2); img = put(img, sp[3], x1, 990); img = put(img, sp[4], x1 + sp[3].width + 30, 990)
    return img.convert("RGB")
K = ["Jasny brąz", "Brąz", "Ciemny brąz", "Grafit", "Czerń"]; KF = [18, 17, 15, 16, 14]
ANIM = sorted(glob.glob(B + "produkty/*7b25c15*.mp4"))[0]; BOX = (402, 190, 822, 668)
def anim_frames():
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", ANIM, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = 1152 * 720 * 3; return [Image.frombytes("RGB", (1152, 720), r[i:i + n]) for i in range(0, len(r) - n + 1, n)]
def anim_canvas(t, h=H, frames=[]):
    if not frames: frames.extend(anim_frames())
    f = frames[min(len(frames) - 1, int(t * 20))].crop(BOX).resize((W, round((BOX[3] - BOX[1]) * W / (BOX[2] - BOX[0]))), Image.LANCZOS)
    f = f.point(lambda v: min(255, int(v * 255 / 212)))  # tło animacji (szare) → białe, żeby wtopiło się w krem
    bg = cream_bg(W, h); y = (h - f.height) // 2 - 80; bg.paste(ImageChops.multiply(bg.crop((0, y, W, y + f.height)), f), (0, y)); return bg
def reel(path, sceny, fps=30):
    """sceny: [(funkcja t→obraz RGB 1080×1920, nakładka RGBA lub None, sekundy)]"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", path], stdin=subprocess.PIPE)
    for fn, ov, sec in sceny:
        for i in range(int(sec * fps)):
            fr = fn(i / fps).convert("RGBA")
            if ov is not None:
                o = ov.copy(); a = min(1, (i / fps) / 0.35); o.putalpha(o.getchannel("A").point(lambda v: int(v * a))); fr = Image.alpha_composite(fr, o)
            ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
def overlay(tag, head, sub=None, dark=False):
    return chrome(Image.new("RGBA", (W, 1920), (0, 0, 0, 0)), None, head, sub, dark=dark, w=W, h=1920, rgba=True)
def kb(img, zoom0=1.0, zoom1=1.15, sec=4.0, fy=0.5):
    def f(t): return cover(img, W, 1920, 0.5, fy, zoom0 + (zoom1 - zoom0) * min(1, t / sec))
    return f
def zoomcream(path, sec, y=380):
    return lambda t: on_cream(path, int(940 + 90 * min(1, t / sec)), y, W, 1920)
def reelsy():
    P = OUT + "posty/"
    a, b = rd(g("wyciete-blaty")), rd(g("stolik-patek-blat"))
    reel(P + "P3-reel.mp4", [(kb(a, 1.0, 1.2, 4), overlay(None, "Od płatka do stolika"), 4.0), (kb(b, 1.0, 1.2, 4, 0.55), overlay(None, "Tak to wygląda od środka"), 4.0),
                          (lambda t: cream_bg(W, 1920), overlay(None, "Który kształt blatu wolisz?", "Napisz w komentarzu.", dark=True), 2.5)])
    wi = rd(g("szary-grafitowo"))
    reel(P + "P7-reel.mp4", [(zoomcream(pro(10), 2.6), overlay(None, "Składa się na płasko", dark=True), 2.6), (zoomcream(pro(5), 2.6), overlay(None, "Rozkładasz – siedzisz.", dark=True), 2.6),
                           (kb(wi, 1.0, 1.15, 3.2, 0.55), overlay(None, "Jodła · 10 kg"), 3.2), (lambda t: cream_bg(W, 1920), overlay(None, "Chcesz film z warsztatu?", "Napisz TAK.", dark=True), 1.6)])
def siatka():
    P = OUT + "posty/"; kol = [["P9/slajd-1", "P8/slajd-1", "P7/okladka"], ["P6/slajd-1", "P5/slajd-1", "P4/slajd-1"], ["P3/okladka", "P2/slajd-1", "P1/slajd-1"]]
    tw, th, gp = 360, 480, 4; m = Image.new("RGB", (3 * tw + 4 * gp, 3 * th + 4 * gp + 90), (238, 232, 220)); d = ImageDraw.Draw(m)
    d.text((gp + 12, 24), "fudali_nowoczesne_stolarstwo – podgląd siatki po 9 postach", font=F(26), fill=GREEN)
    for r, row in enumerate(kol):
        for c, nm in enumerate(row):
            im = Image.open(P + nm + ".jpg").convert("RGB"); cw = round(H * 3 / 4); im = im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((tw, th), Image.LANCZOS)
            m.paste(im, (gp + c * (tw + gp), 90 + gp + r * (th + gp)))
    save(m, OUT + "siatka-3x3.jpg")
def ikona(nm, d, c=(540, 960)):
    x0, y0 = c[0] - 180, c[1] - 180; L = lambda *p, w=18: d.line([(x0 + a, y0 + b) for a, b in zip(p[::2], p[1::2])], fill=GREEN, width=w, joint="curve")
    if nm == "lezak":
        L(95, 50, 195, 240); L(195, 240, 305, 215); L(195, 240, 150, 325); L(255, 227, 300, 325); L(80, 78, 128, 40, w=26)
    elif nm == "gear":
        d.ellipse((x0 + 90, y0 + 90, x0 + 270, y0 + 270), outline=GREEN, width=18); d.ellipse((x0 + 140, y0 + 140, x0 + 220, y0 + 220), outline=GREEN, width=18)
        for k in range(8):
            a = k * math.pi / 4; L(180 + 90 * math.cos(a), 180 + 90 * math.sin(a), 180 + 128 * math.cos(a), 180 + 128 * math.sin(a), w=34)
    elif nm == "dom":
        L(35, 175, 180, 50, 320, 175); L(80, 160, 80, 310, 280, 310, 280, 160); L(150, 310, 150, 225, 210, 225, 210, 310)
    elif nm == "kropla":
        pts = [(x0 + 270 - 180 * t + 85 * math.sin(math.pi * t) * sg * 1.0 * (0.9), y0 + 60 + 240 * t + 85 * math.sin(math.pi * t) * sg * 0.9) for sg in (1, -1) for t in ([i / 30 for i in range(31)] if sg == 1 else [i / 30 for i in range(30, -1, -1)])]
        d.line(pts + [pts[0]], fill=GREEN, width=18, joint="curve"); L(255, 75, 110, 285, w=12)
    elif nm == "prezent":
        L(60, 150, 60, 310, 300, 310, 300, 150); L(40, 112, 320, 112, 320, 150, 40, 150, 40, 112); L(180, 112, 180, 310)
        d.ellipse((x0 + 105, y0 + 40, x0 + 180, y0 + 112), outline=GREEN, width=16); d.ellipse((x0 + 180, y0 + 40, x0 + 255, y0 + 112), outline=GREEN, width=16)
    elif nm == "pytanie":
        f = F(330); d.text((c[0] - d.textlength("?", font=f) / 2, c[1] - 215), "?", font=f, fill=GREEN)
def okladki():
    D = OUT + "wyroznione/"; os.makedirs(D, exist_ok=True); lista = [("Leżak", "lezak"), ("Jak to robimy", "gear"), ("Realizacje", "dom"), ("Pielęgnacja", "kropla"), ("Prezenty", "prezent"), ("Pytania", "pytanie")]; pr = []
    for nm, ic in lista:
        im = cream_bg(W, 1920).convert("RGBA"); d = ImageDraw.Draw(im)
        d.ellipse((540 - 340, 960 - 340, 540 + 340, 960 + 340), fill=(252, 249, 242, 255), outline=WOOD + (255,), width=16)
        t_ = Image.new('RGBA', (360, 360), (0, 0, 0, 0)); ikona(ic, ImageDraw.Draw(t_), (180, 180)); t_ = t_.resize((540, 540), Image.LANCZOS); im.alpha_composite(t_, (270, 690))
        f = FS(84); d.text((540 - d.textlength(nm, font=f) / 2, 1360), nm, font=f, fill=GREEN + (255,)); d.rectangle((540 - 45, 1340, 540 + 45, 1346), fill=GOLD + (255,))
        im = im.convert("RGB"); im.save(D + f"okladka-{ic}.png"); pr.append(im)
    m = Image.new("RGB", (6 * 230, 250), (60, 60, 60))
    for i, im in enumerate(pr):
        c = im.crop((140, 560, 940, 1360)).resize((200, 200), Image.LANCZOS); mk = Image.new("L", (200, 200), 0); ImageDraw.Draw(mk).ellipse((0, 0, 199, 199), fill=255); m.paste(c, (15 + i * 230, 25), mk)
    m.save(D + "podglad-kolka.png")

def posty():
    P = OUT + "posty/"
    C = lambda **k: dict(logo=False, small=True, **k)   # okładka: bez logo, mały napis (tylko P1, P4, P6)
    # P1 – 5 kolorów (6 slajdów)
    for i, (n, nm) in enumerate(zip(KF, K)):
        im = cover(rd(pro(n)), W, H, 0.5, 0.5)
        if i == 0: save(chrome(im, head="5 kolorów. Który Twój?", **C()), P + "P1/slajd-1.jpg")
        else: save(chrome(im, head=f"{i+1} · {nm}"), P + f"P1/slajd-{i+1}.jpg")
    save(chrome(kolory5(), head="Który Twój?", sub="1 jasny brąz · 2 brąz · 3 ciemny brąz · 4 grafit · 5 czerń. Napisz numer w komentarzu.", dark=True), P + "P1/slajd-6.jpg")
    # P2 – leżak na zimę (5): okładka = czyste zdjęcie
    save(cover(rd(g("lezaki-realizacja")), W, H, 0.5, 0.55), P + "P2/slajd-1.jpg")
    save(chrome(on_cream(pro(10), 1000, 70), head="Leżak na zimę – 3 zasady", dark=True), P + "P2/slajd-2.jpg")
    save(chrome(on_cream(pro(11), 1000, 70), head="1 · Sucho", dark=True), P + "P2/slajd-3.jpg")
    save(chrome(on_cream(pro(0), 1000, 70), head="2 · Przewiewnie", dark=True), P + "P2/slajd-4.jpg")
    save(chrome(cover(rd(g("taras-z-palenisko")), W, H, 0.5, 0.6), head="3 · Z dala od wilgoci i dużego ciepła", sub="Zapisz, zanim spadnie śnieg."), P + "P2/slajd-5.jpg")
    # P3 – okładka (reel osobno)
    save(cover(rd(g("wyciete-blaty")), W, H, 0.5, 0.4), P + "P3/okladka.jpg")
    # P4 – z czego jest leżak (5): okładka = cały leżak
    save(chrome(on_cream(pro(3), 1000, 90), head="10 kg · 30 mm", dark=True, **C()), P + "P4/slajd-1.jpg")
    save(chrome(on_cream(pro(12), 1000, 70), head="100 × 55 × 90 cm", sub="Rama 30 mm · listwy 50 mm · waga 10 kg", dark=True), P + "P4/slajd-2.jpg")
    save(chrome(on_cream(pro(19), 1000, 70), head="Złożony: 125 × 55 × 25 cm", dark=True), P + "P4/slajd-3.jpg")
    save(chrome(on_cream(pro(20), 1000, 120), head="Poduszka w zestawie", dark=True), P + "P4/slajd-4.jpg")
    save(chrome(on_cream(pro(21), 1000, 120), head="Lina jutowa", sub="Co chcesz zobaczyć z bliska? Napisz w komentarzu.", dark=True), P + "P4/slajd-5.jpg")
    # P5 – czyste zdjęcie
    save(cover(rd(g("taras-z-palenisko")), W, H, 0.5, 0.55), P + "P5/slajd-1.jpg")
    # P6 – prezent dla taty (4)
    save(chrome(cover(rd(g("trzy-drewniane-otwieracze")), W, H, 0.5, 0.45), head="Prezent dla taty · od 49 zł", **C()), P + "P6/slajd-1.jpg")
    save(chrome(cover(rd(g("podkadki-z-orzecha")), W, H, 0.5, 0.35), head="Podkładka z orzecha czarnego", sub="99 zł"), P + "P6/slajd-2.jpg")
    save(chrome(cover(rd(g("skadany-drewniany-stolik-taboret-z-lina-na-parkiec.jpg")), W, H, 0.5, 0.5), head="Składany stolik kawowy", sub="229 zł"), P + "P6/slajd-3.jpg")
    save(chrome(cover(rd(g("dwa-lezaki-z-poduszkami")), W, H, 0.5, 0.6), head="Leżak z poduszką w zestawie", sub="299 zł · darmowa wysyłka. Komu to wyślesz?"), P + "P6/slajd-4.jpg")
    # P7 – okładka reelu = prawdziwe zdjęcie leżaka
    save(cover(rd(g("szary-grafitowo")), W, H, 0.5, 0.55), P + "P7/okladka.jpg")
    # P8 – lato na tarasie (3), bez „klienta”
    save(cover(rd(g("dwa-lezaki-z-poduszkami")), W, H, 0.5, 0.6), P + "P8/slajd-1.jpg")
    save(chrome(cover(rd(g("dwa-lezaki-z-poduszkami")), W, H, 0.3, 0.7, 1.5), head="Dwa leżaki, taras i trawnik – tak wygląda lato"), P + "P8/slajd-2.jpg")
    save(chrome(cover(rd(g("image-20260904-110937-616")), W, H, 0.5, 0.55), head="Jak urządzasz swój taras?", sub="Napisz w komentarzu."), P + "P8/slajd-3.jpg")
    # P9 – dąb czy jodła (5)
    save(cover(rd(g("zestaw-drewnianych-stokow-dab-rozstawionych-na-par-2.jpg")), W, H, 0.5, 0.5), P + "P9/slajd-1.jpg")
    save(chrome(on_cream(pro(13), 1000, 70), head="Leżak: jodła bieszczadzka z certyfikatem FSC", dark=True), P + "P9/slajd-2.jpg")
    save(chrome(cover(rd(g("zestaw-drewnianych-stokow-dab-rozstawionych-na-par.jpg")), W, H, 0.5, 0.5), head="Stołki: dąb czerwony"), P + "P9/slajd-3.jpg")
    save(chrome(cover(rd(g("stolik-patek-blat")), W, H, 0.5, 0.5), head="Stolik Płatek: dąb czerwony"), P + "P9/slajd-4.jpg")
    save(chrome(on_cream(pro(7), 1000, 70), head="Jodła czy dąb?", sub="Głosuj w komentarzu.", dark=True), P + "P9/slajd-5.jpg")
def stories():
    """Stories na 7 dni (9–15.11): 1080×1920, mało tekstu, pola interaktywne (ankieta/quiz/pytanie) zostają puste – naklejki w aplikacji"""
    D = OUT + "stories/"; SH, SW = 1920, W
    def ph(path, fx=0.5, fy=0.5, zoom=1.0): return cover(rd(path), SW, SH, fx, fy, zoom)
    def cr(path, y=330, width=1000): return on_cream(path, width, y, SW, SH)
    def fr(day, n, img, head=None, sub=None, top=False, dark=False, logo=True): save(chrome(img, head=head, sub=sub, dark=dark, w=SW, h=SH, top=top, logo=logo, hs=80 if head and len(head) < 26 else 66), D + f"D{day}/klatka-{n}.jpg")
    cta = lambda: cream_bg(SW, SH)
    CTA = ("Pisz w wiadomości", "wycena · wymiary · dostawa")
    # D1 pon – Jodła czy dąb? (ankieta)
    fr(1, 1, cr(pro(13), 380), "Leżak: jodła", "bieszczadzka, certyfikat FSC", dark=True)
    fr(1, 2, ph(g("zestaw-drewnianych-stokow-dab-rozstawionych-na-par.jpg")), "Stołki: dąb czerwony")
    fr(1, 3, cta(), "Jodła czy dąb?", "Głosuj w ankiecie", top=True, dark=True)
    fr(1, 4, cta(), *CTA, top=True, dark=True)
    # D2 wt – Ile waży leżak? (quiz 5 / 10 / 15 kg)
    fr(2, 1, cr(pro(0), 330), "Ile waży nasz leżak?", None, dark=True)
    fr(2, 2, cta(), "5 · 10 · 15 kg?", "Wybierz odpowiedź", top=True, dark=True)
    fr(2, 3, ph(g("dwa-lezaki-z-poduszkami"), 0.5, 0.6), "10 kg", "Tyle waży leżak. Składa się na płasko.")
    fr(2, 4, cta(), *CTA, top=True, dark=True)
    # D3 śr – z czego to zrobione
    fr(3, 1, cr(pro(21), 380), "Lina jutowa", dark=True)
    fr(3, 2, ph(pro(15)), "Listwy z jodły", "certyfikat FSC")
    fr(3, 3, cr(pro(20), 380), "Poduszka w zestawie", dark=True)
    fr(3, 4, cta(), *CTA, top=True, dark=True)
    # D4 czw – wybierz kolor (2 detale na klatkę)
    def split(a, b):
        im = Image.new("RGB", (SW, SH)); im.paste(cover(rd(pro(a)), SW, SH // 2), (0, 0)); im.paste(cover(rd(pro(b)), SW, SH // 2), (0, SH // 2)); return im
    fr(4, 1, split(18, 17), "Który wolisz?", "1 jasny brąz · 2 brąz", top=True)
    fr(4, 2, split(15, 16), "A teraz?", "3 ciemny brąz · 4 grafit", top=True)
    fr(4, 3, ph(pro(14)), "5 · czerń", "Wyniki w piątek")
    fr(4, 4, cta(), "Wszystkie 5 kolorów", "w zapowiedzi posta – poniedziałek", top=True, dark=True)
    # D5 pt – zadaj pytanie stolarzowi
    fr(5, 1, ph(g("wyciete-blaty"), 0.5, 0.4), "Zadaj pytanie stolarzowi", "O drewno, wymiary, pielęgnację", top=True)
    fr(5, 2, cta(), "Twoje pytanie?", "Wpisz w okienku", top=True, dark=True)
    fr(5, 3, cta(), "Odpowiem w reelsie", "w przyszłym tygodniu", top=True, dark=True)
    # D6 sob – taras o zmierzchu
    fr(6, 1, ph(g("taras-z-palenisko"), 0.5, 0.55), "Wieczór przy ogniu")
    fr(6, 2, ph(g("taras-z-palenisko"), 0.4, 0.65, 1.25), "Z kim byś tu usiadł?", None, top=True)
    fr(6, 3, cta(), *CTA, top=True, dark=True)
    # D7 ndz – zapowiedź tygodnia
    fr(7, 1, ph(g("wyciete-blaty"), 0.5, 0.4), "Nowy tydzień", "Zaglądaj codziennie", top=True)
    two = Image.new("RGB", (SW, SH)); two.paste(cover(rd(g("wyciete-blaty")), SW, SH // 2, 0.5, 0.4), (0, 0)); two.paste(cover(rd(g("image-20260904-110937-616")), SW, SH // 2, 0.5, 0.55), (0, SH // 2))
    fr(7, 2, two, "Warsztat czy realizacje?", "Co chcesz zobaczyć?", top=True)
    fr(7, 3, cta(), *CTA, top=True, dark=True)
if __name__ == "__main__":
    for a in (sys.argv[1:] or ["posty"]):
        if a == "posty": posty()
        if a == "reelsy": reelsy()
        if a == "siatka": siatka()
        if a == "okladki": okladki()
        if a == "stories": stories()
    print("OK")
