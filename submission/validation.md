# Final validation

Verified locally on Windows on 16 October 2026. All source, dependencies, caches, generated data and evidence were kept inside the project folder. The user-supplied attachment and skill instructions were read from their provided locations.

| Check | Observed result |
|---|---|
| Backend pytest | 29 passed; one Starlette/httpx deprecation warning |
| Frontend Vitest | 8 passed |
| ESLint | Passed |
| TypeScript | Passed |
| Production Next.js build | Passed |
| Production dependency audit | Zero reported production vulnerabilities; five development-tool advisories remain |
| Playwright production workflows | 7 passed; no skipped or flaky tests |
| Responsive UI | All 8 views at 1440×900, 1280×800, 768×1024 and 390×844; no page errors or document overflow |
| Paired policy evaluation | 28/28 gated expected outcomes matched |
| Local development and production launchers | Both returned frontend HTTP 200 and backend healthy |
| Reset and stop/start | Verified on Windows; local backups preserved |
| Final initial scenario | CNY 42,000 cash; CNY 2,000 expected shortfall on 28 October |
| Final audit | Database and append-only JSONL/checkpoint integrity valid |

The browser journeys cover shortage presentation; reminder approval/execution without a receipt; modified expense approval and recalculation; desktop navigation; business switching; financing costs; security evidence; recorded injection comparison; read-only API denial; mobile layout; proposal rejection; and an explicit partial receipt updating cash and invoice balance. Protected payroll and controlled audit modification/deletion detection are additionally exercised in backend/evaluation tests. The tests never corrupt the live demonstration audit trail.

During development, browser checks exposed waits that ran before a transaction committed, selectors that matched hidden select options or an empty Next.js announcer, and a navigation label whose pending-count changed its accessible name. Those checks were corrected without weakening the financial assertions. The initial four-test run was expanded during the UI redesign; all seven current journeys pass against the production frontend. A startup race was also fixed: the launcher now waits for backend health before starting the frontend.

The evaluation report's recorded engine SHA-256 matches the final `backend/app/engine.py`. The frozen manifest and source hashes are included in `evaluation/reports/latest.json`. Gated unauthorized execution was 0/14 versus 14/14 in the isolated baseline; legitimate completion was 8/8 in each arm. Both arms retained financial verification and had 0/6 false resolutions. These are self-authored forced proposals, not live-model reliability results.

## Evidence

- `submission/browser-results.json`: final Playwright machine report.
- `submission/layout-results.json`: viewport overflow and page-error checks.
- `submission/action-evidence.jsonl`: 22 synthetic events from the completed owner workflow, saved before the demonstration reset.
- `submission/workflow-final-state.json`: completed workflow state, including the CNY 100.25 partial receipt.
- `submission/screenshots/`: desktop overview, recovery, approval dialog, financing, cash-flow detail, security, evaluation and audit; mobile and tablet overview.

The app was then reset to the initial payroll-shortfall story and left running locally. Saved workflow screenshots intentionally show different stages of the demonstration. The 375/768/1440 overview screenshots show the restored initial state. The 32 primary-view captures in `submission/ui-review/` show the completed synthetic workflow. See `docs/ui-validation.md` for the UI-specific changes and test scope.

## Unverified and incomplete requirements

Live OpenRouter inference has not been run because no key was supplied. Adapter success/error paths were tested with mocked HTTP responses. Docker is unavailable, so Compose runtime is unverified. Six independent adversarial contributions are pending. Forward receipt dates are scenario assumptions rather than an estimated customer-history model. Demo identities are not production authentication. Source code is available at [FlowGuard-Sentinel](https://github.com/daudibrahimhasan/FlowGuard-Sentinel); no application deployment or portal submission has been made. A local demo and submission documentation are ready; external validation and official packaging are still needed before claiming a final competition submission.
