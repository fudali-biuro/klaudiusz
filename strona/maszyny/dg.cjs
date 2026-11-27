const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));const bad=[];p.on('response',r=>{if(r.status()>=400&&/\.css|\.js/.test(r.url()))bad.push(r.status()+' '+r.url())});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log('css links:',await p.evaluate(()=>[...document.querySelectorAll('link[rel=stylesheet]')].map(l=>l.href).filter(h=>/post-|elementor/.test(h)).map(h=>h.split('/').pop()).join(' ')));
console.log('inline post css:',await p.evaluate(()=>[...document.querySelectorAll('style')].map(s=>s.id).filter(Boolean).join(' ')));
console.log('bad',bad.join('\n'),'errs',errs.join(' / '));
console.log(await p.evaluate(()=>['78da94c0','4928af29','43ab56f1'].map(id=>{const e=document.querySelector('.elementor-element-'+id);return id+' cls:'+e.className.slice(0,140)+' txt:'+e.innerText.slice(0,60)}).join('\n')));
await b.close();})();
