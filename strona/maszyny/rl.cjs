const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/realizacje/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const w=document.querySelector('.elementor-widget-gallery, [data-widget_type^="gallery"]');if(!w)return [...document.querySelectorAll('.elementor-widget')].map(x=>x.dataset.widget_type).join(',');const imgs=w.querySelectorAll('.e-gallery-item');const tags=[...w.querySelectorAll('.elementor-gallery-title')].map(t=>t.innerText+':'+t.dataset.galleryIndex);return w.dataset.widget_type+' id:'+w.dataset.id+' items:'+imgs.length+' tabs:'+tags.join(' | ')}));
await b.close();})();
