const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
for(const [n,opt] of [['d',{viewport:{width:1440,height:900}}],['m',{viewport:{width:390,height:844},isMobile:true,hasTouch:true}]]){
const c=await b.newContext(opt);const p=await c.newPage();
await p.goto('https://www.fudali.com.pl/?add-to-cart=2146',{waitUntil:'networkidle'});
for(let i=0;i<4;i++){const r=await p.goto('https://www.fudali.com.pl/koszyk/',{waitUntil:'networkidle'}).catch(()=>null);if(r&&r.status()<500&&!(await p.content()).includes('upstream request failed'))break;await p.waitForTimeout(4000);}
await p.waitForTimeout(2500);
console.log(n,JSON.stringify(await p.evaluate(()=>({sw:document.documentElement.scrollWidth,h2:[...document.querySelectorAll('h2')].map(h=>h.innerText).slice(0,3),cross:document.querySelectorAll('.wp-block-woocommerce-product-collection li').length,coupon:!!([...document.querySelectorAll('.wc-block-components-totals-coupon')].find(e=>e.offsetParent)),cartL:Math.round((document.querySelector('.wp-block-woocommerce-cart')||document.body).getBoundingClientRect().left)}))));
await p.screenshot({path:S+'cart3-'+n+'.png',fullPage:true});
if(n=='m'){const btn=p.locator('.wc-block-cart__submit-button').first();await btn.click({timeout:8000}).catch(e=>console.log('click err',e.message));await p.waitForTimeout(3000);console.log('po kliknięciu:',p.url());}
await c.close();}
await b.close();})();
