import sys, re, json
import build as B

TEL, TELH, MAIL, FUJI, BASE = B.TEL, B.TELH, B.MAIL, B.FUJI, B.BASE
LOCAL = B.LOCAL
im = B.im

call = f'<a class="btn b1 call" href="{TELH}">Zadzwoń: {TEL}</a>'
call_side = f'<a class="btn b1 call" href="{TELH}">Zadzwoń: {TEL}</a>'
ask = '<a class="btn b3" href="#zapytanie">Wyślij zapytanie</a>'
bar = f'<div class="bar"><a class="btn b1 call" href="{TELH}">Zadzwoń</a><a class="btn b3" href="#zapytanie">Zapytaj o cenę</a></div>'

TRUST = ('<div class="trust"><div class="w"><ul>'
         '<li><b>12 miesięcy</b>gwarancji producenta</li>'
         '<li><b>Jazda próbna</b>na placu w Rzeszowie</li>'
         '<li><b>Leasing i kredyt</b>pomoc w formalnościach</li>'
         '<li><b>Transport</b>na Twoją budowę</li>'
         '</ul></div></div>')


def head_ld(*objs):
    return ''.join(B.ld(o) for o in objs)


def inquiry_section(title):
    return (f'<section class="alt" id="zapytanie"><div class="w c"><span class="eyebrow">Zapytanie</span>'
            f'<h2>{title}</h2><p>Zostaw numer – oddzwonimy z ofertą i finansowaniem. Albo zadzwoń od razu:</p>'
            f'<div class="cta cc">{call}</div></div></section>')


def catalog_part1():
    feat = (f'<section id="oferta"><div class="w"><span class="eyebrow">Dostępna od ręki</span>'
            f'<h2>Shanmon Fuji 388 – nowa, 2026</h2><div class="feat"><div class="ph"><span class="tag">Od ręki · Rzeszów</span>'
            f'<img src="{im("3")}" alt="{B.ALT["3"]}" loading="lazy"></div><div class="bd">'
            f'<h3>Koparko-ładowarka Shanmon Fuji 388</h3>'
            + B.spec([('Rok produkcji', '2026 (lipiec)'), ('Motogodziny', '5 mth'), ('Moc silnika', '74 kW (ok. 100 KM)'),
                      ('Masa robocza', '8 200 kg'), ('Napęd', '4x4'), ('Głębokość kopania', 'do 5,5 m'),
                      ('Łyżka przednia', '6w1, 2 200 mm'), ('Gwarancja', '12 miesięcy')])
            + '<div class="price">250 000 zł netto<small>307 500 zł brutto · możliwość odliczenia VAT</small></div>'
              f'<div class="cta"><a class="btn b1" href="{FUJI}">Szczegóły maszyny</a>'
              f'<a class="btn b2" href="{TELH}">Zadzwoń: {TEL}</a></div></div></div></div></section>')
    hero = (f'<section class="hero"><div class="w row"><div class="ht"><span class="eyebrow">Maszyny budowlane FUDALI</span>'
            f'<h1>Koparko-ładowarki na sprzedaż</h1>'
            f'<p>Nowa koparko-ładowarka od ręki w Rzeszowie. 12 miesięcy gwarancji, leasing, transport na budowę i serwis w całej Polsce.</p>'
            f'<div class="cta">{call}{ask}</div></div>'
            f'<div class="hi"><img src="{im("1")}" alt="{B.ALT["1"]}" loading="eager"></div></div></section>')
    return ('<div class="fm">' + head_ld(B.coll, B.bc(None, None), B.product) + hero + TRUST + feat
            + inquiry_section('Zapytaj o maszynę') + '</div>')


