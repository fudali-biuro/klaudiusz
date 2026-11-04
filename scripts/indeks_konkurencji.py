#!/usr/bin/env python3
"""Generuje konkurencja/konkurenci.md (tabela-indeks) z plików konkurencja/firmy/*.md."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wspolne import ROOT, wczytaj_konkurentow

def main():
    rows = sorted(wczytaj_konkurentow(), key=lambda k: (k.get("priorytet", "Z"), k["slug"]))
    out = ["# Obserwowani konkurenci (indeks)", "",
           "Plik generowany automatycznie z `konkurencja/firmy/*.md` – **edytuj pliki firm, nie ten plik.**",
           "Priorytet: A = bezpośredni, B = częściowy, C = rynek/ceny referencyjne.", "",
           "| Firma | Strona | Instagram | TikTok | Priorytet | Monitoring | Plik |",
           "|---|---|---|---|---|---|---|"]
    for k in rows:
        ig = f"[@{k['instagram']}](https://www.instagram.com/{k['instagram']}/)" if k.get("instagram") else "—"
        tt = f"[@{k['tiktok']}](https://www.tiktok.com/@{k['tiktok']})" if k.get("tiktok") else "—"
        out.append(f"| {k.get('nazwa', k['slug'])} | {k.get('www') or '—'} | {ig} | {tt} | "
                   f"{k.get('priorytet', '')} | {k.get('aktywny_monitoring', '')} | [firmy/{k['slug']}.md](firmy/{k['slug']}.md) |")
    out += ["", "## Nowo wykryci", "Nowych konkurentów dodawaj jako nowe pliki w `firmy/` (szablon: dowolny istniejący plik).", ""]
    (ROOT / "konkurencja" / "konkurenci.md").write_text("\n".join(out), encoding="utf-8")
    print(f"Zapisano indeks: {len(rows)} firm")

if __name__ == "__main__":
    main()
