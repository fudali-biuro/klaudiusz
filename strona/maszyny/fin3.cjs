const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
for(const [w,n] of [[1440,'d'],[390,'m']]){
const p=await b.newPage({viewport:{width:w,height:900}});await p.goto('https://www.fudali.com.pl/kontakt/',{waitUntil:'networkidle'});
await p.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));await p.waitForTimeout(800);
const f=await p.$('.elementor-location-footer');await f.screenshot({path:S+'f3-foot-'+n+'.png'});
if(n=='m'){const q=await b.newPage({viewport:{width:390,height:844}});await q.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});await q.screenshot({path:S+'f3-home-m.png'});}
await p.close();}
await b.close();})();
