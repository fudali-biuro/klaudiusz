const {chromium}=require('playwright');
const S='/tmp/aud/';
const pages=[['glowna','/'],['sklep','/sklep/'],['kat-akcesoria','/kategorie/akcesoria-drewniane/'],['kat-architektura','/kategorie/architektura/'],['kat-meble','/kategorie/meble-ogrodowe/'],['kat-drewutnie','/kategorie/drewutnie/'],['kat-wyroby','/kategorie/wyroby-tartaczne/'],['kat-przydatne','/kategorie/przydatne-produkty/'],['produkt-stolik','/produkt/stolik-boczny-platek-debowy/'],['produkt-lezak','/produkt/lezak-ogrodowy/'],['produkt-kot','/produkt/otwieracz-do-butelek-kot/'],['realizacje','/realizacje/'],['o-firmie','/o-firmie/'],['kontakt','/kontakt/'],['maszyny','/maszyny-budowlane/'],['fuji','/maszyny-budowlane/shanmon-fuji-388/'],['minikoparka','/maszyny-budowlane/minikoparka/'],['stare-architektura','/kategorie/architektura-drewniana-i-dekoracje/'],['stare-drewno','/kategorie/drewno-konstrukcyjne-i-deski/'],['stare-akcesoria-domowe','/kategorie/akcesoria-domowe/'],['regulamin','/regulamin/']];
(async()=>{const b=await chromium.launch();const out=[];
for(const [w,v] of [[1440,'d'],[390,'m']]){
 const ctx=await b.newContext(v=='m'?{viewport:{width:390,height:844},isMobile:true,hasTouch:true}:{viewport:{width:1440,height:900}});
 for(const [n,u] of pages){const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message.slice(0,120)));const bad=[];p.on('response',r=>{if(r.status()>=400&&!/google|facebook|gstatic|doubleclick/.test(r.url()))bad.push(r.status()+' '+r.url().slice(0,100))});
  let st=0,t0=Date.now();for(let i=0;i<3;i++){const r=await p.goto('https://www.fudali.com.pl'+u,{waitUntil:'networkidle',timeout:60000}).catch(()=>null);st=r?r.status():0;if(st&&st<500&&!(await p.content()).includes('upstream request failed'))break;await p.waitForTimeout(4000);}
  const load=Date.now()-t0;
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,90));}window.scrollTo(0,0)}).catch(()=>{});
  await p.waitForTimeout(600);
  const info=await p.evaluate(()=>{const t=document.body.innerText;return{title:document.title,h1:[...document.querySelectorAll('h1')].map(h=>h.innerText.trim()).slice(0,2),desc:(document.querySelector('meta[name=description]')||{}).content||'',sw:document.documentElement.scrollWidth,iw:innerWidth,imgBroken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.offsetParent).map(i=>i.src.slice(-60)),en:(t.match(/\b(You may|Add to cart|Read more|Select options|No products|Proceed to checkout|Shopping cart|Related products|Description|Reviews)\b/g)||[]).slice(0,5),zakazane:(t.match(/[^.\n]{0,40}(opałow|tarcica i deski|altany i domki|drewno konstrukcyjne|Zapłać później|Akcesoria domowe)[^.\n]{0,30}/gi)||[]).slice(0,4),emptyLinks:[...document.querySelectorAll('a[href="#"],a:not([href])')].filter(a=>a.offsetParent&&a.innerText.trim()).length,tel:[...document.querySelectorAll('a[href^="tel:"]')].length}}).catch(e=>({err:e.message}));
  if(v=='m'||['glowna','sklep','produkt-stolik','realizacje','kontakt'].includes(n))await p.screenshot({path:S+n+'-'+v+'.png',fullPage:true}).catch(()=>{});
  out.push({n,v,st,load,errs:errs.slice(0,3),bad:bad.slice(0,3),...info});await p.close();}
 await ctx.close();}
require('fs').writeFileSync(S+'audit.json',JSON.stringify(out,null,1));await b.close();
for(const o of out)console.log(o.v,o.n,o.st,o.load+'ms','sw'+o.sw,JSON.stringify({h1:o.h1,desc:(o.desc||'').length,en:o.en,zak:o.zakazane,img:o.imgBroken,errs:o.errs,bad:o.bad}));
})();
