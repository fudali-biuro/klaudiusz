// Zrzut ekranu strony (komputer + telefon), żeby sprawdzić wygląd zamiast zgadywać.
// Użycie: node strona/narzedzia/zrzut.cjs <adres> <folder-wyjściowy> [nazwa]
// Działa tylko dla stron publicznych (szkice w panelu wymagają logowania).
const { chromium } = require('playwright');
const [url, out, name = 'strona'] = process.argv.slice(2);
if (!url || !out) { console.log('Użycie: node zrzut.cjs <adres> <folder> [nazwa]'); process.exit(1); }
(async () => {
  const b = await chromium.launch();
  for (const [tag, vp] of [['komputer', { width: 1440, height: 900 }], ['telefon', { width: 390, height: 844 }]]) {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: 1 });
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await p.waitForTimeout(1500);
    // przewiń całą stronę, żeby uruchomić animacje wjazdu
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 250)); } window.scrollTo(0, 0); });
    await p.waitForTimeout(800);
    await p.screenshot({ path: `${out}/${name}-${tag}.png`, fullPage: true });
    console.log('zapisano', `${out}/${name}-${tag}.png`);
    await p.close();
  }
  await b.close();
})();
