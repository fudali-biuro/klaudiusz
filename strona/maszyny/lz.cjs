const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();for(const [w,m] of [[390,1],[1440,0]]){const c=await b.newContext(m?{viewport:{width:390,height:844},isMobile:true,hasTouch:true}:{viewport:{width:1440,height:900}});const p=await c.newPage();
await p.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'});await p.waitForTimeout(3000);
const li=await p.evaluateHandle(()=>[...document.querySelectorAll('li.product')].find(l=>/le[żz]ak/i.test(l.innerText)&&l.offsetParent));
await li.asElement().scrollIntoViewIfNeeded();await p.waitForTimeout(1500);await li.asElement().screenshot({path:'/tmp/aud/lz'+w+'.png'});
console.log(w,await li.evaluate(l=>{const t=l.querySelector('table.variations, .cfvsw-swatches-container');const s=l.querySelector('select');return 'h'+Math.round(l.getBoundingClientRect().height)+' table:'+(t?Math.round(t.getBoundingClientRect().height):'-')+' sel:'+(s?s.outerHTML.slice(0,200):'-')+' swatches:'+l.querySelectorAll('.cfvsw-swatches-option').length}));await c.close();}
await b.close();})();