def catalog_part2():
    h = '<div class="fm">' + B.ld(B.faqld)
    h += ('<section><div class="w"><span class="eyebrow">Katalog producenta</span><h2>Pozostałe modele – na zamówienie</h2>'
          '<p class="lead">Maszyny z katalogu producenta. Cenę, termin dostawy i osprzęt podajemy po zapytaniu. Parametry mogą ulec zmianie bez powiadomienia.</p>'
          '<div class="grid">' + ''.join(B.card(c) for c in B.cat) + '</div></div></section>')
    h += ('<section class="alt"><div class="w"><span class="eyebrow">Finansowanie i transport</span><h2>Kup maszynę bez zamrażania gotówki</h2><div class="two">'
          '<div class="box"><h3>Leasing i kredyt</h3><ul><li>leasing operacyjny i finansowy dla firm</li><li>kredyt dla firm i osób prywatnych</li>'
          '<li>pomoc w formalnościach na miejscu</li><li>możliwość odliczenia VAT</li></ul></div>'
          '<div class="box"><h3>Transport na budowę</h3><ul><li>pomagamy zorganizować dowóz pod wskazany adres</li><li>koszt wyceniamy indywidualnie</li>'
          '<li>odbiór osobisty w Rzeszowie z jazdą próbną</li><li>serwis z dojazdem w całej Polsce</li></ul></div></div></div></section>')
    h += ('<section><div class="w"><span class="eyebrow">Dlaczego Fudali</span><h2>Maszyna gotowa do pracy</h2><div class="why">'
          '<div class="box"><h3>Sprawdzona przed sprzedażą</h3><p>Każdą maszynę kontrolujemy technicznie przed wydaniem. Oględziny i jazda próbna po umówieniu.</p></div>'
          '<div class="box"><h3>Serwis i części</h3><p>Całodobowa infolinia, serwis z dojazdem w całej Polsce, pomoc w doborze części.</p></div>'
          '<div class="box"><h3>Dobór osprzętu</h3><p>Łyżki 30/40/60 cm, skarpowa, młot hydrauliczny, zagęszczarka, świder – doradzimy.</p></div></div></div></section>')
    h += f'<section class="alt"><div class="w"><span class="eyebrow">Pytania i odpowiedzi</span><h2>Najczęstsze pytania</h2>{B.faqh()}</div></section>'
    h += (f'<section><div class="w c"><h2>Masz pytania? Zadzwoń.</h2><div class="cta cc">{call}'
          f'<a class="btn b3" href="mailto:{MAIL}">{MAIL}</a></div></div></section>')
    return h + bar + '</div>'


def fuji_part1():
    thumbs = ''.join(f'<img src="{im(k)}" alt="{B.ALT[k]}" class="{"on" if k == "1" else ""}" data-s="{im(k)}" loading="lazy">' for k in '123456')
    side = ('<aside class="side"><span class="tag in">Od ręki · Rzeszów</span><h1>Koparko-ładowarka Shanmon Fuji 388 – 2026</h1>'
            '<div class="price">250 000 zł netto<small>307 500 zł brutto · możliwość odliczenia VAT</small></div>'
            + B.spec([('Rok', '2026'), ('Motogodziny', '5 mth'), ('Moc', '74 kW / ok. 100 KM'), ('Masa', '8 200 kg'), ('Napęd', '4x4'), ('Kopanie', 'do 5,5 m')])
            + f'{call_side}<a class="btn b2" href="#zapytanie">Zapytaj o finansowanie</a><a class="btn b2" href="#zapytanie">Umów oględziny i jazdę próbną</a></aside>')
    h = '<div class="fm">' + head_ld(B.product, B.bc('Koparko-ładowarka Shanmon Fuji 388', FUJI))
    h += '<div class="w crumb"><a href="/">Strona główna</a> › <a href="/maszyny-budowlane/">Maszyny budowlane</a> › Shanmon Fuji 388</div>'
    h += (f'<section style="padding-top:20px"><div class="w det"><div class="gal"><div class="main"><img id="fmMain" src="{im("1")}" alt="{B.ALT["1"]}"></div>'
          f'<div class="thumbs">{thumbs}</div></div>{side}</div></section>')
    h += inquiry_section('Zapytaj o Shanmon Fuji 388')
    return h + '</div>'


