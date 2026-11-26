const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
const a=p.locator('.elementor-location-header .elementor-nav-menu--main a',{hasText:/^\s*Sklep/i}).first();const bb=await a.boundingBox();await p.mouse.move(bb.x+bb.width/2,bb.y+bb.height/2);await p.waitForTimeout(900);
console.log(await p.evaluate(()=>{const s=document.querySelector('.elementor-element-1db07d26 .elementor-nav-menu--main .sub-menu');const c=getComputedStyle(s),r=s.getBoundingClientRect();return 'disp:'+c.display+' vis:'+c.visibility+' op:'+c.opacity+' pos:'+c.position+' top:'+Math.round(r.top)+' L'+Math.round(r.left)+' W'+Math.round(r.width)+' H'+Math.round(r.height)+' ml:'+c.marginLeft+' mt:'+c.marginTop+' z:'+c.zIndex+' bg:'+c.backgroundColor+' parent:'+s.parentElement.className}));
await p.screenshot({path:S+'sub.png',clip:{x:100,y:0,width:700,height:420}});await b.close();})();
