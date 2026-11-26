const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();
 const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
 const slugs=['','minikoparka','ladowarki-kolowe','ladowarki-teleskopowe','koparki','spycharki','ciagniki-kolowe','nowa-koparko-ladowarka-cena','alternatywa-dla-jcb-3cx','chinska-koparko-ladowarka-czy-warto','leasing-koparko-ladowarki'];
 for(const s of slugs){
  const p=await b.newPage({viewport:{width:390,height:900}});
  const r=await p.goto('https://www.fudali.com.pl/maszyny-budowlane/'+(s?s+'/':''),{waitUntil:'networkidle'}).catch(e=>null);
  await p.waitForTimeout(800);
  const info=await p.evaluate(()=>({h1:(document.querySelector('h1')||{}).innerText,tel:document.querySelectorAll('a[href^="tel:"]').length,form:!!document.querySelector('form.elementor-form'),sw:document.documentElement.scrollWidth,imgBroken:[...document.images].filter(i=>i.complete&&i.naturalWidth==0).length,bg:getComputedStyle(document.querySelector('.fm')||document.body).backgroundColor,desc:(document.querySelector('meta[name=description]')||{}).content}));
  console.log(s||'hub',r&&r.status(),JSON.stringify(info));
  await p.screenshot({path:S+'live-'+(s||'hub')+'.png',fullPage:true});
  await p.close();
 }
 await b.close();
})();
