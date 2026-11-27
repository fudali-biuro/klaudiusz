const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/produkt/stolik-boczny-platek-debowy/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const s=document.querySelector('.elementor-element-3a76ce6 .elementor-widget-woocommerce-product-content, .elementor-element-3a76ce6 .woocommerce-Tabs-panel--description, .elementor-element-3a76ce6');return s.innerHTML.replace(/\s+/g,' ').replace(/data-[a-z_-]+="[^"]*"/g,'').slice(0,3500)}));
console.log(await p.evaluate(()=>[...document.querySelectorAll('table.woocommerce-product-attributes tr')].map(r=>r.innerText.replace(/\s+/g,' ')).join(' | ')));
await b.close();})();
