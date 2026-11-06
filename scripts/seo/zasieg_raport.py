#!/usr/bin/env python3
"""Kuba: tabela rankingowa zasięgu fraz = Google Trends (na skali kotwicy) + podpowiedzi Google + konkurencja.
Czyta monitoring/stan/zasieg.json, slowa-metryki.json, trendy-swieta.json; pisze slowa-kluczowe/zasieg/RRRR-MM-DD.md."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from wspolne import ROOT, teraz  # noqa: E402

st = ROOT / "monitoring" / "stan"
z = json.loads((st / "zasieg.json").read_text(encoding="utf-8"))
m = {f["fraza"]: f for f in json.loads((st / "slowa-metryki.json").read_text(encoding="utf-8"))["frazy"]}
kot = z["kotwica"]
# Frazy świąteczne od Bartka (inne grupy) – przeliczamy przez frazę wspólną ("pomysł na prezent" albo "prezent dla taty")
sw = json.loads((st / "trendy-swieta.json").read_text(encoding="utf-8"))
mostek = {}
for g in sw["grupy"]:
    w = {r["fraza"]: r for r in g.get("wiersze", [])}
    for b in ("pomysł na prezent", "prezent dla taty"):
        if b in w and b in z["frazy"] and w[b]["srednia_12m"]:
            mostek = {"fraza": b, "wsp": z["frazy"][b]["zasieg_12m"] / w[b]["srednia_12m"],
                      "wsp_teraz": (z["frazy"][b]["zasieg_teraz"] / w[b]["ost_4tyg"]) if w[b]["ost_4tyg"] else None}
            break
    if mostek:
        break
dod = {}
if mostek:
    for g in sw["grupy"]:
        if not any(r["fraza"] == mostek["fraza"] for r in g.get("wiersze", [])):
            continue
        for r in g["wiersze"]:
            if r["fraza"] not in z["frazy"]:
                dod[r["fraza"]] = {"zasieg_12m": round(r["srednia_12m"] * mostek["wsp"], 1),
                                   "zasieg_teraz": round(r["ost_4tyg"] * (mostek["wsp_teraz"] or 0), 1),
                                   "zmiana_proc": r["zmiana_proc"], "szczyt": r["szczyt_tydzien"],
                                   "teraz_vs_szczyt_proc": r["teraz_vs_szczyt_proc"], "zrodlo": "Bartek, przez „" + mostek["fraza"] + "”"}
wszystkie = {**dod, **z["frazy"]}
wiersze = []
for f, v in wszystkie.items():
    mm = m.get(f, {})
    wiersze.append((f, v["zasieg_12m"], v["zasieg_teraz"], v.get("zmiana_proc"), v.get("szczyt", ""), v.get("teraz_vs_szczyt_proc"),
                    mm.get("ocena"), mm.get("liczba_podpowiedzi"), mm.get("wzmianki_konkurencji_7d", 0)))
wiersze.sort(key=lambda r: -r[2])
md = [f"# Porównanie zasięgu fraz – {teraz().strftime('%Y-%m-%d')} (Kuba)", "",
      f"**Zasięg = zainteresowanie w Google (Trends, Polska), przeliczone na jedną skalę: „{kot}” = 100.** "
      "Fraza z wartością 200 jest wyszukiwana ok. 2× częściej niż drewutnia; 10 = 10× rzadziej. "
      "To liczby względne (Google nie podaje bezwzględnej liczby wyszukań bez płatnego Planera Słów Kluczowych).", "",
      "- **Teraz** = średnia z ostatnich 4 tygodni · **12 mies.** = średnia z roku · **vs szczyt** = jak blisko rocznego szczytu jesteśmy dziś",
      "- Ocena/podpowiedzi = mój wskaźnik z podpowiedzi Google (kiedy ocena jest wysoka, a zasięg ~0, fraza jest „ładna”, ale nikt jej nie wpisuje)", "",
      "| # | Fraza | Zasięg teraz | Zasięg 12 mies. | Zmiana 4 tyg. | Szczyt roku | Teraz vs szczyt | Ocena (podpowiedzi) | Wzm. konkurencji 7 d |",
      "|---|---|---|---|---|---|---|---|---|"]
for i, r in enumerate(wiersze, 1):
    zm = "—" if r[3] is None else f"{r[3]:+d}%"
    md.append(f"| {i} | {r[0]} | **{r[2]}** | {r[1]} | {zm} | {r[4]} | {r[5]}% | {r[6] if r[6] is not None else '—'} ({r[7] if r[7] is not None else '—'}/10) | {r[8]} |")
md += ["", "_Źródła: Google Trends przez Apify (paczki z kotwicą `slowa-kluczowe/zasieg/paczki.json`), frazy świąteczne z `seo/swieta-2026.md` (Bartek) przeliczone przez wspólną frazę, podpowiedzi Google, monitoring konkurencji (Mietek)._"]
out = ROOT / "slowa-kluczowe" / "zasieg" / f"{teraz().strftime('%Y-%m-%d')}.md"
out.write_text("\n".join(md) + "\n", encoding="utf-8")
print("zapisano", out.relative_to(ROOT))
print("\n".join(md[8:8 + len(wiersze) + 1]))
