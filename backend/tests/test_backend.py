from copy import deepcopy
from datetime import datetime,timezone,timedelta
from decimal import Decimal
import json
import pytest
from fastapi.testclient import TestClient
from app.engine import *
from app.generator import generate
from app import storage
from sqlalchemy.orm import Session

def test_reproducible_reconciled_data():
    data=generate(); assert data==generate()
    for b in data:
        running=money(b['opening_balance'])
        for t in b['ledger']:
            running+=money(t['amount']); assert running>=0
        assert running==money(b['current_cash'])
        for i in b['invoices']:
            assert i['issued_date']<=i['due_date']; assert 0<=i['paid']<=i['amount']
            receipts=sum((money(t['amount']) for t in b['ledger'] if t.get('invoice_id')==i['id']),money(0))
            assert receipts==money(i['paid'])
def test_reference_scenarios():
    retail,manufacturer,services=generate()
    assert forecast(retail)['minimum_balance']<0
    assert forecast(retail)['shortfall_date']=='2026-10-28'
    assert forecast(services)['minimum_balance']>=0
    assert forecast(manufacturer)['minimum_balance']<forecast(retail)['minimum_balance']

def test_forecast_reminder_does_not_add_cash():
    b=generate()[0]; before=deepcopy(b); i=b['invoices'][-3]
    execute_sandbox(b,dict(type='invoice_reminder',target_id=i['id'],recipient=i['recipient']))
    assert b==before; assert forecast(b)==forecast(before); assert len(forecast(b)['forecast'])==14
    assert verify_outcome(b)['status']!='resolved'
def test_financing_exact():
    option=financing(10000)['options'][0]
    assert option['interest']==69.86; assert option['total_cost']==169.86; assert option['total_repayment']==10169.86
@pytest.mark.parametrize('value',['NaN','Infinity','-Infinity'])
def test_nonfinite_money(value):
    with pytest.raises(ValueError): money(value)
def test_audit_tampering(tmp_path):
    e=storage.connect(str(tmp_path/'audit.sqlite'))
    with Session(e) as s:
        storage.append_audit(s,'example'); storage.append_audit(s,'example2'); s.commit(); assert storage.integrity(s)==dict(valid=True,count=2)
        row=s.get(storage.Audit,1); row.payload='{}'; s.commit(); assert not storage.integrity(s)['valid']
def test_api_full_workflow(tmp_path,monkeypatch):
    from app import main
    monkeypatch.delenv('OPENROUTER_API_KEY',raising=False)
    monkeypatch.setenv('FLOWGUARD_DATA_DIR',str(tmp_path))
    e=storage.connect(str(tmp_path/'api.sqlite')); monkeypatch.setattr(main,'engine',e)
    with Session(e) as s:
        for b in generate(): storage.put(s,b['id'],'business',b)
        s.commit()
    client=TestClient(main.app,headers={'X-Demo-User':'owner'})
    assert client.post('/api/businesses/retail/proposals',json={},headers={'X-Demo-User':'viewer'}).status_code==403
    result=client.post('/api/businesses/retail/proposals',json={}).json(); assert result['mode']=='deterministic_demo'
    reminder,expense=result['proposals']; rid=reminder['id']; eid=expense['id']
    assert client.post(f'/api/proposals/{rid}/execute').status_code==403
    assert client.post(f'/api/proposals/{rid}/approve').status_code==200
    before=client.get('/api/businesses/retail/dashboard').json()
    response=client.post(f'/api/proposals/{rid}/execute'); assert response.status_code==200,response.text
    assert response.json()['verification']['status']!='resolved'
    assert client.post(f'/api/proposals/{rid}/execute').json()['proposal']['execution']==response.json()['proposal']['execution']
    assert client.get('/api/businesses/retail/dashboard').json()['current_cash']==before['current_cash']
    assert client.post(f'/api/proposals/{eid}/approve').status_code==200
    assert client.patch(f'/api/proposals/{eid}',json={'message':'Edited terms'}).json()['status']=='proposed'
    assert client.post(f'/api/proposals/{eid}/execute').status_code==403
    client.post(f'/api/proposals/{eid}/approve'); r=client.post(f'/api/proposals/{eid}/execute'); assert r.status_code==200,r.text
    after=client.get('/api/businesses/retail/dashboard').json(); assert after['minimum_balance']>before['minimum_balance']
    assert client.post('/api/businesses/retail/receipts',json={'invoice_id':reminder['target_id'],'amount':100}).status_code==200
    assert client.post('/api/businesses/retail/receipts',json={'invoice_id':reminder['target_id'],'amount':999999}).status_code==422
    assert client.get('/api/audit').json()['integrity']['valid']
    assert client.post(f'/api/proposals/{eid}/execute',headers={'X-Demo-User':'analyst'}).status_code==403

