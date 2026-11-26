# 🚜 Plan treści i wdrożenia SEO – maszyny budowlane (Bartek, 26.11.2026)

Mapa fraz i dane: `seo/maszyny-mapa-fraz.md` (czytaj najpierw). Brief: `marketing/kampanie/maszyny-seo/brief.md`.
Wykonawcy: strona WWW = sesja „Strona FUDALI” (edycja), teksty = Ola (pracownia tekstu: Ola → Kuba → Bartek), ceny/oferta = Marek, reklamy = Klaudiusz. 🔒 Nic nie publikujemy bez „tak” Pablo.

## 0. Zasady twarde (z briefu i lekcji Pablo)
- **Nigdy nie piszemy, że FUDALI jest dealerem JCB/CAT/Volvo/Case/Komatsu.** Cudze marki tylko w porównaniach („alternatywa dla JCB 3CX”, „czym różni się od JCB”) z datą i źródłem cen.
- **„Najlepsza/najtańsza” tylko z uzasadnieniem** (gwarancja, serwis, cena, dostępność od ręki). Fakty z katalogu producenta i z ogłoszenia – nic wymyślonego. Parametry modeli innych niż 388 – wyłącznie z `katalog/Katalog-koparko-ladowarki-PL.pdf`.
- Cena publikowana **tylko dla Shanmon Fuji 388 (250 000 zł netto)**. Pozostałe modele: „na zamówienie – zapytaj o ofertę” (nie mamy cenników).
- Kontakt w każdej treści: **biuro@fudali.com.pl · numer maszyn (patrz NAP niżej)**.
- ⚠️ **Do wyjaśnienia z Pablo przed publikacją strony 388:** katalog podaje dla „388” 81 kW i głęb. kopania 3 967 mm, a ogłoszenie/strona (nasz egzemplarz) 74 kW, ramię do 5,5 m (4,1 m bez wysuwu). Takie dane (ramię teleskopowe 4 300/5 510 mm) katalog przypisuje wersji **388T**. Trzeba ustalić, którą wersją jest egzemplarz na sprzedaż – inaczej kupujący (i Google) zobaczą niezgodność strony z katalogiem. Do czasu odpowiedzi: **na stronie 388 zostają dane z ogłoszenia** (to maszyna, którą sprzedajemy).

## 1. Architektura adresów (WordPress/Elementor – istniejące i nowe)
```
/maszyny-budowlane/                         HUB: koparko-ładowarki na sprzedaż (istnieje – rozbudować)
 ├─ /maszyny-budowlane/shanmon-fuji-388/    model 388 – nasza maszyna od ręki (istnieje – dopracować)
 ├─ /maszyny-budowlane/shanmon-fuji-377/    (nowe, „na zamówienie”)
 ├─ /maszyny-budowlane/shanmon-fuji-388-ii/
 ├─ /maszyny-budowlane/shanmon-fuji-388t/
 ├─ /maszyny-budowlane/shanmon-fuji-388h/
 ├─ /maszyny-budowlane/shanmon-fuji-398h/
 ├─ /maszyny-budowlane/shanmon-fuji-378h/
 ├─ /maszyny-budowlane/ladowarka-kolowa-wz30-25/
 ├─ /maszyny-budowlane/shanmon/             strona-marka: „Shanmon w Polsce”, tabela porównawcza modeli
 ├─ /maszyny-budowlane/nowa-koparko-ladowarka-cena/      poradnik cenowy (T)
 ├─ /maszyny-budowlane/chinska-koparko-ladowarka-czy-warto/   (K)
 ├─ /maszyny-budowlane/alternatywa-dla-jcb-3cx/           (K, największy popyt)
 ├─ /maszyny-budowlane/leasing-koparko-ladowarki/         (T)
 ├─ /maszyny-budowlane/gwarancja-i-serwis/               (T/zaufanie)
 └─ /maszyny-budowlane/dostawa-koparko-ladowarki-cala-polska/  (regiony)
```
Konwencja: małe litery, bez polskich znaków w adresie, myślniki; **nie zmieniać istniejących adresów** (jeśli trzeba – 301). Slug „shanmon-fuji-…” jest zgodny z istniejącym `/shanmon-fuji-388/`. Nazwa „Fuji” wg strony 388 – **potwierdzić, że wszystkie modele (377…WZ30-25) to ta sama linia „Shanmon Fuji”** (katalog nie podaje nazwy marki; ceny.md/ogłoszenie podają „Shanmon Fuji 388”). Jeśli linia ma inną nazwę – w slugach i tytułach użyć „Shanmon” + numer modelu.

