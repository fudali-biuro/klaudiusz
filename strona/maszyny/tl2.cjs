const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const o=[];for(const s of document.querySelectorAll('style')){const t=s.textContent;let i=t.indexOf('e-loop-item-85');if(i>-1)o.push(s.id+' '+t.slice(Math.max(0,i-80),i+120));}
const e=document.querySelector('.e-loop-item-85');o.push('inline:'+e.getAttribute('style'));o.push('parent:'+e.parentElement.className+' '+e.parentElement.tagName);return o.join('\n')}));
await b.close();})();
