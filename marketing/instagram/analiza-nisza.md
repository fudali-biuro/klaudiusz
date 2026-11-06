# 📸 Instagram – analiza niszy (Etap 1) – wersja bez scrapera (Mietek, 06.11.2026)

**Uczciwie o danych:** Apify (scraper) jest zablokowany do 3.12 (wyczerpany darmowy limit), a Instagram sam zwraca błąd 429. Ta wersja opiera się na:
- 📊 **DANE:** posty 4 obserwowanych kont z naszego monitoringu (`monitoring/stan/posty-30dni.json`, 14 postów z ostatnich tygodni; stan 06.11).
- 🔎 **WYSZUKIWARKA:** przykładowe konta i zalecenia z artykułów (źródła niskiej wiarygodności – blogi, firmy narzędziowe; kierunek ważniejszy niż liczby).
- 👁️ **OBSERWACJA:** moje wnioski z opisów i wcześniejszych analiz klatek (`monitoring/social/`).
**Czego tu NIE ma:** prawdziwego TOP 10 postów niszy wg komentarzy/zapisów, danych o stories i wyróżnionych relacjach, kont zagranicznych z liczbami. Uzupełnię po odblokowaniu Apify (plan na dole).

## 1. Co pokazują dane z naszych 4 kont (📊)
| Konto | Postów w próbce | Formaty | Polubienia (zakres) | Komentarze | Wyświetlenia filmów |
|---|---|---|---|---|---|
| @domkisauny | 7 | 5 reelów, 2 karuzele | 3–11 (reel), 6–9 (karuzela) | 0–1 | 657–1 299 |
| @sklepaltanka | 7 | 2 reele, 3 karuzele, 2 zdjęcia | 1–21 | 0–1 | 276–1 093 |
| @bogatecoeu, @vivengarden | brak postów w próbce (konta praktycznie nie publikują) | – | – | – | – |

**Wniosek:** konkurenci z naszej niszy mają **bardzo słabe zaangażowanie** (zwykle poniżej 25 polubień, prawie zero komentarzy; filmy poniżej 1,5 tys. wyświetleń). Kto na Instagramie pokaże prawdziwy warsztat i konkretną ofertę, ma tu łatwo być zauważony – ale nie ma w tej niszy gotowych wzorców „viralowych”.

