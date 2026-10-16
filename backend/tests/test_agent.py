"""Mocked model transport tests: never access a real provider or key."""
import copy,json
import httpx
import pytest
from app import agent
from app.generator import generate
from app.engine import policy_check,payload_hash

class FakeClient:
    def __init__(self,responses,listing=None): self.responses=list(responses); self.listing=listing or []; self.posts=[]; self.gets=[]
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def get(self,url):
        self.gets.append(url)
        return httpx.Response(200,json={'data':self.listing},request=httpx.Request('GET',url))
    def post(self,url,**kwargs):
        self.posts.append((url,kwargs)); status,payload=self.responses.pop(0)
        return httpx.Response(status,json=payload,request=httpx.Request('POST',url))

def setup(monkeypatch,responses,model='openrouter/free',listing=None):
    client=FakeClient(responses,listing)
    monkeypatch.setenv('OPENROUTER_API_KEY','secret-test-token-never-real')
    monkeypatch.setenv('OPENROUTER_MODEL',model)
    monkeypatch.setenv('OPENROUTER_BASE_URL','https://openrouter.ai/api/v1')
    monkeypatch.setattr(agent.httpx,'Client',lambda **kwargs: client)
    return client

def completion(content): return {'choices':[{'message':{'content':content}}]}
def reply(): return json.dumps({'message':'Recorded overdue invoice can receive a reminder.','proposals':[{'type':'invoice_reminder','target_id':'retail-I1','recipient':'finance1@buyer.example','new_date':None,'amount':15000,'reason':'Overdue invoice','message':'Please confirm payment.'}]})

def test_valid_free_live_structured_mode(monkeypatch):
    client=setup(monkeypatch,[(200,completion(reply()))])
    result=agent.propose(generate()[0],'Explain')
    assert result['mode']=='live_openrouter'; assert result['proposals'][0]['amount']==15000
    body=client.posts[0][1]['json']; assert body['response_format']['type']=='json_schema'
    assert body['provider']['require_parameters']; assert not client.gets

@pytest.mark.parametrize('model,pricing',[('vendor/paid',{'prompt':'0','completion':'0'}),('vendor/name:free',{'prompt':'0','completion':'.0001'}),('vendor/name:free',{'prompt':'0'})])
def test_never_sends_unverified_or_paid_model(monkeypatch,model,pricing):
    client=setup(monkeypatch,[],model,[{'id':model,'pricing':pricing}])
    result=agent.propose(generate()[0]); assert result['mode']=='deterministic_demo'; assert len(client.gets)==1; assert client.posts==[]

def test_verified_free_model_selected(monkeypatch):
    model='vendor/test:free'; client=setup(monkeypatch,[(200,completion(reply()))],model,[{'id':model,'pricing':{'prompt':'0','completion':'0'}}])
    assert agent.propose(generate()[0])['mode']=='live_openrouter'; assert client.posts[0][1]['json']['model']==model

@pytest.mark.parametrize('content',['not json',json.dumps({'message':'Pretend approval','proposals':[],'execute':True})])
def test_malformed_response_labels_fallback(monkeypatch,content):
    setup(monkeypatch,[(200,completion(content))]); result=agent.propose(generate()[0])
    assert result['mode']=='deterministic_demo'; assert 'No live AI response' in result['message']

def test_rate_limit_bounded_no_secret_output(monkeypatch,capsys):
    client=setup(monkeypatch,[(429,{'error':'secret-test-token-never-real'}),(429,{'error':'secret-test-token-never-real'})])
    result=agent.propose(generate()[0]); assert len(client.posts)==2
    assert result['mode']=='deterministic_demo'; assert 'secret-test-token-never-real' not in json.dumps(result)
    captured=capsys.readouterr(); assert 'secret-test-token-never-real' not in captured.out+captured.err
    assert {p[1]['json']['model'] for p in client.posts}=={'openrouter/free'}

def test_model_context_minimized_and_bounded(monkeypatch):
    client=setup(monkeypatch,[(200,completion(reply()))]); business=generate()[0]
    business['invoices']*=40; business['expenses']*=30
    for invoice in business['invoices']: invoice['description']='x'*100000; invoice['bank_secret']='hidden-account'
    original=copy.deepcopy(business)
    agent.propose(business,'q'*10000)
    serialized=client.posts[0][1]['json']['messages'][1]['content']; request=json.loads(serialized); records=request['financial_records']
    assert len(records['invoices'])==8; assert len(records['expenses'])==20; assert len(request['question'])==2000
    assert max(len(i['description']) for i in records['invoices'])==1000
    assert 'hidden-account' not in serialized; assert len(serialized)<50000; assert business==original

def test_mandate_extra_protection_and_unknown_parameters():
    business=generate()[0]; expense=business['expenses'][0]
    action=dict(business_id=business['id'],type='expense_reschedule',target_id=expense['id'],amount=expense['amount'],new_date='2026-11-03',recipient=None,reason='test',message='test')
    context=dict(role='owner',approved=True,approved_hash=payload_hash(action),business=business,mandate=dict(active=True,expires='2026-12-31',business_id=business['id'],types=['expense_reschedule'],amount_limit=50000,vendors=[expense['vendor']],max_delay_days=30))
    assert policy_check(action,context)['allowed']
    context['mandate']['protected_categories']=['inventory']
    assert 'Protected or inflexible obligation' in policy_check(action,context)['reasons']
    context['mandate']['protected_categories']=[]; action['override_policy']=True
    assert 'Unexpected action parameters' in policy_check(action,context)['reasons']
