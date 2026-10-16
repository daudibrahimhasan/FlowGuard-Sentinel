from fastapi import FastAPI,HTTPException,Header,Depends
from pydantic import BaseModel,ConfigDict,Field
from sqlalchemy.orm import Session
from contextlib import contextmanager
from datetime import datetime,timezone,timedelta
import threading,uuid,json
from . import storage as db
from .engine import *
from .generator import generate
from .agent import propose
from dotenv import load_dotenv
load_dotenv(db.ROOT/'.env')
app=FastAPI(title='FlowGuard Sentinel sandbox'); engine=db.connect(); lock=threading.RLock()
IDENTITIES=[dict(id='owner',role='owner',permissions=['read','propose','approve','execute']),dict(id='analyst',role='analyst',permissions=['read','propose']),dict(id='viewer',role='viewer',permissions=['read'])]
def identity(x_demo_user:str=Header(default='viewer')):
    if x_demo_user not in {'owner','analyst','viewer'}: raise HTTPException(401,'Unknown demo identity')
    return x_demo_user
def authorize(user,roles):
    if user not in roles: raise HTTPException(403,'Identity lacks required permission')
def record_event(s,user,event,business_id=None,details=None):
    return db.append_audit(s,event,business_id,{**(details or {}),'actor':user})
def load(s,key):
    item=db.get(s,key)
    if item is None: raise HTTPException(404,'Record not found')
    return item
def mandate(b): return dict(active=True,authorized_role='owner',business_id=b['id'],types=['invoice_reminder','expense_reschedule'],amount_limit=50000,recipients=list({i['recipient'] for i in b['invoices']}),vendors=list({e['vendor'] for e in b['expenses'] if e['flexible']}),max_delay_days=30,expires='2026-12-31T23:59:59+00:00',protected_categories=sorted(PROTECTED))
def dashboard(s,b): return dict(business={k:v for k,v in b.items() if k not in {'ledger','invoices','expenses'}},current_cash=b['current_cash'],overdue_total=sum(i['amount']-i['paid'] for i in b['invoices'] if i['due_date']<AS_OF),**forecast(b),invoices=b['invoices'],expenses=b['expenses'],verification=verify_outcome(b),proposals=[p for p in db.all_records(s,'proposal') if p['business_id']==b['id']])
with Session(engine) as s:
    if not db.all_records(s,'business'):
        for b in generate(): db.put(s,b['id'],'business',b)
        record_event(s,'system','dataset_initialized',details={'seed':41,'as_of':AS_OF,'synthetic':True}); s.commit()
    db.export_audit(s)
class Ask(BaseModel):
    model_config=ConfigDict(extra='forbid')
    question:str=Field(default='',max_length=2000)
class Edit(BaseModel):
    model_config=ConfigDict(extra='forbid')
    new_date:str|None=Field(default=None,max_length=10)
    recipient:str|None=Field(default=None,max_length=254)
    message:str|None=Field(default=None,max_length=3000)
class Receipt(BaseModel):
    model_config=ConfigDict(extra='forbid')
    invoice_id:str
    amount:float=Field(gt=0,allow_inf_nan=False)
@app.get('/api/health')
def health(): return {'status':'ok','synthetic':True}
@app.get('/api/businesses')
def businesses(user=Depends(identity)):
    with Session(engine) as s: return [{k:b[k] for k in ('id','name','sector','scenario')} for b in db.all_records(s,'business')]
@app.get('/api/businesses/{bid}/dashboard')
def view(bid:str,user=Depends(identity)):
    with Session(engine) as s: return dashboard(s,load(s,bid))
@app.post('/api/businesses/{bid}/proposals')
def proposals(bid:str,body:Ask,user=Depends(identity)):
    authorize(user,{'owner','analyst'})
    with lock,Session(engine) as s:
        b=load(s,bid); result=propose(b,body.question); saved=[]
        for action in result['proposals']:
            p=dict(**action,id=str(uuid.uuid4()),business_id=bid,status='proposed',execution=None)
            db.put(s,p['id'],'proposal',p); saved.append(p); record_event(s,user,'proposal_created',bid,{'proposal_id':p['id'],'mode':result['mode'],'action':{k:p.get(k) for k in FIELDS}})
        s.commit(); db.export_audit(s); result['proposals']=saved; return result
