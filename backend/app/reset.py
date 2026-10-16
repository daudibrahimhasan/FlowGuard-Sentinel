"""Reset local synthetic state while preserving its previous files. Stop server first."""
import argparse,os,shutil,json
from datetime import datetime,timezone
from pathlib import Path
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from . import storage
from .generator import generate

def reset(confirm=False):
    if not confirm: raise ValueError('Pass --confirm to reset synthetic state; stop the backend server first.')
    load_dotenv(storage.ROOT/'.env')
    directory=Path(os.getenv('FLOWGUARD_DATA_DIR',str(storage.ROOT/'data'))).resolve()
    allowed=(storage.ROOT/'data').resolve()
    if directory!=allowed and allowed not in directory.parents: raise ValueError('Reset only supports data directories inside project/data')
    database=Path(os.getenv('FLOWGUARD_DB',str(directory/'flowguard.sqlite'))).resolve()
    if database.parent!=directory: raise ValueError('Database must be directly inside the configured project data directory')
    directory.mkdir(parents=True,exist_ok=True)
    backup=directory/'backups'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'); backup.mkdir(parents=True)
    targets=[database,Path(str(database)+'-wal'),Path(str(database)+'-shm'),directory/'audit.jsonl',directory/'audit-checkpoint.json']
    for target in targets:
        if target.exists(): shutil.copy2(target,backup/target.name)
    # Refuse a busy database instead of deleting live state.
    if database.exists():
        import sqlite3
        probe=sqlite3.connect(database,timeout=0)
        try:
            probe.execute('BEGIN EXCLUSIVE'); probe.rollback()
        finally:
            probe.close()
    for target in targets:
        if target.exists(): target.unlink()
    engine=storage.connect(str(database))
    with Session(engine) as session:
        for business in generate(): storage.put(session,business['id'],'business',business)
        storage.append_audit(session,'dataset_reset',details={'actor':'local_operator','seed':41,'synthetic':True,'backup':str(backup.relative_to(directory))})
        session.commit(); storage.export_audit(session)
    engine.dispose()
    return {'status':'reset','backup':str(backup),'database':str(database)}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--confirm',action='store_true'); args=parser.parse_args()
    print(json.dumps(reset(args.confirm),indent=2))
