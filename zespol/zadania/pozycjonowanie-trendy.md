---
nazwa: "🧭 Bartek – trendy tygodnia (pon 7:17)"
cron: "CRON_TZ=Europe/Warsaw 17 7 * * 1"
---
# Trendy tygodnia (Google Trends) – dla planu marketingu Oli

1. `python3 scripts/status.py pozycjonowanie pracuje "Trendy tygodnia"`.
2. Przeczytaj swoją kartę, ostatnie `seo/trendy/*.md` i ostatnie podsumowanie z `slowa-kluczowe/podsumowania/`.
3. `python3 scripts/seo/trendy.py` (Google Trends przez Apify, grupy w `seo/trendy-grupy.json`).
4. Zapisz `seo/trendy/RRRR-MM-DD.md`: co rośnie / spada (PL i DE), sezonowość, TOP 3 frazy na ten tydzień, konkretne rekomendacje dla Oli (który produkt promować) i dla strony (jaki tekst/poradnik).
5. Zapis na main, `python3 scripts/status.py pozycjonowanie gotowe "Trendy DD.MM: <1 zdanie>"`.
6. Przekaż Oli (send_message do jej sesji z zespol/sesje.json): „🧭 Trendy gotowe: seo/trendy/RRRR-MM-DD.md – TOP 3: …” – Ola planuje tydzień o 7:47. Meldunek do Klaudiusza w 1 zdaniu.
