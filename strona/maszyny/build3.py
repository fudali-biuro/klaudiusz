"""Generator wszystkich podstron „Maszyny budowlane” (26.11.2026).
Uruchom: python3 build3.py   -> pages/*.json (treść do save-page) + pages/*.html (podgląd)
Zdjęcia: adresy w media.json (po wgraniu na stronę).
"""
import json, re, os, sys
import markdown

BASE = 'https://www.fudali.com.pl'
TEL, TELH, MAIL = '791 589 997', 'tel:+48791589997', 'biuro@fudali.com.pl'
HUB = '/maszyny-budowlane/'
MEDIA = json.load(open('media.json')) if os.path.exists('media.json') else {}
LOCAL = len(sys.argv) > 1 and sys.argv[1] == 'local'
CSS = open('fm.css').read() + open('fm3.css').read()
ROOT = os.path.abspath('../..')


def img(key):
    if LOCAL:
        m = {'koparko-ladowarki': 'marketing/zdjecia/maszyny/kategorie/koparko-ladowarki.jpg', 'ladowarki-kolowe': 'marketing/zdjecia/maszyny/kategorie/ladowarki-kolowe.jpg',
             'ladowarki-teleskopowe': 'marketing/zdjecia/maszyny/kategorie/ladowarki-teleskopowe.jpg', 'koparki': 'marketing/zdjecia/maszyny/kategorie/koparki.jpg',
             'spycharki': 'marketing/zdjecia/maszyny/kategorie/spycharki.jpg', 'miniladowarki': 'marketing/zdjecia/maszyny/kategorie/miniladowarki.jpg',
             'ciagniki': 'marketing/zdjecia/maszyny/kategorie/ciagniki.jpg', 'minikoparka-1': 'marketing/zdjecia/maszyny/kategorie/minikoparka-1.jpg',
             'minikoparka-2': 'marketing/zdjecia/maszyny/kategorie/minikoparka-2.jpg', 'minikoparka-3': 'marketing/zdjecia/maszyny/kategorie/minikoparka-3.jpg'}
        if key in m:
            return ROOT + '/' + m[key]
    return MEDIA.get(key, '')


def ld(o):
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(',', ':')) + '</script>'


def bc(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + u} for i, (n, u) in enumerate(items)]}


ORG = {'@type': 'LocalBusiness', 'name': 'FUDALI', 'telephone': '+48791589997', 'email': MAIL, 'url': BASE + '/',
       'address': {'@type': 'PostalAddress', 'streetAddress': 'ul. św. Maksymiliana Kolbego 26', 'postalCode': '36-060', 'addressLocality': 'Głogów Małopolski', 'addressCountry': 'PL'},
       'areaServed': 'PL'}

call = f'<a class="btn b1 call" href="{TELH}">Zadzwoń: {TEL}</a>'
bar = f'<div class="bar"><a class="btn b1 call" href="{TELH}">Zadzwoń</a><a class="btn b3" href="#zapytanie">Zapytaj o cenę</a></div>'
SPEC = lambda items: '<ul class="spec">' + ''.join(f'<li><small>{a}</small><b>{b}</b></li>' for a, b in items) + '</ul>'


def crumb(items):
    out = '<div class="w crumb"><a href="/">Strona główna</a>'
    for n, u in items[:-1]:
        out += f' › <a href="{u}">{n}</a>'
    return out + f' › {items[-1][0]}</div>'


def inquiry(title, lead='Zostaw numer – oddzwonimy z ofertą i finansowaniem. Albo zadzwoń od razu:'):
    return (f'<section class="alt" id="zapytanie"><div class="w c"><span class="eyebrow">Zapytanie</span><h2>{title}</h2><p>{lead}</p>'
            f'<div class="cta cc">{call}</div></div></section>')


def mtable(cols, rows, caption):
    h = f'<div class="tw"><table class="mt"><caption>{caption}</caption><thead><tr>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr></thead><tbody>'
    for r in rows:
        h += '<tr>' + ''.join(f'<td>{c}</td>' if i else f'<th scope="row">{c}</th>' for i, c in enumerate(r)) + '</tr>'
    return h + '</tbody></table></div>'


def form(wid, name, subject, topics='Cena i dostępność\nFinansowanie (leasing, kredyt)\nTransport na budowę\nOględziny i jazda próbna'):
    return {'id': wid, 'elType': 'widget', 'widgetType': 'form', 'settings': {
        'form_name': name,
        'form_fields': [
            {'_id': 'fname', 'custom_id': 'name', 'field_type': 'text', 'field_label': 'Imię i nazwisko', 'placeholder': 'Imię i nazwisko', 'required': 'true', 'width': '50'},
            {'_id': 'ftel', 'custom_id': 'tel', 'field_type': 'tel', 'field_label': 'Telefon', 'placeholder': 'Telefon', 'required': 'true', 'width': '50'},
            {'_id': 'fmail', 'custom_id': 'email', 'field_type': 'email', 'field_label': 'E-mail', 'placeholder': 'E-mail', 'width': '50'},
            {'_id': 'ftopic', 'custom_id': 'temat', 'field_type': 'select', 'field_label': 'Interesuje mnie', 'field_options': topics, 'width': '50'},
            {'_id': 'fmsg', 'custom_id': 'wiadomosc', 'field_type': 'textarea', 'field_label': 'Wiadomość', 'placeholder': 'Model, lokalizacja budowy, pytania', 'width': '100', 'rows': '4'},
            {'_id': 'fhp', 'custom_id': 'hp', 'field_type': 'honeypot', 'field_label': 'Nie wypelniaj'},
            {'_id': 'fok', 'custom_id': 'zgoda', 'field_type': 'acceptance', 'field_label': 'Zgadzam się na kontakt w sprawie zapytania.', 'required': 'true', 'width': '100'}],
        'button_text': 'Wyślij zapytanie', 'button_width': '100', 'input_size': 'md', 'show_labels': 'true', 'mark_required': 'true',
        'submit_actions': ['email'], 'email_to': MAIL, 'email_subject': f'Zapytanie – {subject} (strona)', 'email_from_name': '[field id="name"]',
        'email_content': '[all-fields]', 'email_content_type': 'html',
        'success_message': 'Dziękujemy! Oddzwonimy najszybciej, jak to możliwe.', 'error_message': 'Coś poszło nie tak. Zadzwoń: 791 589 997.',
        'button_background_color': '#F5B000', 'button_text_color': '#111111', 'label_color': '#FFFFFF'}}


def page_data(prefix, parts, form_after=0, form_name='Zapytanie', subject='maszyny', topics=None):
    """parts = lista html; formularz wstawiany po parts[form_after] (None = bez formularza)."""
    els = []
    n = 0
    for i, h in enumerate(parts):
        n += 1
        els.append({'id': f'{prefix}{n:02d}000a', 'elType': 'widget', 'widgetType': 'html', 'settings': {'html': h}})
        if form_after is not None and i == form_after:
            n += 1
            cont = {'id': f'{prefix}{n:02d}000b', 'elType': 'container', 'settings': {
                'container_type': 'flex', 'flex_direction': 'column', 'content_width': 'boxed', 'boxed_width': {'unit': 'px', 'size': 820},
                'background_background': 'classic', 'background_color': '#151515', 'padding': {'unit': 'px', 'top': 0, 'right': 20, 'bottom': 60, 'left': 20, 'isLinked': False}},
                'elements': [form(f'{prefix}{n:02d}000c', form_name, subject, topics) if topics else form(f'{prefix}{n:02d}000c', form_name, subject)]}
            els.append(cont)
    return [{'id': f'{prefix}root001', 'elType': 'container', 'settings': {
        'container_type': 'flex', 'flex_direction': 'column', 'content_width': 'full', 'flex_gap': {'size': 0, 'unit': 'px', 'column': '0', 'row': '0', 'isLinked': True},
        'padding': {'unit': 'px', 'top': 0, 'right': 0, 'bottom': 0, 'left': 0, 'isLinked': True}}, 'elements': els}]


def mini(h):
    return re.sub(r'>\s+<', '><', h)


def wrap(h):
    return '<div class="fm">' + h + '</div>'


