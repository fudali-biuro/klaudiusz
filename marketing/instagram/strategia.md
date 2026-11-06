# 📸 Instagram FUDALI – strategia i pierwsza siatka (Ola, 06.11.2026) – Etap 2, wersja robocza
Podstawa: `audyt-profilu.md` (Buffer, 41 postów), `tematy-z-wyszukiwan.md` (Bartek + Kuba), `zespol/lekcje-pablo.md`.
⚠️ Analiza niszy Mietka (`analiza-nisza.md`) wstrzymana – Apify zablokowany; strategia nie opiera się na danych konkurencji. Gdy wrócą dane – korekta.
Cel: profil „wow, to jest naprawdę dobra robota” → **zapytania (DM, strona, telefon)**, nie lajki. Mierzymy: komentarze, zapisy, udostępnienia, wiadomości.

## 1. Filary treści (proporcje z 10 postów)
| # | Filar | Udział | Po co | Format |
|---|---|---|---|---|
| 1 | **Jak powstaje** (warsztat, proces, maszyny) | 3/10 | najwyższy zasięg w historii konta; „jak powstaje/jak zrobić” to największa grupa pytań | reel 5–15 s |
| 2 | **Detal i rzemiosło** (słoje, łączenia, lina, 5 kolorów) | 2/10 | pokazuje jakość z bliska | karuzela 3–5 slajdów |
| 3 | **Wiedza** (drewno, pielęgnacja, przechowywanie) | 2/10 | zapisy i udostępnienia; sezon: zima | karuzela „zapisz” |
| 4 | **Realizacje i życie z produktem** (u klientów, lokalne, tarasy) | 2/10 | udostępnienia, dowód | zdjęcie „wow” / karuzela |
| 5 | **Oferta/sezon** (prezenty, nowość) | 1/10 | sprzedaż bez „kup” | karuzela / story |
Dodatkowo: **dowody zaufania** (opinie, gwarancja 1 rok, realizacje po latach) – wplatane w 1–4. Ludzie i historia firmy – gdy Pablo dostarczy zdjęcia/filmy ludzi przy pracy.

## 2. Zasady każdego posta
- **Pierwsza linia opisu = haczyk (≤100 znaków)**, nie „Cześć wszystkim”. Opis 150–400 znaków, nie 700.
- **1 pytanie lub „zapisz”** na końcu (komentarz/zapis > lajk). Max **3–5 hashtagów**, trafnych.
- Slajd 1 karuzeli = obietnica/pytanie; ostatni slajd = jedno CTA (napisz / zapisz).
- Grafiki: **prawdziwe zdjęcia z biblioteki** (rotacja, `zdjecia.py nastepne/uzyj`), montaż Zosi, spójny wzór: ciepły kremowy + ciemna zieleń + drewno, logo FUDALI w rogu, mało tekstu (styl Formatwood). Bez „grafika AI” na montażach.
- Rytm (polecenie Pablo, wzór Form at Wood): **codziennie 1 post lub reel + relacje każdego dnia** (zero „AI slopu”, każdy post ma sens i prawdziwy wygląd); reels min. 2–3/tydz.

## 3. Bio i wyróżnione
**Bio (propozycja, ≤150 znaków):**
```
Nowoczesne stolarstwo z Głogowa Młp. 🪵
Leżaki, meble i altany z litego drewna – robimy u nas.
📩 Napisz po wycenę ⬇️ fudali.com.pl
```
**Wyróżnione relacje (6) – okładki w stylu serii (Zosia):** **Leżak** (kolory, wymiary, jak złożyć) · **Jak to robimy** (warsztat, proces) · **Realizacje** · **Pielęgnacja** (przechowywanie, zima) · **Prezenty** (sezon) · **Pytania** (FAQ, wyceny, dostawa).

## 4. Pierwsza siatka 3×3 – 9 postów (kolejność publikacji od P1; w siatce najnowszy = lewy górny róg)
Układ po 9 postach (rząd górny = P9 P8 P7, środek = P6 P5 P4, dół = P3 P2 P1) – kolory naprzemiennie: ciepłe tarasowe zdjęcie / jasny detal / zdjęcie ciemne, żeby siatka „oddychała”.

