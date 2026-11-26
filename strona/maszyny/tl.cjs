const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const it=document.querySelector('.elementor-1861');const o=[];const q=(e,n)=>{const c=getComputedStyle(e),r=e.getBoundingClientRect();o.push(n+' '+e.tagName+'.'+e.className.toString().slice(0,60)+' H'+Math.round(r.height)+' disp:'+c.display+' fd:'+c.flexDirection+' jc:'+c.justifyContent+' ai:'+c.alignItems+' mh:'+c.minHeight)};
q(it,'item');const con=it.querySelector('.e-con');q(con,'con');const inner=it.querySelector('.e-con-inner');q(inner,'inner');inner.querySelectorAll(':scope > *').forEach((w,i)=>q(w,'w'+i));
o.push('slide85:'+[...document.querySelectorAll('.e-loop-item-85')].map(e=>getComputedStyle(e).display).join(','));o.push('styleLoop:'+(document.querySelector('style#loop-1861')||{textContent:''}).textContent.slice(0,600));return o.join('\n')}));
await b.close();})();