FAQ = [
    ('Ile kosztuje nowa koparko-ładowarka?', 'W ogłoszeniach z listopada 2026 nowe maszyny kosztują od ok. 140 do ponad 460 tys. zł netto, zależnie od marki i klasy. Nasza Shanmon Fuji 388: 250 000 zł netto (307 500 zł brutto). <a href="/maszyny-budowlane/nowa-koparko-ladowarka-cena/">Zobacz porównanie cen</a>.'),
    ('Koparko-ładowarka cena netto czy brutto?', 'Ceny maszyn podaje się zwykle netto (bez 23% VAT). 250 000 zł netto to 307 500 zł brutto.'),
    ('Czy chińska koparko-ładowarka jest dobra?', 'To zależy od sprzedawcy: ważne są gwarancja, serwis, części i dokumenty. U nas: gwarancja 12 mies. na silnik, skrzynię i most, całodobowa infolinia serwisowa, serwis z dojazdem w całej Polsce, pomoc w częściach. <a href="/maszyny-budowlane/chinska-koparko-ladowarka-czy-warto/">Poradnik</a>.'),
    ('Czy chińska koparko-ładowarka ma serwis w Polsce?', 'U nas tak: serwis z dojazdem w całej Polsce, całodobowa infolinia serwisowa i pomoc w częściach (płatny serwis).'),
    ('Czy FUDALI sprzedaje JCB lub CAT?', 'Nie. Sprzedajemy koparko-ładowarki Shanmon. Marki JCB, CAT i Case wymieniamy wyłącznie w porównaniach.'),
    ('Czy koparko-ładowarka jest od ręki? Gdzie można ją obejrzeć?', 'Shanmon Fuji 388: tak, 2 sztuki w Rzeszowie; oględziny i jazda próbna po telefonicznym umówieniu. Pozostałe modele – na zamówienie, zapytaj o ofertę.'),
    ('Czy koparko-ładowarkę można kupić w leasingu?', 'Tak: leasing operacyjny i finansowy dla firm, kredyty firmowe i prywatne, pomagamy w formalnościach. <a href="/maszyny-budowlane/leasing-koparko-ladowarki/">Leasing krok po kroku</a>.'),
    ('Czy mogę odliczyć VAT?', 'Cena 250 000 zł to netto; możliwość odliczenia VAT dotyczy czynnych podatników VAT, szczegóły omów z księgowym.'),
    ('Jak głęboko kopie ta maszyna?', 'Shanmon Fuji 388: do ok. 5,5 m (4,1 m bez wysuwu ramienia teleskopowego).'),
    ('Czy koparko-ładowarka ma napęd 4x4 i jakie wyposażenie?', 'Shanmon Fuji 388: napęd 4x4 (z przełączaniem na 2WD), łyżka przednia 6w1, szybkozłącza (przód i tył), podpory H z przesuwem bocznym, sterowanie joystickami, kabina ROPS/FOPS z klimatyzacją, kamera cofania, oświetlenie LED.'),
    ('Jaka jest gwarancja i serwis?', '12 mies. na silnik, skrzynię i most; całodobowa infolinia serwisowa; płatny serwis z dojazdem w całej Polsce; filtry i narzędzia do 500 mth do ustalenia przy zakupie.'),
    ('Czy dostarczacie maszynę?', 'Oględziny i odbiór w Rzeszowie po umówieniu. Transport na zapytanie, wycenimy dostawę.'),
    ('Czy sprzedajecie też inne maszyny budowlane?', 'Tak, na zamówienie, prosto z fabryki: minikoparki, ładowarki kołowe i teleskopowe, koparki gąsienicowe, spycharki, miniładowarki i ciągniki – zapytaj o ofertę.'),
    ('Jak się skontaktować?', f'<a href="{TELH}"><b>{TEL}</b></a> (Rzeszów – sprzedaż i serwis) · <a href="mailto:{MAIL}">{MAIL}</a>'),
]


def faq_html(qs):
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in qs)