| P | Dzień | Filar | Format | Slajd 1 / haczyk (pierwsza linia) | Materiał (biblioteka) | Pytanie / CTA |
|---|---|---|---|---|---|---|
| P1 | pon 9.11 | Detal | karuzela 6 slajdów | „Ten sam leżak. 5 kolorów. Który jest Twój?” | zdjęcia reklamowe fotografa `produkty/*banasik-zdjecia-reklamowe-fud-14`(czarny), `-15`(ciemny brąz), `-16`(grafit), `-17`(brąz), `-18`(jasny) – 1 slajd = 1 kolor (zbliżenie listew) + slajd końcowy ze wszystkimi (`…-fud-10`/`-11`/`fud`) | „Napisz numer koloru 👇” (jasny brąz, brąz, ciemny brąz, grafit, czerń – wg `produkty.md`) |
| P2 | wt 10.11 | Wiedza | karuzela 4 slajdy | „Jak przechować drewniany leżak na zimę – 3 zasady” | leżak złożony: `…banasik…-fud-10` (grafit), `-11` (czarny), `…-fud.jpg` (brąz) + zdjęcie tarasu/zimy z biblioteki | „Zapisz, zanim spadnie śnieg 📌” (fakty: sucho, przewiewnie, z dala od wilgoci i dużego ciepła – `produkty.md`) |
| P3 | śr 11.11 | Proces | reel 8–12 s | „Z płatka dębu robimy stolik. Tak to wygląda od środka” | `gotowe/…wyciete-blaty-…patka` → `gotowe/…stolik-patek-…` (montaż prawdziwych zdjęć, ruch) | „Który kształt blatu wolisz?” |
| P4 | czw 12.11 | Detal/dowód | karuzela 5 slajdów | „Rama 30 mm, listwy 50 mm, 10 kg. Z czego jest nasz leżak?” | infografika wymiarów `…-fud-12` (100×55×90) i `-19` (złożony 125 cm), poduszka `-20`, lina `-21`, detal listew `-15` | „Co chcesz zobaczyć z bliska?” |
| P5 | pt 13.11 | Życie | pojedyncze „wow” | „Wieczór, który zaczyna się od ognia 🔥” | `gotowe/…taras-z-palenisko…` | „Z kim byś tu usiadł?” |
| P6 | sob 14.11 | Oferta/sezon | karuzela 4 slajdy | „Prezent dla taty, który ma wszystko – 4 pomysły od 49 zł” | otwieracz „Kot”, podkładka, składany stolik, leżak (ceny: 49/99/229/299 zł z `produkty.md`) | „Komu to wyślesz?” |
| P7 | ndz 15.11 | Proces | reel 8 s | „Jak się składa leżak? Zobacz animację konstrukcji” | `produkty/…7b25c15….mp4` (animacja 3D składania, 7 s) + napisy | „Chcesz film z warsztatu? Napisz TAK” |
| P8 | pon 16.11 | Realizacje | karuzela 3 slajdy | „Leżaki na werandzie klienta – tak mieszkają” | **tylko prawdziwa realizacja u klienta:** `produkty/…image-20260904-110937-616` (weranda z mozaiką; wg Zosi/Pablo) – zdjęcia „istock” to stock, NIE podpisujemy jako realizacji | „Jak urządzasz taras?” |
| P9 | wt 17.11 | Wiedza | karuzela 5 slajdów | „Dąb czy jodła? Czym się różnią nasze meble” | stołki z dębu (`gotowe/…stokow…`), leżak z jodły | „Jodła czy dąb – głosuj w komentarzu” (**fakty o twardości/kolorze – do weryfikacji, na razie tylko: jodła FSC (leżak), dąb czerwony (stołki, Płatek)**) |
**Materiał:** pracujemy na bibliotece (60+ prawdziwych zdjęć). Dodatkowe filmy/zdjęcia z warsztatu, realizacji z nazwą miejscowości i ludzi przy pracy załatwia Klaudiusz (nie prosimy Pabla) – gdy się pojawią, zamieniamy nimi P3/P7 i dokładamy serię z bohaterem.

## 5. Stories – 7 dni (9–15.11), codziennie 3–5 klatek, ankieta/quiz/pytanie
| Dzień | Temat | Klatki |
|---|---|---|
| pon 9.11 | **Jodła czy dąb?** (ankieta) | leżak (jodła FSC) vs stołki (dąb czerwony); wynik w kolejnej klatce |
| wt 10.11 | **Quiz: ile waży leżak?** 5 / 10 / 15 kg | leżak złożony; odpowiedź: 10 kg (`produkty.md`) |
| śr 11.11 | **Zza kulis: z czego to zrobione** | lina jutowa, detal listew, poduszka bawełniana |
| czw 12.11 | **Wybierz kolor** (ankieta 2 opcje ×2) | 4 detale kolorów; zapowiedź posta P1 wyniki |
| pt 13.11 | **Zadaj pytanie stolarzowi** (okienko pytań) | zdjęcie podkładek z warsztatu; „odpowiem w reelsie” |
| sob 14.11 | **Taras o zmierzchu** + „z kim usiądziesz?” (suwak) | taras z paleniskiem |
| ndz 15.11 | **Zapowiedź tygodnia** + „Co chcesz zobaczyć: warsztat czy realizacje?” | 2 miniatury |
Każdy dzień: 1 klatka z CTA „Pisz w wiadomości – wycena, wymiary, dostawa”. Sezon prezentów (Mikołajki) w 1 story/tydz.

## 6. Podgląd siatki 3×3
Zlecone Zosi: `marketing/instagram/siatka-3x3.jpg` (9 miniatur P1–P9 wg tabeli, spójne okładki, logo, kolory) + okładki wyróżnionych.

## 7. Pomiar (co tydzień, poniedziałek)
Z Buffera: zasięg, komentarze, zapisy, udostępnienia na post; liczba wiadomości (DM) – zgłasza Pablo; cel na 4 tygodnie: ≥3 komentarze/post, ≥10 zapisów w karuzelach „wiedzy”, ≥5 zapytań DM/tydz.

## 8. Wnioski z analizy niszy (Mietek, wersja bez scrapera) – co dokładamy
- Konkurenci (Domki Sauny, Altanka) mają **bardzo słabe zaangażowanie** (<25 polubień, ~0 komentarzy, filmy <1,5 tys.) – prawdziwy warsztat + konkretna oferta łatwo się wyróżni; siatka spójna sama jest przewagą.
- Najlepszy format u nich: **osoba + proces + napisy słowo po słowie + konkretny termin** → **seria z bohaterem** (osoba z warsztatu, stała nazwa serii, np. „Stolarz tłumaczy”) – wymaga krótkich nagrań z Pablem/pracownikiem (prośba o telefon).
- Dołożyć do planu po P9: karuzele „Jak rozpoznać dobre drewno” i „Jak olejować leżak” (fakty o pielęgnacji do weryfikacji – Marek/Bartek), „5 prezentów z drewna do 300 zł”, CTA „napisz w wiadomości + termin wysyłki przed świętami”.
- Stories i wyróżnione konkurencji – niezweryfikowane (brak dostępu).
