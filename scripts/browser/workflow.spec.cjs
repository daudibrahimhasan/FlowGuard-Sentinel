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
  await expect(page.getByRole('heading',{name:'Projected effect of the saved action'})).toBeVisible();
  await expect(page.getByText('Current forecast minimum',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:/Approve exact action/i}).click();
  await Promise.all([page.waitForResponse(r=>r.url().endsWith('/execute')&&r.status()===200),page.getByRole('button',{name:/Execute in sandbox/i}).click()]);
  await expect(page.getByRole('dialog')).toHaveCount(0);
  const after=await (await request.get('/api/businesses/retail/dashboard',{headers})).json();
  expect(after.current_cash).toBe(before.current_cash);expect(after.verification.status).not.toBe('resolved');
  await page.getByRole('button',{name:/Inspect action/i}).nth(1).click();
  await expect(page.getByText('Projected timing effect only. The expense remains payable; collections are uncertain.')).toBeVisible();
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
  await expect(page.getByLabel('Business scenario')).toHaveValue('services');
  await expect(page.getByLabel('Business scenario').locator('option:checked')).toHaveText('Willow Studio Services (synthetic)');
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
  await expect(page.getByText('Current forecast minimum',{exact:true})).toBeVisible();
  await page.screenshot({path:path.join(out,'approval-dialog-desktop.png'),fullPage:false,animations:'disabled'});
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
test('Command navigation, invoice filters, chart selection and mobile drawer work',async({page})=>{
  await page.goto('/');
  await expect(page.getByText('Available cash',{exact:true})).toBeVisible();
  await page.keyboard.press('Control+k');
  await page.getByLabel('Search workspace pages').fill('cash-flow');
  await page.getByLabel('Search workspace pages').press('Enter');
  await expect(page.getByRole('heading',{level:1})).toHaveText('Cash-flow analysis');
  await page.getByLabel('Invoice status').selectOption('paid');
  const table=page.getByRole('heading',{name:'Receivables behind the projection'}).locator('xpath=ancestor::section');
  await expect(table.getByText('paid',{exact:true}).first()).toBeVisible();
  await page.getByLabel('Search invoices').fill('not-a-real-customer');
  await expect(page.getByText('No invoices match these filters. Try another status or search.')).toBeVisible();
  await page.getByRole('button',{name:'Expected only',exact:true}).click();
  await expect(page.getByRole('button',{name:'Expected only',exact:true})).toHaveAttribute('aria-pressed','true');
  await page.getByRole('button',{name:'Collapse sidebar'}).click();
  await expect(page.locator('.workspace')).toHaveClass(/is-collapsed/);
  await page.setViewportSize({width:390,height:844});
  await page.getByRole('button',{name:'Open navigation'}).click();
  await page.getByRole('dialog').getByRole('button',{name:'Financing',exact:true}).click();
  await expect(page.getByRole('heading',{level:1})).toHaveText('Financing');
  await expect(page.getByRole('dialog')).toHaveCount(0);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
});
test('Changed recipient is blocked after approval and explained in Security center',async({page})=>{
  await page.goto('/');
  const consent=page.getByRole('button',{name:/Enter sandbox/i});if(await consent.isVisible())await consent.click();
  await page.getByRole('button',{name:'Recovery agent',exact:true}).click();
  await page.getByRole('button',{name:'Generate recovery plan'}).click();
  await expect(page.locator('.proposal')).toHaveCount(6);
  await page.getByRole('button',{name:/Inspect action/}).nth(4).click();
  await page.getByLabel('Reminder recipient').fill('unauthorized@external.example');
  await expect(page.getByRole('button',{name:'Approve exact action'})).toBeDisabled();
  await page.getByRole('button',{name:'Save changes'}).click();
  await page.getByRole('button',{name:'Approve exact action'}).click();
  await Promise.all([page.waitForResponse(r=>r.url().endsWith('/execute')&&r.status()===403),page.getByRole('button',{name:'Execute in sandbox'}).click()]);
  await page.getByRole('button',{name:'Close proposal'}).click();
  await expect(page.locator('.error')).toContainText('Recipient outside allowlist');
  await page.getByRole('button',{name:'Dismiss error'}).click();
  await page.getByRole('button',{name:'Security center',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Recent blocked actions'})).toBeVisible();
  await expect(page.getByText('policy_blocked',{exact:true})).toBeVisible();
});
test('A failed financial read can be retried without refreshing the page',async({page})=>{
  let fail=true;
  await page.route('**/api/businesses/retail/dashboard',async route=>{if(fail){fail=false;await route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({detail:'Financial records temporarily unavailable'})})}else await route.continue()});
  await page.goto('/');
  await expect(page.locator('.error')).toContainText('Financial records temporarily unavailable');
  await page.getByRole('button',{name:'Retry financial data'}).click();
  await expect(page.getByText('Available cash',{exact:true})).toBeVisible();
  await expect(page.locator('.error')).toHaveCount(0);
});