## 2. Specyfikacja stron (title ≤ 60 zn., meta ≤ 155 zn.)
### 2.1 HUB `/maszyny-budowlane/` (poprawki istniejącej)
- **Title:** `Koparko-ładowarki na sprzedaż – nowe, od ręki | FUDALI` (frazy: koparko-ładowarki, na sprzedaż, nowe, od ręki)
- **Meta:** `Nowe koparko-ładowarki Shanmon: 388 od ręki w Rzeszowie, pozostałe modele na zamówienie. Gwarancja, serwis, leasing, dostawa w całej Polsce. Zadzwoń.`
- **H1:** zostaje „Koparko-ładowarki na sprzedaż”.
- **Dodać sekcje (H2):** „Dla kogo koparko-ładowarka” · „Tabela modeli 377 / 388 / 388T / 388H / 398H / 378H” (masa, moc, pojemność łyżek, głębokość kopania – z katalogu; link do każdego modelu) · „Czym różni się od JCB 3CX” (link do porównania; **bez** twierdzenia o dealerstwie) · „Gwarancja i serwis” · „Leasing” · „Dostawa i oględziny w Rzeszowie” · „Najczęstsze pytania” (rozszerzyć o: ile kosztuje nowa, czy chińska jest dobra, jak z gwarancją, jak z częściami, czy da się leasing, dowóz).
- Akapit z frazą potoczną: „koparko-ładowarka (potocznie ‘ostrówek’)”.
- **Schema:** CollectionPage/ItemList (modele) + Organization/LocalBusiness (pkt 4) + FAQPage (pkt 4).

### 2.2 `/maszyny-budowlane/shanmon-fuji-388/` (dopracować)
- **Title:** `Koparko-ładowarka Shanmon Fuji 388 – nowa 2026, od ręki | FUDALI` (59 zn.)
- **Meta:** zostaje obecna (jest dobra: 74 kW, 5,5 m, 6w1, 250 000 zł netto, Rzeszów, gwarancja 12 mies., leasing).
- **Dodać:** akapit „(często wpisywane też jako Shannon 388)” w FAQ; tabela „388 vs JCB 3CX” (link do porównania); video z pracy maszyny (Zosia/Marek) – VideoObject; link „Pozostałe modele Shanmon”; breadcrumbs są ✓.
- **Schema Product** – patrz pkt 4.

### 2.3 Podstrony modeli (7 + WZ30-25) – szablon
- **Title:** `Shanmon Fuji {MODEL} – koparko-ładowarka na zamówienie | FUDALI`
- **Meta:** `Shanmon Fuji {MODEL}: {moc} kW, {masa} kg, głębokość kopania do {głęb.} mm. Dane z katalogu, oferta na zamówienie – FUDALI, Rzeszów, tel. {NAP}.`
- **H1:** `Koparko-ładowarka Shanmon Fuji {MODEL}`
- **Sekcje:** „Dane techniczne” (tabela z katalogu) · „Dla kogo ten model” (2–3 zdania, bez zmyśleń) · „Zapytaj o ofertę” (formularz + telefon) · „Gwarancja, serwis, leasing” (linki) · „Porównaj z innymi modelami” (link do `/shanmon/`) · FAQ (3–4 pytania).
- **Cena:** „na zapytanie” (nie podajemy kwot).
- **Dane z katalogu PL (do wklejenia do tabel; masa eksploatacyjna / silnik / łyżki / głębokość):**

| Model | Masa | Moc znamionowa (silnik wg katalogu) | Łyżka przód / tył | Maks. głęb. kopania |
|---|---|---|---|---|
| 377 | 8 100 kg | 77,3 kW (Yudong YCD4M22T-105) | 1,0 m³ / 0,3 m³ | 3 967 mm |
| 388 (wg katalogu) | 8 445 kg | 81 kW (Yuchai YC4A110Z-T23) | 1,0 / 0,3 m³ | 3 967 mm |
| 388-II | 8 700 kg | 82 kW (Cummins 4BTA3.9-C110) | 1,0 / 0,3 m³ | 3 967 mm |
| 388T | 8 700 kg | wersje silnika 70–81 kW (4 opcje: Perkins 74,5; Weichai 74; Yuchai 81; Weichai 70) | 1,0 / 0,3 m³ | 4 300 / 5 510 mm (ramię teleskopowe); siła uciągu 76 kN |
| 388H | 10 200 kg | wersje silnika 74–82 kW (Perkins/Weichai Euro V oraz Yuchai/Weichai China II) | 1,2 / 0,3 m³ | 4 150 / 5 360 mm; siła uciągu 84 kN |
| 398H | 10 200 kg | jak 388H (74–82 kW) | 1,2 / 0,3 m³ | 4 150 / 5 360 mm |
| 378H | 8 800 kg | 82 kW (WP4G110E220) | 1,0 / 0,3 m³ | 3 780 mm; prześwit 390 mm |
| WZ30-25 (ładowarka kołowa z osprzętem koparkowym) | 7 650 kg | 75 kW (YC4A105Z-T20) | 1,0 / 0,3 m³ | 4 082 mm; udźwig ładowarki 2 500 kg; do 22 km/h |
⚠️ Przed publikacją: **Marek/Pablo potwierdzają**, które wersje silnika są w ofercie (388T/388H/398H mają kilka), czy wymiary „(Parametry mogą ulec zmianie bez powiadomienia)” trzeba oznaczyć jako „wg katalogu producenta”, oraz certyfikację CE/Stage V dla każdego modelu (katalog wymienia „Euro V” tylko przy wybranych silnikach – nie pisać „Stage V” dla modeli bez dokumentu).

