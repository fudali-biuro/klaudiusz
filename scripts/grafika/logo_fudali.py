#!/usr/bin/env python3
"""Nowe logo FUDALI – warianty wektorowe (Zosia, 23.11.2026). Tekst zamieniony na krzywe (SVG samodzielne, bez fontów).
Użycie: python3 scripts/grafika/logo_fudali.py   → marketing/logo/propozycja-2026-11/svg/*.svg + plansza.html
Fonty: Zilla Slab (Mozilla/Google Fonts, licencja OFL) w marketing/logo/propozycja-2026-11/fonty/."""
import os, math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
P = os.path.join(R, "marketing/logo/propozycja-2026-11")
FD = os.path.join(P, "fonty")
GREEN, GREEN2, OLIVE, PARCH = "#34442F", "#475638", "#737D4F", "#F7F5EF"
RUST, RUST_DARK = "#B4552A", "#DB8453"   # akcent: na parchment / na ciemnej zieleni
DESC = os.environ.get("FUDALI_OPIS", "STOLARSTWO I DREWNO OGRODOWE")

_fonts = {}
def font(name):
    if name not in _fonts: _fonts[name] = TTFont(os.path.join(FD, name))
    return _fonts[name]

def text_path(txt, fname, size, tracking=0.0):
    """→ (d, width, capheight_px): kontur tekstu, baseline y=0, rosnące y w dół."""
    f = font(fname); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    k = size / upm; x = 0.0; d = []
    for ch in txt:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))
        d.append(pen.getCommands()); x += f["hmtx"][g][0] * k + tracking
    return " ".join(d), x - tracking, f["OS/2"].sCapHeight * k

def leaf_shapes(s=1.0, fill="#000"):
    """Liść dębu: wrzecionowate ciało + zaokrąglone, ukośne klapy (4 pary, największe w 2/3 wysokości) + klapa na czubku. Środek x=0, wysokość ok. 92."""
    c = [f'<ellipse cx="0" cy="{50*s:.2f}" rx="{10*s:.2f}" ry="{40*s:.2f}"/>']
    lobes = [(13, 24, 12, 8.2, 52), (14, 40, 14, 8.8, 40), (15, 57, 14.5, 8.8, 30), (11, 72, 11, 7.6, 22)]   # (x, y, rx, ry, kąt)
    for x, y, rx, ry, ang in lobes:
        for sg in (1, -1):
            c.append(f'<ellipse cx="{sg*x*s:.2f}" cy="{y*s:.2f}" rx="{rx*s:.2f}" ry="{ry*s:.2f}" transform="rotate({-sg*ang} {sg*x*s:.2f} {y*s:.2f})"/>')
    c.append(f'<ellipse cx="0" cy="{10*s:.2f}" rx="{9*s:.2f}" ry="{11*s:.2f}"/>')
    return f'<g fill="{fill}">' + "".join(c) + '</g>'

def leaf_group(x, y, h, fill, hole, rot=0):
    """Liść o wysokości h z łodygą; żyłka jako maska (przezroczysta). x = środek, y = wierzchołek."""
    s = h / 112.0; uid = f"m{abs(hash((x, y, h, fill, rot))) % 10**8}"
    vein = f"M0 {16*s:.2f} L0 {84*s:.2f}"
    side = "".join(f"M0 {yy*s:.2f} L{xx*s:.2f} {(yy-9)*s:.2f} M0 {yy*s:.2f} L{-xx*s:.2f} {(yy-9)*s:.2f}" for yy, xx in [(34, 11), (52, 13), (68, 10)])
    return (f'<g transform="translate({x:.2f} {y:.2f}) rotate({rot})">'
            f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="{-50*s:.1f}" y="{-5*s:.1f}" width="{100*s:.1f}" height="{125*s:.1f}">'
            f'<rect x="{-50*s:.1f}" y="{-5*s:.1f}" width="{100*s:.1f}" height="{125*s:.1f}" fill="#fff"/>'
            f'<path d="{vein} {side}" stroke="#000" stroke-width="{3.4*s:.2f}" stroke-linecap="round" fill="none"/></mask>'
            f'<g mask="url(#{uid})">{leaf_shapes(s, fill)}</g>'
            f'<path d="M0 {88*s:.2f} L0 {98*s:.2f}" stroke="{fill}" stroke-width="{5.2*s:.2f}" stroke-linecap="round"/></g>')

