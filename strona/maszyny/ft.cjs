const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
await p.goto('https://www.fudali.com.pl/kontakt/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>[...document.querySelectorAll('.elementor-location-footer .elementor-widget-heading')].map(w=>{const cs=getComputedStyle(w,'::after'),cs2=getComputedStyle(w.querySelector('.elementor-heading-title'),'::after'),cs3=getComputedStyle(w.querySelector('.elementor-widget-container'),'::after');return w.dataset.id+' '+w.innerText.trim()+' | w:'+cs.content+' '+cs.marginLeft+' '+cs.left+' | t:'+cs2.content+' '+cs2.marginLeft+' | c:'+cs3.content+' '+cs3.marginLeft+' '+cs3.left+' pad:'+getComputedStyle(w).paddingLeft+' marg:'+getComputedStyle(w).marginLeft}).join('\n')));
await b.close();})();
