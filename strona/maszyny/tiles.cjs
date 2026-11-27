const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
for(const [w,n] of [[1440,'d'],[390,'m']]){const p=await b.newPage({viewport:{width:w,height:900}});
for(let i=0;i<4;i++){const r=await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'}).catch(()=>null);if(r&&r.status()<500&&!(await p.content()).includes('upstream request failed'))break;await p.waitForTimeout(4000);}
await p.evaluate(async()=>{for(let y=0;y<2500;y+=300){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,150));}});
const t=await p.$('.elementor-element-30419b0');await t.scrollIntoViewIfNeeded();await p.waitForTimeout(800);await t.screenshot({path:S+'tiles2-'+n+'.png'});
if(n=='d')console.log(await p.evaluate(()=>[...document.querySelectorAll('.elementor-location-footer a')].filter(a=>/Drewno|Przydat/.test(a.innerText)).map(a=>a.innerText+' '+a.href).join(' | ')+' || links:'+[...document.querySelectorAll('.elementor-element-30419b0 a')].map(a=>a.href.split('/').slice(-2)[0]).join(',')));
await p.close();}
await b.close();})();