### 2.4 Strona-marka `/maszyny-budowlane/shanmon/`
- **Title:** `Shanmon w Polsce – koparko-ładowarki Fuji, modele i serwis | FUDALI`
- **Treść:** kim jest producent (z katalogu: zakład przemysłowy w Chinach, ok. 32 ha, 120 000 m² zabudowy – **sprawdzić brzmienie w broszurze** `Broszura-maszyny-budowlane-PL.pdf` i cytować dosłownie), tabela porównawcza wszystkich modeli, „jak wybrać model” (masa/głębokość/łyżka), gwarancja i serwis, linki do modeli. Wzmianka „Shannon” (pisownia).

### 2.5 Poradniki sprzedażowe (Ola – pracownia tekstu; ja – brief + SEO)
| Strona | Title (≤60) | Kluczowe frazy | Zawartość (bez zmyśleń) |
|---|---|---|---|
| `nowa-koparko-ladowarka-cena` | `Ile kosztuje nowa koparko-ładowarka? Ceny 2026 | FUDALI` | nowa koparko ładowarka cena, jcb nowa cena, chińska cena | tabela przedziałów cen **z datą i źródłem** (Mietek: Kingway 139, Stroer 220, FUDALI 250, CASE 399, JCB 3CX PRO 464 tys. zł netto – z ogłoszeń 25–26.11; zaznaczyć, że netto/brutto bywa niepodane i że to ceny ofertowe); co wchodzi w cenę (wyposażenie, gwarancja, serwis); uwaga „cena za godzinę to wynajem – inna usługa”. |
| `chinska-koparko-ladowarka-czy-warto` | `Chińska koparko-ładowarka – czy warto? Uczciwy poradnik | FUDALI` | chińska koparko ładowarka (cena/nowa/olx/otomoto) | kryteria wyboru (serwis, części, gwarancja, silnik, dokumenty), co sprawdzić przy zakupie, jak FUDALI to zabezpiecza (gwarancja 12 mies. silnik/skrzynia/most, infolinia, serwis z dojazdem – fakty z ogłoszenia). Ton: pomocny, bez ataku na rywali. |
| `alternatywa-dla-jcb-3cx` | `Alternatywa dla JCB 3CX – porównanie ceny i parametrów | FUDALI` | jcb 3cx cena, jcb 4cx, jcb nowa cena, cat 432, alternatywa | tabela: cena (JCB z ogłoszenia, data), moc, masa, głębokość kopania, gwarancja; **wyraźny disclaimer: FUDALI nie jest dealerem JCB/CAT; marki użyte porównawczo**. Dane techniczne JCB tylko ze stron producenta/ogłoszeń z linkiem. |
| `leasing-koparko-ladowarki` | `Leasing koparko-ładowarki – jak kupić bez gotówki | FUDALI` | koparko ładowarka leasing, kredyt, cesja | leasing operacyjny/finansowy dla firm, kredyty (zgodnie z ogłoszeniem: pomoc w formalnościach); **bez rat i oprocentowania** (nie mamy – Marek). CTA: kalkulator/telefon. |
| `gwarancja-i-serwis` | `Gwarancja i serwis koparko-ładowarek Shanmon | FUDALI` | gwarancja, serwis, części | 12 mies. (silnik, skrzynia, most), całodobowa infolinia, serwis z dojazdem, pomoc w częściach, filtry/narzędzia do 500 mth (z ogłoszenia – „do ustalenia przy zakupie”). |
| `dostawa-koparko-ladowarki-cala-polska` | `Dostawa koparko-ładowarki w całej Polsce | FUDALI` | olx + województwo, transport | tabela województw (czas/koszt dostawy – **Marek poda**; do tego czasu „wycena transportu”), oględziny i jazda próbna w Rzeszowie po umówieniu. |

