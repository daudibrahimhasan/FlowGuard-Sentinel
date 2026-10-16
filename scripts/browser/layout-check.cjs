const {chromium}=require('@playwright/test');
const fs=require('node:fs');const path=require('node:path');
(async()=>{
 const browser=await chromium.launch();const out=path.resolve(__dirname,'../../submission/screenshots');
 const results=[];
 for(const width of [375,768,1440]){
  const page=await browser.newPage({viewport:{width,height:1000},reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:3000',{waitUntil:'networkidle'});await page.getByText('Available cash',{exact:true}).waitFor();
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
  await page.screenshot({path:path.join(out,`overview-${width}.png`),fullPage:true});
  results.push({width,overflow,page_errors:errors});await page.close();
 }
 fs.writeFileSync(path.resolve(__dirname,'../../submission/layout-results.json'),JSON.stringify(results,null,2));
 console.log(JSON.stringify(results));await browser.close();
 if(results.some(r=>r.overflow||r.page_errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