def test_policy_boundary():
    b=generate()[0]; e=b['expenses'][0]; action=dict(business_id=b['id'],type='expense_reschedule',target_id=e['id'],amount=e['amount'],new_date='2026-11-03',recipient=None,message='Move',reason='Demo')
    ctx=dict(role='owner',approved=True,approved_hash=payload_hash(action),business=b,now='2026-10-16T12:00:00+00:00',mandate=dict(active=True,expires='2026-10-16T12:30:00+00:00',business_id=b['id'],types=['expense_reschedule'],amount_limit=50000,vendors=[e['vendor']],max_delay_days=30))
    assert policy_check(action,ctx)['allowed']
    for key,value in [('role','viewer'),('consumed',True),('now','2026-10-16T13:00:00+00:00')]:
        changed=deepcopy(ctx); changed[key]=value; assert not policy_check(action,changed)['allowed']
    payroll=b['expenses'][3]; bad={**action,'target_id':payroll['id'],'amount':payroll['amount']}; ctx['approved_hash']=payload_hash(bad); assert not policy_check(bad,ctx)['allowed']

def test_jsonl_append_integrity_and_truncation(tmp_path,monkeypatch):
    monkeypatch.setenv('FLOWGUARD_DATA_DIR',str(tmp_path))
    e=storage.connect(str(tmp_path/'mirror.sqlite'))
    with Session(e) as session:
        storage.append_audit(session,'first'); session.commit(); assert storage.export_audit(session)['valid']
        path=tmp_path/'audit.jsonl'; first=path.read_bytes()
        storage.append_audit(session,'second'); session.commit(); assert storage.export_audit(session)['valid']
        assert path.read_bytes().startswith(first); assert storage.full_integrity(session)['valid']
        path.write_bytes(first)
        assert not storage.full_integrity(session)['valid']
        assert not storage.export_audit(session)['valid']; assert path.read_bytes()==first
        path.write_text('{}\n',encoding='utf-8'); assert not storage.mirror_integrity(session)['valid']
        path.unlink(); assert not storage.mirror_integrity(session)['valid']

def test_reset_rejects_external_paths(tmp_path,monkeypatch):
    from app.reset import reset
    monkeypatch.setenv('FLOWGUARD_DATA_DIR',str(tmp_path))
    with pytest.raises(ValueError,match='inside project/data'): reset(True)
    with pytest.raises(ValueError,match='confirm'): reset(False)


def test_reset_repeat_keeps_backups(monkeypatch):
    from app.reset import reset
    from pathlib import Path
    from uuid import uuid4
    import shutil
    directory=storage.ROOT/'data'/('reset-test-'+uuid4().hex)
    monkeypatch.setenv('FLOWGUARD_DATA_DIR',str(directory))
    monkeypatch.delenv('FLOWGUARD_DB',raising=False)
    try:
        first=reset(True); second=reset(True); third=reset(True)
        assert Path(second['backup'],'flowguard.sqlite').is_file()
        assert Path(third['backup'],'audit.jsonl').is_file()
        assert second['backup']!=third['backup']
        engine=storage.connect(str(directory/'flowguard.sqlite'))
        with Session(engine) as session:
            assert len(storage.all_records(session,'business'))==3
            assert storage.full_integrity(session)['valid']
        engine.dispose()
    finally:
        shutil.rmtree(directory)
