const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const go=async(p,u)=>{for(let i=0;i<4;i++){const r=await p.goto(u,{waitUntil:'networkidle'}).catch(()=>null);if(r&&r.status()<500&&!(await p.content()).includes('upstream request failed'))return;await p.waitForTimeout(4000);}};
const d=await b.newPage({viewport:{width:1440,height:900}});
await go(d,'https://www.fudali.com.pl/');await d.evaluate(async()=>{for(let y=0;y<3000;y+=300){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,150));}});
for(const [sel,n] of [['.elementor-element-30419b0','fb-tiles'],['.elementor-element-78da94c0','fb-best']]){const e=await d.$(sel);await e.scrollIntoViewIfNeeded();await d.waitForTimeout(900);await e.screenshot({path:S+n+'.png'});}
await go(d,'https://www.fudali.com.pl/sklep/');await d.screenshot({path:S+'fb-shop.png'});
await go(d,'https://www.fudali.com.pl/produkt/lezak-ogrodowy/');await d.evaluate(async()=>{for(let y=0;y<4000;y+=300){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}});
const a=await d.$('.elementor-element-3a76ce6');await a.scrollIntoViewIfNeeded();await d.waitForTimeout(500);await d.screenshot({path:S+'fb-acc.png'});
console.log('link:',await d.evaluate(()=>!!document.querySelector('.fud-acc-link')));
const m=await b.newPage({viewport:{width:390,height:844}});await go(m,'https://www.fudali.com.pl/sklep/');await m.screenshot({path:S+'fb-mob.png'});
await go(m,'https://www.fudali.com.pl/produkt/lezak-ogrodowy/');await m.evaluate(async()=>{for(let y=0;y<6000;y+=300){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,100));}});const am=await m.$('.elementor-element-3a76ce6');await am.scrollIntoViewIfNeeded();await m.waitForTimeout(500);await m.screenshot({path:S+'fb-mob-acc.png'});console.log('sw',await m.evaluate(()=>document.documentElement.scrollWidth));
await b.close();})();
