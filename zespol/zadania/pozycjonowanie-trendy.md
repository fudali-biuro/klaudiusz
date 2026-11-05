---
nazwa: "Trendy tygodnia (Google Trends)"
kiedy: "rano pon"
---
# Trendy tygodnia (Google Trends) – dla planu marketingu Oli

1. `python3 scripts/status.py pozycjonowanie pracuje "Trendy tygodnia"`.
2. Przeczytaj swoją kartę, ostatnie `seo/trendy/*.md` i ostatnie podsumowanie z `slowa-kluczowe/podsumowania/`.
3. `python3 scripts/seo/trendy.py` (Google Trends przez Apify, grupy w `seo/trendy-grupy.json`).
4. Zapisz `seo/trendy/RRRR-MM-DD.md`: co rośnie / spada (PL i DE), sezonowość, TOP 3 frazy na ten tydzień, konkretne rekomendacje dla Oli (który produkt promować) i dla strony (jaki tekst/poradnik).
5. Zapis na main, `python3 scripts/status.py pozycjonowanie gotowe "Trendy DD.MM: <1 zdanie>"`.
6. Ola planuje tydzień na swojej porannej zmianie (kilkanaście minut po Tobie) i sama czyta `seo/trendy/RRRR-MM-DD.md` – nie musisz do niej pisać. Meldunek do Klaudiusza tylko, gdy coś wymaga jego decyzji.
