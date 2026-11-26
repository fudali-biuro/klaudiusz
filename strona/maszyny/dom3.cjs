const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{
 const o=[];
 const el=[...document.querySelectorAll('a,span,div,p')].filter(e=>/Zapłać później/.test(e.textContent)&&e.children.length<3).slice(0,2);
 el.forEach(e=>o.push('ZAP:'+e.tagName+'.'+e.className+' parent:'+e.parentElement.className));
 const h=[...document.querySelectorAll('h1,h2,h3')].filter(e=>/PROMOCJE|Promocje/i.test(e.textContent))[0];
 let s=h&&h.closest('.elementor-top-section,.elementor-top-container,.e-parent');o.push('PROMO:'+(s&&s.className.slice(0,200)));
 return o.join('\n');}));
await b.close();})();
