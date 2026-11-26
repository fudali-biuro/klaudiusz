const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
for(const [u,n] of [['','home'],['produkt/stolik-boczny-platek-debowy/','prod'],['sklep/','shop'],['kontakt/','kont']]){
 const p=await b.newPage({viewport:{width:390,height:844}});await p.goto('https://www.fudali.com.pl/'+u,{waitUntil:'networkidle'});
 await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,100));}window.scrollTo(0,0);});
 console.log(n,await p.evaluate(()=>({sw:document.documentElement.scrollWidth,over:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>392&&getComputedStyle(e).position!=='fixed'&&e.offsetParent).slice(0,3).map(e=>e.className.toString().slice(0,50))})));
 await p.screenshot({path:S+'fin-'+n+'.png',fullPage:true});await p.close();}
await b.close();})();
