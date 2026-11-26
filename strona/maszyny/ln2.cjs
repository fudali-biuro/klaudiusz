const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const w of [1440,390]){const p=await b.newPage({viewport:{width:w,height:900}});
await p.goto('https://www.fudali.com.pl/kontakt/',{waitUntil:'networkidle'});
console.log(w,await p.evaluate(()=>[...document.querySelectorAll('.elementor-location-footer .elementor-widget-divider')].map(d=>{const r=d.getBoundingClientRect(),s=d.querySelector('.elementor-divider-separator'),sr=s&&s.getBoundingClientRect();const pv=d.previousElementSibling;return d.dataset.id+' prev:'+(pv?pv.innerText.trim().slice(0,14):'-')+' wL'+Math.round(r.left)+' W'+Math.round(r.width)+' sepL'+(sr?Math.round(sr.left)+' W'+Math.round(sr.width):'')+' jc:'+(s?getComputedStyle(d.querySelector('.elementor-divider')).textAlign:'')}).join('\n')));await p.close();}
await b.close();})();
