const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=300){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,250));}});await p.waitForTimeout(1500);
console.log(await p.evaluate(()=>{const h=document.querySelector('.elementor-location-footer .elementor-heading-title');const im=document.querySelector('.elementor-location-footer img');return 'fs:'+getComputedStyle(h).fontSize+' imgW:'+im.getBoundingClientRect().width+' txt78:'+document.querySelector('.elementor-element-78da94c0').innerText.slice(0,80)}));
const f=await p.$('.elementor-location-footer');await f.screenshot({path:S+'foot.png'});
const s=await p.$('.elementor-element-78da94c0');await s.screenshot({path:S+'s78.png'});
await b.close();})();
