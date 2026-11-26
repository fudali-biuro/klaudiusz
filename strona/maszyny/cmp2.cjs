const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const R=document.querySelector('.elementor-element-802c4aa');return [...R.querySelectorAll('.elementor-widget')].map(w=>w.dataset.widget_type+' '+w.dataset.id).join(' | ')+'\n'+R.querySelector('.elementor-widget:not(.elementor-widget-heading) ').outerHTML.replace(/\s+/g,' ').replace(/data-[a-z_-]+="[^"]*"/g,'').replace(/<svg.*?<\/svg>/g,'').slice(0,900)}));
await b.close();})();
