const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<1400;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,150));}});
const li=await p.evaluateHandle(()=>[...document.querySelectorAll('li.product')].find(l=>l.offsetParent&&l.querySelector('.cfvsw-swatches-container')));
await li.asElement().screenshot({path:S+'c-card.png'});
const m=await b.newPage({viewport:{width:390,height:844}});await m.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});await m.screenshot({path:S+'c-mob.png'});
await b.close();})();