def faq_ld(qs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', a)}} for q, a in qs]}


# ---------------------------------------------------------------- Koparko-ładowarki (modele)
KL = [  # model, masa, łyżka, udźwig, moc, rozstaw, wymiary, opis
    ('377', '8 410 kg', '1,0 / 0,3 m³', '2 500 kg', '77,3 kW', '2 280 mm', '6300×2340×3813 mm', 'Napęd 4WD, przekładnia PowerShift 4+4, rama ze stali manganowej.', 'Koparko-ladowarka-377.jpg'),
    ('388', '8 455 kg', '1,0 / 0,3 m³', '2 500 kg', '82 kW', '2 280 mm', '6300×2340×3813 mm', 'Zintegrowana rama, przesuw boczny ramienia, 8-punktowa kinematyka ładowarki.', 'Koparko-ladowarka-388.jpg'),
    ('388-II', '8 755 kg', '1,0 / 0,3 m³', '2 500 kg', '82 kW', '2 280 mm', '6375×2340×3580 mm', 'Kabina FOPS/ROPS, hydrauliczny przesuw boczny, opcja stabilizacji jazdy.', 'Koparko-ladowarka-388-II.jpg'),
    ('388T', '8 755 kg', '1,0 / 0,3 m³', '2 500 kg', '82 kW', '2 280 mm', '6375×2340×3580 mm', 'Wersja z ramieniem teleskopowym (głębokość kopania do 5,5 m wg katalogu), układ hydrauliczny 25 MPa.', 'Koparko-ladowarka-388T.jpg'),
    ('388H', '9 815 kg', '1,2 / 0,3 m³', '2 500 kg', '82 kW', '2 288 mm', '6232×2490×3714 mm', 'Hydraulika Load Sensing, trzy tryby skrętu 4WS, opcjonalny fotel obrotowy z joystickami.', 'Koparko-ladowarka-388H.jpg'),
    ('398H', '9 815 kg', '1,2 / 0,3 m³', '2 500 kg', '82 kW', '2 288 mm', '6232×2490×3714 mm', 'Mocna wersja do cięższych robót ziemnych, układ hydrauliczny 25 MPa.', 'Koparko-ladowarka-398H.jpg'),
    ('378H', '8 800 kg', '1,0 / 0,3 m³', '2 500 kg', '82 kW', '2 335 mm', '6312×2440×3780 mm', 'Napęd 4WD, przekładnia PowerShift 4+4, prędkość do 39 km/h.', 'Koparko-ladowarka-378H.jpg'),
    ('WZ30-25', '7 600 kg', '1,0 / 0,3 m³', '2 500 kg', '75 kW', '2 415 mm', '6174×2340×3813 mm', 'Przegub centralny – mały promień skrętu, napęd 4WD, zwrotna na ciasnych budowach.', 'Ladowarka-WZ30-25-z-osprzetem-koparkowym.jpg'),
]
UP = BASE + '/wp-content/uploads/2026/11/'


def kl_card(m):
    name = 'Ładowarka z osprzętem koparkowym WZ30-25' if m[0] == 'WZ30-25' else f'Koparko-ładowarka {m[0]}'
    return (f'<article class="card"><div class="ph"><img src="{UP + m[8]}" alt="{name}" loading="lazy"></div><div class="bd">'
            f'<span class="eyebrow" style="margin:0">Model {m[0]} · na zamówienie</span><h3>{name}</h3>'
            + SPEC([('Masa robocza', m[1]), ('Moc', m[4]), ('Łyżka ład./kop.', m[2]), ('Udźwig', m[3])])
            + f'<p style="font-size:.92rem;margin:0">{m[7]}</p><a class="btn b1" href="#zapytanie">Zapytaj o ofertę</a></div></article>')


def product_ld():
    return {'@context': 'https://schema.org', '@type': 'Product', 'name': 'Koparko-ładowarka Shanmon Fuji 388 (2026)',
            'image': [UP + 'Shanmon-Fuji-388-%E2%80%93-widok-z-przodu.jpg', UP + 'Shanmon-Fuji-388-%E2%80%93-lyzka-przednia-6w1.jpg', UP + 'Shanmon-Fuji-388-na-placu-w-Rzeszowie.jpg'],
            'description': 'Nowa koparko-ładowarka Shanmon Fuji 388, rok 2026, ok. 75 kW, napęd 4x4, ramię teleskopowe do ok. 5,5 m, łyżka 6w1, podpory H z przesuwem bocznym, joysticki, klimatyzacja. 2 sztuki od ręki w Rzeszowie, gwarancja 12 mies.',
            'brand': {'@type': 'Brand', 'name': 'Shanmon'}, 'model': 'Fuji 388', 'productionDate': '2026-07', 'itemCondition': 'https://schema.org/NewCondition', 'category': 'Koparko-ładowarki',
            'additionalProperty': [{'@type': 'PropertyValue', 'name': 'Moc silnika', 'value': 'ok. 75 kW'}, {'@type': 'PropertyValue', 'name': 'Masa robocza', 'value': '8200 kg'}, {'@type': 'PropertyValue', 'name': 'Maks. głębokość kopania', 'value': 'ok. 5,5 m'}],
            'offers': {'@type': 'Offer', 'url': BASE + '/maszyny-budowlane/shanmon-fuji-388/', 'priceCurrency': 'PLN', 'price': '250000', 'priceValidUntil': '2027-06-30', 'availability': 'https://schema.org/InStock', 'itemCondition': 'https://schema.org/NewCondition',
                       'seller': {'@type': 'Organization', 'name': 'FUDALI'}, 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': '250000', 'priceCurrency': 'PLN', 'valueAddedTaxIncluded': False}}}


TILES = [('Minikoparki', 'minikoparka-1', '/maszyny-budowlane/minikoparka/', 'Nowa minikoparka, 2 szt. od ręki'), ('Ładowarki kołowe', 'ladowarki-kolowe', '/maszyny-budowlane/ladowarki-kolowe/', 'Od 2 do 7,5 t udźwigu'),
         ('Ładowarki teleskopowe', 'ladowarki-teleskopowe', '/maszyny-budowlane/ladowarki-teleskopowe/', 'Wysokość podnoszenia do 18 m'), ('Koparki gąsienicowe', 'koparki', '/maszyny-budowlane/koparki/', 'Od 14 do 78 ton'),
         ('Spycharki', 'spycharki', '/maszyny-budowlane/spycharki/', 'Od 16,4 do 57 ton'), ('Miniładowarki', 'miniladowarki', '/maszyny-budowlane/miniladowarki/', 'Udźwig 850–1 200 kg'),
         ('Ciągniki kołowe', 'ciagniki', '/maszyny-budowlane/ciagniki-kolowe/', 'Od 191 do 294 kW')]


def tiles_html():
    h = '<section><div class="w"><span class="eyebrow">Cała oferta</span><h2>Maszyny budowlane na zamówienie – prosto z fabryki</h2><p class="lead">Poza koparko-ładowarkami zamawiamy dla klientów inne maszyny. Cenę i termin dostawy podajemy po zapytaniu.</p><div class="grid g3">'
    for t, k, u, d in TILES:
        if not img(k):
            continue
        h += f'<a class="tile" href="{u}"><div class="ph"><img src="{img(k)}" alt="{t}" loading="lazy"></div><div class="bd"><h3>{t}</h3><p>{d}</p><span class="more">Zobacz modele</span></div></a>'
    return h + '</div></div></section>'


def hub_parts():
    hero = (f'<section class="hero"><div class="w row"><div class="ht"><span class="eyebrow">Maszyny budowlane FUDALI</span><h1>Koparko-ładowarki na sprzedaż</h1>'
            f'<p>Nowe koparko-ładowarki od ręki w Rzeszowie i cała oferta maszyn budowlanych na zamówienie. 12 miesięcy gwarancji, leasing, transport na budowę i serwis w całej Polsce.</p>'
            f'<div class="cta">{call}<a class="btn b3" href="#zapytanie">Wyślij zapytanie</a></div></div>'
            f'<div class="hi"><img src="{UP}Shanmon-Fuji-388-%E2%80%93-widok-z-przodu.jpg" alt="Koparko-ładowarka Shanmon Fuji 388 – widok z przodu, łyżka 6w1" loading="eager"></div></div></section>')
    trust = ('<div class="trust"><div class="w"><ul><li><b>12 miesięcy</b>gwarancji producenta</li><li><b>Jazda próbna</b>na placu w Rzeszowie</li><li><b>Leasing i kredyt</b>pomoc w formalnościach</li><li><b>Transport</b>na Twoją budowę</li></ul></div></div>')
    feat = (f'<section id="oferta"><div class="w"><span class="eyebrow">Dostępna od ręki · 2 sztuki</span><h2>Shanmon Fuji 388 – nowa, 2026</h2><div class="feat"><div class="ph"><span class="tag">Od ręki · Rzeszów</span>'
            f'<img src="{UP}Shanmon-Fuji-388-na-placu-w-Rzeszowie.jpg" alt="Koparko-ładowarka Shanmon Fuji 388 na placu w Rzeszowie" loading="lazy"></div><div class="bd"><h3>Koparko-ładowarka Shanmon Fuji 388</h3>'
            + SPEC([('Stan', 'Nowa, rok 2026'), ('Dostępność', '2 sztuki od ręki'), ('Moc silnika', 'ok. 75 kW'), ('Masa robocza', '8 200 kg'), ('Napęd', '4x4'), ('Głębokość kopania', 'do ok. 5,5 m'), ('Łyżka przednia', '6w1, 2 200 mm'), ('Gwarancja', '12 miesięcy')])
            + '<div class="price">250 000 zł netto<small>307 500 zł brutto · sprzedaż na fakturę VAT, leasing dla firm</small></div>'
              f'<div class="cta"><a class="btn b1" href="/maszyny-budowlane/shanmon-fuji-388/">Szczegóły maszyny</a><a class="btn b2" href="{TELH}">Zadzwoń: {TEL}</a></div></div></div></div></section>')
    p1 = wrap(ld(bc([('Strona główna', '/'), ('Maszyny budowlane', HUB)])) + ld(product_ld()) + hero + trust + feat + inquiry('Zapytaj o maszynę'))
    cards = ''.join(kl_card(m) for m in KL)
    tbl = mtable(['Model', 'Masa robocza', 'Łyżka ład./kop.', 'Udźwig', 'Moc', 'Rozstaw osi', 'Wymiary'], [[m[0], m[1], m[2], m[3], m[4], m[5], m[6]] for m in KL],
                 'Koparko-ładowarki na zamówienie – parametry modeli')
    coll = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Maszyny budowlane – koparko-ładowarki na sprzedaż', 'url': BASE + HUB, 'mainEntity': {'@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n} for i, n in enumerate(['Koparko-ładowarka Shanmon Fuji 388'] + [f'Koparko-ładowarka {m[0]}' for m in KL] + [t[0] for t in TILES])]}}
    p2 = wrap(ld(faq_ld(FAQ)) + ld(coll)
              + '<section><div class="w"><span class="eyebrow">Koparko-ładowarki</span><h2>Pozostałe modele – na zamówienie, prosto z fabryki</h2><p class="lead">Cenę, termin dostawy i osprzęt podajemy po zapytaniu. Parametry mogą ulec zmianie bez powiadomienia.</p><div class="grid">' + cards + '</div>' + tbl + '</div></section>'
              + tiles_html()
              + '<section class="alt"><div class="w"><span class="eyebrow">Finansowanie i transport</span><h2>Kup maszynę bez zamrażania gotówki</h2><div class="two"><div class="box"><h3>Leasing i kredyt</h3><ul><li>leasing operacyjny i finansowy dla firm</li><li>kredyt dla firm i osób prywatnych</li><li>pomoc w formalnościach na miejscu</li><li>możliwość odliczenia VAT</li></ul></div><div class="box"><h3>Transport na budowę</h3><ul><li>pomagamy zorganizować dowóz pod wskazany adres</li><li>koszt wyceniamy indywidualnie</li><li>odbiór osobisty w Rzeszowie z jazdą próbną</li><li>serwis z dojazdem w całej Polsce</li></ul></div></div></div></section>'
              + '<section><div class="w"><span class="eyebrow">Poradniki</span><h2>Zanim kupisz koparko-ładowarkę</h2><div class="grid g3 gl">'
                '<a class="box lnk" href="/maszyny-budowlane/nowa-koparko-ladowarka-cena/"><h3>Ile kosztuje nowa koparko-ładowarka?</h3><p>Ceny z ogłoszeń (listopad 2026) i co wchodzi w cenę.</p></a>'
                '<a class="box lnk" href="/maszyny-budowlane/alternatywa-dla-jcb-3cx/"><h3>Alternatywa dla JCB 3CX</h3><p>Porównanie cen i tego, co sprawdzić przed zakupem.</p></a>'
                '<a class="box lnk" href="/maszyny-budowlane/chinska-koparko-ladowarka-czy-warto/"><h3>Chińska koparko-ładowarka – czy warto?</h3><p>Kiedy się opłaca i jak nie dać się nabrać.</p></a>'
                '<a class="box lnk" href="/maszyny-budowlane/leasing-koparko-ladowarki/"><h3>Leasing koparko-ładowarki</h3><p>Krok po kroku: jak sfinansować maszynę.</p></a></div></div></section>'
              + f'<section class="alt"><div class="w"><span class="eyebrow">Pytania i odpowiedzi</span><h2>Najczęstsze pytania o koparko-ładowarki</h2>{faq_html(FAQ)}</div></section>'
              + f'<section><div class="w c"><h2>Masz pytania? Zadzwoń.</h2><div class="cta cc">{call}<a class="btn b3" href="mailto:{MAIL}">{MAIL}</a></div></div></section>' + bar)
    return [mini(p1), mini(p2)]


