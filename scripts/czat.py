#!/usr/bin/env python3
"""Czat w biurze: rozmowy Pablo ↔ pracownicy (okno czatu na https://biuro-fudali.vercel.app).

Każda wiadomość to osobny plik zespol/czat/<id>/<RRRRMMDD-HHMMSS>-<msg>.json (bez konfliktów przy zapisie).
Biuro pokazuje je w oknie czatu kilkanaście sekund po zapisie w archiwum.

Pracownik pisze do Pablo (domyślnie od razu zapisuje w archiwum, żeby było widać w biurze):
  python3 scripts/czat.py napisz <id> "tekst"                    # zwykła odpowiedź
  python3 scripts/czat.py napisz <id> - <<'KONIEC'               # dłuższy tekst (markdown) ze stdin
  python3 scripts/czat.py napisz <id> "…" --plik marketing/posty/x.md --plik marketing/zdjecia/a.jpg
  python3 scripts/czat.py napisz <id> "…" --typ prosba            # potrzebuję czegoś od Pablo (+ Telegram)
  python3 scripts/czat.py napisz <id> "…" --typ koniec            # skończyłem zadanie (melduję wynik)
Przyjęcie wiadomości z biura (robi ADRESAT, gdy listonosz czatu przyniesie mu wiadomość – JSON jest w tej wiadomości):
  python3 scripts/czat.py przyjmij <<'KONIEC_JSON'
  {"id": "m_…", "do": "marketing", "tekst": "…", "zalaczniki": [...]}
  KONIEC_JSON
Skrzynka (po obudzeniu przez zadanie „📥 Skrzynka”): wiadomości od Pablo, na które jeszcze nie odpowiedziałeś:
  python3 scripts/czat.py skrzynka <id>
Historia rozmowy (kontekst przed odpowiedzią):
  python3 scripts/czat.py pokaz <id> [-n 15]
Opcja --bez-zapisu: nie wysyłaj od razu do archiwum (np. gdy i tak zaraz zapisujesz większą zmianę).
"""
import argparse, base64, json, mimetypes, os, re, secrets, subprocess, sys, urllib.request, urllib.error, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wspolne import ROOT, teraz

CZAT = ROOT / "zespol" / "czat"
ZALACZNIKI = CZAT / "zalaczniki"
SESJE = ROOT / "zespol" / "sesje.json"
BIURO = "https://biuro-fudali.vercel.app"
TYPY = ("odpowiedz", "prosba", "koniec", "info")
MAX_ZALACZNIK = 25 * 1024 * 1024
MODEL_AUDIO = os.environ.get("OPENROUTER_MODEL_AUDIO", os.environ.get("OPENROUTER_MODEL", "google/gemini-4-argon"))


# ---------------------------------------------------------------- pomocnicze
def znane_id():
    """Identyfikatory pracowników = karty zespol/<id>.md z nagłówkiem „id:” (inne pliki .md to dokumentacja)."""
    wynik = []
    for p in (ROOT / "zespol").glob("*.md"):
        tekst = p.read_text(encoding="utf-8")
        if tekst.startswith("---") and re.search(rf"^id:\s*{re.escape(p.stem)}\s*$", tekst.split("---", 2)[1], re.M):
            wynik.append(p.stem)
    return sorted(wynik)


def karta(pid):
    """Nagłówek karty pracownika (imię, przydomek, emoji, rola)."""
    p = ROOT / "zespol" / f"{pid}.md"
    dane = {"id": pid, "imie": pid}
    try:
        tekst = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return dane
    if tekst.startswith("---"):
        for linia in tekst.split("---", 2)[1].splitlines():
            m = re.match(r"^([\w-]+):\s*(.*?)(\s+#.*)?\s*$", linia)
            if m:
                dane[m.group(1)] = m.group(2).strip().strip('"')
    return dane


def kto(pid):
    k = karta(pid)
    return f"{k.get('emoji', '')} {k.get('imie', pid)}".strip()


