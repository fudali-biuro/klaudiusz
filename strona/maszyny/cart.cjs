const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const c=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});const p=await c.newPage();
await p.goto('https://www.fudali.com.pl/?add-to-cart=2146',{waitUntil:'networkidle'});
const r=await p.goto('https://www.fudali.com.pl/koszyk/',{waitUntil:'networkidle'}).catch(()=>null);console.log('url',p.url(),r&&r.status());
await p.waitForTimeout(1500);
console.log(await p.evaluate(()=>({sw:document.documentElement.scrollWidth,vp:(document.querySelector('meta[name=viewport]')||{}).content,wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return (r.right>395||r.left<-5)&&e.offsetParent&&getComputedStyle(e).position!=='fixed'}).slice(0,8).map(e=>e.tagName+'.'+e.className.toString().slice(0,60)+' L'+Math.round(e.getBoundingClientRect().left)+' R'+Math.round(e.getBoundingClientRect().right)),body:document.body.className.slice(0,200),cross:[...document.querySelectorAll('.cross-sells li.product, .e-cart-section .products li')].length,head:[...document.querySelectorAll('h2')].map(h=>h.innerText).join(' | ')})));
await p.screenshot({path:S+'cart-m.png',fullPage:true});
await b.close();})();
