const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/o-firmie/',{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,200));}});await p.waitForTimeout(1000);
for(const id of ['a3000001','a5000001']){const e=await p.$('.elementor-element-'+id);await e.scrollIntoViewIfNeeded();await p.waitForTimeout(800);await e.screenshot({path:S+'ab-'+id+'.png'});}
console.log(await p.evaluate(()=>{const o=[];for(const id of ['a3000001','a5000001']){const R=document.querySelector('.elementor-element-'+id);o.push(id+': '+[...R.querySelectorAll('.elementor-widget')].map(w=>w.dataset.id+':'+w.dataset.widget_type+':'+w.innerText.replace(/\s+/g,' ').slice(0,60)).join(' | '))}return o.join('\n')}));
await b.close();})();
