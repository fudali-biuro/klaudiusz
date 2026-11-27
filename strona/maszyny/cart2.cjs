const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});const p=await c.newPage();
await p.goto('https://www.fudali.com.pl/?add-to-cart=2146',{waitUntil:'networkidle'});
await p.goto('https://www.fudali.com.pl/koszyk/',{waitUntil:'networkidle'});await p.waitForTimeout(1200);
console.log(await p.evaluate(()=>{const h=[...document.querySelectorAll('h2')].find(x=>/INTERESTED/i.test(x.innerText));let e=h,o=[];for(let i=0;i<9&&e;i++){const r=e.getBoundingClientRect(),cs=getComputedStyle(e);o.push(e.tagName+'.'+e.className.toString().slice(0,70)+' L'+Math.round(r.left)+' W'+Math.round(r.width)+' ml:'+cs.marginLeft+' tr:'+cs.transform+' pos:'+cs.position+' left:'+cs.left+' disp:'+cs.display+' gtc:'+cs.gridTemplateColumns);e=e.parentElement}return o.join('\n')}));
await b.close();})();
