#!/usr/bin/env python3
"""Analiza wideo nowych postów konkurencji – dwutorowo:

1. Klatki dla Claude: ffmpeg wycina klatki (domyślnie co 1 s, max 24) i składa z nich arkusz
   (monitoring/media/<id>/arkusz.jpg), który Claude ogląda narzędziem Read.
2. Gemini 4 przez OpenRouter (obraz + dźwięk, klatka po klatce): pełny rozbiór wideo z timestampami,
   transkrypcją, muzyką, napisami, hookiem i propozycją, jak FUDALI może zrobić podobne.

Wejście: monitoring/stan/nowe-posty.json (z monitoring_social.py)
Wyjście: monitoring/stan/wideo-analizy/<id>.json   (media w monitoring/media/ – nie trafiają do gita)
Wymaga: OPENROUTER_API_KEY (bez niego robi tylko klatki). Model: OPENROUTER_MODEL (domyślnie google/gemini-4-argon).
"""
import base64, json, os, re, subprocess, sys, urllib.request, urllib.error, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wspolne import ROOT, STAN, json_wczytaj, json_zapisz

MEDIA = ROOT / "monitoring" / "media"
WYNIKI = STAN / "wideo-analizy"
MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemini-4-argon")
MAX_MB = 18           # większe pliki kompresujemy przed wysłaniem (base64 ~ +33%)
MAX_KLATEK = 24
MAX_WIDEO = int(os.environ.get("MAX_WIDEO_NA_PRZEBIEG", "6"))

PROMPT = """Jesteś analitykiem marketingu wideo dla FUDALI Sp. z o.o. – rodzinnej stolarni z Podkarpacia
(fudali.com.pl): drewutnie, domki ogrodowe i nowoczesne domki, altany, pergole, meble ogrodowe
(m.in. składany leżak z jodły), drewno konstrukcyjne, akcesoria z drewna. Sprzedaż w całej Polsce i na Etsy.

Przeanalizuj to wideo konkurencji KLATKA PO KLATCE, łącznie z dźwiękiem. Opis posta: {opis}
Konto: @{konto} ({platforma}), polubienia: {polubienia}, komentarze: {komentarze}, wyświetlenia: {wyswietlenia}.

Odpowiedz WYŁĄCZNIE poprawnym JSON-em (po polsku) o polach:
{{
 "dlugosc_s": liczba,
 "hook_0_3s": "co dokładnie dzieje się w pierwszych 3 s i dlaczego zatrzymuje (albo nie)",
 "sceny": [{{"od_s": 0, "do_s": 2.5, "obraz": "co widać, ujęcie, ruch kamery", "tekst_na_ekranie": "", "dzwiek": "lektor/muzyka/efekt"}}],
 "transkrypcja": "dosłownie, co mówi lektor/osoba (pusty string, jeśli nic)",
 "muzyka": "charakter, tempo, czy trend/viral audio, czy zsynchronizowana z cięciami",
 "montaz": "tempo cięć, przejścia, format (pionowy?), napisy",
 "produkt_i_oferta": "jaki produkt, czy cena/promocja, jak pokazany",
 "cta": "wezwanie do działania (jeśli jest)",
 "dlaczego_dziala": ["..."],
 "slabe_strony": ["..."],
 "ocena_potencjalu_1_10": liczba,
 "czy_fudali_moze_zrobic_podobne": "tak/nie/czesciowo + krótko dlaczego",
 "pomysl_dla_fudali": {{"tytul": "", "produkt_fudali": "", "hook": "", "scenariusz": ["ujęcie 1 ...", "ujęcie 2 ..."], "audio": "", "tekst_na_ekranie": "", "cta": "", "potrzebny_sprzet_i_czas": ""}},
 "slowa_kluczowe_i_hashtagi": ["..."]
}}"""

def pobierz(url, cel):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(cel, "wb") as f:
        f.write(r.read())

def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)

def dlugosc(plik):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(plik)],
                         capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0

