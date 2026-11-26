# Podłączenie Google Search Console – bezpiecznie, tylko do odczytu (wg zaleceń Pablo, 26.11.2026)

Cel: zespół widzi prawdziwe pozycje i kliknięcia fudali.com.pl, bez pośredników. Dane idą prosto z Google do naszego środowiska.
Dostęp **tylko do odczytu** (zakres `webmasters.readonly`, w Search Console uprawnienie „Ograniczone”).

## Kroki dla Pablo (ok. 10 minut, w przeglądarce, na koncie biuro@fudali.com.pl)
1. https://console.cloud.google.com → „Nowy projekt” → nazwa `fudali-seo` → Utwórz.
2. „Interfejsy API i usługi” → „Włącz interfejsy API” → wyszukaj **Google Search Console API** → Włącz.
3. „Konta usługi” → „Utwórz konto usługi” → nazwa `fudali-seo-odczyt` → bez nadawania ról → Gotowe.
4. Wejdź w to konto → „Klucze” → „Dodaj klucz” → JSON → plik pobierze się na komputer.
5. https://search.google.com/search-console → właściwość fudali.com.pl (jeśli jej nie ma – dodać i zweryfikować domenę) →
   Ustawienia → Użytkownicy i uprawnienia → Dodaj użytkownika: adres konta usługi (kończy się na `@fudali-seo.iam.gserviceaccount.com`),
   uprawnienie **Ograniczone**.
6. Klucz JSON: NIE wklejać do czatu. Wkleić w ustawieniach środowiska (menu środowiska → Edit → zmienne środowiskowe) jako
   `GSC_KEY_B64` = zawartość pliku zakodowana base64 (Klaudiusz poda gotową komendę), albo przez okno „sekret” w sesji.
7. Klaudiusz/Kuba robią test (lista fraz i pozycji z ostatnich 28 dni) i dopisują wiersz w tabeli narzędzi w AGENTS.md.

Po stronie zespołu: skrypt `scripts/seo/gsc.py` (do napisania po otrzymaniu klucza) – codziennie pobiera pozycje do `seo/pozycje/historia.csv`.
Tak samo później: **Google Business Profile** (wizytówka w Mapach, adres Rzeszów) i **Google Ads** (Planer słów kluczowych – realne wolumeny).

## Stan (26.11.2026)
- ✅ Własność fudali.com.pl zweryfikowana (tag HTML). Tag siedzi w Elementor → Custom Code, wpis **2299** „Google Search Console – weryfikacja”
  (`_elementor_code` + warunek `include/general` także w opcji `elementor_pro_theme_builder_conditions`). **NIE USUWAĆ** – inaczej weryfikacja przepadnie.
- ⏳ Pablo: dodać konto usługi (Ograniczone) + klucz jako `GSC_KEY_B64` w ustawieniach środowiska.
