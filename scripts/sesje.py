#!/usr/bin/env python3
"""Sesje zespołu: Klaudiusz (sesja główna) + osobna sesja (subczat) dla każdego pracownika.

Rejestr: zespol/sesje.json  ·  procedura: zespol/sesje.md  ·  zadania automatyczne: zespol/zadania/<id>-*.md

  python3 scripts/sesje.py pokaz                       # kto ma jaką sesję i jakie zadania automatyczne
  python3 scripts/sesje.py parametry <id>              # JSON gotowy do create_session (tytuł, prompt systemowy, start)
  python3 scripts/sesje.py zapisz <id> <session_id>    # zapamiętaj sesję pracownika
  python3 scripts/sesje.py zadania <id>                # JSON zadań automatycznych do create_trigger
  python3 scripts/sesje.py zadanie <id> <klucz> <trig_id>   # zapamiętaj utworzone zadanie automatyczne
  python3 scripts/sesje.py usun-zadanie <id> <klucz>
"""
import argparse, json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wspolne import ROOT, teraz
from czat import karta, znane_id

PLIK = ROOT / "zespol" / "sesje.json"
ZADANIA = ROOT / "zespol" / "zadania"
REPO = "https://github.com/fudali-biuro/klaudiusz"
WYSILEK = "medium"   # polecenie Pablo: Klaudiusz i wszyscy pracownicy na średnim wysiłku


