const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
for(const u of ['maszyny-budowlane/','maszyny-budowlane/minikoparka/','maszyny-budowlane/shanmon-fuji-388/']){const r=await p.goto('https://www.fudali.com.pl/'+u,{waitUntil:'networkidle'});console.log(u,r.status(),(await p.title()).slice(0,50));}
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
await p.hover('.elementor-element-1db07d26 a[href*="/sklep/"]');await p.waitForTimeout(600);
console.log(await p.evaluate(()=>[...document.querySelectorAll('.elementor-element-1db07d26 .sub-menu a')].filter(a=>a.offsetParent).map(a=>a.innerText.trim()).join(' | ')));
console.log('top-level:',await p.evaluate(()=>[...document.querySelectorAll('.elementor-element-1db07d26 .elementor-nav-menu>li>a')].map(a=>a.innerText.trim()).join(' | ')));
await b.close();})();
