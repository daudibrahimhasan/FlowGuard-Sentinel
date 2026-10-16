import json,hashlib,os
from datetime import datetime,timezone
from pathlib import Path
from sqlalchemy import create_engine,Column,String,Text,Integer,select
from sqlalchemy.orm import DeclarativeBase,Session
ROOT=Path(__file__).resolve().parents[2]
class Base(DeclarativeBase): pass
class Record(Base):
    __tablename__='records'
    key=Column(String,primary_key=True); kind=Column(String,index=True); value=Column(Text)
class Audit(Base):
    __tablename__='audit'
    id=Column(Integer,primary_key=True); payload=Column(Text); hash=Column(String); previous_hash=Column(String)
def connect(path=None):
    directory=Path(os.getenv('FLOWGUARD_DATA_DIR',str(ROOT/'data'))); directory.mkdir(parents=True,exist_ok=True)
    db=path or os.getenv('FLOWGUARD_DB',str(directory/'flowguard.sqlite'))
    engine=create_engine('sqlite:///'+db,connect_args={'check_same_thread':False}); Base.metadata.create_all(engine); return engine
def get(session,key):
    row=session.get(Record,key); return json.loads(row.value) if row else None
def put(session,key,kind,value):
    row=session.get(Record,key)
    if not row: row=Record(key=key,kind=kind); session.add(row)
    row.value=json.dumps(value,sort_keys=True); session.flush()
def all_records(session,kind): return [json.loads(r.value) for r in session.scalars(select(Record).where(Record.kind==kind))]
def append_audit(session,event,business_id=None,details=None):
    previous=session.scalars(select(Audit).order_by(Audit.id.desc())).first(); prior=previous.hash if previous else '0'*64
    payload=dict(timestamp=datetime.now(timezone.utc).isoformat(),event=event,business_id=business_id,details=details or {})
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')); digest=hashlib.sha256((prior+raw).encode()).hexdigest()
    row=Audit(payload=raw,hash=digest,previous_hash=prior); session.add(row); session.flush(); return row.id
def audit_events(session): return [dict(id=r.id,**json.loads(r.payload),hash=r.hash,previous_hash=r.previous_hash) for r in session.scalars(select(Audit).order_by(Audit.id))]
def integrity(session):
    prior='0'*64; count=0
    for row in session.scalars(select(Audit).order_by(Audit.id)):
        count+=1
        if row.previous_hash!=prior or row.hash!=hashlib.sha256((prior+row.payload).encode()).hexdigest(): return dict(valid=False,count=count)
        prior=row.hash
    return dict(valid=True,count=count)

def audit_paths():
    directory=Path(os.getenv('FLOWGUARD_DATA_DIR',str(ROOT/'data')))
    directory.mkdir(parents=True,exist_ok=True)
    return directory/'audit.jsonl',directory/'audit-checkpoint.json'

def mirror_integrity(session, require_complete=True):
    path,checkpoint=audit_paths(); expected=audit_events(session)
    try:
        actual=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()] if path.exists() else []
        marker=json.loads(checkpoint.read_text(encoding='utf-8')) if checkpoint.exists() else {'count':0}
        if len(actual)<marker['count']: return dict(valid=False,count=len(actual),reason='Audit JSONL truncation or deletion detected')
        if len(actual)>len(expected) or actual!=expected[:len(actual)]: return dict(valid=False,count=len(actual),reason='Audit JSONL differs from committed chain')
        if marker['count'] and (marker['count']>len(expected) or marker.get('hash')!=expected[marker['count']-1]['hash']): return dict(valid=False,count=len(actual),reason='Audit checkpoint differs from chain')
        if require_complete and len(actual)!=len(expected): return dict(valid=False,count=len(actual),reason='Committed events have not been mirrored')
        return dict(valid=True,count=len(actual))
    except (ValueError,KeyError,TypeError,OSError): return dict(valid=False,count=0,reason='Unreadable or malformed audit JSONL/checkpoint')

def full_integrity(session):
    sql=integrity(session); mirror=mirror_integrity(session)
    return dict(valid=sql['valid'] and mirror['valid'],count=sql['count'],database=sql,jsonl=mirror)

def export_audit(session):
    """Append committed events only; preserve and flag any corrupted existing log."""
    status=mirror_integrity(session,require_complete=False)
    if not status['valid']: return status
    events=audit_events(session); path,checkpoint=audit_paths()
    with path.open('a',encoding='utf-8',newline='\n') as stream:
        for event in events[status['count']:]: stream.write(json.dumps(event,sort_keys=True)+'\n')
        stream.flush(); os.fsync(stream.fileno())
    temporary=checkpoint.with_suffix('.tmp')
    temporary.write_text(json.dumps({'count':len(events),'hash':events[-1]['hash'] if events else '0'*64}),encoding='utf-8')
    temporary.replace(checkpoint)
    return mirror_integrity(session)
