const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/produkt/stolik-boczny-platek-debowy/',{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}window.scrollTo(0,0);});
await p.screenshot({path:S+'prod2-d.png',fullPage:true});
for(const [u,n] of [['kontakt','kontakt'],['realizacje','real'],['o-firmie','ofirmie']]){
 for(const [w,t] of [[1280,'d'],[390,'m']]){
  const q=await b.newPage({viewport:{width:w,height:900}});await q.goto('https://www.fudali.com.pl/'+u+'/',{waitUntil:'networkidle'});
  await q.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,100));}window.scrollTo(0,0);});
  await q.screenshot({path:S+n+'-'+t+'.png',fullPage:true});
  if(t=='d')console.log(u,await q.evaluate(()=>[...document.querySelectorAll('[data-elementor-type="wp-page"] > *')].map(e=>(e.dataset.id||'')+' h='+Math.round(e.getBoundingClientRect().height)+' '+e.innerText.replace(/\s+/g,' ').slice(0,60)).join('\n')));
  await q.close();}}
await b.close();})();