def svg(w, h, body, bg=None):
    r = f'<rect width="{w:.1f}" height="{h:.1f}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" height="{h:.1f}">{r}{body}</svg>'

# ---------- kolory zależne od tła ----------
def pal(dark):
    return dict(ink=PARCH if dark else GREEN, sub=("#C9CDB5" if dark else OLIVE), acc=RUST_DARK if dark else RUST, bg=GREEN if dark else PARCH)

WM = "ZillaSlab-Bold.ttf"; DF = "ZillaSlab-Bold.ttf"

def wordmark(dark, size=100, tracking=6):
    p = pal(dark); d, w, cap = text_path("FUDALI", WM, size, tracking)
    return p, d, w, cap

def lockup(variant, dark, desc=True, size=100):
    """Zwraca (svg_body, w, h) – bez tła, z marginesem 0."""
    p, d, w, cap = wordmark(dark, size)
    body = ""; y = cap  # baseline FUDALI
    if variant == "C":
        inner, iw, ih = lockup("A", dark, desc=desc, size=size)
        side = ih; gap = side * 0.28
        fd, fw, fcap = text_path("F", WM, side * 0.78)
        sq = (f'<rect width="{side:.1f}" height="{side:.1f}" rx="{side*0.12:.1f}" fill="{p["ink"]}"/>'
              f'<g transform="translate({(side-fw)/2:.1f} {side*0.45+fcap/2:.1f})"><path d="{fd}" fill="{p["bg"]}"/></g>'
              f'<rect x="{side*0.31:.1f}" y="{side*0.80:.1f}" width="{side*0.38:.1f}" height="{side*0.05:.1f}" fill="{p["acc"]}"/>')
        return sq + f'<g transform="translate({side+gap:.1f} 0)">{inner}</g>', side + gap + iw, ih
    body += f'<path d="{d}" fill="{p["ink"]}" transform="translate(0 {y:.1f})"/>'
    ly = y + (cap * 0.42 if variant == "B" else cap * 0.17); lh = cap * 0.075
    if variant == "B":
        lh_leaf = cap * 0.62; gapw = lh_leaf * 0.60
        mid = w / 2
        body += f'<rect x="0" y="{ly:.1f}" width="{mid - gapw/2:.1f}" height="{lh:.1f}" fill="{p["acc"]}"/>'
        body += f'<rect x="{mid + gapw/2:.1f}" y="{ly:.1f}" width="{w - mid - gapw/2:.1f}" height="{lh:.1f}" fill="{p["acc"]}"/>'
        body += leaf_group(mid, ly + lh / 2 - lh_leaf * 0.66, lh_leaf, p["acc"], p["bg"], rot=0)
    else:
        body += f'<rect x="0" y="{ly:.1f}" width="{w:.1f}" height="{lh:.1f}" fill="{p["acc"]}"/>'
    H = ly + lh
    if desc:
        target = w; dsize = cap * 0.30
        dd, dw, dcap = text_path(DESC, DF, dsize, 0)
        extra = (cap * 0.50 if variant == "B" else 0)
        tr = (target - dw) / max(len(DESC) - 1, 1)   # rozciągnij kerning do szerokości napisu
        dd, dw, dcap = text_path(DESC, DF, dsize, tr)
        body += f'<path d="{dd}" fill="{p["sub"]}" transform="translate(0 {ly + lh + cap*0.14 + dcap:.1f})"/>'
        H = ly + lh + cap * 0.14 + dcap
    # margines na liść w B (wystaje ponad linię)
    top = 0
    return f'<g transform="translate(0 {-top:.1f})">{body}</g>', w, H - top

