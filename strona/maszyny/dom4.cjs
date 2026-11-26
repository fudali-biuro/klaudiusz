const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{
 const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n,o=[];
 while(n=w.nextNode()){if(/Zapłać później/i.test(n.textContent)){let e=n.parentElement;o.push(e.tagName+'.'+e.className+' > '+e.parentElement.tagName+'.'+e.parentElement.className+' > '+e.parentElement.parentElement.className);}}
 return o.slice(0,3).join('\n');}));
await p.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>[document.body.className.slice(0,300),[...document.querySelectorAll('.elementor-location-header ~ * > *,main > *,.site-main > *')].slice(0,12).map(e=>e.tagName+'.'+e.className.slice(0,90)+' h='+Math.round(e.getBoundingClientRect().height)+' '+e.innerText.replace(/\s+/g,' ').slice(0,60)).join('\n')].join('\n')));
await b.close();})();
