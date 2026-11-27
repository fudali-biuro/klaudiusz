const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/realizacje/',{waitUntil:'networkidle'});await p.waitForTimeout(1500);
await p.click('.elementor-gallery-item');await p.waitForTimeout(1500);
console.log(await p.evaluate(()=>{const c=[...document.querySelectorAll('.dialog-close-button,.fudali-lb-x,[class*=close]')].filter(e=>e.offsetParent||getComputedStyle(e).position==='fixed').map(e=>{const r=e.getBoundingClientRect(),cs=getComputedStyle(e);return e.tagName+'.'+e.className.toString().slice(0,60)+' '+Math.round(r.width)+'x'+Math.round(r.height)+' disp:'+cs.display+' pad:'+cs.padding+' lh:'+cs.lineHeight+' bg:'+cs.backgroundColor+' fs:'+cs.fontSize+' inner:'+e.innerHTML.slice(0,80)});return c.join('\n')}));
await p.screenshot({path:S+'lb.png',clip:{x:1240,y:0,width:200,height:120}});
const s=await b.newPage({viewport:{width:1440,height:900}});await s.goto('https://www.fudali.com.pl/kategorie/architektura/',{waitUntil:'networkidle'});
console.log(await s.evaluate(()=>{const e=document.querySelector('.elementor-element-e2000001');const cs=getComputedStyle(e);const r=e.getBoundingClientRect();const ch=[...e.querySelectorAll('.fudali-pill')].map(x=>x.getBoundingClientRect());return 'pad:'+cs.padding+' top'+Math.round(r.top)+' h'+Math.round(r.height)+' chipsTop'+Math.round(ch[0].top)+' chipsBottom'+Math.round(ch[0].bottom)+' ai:'+cs.alignItems+' jc:'+cs.justifyContent}));
await b.close();})();
