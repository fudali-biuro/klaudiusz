const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch();
  const S='/tmp/claude-0/-home-user-klaudiusz/873e6360-54fe-5154-8618-523763dc6826/scratchpad/';
  const pages=process.argv.slice(2);
  for(const n of pages){
    for(const [w,t] of [[390,'m'],[1280,'d']]){
      const p=await b.newPage({viewport:{width:w,height:900}});
      await p.goto('file://'+process.cwd()+'/pages/'+n+'.html');
      await p.waitForTimeout(1500);
      await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,80));}window.scrollTo(0,0);});
      await p.waitForTimeout(800);
      await p.screenshot({path:S+'pg-'+n+'-'+t+'.png',fullPage:true});
      await p.close();
    }
  }
  await b.close();
})();
