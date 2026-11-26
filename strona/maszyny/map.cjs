const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
const r=await p.evaluate(()=>[...document.querySelectorAll('[data-elementor-type="wp-page"] > .elementor-element, .elementor-location-header > .elementor-element')].map(e=>({id:e.dataset.id,t:e.dataset.element_type,cls:e.className.split(' ').filter(c=>c.startsWith('elementor-element-')).join(),h:Math.round(e.getBoundingClientRect().height),txt:e.innerText.replace(/\s+/g,' ').slice(0,110)})));
console.log(JSON.stringify(r,null,1));
await p.screenshot({path:'/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/home-d.png',fullPage:true});
await b.close();})();