// Read-only component coverage, independent of the synthetic financial ledger.
test('Command keyboard selection, empty results, logo and collapsed tooltips',async({page})=>{
 await page.goto('/');
 await expect(page.locator('.sidebar .brand img')).toBeVisible();
 await page.getByRole('button',{name:'Open command palette'}).click();
 const search=page.getByRole('combobox',{name:'Search workspace pages'});
 await expect(search).toBeFocused();
 await search.press('ArrowDown');
 await search.press('Enter');
 await expect(page.getByRole('heading',{level:1})).toHaveText('Cash-flow analysis');
 await page.getByRole('button',{name:'Open command palette'}).click();
 await search.fill('zzzzmissing');
 await expect(page.getByText(/No pages match/)).toBeVisible();
 await search.press('Escape');
 await expect(page.getByRole('button',{name:'Open command palette'})).toBeFocused();
 await page.getByRole('button',{name:'Collapse sidebar'}).click();
 await page.getByRole('navigation').getByRole('button',{name:'Security center',exact:true}).focus();
 await expect(page.getByRole('tooltip')).toContainText('Security center');
 await page.screenshot({path:'../../submission/screenshots/component-navigation.png',animations:'disabled'});
});

// Browser-only records exercise the ledger without creating proposals or calling the LLM.
test('Approval ledger renders populated rows and opens a read-only preview',async({page,request})=>{
 const dashboard=await (await request.get('/api/businesses/retail/dashboard',{headers:{'X-Demo-User':'owner'}})).json();
 const invoice=dashboard.invoices.find(i=>i.amount>i.paid);
 const expense=dashboard.expenses.find(e=>e.flexible);
 const rows=[{id:'ui-preview-reminder',business_id:'retail',type:'invoice_reminder',target_id:invoice.id,recipient:invoice.recipient,amount:invoice.amount-invoice.paid,reason:'Read-only browser fixture: review an outstanding invoice.',message:'Payment reminder preview.',status:'proposed'},{id:'ui-preview-expense',business_id:'retail',type:'expense_reschedule',target_id:expense.id,amount:expense.amount,new_date:'2026-11-04',reason:'Read-only browser fixture: review an eligible obligation.',status:'proposed'}];
 await page.route('**/api/businesses/retail/dashboard',route=>route.fulfill({json:{...dashboard,proposals:rows}}));
 await page.route('**/api/proposals/ui-preview-*/preview',route=>route.fulfill({json:{available:false,reason:'Read-only visual fixture. No server proposal was created.'}}));
 await page.goto('/');
 await page.getByRole('navigation').getByRole('button',{name:'Approvals',exact:true}).click();
 await expect(page.locator('.proposal-table tbody tr')).toHaveCount(2);
 await expect(page.locator('.proposal-table')).toContainText(invoice.recipient);
 await page.screenshot({path:'../../submission/ramp-rebuild/approval-ledger-fixture-1440.png',animations:'disabled'});
 await page.getByRole('button',{name:'Inspect action'}).first().click();
 await expect(page.getByRole('dialog')).toContainText('Read-only visual fixture. No server proposal was created.');
 await page.getByRole('button',{name:'Close proposal'}).click();
 await page.setViewportSize({width:390,height:844});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
 await page.screenshot({path:'../../submission/ramp-rebuild/approval-ledger-fixture-390.png',animations:'disabled'});
});
