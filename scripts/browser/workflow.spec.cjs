const {test,expect}=require('@playwright/test');
const path=require('node:path');
const fs=require('node:fs');
const out=path.resolve(__dirname,'../../submission/screenshots');fs.mkdirSync(out,{recursive:true});
test('Owner workflow: detect gap, reminder without cash, edit approval, reschedule and inspect evidence',async({page,request})=>{
  const headers={'X-Demo-User':'owner'};
  const before=await (await request.get('/api/businesses/retail/dashboard',{headers})).json();
  await page.goto('/');
  await expect(page.getByRole('heading',{level:1})).toBeVisible();
  const consent=page.getByRole('button',{name:/Enter sandbox/i});if(await consent.isVisible())await consent.click();
  await expect(page.getByText('Available cash',{exact:true})).toBeVisible();
  await page.screenshot({path:path.join(out,'overview-desktop.png'),fullPage:true});
  await page.getByRole('button',{name:'Recovery agent',exact:true}).click();
  await page.getByRole('button',{name:/Generate recovery plan/i}).click();
  await expect(page.getByText('deterministic_demo',{exact:false}).first()).toBeVisible();
  const inspect=page.getByRole('button',{name:/Inspect action/i});await expect(inspect.first()).toBeVisible();
  await inspect.first().click();
  await page.getByRole('button',{name:/Approve exact action/i}).click();
  await Promise.all([page.waitForResponse(r=>r.url().endsWith('/execute')&&r.status()===200),page.getByRole('button',{name:/Execute in sandbox/i}).click()]);
  await expect(page.getByRole('dialog')).toHaveCount(0);
  const after=await (await request.get('/api/businesses/retail/dashboard',{headers})).json();
  expect(after.current_cash).toBe(before.current_cash);expect(after.verification.status).not.toBe('resolved');
  await page.getByRole('button',{name:/Inspect action/i}).nth(1).click();
  await page.getByRole('button',{name:/Approve exact action/i}).click();
  await page.getByLabel('New payment date').fill('2026-11-04');
  await page.getByRole('button',{name:'Save changes',exact:true}).click();
  await expect(page.getByRole('button',{name:/Approve exact action/i})).toBeVisible();
  await page.getByRole('button',{name:/Approve exact action/i}).click();
  await Promise.all([page.waitForResponse(r=>r.url().endsWith('/execute')&&r.status()===200),page.getByRole('button',{name:/Execute in sandbox/i}).click()]);
  await expect(page.getByRole('dialog')).toHaveCount(0);
  const deferred=await (await request.get('/api/businesses/retail/dashboard',{headers})).json();
  expect(deferred.minimum_balance).toBeGreaterThan(before.minimum_balance);
  const dismiss=page.getByRole('button',{name:'Dismiss notification'});if(await dismiss.isVisible())await dismiss.click();
  await page.screenshot({path:path.join(out,'recovery-desktop.png'),fullPage:true});
  await page.getByRole('button',{name:'Audit trail',exact:true}).click();
  await expect(page.getByText('sandbox executed',{exact:false}).first()).toBeVisible();
  await page.screenshot({path:path.join(out,'audit-desktop.png'),fullPage:true});
});
test('Navigation, financial details, financing, security and recorded paired scenarios',async({page})=>{
  await page.goto('/');
  const consent=page.getByRole('button',{name:/Enter sandbox/i});if(await consent.isVisible())await consent.click();
  for(const name of ['Cash-flow analysis','Financing','Security center','Evaluation lab']){
    await page.getByRole('button',{name,exact:true}).click();
    await expect(page.getByRole('heading',{level:1})).toHaveText(name);
    await expect(page.locator('.error[role="alert"]')).toHaveCount(0);
    if(name==='Financing')await expect(page.getByRole('heading',{name:'Calculation assumptions'})).toBeVisible();
    if(name==='Security center')await expect(page.getByRole('heading',{name:'Authority is checked independently.'})).toBeVisible();
    if(name==='Cash-flow analysis')await expect(page.getByRole('heading',{name:'Scheduled obligations'})).toBeVisible();
    if(name==='Evaluation lab'){
      await expect(page.getByLabel('Evaluation scenario')).toBeVisible();
      await page.getByLabel('Evaluation scenario').selectOption({index:17});
      await expect(page.getByText('Ungated baseline',{exact:true}).last()).toBeVisible();
    }
    await page.screenshot({path:path.join(out,name.toLowerCase().replaceAll(' ','-')+'-desktop.png'),fullPage:true});
  }
  await page.getByLabel('Business scenario').selectOption('services');
  await page.getByRole('button',{name:'Overview',exact:true}).click();
  await expect(page.locator('.overview-meta strong')).toHaveText('Willow Studio Services (synthetic)');
});
test('Read-only API restrictions and mobile layout',async({page,request})=>{
  const r=await request.post('/api/businesses/retail/proposals',{headers:{'X-Demo-User':'viewer'},data:{}});expect(r.status()).toBe(403);
  const list=await (await request.get('/api/businesses/retail/dashboard',{headers:{'X-Demo-User':'owner'}})).json();
  if(list.proposals.length){const denied=await request.post('/api/proposals/'+list.proposals[0].id+'/execute',{headers:{'X-Demo-User':'viewer'}});expect(denied.status()).toBe(403)}
  await page.setViewportSize({width:375,height:900});await page.goto('/');
  await expect(page.getByRole('heading',{level:1})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  await page.screenshot({path:path.join(out,'overview-mobile.png'),fullPage:true});
});
test('Owner rejects a proposal and explicitly records a partial sandbox receipt',async({page,request})=>{
  const headers={'X-Demo-User':'owner'};
  const before=await (await request.get('/api/businesses/retail/dashboard',{headers})).json();
  await page.goto('/');
  const consent=page.getByRole('button',{name:/Enter sandbox/i});if(await consent.isVisible())await consent.click();
  await page.getByRole('button',{name:'Recovery agent',exact:true}).click();
  await page.getByRole('button',{name:/Generate recovery plan/i}).click();
  await expect(page.locator('.proposal')).toHaveCount(4);
  await page.getByRole('button',{name:/Inspect action/i}).nth(2).click();
  await page.screenshot({path:path.join(out,'approval-dialog-desktop.png'),fullPage:false});
  await page.getByRole('button',{name:'Reject',exact:true}).click();
  await expect(page.getByRole('dialog').getByText('rejected',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Close proposal'}).click();
  await page.getByRole('button',{name:/^Approvals/}).click();
  const invoice=before.invoices.find(i=>i.amount>i.paid&&i.id==='retail-I1');
  await page.getByLabel('Receipt invoice').selectOption(invoice.id);
  await page.getByLabel('Receipt amount').fill('100.25');
  await Promise.all([page.waitForResponse(r=>r.url().endsWith('/receipts')&&r.status()===200),page.getByRole('button',{name:'Record receipt',exact:true}).click()]);
  const after=await (await request.get('/api/businesses/retail/dashboard',{headers})).json();
  expect(after.current_cash).toBe(before.current_cash+100.25);
  expect(after.invoices.find(i=>i.id===invoice.id).paid).toBe(invoice.paid+100.25);
  expect(after.verification.status).not.toBe('resolved');
});