def compact(variant, dark):
    """Wersja ≤40 px wysokości: bez opisu."""
    return lockup(variant, dark, desc=False)

def mark(variant, dark, shape="circle", size=100):
    """Znak (awatar/favicon). A: F, B: liść, C: F w kwadracie (w kole = F)."""
    p = pal(dark); r = size / 2
    fill = p["ink"]; txt = p["bg"]
    clip = (f'<circle cx="{r}" cy="{r}" r="{r}" fill="{fill}"/>' if shape == "circle"
            else f'<rect width="{size}" height="{size}" rx="{size*0.14}" fill="{fill}"/>')
    if variant == "B":
        body = leaf_group(r, size * 0.16, size * 0.60, p["bg"], fill) + f'<rect x="{size*0.3}" y="{size*0.82}" width="{size*0.4}" height="{size*0.045}" fill="{p["acc"]}"/>'
    else:
        fd, fw, fcap = text_path("F", WM, size * 0.62)
        body = (f'<g transform="translate({(size - fw)/2:.2f} {size*0.5 + fcap*0.5 - size*0.03:.2f})"><path d="{fd}" fill="{txt}"/></g>'
                f'<rect x="{size*0.3}" y="{size*0.78}" width="{size*0.4}" height="{size*0.045}" fill="{p["acc"]}"/>')
    return clip + body

def save(name, s):
    os.makedirs(os.path.join(P, "svg"), exist_ok=True)
    open(os.path.join(P, "svg", name), "w").write(s)

def build_all():
    out = {}
    for v in "ABC":
        for dark in (False, True):
            tag = "ciemne" if dark else "jasne"; bg = pal(dark)["bg"]
            b, w, h = lockup(v, dark); pad = h * 0.18
            save(f"logo-{v}-{tag}.svg", svg(w + 2 * pad, h + 2 * pad, f'<g transform="translate({pad:.1f} {pad:.1f})">{b}</g>', bg))
            # wersja przezroczysta (do nakładania)
            save(f"logo-{v}-{tag}-przezroczyste.svg", svg(w + 2 * pad, h + 2 * pad, f'<g transform="translate({pad:.1f} {pad:.1f})">{b}</g>'))
            b2, w2, h2 = compact(v, dark)
            save(f"logo-{v}-{tag}-naglowek.svg", svg(w2, h2, b2))
            b3, w3, h3 = lockup(v, dark, desc=True)
            save(f"logo-{v}-{tag}-naglowek-z-opisem.svg", svg(w3, h3, b3))
            shape = "circle"
            save(f"znak-{v}-{tag}-awatar.svg", svg(100, 100, mark(v, dark, shape)))
    return True

if __name__ == "__main__":
    build_all(); print("OK")


def inline(name):
    return open(os.path.join(P, "svg", name)).read()

