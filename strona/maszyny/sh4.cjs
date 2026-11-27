const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const m=await b.newPage({viewport:{width:390,height:844}});
await m.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'});await m.waitForTimeout(2500);
console.log(await m.evaluate(()=>['e1000001','e2000001'].map(id=>{const e=document.querySelector('.elementor-element-'+id);const r=e.getBoundingClientRect();return id+' '+Math.round(r.left)+'-'+Math.round(r.right)+' top'+Math.round(r.top)+' h'+Math.round(r.height)+' parent:'+e.parentElement.className.slice(0,50)}).join('\n')));
await m.screenshot({path:S+'s4-m.png',clip:{x:0,y:0,width:390,height:700}});
await b.close();})();
