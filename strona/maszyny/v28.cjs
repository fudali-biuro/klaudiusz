const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
for(const [w,n] of [[1440,'d'],[390,'m']]){const p=await b.newPage({viewport:{width:w,height:900}});
for(let i=0;i<4;i++){const r=await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'}).catch(()=>null);if(r&&r.status()<500&&!(await p.content()).includes('upstream request failed'))break;await p.waitForTimeout(4000);}
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,90));}window.scrollTo(0,0)});await p.waitForTimeout(600);
await p.screenshot({path:S+'v28-'+n+'.png',fullPage:true});
console.log(n,'slideBtn visible:',await p.evaluate(()=>[...document.querySelectorAll('.elementor-slide-button')].some(e=>e.offsetParent)),'sw:',await p.evaluate(()=>document.documentElement.scrollWidth));await p.close();}
await b.close();})();
