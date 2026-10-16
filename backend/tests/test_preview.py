from copy import deepcopy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import storage
from app.generator import generate


def test_forecast_preview_is_read_only_and_protects_payroll(tmp_path, monkeypatch):
    from app import main
    monkeypatch.delenv('OPENROUTER_API_KEY',raising=False)
    engine=storage.connect(str(tmp_path/'preview.sqlite'))
    monkeypatch.setattr(main,'engine',engine)
    monkeypatch.setenv('FLOWGUARD_DATA_DIR',str(tmp_path))
    with Session(engine) as session:
        for business in generate():storage.put(session,business['id'],'business',business)
        session.commit()
    owner=TestClient(main.app,headers={'X-Demo-User':'owner'})
    viewer=TestClient(main.app,headers={'X-Demo-User':'viewer'})
    reminder,expense=owner.post('/api/businesses/retail/proposals',json={}).json()['proposals']
    before=owner.get('/api/businesses/retail/dashboard').json()
    log_before=owner.get('/api/audit').json()['events']
    assert viewer.get(f"/api/proposals/{reminder['id']}/preview").json()['change']==0
    result=viewer.get(f"/api/proposals/{expense['id']}/preview").json()
    assert result['change']==28000 and result['proposed_minimum']==26000
    assert not result['approval_granted'] and result['confirmed_cash_change']==0
    assert owner.get('/api/businesses/retail/dashboard').json()==before
    assert owner.get('/api/audit').json()['events']==log_before
    assert owner.post(f"/api/proposals/{expense['id']}/execute").status_code==403
    payroll=deepcopy(expense);payroll['id']='protected-preview';payroll['target_id']='retail-E4'
    with Session(engine) as session:
        storage.put(session,payroll['id'],'proposal',payroll);session.commit()
    assert not viewer.get('/api/proposals/protected-preview/preview').json()['available']
    owner.patch(f"/api/proposals/{expense['id']}",json={'new_date':'invalid'})
    assert not viewer.get(f"/api/proposals/{expense['id']}/preview").json()['available']
