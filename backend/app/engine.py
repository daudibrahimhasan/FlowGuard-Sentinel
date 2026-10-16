from datetime import date, timedelta, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib, json
AS_OF = '2026-10-16'
PROTECTED = {'payroll','rent','tax','utilities'}
FIELDS = {'business_id','type','target_id','amount','recipient','new_date','message','reason'}
def money(x):
    value=Decimal(str(x))
    if not value.is_finite(): raise ValueError('Money must be finite')
    return value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
def payload_hash(action):
    return hashlib.sha256(json.dumps({k:action.get(k) for k in sorted(FIELDS)},sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def forecast(business):
    start=date.fromisoformat(business.get('as_of',AS_OF)); balance=money(business['current_cash']); conservative=balance; rows=[]
    for offset in range(1,15):
        day=start+timedelta(days=offset)
        inflow=sum((money(i['amount'])-money(i.get('paid',0)) for i in business['invoices'] if i.get('expected_date',i['due_date'])==day.isoformat()),Decimal(0))
        outflow=sum((money(e['amount']) for e in business['expenses'] if e['date']==day.isoformat()),Decimal(0))
        balance+=inflow-outflow; conservative-=outflow
        rows.append(dict(date=day.isoformat(),inflow=float(inflow),outflow=float(outflow),balance=float(balance),conservative_balance=float(conservative)))
    minimum=min(money(r['balance']) for r in rows); first=next((r['date'] for r in rows if r['balance']<0),None)
    return dict(forecast=rows,minimum_balance=float(minimum),shortfall_date=first,shortfall_amount=float(max(-minimum,Decimal(0))))
def policy_check(action,context):
    reasons=[]; mandate=context.get('mandate',{}); business=context.get('business',{}); kind=action.get('type'); today=date.fromisoformat(AS_OF)
    try: today=date.fromisoformat(context.get('now',AS_OF)[:10])
    except (ValueError,TypeError): reasons.append('Invalid execution timestamp')
    if context.get('role')!='owner': reasons.append('Owner execution permission required')
    if not context.get('approved') or context.get('approved_hash')!=payload_hash(action): reasons.append('Exact payload approval required')
    if context.get('consumed') or action.get('status')=='executed': reasons.append('Authorization already consumed')
    try:
        now_raw=context.get('now',AS_OF); now=datetime.fromisoformat(now_raw).replace(tzinfo=timezone.utc) if len(now_raw)==10 else datetime.fromisoformat(now_raw)
        if now.tzinfo is None: now=now.replace(tzinfo=timezone.utc)
        expiry=datetime.fromisoformat(mandate.get('expires','0001-01-01'))
        if expiry.tzinfo is None: expiry=expiry.replace(tzinfo=timezone.utc)
        if not mandate.get('active') or expiry<=now: reasons.append('Mandate inactive or expired')
    except (ValueError,TypeError): reasons.append('Invalid mandate expiry')
    if mandate.get('authorized_role','owner')!=context.get('role'): reasons.append('Mandate role mismatch')
    if mandate.get('authorized_user') and mandate['authorized_user']!=context.get('user',context.get('role')): reasons.append('Mandate user mismatch')
    if action.get('business_id')!=mandate.get('business_id'): reasons.append('Business outside mandate')
    if kind not in mandate.get('types',[]): reasons.append('Action type outside mandate')
    if set(action)-FIELDS-{'id','status','execution','approved_hash','approved_at','approval'}: reasons.append('Unexpected action parameters')
    try:
        amount=money(action.get('amount',0))
        if amount<=0 or amount>money(mandate.get('amount_limit',0)): reasons.append('Amount outside mandate limit')
    except Exception: amount=Decimal(0); reasons.append('Invalid amount')
    if kind=='invoice_reminder':
        target=next((i for i in business.get('invoices',[]) if i['id']==action.get('target_id')),None)
        if not target: reasons.append('Invoice not found')
        elif target['due_date']>=today.isoformat() or money(target['amount'])<=money(target.get('paid',0)): reasons.append('Invoice is not overdue and outstanding')
        elif amount!=money(target['amount'])-money(target.get('paid',0)): reasons.append('Invoice amount mismatch')
        if not target or action.get('recipient')!=target.get('recipient') or action.get('recipient') not in mandate.get('recipients',[]): reasons.append('Recipient outside allowlist')
        if action.get('new_date'): reasons.append('Reminder cannot reschedule payment')
    elif kind=='expense_reschedule':
        target=next((e for e in business.get('expenses',[]) if e['id']==action.get('target_id')),None)
        if not target: reasons.append('Expense not found')
        else:
            if target['category'] in PROTECTED.union(mandate.get('protected_categories',[])) or not target.get('flexible'): reasons.append('Protected or inflexible obligation')
            if amount!=money(target['amount']): reasons.append('Expense amount mismatch')
            if target.get('vendor') not in mandate.get('vendors',[]): reasons.append('Vendor outside allowlist')
            try:
                delta=(date.fromisoformat(action.get('new_date',''))-date.fromisoformat(target['date'])).days
                if not 1<=delta<=mandate.get('max_delay_days',30): reasons.append('Rescheduling outside allowed window')
            except Exception: reasons.append('Invalid reschedule date')
        if action.get('recipient'): reasons.append('Expense cannot change recipient')
    else: reasons.append('Unsupported executable action')
    return dict(allowed=not reasons,reasons=reasons)
def execute_sandbox(business,action):
    if action['type']=='invoice_reminder': return dict(status='simulated_delivery',target_id=action['target_id'],recipient=action['recipient'],cash_received=0)
    if action['type']=='expense_reschedule':
        target=next(e for e in business['expenses'] if e['id']==action['target_id']); old=target['date']; target['date']=action['new_date']
        return dict(status='rescheduled',target_id=target['id'],previous_date=old,new_date=target['date'])
    raise ValueError('Unsupported sandbox operation')
def verify_outcome(business,action=None):
    f=forecast(business); conservative=min(r['conservative_balance'] for r in f['forecast'])
    status='resolved' if conservative>=0 else 'projected_recovery' if f['minimum_balance']>=0 else 'unresolved'
    message={'resolved':'Scheduled obligations are covered by recorded cash. Future obligations and collection uncertainty remain.','projected_recovery':'Expected collections cover the forecast, but cash recovery is not yet observed.','unresolved':'A projected cash shortfall remains. Reminder delivery is not payment.'}[status]
    return dict(status=status,message=message,observed_cash=float(money(business['current_cash'])),minimum_balance=f['minimum_balance'],conservative_minimum=conservative)
def financing(principal):
    p=money(principal); options=[]
    for name,rate,fee,term in [('Illustrative bridge',Decimal('.085'),Decimal('.01'),30),('Illustrative working capital',Decimal('.105'),Decimal('.005'),60),('Illustrative invoice advance',Decimal('.12'),Decimal('.015'),45)]:
        interest=money(p*rate*term/365); fees=money(p*fee); total=p+interest+fees
        options.append(dict(name=name,principal=float(p),annual_rate=float(rate),fee=float(fees),term_days=term,interest=float(interest),total_repayment=float(total),total_cost=float(interest+fees),repayment_schedule=[dict(date=(date.fromisoformat(AS_OF)+timedelta(days=term)).isoformat(),amount=float(total))],projected_cash_effect=dict(initial_inflow=float(p),maturity_outflow=float(total),maturity_date=(date.fromisoformat(AS_OF)+timedelta(days=term)).isoformat()),risk='Hypothetical bullet repayment; affordability depends on future collections. Not a credit offer.'))
    return dict(options=options,assumptions='Simulated CNY offers. Simple annual interest, ACT/365, financed fee paid with principal and interest at maturity; no compounding, no application or execution.')
