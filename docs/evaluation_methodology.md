# Evaluation methodology

FlowGuard Sentinel evaluates 28 frozen, self-authored scenarios: eight legitimate operations, eight authorization violations, six forced prompt-injection proposals and six false-resolution cases. The input manifest is [frozen-v1.json](../evaluation/scenarios/frozen-v1.json). It contains financial state, agent-visible context, proposal, approval payload, mandate, expected decisions, financial outcomes, criteria and authorship. Every run hashes the exact manifest bytes.

Manifest version 1.1 explicitly lists the two authorized flexible vendors. During integration, stricter default-deny vendor enforcement exposed five fixture rejections because the earlier fixture omitted its intended vendor scope. The failed run is preserved in [vendor-scope-regression.json](../evaluation/reports/vendor-scope-regression.json). Expected decisions were unchanged; the authorization input was corrected and the suite was frozen and rerun.

The fixture construction script is retained for review, but the runner reads the committed JSON rather than regenerating it. Expected outcomes are specified before execution. A failing expectation is a failure, not a reason to change the expected result. Deliberate future fixture changes require version control review and a new run.

## Paired comparison

Each scenario runs on separate deep copies of identical business state, proposed payload and approval context. The gated arm calls the production policy engine before execution. The ungated arm removes these policy checks and calls the same sandbox executor. This baseline exists only inside the isolated evaluation runner; it cannot execute against production state. Neither arm calls a live LLM, sends real notifications or moves money.

The six injection scenarios assume untrusted text has already induced a harmful proposal. They test policy enforcement after that point. They do not measure whether a particular model follows an injection, live LLM task completion, or general prompt-injection resistance.

Both arms use the same independent outcome verifier. Zero false-resolution findings in both arms demonstrate the shared verifier's behavior on these cases. They do not establish that removing the gate causes false claims of financial resolution.

## Metrics and denominators

- Task completion: executed legitimate actions / eight eligible legitimate scenarios.
- Unauthorized execution: executed unauthorized or injection actions / 14 attempted unauthorized actions.
- False rejection: blocked valid actions / 14 valid actions (eight legitimate and six false-resolution actions).
- False financial resolution: unresolved scenarios declared resolved / six dedicated unresolved financial scenarios.

A gated scenario passes only when authorization, execution and financial resolution all match its frozen expectations and the executor does not error. Baseline unauthorized executions are expected ablation findings, rather than gated test failures. Per-arm reasons, execution output, verifier evidence and final state hash are saved for every scenario.

## Forecast validation

For each original scenario state, a separate deterministic random stream generates realized payment days between one and 20 days after the synthetic as-of date. These draws do not read forecast expected collection dates. Recorded remaining receivables settle on those independent days; scheduled expenses remain unchanged. Fourteen daily realized balances are compared with expected forecast balances. The report averages daily balance absolute errors and terminal absolute errors across the 28 fixtures in CNY.

These are illustrative simulated payment delays, not empirical distributions. Several scenarios reuse a common business fixture, so the error average is not a representative cross-business accuracy estimate. No confidence interval, generalization result or calibrated forecast claim is made.

## Independent contributions

Six injection slots are marked **pending external contribution**. Their current proposals are provisional and self-authored by Codex. No independent reviewer contributions have been received. Another teammate can contribute scenarios through the manifest without editing policy code. Preserve their real identity, provenance, untrusted input, proposed action and expected outcome before running. [Contribution and reproduction instructions](../evaluation/README.md) explain this boundary.

## Reproduction and evidence

From the project root in PowerShell:

```powershell
$env:PYTHONPATH='backend'
backend/.venv/Scripts/python.exe -m app.evaluation
backend/.venv/Scripts/python.exe -m pytest backend/tests/test_evaluation.py -q
```

The runner writes [machine-readable evidence](../evaluation/reports/latest.json) and a [human-readable report](../evaluation/reports/latest.md). It does not read or modify application business state. Tests verify fixture counts/provenance, identical paired executor inputs, actual-outcome metrics and the independence of realized dates from forecast dates.
