const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const a=[...document.querySelectorAll('a')].filter(a=>/Zobacz sklep/i.test(a.innerText));return a.map(x=>x.className+' | parent:'+x.parentElement.className.slice(0,80)+' | gp:'+x.parentElement.parentElement.className.slice(0,80)).join('\n')}));
await b.close();})();
