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
