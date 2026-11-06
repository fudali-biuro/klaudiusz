#!/usr/bin/env python3
"""Krótkie realistyczne filmy AI (Gemini Omni przez OpenRouter, endpoint /api/v1/videos) z prawdziwego zdjęcia produktu.

  python3 scripts/grafika/wideo.py --zdjecie <plik.jpg> [--zdjecie …] --opis "<scena EN>" --wyjscie <plik.mp4> [--format 9:16] [--sekundy 8]

Zasady (zespol/lekcje-pablo.md): realistycznie, prawdziwy produkt 1:1 ze zdjęcia, bez napisów i logo w kadrze.
Nie kopiujemy cudzych filmów – cudzy film to tylko inspiracja opisana słowami (scena, ruch kamery, światło).
Koszt: płatne z konta OpenRouter – generuj z głową (1 próba → ocena → ewentualnie poprawka).
"""
import argparse, base64, json, mimetypes, os, pathlib, sys, time, urllib.request, urllib.error

API = "https://openrouter.ai/api/v1/videos"
MODEL = "google/gemini-omni-1.1-flash"  # 1.2 zwraca „failed” (06.11.2026); koszt ok. 1 USD za klip


def zapytanie(url, dane=None, metoda=None):
    req = urllib.request.Request(url, data=json.dumps(dane).encode() if dane is not None else None, method=metoda,
                                 headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
                                          "Content-Type": "application/json", "X-Title": "Klaudiusz FUDALI - wideo"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"Błąd {e.code}: {e.read()[:800].decode(errors='replace')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zdjecie", action="append", required=True)
    ap.add_argument("--opis", required=True)
    ap.add_argument("--wyjscie", required=True)
    ap.add_argument("--format", default="9:16")
    ap.add_argument("--sekundy", type=int, default=8)
    ap.add_argument("--model", default=MODEL)
    a = ap.parse_args()
    if not os.environ.get("OPENROUTER_API_KEY"):
        sys.exit("Brak OPENROUTER_API_KEY")
    refs = []
    for z in a.zdjecie:
        typ = mimetypes.guess_type(z)[0] or "image/jpeg"
        refs.append({"type": "image_url", "image_url": {"url": f"data:{typ};base64," + base64.b64encode(pathlib.Path(z).read_bytes()).decode()}})
    zad = zapytanie(API, {"model": a.model, "prompt": a.opis, "input_references": refs, "aspect_ratio": a.format, **({"duration": a.sekundy} if a.sekundy else {})})
    print(json.dumps({k: v for k, v in zad.items() if k not in ("output", "data")}, ensure_ascii=False)[:600])
    vid = zad.get("id")
    wynik = zad
    for _ in range(120):
        if wynik.get("status") in ("completed", "succeeded", "failed", "error") or wynik.get("url") or wynik.get("output"):
            break
        time.sleep(10)
        wynik = zapytanie(f"{API}/{vid}")
        print("…", wynik.get("status"), flush=True)
    pathlib.Path(a.wyjscie).with_suffix(".json").write_text(json.dumps({k: v for k, v in wynik.items() if k != "data"}, ensure_ascii=False, indent=1)[:20000])
    url = wynik.get("url") or (wynik.get("output") or [{}])[0].get("url") if isinstance(wynik.get("output"), list) else wynik.get("url")
    url = url or (wynik.get("unsigned_urls") or [None])[0]
    for k in ("video_url", "download_url"):
        url = url or wynik.get(k)
    if not url:
        sys.exit("Brak linku do filmu – zobacz " + str(pathlib.Path(a.wyjscie).with_suffix(".json")))
    if url.startswith("data:"):
        pathlib.Path(a.wyjscie).write_bytes(base64.b64decode(url.split(",", 1)[1]))
    else:
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
        with urllib.request.urlopen(req, timeout=300) as r:
            pathlib.Path(a.wyjscie).write_bytes(r.read())
    print("✔ zapisano", a.wyjscie)


if __name__ == "__main__":
    main()
