const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{
 const o=[];
 const sw=document.querySelector('.elementor-element-62a19c1');o.push('SW:'+sw.innerHTML.slice(0,900));
 const t=document.querySelector('.elementor-element-4ef26fee');o.push('TILES:'+t.outerHTML.replace(/\s+/g,' ').slice(0,2500));
 return o.join('\n\n');}));
await b.close();})();
