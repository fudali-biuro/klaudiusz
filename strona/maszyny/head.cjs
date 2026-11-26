const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const s of ['koparki','leasing-koparko-ladowarki']){
await p.goto('https://www.fudali.com.pl/maszyny-budowlane/'+s+'/');
console.log(await p.evaluate(()=>[document.title,[...document.querySelectorAll('meta[name=description],meta[property="og:description"],link[rel=canonical],meta[name=robots]')].map(e=>e.outerHTML)]));}
await b.close();})();