## 2. Najlepsze posty w tej próbce (zamiast pełnego TOP 10 – tylko to, co jest w danych)
| # | Post | Dlaczego wyróżnia się | Co bierzemy |
|---|---|---|---|
| 1 | [Domki Sauny – reel „zimą własna sauna, zarezerwuj termin”](https://www.instagram.com/p/DfXhRsdiPbD/) (11 polub., 1 299 wyśw. – najwięcej w próbce) | prezenterka mówi do kamery, ujęcia z produkcji (wózek, montaż), napisy słowo po słowie, CTA przez termin realizacji | format „twarz + proces + napisy + termin”; u nas „ostatni termin zamówień na święta” |
| 2 | [Domki Sauny – nowa seria z „saunamistrzem”](https://www.instagram.com/p/DfIAAK5gBZQ/) (11 polub., 1 136 wyśw.) | **seria z postacią** (Łukasz) – powtarzalny bohater, wchodzi w nawyk | cykl z osobą z warsztatu (np. „Pablo/stolarz tłumaczy: jak rozpoznać dobre drewno”) |
| 3 | [Altanka – reel o basenach „praca trwa w najlepsze”](https://www.instagram.com/p/DfPNUOAkVdX/) (21 polub., 1 093 wyśw. – najwięcej polubień) | proces pracy na hali, sezonowy kontekst (jesień) | pokazywanie warsztatu i procesu, nie tylko produktu |
| 4 | [Domki Sauny – realizacja według wizji klienta](https://www.instagram.com/p/DfM0zynD4Nf/) | realizacja z indywidualnym projektem (2 strefy) | „realizacja u klienta” jako filar |
| 5 | [Altanka – „domek nie tylko na sprzęt”](https://www.instagram.com/p/DejMuCDFF6u/) (karuzela, 5 polub.) | nietypowe zastosowanie produktu = ciekawostka | karuzela „5 sposobów na…” (np. leżak/drewutnia w nowej roli) |
Pozostałych pozycji do 10 nie da się uczciwie wskazać z tej próbki.

## 3. Haczyki i wołanie do zakupu (👁️ + 📊)
- **Haczyki, które widzę:** pytanie („Kto chciałby prysznic w swojej saunie?”), sezonowość („zimą”, „jesień”), nowa seria, „zamów z terminem”, realizacja „od A do Z”.
- **Wołanie do zakupu:** prawie wszyscy kończą kontaktem w opisie (mail/telefon) lub „odwiedź sklep”. Rzadkie: konkretny termin, konkretna cena, „napisz w wiadomości”. Altanka w poście o Black Friday nie podała żadnej ceny.
- **Hashtagi:** rozbudowane, ogólne (#blackfriday2026 #promocja #domkiogrodowe); brak niszowych i brak społeczności.
- **Stories i wyróżnione:** NIE zweryfikowano (scraper ich nie zbierał, a Instagram jest zablokowany). Do ręcznego sprawdzenia: czy mają wyróżnione „Realizacje”, „Opinie”, „Zamów”.

## 4. Przykłady spoza naszego rynku (🔎 – tylko wskazówki, liczby z wyszukiwarki nieweryfikowane)
- [@fernwehwoodworking](https://www.instagram.com/fernwehwoodworking/) (ok. 149 tys.; wg artykułu mocny „proces”: przed/w trakcie/po) – wzór: dokumentowanie procesu. Źródło: [Fluxnote](https://fluxnote.io/guides/instagram-reels-woodworking-strategy), [Avvale](https://avvale.co.uk/pages/a-guide-to-social-media-for-woodworking-businesses).
- [@sentientfurniture](https://www.instagram.com/sentientfurniture/) (ok. 31 tys., Brooklyn) – pozycjonowanie „ręcznie robione meble”.
- [@zapachdrewnacom](https://www.instagram.com/zapachdrewnacom/) – mała pracownia z Gdańska (meble i oświetlenie z litego drewna); konto podane na ich [stronie](https://zapachdrewna-com.pages.dev/about); nie sprawdzałem treści.
- **Zalecenia z artykułów (jakość niska, kierunek):** reelsy = zasięg, karuzele = zaangażowanie i **zapisy**; karuzele edukacyjne (instrukcja, porównanie, przed/po, „jak wybrać”) są zapisywane częściej; pierwszy slajd decyduje. Wskaźniki liczbowe w źródłach się wykluczają – nie opieram na nich decyzji. [DEV Community](https://dev.to/wedgemethoddev/instagram-carousel-ideas-that-actually-get-saves-in-2026-5a97), [Storrito](https://storrito.com/resources/how-instagram-carousels-beat-reels-for-engagement-in-2026-and-when-to-use-each/).

## 5. Co z tego bierzemy dla FUDALI (rekomendacje)
1. **Seria z bohaterem** (osoba z warsztatu, powtarzalna nazwa serii) – tylko Domki Sauny to robią, a z wynikiem powyżej średniej ich konta.
2. **Reel 15–25 s „proces”**: od deski do gotowego leżaka (cięcie, szlifowanie, olejowanie, pakowanie paczki), napisy słowo po słowie.
3. **Karuzele edukacyjne na zapisy**: „Jak rozpoznać dobre drewno”, „Jak olejować leżak”, „5 prezentów z drewna do 300 zł” – pierwszy slajd = haczyk.
4. **Konkretne CTA**: termin wysyłki przed świętami + „napisz w wiadomości” – konkurenci tego nie robią.
5. **Niszowe hashtagi**, nie #blackfriday i #promocja: #stolarstwo #meblezdrewna #prezentzdrewna #lezakogrodowy.
6. **Realizacje u klientów** jako osobny filar i wyróżnione relacje (wymaga zdjęć od klientów – zapytać Pabla).
7. Pomysł „wow”: porównanie siatki profilu z konkurencją (ich profile są wyraźnie niespójne, bez jednej marki) – spójna siatka sama w sobie wyróżnia.

## 6. Uzupełnienie po odblokowaniu Apify (koszt ok. 0,5–1 USD)
- 10–15 kont: powyższe 4 + @fernwehwoodworking, @sentientfurniture, @zapachdrewnacom + konta znalezione po hashtagach #stolarz #stolarstwo #meblezdrewna #meblenawymiar + polskie/zagraniczne marki drewniane i leżakowe (Ecofurn – oficjalnego IG nie znaleziono).
- Dla każdego 12–15 postów: format, komentarze, zapisy, haczyk, CTA, hashtagi; prawdziwy TOP 10 wg komentarzy i zapisów z linkami.
