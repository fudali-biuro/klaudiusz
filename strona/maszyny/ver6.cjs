const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
const a=p.locator('.elementor-location-header .elementor-nav-menu--main a',{hasText:/^\s*Sklep/i}).first();const bb=await a.boundingBox();
await p.mouse.move(bb.x+bb.width/2,bb.y+bb.height/2);await p.waitForTimeout(400);
const it=p.locator('.elementor-location-header ul.sub-menu a',{hasText:'Maszyny budowlane'}).first();const ib=await it.boundingBox();console.log('gap sklep->sub:',Math.round(await p.evaluate(()=>document.querySelector('.elementor-location-header ul.sub-menu').getBoundingClientRect().top)-(bb.y+bb.height)));
const tx=ib.x+40,ty=ib.y+ib.height/2;let sx=bb.x+bb.width/2,sy=bb.y+bb.height/2;
for(let i=1;i<=40;i++){await p.mouse.move(sx+(tx-sx)*i/40,sy+(ty-sy)*i/40);await p.waitForTimeout(40);}
console.log('open after slow move:',await p.evaluate(()=>getComputedStyle(document.querySelector('.elementor-location-header ul.sub-menu')).display));
await p.screenshot({path:S+'sub2.png',clip:{x:250,y:20,width:520,height:380}});
await Promise.all([p.waitForNavigation({timeout:8000}).catch(()=>null),p.mouse.click(tx,ty)]);console.log('url',p.url());
await b.close();})();