def sesja(pid):
    try:
        return (json.loads(SESJE.read_text(encoding="utf-8")).get("sesje", {}).get(pid) or {}).get("sesja")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def nowe_id(prefiks="o"):
    return f"{prefiks}_{teraz().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(3)}"


def bezpieczna_nazwa(nazwa):
    nazwa = re.sub(r"[^\w.\-]+", "-", pathlib.Path(nazwa or "plik").name, flags=re.U).strip("-.") or "plik"
    return nazwa[-80:]


def zapisz_wiadomosc(pid, wiadomosc):
    """Zapisuje wiadomość jako osobny plik. Zwraca ścieżkę (albo None, gdy taka wiadomość już jest)."""
    katalog = CZAT / pid
    katalog.mkdir(parents=True, exist_ok=True)
    for p in katalog.glob(f"*-{wiadomosc['id']}.json"):
        return None  # już zapisana (np. drugie obudzenie tą samą wiadomością)
    znacznik = wiadomosc["czas"][:19].replace("-", "").replace(":", "").replace("T", "-")
    p = katalog / f"{znacznik}-{wiadomosc['id']}.json"
    p.write_text(json.dumps(wiadomosc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return p


def git(*args, cicho=False):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode and not cicho:
        print(f"git {' '.join(args)}: {(r.stderr or r.stdout).strip()[:400]}", file=sys.stderr)
    return r.returncode == 0


def zapisz_w_archiwum(sciezki, opis):
    """Commit tylko podanych plików + wypchnięcie na main (do 4 prób). Nie rusza reszty pracy w toku."""
    rel = [str(pathlib.Path(s).resolve().relative_to(ROOT)) for s in sciezki if s]
    if not rel:
        return True
    git("add", "--", *rel)
    if subprocess.run(["git", "diff", "--cached", "--quiet", "--", *rel], cwd=ROOT).returncode == 0:
        return True  # nic nowego
    if not git("commit", "-q", "-m", opis, "--only", "--", *rel):
        return False
    for _ in range(4):
        git("pull", "-q", "--rebase", "--autostash", "origin", "main", cicho=True)
        if git("push", "-q", "origin", "HEAD:main", cicho=True):
            print("💾 Zapisane w archiwum – w biurze widać za ok. 15 s.")
            return True
    print("⚠️ Nie udało się wypchnąć do archiwum (zapisane lokalnie) – zapisz ręcznie: git pull --rebase origin main && git push origin HEAD:main",
          file=sys.stderr)
    return False


def telegram(tekst):
    skrypt = ROOT / "scripts" / "powiadom-telegram.sh"
    try:
        subprocess.run(["bash", str(skrypt), tekst], cwd=ROOT, timeout=60, capture_output=True)
    except Exception as e:  # powiadomienie to dodatek – nie przerywamy pracy
        print(f"Telegram: {e}", file=sys.stderr)


def plik_info(sciezka_lub_url):
    s = sciezka_lub_url.strip()
    if re.match(r"^https?://", s):
        nazwa = bezpieczna_nazwa(s.split("?")[0].rsplit("/", 1)[-1])
        return {"url": s, "nazwa": nazwa, "typ": mimetypes.guess_type(nazwa)[0] or ""}
    p = (ROOT / s).resolve() if not pathlib.Path(s).is_absolute() else pathlib.Path(s).resolve()
    try:
        rel = str(p.relative_to(ROOT))
    except ValueError:
        sys.exit(f"Plik {s} jest poza archiwum – skopiuj go najpierw do repozytorium.")
    if not p.exists():
        sys.exit(f"Nie ma pliku {rel}")
    return {"sciezka": rel, "nazwa": p.name, "typ": mimetypes.guess_type(p.name)[0] or "", "rozmiar": p.stat().st_size}


# ---------------------------------------------------------------- transkrypcja nagrań głosowych
def transkrybuj(plik):
    """Nagranie z mikrofonu → tekst (Gemini przez OpenRouter). Zwraca tekst albo None."""
    klucz = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not klucz:
        return None
    mp3 = plik.with_suffix(".transkrypcja.mp3")
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(plik), "-ac", "1", "-ar", "16000", "-b:a", "48k", str(mp3)],
                       check=True, timeout=180)
        b64 = base64.b64encode(mp3.read_bytes()).decode()
    except Exception as e:
        print(f"Transkrypcja: konwersja nie wyszła ({e})", file=sys.stderr)
        mp3.unlink(missing_ok=True)
        return None
    body = {"model": MODEL_AUDIO, "temperature": 0, "messages": [{"role": "user", "content": [
        {"type": "text", "text": "Przepisz dokładnie, co mówi osoba na nagraniu (po polsku, z interpunkcją). "
                                 "Zwróć wyłącznie transkrypcję, bez komentarzy. Jeśli nic nie słychać, zwróć: [cisza]"},
        {"type": "input_audio", "input_audio": {"data": b64, "format": "mp3"}}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {klucz}", "Content-Type": "application/json",
                                          "X-Title": "Klaudiusz FUDALI - czat"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            odp = json.loads(r.read().decode())
        return (odp.get("choices", [{}])[0].get("message", {}).get("content") or "").strip() or None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"Transkrypcja: {e}", file=sys.stderr)
        return None
    finally:
        mp3.unlink(missing_ok=True)


# ---------------------------------------------------------------- komendy
def napisz(a):
    if a.id not in znane_id():
        sys.exit(f"Nieznany pracownik '{a.id}'. Dostępni: {', '.join(znane_id())}")
    tekst = sys.stdin.read() if a.tekst == "-" else a.tekst
    tekst = (tekst or "").strip()
    if not tekst and not a.plik:
        sys.exit("Pusta wiadomość – podaj tekst albo --plik.")
    w = {"id": nowe_id("o"), "czas": teraz().isoformat(timespec="seconds"), "od": a.id, "do": "pablo",
         "typ": a.typ, "tekst": tekst, "pliki": [plik_info(p) for p in a.plik]}
    if a.re:
        w["re"] = a.re
    p = zapisz_wiadomosc(a.id, w)
    print(f"✉️  {kto(a.id)} → Pablo: {tekst[:120]}{'…' if len(tekst) > 120 else ''}")
    sciezki = [p] + [ROOT / f["sciezka"] for f in w["pliki"] if f.get("sciezka")]
    if not a.bez_zapisu:
        zapisz_w_archiwum(sciezki, f"Czat: {karta(a.id).get('imie', a.id)} pisze do Pablo")
    if a.typ == "prosba" or a.telegram:
        ikona = {"prosba": "🙋", "koniec": "✅"}.get(a.typ, "💬")
        telegram(f"{ikona} {kto(a.id)}: {tekst[:700]}\n\nOdpowiedz w biurze: {BIURO}/#czat-{a.id}")


def przyjmij(a):
    surowe = sys.stdin.read() if not a.json else a.json
    m = re.search(r"\{.*\}", surowe, re.S)
    if not m:
        sys.exit("Nie znalazłem JSON-a wiadomości (skopiuj całą zawartość bloku routine-fire-payload).")
    try:
        dane = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        sys.exit(f"Niepoprawny JSON wiadomości: {e}")
    pid = dane.get("do") or "klaudiusz"
    if pid not in znane_id():
        sys.exit(f"Wiadomość do nieznanego adresata '{pid}'.")
    czas = dane.get("czas") or teraz().isoformat(timespec="seconds")
    w = {"id": re.sub(r"[^\w-]", "", dane.get("id") or nowe_id("m"))[:60], "czas": czas, "od": "pablo", "do": pid,
         "typ": dane.get("typ") or "wiadomosc", "tekst": (dane.get("tekst") or "").strip(), "pliki": []}
    if dane.get("re"):
        w["re"] = str(dane["re"])[:80]
    if dane.get("re_tekst"):
        w["re_tekst"] = str(dane["re_tekst"])[:500]

    # załączniki: pobierz do archiwum (żeby pracownik mógł je obejrzeć narzędziem Read i użyć w pracy)
    zapisane = []
    for z in (dane.get("zalaczniki") or [])[:12]:
        url = z.get("url") or ""
        info = {"url": url, "nazwa": bezpieczna_nazwa(z.get("nazwa")), "typ": z.get("typ") or "", "rozmiar": z.get("rozmiar")}
        if re.match(r"^https://[\w.-]+\.blob\.vercel-storage\.com/", url):
            cel = ZALACZNIKI / pid / f"{czas[:19].replace('-', '').replace(':', '').replace('T', '-')}-{info['nazwa']}"
            cel.parent.mkdir(parents=True, exist_ok=True)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "klaudiusz-fudali"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    dane_pliku = r.read(MAX_ZALACZNIK + 1)
                if len(dane_pliku) > MAX_ZALACZNIK:
                    raise ValueError("plik za duży")
                cel.write_bytes(dane_pliku)
                info["sciezka"] = str(cel.relative_to(ROOT))
                zapisane.append(cel)
                if info["typ"].startswith("audio/"):
                    t = transkrybuj(cel)
                    if t:
                        info["transkrypcja"] = t
            except Exception as e:
                info["blad"] = f"nie pobrano: {e}"
        w["pliki"].append(info)
    if dane.get("transkrypcja_przegladarki"):
        w["transkrypcja_przegladarki"] = str(dane["transkrypcja_przegladarki"])[:8000]

    p = zapisz_wiadomosc(pid, w)
    if p is None:
        print(f"ℹ️  Wiadomość {w['id']} była już zapisana – nie dubluję.")
    elif not a.bez_zapisu:
        zapisz_w_archiwum([p, *zapisane], f"Czat: wiadomość od Pablo do {karta(pid).get('imie', pid)}")

    # podsumowanie dla pracownika (to on uruchamia „przyjmij” po wiadomości od listonosza czatu)
    linie = [f"📨 Wiadomość od Pablo z czatu w biurze → {kto(pid)} (id {w['id']}, {czas[11:16]})"]
    if w.get("re_tekst"):
        linie.append(f"(Odpowiedź na: „{w['re_tekst'][:300]}”)")
    if w["typ"] == "test":
        linie.append("[TEST POŁĄCZENIA – odpisz Pablo jednym zdaniem, że czat działa]")
    linie.append("")
    linie.append(w["tekst"] or "(bez tekstu – same załączniki)")
    if w.get("transkrypcja_przegladarki"):
        linie.append(f"\n🎤 Dyktowane (rozpoznanie w przeglądarce): {w['transkrypcja_przegladarki']}")
    if w["pliki"]:
        linie.append("\nZałączniki (zapisane w archiwum):")
        for f in w["pliki"]:
            opis = f.get("sciezka") or f.get("url")
            rodzaj = "obraz – obejrzyj narzędziem Read" if f["typ"].startswith("image/") else (
                "nagranie głosowe" if f["typ"].startswith("audio/") else f["typ"] or "plik")
            linie.append(f"- {opis} ({rodzaj})" + (f" – {f['blad']}" if f.get("blad") else ""))
            if f.get("transkrypcja"):
                linie.append(f"  🎤 Transkrypcja: {f['transkrypcja']}")
    linie.append(f"\nOdpowiadaj Pablo w czacie: python3 scripts/czat.py napisz {pid} \"…\"  "
                 f"(potrzebujesz czegoś → status.py {pid} czeka … --prosba; skończone → --typ koniec + meldunek do Klaudiusza).")
    print("=" * 70)
    s = sesja(pid)
    print(f"ADRESAT: {kto(pid)} (sesja {s or 'brak – zob. zespol/sesje.md'}). Jeśli to Ty – działaj. "
          f"Jeśli nie (np. jesteś Klaudiuszem, a wiadomość jest do pracownika) – przekaż poniższą treść send_message do jego sesji.")
    print("=" * 70)
    print("\n".join(linie))


def skrzynka(a):
    """Wiadomości od Pablo po ostatniej odpowiedzi pracownika (czyli jeszcze nieobsłużone) – z pełnymi szczegółami."""
    pliki = sorted((CZAT / a.id).glob("*.json"))
    wiad = [json.loads(p.read_text(encoding="utf-8")) for p in pliki]
    ostatnia_moja = max((i for i, w in enumerate(wiad) if w.get("od") == a.id), default=-1)
    nowe = [w for w in wiad[ostatnia_moja + 1:] if w.get("od") == "pablo"]
    if not nowe:
        print(f"📭 Skrzynka {kto(a.id)}: brak nowych wiadomości od Pablo (wszystko obsłużone). "
              f"Jeśli dopiero przyszło – zrób git pull --rebase origin main i sprawdź ponownie.")
        return
    print(f"📬 Skrzynka {kto(a.id)}: {len(nowe)} {'nowa wiadomość' if len(nowe) == 1 else 'nowe wiadomości'} od Pablo\n")
    for w in nowe:
        print(f"── {w['czas'][:16].replace('T', ' ')} · id {w['id']}" + (" · TEST POŁĄCZENIA" if w.get("typ") == "test" else ""))
        if w.get("re_tekst"):
            print(f"(odpowiedź na: „{w['re_tekst'][:300]}”)")
        print(w.get("tekst") or "(bez tekstu – same załączniki)")
        for f in w.get("pliki") or []:
            opis = f.get("sciezka") or f.get("url")
            rodzaj = "obraz – obejrzyj narzędziem Read" if (f.get("typ") or "").startswith("image/") else (
                "nagranie głosowe" if (f.get("typ") or "").startswith("audio/") else f.get("typ") or "plik")
            print(f"  📎 {opis} ({rodzaj})" + (f" – {f['blad']}" if f.get("blad") else ""))
            if f.get("transkrypcja"):
                print(f"     🎤 Transkrypcja: {f['transkrypcja']}")
        print()
    print(f"Odpowiadaj: python3 scripts/czat.py napisz {a.id} \"…\"  (prośba → status.py {a.id} czeka … --prosba; "
          f"koniec → --typ koniec + meldunek do Klaudiusza). Odpowiedź zamyka skrzynkę.")


def pokaz(a):
    pliki = sorted((CZAT / a.id).glob("*.json"))[-a.n:]
    if not pliki:
        print(f"Brak rozmów z {kto(a.id)}.")
    for p in pliki:
        w = json.loads(p.read_text(encoding="utf-8"))
        od = "Pablo" if w["od"] == "pablo" else kto(w["od"])
        zal = f" [+{len(w.get('pliki') or [])} zał.]" if w.get("pliki") else ""
        print(f"[{w['czas'][:16].replace('T', ' ')}] {od} ({w.get('typ', '')}){zal}: {w.get('tekst', '')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="komenda", required=True)
    n = sub.add_parser("napisz", help="pracownik pisze do Pablo")
    n.add_argument("id")
    n.add_argument("tekst", nargs="?", default="")
    n.add_argument("--plik", action="append", default=[], help="plik z archiwum albo link (można kilka razy)")
    n.add_argument("--typ", choices=TYPY, default="odpowiedz")
    n.add_argument("--re", help="id wiadomości Pablo, na którą odpowiadasz")
    n.add_argument("--telegram", action="store_true", help="dodatkowo powiadom Pablo na Telegramie")
    n.add_argument("--bez-zapisu", action="store_true")
    n.set_defaults(f=napisz)
    p = sub.add_parser("przyjmij", help="zapisz wiadomość od Pablo z biura (JSON na stdin)")
    p.add_argument("--json", help="JSON w argumencie zamiast stdin")
    p.add_argument("--bez-zapisu", action="store_true")
    p.set_defaults(f=przyjmij)
    k = sub.add_parser("skrzynka", help="nieobsłużone wiadomości od Pablo")
    k.add_argument("id")
    k.set_defaults(f=skrzynka)
    s = sub.add_parser("pokaz", help="ostatnie wiadomości z pracownikiem")
    s.add_argument("id")
    s.add_argument("-n", type=int, default=15)
    s.set_defaults(f=pokaz)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
