const {chromium}=require('@playwright/test');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
  const root=path.resolve(__dirname,'../..');
  const out=path.join(root,'submission/screenshots');fs.mkdirSync(out,{recursive:true});
  const browser=await chromium.launch({headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:3000',{waitUntil:'networkidle'});
  console.log((await page.locator('body').innerText()).slice(0,6500));
  await page.screenshot({path:path.join(out,'overview-desktop.png'),fullPage:true});
  console.log('ERRORS',JSON.stringify(errors));
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
