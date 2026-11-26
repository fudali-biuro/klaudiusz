const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
const a=p.locator('.elementor-location-header .elementor-nav-menu--main a',{hasText:/^\s*Sklep/i}).first();const bb=await a.boundingBox();
await p.mouse.move(bb.x+bb.width/2,bb.y+bb.height/2);await p.waitForTimeout(500);
console.log(await p.evaluate(()=>{const s=document.querySelector('.elementor-location-header ul.sub-menu');const li=s.parentElement;const c=getComputedStyle(s),lr=li.getBoundingClientRect(),sr=s.getBoundingClientRect();return 'mt:'+c.marginTop+' top:'+c.top+' inline:'+s.getAttribute('style')+' li:'+Math.round(lr.top)+'-'+Math.round(lr.bottom)+' sub:'+Math.round(sr.top)+' liPos:'+getComputedStyle(li).position}));
await b.close();})();
