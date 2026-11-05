#!/usr/bin/env python3
"""Zosia: umieszcza prawdziwy produkt FUDALI w nowej scenerii (edycja zdjęcia – produkt zostaje ten sam).

Użycie:
  python3 scripts/grafika/scena.py --zdjecie <URL lub plik zdjęcia produktu> --opis "scena po angielsku" --wyjscie marketing/zdjecia/x/plik.jpg
  [--proporcje 4:5] [--bez-api]
Wynik: plik JPG (przycięty do proporcji) + obok <plik>.json (model, prompt, źródło).

Kolejność (pierwszy działający wygrywa):
  1. Antigravity CLI (agy, konto Google biuro@fudali.com.pl – bez opłat za obrazek; scripts/antigravity/README.md)
  2. zapas płatny: OpenRouter (OPENROUTER_API_KEY, modele Gemini Image) – wyłączany flagą --bez-api
fal.ai NIE jest używane do obrazów (decyzja Pablo 05.11.2026).
"""
import argparse, base64, io, json, os, pathlib, shutil, subprocess, sys, time, urllib.request, urllib.error

REPO = pathlib.Path(__file__).resolve().parents[2]
AGY_PRACA = pathlib.Path(os.environ.get("AGY_PRACA", pathlib.Path.home() / ".cache/fudali-agy"))
AGY_MOZG = pathlib.Path.home() / ".gemini/antigravity-cli/brain"
MODELE = ["antigravity", "openrouter:google/gemini-3-pro-image", "openrouter:google/gemini-nano-banana-2.1"]
UA = {"User-Agent": "Mozilla/5.0 (KlaudiuszFUDALI)"}
ZASADY = ("Keep the product EXACTLY as in the reference photo: same shape, proportions, wood grain, colour and details – "
          "do not redesign, add or remove parts. It must look like a real, unedited photo taken with a full-frame camera "
          "and a 50mm or 85mm lens: natural light, shallow depth of field, true-to-life colours, real wood texture with "
          "natural grain and tiny imperfections, realistic soft shadows, subtle natural film grain. Avoid any CGI / 3D-render "
          "look, plastic surfaces, oversaturation, HDR glow or perfect symmetry. No text, no logos, no watermarks. Scene: ")


def jpeg_referencji(url):
    from PIL import Image
    if os.path.exists(url):
        surowe = pathlib.Path(url).read_bytes()
    else:
        surowe = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    im = Image.open(io.BytesIO(surowe)).convert("RGB"); im.thumbnail((1600, 1600))
    b = io.BytesIO(); im.save(b, "JPEG", quality=90)
    return b.getvalue()


def antigravity(prompt, url, proporcje):
    start = subprocess.run([str(REPO / "scripts/antigravity/start.sh")], capture_output=True, text=True)
    if start.returncode:
        raise RuntimeError((start.stderr or start.stdout).strip())
    AGY_PRACA.mkdir(parents=True, exist_ok=True)
    nazwa = f"produkt-{int(time.time() * 1000)}.jpg"
    ref = AGY_PRACA / nazwa
    ref.write_bytes(jpeg_referencji(url))
    polecenie = (f"Generate exactly one image with your built-in image generation tool, using the photo {nazwa} in this "
                 f"folder as the reference image. {prompt} Aspect ratio {proporcje}. Do not run any commands and do not "
                 "copy or move files - just generate the image and reply with its file name.")
    agy = shutil.which("agy") or str(pathlib.Path.home() / ".local/bin/agy")
    try:
        w = subprocess.run([agy, "-p", polecenie, "--sandbox", "--mode", "accept-edits", "--output-format", "json"],
                           cwd=AGY_PRACA, capture_output=True, text=True, timeout=900)
    finally:
        ref.unlink(missing_ok=True)
    try:
        dane = json.loads(w.stdout)
    except json.JSONDecodeError:
        raise RuntimeError((w.stderr or w.stdout).strip()[-300:])
    obrazy = sorted((p for p in (AGY_MOZG / dane.get("conversation_id", "-")).glob("*")
                     if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")), key=lambda p: p.stat().st_mtime)
    if dane.get("status") != "SUCCESS" or not obrazy:
        raise RuntimeError(f"{dane.get('status')}: {(dane.get('response') or w.stderr).strip()[-300:]}")
    return obrazy[-1].read_bytes()


def openrouter(model, prompt, url, proporcje):
    data_url = "data:image/jpeg;base64," + base64.b64encode(jpeg_referencji(url)).decode()
    dane = {"model": model, "modalities": ["image", "text"], "image_config": {"aspect_ratio": proporcje},
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt},
                                                      {"type": "image_url", "image_url": {"url": data_url}}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(dane).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        w = json.loads(r.read())
    obraz = w["choices"][0]["message"]["images"][0]["image_url"]["url"]
    return base64.b64decode(obraz.split(",", 1)[1])


def przytnij(im, proporcje):
    """Środkowe przycięcie do proporcji „szer:wys” (agy nie zawsze trzyma format)."""
    sz, wy = (float(x) for x in proporcje.split(":"))
    w, h = im.size
    if w / h > sz / wy:
        nw = round(h * sz / wy); return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = round(w * wy / sz); return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zdjecie", required=True)
    ap.add_argument("--opis", required=True)
    ap.add_argument("--wyjscie", required=True)
    ap.add_argument("--proporcje", default="4:5")
    ap.add_argument("--bez-api", action="store_true", help="tylko Antigravity – bez płatnego zapasu OpenRouter")
    a = ap.parse_args()
    prompt = ZASADY + a.opis
    for model in MODELE:
        if model.startswith("openrouter:") and (a.bez_api or not os.environ.get("OPENROUTER_API_KEY")):
            continue
        try:
            obraz = antigravity(prompt, a.zdjecie, a.proporcje) if model == "antigravity" else \
                openrouter(model.split(":", 1)[1], prompt, a.zdjecie, a.proporcje)
            break
        except urllib.error.HTTPError as e:
            print(f"{model}: nie wyszło ({e.read().decode()[:300]})", file=sys.stderr)
        except (RuntimeError, KeyError, IndexError, OSError, subprocess.SubprocessError) as e:
            print(f"{model}: nie wyszło ({e})", file=sys.stderr)
    else:
        sys.exit("Żaden model nie zadziałał.")
    out = pathlib.Path(a.wyjscie); out.parent.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    im = przytnij(Image.open(io.BytesIO(obraz)).convert("RGB"), a.proporcje); im.thumbnail((1440, 1800))
    im.save(out, "JPEG", quality=88, optimize=True)
    out.with_suffix(".json").write_text(json.dumps({"model": model, "zrodlo": a.zdjecie, "prompt": prompt, "ai": True},
                                                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"OK {model} -> {out} {im.size}")


if __name__ == "__main__":
    main()
