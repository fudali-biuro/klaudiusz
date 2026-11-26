const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/produkt/stolik-boczny-platek-debowy/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(/Marka/.test(n.textContent)){let e=n.parentElement;return e.outerHTML.slice(0,200)+' || P: '+e.parentElement.tagName+'.'+e.parentElement.className}}}));
await b.close();})();