# ---------------------------------------------------------------- Fuji 388
def fuji_parts():
    gal = [('Shanmon-Fuji-388-%E2%80%93-widok-z-przodu.jpg', 'Koparko-ładowarka Shanmon Fuji 388 – widok z przodu, kabina i ramię koparkowe'), ('Shanmon-Fuji-388-%E2%80%93-lyzka-przednia-6w1.jpg', 'Shanmon Fuji 388 – łyżka przednia 6w1 i ładowarka'),
           ('Shanmon-Fuji-388-na-placu-w-Rzeszowie.jpg', 'Koparko-ładowarka Shanmon Fuji 388 na placu w Rzeszowie'), ('Shanmon-Fuji-388-w-pracy-na-terenie.jpg', 'Shanmon Fuji 388 podczas pracy na nierównym terenie'),
           ('Shanmon-Fuji-388-%E2%80%93-ramie-teleskopowe-z-tylu.jpg', 'Shanmon Fuji 388 – ramię teleskopowe, głębokość kopania do ok. 5,5 m'), ('Shanmon-Fuji-388-%E2%80%93-widok-z-boku.jpg', 'Koparko-ładowarka Shanmon Fuji 388 – widok z boku')]
    thumbs = ''.join(f'<img src="{UP + f}" alt="{a}" class="{"on" if i == 0 else ""}" data-s="{UP + f}" loading="lazy">' for i, (f, a) in enumerate(gal))
    side = ('<aside class="side"><span class="tag in">Od ręki · Rzeszów · 2 sztuki</span><h1>Koparko-ładowarka Shanmon Fuji 388 – 2026</h1>'
            '<div class="price">250 000 zł netto<small>307 500 zł brutto · sprzedaż na fakturę VAT, leasing dla firm</small></div>'
            + SPEC([('Stan', 'Nowa, rok 2026'), ('Dostępność', '2 sztuki od ręki'), ('Moc', 'ok. 75 kW'), ('Masa', '8 200 kg'), ('Napęd', '4x4'), ('Kopanie', 'do ok. 5,5 m')])
            + f'{call}<a class="btn b2" href="#zapytanie">Zapytaj o finansowanie</a><a class="btn b2" href="#zapytanie">Umów oględziny i jazdę próbną</a></aside>')
    p1 = wrap(ld(product_ld()) + ld({'@context': 'https://schema.org', **ORG}) + ld(bc([('Strona główna', '/'), ('Maszyny budowlane', HUB), ('Koparko-ładowarka Shanmon Fuji 388', '/maszyny-budowlane/shanmon-fuji-388/')]))
              + crumb([('Maszyny budowlane', HUB), ('Shanmon Fuji 388', '')])
              + f'<section style="padding-top:20px"><div class="w det"><div class="gal"><div class="main"><img id="fmMain" src="{UP + gal[0][0]}" alt="{gal[0][1]}"></div><div class="thumbs">{thumbs}</div></div>{side}</div></section>'
              + inquiry('Zapytaj o Shanmon Fuji 388'))
    rows = [('Marka / model', 'Shanmon Fuji 388'), ('Stan', 'Nowa, rok produkcji 2026 (lipiec), pierwszy właściciel'), ('Dostępność', '2 sztuki od ręki, Rzeszów'), ('Silnik', 'ok. 75 kW, norma Euro V (wg dokumentów maszyny)'),
            ('Napęd', '4x4, przełączany na 2WD'), ('Masa robocza', '8 200 kg'), ('Ramię koparkowe', 'teleskopowe, głębokość kopania do ok. 5,5 m (4,1 m bez wysuwu)'), ('Łyżka tylna', '550 mm (w komplecie)'),
            ('Łyżka przednia', '6w1 z wypychaczem, hydraulicznie dzielona, szer. 2 200 mm, ok. 1,0 m³'), ('Udźwig ładowarki', '2 500 kg'), ('Wysokość wyładunku', 'do 3 200 mm'),
            ('Podpory', 'typu H z hydraulicznym przesuwem bocznym'), ('Sterowanie', 'joysticki (sterowanie pilotowe)'), ('Szybkozłącza', 'przód + hydrauliczne szybkozłącze tył'),
            ('Instalacja hydrauliczna', 'przewody do młota hydraulicznego (tył), zawór trójsekcyjny (przód)'), ('Kabina', 'ROPS/FOPS, klimatyzacja, radio'),
            ('Bezpieczeństwo', 'kamera cofania, alarm cofania, lampa ostrzegawcza, oświetlenie LED'), ('Rozruch zimą', 'podgrzewanie rozruchowe'), ('Opony', '14-17.5 (przód) / 19.5L-24 (tył)'),
            ('Gwarancja', '12 mies. – silnik, skrzynia biegów, most'), ('Sprzedaż', 'faktura VAT, leasing dla firm możliwy'), ('Lokalizacja', 'Rzeszów – oględziny i jazda próbna po umówieniu')]
    fq = [q for q in FAQ if any(k in q[0] for k in ('od ręki', 'napęd', 'głęboko', 'gwarancja', 'leasing', 'netto'))]
    p2 = wrap('<section class="alt"><div class="w two"><div><span class="eyebrow">Specyfikacja</span><h2>Dane techniczne</h2><table><tbody><tr><th class="tbh" colspan="2">Shanmon Fuji 388 – szczegóły maszyny</th></tr>'
              + ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in rows)
              + '</tbody></table><p class="note">Dane z dokumentów maszyny; parametry mogą ulec zmianie bez powiadomienia.</p></div><div><span class="eyebrow">Stan techniczny</span><h2>Gotowa do pracy od zaraz</h2><div class="box"><ul><li>maszyna nowa, rok 2026</li><li>weryfikacja techniczna przed wydaniem</li><li>jazda próbna i oględziny na placu w Rzeszowie</li><li>w zestawie filtry (paliwa, powietrza) i narzędzia – zakres do 500 mth do uzgodnienia przy zakupie</li></ul></div><div class="box" style="margin-top:18px"><h3>Osprzęt na zamówienie</h3><p style="margin:0">Łyżki kopiące 30/40/60 cm, łyżka skarpowa, młot hydrauliczny, zagęszczarka, świder.</p></div></div></div></section>'
              + '<section><div class="w two"><div class="box"><span class="eyebrow">Finansowanie</span><h3>Leasing i kredyt</h3><ul><li>leasing operacyjny i finansowy dla firm</li><li>kredyt dla firm i osób prywatnych</li><li>pomoc w formalnościach na miejscu</li></ul><p style="margin-top:12px"><a href="/maszyny-budowlane/leasing-koparko-ladowarki/">Leasing krok po kroku</a></p></div><div class="box"><span class="eyebrow">Transport</span><h3>Dowóz na Twoją budowę</h3><ul><li>pomagamy zorganizować transport pod wskazany adres</li><li>koszt wyceniamy indywidualnie</li><li>serwis z dojazdem w całej Polsce, infolinia 24/7</li></ul></div></div></section>'
              + f'<section class="alt"><div class="w"><h2>Pytania o tę maszynę</h2>{faq_html(fq)}<p style="margin-top:18px"><a href="/maszyny-budowlane/nowa-koparko-ladowarka-cena/">Ile kosztuje nowa koparko-ładowarka?</a> · <a href="/maszyny-budowlane/alternatywa-dla-jcb-3cx/">Alternatywa dla JCB 3CX</a> · <a href="/maszyny-budowlane/">Cała oferta maszyn</a></p></div></section>'
              + f'<section><div class="w c"><h2>Chcesz kupić? Zadzwoń.</h2><div class="cta cc">{call}<a class="btn b3" href="mailto:{MAIL}">{MAIL}</a></div></div></section>' + bar
              + "<script>(function(){var m=document.getElementById('fmMain');document.querySelectorAll('.fm .thumbs img').forEach(function(t){t.addEventListener('click',function(){m.src=t.getAttribute('data-s');m.alt=t.alt;document.querySelectorAll('.fm .thumbs img').forEach(function(x){x.classList.remove('on')});t.classList.add('on')})})})();</script>")
    return [mini(p1), mini(p2)]