def plansza_html():
    cur = os.path.relpath(os.path.join(R, "marketing/logo/fudali-logo.png"), P)
    css = f"""body{{margin:0;background:#E9E6DC;font:15px/1.4 'DejaVu Sans',sans-serif;color:{GREEN}}}
.w{{width:2600px;padding:40px 48px;box-sizing:border-box}} h1{{font:700 34px 'Zilla Slab','DejaVu Serif',serif;margin:0 0 4px}}
.sub{{color:#5b6249;margin-bottom:22px}} .row{{display:flex;gap:18px;align-items:stretch;margin-bottom:18px}}
.lab{{width:170px;flex:none;padding-top:10px}} .lab b{{font:700 26px 'Zilla Slab','DejaVu Serif';display:block}} .lab span{{font-size:13px;color:#5b6249}}
.c{{border-radius:10px;display:flex;align-items:center;justify-content:center;gap:18px;padding:18px 16px;flex-wrap:nowrap;min-width:0}}
.l{{background:{PARCH}}} .d{{background:{GREEN}}} .c small{{display:block;font-size:11px;opacity:.65;margin-top:6px;text-align:center}}
.col{{display:flex;flex-direction:column;align-items:center}} img,svg{{display:block}} .sw{{display:flex;gap:12px;margin:6px 0 22px}} .sw div{{width:150px;height:62px;border-radius:8px;color:#fff;font:12px/1.3 sans-serif;padding:8px;box-sizing:border-box}}"""
    def full(v, t, h): 
        s = inline(f"logo-{v}-{t}.svg"); return s.replace("<svg ", f'<svg style="height:{h}px;width:auto" ', 1)
    def cell(v, dark):
        t = "ciemne" if dark else "jasne"; cls = "d" if dark else "l"
        hd = inline(f"logo-{v}-{t}-naglowek.svg").replace("<svg ", '<svg style="height:40px;width:auto" ', 1)
        hd2 = inline(f"logo-{v}-{t}-naglowek-z-opisem.svg").replace("<svg ", '<svg style="height:40px;width:auto" ', 1)
        fv = inline(f"znak-{v}-{t}-awatar.svg").replace("<svg ", '<svg style="height:32px;width:32px" ', 1)
        av = inline(f"znak-{v}-{t}-awatar.svg").replace("<svg ", '<svg style="height:96px;width:96px" ', 1)
        # na jasnym: awatar ciemny; na ciemnym: awatar jasny (w kolorze bg)
        return (f'<div class="c {cls}" style="flex:1;color:{PARCH if dark else GREEN}">'
                f'<div class="col">{full(v, t, {'A':112,'B':112,'C':74}[v])}<small>logo pełne</small></div>'
                f'<div class="col">{hd}<small>nagłówek 40 px (bez opisu)</small></div>'
                f'<div class="col">{hd2}<small>40 px Z opisem</small></div>'
                f'<div class="col">{fv}<small>32 px (favicon)</small></div>'
                f'<div class="col">{av}<small>awatar (koło)</small></div></div>')
    rows = ""
    names = {"A": ("A", "mocna płytka + rdzawa linia + opis"), "B": ("B", "A + prosty liść dębu w linii"), "C": ("C", "monogram F w kwadracie + napis")}
    for v in "ABC":
        rows += f'<div class="row"><div class="lab"><b>{names[v][0]}</b><span>{names[v][1]}</span></div>{cell(v, False)}{cell(v, True)}</div>'
    cur_html = (f'<div class="row"><div class="lab"><b>Obecne</b><span>fudali-logo.png</span></div>'
                f'<div class="c l" style="flex:1"><img src="{cur}" style="height:118px"></div>'
                f'<div class="c d" style="flex:1"><div style="background:#fff;padding:8px;border-radius:6px"><img src="{cur}" style="height:102px"></div></div></div>')
    sw = "".join(f'<div style="background:{c};color:{"#fff" if c not in (PARCH,) else GREEN}">{n}<br>{c}</div>' for n, c in
                 [("zieleń główna", GREEN), ("zieleń 2", GREEN2), ("oliwka", OLIVE), ("parchment", PARCH), ("rdzawy (jasne tło)", RUST), ("rdzawy (ciemne tło)", RUST_DARK)])
    return (f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="w"><h1>Nowe logo FUDALI – propozycja (23.11.2026)</h1>'
            f'<div class="sub">Krój: Zilla Slab Bold (płytka, zaokrąglone szeryfy) · opis: Zilla Slab Medium · opis: „{DESC}” (robocza wersja; do wyboru z propozycji Oli) · tylko podgląd, nic nie wdrożone</div>'
            f'<div class="sw">{sw}</div>{cur_html}{rows}</div></body></html>')

def build_plansza():
    open(os.path.join(P, "plansza.html"), "w").write(plansza_html())

if __name__ == "__main__":
    build_plansza()
