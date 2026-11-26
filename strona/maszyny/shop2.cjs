const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('https://www.fudali.com.pl/sklep/',{waitUntil:'networkidle'});
const link=await p.evaluate(()=>{const a=[...document.querySelectorAll('a')].map(a=>a.href).filter(h=>/fudali\.com\.pl\/(produkt|product)\//.test(h));return a[0]});console.log('link',link);
console.log(await p.evaluate(()=>[...document.querySelectorAll('footer a,.elementor-location-footer a')].map(a=>a.innerText.trim()).filter(Boolean).join(' | ')));
await p.screenshot({path:S+'shop2-top.png'});
if(link){await p.goto(link,{waitUntil:'networkidle'});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}window.scrollTo(0,0);});
await p.screenshot({path:S+'prod-d.png',fullPage:true});
console.log(await p.evaluate(()=>[...document.querySelectorAll('body > .elementor > *, [data-elementor-type] > *')].slice(0,14).map(e=>e.tagName+'.'+e.className.slice(0,60)+' h='+Math.round(e.getBoundingClientRect().height)+' '+e.innerText.replace(/\s+/g,' ').slice(0,50)).join('\n')));}
await b.close();})();
