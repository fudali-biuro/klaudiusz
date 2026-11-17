# Strona fudali.com.pl – zasady projektowania (styl Apple)

Narzędzie: `.claude/skills/apple-hig-designer/` (MIT, źródło: github.com/axiaoge2/apple-hig-designer).
Wybrane zamiast „apple-ui-skills": tamten wymusza niebieski kolor i czcionkę Inter, ma niespójne kontrasty i niejasną licencję.

## Zasady współpracy z Pablo (13.11.2026)
- Strona główna i sklep: **bez przebudowy**. Tylko małe zmiany, każda po wyraźnym OK Pablo.
- Poligon do prób i błędów: podstrona **„O firmie"** (mały ruch) – tam wolno projektować śmielej, Pablo ocenia na żywo.
- Przed większą zmianą (także poza „O firmie") – zapisana kopia elementu, który zmieniamy (Elementor `_elementor_data`).
- Pablo mówi, że kopie hostingu/ManageWP robią się same.

## Jak stosować HIG na tej stronie
- Biel i dużo przestrzeni, duże zdjęcia produktów, mało tekstu; hierarchia wagą i rozmiarem.
- Siatka 8 px, nagłówki 28–34 px, tekst 17 px, line-height 1,2–1,5.
- **Kolory marki FUDALI (zielone logo) zostają** – z HIG bierzemy układ, odstępy, typografię i kontrasty (WCAG AA), nie niebieski akcent.
- Efekty szkła/rozmycia tylko jeśli Pablo poprosi.
- Elementor: natywne widgety, bez wstawek HTML; wersje mobilne sprawdzać zawsze.

## Zrobione
- 13.11.2026: logo w nagłówku mobilnym (szablon Header, id 973) = zielone `LOGO-FUDALI-GREEN` (media id 1814).
- Czeka: ikona strony (potrzebny kwadrat min. 512×512 px od Pablo).
- 13.11.2026: **„O firmie" (id 1293) przebudowana NA ŻYWO** (polecenie Pablo: poligon do prób). Stara wersja = rewizja WordPress/Elementor id 2204 (do przywrócenia w historii zmian strony). Szkic 2200 usunięty.
- Kolory marki (z motywu): zieleń akcentowa #70B63F, jasna #B3E391; dla czytelności przyciski #437A24 (hover #2F5A18), nagłówki #2F4A1F, tekst #4A5742, jasne tła #F1F6EA. **Nie używamy czerni/szarości #1d1d1f** (Pablo: ma być inny kolor niż czarny). Czcionki motywu: Jost (nagłówki) i Heebo (tekst) – nie nadpisywać.
- Pablo: strona ma być oglądana pod adresem /o-firmie/?v=288404204e3d (parametr omija pamięć podręczną).
- 13.11.2026: „O firmie" – efekty: zdjęcie na całą szerokość z paralaksą (klasa `fudali-hero`), wjazd napisów i kafelków falą (animacje Elementora), zdjęcie „Znajdź rozwiązanie" odsłaniane żaluzją (klasa `fudali-shutter`; CSS w widżecie HTML na dole strony – usunąć go, żeby wyłączyć). WPCode nie jest zainstalowany, więc własny kod siedzi w stronie. Poprzednia wersja (bez efektów) = rewizja strony 1293 sprzed zapisu.
- 13.11.2026: **szkic sklepu na stronie roboczej id 2212** („O firmie – SZKIC SKLEPU", status draft, edycja: /wp-admin/post.php?post=2212&action=elementor): hero z „Kup teraz" (pulsujący) i „Zobacz sklep", pasek zaufania (tylko znane fakty: wysyłka gratis od 200 zł, PayU, kurier, telefon), kafelki kategorii (3 niepuste), polecane produkty (żywy widżet WooCommerce), „Kup to, co widzisz", stały przycisk „Sklep” na telefonie. Czeka na akceptację Pablo; potem przenieść na stronę główną (po OK).
- Ustalenia: „Cart" w nagłówku to tekst tylko dla czytników ekranu (niewidoczny), poprawka niepilna. Puste kategorie (Drewutnie, Drewno konstrukcyjne, Akcesoria domowe) nie pokazywać w kafelkach, dopóki nie mają produktów. Cena „od" potrzebna tylko gdy warianty mają różne ceny (leżak: jedna cena).
- Brakuje faktów od Pablo do paska zaufania: czas dostawy, zwroty, raty.

## Narzędzia projektowe (14.11.2026, z rolki „5 narzędzi dla Claude Code")
Zainstalowane w repozytorium (działają w każdej sesji):
- `.claude/skills/apple-hig-designer/` – zasady Apple HIG (od 13.11).
- `.claude/skills/taste-skill/` – „taste skill" (Leonxlnx, MIT): zasady anty-generycznego designu, treści i zdjęć. **Bez hooka i bez skryptów** (nie uruchamiamy cudzego kodu). Uwaga: napisany pod statyczny HTML – u nas strona jest w Elementorze, więc stosujemy zasady (układ, odstępy, kopia, zdjęcia), nie gotowe pliki.
- `.claude/skills/web-design-guidelines/` – lista kontrolna Vercel (czytelność, dostępność, UX); pobiera aktualne reguły z GitHuba przy użyciu.
- `strona/wzorce-design/*.DESIGN.md` – opisy systemów designu Nike, Shopify, Apple, Airbnb, Starbucks (VoltAgent/awesome-design-md, MIT) jako inspiracja układu sklepu.
- `strona/narzedzia/zrzut.cjs` – **Playwright**: zrzuty ekranu strony publicznej na komputerze i telefonie (`node strona/narzedzia/zrzut.cjs <adres> <folder>`). Dzięki temu sprawdzam wygląd na własne oczy po każdej zmianie. Szkice w panelu wymagają logowania, więc tych nie widzę.
- „Image to code": nie jest osobnym narzędziem – obraz → układ robię na bieżąco (rozumiem zrzuty); `zrzut.cjs` służy do porównania efektu z wzorem.
- 14.11.2026: szkic sklepu (strona robocza 2212) poprawiony wg nowych narzędzi (Vercel guidelines + wzorce Nike/Shopify): ruch tylko transform/opacity (pulsujący pierścień zamiast cienia), widoczny focus, cele dotyku ≥44 px, bezpieczny margines dolny na telefonie, `text-wrap: balance`, nierozdzielne spacje w cenach/telefonie, nagłówki bez przeskoku poziomów, mocniejszy kontrast napisu na zdjęciu (przyciemnienie 0,52 + delikatny cień tekstu), opisowe linki kategorii. Test podglądu: hasło na stronie nie przechodzi przez zaporę hostingu (403 dla mojego adresu) – szkiców nie da się obejrzeć automatem; stronę 2212 przywrócono do szkicu.
- 17.11.2026: kolory z rolki (diego.a.does): sage #9CAF88, off-white #F7F5EF, tomato #E8412C → u nas: tło #F7F5EF, sekcje #EEF2E8, ikony #7E9568, **czerwień tylko na przyciskach zakupu (#D9381E, hover #B82E17)**, przyciski drugorzędne = zielona obwódka (#3E5A2C). Sekcja „Polecane” → „Nowości w sklepie” (brak sprzedaży = brak „Bestsellerów”; przełączyć na bestsellery, gdy będą zamówienia).
- 17.11.2026: Pablo: sklep = zdjęcie nie jest dużym hero (usunięte), „Kup to, co widzisz” usunięte (dublowało produkty). Szkic strony kategorii: strona robocza **id 2219** („SZKIC – strona kategorii (Meble ogrodowe)”): nagłówek + opis, pastylki kategorii (zamiast bocznych filtrów), duże karty produktów, pasek zaufania, „Zobacz też”. Obecna strona kategorii ma niedziałające/puste filtry (Kolor, Długość, Szerokość) i płaską listę kategorii – do zamiany po OK Pablo (szablon Elementora 929 „Sklep, archiwa, kategorie”). W sklepie widać „Zapłać później” (PayU) – do potwierdzenia z Pablo.
- 17.11.2026 (Pablo: „allow auto”): **szablon sklepu/kategorii (Elementor 929 „Sklep, archiwa, kategorie”) przebudowany NA ŻYWO** – dotyczy /sklep/ i wszystkich kategorii: nagłówek (tytuł + opis kategorii), pastylki kategorii z automatycznym zaznaczeniem aktywnej (JS po adresie), karty produktów w nowym stylu (czerwony przycisk zakupu), „Zobacz też” (inne kategorie; aktualna chowa się sama), pasek zaufania NA DOLE nad stopką. Stary układ (baner, boczne filtry) nie został usunięty – tylko ukryty (hide_desktop/tablet/mobile) w szablonie 929: aby cofnąć, usuń te klucze z sekcji 684dfd0b i kolumny 333de552 i ukryj nowe kontenery e1000001…e9000001. Widżet „Zapłać później” (PayU) ostylowany na zielono. Zrzuty kontrolne zrobione Playwrightem.
- Inspiracja Bonami (bonami.pl): pasek promocji nad nagłówkiem, nawigacja „Kategorie / Pomieszczenia”, kafelki popularnych kategorii, przyciski „Do koszyka” przy produktach, moduły (Nowości, Oferty), stopka z ikonami płatności, poradniki zakupowe.
