const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>[...document.querySelectorAll('.sub-menu a')].map(a=>a.innerText.trim()+(a.offsetParent?'':'(h)')).join(' | ')));
const a=await p.$('.elementor-location-header .elementor-element-1db07d26 .elementor-nav-menu--main a[href*="/sklep"]');await a.hover();await p.waitForTimeout(800);
await p.screenshot({path:S+'sub.png',clip:{x:200,y:0,width:700,height:360}});await b.close();})();
