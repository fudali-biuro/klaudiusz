const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
const p=await b.newPage({viewport:{width:390,height:844}});
await p.goto('https://www.fudali.com.pl/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const o=[];const h=document.querySelector('.elementor-element-a1c0de11');let e=h;for(let i=0;i<4&&e;i++){const r=e.getBoundingClientRect();o.push(e.className.toString().slice(0,60)+' L'+Math.round(r.left)+' R'+Math.round(r.right)+' W'+Math.round(r.width));e=e.parentElement}
const m=document.querySelector('.elementor-element-1543179');o.push('MENUCOL '+m.innerHTML.replace(/\s+/g,' ').replace(/data-[a-z_-]+="[^"]*"/g,'').slice(0,700));
o.push('SECS '+[...document.querySelectorAll('[data-elementor-type="wp-page"] > .elementor-element')].map(s=>{const r=s.getBoundingClientRect();return (s.dataset.id)+':L'+Math.round(r.left)+'R'+Math.round(r.right)}).join(' '));return o.join('\n')}));
await p.screenshot({path:S+'mob-top.png'});await b.close();})();
