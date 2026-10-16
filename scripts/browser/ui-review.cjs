const {chromium,expect}=require('@playwright/test');
const fs=require('node:fs');const path=require('node:path');
const out=path.resolve(__dirname,process.argv[2]||'../../submission/ui-review');fs.mkdirSync(out,{recursive:true});
const screens=['Overview','Cash-flow analysis','Recovery agent','Approvals','Financing','Security center','Evaluation lab','Audit trail'];
(async()=>{
 const browser=await chromium.launch();const results=[];
 try{
  for(const viewport of [{width:1440,height:900},{width:1280,height:800},{width:768,height:1024},{width:390,height:844}]){
   const page=await browser.newPage({viewport,reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto('http://127.0.0.1:3000',{waitUntil:'networkidle'});
   await expect(page.getByText('Available cash',{exact:true})).toBeVisible();
   const consent=page.getByRole('button',{name:'Enter sandbox'});if(await consent.isVisible())await consent.click();
   for(const screen of screens){
    if(screen!=='Overview'){
     if(viewport.width<651)await page.getByRole('button',{name:'Open navigation'}).click();
     const nav=viewport.width<651?page.getByRole('dialog').getByRole('navigation'):page.getByRole('navigation');
     await nav.getByRole('button',{name:screen==='Approvals'?/^Approvals/:screen,exact:screen!=='Approvals'}).click();
    }
    await expect(page.getByRole('heading',{level:1})).toHaveText(screen);
    await expect(page.locator('.loading')).toHaveCount(0);await page.waitForLoadState('networkidle');
    if(screen==='Evaluation lab'){await page.getByLabel('Evaluation scenario').selectOption({index:17});await expect(page.getByText('Blocked',{exact:true})).toBeVisible()}
    if(screen==='Audit trail'){await page.getByLabel('Audit event type').selectOption('policy')}
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
    const filename=`${screen.toLowerCase().replaceAll(' ','-')}-${viewport.width}.png`;
    await page.screenshot({path:path.join(out,filename),fullPage:true});
    results.push({screen,...viewport,overflow,page_errors:[...errors],request_error:await page.locator('.error').count(),screenshot:filename});
   }
   await page.close();
  }
  fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));
  console.log(JSON.stringify({screenshots:results.length,problems:results.filter(r=>r.overflow||r.page_errors.length||r.request_error)},null,2));
  if(results.some(r=>r.overflow||r.page_errors.length||r.request_error))process.exitCode=1;
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