# ---------------------------------------------------------------- Minikoparka
def mini_parts():
    thumbs = ''.join(f'<img src="{img(k)}" alt="{a}" class="{"on" if i == 0 else ""}" data-s="{img(k)}" loading="lazy">' for i, (k, a) in enumerate([
        ('minikoparka-1', 'Minikoparka z zamkniętą kabiną i gumowymi gąsienicami'), ('minikoparka-2', 'Minikoparka – widok z boku, ramię i łyżka'), ('minikoparka-3', 'Minikoparka – widok z tyłu'), ('minikoparka-4', 'Minikoparka – widok z przodu, łyżka i lemiesz'), ('minikoparka-5', 'Minikoparka – wnętrze kabiny, fotel i joysticki')]))
    side = ('<aside class="side"><span class="tag in">Nowa · 2 sztuki · prosto z fabryki</span><h1>Minikoparka na sprzedaż</h1><div class="price">134 990 zł netto<small>z dostawą do klienta · ok. 166 038 zł brutto</small></div>'
            + SPEC([('Stan', 'Nowa'), ('Dostępność', '2 sztuki'), ('Kabina', 'zamknięta, z ogrzewaniem'), ('Podwozie', 'gumowe gąsienice'), ('Lemiesz', 'tak'), ('OEM', 'własny kolor i logo na zamówienie')])
            + f'{call}<a class="btn b2" href="#zapytanie">Zapytaj o ofertę</a></aside>')
    pr = {'@context': 'https://schema.org', '@type': 'Product', 'name': 'Minikoparka nowa – prosto z fabryki', 'image': [img(k) for k in ('minikoparka-1', 'minikoparka-2', 'minikoparka-4')],
          'description': 'Nowa minikoparka z zamkniętą kabiną, oświetleniem LED, lemieszem, gumowymi gąsienicami i szybkozłączem. Dostępne 2 sztuki. Możliwość wykonania OEM (własny kolor i logo).',
          'itemCondition': 'https://schema.org/NewCondition', 'category': 'Minikoparki',
          'offers': {'@type': 'Offer', 'url': BASE + '/maszyny-budowlane/minikoparka/', 'priceCurrency': 'PLN', 'price': '134990', 'availability': 'https://schema.org/InStock', 'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@type': 'Organization', 'name': 'FUDALI'}, 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': '134990', 'priceCurrency': 'PLN', 'valueAddedTaxIncluded': False}}}
    p1 = wrap(ld(pr) + ld({'@context': 'https://schema.org', **ORG}) + ld(bc([('Strona główna', '/'), ('Maszyny budowlane', HUB), ('Minikoparka', '/maszyny-budowlane/minikoparka/')]))
              + crumb([('Maszyny budowlane', HUB), ('Minikoparka', '')])
              + f'<section style="padding-top:20px"><div class="w det"><div class="gal"><div class="main"><img id="fmMain" src="{img("minikoparka-1")}" alt="Minikoparka z zamkniętą kabiną i gumowymi gąsienicami"></div><div class="thumbs t5">{thumbs}</div></div>{side}</div></section>'
              + inquiry('Zapytaj o minikoparkę'))
    p2 = wrap('<section class="alt"><div class="w two"><div><span class="eyebrow">Wyposażenie</span><h2>Co widać na zdjęciach</h2><div class="box"><ul><li>zamknięta kabina z ogrzewaniem i wycieraczką</li><li>oświetlenie robocze LED</li><li>lemiesz</li><li>gumowe gąsienice</li><li>szybkozłącze i linia hydrauliczna do osprzętu</li><li>wysięgnik z przesuwem (offset)</li><li>sterowanie joystickami</li></ul></div><p class="note">Pełne parametry (masa, silnik, głębokość kopania) podajemy na zapytanie – skontaktuj się z nami.</p></div>'
              '<div><span class="eyebrow">Zamówienie</span><h2>Prosto z fabryki, możliwość OEM</h2><div class="box"><ul><li>cena 134 990 zł netto – z dostawą do klienta</li><li>2 sztuki dostępne od ręki</li><li>możliwość wykonania w Twoim kolorze i z Twoim logo (OEM)</li><li>pomoc w formalnościach, leasing dla firm</li><li>serwis z dojazdem, pomoc w częściach</li></ul></div></div></div></section>'
              + f'<section><div class="w c"><h2>Chcesz kupić minikoparkę? Zadzwoń.</h2><div class="cta cc">{call}<a class="btn b3" href="mailto:{MAIL}">{MAIL}</a></div><p style="margin-top:18px"><a href="/maszyny-budowlane/">Cała oferta maszyn budowlanych</a></p></div></section>' + bar
              + "<script>(function(){var m=document.getElementById('fmMain');document.querySelectorAll('.fm .thumbs img').forEach(function(t){t.addEventListener('click',function(){m.src=t.getAttribute('data-s');m.alt=t.alt;document.querySelectorAll('.fm .thumbs img').forEach(function(x){x.classList.remove('on')});t.classList.add('on')})})})();</script>")
    return [mini(p1), mini(p2)]


# ---------------------------------------------------------------- Kategorie
def cat_parts(slug, h1, eyebrow, lead, photo, alt, tables, text, faq):
    hero = (f'<section class="hero"><div class="w row"><div class="ht"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p>{lead}</p><div class="cta">{call}<a class="btn b3" href="#zapytanie">Wyślij zapytanie</a></div></div>'
            f'<div class="hi"><img src="{img(photo)}" alt="{alt}" loading="eager"></div></div></section>')
    sect = '<section><div class="w">' + ''.join(tables) + '<p class="note">Parametry wg broszury producenta; mogą ulec zmianie bez powiadomienia. Cenę, wersję i termin dostawy podajemy po zapytaniu.</p></div></section>'
    items = []
    for t in tables:
        for m in re.findall(r'<th scope="row">([^<]+)</th>', t):
            items.append({'@type': 'ListItem', 'position': len(items) + 1, 'name': f'{h1.split(" –")[0]} {m}'})
    p1 = wrap(ld(bc([('Strona główna', '/'), ('Maszyny budowlane', HUB), (h1.split(' –')[0], f'/maszyny-budowlane/{slug}/')])) + ld({'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': h1, 'url': f'{BASE}/maszyny-budowlane/{slug}/', 'mainEntity': {'@type': 'ItemList', 'itemListElement': items}})
              + crumb([('Maszyny budowlane', HUB), (h1.split(' –')[0], '')]) + hero + sect + inquiry('Zapytaj o ofertę'))
    p2 = wrap(ld(faq_ld(faq)) + f'<section class="alt"><div class="w"><span class="eyebrow">O ofercie</span><h2>{text[0]}</h2>{text[1]}</div></section>'
              + f'<section><div class="w"><h2>Pytania i odpowiedzi</h2>{faq_html(faq)}</div></section>'
              + f'<section class="alt"><div class="w c"><h2>Masz pytania? Zadzwoń.</h2><div class="cta cc">{call}<a class="btn b3" href="mailto:{MAIL}">{MAIL}</a></div><p style="margin-top:18px"><a href="/maszyny-budowlane/">Cała oferta maszyn budowlanych</a> · <a href="/maszyny-budowlane/leasing-koparko-ladowarki/">Leasing maszyn</a></p></div></section>' + bar)
    return [mini(p1), mini(p2)]


def faq_cat(what):
    return [(f'Czy {what} są dostępne od ręki?', 'Maszyny z tej kategorii zamawiamy na zlecenie, prosto z fabryki. Termin dostawy i cenę podajemy po zapytaniu.'),
            ('Czy można kupić na leasing?', 'Tak, dla firm: leasing operacyjny i finansowy oraz kredyt. Pomagamy w formalnościach. Szczegóły: <a href="/maszyny-budowlane/leasing-koparko-ladowarki/">leasing krok po kroku</a>.'),
            ('Jaka jest gwarancja i serwis?', 'Gwarancję, serwis i dostępność części ustalamy przy zamówieniu konkretnego modelu – zapytaj o warunki.'),
            ('Czy FUDALI jest dealerem JCB lub CAT?', 'Nie. Sprzedajemy maszyny Shanmon zamawiane prosto z fabryki.'),
            ('Jak zamówić?', f'Zadzwoń <a href="{TELH}"><b>{TEL}</b></a> lub napisz <a href="mailto:{MAIL}">{MAIL}</a> – podaj model i miejsce dostawy.')]


CATS = {}
CATS['ladowarki-kolowe'] = cat_parts('ladowarki-kolowe', 'Ładowarki kołowe – sprzedaż, modele i parametry', 'Ładowarki kołowe', 'Ładowarki kołowe od 2 do 7,5 tony udźwigu: modele 928G–978G, wersje z wysięgnikiem teleskopowym oraz z baterią (EV/HEV). Zamawiamy prosto z fabryki – zapytaj o cenę.', 'ladowarki-kolowe', 'Ładowarka kołowa podczas załadunku na placu budowy',
    [mtable(['Model', 'Masa robocza', 'Pojemność łyżki', 'Udźwig', 'Moc', 'Rozstaw osi / inne', 'Wymiary'], [
        ['928G', '5 700 kg', '1,0 m³', '2 000 kg', '81 kW', '2 550 mm', '6220×2200×3200 mm'], ['935G (z wysięgnikiem teleskopowym)', '9 000 kg', '1,5 m³', '3 000 kg', '92 kW', 'wysokość wyładunku 5 000 mm', '8000×2200×3200 mm'],
        ['936G', '10 275 kg', '1,8 m³', '3 000 kg', '92 kW', '2 740 mm', '7120×2350×3230 mm'], ['955G', '16 400 kg', '3,0 m³', '5 000 kg', '162 kW', '3 100 mm', '7845×2965×3450 mm'],
        ['956G', '16 950 kg', '3,3 m³', '5 000 kg', '162 kW', '3 250 mm', '8250×2880×3570 mm'], ['966G', '17 800 kg', '3,5 m³', '6 000 kg', '175 kW', '3 250 mm', '8400×3050×3470 mm'],
        ['967G', '19 500 kg', '4,0 m³', '6 500 kg', '175 kW', '3 400 mm', '8750×3100×3400 mm'], ['978G', '23 000 kg', '4,5 m³', '7 500 kg', '210 kW', '3 500 mm', '9500×3250×3400 mm']],
        'Ładowarki kołowe – modele 928G–978G'),
     mtable(['Model', 'Masa robocza', 'Pojemność łyżki', 'Udźwig', 'Pojemność baterii', 'Rozstaw osi', 'Wymiary'], [
        ['960EV', '18 500 kg', '3,5 m³', '5 800 kg', '350 kWh', '3 350 mm', '8800×2950×3500 mm'], ['970EV', '23 000 kg', '4,5 m³', '7 000 kg', '425 kWh', '3 500 mm', '9697×3244×3548 mm'],
        ['960HEV', '18 500 kg', '3,5 m³', '5 800 kg', '32,56 kWh', '3 250 mm', '8085×2965×3450 mm'], ['970HEV', '19 000 kg', '4,0 m³', '6 800 kg', '48,38 kWh', '3 450 mm', '8000×3200×3400 mm']],
        'Ładowarki kołowe z baterią – modele EV i HEV'),
     mtable(['Model', 'Masa robocza', 'Pojemność łyżki', 'Udźwig', 'Moc', 'Rozstaw osi', 'Wymiary'], [
        ['ZLJ20F', '5 500 kg', '1,0 m³', '2 000 kg', '88,2 kW', '2 450 mm', '5535×1880×1900 mm'], ['ZLJ28F', '5 720 kg', '1,0 m³', '2 000 kg', '88,2 kW', '2 340 mm', '5670×1950×2310 mm'], ['ZLJ30F', '9 600 kg', '1,7 m³', '3 000 kg', '125 kW', '2 720 mm', '7314×2350×2600 mm']],
        'Ładowarki kołowe – modele ZLJ')],
    ('Ładowarki kołowe – od małych do ciężkich', '<p>Oferta obejmuje ładowarki od klasy 2 ton udźwigu (928G) do 7,5 tony (978G), model 935G z wysięgnikiem teleskopowym (wysokość wyładunku 5 m), wersje z baterią (EV/HEV) oraz serię ZLJ. Dobór modelu zależy od rodzaju pracy i materiału – doradzimy po telefonie.</p>'),
    faq_cat('ładowarki kołowe'))
CATS['ladowarki-teleskopowe'] = cat_parts('ladowarki-teleskopowe', 'Ładowarki teleskopowe – sprzedaż, modele i parametry', 'Ładowarki teleskopowe', 'Ładowarki teleskopowe o udźwigu 3–4 t i wysokości podnoszenia od 7 do 18 m: modele 3007J, 3007Y, 3507J, 3511J, 4018J i 4018Y. Zamawiamy prosto z fabryki – zapytaj o cenę.', 'ladowarki-teleskopowe', 'Ładowarka teleskopowa podnosząca bele na placu',
    [mtable(['Model', 'Masa robocza', 'Pojemność łyżki', 'Udźwig', 'Moc', 'Maks. wysokość podnoszenia', 'Wymiary'], [
        ['3007J', '8 582 kg', '1,7 m³', '3 000 kg', '75 kW', '7 000 mm', '6010×2280×2540 mm'], ['3007Y', '8 300 kg', '1,7 m³', '3 000 kg', '73,5 kW', '7 000 mm', '6010×2280×2540 mm'],
        ['3507J', '8 580 kg', '1,7 m³', '3 500 kg', '75 kW', '7 000 mm', '6425×2280×2580 mm'], ['3511J', '9 700 kg', '1,7 m³', '3 500 kg', '75 kW', '11 000 mm', '7135×2280×2580 mm'],
        ['4018J', '13 000 kg', '2,0 m³', '4 000 kg', '104 kW', '18 000 mm', '7700×2420×2710 mm'], ['4018Y', '13 000 kg', '2,0 m³', '4 000 kg', '104 kW', '18 000 mm', '6330×2420×2815 mm']], 'Ładowarki teleskopowe – modele 3007–4018')],
    ('Ładowarki teleskopowe do rolnictwa i budowy', '<p>Sześć modeli: od 7 m wysokości podnoszenia (3007, 3507) przez 11 m (3511J) do 18 m (4018). Udźwig 3–4 tony, moc 73,5–104 kW. Dostępne na zamówienie z osprzętem – zapytaj o konfigurację.</p>'),
    faq_cat('ładowarki teleskopowe'))
CATS['koparki'] = cat_parts('koparki', 'Koparki gąsienicowe – sprzedaż, modele i parametry', 'Koparki gąsienicowe', 'Koparki gąsienicowe od 14 do 78 ton: modele E15D–E80F, pojemność łyżki od 0,63 do 5,2 m³. Zamawiamy prosto z fabryki – zapytaj o cenę.', 'koparki', 'Koparka gąsienicowa pracująca w kamieniołomie',
    [mtable(['Model', 'Masa robocza', 'Moc (kW / obr./min)', 'Pojemność łyżki'], [
        ['E15D', '14 000 kg', '86 / 2200', '0,63 m³'], ['E15DF', '16 500 kg', '86 / 2200', 'na zapytanie'], ['E22D', '21 700 kg', '133 / 2000', '1,0 m³'], ['E23D', '22 650 kg', '133 / 2000', '1,1 m³'],
        ['E33D', '32 500 kg', '241 / 1900', '1,6 m³'], ['E36D', '36 200 kg', '241 / 1900', '1,6 m³'], ['E38D', '37 600 kg', '241 / 1900', '1,9 m³'], ['E40D', '39 800 kg', '241 / 1900', '2,1 m³'],
        ['E50E', '49 800 kg', '299 / 1800', '2,8 m³'], ['E55E', '53 200 kg', '299 / 1800', '3,2 m³'], ['E80F', '78 200 kg', '563 / 2100', '5,2 m³']], 'Koparki gąsienicowe – modele E15D–E80F')],
    ('Koparki od 14 do 78 ton', '<p>Jedenaście modeli: od klasy 14 t (E15D) po 78 t (E80F). Moc od 86 do 563 kW, łyżki od 0,63 do 5,2 m³. Wersje z osprzętem specjalnym (np. chwytak) na zapytanie.</p>'),
    faq_cat('koparki'))
CATS['spycharki'] = cat_parts('spycharki', 'Spycharki – sprzedaż, modele i parametry', 'Spycharki', 'Spycharki gąsienicowe od 16,4 do 57 ton: modele D18D, D18DL, D26D, D26DS, D26DR, D36D i DH56E. Zamawiamy prosto z fabryki – zapytaj o cenę.', 'spycharki', 'Spycharka gąsienicowa na hałdzie ziemi',
    [mtable(['Model', 'Masa robocza', 'Lemiesz', 'Silnik', 'Moc (kW / obr./min)', 'Podziałka gąsienicy', 'Wymiary'], [
        ['D18D', '16,4 t', 'prosty uchylny 4,5 m³', 'WD10G178E25', '131 / 1850', '203,2 mm', '4990×3440×3110 mm'], ['D18DL', '18 t', 'prosty uchylny 3,8 m³', 'WD10', '131 / 1850', '203,2 mm', '5262×4150×3074 mm'],
        ['D26D', '23,5 t', 'prosty uchylny 6,4 m³', 'NT855-C280', '187 / 1850', '216 mm', '5390×3735×3350 mm'], ['D26DS', '25,7 t', 'prosty uchylny 6,8 m³', 'NT855-C280', '187 / 1850', '216 mm', '6290×4365×3402 mm'],
        ['D26DR', '26 t', 'na zapytanie', 'NT855-C280', '254 (187) / 1800', '216 mm', '6290×4365×3745 mm'], ['D36D', '37,2 t', 'prosty uchylny 10 m³', 'NTA855-C360', '268 / 2000', '228,6 mm', '6535×4150×3515 mm'],
        ['DH56E', '57 t', 'skalny 15,2 m³', 'Cummins QSM15', '563 / 1900', '260 mm', '9235×4320×3990 mm']], 'Spycharki – modele D18D–DH56E')],
    ('Spycharki od 16 do 57 ton', '<p>Siedem modeli o masie od 16,4 do 57 ton, z lemieszem prostym uchylnym (3,8–10 m³) lub skalnym (15,2 m³). Moc od 131 do 563 kW.</p>'),
    faq_cat('spycharki'))
CATS['miniladowarki'] = cat_parts('miniladowarki', 'Miniładowarki – sprzedaż, modele i parametry', 'Miniładowarki', 'Miniładowarki WM308 i WM312: udźwig 850 i 1 200 kg, moc 36,7 i 55 kW. Zamawiamy prosto z fabryki – zapytaj o cenę.', 'miniladowarki', 'Miniładowarka podczas załadunku żwiru',
    [mtable(['Model', 'Masa robocza', 'Pojemność łyżki', 'Udźwig', 'Moc', 'Rozstaw osi', 'Wymiary'], [
        ['WM308', '3 000 kg', '0,48 m³', '850 kg', '36,7 kW', '1 045 mm', '3440×1830×2020 mm'], ['WM312', '3 500 kg', '0,54 m³', '1 200 kg', '55 kW', '1 080 mm', '3580×1830×2050 mm']], 'Miniładowarki – modele WM308 i WM312')],
    ('Miniładowarki do ciasnych placów', '<p>Zwrotne miniładowarki z podwoziem kołowym i obrotem w miejscu – do prac porządkowych, załadunku i robót w ograniczonej przestrzeni. Dwa modele: WM308 (850 kg) i WM312 (1 200 kg).</p>'),
    faq_cat('miniładowarki'))
CATS['ciagniki-kolowe'] = cat_parts('ciagniki-kolowe', 'Ciągniki kołowe – sprzedaż, modele i parametry', 'Ciągniki kołowe', 'Ciągniki kołowe dużej mocy: S2604 (191 kW), F3004 (221 kW) i F4004 (294 kW). Zamawiamy prosto z fabryki – zapytaj o cenę.', 'ciagniki', 'Ciągnik kołowy podczas orki',
    [mtable(['Model', 'Min. masa eksploatacyjna', 'Maks. siła uciągu', 'Maks. siła podnoszenia', 'Moc silnika', 'Rozstaw osi', 'Wymiary'], [
        ['S2604', '9 000 kg', '75 kN', '65 kN', '191 kW', '3 080 mm', '5840×2635×3200 mm'], ['F3004', '10 800 kg', '90 kN', '72 kN', '221 kW', '3 210 mm', '6210×2870×3420 mm'], ['F4004', '12 400 kg', '106 kN', '85 kN', '294 kW', '3 200 mm', '6900×2950×3450 mm']], 'Ciągniki kołowe – modele S2604, F3004, F4004')],
    ('Ciągniki dużej mocy', '<p>Trzy modele o mocy 191, 221 i 294 kW, z siłą uciągu 75–106 kN i siłą podnoszenia 65–85 kN – do prac polowych i ciężkich zadań transportowych.</p>'),
    faq_cat('ciągniki'))


# ---------------------------------------------------------------- Artykuły
def md_article(path, fixes):
    t = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n', t, re.S)
    meta = dict(re.findall(r'^(\w+): (.*)$', m.group(1), re.M))
    t = t[m.end():]
    for a, b in fixes:
        t = t.replace(a, b)

    def conv_table(mm):
        cap = mm.group(1)
        lines = [l for l in mm.group(2).strip().splitlines() if l.strip()]
        rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if not re.match(r'^\|?\s*-+', l)]
        h = f'<div class="tw"><table class="mt"><caption>{cap}</caption><thead><tr>' + ''.join(f'<th>{c}</th>' for c in rows[0]) + '</tr></thead><tbody>'
        for r in rows[1:]:
            h += '<tr>' + ''.join(f'<td>{c}</td>' if i else f'<th scope="row">{c}</th>' for i, c in enumerate(r)) + '</tr>'
        TB.append(h + '</tbody></table></div>')
        return '\n\n<!--T' + str(len(TB) - 1) + '-->\n\n'
    TB.clear()
    t = re.sub(r'<table><caption>(.*?)</caption>\n(.*?)</table>', conv_table, t, flags=re.S)
    html = markdown.markdown(t, extensions=['tables'])
    for i, h in enumerate(TB):
        html = html.replace(f'<!--T{i}-->', h)
    html = re.sub(r'<table>', '<div class="tw"><table class="mt">', html)
    html = html.replace('</table>', '</table></div>')
    html = html.replace('<blockquote>', '<div class="box note-box">').replace('</blockquote>', '</div>')
    html = re.sub(r'<h1>(.*?)</h1>', r'<h1>\1</h1>', html)
    return meta, html