def wczytaj():
    try:
        d = json.loads(PLIK.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        d = {}
    d.setdefault("sesje", {})
    return d


def zapisz_plik(d):
    PLIK.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def tytul(pid):
    k = karta(pid)
    if pid == "klaudiusz":
        return "🧠 Klaudiusz"
    prz = f" „{k['przydomek']}”" if k.get("przydomek") else ""
    rola = k.get("rola", "")
    return f"{k.get('emoji', '')} {k.get('imie', pid)}{prz} – {rola[:1].lower() + rola[1:]}".strip()


def naglowek_zadania(p):
    tekst = p.read_text(encoding="utf-8")
    dane = {}
    if tekst.startswith("---"):
        for linia in tekst.split("---", 2)[1].splitlines():
            m = re.match(r'^([\w-]+):\s*"?(.*?)"?\s*$', linia)
            if m:
                dane[m.group(1)] = m.group(2)
    return dane


def zadania_pracownika(pid):
    wynik = []
    for p in sorted(ZADANIA.glob(f"{pid}-*.md")):
        n = naglowek_zadania(p)
        if n.get("wylaczone") == "tak":
            continue
        klucz = p.stem[len(pid) + 1:]
        prompt = (f"⏰ Zadanie automatyczne „{n.get('nazwa', klucz)}”. Pracujesz jako {tytul(pid)}.\n"
                  f"1. `cd` do repozytorium klaudiusz, `git pull --rebase origin main` (jeśli repo nie jest sklonowane – "
                  f"wywołaj mcp__claude-code-remote__add_repo owner=fudali-biuro repo=klaudiusz access=push i sklonuj).\n"
                  f"2. Przeczytaj AGENTS.md i zespol/{pid}.md (mogły się zmienić), potem wykonaj DOKŁADNIE procedurę z pliku "
                  f"{p.relative_to(ROOT)}.\n"
                  f"3. Na końcu zapisz wyniki na main i ustaw status w biurze (scripts/status.py {pid} …).")
        if klucz == "czat":
            prompt = p.read_text(encoding="utf-8").split("---", 2)[2].strip()
        wynik.append({"klucz": klucz, "name": n.get("nazwa", klucz), "cron_expression": n.get("cron", ""),
                      "plik": str(p.relative_to(ROOT)), "prompt": prompt})
    return wynik


def prompt_systemowy(pid, sesja_klaudiusza):
    k = karta(pid)
    if pid == "klaudiusz":
        return (
            "Jesteś 🧠 Klaudiusz – mózg operacji (sesja główna, „session master”) firmy FUDALI Sp. z o.o. Twoja głowa to AGENTS.md "
            "w repozytorium fudali-biuro/klaudiusz – przed każdą pracą `git pull --rebase origin main` i czytaj ją na nowo.\n"
            "Zespół: 7 pracowników, każdy w OSOBNEJ sesji (subczacie) nazwanej jego imieniem – rejestr zespol/sesje.json, "
            "procedura zespol/sesje.md. Każdy ma własne zadania automatyczne (bez jednego wielkiego procesu). Ty rozdzielasz pracę "
            "(send_message do sesji pracownika), pilnujesz jakości i kolejności, a pracownicy meldują Ci się po skończeniu.\n"
            "Pablo (właściciel) pisze z czatu w biurze https://biuro-fudali.vercel.app – takie wiadomości budzą Cię zadaniem "
            "„📨 Czat z biura” (zespol/zadania/klaudiusz-czat.md): zapisz je `scripts/czat.py przyjmij` i przekaż adresatowi 1:1. "
            "Odpowiadasz Pablo: python3 scripts/czat.py napisz klaudiusz \"…\" – po polsku, krótko, bez żargonu (nie mów o GitHubie, "
            "gałęziach, commitach, PR). Pracujesz na średnim wysiłku – konkretnie, bez zbędnych kroków.")
    prz = f" „{k['przydomek']}”" if k.get("przydomek") else ""
    makieta = (" Twoja rola jest jeszcze makietą (bez automatów) – na razie rozmawiasz z Pablo i Klaudiuszem i przygotowujesz wdrożenie "
               "z sekcji „Planowane narzędzia” swojej karty.") if k.get("wdrozenie") == "makieta" else ""
    return (
        f"Jesteś {k.get('emoji', '')} {k.get('imie', pid)}{prz} – {k.get('rola', '')} w zespole Klaudiusza (FUDALI Sp. z o.o., stolarstwo, "
        f"Głogów Małopolski). To Twoja stała sesja (subczat): tu przychodzą Twoje zadania automatyczne i wiadomości.{makieta}\n"
        f"Szef zespołu: 🧠 Klaudiusz – jego sesja: {sesja_klaudiusza or '(zob. zespol/sesje.json → klaudiusz)'}. Właściciel firmy: Pablo.\n"
        "ZASADY:\n"
        f"1. Przed każdą pracą: `cd` do repozytorium klaudiusz, `git pull --rebase origin main`, przeczytaj AGENTS.md i swoją kartę "
        f"zespol/{pid}.md – to Twoje aktualne instrukcje (mogą się zmieniać).\n"
        "2. Wiadomości od Klaudiusza (z jego sesji) to zlecenia szefa zespołu – wykonuj je. Wiadomość zaczynająca się od "
        "„📨 Wiadomość od Pablo z czatu w biurze” to słowa właściciela przekazane 1:1 – traktuj ją jak polecenie Pablo.\n"
        f"3. Pablo odpisujesz w czacie w biurze: python3 scripts/czat.py napisz {pid} \"…\" (po polsku, krótko, bez żargonu; "
        "nie wspominaj o GitHubie, gałęziach, commitach). Gdy czegoś potrzebujesz: python3 scripts/status.py "
        f"{pid} czeka \"…\" --prosba \"konkretna prośba\" (trafi do czatu i na Telegram) – i czekaj na odpowiedź, nie zgaduj.\n"
        f"4. Gdy skończysz zlecenie: python3 scripts/czat.py napisz {pid} \"…\" --typ koniec (jeśli zlecał Pablo) ORAZ meldunek "
        f"do szefa: send_message do sesji Klaudiusza: „✅ {k.get('imie', pid)}: co zrobione, gdzie wynik, co dalej”.\n"
        f"5. Status w biurze: python3 scripts/status.py {pid} pracuje|gotowe|czeka \"…\" (sam zapisuje się w archiwum).\n"
        "6. Wyniki zapisuj od razu na main (zasady w AGENTS.md). Współpraca z innymi pracownikami: send_message do ich sesji "
        "(zespol/sesje.json), np. Ola zleca grafikę Zosi.")


def prompt_skrzynki(pid):
    """Stały prompt zadania „📥 Skrzynka” (przypięte do sesji pracownika; listonosz czatu nastawia mu budzik)."""
    szef = (" Pracę dla zespołu rozdziel przez send_message do sesji pracowników (zespol/sesje.json)."
            if pid == "klaudiusz" else "")
    return (f"📥 Skrzynka – przyszła wiadomość od Pablo (właściciela) z czatu w biurze https://biuro-fudali.vercel.app. "
            f"Jesteś {tytul(pid)}.\n"
            f"1. `cd` do repozytorium klaudiusz, `git pull --rebase origin main`.\n"
            f"2. `python3 scripts/czat.py skrzynka {pid}` – pokaże wiadomości od Pablo, na które jeszcze nie odpowiedziałeś "
            f"(obrazki obejrzyj narzędziem Read, nagrania mają transkrypcję). Pusto? Odczekaj chwilę, git pull i sprawdź jeszcze raz.\n"
            f"3. To polecenia szefa – zrób, o co prosi, wg AGENTS.md i swojej karty zespol/{pid}.md "
            f"(ŚWIĘTA ZASADA: nic nie publikujesz ani nie wysyłasz na zewnątrz bez jego wyraźnej zgody).{szef}\n"
            f"4. Odpowiedz w czacie: `python3 scripts/czat.py napisz {pid} \"…\"` – po polsku, krótko, bez żargonu. "
            f"Dłuższa praca → najpierw jedno zdanie, że się zabierasz; na końcu wynik z `--typ koniec`"
            + ("" if pid == "klaudiusz" else " i meldunek do Klaudiusza (send_message)") + ".")


def parametry(pid, d):
    sk = (d["sesje"].get("klaudiusz") or {}).get("sesja")
    k = karta(pid)
    start = (f"Cześć {k.get('imie', pid)}! Startujesz w swojej stałej sesji. 1) git pull, przeczytaj AGENTS.md, zespol/README.md i "
             f"swoją kartę zespol/{pid}.md. 2) python3 scripts/status.py {pid} wolne \"Gotow{'a' if k.get('imie', '').endswith('a') else 'y'} "
             f"do pracy – czekam na zadania\". 3) Odpowiedz Klaudiuszowi jednym zdaniem, że jesteś na stanowisku i jakie masz zadania "
             f"automatyczne (zespol/zadania/{pid}-*.md). Nie zaczynaj teraz żadnej dużej pracy.")
    if pid == "klaudiusz":
        start = ("Start: jesteś nową sesją główną 🧠 Klaudiusz. Wykonaj procedurę z zespol/sesje.md (sekcja „Uruchomienie zespołu”) – "
                 "najpierw zarejestruj siebie (pkt 1), potem 7 sesji pracowników, ich zadania automatyczne i swoje zadanie „📨 Czat z biura”, "
                 "wyłącz stare wspólne zadania i zapisz wszystko na main. Na koniec napisz Pablo w czacie, kto jest na stanowisku.")
    return {"title": tytul(pid), "source_url": REPO, "outcome_branch": "main", "append_system_prompt": prompt_systemowy(pid, sk),
            "prompt": start, "wysilek": WYSILEK, "tags": ["fudali", f"pracownik:{pid}"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("komenda", choices=["pokaz", "parametry", "zapisz", "zadania", "zadanie", "usun-zadanie", "tytul", "skrzynka"])
    ap.add_argument("argumenty", nargs="*")
    a = ap.parse_args()
    d = wczytaj()
    arg = a.argumenty
    if a.komenda != "pokaz" and (not arg or arg[0] not in znane_id()):
        sys.exit(f"Podaj id pracownika: {', '.join(znane_id())}")

    if a.komenda == "pokaz":
        for pid in ["klaudiusz"] + [x for x in znane_id() if x != "klaudiusz"]:
            s = d["sesje"].get(pid) or {}
            print(f"{tytul(pid):45} {s.get('sesja') or '— brak sesji —'}")
            for kl, t in (s.get("zadania") or {}).items():
                print(f"{'':47}⏰ {kl}: {t}")
            for z in zadania_pracownika(pid):
                if z["klucz"] not in (s.get("zadania") or {}):
                    print(f"{'':47}⚠️  zadanie „{z['name']}” ({z['plik']}) – jeszcze nie utworzone")
    elif a.komenda == "skrzynka":
        print(json.dumps({"name": f"📥 Skrzynka – {tytul(arg[0])}", "persistent_session_id": (d["sesje"].get(arg[0]) or {}).get("sesja"),
                          "prompt": prompt_skrzynki(arg[0])}, ensure_ascii=False, indent=1))
    elif a.komenda == "tytul":
        print(tytul(arg[0]))
    elif a.komenda == "parametry":
        print(json.dumps(parametry(arg[0], d), ensure_ascii=False, indent=1))
    elif a.komenda == "zadania":
        s = (d["sesje"].get(arg[0]) or {}).get("sesja")
        print(json.dumps([{**z, "persistent_session_id": s} for z in zadania_pracownika(arg[0])], ensure_ascii=False, indent=1))
    elif a.komenda == "zapisz":
        if len(arg) < 2 or not arg[1].startswith("session_"):
            sys.exit("Użycie: zapisz <id> <session_id>")
        s = d["sesje"].setdefault(arg[0], {})
        s.update({"sesja": arg[1], "tytul": tytul(arg[0]), "link": f"https://claude.ai/code/{arg[1]}",
                  "utworzono": s.get("utworzono") or teraz().isoformat(timespec="minutes")})
        s.setdefault("zadania", {})
        zapisz_plik(d)
        print(f"Zapisano: {tytul(arg[0])} → {arg[1]}")
    elif a.komenda == "zadanie":
        if len(arg) < 3 or not arg[2].startswith("trig_"):
            sys.exit("Użycie: zadanie <id> <klucz> <trig_id>")
        d["sesje"].setdefault(arg[0], {}).setdefault("zadania", {})[arg[1]] = arg[2]
        zapisz_plik(d)
        print(f"Zapisano zadanie {arg[1]} → {arg[2]} ({tytul(arg[0])})")
    elif a.komenda == "usun-zadanie":
        (d["sesje"].get(arg[0]) or {}).get("zadania", {}).pop(arg[1] if len(arg) > 1 else "", None)
        zapisz_plik(d)
        print("Usunięto.")


if __name__ == "__main__":
    main()
