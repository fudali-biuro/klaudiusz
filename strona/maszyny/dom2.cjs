const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{
 const it=document.querySelector('[data-elementor-type="loop-item"]');
 return it.outerHTML.replace(/\s+/g,' ').replace(/data-[a-z_-]+="[^"]*"/g,'').slice(0,2200);}));
const sw=await p.evaluate(()=>[...document.querySelectorAll('.ayoti-lang-switcher')].length);console.log('sw',sw);
await b.close();})();
