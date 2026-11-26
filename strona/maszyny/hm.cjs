const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
for(const [w,n] of [[1440,'d'],[390,'m']]){const p=await b.newPage({viewport:{width:w,height:900}});await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}});await p.waitForTimeout(1500);
const t=await p.$('.elementor-widget-loop-grid');await t.scrollIntoViewIfNeeded();await t.screenshot({path:S+'h-tiles-'+n+'.png'});
const f=await p.$('.elementor-element-802c4aa');await f.scrollIntoViewIfNeeded();await f.screenshot({path:S+'h-faq-'+n+'.png'});await p.close();}
await b.close();})();