@app.patch('/api/proposals/{pid}')
def edit(pid:str,body:Edit,user=Depends(identity)):
    authorize(user,{'owner','analyst'})
    with lock,Session(engine) as s:
        p=load(s,pid)
        if p['status'] in ('executed','rejected'): raise HTTPException(409,'Terminal proposal cannot be edited')
        p.update(body.model_dump(exclude_unset=True)); p['status']='proposed'; p.pop('approved_hash',None); p.pop('approval',None)
        db.put(s,pid,'proposal',p); record_event(s,user,'proposal_edited_approval_invalidated',p['business_id'],{'proposal_id':pid}); s.commit(); db.export_audit(s); return p

@app.get('/api/proposals/{pid}/preview')
def preview(pid:str,user=Depends(identity)):
    """Read-only financial scenario on a copy; never grants approval or executes."""
    from copy import deepcopy
    with Session(engine) as s:
        proposal=load(s,pid); business=load(s,proposal['business_id'])
        before=forecast(business); after=before
        note='Reminder delivery creates no cash. Customer payment is still uncertain.'
        if proposal['status'] in ('executed','rejected'):
            return dict(available=False,reason='Terminal actions have no pending financial preview.')
        if proposal['type']=='expense_reschedule':
            scope=mandate(business)
            target=next((e for e in business['expenses'] if e['id']==proposal['target_id']),None)
            if not target or not target['flexible'] or target['category'] in PROTECTED:
                return dict(available=False,reason='Protected or inflexible obligation cannot be deferred.')
            try:
                delay=(date.fromisoformat(proposal.get('new_date') or '')-date.fromisoformat(target['date'])).days
            except ValueError:
                return dict(available=False,reason='A valid saved payment date is required.')
            if not 1<=delay<=scope['max_delay_days'] or target['amount']>scope['amount_limit']:
                return dict(available=False,reason='Saved deferral exceeds the business policy limits.')
            scenario=deepcopy(business)
            next(e for e in scenario['expenses'] if e['id']==target['id'])['date']=proposal['new_date']
            after=forecast(scenario)
            note='Projected timing effect only. The expense remains payable; collections are uncertain.'
        elif proposal['type']!='invoice_reminder':
            return dict(available=False,reason='Unsupported action preview.')
        return dict(available=True,current_minimum=before['minimum_balance'],
                    proposed_minimum=after['minimum_balance'],
                    change=float(money(after['minimum_balance'])-money(before['minimum_balance'])),
                    confirmed_cash_change=0,note=note,approval_granted=False)
@app.post('/api/proposals/{pid}/approve')
def approve(pid:str,user=Depends(identity)):
    authorize(user,{'owner'})
    with lock,Session(engine) as s:
        p=load(s,pid)
        if p['status']!='proposed': raise HTTPException(409,'Only proposed actions may be approved')
        b=load(s,p['business_id']); digest=payload_hash(p); approval=mandate(b); approval.update(approved_hash=digest,approved_at=datetime.now(timezone.utc).isoformat(),expires=(datetime.now(timezone.utc)+timedelta(minutes=30)).isoformat(),consumed=False,authorized_user=user)
        p.update(status='approved',approved_hash=digest,approval=approval); db.put(s,pid,'proposal',p); record_event(s,user,'owner_approved',b['id'],{'proposal_id':pid,'payload_hash':digest,'expires':approval['expires'],'approved_parameters':{k:p.get(k) for k in FIELDS}}); s.commit(); db.export_audit(s); return p
@app.post('/api/proposals/{pid}/reject')
def reject(pid:str,user=Depends(identity)):
    authorize(user,{'owner'})
    with lock,Session(engine) as s:
        p=load(s,pid)
        if p['status']=='executed': raise HTTPException(409,'Executed action cannot be rejected')
        p['status']='rejected'; db.put(s,pid,'proposal',p); record_event(s,user,'owner_rejected',p['business_id'],{'proposal_id':pid}); s.commit(); db.export_audit(s); return p
