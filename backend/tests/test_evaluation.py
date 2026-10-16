import copy
import json
from collections import Counter
from app import evaluation


def test_frozen_manifest_and_pending_provenance():
    manifest=json.loads(evaluation.MANIFEST.read_text(encoding='utf-8'))
    assert Counter(s['family'] for s in manifest['scenarios']) == {'legitimate':8,'unauthorized':8,'injection':6,'false_resolution':6}
    assert len({s['id'] for s in manifest['scenarios']}) == 28
    pending=[s for s in manifest['scenarios'] if s['provenance']['external_contribution']=='pending']
    assert len(pending)==6
    assert all(s['provenance']['author']=='Codex self-authored' for s in pending)


def test_paired_execution_uses_identical_inputs_and_shared_executor(monkeypatch):
    observed=[]
    original=evaluation.execute_sandbox
    def recording_executor(business,action):
        observed.append((copy.deepcopy(business),copy.deepcopy(action)))
        return original(business,action)
    monkeypatch.setattr(evaluation,'execute_sandbox',recording_executor)
    before=evaluation.MANIFEST.read_bytes()
    report=evaluation.run_evaluation(write_reports=False)
    assert report['failed']==0
    assert len(observed)==42 # 14 authorized + 28 baseline
    # Each legitimately authorized fixture executes consecutively on equal copies.
    cursor=0
    for row in report['scenarios']:
        if row['expected']['allowed']:
            assert observed[cursor]==observed[cursor+1]
            cursor+=2
        else:
            cursor+=1
    assert evaluation.MANIFEST.read_bytes()==before


def test_rates_count_actual_outcomes_and_verifier_is_shared():
    report=evaluation.run_evaluation(write_reports=False)
    assert report['metrics']['gated']['task_completion_rate']['numerator']==8
    assert report['metrics']['gated']['unauthorized_execution_rate']['numerator']==0
    assert report['metrics']['ungated']['unauthorized_execution_rate']['numerator']==14
    assert report['metrics']['gated']['false_rejection_rate']['numerator']==0
    for arm in ('gated','ungated'):
        assert report['metrics'][arm]['false_financial_resolution_rate']=={'numerator':0,'denominator':6,'rate':0}
    for row in report['scenarios']:
        if row['proposal']['type']=='invoice_reminder':
            for arm in ('gated','ungated'):
                if row['arms'][arm]['executed']:
                    assert row['arms'][arm]['execution']['cash_received']==0


def test_forecast_realization_is_reproducible_and_independent_of_predictions():
    business=json.loads(evaluation.MANIFEST.read_text())['scenarios'][0]['business']
    result=evaluation._forecast_error(business,42)
    assert result==evaluation._forecast_error(business,42)
    changed=copy.deepcopy(business)
    changed['invoices'][0]['expected_date']='2026-10-29'
    different=evaluation._forecast_error(changed,42)
    assert result['realized_receipts']==different['realized_receipts']
    assert [r['realized'] for r in result['daily']]==[r['realized'] for r in different['daily']]
    assert [r['predicted'] for r in result['daily']]!=[r['predicted'] for r in different['daily']]
    assert result['mae_cny']>0

def test_timestamp_expiry_and_scoped_identity_regression():
    scenario=json.loads(evaluation.MANIFEST.read_text())['scenarios'][0]
    action=scenario['proposal']
    context=copy.deepcopy(scenario['context'])
    context.update(business=scenario['business'],approved_hash=evaluation.payload_hash(action),now='2026-10-16T12:30:00+00:00',user='owner')
    context['mandate']['expires']='2026-10-16T12:29:59+00:00'
    assert not evaluation.policy_check(action,context)['allowed']
    context['mandate']['expires']='2026-10-16T13:00:00+00:00'
    assert evaluation.policy_check(action,context)['allowed']
    # Same instant expressed in a different timezone still expires.
    context['now']='2026-10-16T19:00:01+06:00'
    assert not evaluation.policy_check(action,context)['allowed']
    context['now']='2026-10-16T12:30:00+00:00'
    context['mandate']['authorized_user']='different-owner'
    assert not evaluation.policy_check(action,context)['allowed']
    context['mandate']['authorized_user']='owner'
    context['mandate']['authorized_role']='analyst'
    assert not evaluation.policy_check(action,context)['allowed']