TB = []


def art_parts(slug, src, fixes, schema_extra=None):
    meta, html = md_article(src, fixes)
    h1 = re.search(r'<h1>(.*?)</h1>', html).group(1)
    html = html.replace(f'<h1>{h1}</h1>', '', 1)
    lds = ld(bc([('Strona główna', '/'), ('Maszyny budowlane', HUB), (h1, f'/maszyny-budowlane/{slug}/')]))
    lds += ld({'@context': 'https://schema.org', '@type': 'Article', 'headline': h1, 'datePublished': '2026-11-26', 'dateModified': '2026-11-26', 'inLanguage': 'pl',
               'author': {'@type': 'Organization', 'name': 'FUDALI'}, 'publisher': {'@type': 'Organization', 'name': 'FUDALI'}, 'mainEntityOfPage': f'{BASE}/maszyny-budowlane/{slug}/'})
    if schema_extra:
        lds += ld(schema_extra)
    p1 = wrap(lds + crumb([('Maszyny budowlane', HUB), (h1, '')]) + f'<section class="art"><div class="w"><h1>{h1}</h1><div class="body">{html}</div></div></section>'
              + inquiry('Zapytaj o ofertę'))
    p2 = wrap(f'<section><div class="w c"><h2>Masz pytania? Zadzwoń.</h2><div class="cta cc">{call}<a class="btn b3" href="mailto:{MAIL}">{MAIL}</a></div><p style="margin-top:18px"><a href="/maszyny-budowlane/">Cała oferta maszyn budowlanych</a> · <a href="/maszyny-budowlane/shanmon-fuji-388/">Shanmon Fuji 388 – od ręki</a></p></div></section>' + bar)
    return meta, [mini(p1), mini(p2)]


