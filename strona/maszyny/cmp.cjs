const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const g=(sel,props)=>{const e=document.querySelector(sel);if(!e)return'none';const c=getComputedStyle(e),r=e.getBoundingClientRect();return props.map(p=>p+':'+c[p]).join(' ')+' W'+Math.round(r.width)+' H'+Math.round(r.height)};
for(const [u,root] of [['o-firmie','.elementor-element-a6000001'],['','.elementor-element-802c4aa']]){
const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto('https://www.fudali.com.pl/'+u,{waitUntil:'networkidle'});
console.log(u||'home',await p.evaluate(([root,gs])=>{const g=eval(gs);const R=document.querySelector(root);const f=s=>{const e=R.querySelector(s);if(!e)return'none';const c=getComputedStyle(e),r=e.getBoundingClientRect();return ['fontSize','fontWeight','letterSpacing','color','backgroundColor','paddingTop','paddingBottom','paddingLeft','textTransform','textAlign','fontFamily','lineHeight','marginBottom','borderColor'].map(p=>p+':'+c[p]).join(' ')+' W'+Math.round(r.width)};
const rr=getComputedStyle(R);return ['ROOT bg:'+rr.backgroundColor+' pt:'+rr.paddingTop+' pb:'+rr.paddingBottom+' W'+Math.round(R.getBoundingClientRect().width),'H2 '+f('h2'),'ACC '+f('.elementor-accordion'),'ITEM '+f('.elementor-accordion-item'),'TITLE '+f('.elementor-tab-title'),'TA '+f('.elementor-tab-title a'),'CONT '+f('.elementor-tab-content'),'ICON '+f('.elementor-accordion-icon')].join('\n')},[root,'0']));await p.close();}
await b.close();})();
