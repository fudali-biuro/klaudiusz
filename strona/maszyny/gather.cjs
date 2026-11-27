const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
async function scan(u){await p.goto('https://www.fudali.com.pl/'+u,{waitUntil:'networkidle'});await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,80));}});}
await scan('o-firmie/');
console.log('ABOUT');console.log(await p.evaluate(()=>[...document.querySelectorAll('[data-elementor-type="wp-page"] > *')].map(s=>s.dataset.id+' ['+Math.round(s.getBoundingClientRect().height)+'] '+s.innerText.replace(/\s+/g,' ').slice(0,900)).join('\n\n')));
console.log(await p.evaluate(()=>[...document.querySelectorAll('.elementor-element-a6000001 .elementor-tab-content')].map(c=>c.innerText.trim()).join('\n--\n')));
console.log(await p.evaluate(()=>[...document.querySelectorAll('.elementor-element-a6000001 .elementor-tab-title')].map(c=>c.innerText.trim()).join('\n')));
for(const u of ['','sklep/','kontakt/','realizacje/','produkt/stolik-boczny-platek-debowy/']){await scan(u);console.log('MENTIONS',u,await p.evaluate(()=>{const t=document.body.innerText;const m=[];const re=/[^.\n]{0,70}(opałow|kominkow|tarcic|desk[ia]\b|deski)[^.\n]{0,70}/gi;let x;while(x=re.exec(t))m.push(x[0].trim());return m.join(' || ')}));}
await b.close();})();