FIX = [('silnik Yuchai 74 kW', 'silnik ok. 75 kW, norma Euro V (wg dokumentów maszyny)'), ('Yuchai 74 kW', 'ok. 75 kW'), ('– dane z ogłoszenia', '– dane z dokumentów maszyny'), ('dane z ogłoszenia', 'dane z dokumentów maszyny'), ('(74 kW', '(ok. 75 kW'),
       ('Rocznik 2026, silnik ok. 75 kW', 'Rocznik 2026, silnik ok. 75 kW')]
TR = os.path.join(ROOT, 'marketing/kampanie/maszyny-seo/tresci/final/')
ART = {
    'nowa-koparko-ladowarka-cena': TR + '1-nowa-koparko-ladowarka-cena.md',
    'alternatywa-dla-jcb-3cx': TR + '2-alternatywa-dla-jcb-3cx.md',
    'chinska-koparko-ladowarka-czy-warto': TR + '3-chinska-koparko-ladowarka-czy-warto.md',
    'leasing-koparko-ladowarki': TR + '4-leasing-koparko-ladowarki.md'}

PAGES = {}  # slug -> dict(title, meta, parts, form_after, form_name)


def build_all():
    PAGES['hub'] = dict(id=2250, title='Maszyny budowlane – koparko-ładowarki na sprzedaż', meta='Koparko-ładowarki na sprzedaż: nowy Shanmon Fuji 388 od ręki w Rzeszowie, 12 mies. gwarancji, leasing i transport. Minikoparki, ładowarki, koparki, spycharki, ciągniki na zamówienie.', parts=hub_parts(), form_after=0, form_name='Zapytanie – maszyny budowlane', subject='maszyny budowlane', pfx='a1')
    PAGES['fuji'] = dict(id=2253, title='Koparko-ładowarka Shanmon Fuji 388 – 2026, od ręki w Rzeszowie', meta='Nowa koparko-ładowarka Shanmon Fuji 388 (2026), ok. 75 kW, ramię do 5,5 m, łyżka 6w1. 250 000 zł netto, 2 szt. od ręki w Rzeszowie, gwarancja 12 mies., leasing.', parts=fuji_parts(), form_after=0, form_name='Zapytanie – Shanmon Fuji 388', subject='Shanmon Fuji 388', pfx='b1')
    PAGES['minikoparka'] = dict(title='Minikoparka na sprzedaż – 134 990 zł netto z dostawą', meta='Nowa minikoparka z zamkniętą kabiną, gumowymi gąsienicami i szybkozłączem. 134 990 zł netto z dostawą do klienta, 2 szt., możliwość OEM (własny kolor i logo). FUDALI.', parts=mini_parts(), form_after=0, form_name='Zapytanie – minikoparka', subject='minikoparka', pfx='c1')
    metas = {'ladowarki-kolowe': ('Ładowarki kołowe na sprzedaż – modele i parametry', 'Ładowarki kołowe 928G–978G, z wysięgnikiem teleskopowym, EV/HEV i ZLJ: parametry w tabelach, zamówienie prosto z fabryki. Zapytaj o cenę – FUDALI Rzeszów.'),
             'ladowarki-teleskopowe': ('Ładowarki teleskopowe na sprzedaż – modele i parametry', 'Ładowarki teleskopowe 3007–4018: udźwig 3–4 t, wysokość podnoszenia 7–18 m. Parametry w tabeli, zamówienie prosto z fabryki. FUDALI Rzeszów.'),
             'koparki': ('Koparki gąsienicowe na sprzedaż – modele i parametry', 'Koparki gąsienicowe E15D–E80F od 14 do 78 t: moc, pojemność łyżki, parametry. Zamówienie prosto z fabryki, leasing dla firm. FUDALI Rzeszów.'),
             'spycharki': ('Spycharki na sprzedaż – modele i parametry', 'Spycharki D18D–DH56E od 16,4 do 57 t: lemiesz, silnik, moc, wymiary. Zamówienie prosto z fabryki, leasing dla firm. FUDALI Rzeszów.'),
             'miniladowarki': ('Miniładowarki na sprzedaż – WM308 i WM312', 'Miniładowarki WM308 i WM312: udźwig 850 i 1 200 kg, moc 36,7 i 55 kW. Zamówienie prosto z fabryki. FUDALI Rzeszów.'),
             'ciagniki-kolowe': ('Ciągniki kołowe na sprzedaż – 191–294 kW', 'Ciągniki kołowe S2604, F3004, F4004: moc 191–294 kW, siła uciągu do 106 kN. Zamówienie prosto z fabryki. FUDALI Rzeszów.')}
    for i, (s, parts) in enumerate(CATS.items()):
        if s == 'miniladowarki' and not img('miniladowarki'):
            continue
        t, mt = metas[s]
        PAGES[s] = dict(title=t, meta=mt, parts=parts, form_after=0, form_name=f'Zapytanie – {s}', subject=s, pfx=f'd{i + 1}')
    for i, (s, src) in enumerate(ART.items()):
        meta, parts = art_parts(s, src, FIX, faq_ld([('Czy mogę kupić na kredyt jako osoba prywatna?', 'Tak, w ogłoszeniu oferujemy kredyty firmowe i prywatne; warunki ustala bank.'), ('Czy leasing wpływa na gwarancję?', 'Nie. Gwarancja (12 mies. na silnik, skrzynię i most) i serwis działają tak samo jak przy zakupie za gotówkę.'), ('Ile wynosi rata?', 'Zależy od oferty leasingodawcy; podamy po zapytaniu.')]) if s == 'leasing-koparko-ladowarki' else None)
        PAGES[s] = dict(title=meta['title'].strip('"'), meta=meta['meta'].strip('"'), parts=parts, form_after=0, form_name=f'Zapytanie – {s}', subject=s, pfx=f'e{i + 1}')


if __name__ == '__main__':
    build_all()
    os.makedirs('pages', exist_ok=True)
    for s, p in PAGES.items():
        data = page_data(p['pfx'], p['parts'], p['form_after'], p['form_name'], p['subject'])
        body = {'title': p['title'], 'post_type': 'page', 'page_template': 'elementor_header_footer', 'data': data}
        if 'id' in p:
            body['id'] = p['id']
        else:
            body['status'] = 'draft'
        json.dump(body, open(f'pages/{s}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
        head = '<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><link href="https://fonts.googleapis.com/css2?family=Jost:wght@500;600&family=Heebo&display=swap" rel=stylesheet><body style="margin:0"><style>' + CSS + '</style>'
        mock = '<div style="background:#151515;padding:0 20px 60px"><div style="max-width:820px;margin:0 auto;height:200px;background:#fff;color:#000">(formularz Elementor)</div></div>'
        open(f'pages/{s}.html', 'w').write(head + p['parts'][0] + mock + ''.join(p['parts'][1:]))
        print(s, len(json.dumps(body, ensure_ascii=False, separators=(',', ':'))))
