const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://www.fudali.com.pl/kontakt/',{waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{const hs=[...document.querySelectorAll('.elementor-location-footer .elementor-heading-title')];return hs.map(h=>{let o=h.innerText.trim()+': ';let e=h;for(let i=0;i<5&&e;i++){const a=getComputedStyle(e,'::after'),bf=getComputedStyle(e,'::before'),c=getComputedStyle(e);const r=e.getBoundingClientRect();o+='\n  '+e.tagName+'.'+e.className.toString().slice(0,45)+' L'+Math.round(r.left)+' W'+Math.round(r.width)+' bb:'+c.borderBottomWidth+' bg:'+(c.backgroundImage!=='none'?'img':'')+' af:'+a.content+'/'+a.width+'/'+a.marginLeft+'/'+a.left+' bf:'+bf.content+'/'+bf.width+'/'+bf.marginLeft+' ta:'+c.textAlign;e=e.parentElement}return o}).join('\n')}));
await b.close();})();
