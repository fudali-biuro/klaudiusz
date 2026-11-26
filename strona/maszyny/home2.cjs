const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
for(const [w,n] of [[1280,'d'],[390,'m']]){
const p=await b.newPage({viewport:{width:w,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,150));}window.scrollTo(0,0);});
await p.waitForTimeout(800);
await p.screenshot({path:S+'home2-'+n+'.png',fullPage:true});await p.close();}
await b.close();})();
