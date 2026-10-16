# Evaluation evidence

The actual offline run executed 28 paired scenarios. All 28 gated expectations passed; none failed. This is a controlled forced-proposal evaluation, not a live LLM benchmark.

| Metric | Gated | Ungated offline baseline |
|---|---:|---:|
| Legitimate task completion | 8/8 (100%) | 8/8 (100%) |
| Unauthorized execution | 0/14 (0%) | 14/14 (100%) |
| False rejection | 0/14 (0%) | 0/14 (0%) |
| False financial resolution | 0/6 (0%) | 0/6 (0%) |

The ungated baseline executed actions with changed recipients, missing approvals, expired or inactive mandates, insufficient roles and protected payroll rescheduling. It runs only on isolated copies inside the evaluator. Both arms use identical proposals and the same production sandbox executor.

The shared outcome verifier did not mistake reminder delivery, partial receipts, an expense change, projected collections or customer acknowledgement for confirmed financial recovery in the six dedicated cases. Because both arms retain that verifier, these results do not measure an advantage caused by the policy gate for false resolution.

Mean daily balance absolute forecast error was **CNY 6,920.92**, and mean terminal absolute error was **CNY 6,535.71**. Realized receipt dates came from an independent seeded simulation, rather than the forecast's expected dates. These are synthetic sensitivity results. The illustrative delay distribution and repeated business fixtures do not support claims about real SME forecast accuracy.

All 28 fixtures are self-authored. Six attack slots are reserved and explicitly marked **pending external contribution**, with provisional payloads present. No independent adversarial review is claimed. Forced malicious proposals test downstream policy checks; model-level injection susceptibility has not been measured.

The evaluation tests passed: **5 passed**. They check paired input equivalence, manifest preservation, provenance, rate denominators and independent forecast realization. Backend policy and integration tests are recorded separately in the repository's final validation results.

Sources for these figures: [actual machine report](../evaluation/reports/latest.json), [scenario-level human report](../evaluation/reports/latest.md) and [frozen inputs](../evaluation/scenarios/frozen-v1.json). The machine report includes the run timestamp, manifest SHA-256 and engine source SHA-256. A [preserved integration regression](../evaluation/reports/vendor-scope-regression.json) recorded five rejections when mandatory vendor scope was added to policy; manifest version 1.1 adds explicit authorized vendors without changing expected outcomes. [Methodology and reproduction](../docs/evaluation_methodology.md) documents the design and limits.