def fuji_part2():
    rows = [('Marka / model', 'Shanmon Fuji 388 (Yuchai)'), ('Stan', 'Fabrycznie nowa, pierwszy właściciel, bezwypadkowa'), ('Rok produkcji', '2026 (lipiec)'),
            ('Motogodziny', '5 mth'), ('Silnik', 'Yuchai, 74 kW (ok. 100 KM), Stage V'), ('Napęd', '4x4, przełączany na 2WD'), ('Masa robocza', '8 200 kg'),
            ('Ramię koparkowe', 'teleskopowe, głębokość kopania do 5,5 m (4,1 m bez wysuwu)'), ('Łyżka tylna', '550 mm (w komplecie)'),
            ('Łyżka przednia', '6w1, hydraulicznie dzielona, szer. 2 200 mm, ok. 1,0 m³'), ('Udźwig ładowarki', '2 500 kg'), ('Wysokość wyładunku', 'do 3 200 mm'),
            ('Szybkozłącza', '2 (przód i tył)'), ('Kabina', 'ROPS/FOPS, klimatyzacja, radio'), ('Bezpieczeństwo', 'kamera cofania, alarm cofania, oświetlenie LED'),
            ('Rozruch zimą', 'podgrzewanie rozruchowe'), ('Gwarancja', '12 mies. – silnik, skrzynia biegów, most'), ('Lokalizacja', 'Rzeszów – oględziny i jazda próbna po umówieniu')]
    h = '<div class="fm">'
    h += ('<section class="alt"><div class="w two"><div><span class="eyebrow">Specyfikacja</span><h2>Dane techniczne</h2><table><tbody>'
          '<tr><th class="tbh" colspan="2">Shanmon Fuji 388 – szczegóły maszyny</th></tr>'
          + ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in rows)
          + '</tbody></table><p class="note">Dane z oferty producenta i sprzedawcy; parametry mogą ulec zmianie bez powiadomienia.</p></div>'
            '<div><span class="eyebrow">Stan techniczny</span><h2>Gotowa do pracy od zaraz</h2><div class="box"><ul>'
            '<li>maszyna fabrycznie nowa, rok 2026, pierwszy właściciel</li><li>weryfikacja techniczna przed wydaniem</li>'
            '<li>jazda próbna i oględziny na placu w Rzeszowie</li><li>w zestawie filtry (paliwa, powietrza) i narzędzia – zakres do 500 mth do uzgodnienia przy zakupie</li></ul></div>'
            '<div class="box" style="margin-top:18px"><h3>Osprzęt na zamówienie</h3><p style="margin:0">Łyżki kopiące 30/40/60 cm, łyżka skarpowa, młot hydrauliczny, zagęszczarka, świder.</p></div></div></div></section>')
    h += ('<section><div class="w two"><div class="box"><span class="eyebrow">Finansowanie</span><h3>Leasing i kredyt</h3><ul><li>leasing operacyjny i finansowy dla firm</li>'
          '<li>kredyt dla firm i osób prywatnych</li><li>pomoc w formalnościach na miejscu</li></ul></div>'
          '<div class="box"><span class="eyebrow">Transport</span><h3>Dowóz na Twoją budowę</h3><ul><li>pomagamy zorganizować transport pod wskazany adres</li>'
          '<li>koszt wyceniamy indywidualnie</li><li>serwis z dojazdem w całej Polsce, infolinia 24/7</li></ul></div></div></section>')
    h += f'<section class="alt"><div class="w"><h2>Pytania o tę maszynę</h2>{B.faqh()}</div></section>'
    h += (f'<section><div class="w c"><h2>Chcesz kupić? Zadzwoń.</h2><div class="cta cc">{call}'
          f'<a class="btn b3" href="mailto:{MAIL}">{MAIL}</a></div></div></section>')
    h += bar
    h += ("<script>(function(){var m=document.getElementById('fmMain');document.querySelectorAll('.fm .thumbs img').forEach(function(t){t.addEventListener('click',function(){m.src=t.getAttribute('data-s');m.alt=t.alt;document.querySelectorAll('.fm .thumbs img').forEach(function(x){x.classList.remove('on')});t.classList.add('on')})})})();</script></div>")
    return h


def mini(h):
    return re.sub(r'>\s+<', '><', h)


MOCKFORM = ('<div style="background:#0c0c0c;padding:0 20px 60px"><div style="max-width:820px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:14px">'
            '<div style="height:60px;background:#fff"></div><div style="height:60px;background:#fff"></div><div style="grid-column:1/-1;height:110px;background:#fff"></div>'
            '<div style="grid-column:1/-1;height:54px;background:#D82018;color:#fff;text-align:center;line-height:54px">WYŚLIJ ZAPYTANIE (formularz Elementor)</div></div></div>')

if __name__ == '__main__':
    css = open('fm.css').read()
    head = '<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><link href="https://fonts.googleapis.com/css2?family=Jost:wght@500;600&family=Heebo&display=swap" rel=stylesheet><body style="margin:0"><style>' + css + '</style>'
    if LOCAL:
        open('katalog-local.html', 'w').write(head + catalog_part1() + MOCKFORM + catalog_part2())
        open('fuji-388-local.html', 'w').write(head + fuji_part1() + MOCKFORM + fuji_part2())
    else:
        for n, f in [('cat1', catalog_part1), ('cat2', catalog_part2), ('fuji1', fuji_part1), ('fuji2', fuji_part2)]:
            open(n + '.min.html', 'w').write(mini(f()))
            print(n, len(mini(f())))