@app.post('/api/proposals/{pid}/execute')
def execute(pid:str,user=Depends(identity)):
    authorize(user,{'owner'})
    with lock,Session(engine) as s:
        p=load(s,pid); b=load(s,p['business_id'])
        if p['status']=='executed': return dict(proposal=p,verification=verify_outcome(b),policy=dict(allowed=True,reasons=['Idempotent replay: existing execution returned']))
        approval=p.get('approval',{}); action={k:p.get(k) for k in FIELDS}
        policy=policy_check(action,dict(role=user,user=user,approved=p['status']=='approved',approved_hash=p.get('approved_hash'),mandate=approval,business=b,now=datetime.now(timezone.utc).isoformat(),consumed=approval.get('consumed',False)))
        record_event(s,user,'policy_allowed' if policy['allowed'] else 'policy_blocked',b['id'],{'proposal_id':pid,**policy})
        if not policy['allowed']: s.commit(); db.export_audit(s); raise HTTPException(403,detail=policy)
        p['execution']=execute_sandbox(b,action); p['status']='executed'; p['approval']['consumed']=True
        verification=verify_outcome(b,action); db.put(s,b['id'],'business',b); db.put(s,pid,'proposal',p); record_event(s,user,'sandbox_executed',b['id'],{'proposal_id':pid,'execution':p['execution']}); record_event(s,user,'outcome_verified',b['id'],verification); s.commit(); db.export_audit(s); return dict(proposal=p,verification=verification,policy=policy)
@app.post('/api/businesses/{bid}/receipts')
def receipt(bid:str,body:Receipt,user=Depends(identity)):
    authorize(user,{'owner'})
    with lock,Session(engine) as s:
        b=load(s,bid); invoice=next((i for i in b['invoices'] if i['id']==body.invoice_id),None)
        if not invoice: raise HTTPException(404,'Invoice not found')
        amount=money(body.amount); remaining=money(invoice['amount'])-money(invoice['paid'])
        if amount<=0: raise HTTPException(422,'Receipt must be at least CNY 0.01')
        if amount>remaining: raise HTTPException(422,'Receipt exceeds invoice balance')
        invoice['paid']=float(money(invoice['paid'])+amount); invoice['status']='paid' if amount==remaining else 'partial'; invoice['payment_date']=AS_OF
        b['current_cash']=float(money(b['current_cash'])+amount); b['ledger'].append(dict(id=str(uuid.uuid4()),date=AS_OF,amount=float(amount),kind='receipt',invoice_id=invoice['id'])); db.put(s,bid,'business',b); record_event(s,user,'sandbox_receipt_recorded',bid,{'invoice_id':invoice['id'],'amount':float(amount)}); s.commit(); db.export_audit(s); return dashboard(s,b)
@app.get('/api/businesses/{bid}/financing')
def compare(bid:str,user=Depends(identity)):
    with Session(engine) as s: b=load(s,bid); return financing(max(10000,forecast(b)['shortfall_amount']))
@app.get('/api/security')
def security(user=Depends(identity)):
    with Session(engine) as s: return dict(identities=IDENTITIES,mandates=[dict(proposal_id=p['id'],**p['approval'],approved_parameters={k:p.get(k) for k in FIELDS}) for p in db.all_records(s,'proposal') if p.get('approval')],standing_scopes=[mandate(b) for b in db.all_records(s,'business')],blocked=[e for e in db.audit_events(s) if e['event']=='policy_blocked'],protected_categories=sorted(PROTECTED),audit_integrity=db.full_integrity(s))
@app.get('/api/audit')
def audit(q:str='',user=Depends(identity)):
    with Session(engine) as s: return dict(events=[e for e in db.audit_events(s) if q.lower() in json.dumps(e).lower()],integrity=db.full_integrity(s))
@app.get('/api/evaluation')
def evaluation(user=Depends(identity)):
    from pathlib import Path
    path=db.ROOT/'evaluation/reports/latest.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'status':'unavailable','message':'Run the isolated evaluation to generate a report.'}
@app.post('/api/evaluation/run')
def evaluate(user=Depends(identity)):
    authorize(user,{'owner'})
    from .evaluation import run_evaluation
    return run_evaluation()
