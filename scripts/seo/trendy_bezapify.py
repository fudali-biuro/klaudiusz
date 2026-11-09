#!/usr/bin/env python3
"""Bartek: Google Trends BEZ Apify (biblioteka pytrends, za darmo) – zapas, gdy limit Apify jest wyczerpany.
Czyta seo/trendy-grupy.json, zapisuje seo/trendy/RRRR-MM-DD.md w tym samym układzie co trendy.py.
Wymaga: pip install pytrends. Google bywa wolny (429) – skrypt czeka między grupami."""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from wspolne import ROOT, teraz  # noqa: E402
from pytrends.request import TrendReq

def sredn(xs): return round(sum(xs) / len(xs), 1) if xs else 0

def main():
    grupy = json.loads((ROOT / "seo" / "trendy-grupy.json").read_text(encoding="utf-8"))["grupy"]
    dzis = teraz().strftime("%Y-%m-%d")
    md = [f"# Google Trends – {dzis} (Bartek)", "",
          "Skala 0–100 **wewnątrz grupy** (100 = najwyższe zainteresowanie którejkolwiek frazy w grupie w ciągu 12 mies.). "
          "Dane tygodniowe, ostatnie 12 miesięcy. Źródło: Google Trends (bezpośrednio, pytrends).", ""]
    for g in grupy:
        md += [f"## {g['nazwa']} ({g['geo'] or 'świat'})", ""]
        d = None
        for proba in range(4):
            try:
                p = TrendReq(hl="pl-PL", tz=-60, timeout=(10, 30))
                p.build_payload(g["frazy"], geo=g["geo"], timeframe="today 12-m")
                d = p.interest_over_time()
                rel = p.related_queries()
                break
            except Exception as e:
                print("retry", g["nazwa"], str(e)[:80]); time.sleep(20 * (proba + 1))
        if d is None or d.empty:
            md += ["_Brak danych w tym przebiegu._", ""]; continue
        d = d.drop(columns="isPartial", errors="ignore")
        md += ["| Fraza | Średnio 12 mies. | Ostatnie 4 tyg. | Poprzednie 4 tyg. | Zmiana | Szczyt (tydzień) | Teraz vs szczyt |", "|---|---|---|---|---|---|---|"]
        wier = []
        for f in g["frazy"]:
            s = list(d[f]); ost, pop = s[-4:], s[-8:-4]
            i = max(range(len(s)), key=lambda k: s[k])
            zm = "—" if not sredn(pop) else f"{round((sredn(ost) - sredn(pop)) / sredn(pop) * 100):+d}%"
            wier.append((sredn(s), f"| {f} | {sredn(s)} | {sredn(ost)} | {sredn(pop)} | {zm} | {d.index[i].strftime('%d.%m.%Y')} ({s[i]}) | {round(sredn(ost) / s[i] * 100) if s[i] else 0}% |"))
        md += [w for _, w in sorted(wier, key=lambda x: -x[0])]
        try:
            top = rel[g["frazy"][0]]["top"]; ris = rel[g["frazy"][0]]["rising"]
            if top is not None: md += ["", "**Powiązane (top, fraza 1):** " + ", ".join(top["query"].head(8))]
            if ris is not None: md += ["", "**Rosnące:** " + ", ".join(ris["query"].head(8))]
        except Exception: pass
        md.append(""); time.sleep(8)
    md += ["## Wnioski i rekomendacje", "", "_(uzupełnia Bartek)_", ""]
    out = ROOT / "seo" / "trendy" / f"{dzis}.md"; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md), encoding="utf-8"); print("Zapisano", out.relative_to(ROOT))

if __name__ == "__main__": main()
