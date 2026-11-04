#!/usr/bin/env python3
"""Zosia: umieszcza prawdziwy produkt FUDALI w nowej scenerii (edycja zdjęcia – produkt zostaje ten sam).

Użycie:
  python3 scripts/grafika/scena.py --zdjecie <URL zdjęcia produktu> --opis "scena po angielsku" --wyjscie marketing/zdjecia/x/plik.jpg
Wynik: plik JPG + obok <plik>.json (model, prompt, źródło).
Najpierw OpenRouter (OPENROUTER_API_KEY, modele Gemini Image), potem fal.ai (FAL_AI_API_KEY) – pierwszy działający wygrywa.
"""
import argparse, base64, io, json, os, pathlib, sys, urllib.request, urllib.error

MODELE = ["openrouter:google/gemini-3-pro-image", "openrouter:google/gemini-nano-banana-2.1",
          "fal-ai/nano-banana/edit", "fal-ai/flux-pro/kontext"]
UA = {"User-Agent": "Mozilla/5.0 (KlaudiuszFUDALI)"}
ZASADY = ("Keep the product EXACTLY as in the reference photo: same shape, proportions, wood grain, colour and details – "
          "do not redesign, add or remove parts. Photorealistic lifestyle product photography, natural light, "
          "shallow depth of field, no text, no logos, no watermarks. Scene: ")


def jako_data_url(url):
    from PIL import Image
    if os.path.exists(url):
        surowe = pathlib.Path(url).read_bytes()
    else:
        surowe = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    im = Image.open(io.BytesIO(surowe)).convert("RGB"); im.thumbnail((1600, 1600))
    b = io.BytesIO(); im.save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def openrouter(model, prompt, url, proporcje):
    dane = {"model": model, "modalities": ["image", "text"], "image_config": {"aspect_ratio": proporcje},
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt},
                                                      {"type": "image_url", "image_url": {"url": jako_data_url(url)}}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(dane).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        w = json.loads(r.read())
    obraz = w["choices"][0]["message"]["images"][0]["image_url"]["url"]
    return base64.b64decode(obraz.split(",", 1)[1])


def wywolaj(model, prompt, url, proporcje):
    if model.startswith("openrouter:"):
        return openrouter(model.split(":", 1)[1], prompt, url, proporcje)
    if "nano-banana" in model:
        dane = {"prompt": prompt, "image_urls": [url], "num_images": 1, "output_format": "jpeg", "aspect_ratio": proporcje}
    else:
        dane = {"prompt": prompt, "image_url": url, "num_images": 1, "output_format": "jpeg", "aspect_ratio": proporcje}
    req = urllib.request.Request(f"https://fal.run/{model}", data=json.dumps(dane).encode(),
                                 headers={"Authorization": f"Key {os.environ['FAL_AI_API_KEY']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return urllib.request.urlopen(json.loads(r.read())["images"][0]["url"], timeout=120).read()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zdjecie", required=True)
    ap.add_argument("--opis", required=True)
    ap.add_argument("--wyjscie", required=True)
    ap.add_argument("--proporcje", default="4:5")
    a = ap.parse_args()
    prompt = ZASADY + a.opis
    for model in MODELE:
        klucz = "OPENROUTER_API_KEY" if model.startswith("openrouter:") else "FAL_AI_API_KEY"
        if not os.environ.get(klucz):
            continue
        try:
            obraz = wywolaj(model, prompt, a.zdjecie, a.proporcje)
            break
        except (urllib.error.HTTPError, KeyError, IndexError) as e:
            tresc = e.read().decode()[:300] if isinstance(e, urllib.error.HTTPError) else str(e)
            print(f"{model}: nie wyszło ({tresc})", file=sys.stderr)
    else:
        sys.exit("Żaden model nie zadziałał.")
    out = pathlib.Path(a.wyjscie); out.parent.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    im = Image.open(io.BytesIO(obraz)).convert("RGB"); im.thumbnail((1440, 1800))
    im.save(out, "JPEG", quality=88, optimize=True)
    out.with_suffix(".json").write_text(json.dumps({"model": model, "zrodlo": a.zdjecie, "prompt": prompt, "ai": True},
                                                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"OK {model} -> {out} {im.size}")


if __name__ == "__main__":
    main()