## 3. Linkowanie wewnętrzne
- **Menu główne:** „Maszyny budowlane” (jest w sitemapie; dodać do menu na stronie głównej i w stopce) → hub.
- **Hub → modele (tabela z linkami)**, **hub → 6 poradników** (sekcje), **model → hub (okruszki ✓) + sąsiednie modele + 2 poradniki** (cena, JCB).
- **Poradniki → konkretny model** („zobacz Shanmon Fuji 388 od ręki”) i **do siebie** (cena ↔ chińska ↔ JCB ↔ leasing).
- **Anchory:** opisowe, z frazą, różne: „nowa koparko-ładowarka Shanmon Fuji 388”, „koparko-ładowarki na sprzedaż”, „alternatywa dla JCB 3CX”, „leasing koparko-ładowarki”. Bez „kliknij tutaj”.
- **Ze sklepu/strony głównej:** baner „Koparko-ładowarka od ręki – Rzeszów” → hub (nie mieszać z leżakami – brief: osobny produkt).
- **Z zewnątrz:** ogłoszenia OLX/Otomoto, wizytówka Google, posty FB/IG/TikTok (opis z linkiem) → hub lub 388.
- **Linki z innych stron do wykupienia/pozyskania (P3):** katalogi branżowe (maszyny budowlane, leasing), lokalne media (Rzeszów/Podkarpacie), współprace – lista kandydatów po dostępie do narzędzia linków (Ahrefs nie podpięte).

## 4. Dane strukturalne (JSON-LD) – gotowe do wklejenia przez sesję „Strona FUDALI”
Wymaga: wtyczki SEO (Rank Math/Yoast – **sprawdzić, co jest zainstalowane; strona pokazuje tylko BreadcrumbList**) albo bloku HTML w Elementorze. Wartości w `{…}` do uzupełnienia – **nie zgadywać**.

**Product – tylko strona 388 (z ceną):**
```json
{"@context":"https://schema.org","@type":"Product",
 "name":"Koparko-ładowarka Shanmon Fuji 388 (2026)",
 "brand":{"@type":"Brand","name":"Shanmon"},"model":"Fuji 388",
 "description":"Nowa koparko-ładowarka Shanmon Fuji 388, rok produkcji 2026, od ręki w Rzeszowie. Gwarancja 12 mies., leasing, transport.",
 "image":["{URL zdjęcia 1}","{URL zdjęcia 2}"],
 "offers":{"@type":"Offer","priceCurrency":"PLN","price":"250000",
  "priceSpecification":{"@type":"PriceSpecification","price":"250000","priceCurrency":"PLN","valueAddedTaxIncluded":false},
  "availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition",
  "url":"https://www.fudali.com.pl/maszyny-budowlane/shanmon-fuji-388/",
  "seller":{"@type":"Organization","name":"FUDALI Sp. z o.o."}}}
```
⚠️ `itemCondition: NewCondition` tylko jeśli Pablo potwierdzi „nowa” (Otomoto pokazuje „Używany / 5 mth”; decyzja Pablo 06.11: fabrycznie nowa – patrz `koparka/ceny.md`).
**Product – pozostałe modele:** jak wyżej, **bez** `offers.price` (zamiast tego `"availability":"https://schema.org/PreOrder"`), parametry w `additionalProperty` (moc kW, masa kg).
**LocalBusiness / Organization (stopka lub strona maszyn):**
```json
{"@context":"https://schema.org","@type":"LocalBusiness","name":"FUDALI Sp. z o.o. – maszyny budowlane",
 "url":"https://www.fudali.com.pl/maszyny-budowlane/","telephone":"{NAP – numer maszyn}","email":"biuro@fudali.com.pl",
 "address":{"@type":"PostalAddress","streetAddress":"{ulica – Rzeszów}","addressLocality":"Rzeszów","postalCode":"{kod}","addressCountry":"PL"},
 "areaServed":{"@type":"Country","name":"Polska"},
 "openingHours":"{godziny – od Pablo}"}
```
**FAQPage:** hub i modele – 4–6 pytań z odpowiedziami identycznymi z widoczną treścią strony (pytania z pkt 2.1). Uwaga: Google rzadko pokazuje rozwijane FAQ w wynikach, ale schema pomaga w wyszukiwarkach AI i porządkuje treść – priorytet P2.
**VideoObject:** gdy będą filmy z pracy maszyny. **BreadcrumbList:** jest ✓ (sprawdzić, że obejmuje hub → model).