def klatki(plik, katalog):
    """Klatki co ~1 s (max MAX_KLATEK) + arkusz kontaktowy z timestampami do obejrzenia przez Claude."""
    kl = katalog / "klatki"
    kl.mkdir(parents=True, exist_ok=True)
    d = dlugosc(plik) or 1
    fps = min(1.0, MAX_KLATEK / d)
    ffmpeg("-i", str(plik), "-vf", f"fps={fps:.4f},scale=360:-2", "-q:v", "4", str(kl / "k%03d.jpg"))
    n = len(list(kl.glob("k*.jpg")))
    kolumny = 6
    wiersze = max(1, -(-n // kolumny))
    ffmpeg("-i", str(plik), "-vf",
           f"fps={fps:.4f},scale=240:-2,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,"
           f"tile={kolumny}x{wiersze}", "-frames:v", "1", "-q:v", "4", str(katalog / "arkusz.jpg"))
    return {"liczba_klatek": n, "co_ile_s": round(1 / fps, 2), "dlugosc_s": round(d, 1),
            "arkusz": str((katalog / "arkusz.jpg").relative_to(ROOT)), "klatki": str(kl.relative_to(ROOT))}

def gemini(plik, post):
    klucz = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not klucz:
        return {"status": "brak_klucza_openrouter"}
    wyslij = plik
    if plik.stat().st_size > MAX_MB * 1024 * 1024:
        wyslij = plik.with_name("maly.mp4")
        ffmpeg("-i", str(plik), "-vf", "scale=-2:540", "-c:v", "libx264", "-crf", "30", "-preset", "veryfast",
               "-c:a", "aac", "-b:a", "64k", str(wyslij))
    b64 = base64.b64encode(wyslij.read_bytes()).decode()
    tresc = PROMPT.format(**{k: post.get(k, "") or "" for k in
                             ("opis", "konto", "platforma", "polubienia", "komentarze", "wyswietlenia")})
    body = {"model": MODEL, "temperature": 0.3, "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": tresc},
                {"type": "video_url", "video_url": {"url": f"data:video/mp4;base64,{b64}"}}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {klucz}", "Content-Type": "application/json",
                                          "HTTP-Referer": "https://github.com/fudali-biuro/klaudiusz",
                                          "X-Title": "Klaudiusz FUDALI"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            odp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"status": "blad", "blad": f"HTTP {e.code}: {e.read().decode(errors='ignore')[:500]}"}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"status": "blad", "blad": str(e)}
    tekst = odp.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
    m = re.search(r"\{.*\}", tekst, re.S)
    try:
        analiza = json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        analiza = None
    return {"status": "ok" if analiza else "niepoprawny_json", "model": odp.get("model", MODEL),
            "analiza": analiza, "surowa_odpowiedz": None if analiza else tekst[:4000], "koszt": odp.get("usage")}

def main():
    nowe = json_wczytaj(STAN / "nowe-posty.json", {}).get("nowe", [])
    wideo = [p for p in nowe if p.get("wideo_url")][:MAX_WIDEO]
    if not wideo:
        print("Brak nowych wideo do analizy.")
        return
    for post in wideo:
        bezp = re.sub(r"[^a-zA-Z0-9_-]", "_", post["id"])
        cel = WYNIKI / f"{bezp}.json"
        if cel.exists():
            continue
        kat = MEDIA / bezp
        kat.mkdir(parents=True, exist_ok=True)
        plik = kat / "wideo.mp4"
        wynik = {"id": post["id"], "url": post.get("url"), "firma": post.get("firma"), "konto": post.get("konto"),
                 "platforma": post.get("platforma")}
        try:
            pobierz(post["wideo_url"], plik)
            wynik["klatki_claude"] = klatki(plik, kat)
            wynik["gemini"] = gemini(plik, post)
        except Exception as e:  # jeden zły plik nie blokuje reszty
            wynik["blad"] = f"{type(e).__name__}: {e}"
        json_zapisz(cel, wynik)
        print(f"{post['id']}: klatki={'ok' if 'klatki_claude' in wynik else 'brak'}, "
              f"gemini={wynik.get('gemini', {}).get('status', wynik.get('blad'))}")

if __name__ == "__main__":
    main()
