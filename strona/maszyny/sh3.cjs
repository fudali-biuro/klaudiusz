const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const m=await b.newPage({viewport:{width:390,height:844}});
for(let i=0;i<4;i++){const r=await m.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'}).catch(()=>null);if(r&&r.status()<500&&!(await m.content()).includes('upstream request failed'))break;await m.waitForTimeout(4000);}
await m.evaluate(()=>{const c=document.querySelector('.flexible-cookies, #flexible-cookies, [class*=cookie]');});
await m.screenshot({path:S+'s3-m.png',clip:{x:0,y:0,width:390,height:844}});
console.log('sw',await m.evaluate(()=>document.documentElement.scrollWidth),await m.evaluate(()=>[...document.querySelectorAll('.elementor-element-e2000001 .fudali-pill')].map(e=>{const r=e.getBoundingClientRect();return Math.round(r.left)+'-'+Math.round(r.right)}).join(' ')));
await b.close();})();
