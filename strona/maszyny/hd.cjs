const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const ctx=await b.newContext({viewport:{width:1440,height:900}});const p=await ctx.newPage();
await p.goto('https://www.fudali.com.pl/?add-to-cart=2144&quantity=10',{waitUntil:'networkidle'});
for(const w of [1280,1440,1920]){await p.setViewportSize({width:w,height:700});await p.goto('https://www.fudali.com.pl/kontakt/',{waitUntil:'networkidle'});
const m=await p.evaluate(()=>{const h=document.querySelector('.elementor-element-6db7bdac');const r=e=>e?e.getBoundingClientRect():null;
const logo=r(h.querySelector('.elementor-element-5b93a8ba img'));const sk=[...h.querySelectorAll('a')].find(a=>/Sklep/i.test(a.textContent));const cart=r(h.querySelector('.elementor-menu-cart__toggle_button, .elementor-widget-woocommerce-menu-cart a'));const lang=r(h.querySelector('.ayoti-lang-item.is-active'));const o=r(h.querySelector('.elementor-element-58c8f92a .elementor-nav-menu'));
return {W:innerWidth,left:Math.round(r(sk).left),logoC:Math.round(logo.left+logo.width/2),cartR:Math.round(cart.right),langR:Math.round(lang.right),cartL:Math.round(cart.left)}});
console.log(JSON.stringify(m));await p.screenshot({path:S+'hd-'+w+'.png',clip:{x:0,y:0,width:w,height:120}});}
await b.close();})();
