const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,100));}});
await p.screenshot({path:S+'f5-shop.png',fullPage:true});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
await p.evaluate(()=>{const e=[...document.querySelectorAll('h2')].find(h=>/bestseller/i.test(h.textContent));e&&e.scrollIntoView()});await p.waitForTimeout(1200);await p.screenshot({path:S+'f5-home.png'});
await b.close();})();
