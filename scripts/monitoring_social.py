#!/usr/bin/env python3
"""Godzinny scraper Instagram + TikTok konkurencji przez API Apify.

- Konta bierze z konkurencja/firmy/*.md (pola instagram / tiktok, aktywny_monitoring != nie).
- Wymaga zmiennej APIFY_API_KEY (lub APIFY_TOKEN) (https://console.apify.com/settings/integrations).
- Wynik: monitoring/stan/nowe-posty.json (posty, których wcześniej nie widzieliśmy),
         monitoring/stan/posty-30dni.json (baza do analizy słów kluczowych),
         monitoring/stan/widziane.json (ID już przeanalizowanych postów).
Bez tokenu kończy się kodem 0 i zapisuje status "brak_tokenu".
"""
import json, os, sys, urllib.request, urllib.error, datetime as dt, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wspolne import STAN, teraz, wczytaj_konkurentow, json_wczytaj, json_zapisz

LIMIT = int(os.environ.get("SOCIAL_LIMIT_POSTOW", "6"))  # postów na konto na przebieg
AKTOR_IG = os.environ.get("APIFY_AKTOR_IG", "apify~instagram-scraper")
AKTOR_TT = os.environ.get("APIFY_AKTOR_TT", "clockworks~tiktok-scraper")

def apify(aktor, wejscie, token):
    url = f"https://api.apify.com/v2/acts/{aktor}/run-sync-get-dataset-items?timeout=280"
    req = urllib.request.Request(url, data=json.dumps(wejscie).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())

def norm_ig(p, mapa):
    konto = (p.get("ownerUsername") or "").lower()
    return {"id": f"ig:{p.get('id') or p.get('shortCode')}", "platforma": "instagram",
            "konto": konto, "firma": mapa.get(("instagram", konto)),
            "url": p.get("url"), "data": p.get("timestamp"), "typ": p.get("type"),
            "opis": (p.get("caption") or "")[:1500], "hashtagi": p.get("hashtags") or [],
            "polubienia": p.get("likesCount"), "komentarze": p.get("commentsCount"),
            "wyswietlenia": p.get("videoViewCount") or p.get("videoPlayCount"),
            "miniatura": p.get("displayUrl"), "wideo_url": p.get("videoUrl")}

def norm_tt(p, mapa):
    konto = ((p.get("authorMeta") or {}).get("name") or "").lower()
    return {"id": f"tt:{p.get('id')}", "platforma": "tiktok", "konto": konto,
            "firma": mapa.get(("tiktok", konto)), "url": p.get("webVideoUrl"),
            "data": p.get("createTimeISO"), "typ": "video", "opis": (p.get("text") or "")[:1500],
            "hashtagi": [h.get("name") for h in (p.get("hashtags") or []) if h.get("name")],
            "polubienia": p.get("diggCount"), "komentarze": p.get("commentCount"),
            "wyswietlenia": p.get("playCount"), "udostepnienia": p.get("shareCount"),
            "miniatura": (p.get("videoMeta") or {}).get("coverUrl"),
            "wideo_url": (p.get("mediaUrls") or [None])[0] or (p.get("videoMeta") or {}).get("downloadAddr")}

def main():
    start = teraz()
    token = (os.environ.get("APIFY_API_KEY") or os.environ.get("APIFY_TOKEN") or "").strip()
    firmy = [k for k in wczytaj_konkurentow() if k.get("aktywny_monitoring", "tak").lower() != "nie"]
    mapa, ig, tt = {}, [], []
    for k in firmy:
        if k.get("instagram"):
            ig.append(k["instagram"]); mapa[("instagram", k["instagram"].lower())] = k["slug"]
        if k.get("tiktok"):
            tt.append(k["tiktok"]); mapa[("tiktok", k["tiktok"].lower())] = k["slug"]
    raport = {"czas": start.isoformat(timespec="minutes"), "status": "ok", "bledy": [],
              "konta_ig": ig, "konta_tiktok": tt, "nowe": []}
    if not token:
        raport["status"] = "brak_tokenu"
        json_zapisz(STAN / "nowe-posty.json", raport)
        print("APIFY_API_KEY nie ustawiony – pomijam scraping (status: brak_tokenu).")
        return
    posty = []
    if ig:
        try:
            dane = apify(AKTOR_IG, {"directUrls": [f"https://www.instagram.com/{h}/" for h in ig],
                                    "resultsType": "posts", "resultsLimit": LIMIT, "addParentData": False}, token)
            posty += [norm_ig(p, mapa) for p in dane if not p.get("error")]
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            raport["bledy"].append(f"instagram: {e}")
    if tt:
        try:
            dane = apify(AKTOR_TT, {"profiles": tt, "resultsPerPage": LIMIT,
                                    "shouldDownloadVideos": True, "shouldDownloadCovers": False}, token)
            posty += [norm_tt(p, mapa) for p in dane if not p.get("error")]
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            raport["bledy"].append(f"tiktok: {e}")

    widziane = set(json_wczytaj(STAN / "widziane.json", []))
    pierwszy_raz = not widziane
    nowe = [p for p in posty if p["id"] not in widziane]
    raport["nowe"] = [] if pierwszy_raz else nowe
    if pierwszy_raz:
        raport["status"] = "pierwsze_uruchomienie"  # tylko zapamiętujemy stan, nie zalewamy analizą
        raport["zapamietano"] = len(nowe)
    if raport["bledy"] and not posty:
        raport["status"] = "blad"
    widziane |= {p["id"] for p in posty}
    json_zapisz(STAN / "widziane.json", sorted(widziane)[-5000:])

    # baza 30 dni do analizy słów kluczowych (aktualizuje też liczniki starych postów)
    baza = {p["id"]: p for p in json_wczytaj(STAN / "posty-30dni.json", [])}
    for p in posty:
        p = {k: v for k, v in p.items() if k not in ("miniatura", "wideo_url")}  # linki CDN wygasają
        p["pobrano"] = start.isoformat(timespec="minutes")
        baza[p["id"]] = {**baza.get(p["id"], {}), **p}
    granica = (start - dt.timedelta(days=30)).isoformat()
    baza = [p for p in baza.values() if (p.get("data") or p.get("pobrano") or "") >= granica[:10]]
    json_zapisz(STAN / "posty-30dni.json", sorted(baza, key=lambda p: p.get("data") or "", reverse=True))
    json_zapisz(STAN / "nowe-posty.json", raport)
    print(f"Status: {raport['status']}, pobrano {len(posty)} postów, nowych: {len(raport['nowe'])}, błędy: {raport['bledy']}")

if __name__ == "__main__":
    main()
