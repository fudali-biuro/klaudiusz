const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
await p.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const a=[...document.querySelectorAll('a')].find(x=>/wszystkie produkty/i.test(x.textContent));let e=a,o=[];for(let i=0;i<5&&e;i++){o.push(e.tagName+'.'+e.className.toString().slice(0,80)+' disp:'+getComputedStyle(e).display);e=e.parentElement}return o.join('\n')}));
await b.close();})();
