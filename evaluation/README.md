# Offline paired evaluation

Run from the project root: `backend/.venv/Scripts/python.exe -m app.evaluation` with `PYTHONPATH=backend` (PowerShell: `$env:PYTHONPATH='backend'`). Reports are saved in `evaluation/reports/`.

The frozen JSON manifest is the source of test inputs and expected outcomes. Its SHA-256 is included in each report. Both arms receive deep copies of identical state, payload and owner context, and call the production sandbox executor. Only the gated arm calls the independent policy engine. There is no baseline execution endpoint. These are forced proposal tests, not measurements of live model behavior or universal injection resistance.

Injection cases test what happens if untrusted text has already induced a harmful proposal. They do not measure whether an LLM follows the injected instruction. False-resolution cases exercise the independent outcome verifier in both arms, so any benefit from the policy gate is distinguished from the verifier's benefit.

Six injection slots are **pending external contribution**. Current payloads are provisional, self-authored fixtures. A teammate can edit these slots or contribute a new manifest without changing policy code. Preserve contributor identity, source, date, and proposed payload; specify expected authorization, execution and financial outcomes before running. Review and commit the manifest before evaluating. Do not label these fixtures independently authored until real contributions exist.

Forecast error uses an independently seeded simulated collection schedule from held-out payment delays and reports daily balance MAE and terminal absolute error in CNY. This is a synthetic sensitivity check, not an empirical business accuracy estimate or calibrated uncertainty interval.