## 5. NAP i Google Business Profile (lokalnie: Rzeszów)
- **NAP (nazwa–adres–telefon) musi być identyczny** na stronie, w wizytówce, w ogłoszeniach OLX/Otomoto i katalogach. Dziś: `/kontakt/` = **+48 667 666 370**, brief maszyn = **791 589 997**. **Decyzja Pablo:** który numer jest „maszyny/sprzedaż i serwis Rzeszów”? Ten numer na stronach maszyn + wizytówka; drugi zostaje ogólny (Głogów Małopolski). Adres w Rzeszowie (miejsce oględzin) – podać dokładny, jeśli ma być w wizytówce (Google wymaga adresu, pod którym realnie obsługujemy klientów; w przeciwnym razie „firma bez lokalu, obsługa w terminie – obszar działania”).
- **Wizytówka Google (Profil Firmy) – checklista** (wymaga dostępu od Pablo): 1) **Osobna wizytówka „FUDALI – maszyny budowlane, Rzeszów”** (jeśli adres w Rzeszowie jest spełnia zasady) albo kategoria dodatkowa w istniejącej; 2) **Kategoria główna: dealer/dostawca maszyn budowlanych (angielskie odpowiedniki: „Construction equipment supplier”, „Heavy equipment dealer”) – dobrać najbliższą polską nazwę w panelu, bez „dealer JCB”**; 3) opis (750 zn.) z frazami: koparko-ładowarki, Shanmon, od ręki, leasing, serwis, dostawa; 4) zdjęcia/filmy maszyny z placu (10 zdjęć z biblioteki), logo; 5) sekcja **Produkty** (388 z ceną netto) ; 6) **Posty** raz w tygodniu (nowości, film, Q&A); 7) **Pytania i odpowiedzi** (3–5 wstępnych); 8) **opinie** – prośba do pierwszych klientów o opinię (to realna przewaga: konkurenci prawie nie mają opinii – Mietek); 9) link do hub `/maszyny-budowlane/`, tag UTM `?utm_source=gbp`.
- Wpisy w katalogach lokalnych (Panorama Firm, Pkt.pl, Oferteo) z tym samym NAP – P3 (Panorama blokuje automaty – ręcznie).

## 6. Harmonogram (priorytety)
| Termin | Co | Kto |
|---|---|---|
| **P1 – do 5.12** | (1) Hub: nowy title/meta, sekcje, tabela modeli, FAQ (2.1); (2) strona 388: title, FAQ, schema Product; (3) `nowa-koparko-ladowarka-cena`, `alternatywa-dla-jcb-3cx`, `chinska-…` (treści Ola → Kuba → Bartek); (4) NAP – decyzja Pablo; (5) ogłoszenia OLX/Otomoto – frazy z mapy (C/D) + link do hub | Strona FUDALI / Ola / Marek / Pablo |
| **P2 – do 24.12** | podstrony 7 modeli + WZ30-25 + `shanmon`; `leasing`, `gwarancja-i-serwis`, `dostawa-…`; schema LocalBusiness/FAQ; wizytówka Google (po dostępie); pierwsze opinie | Strona FUDALI / Ola / Marek / Pablo |
| **P3 – styczeń–luty (przed sezonem, szczyt marzec)** | poradniki informacyjne (G), porównania CASE/NH, linki zewnętrzne, optymalizacja po danych z Search Console, rozszerzenie FAQ | Ola / Bartek |
| **Co tydzień (pon)** | Trends maszyny (nowa grupa w `seo/trendy-grupy.json`), pozycje TOP 20 (po Search Console), raport w `seo/` | Bartek / Kuba |

## 7. Potrzebne decyzje / dostępy (zbiorczo – dla Klaudiusza)
1. **Który telefon jest numerem maszyn** (667 666 370 czy 791 589 997) i **adres w Rzeszowie** do wizytówki.
2. **Którą wersją jest egzemplarz na sprzedaż** (388 vs 388T – różnica danych katalog/ogłoszenie, pkt 0).
3. Dostępy: **Search Console, Google Business Profile, Google Ads** (już w prośbie Klaudiusza) – bez Search Console nie zmierzymy pozycji.
4. Zgoda na edycję strony: kto wprowadza zmiany (sesja „Strona FUDALI” przez konektor WPVibe/WordPress.com – potwierdzić) i **tak Pablo** na publikację nowych podstron.
5. Marek: ceny/terminy transportu do województw, rata leasingu (jeśli dostępna), wersje silników w ofercie, CE/Stage V per model.
6. Pablo: czy linia to „Shanmon Fuji” dla wszystkich modeli (slugi, tytuły).
