# FlowGuard Sentinel

**An SME finance copilot that checks authority, execution and financial outcomes separately.**

FlowGuard Sentinel forecasts cash availability over 14 days and helps a business owner review recovery options before a shortage. An agent proposes actions. The owner approves an exact payload. A deterministic policy engine checks it again before sandbox execution, and an independent verifier checks what actually changed.

Sending an invoice reminder does not mean the customer paid. Moving an expense does not remove the liability. The interface keeps those distinctions visible.

All businesses, records, financing options, notifications and outcomes are synthetic. There are no payments, loan applications or banking connections. This prototype is intended for a local FinTechathon demonstration, not production financial use.

Built for Topic E, SME Finance Copilot, in the 2026 Shenzhen International FinTech Competition.

![FlowGuard Sentinel overview showing current cash, the payroll shortfall and a 14-day forecast](submission/screenshots/overview-1440.png)

## Run locally on Windows

Prerequisites: Windows PowerShell, Python 3.11 and Node.js 22 or later. Clone the repository, then start the app:

```powershell
git clone https://github.com/daudibrahimhasan/FlowGuard-Sentinel.git
cd FlowGuard-Sentinel
.\scripts\start.ps1 -Install
```

Open [localhost:3000](http://localhost:3000). Interactive API documentation is at [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Later runs can omit `-Install`. Dependencies and caches stay inside this project. The starter waits for backend and frontend readiness, runs local background processes and writes server logs here. Stop those processes before resetting data or launching another copy.

Use `.\scripts\stop.ps1` to stop servers started by the launcher. After a frontend build, `.\scripts\start.ps1 -Production` starts the production frontend with the same local backend.

For visible terminals instead, run these in two terminals from the project root:

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

```powershell
cd frontend
npm run dev -- --hostname 127.0.0.1
```

The owner, analyst and viewer switcher uses explicit demo identities enforced by the backend. Anyone running this local demo can select owner. This is role testing, not production authentication.

## Optional free-model configuration

Copy `.env.example` to `.env` in this folder, add your OpenRouter key and restart the backend. Keep credentials out of source control. The backend loads the root `.env` and supports the official `openrouter/free` router. Explicit configured variants must be verified free. It never intentionally switches to a paid route. Without a usable key/endpoint, the app clearly labels deterministic demonstration mode.

No key was supplied during development, so a successful live free-model response remains unverified. The rest of the product runs without AI spending.

## Financial workflows

- Overview and cash-flow analysis calculate balances from records and distinguish expected collections from the conservative scenario.
- Recovery agent generates inspectable reminder and flexible-expense proposals. Changes invalidate approval; owners approve and execute exact actions.
- Reminder delivery creates no cash. A separate owner sandbox receipt updates the invoice and ledger.
- Payroll, rent, utilities and tax are protected. Recipients, vendor scope, financial caps, expiry and consumed approvals are checked before execution.
- Financing compares three hypothetical offers, with costs and repayment risk. No application or execution is available.
- Security center and Audit trail expose permissions, mandates, blocked decisions, execution and verification evidence.
- Evaluation lab displays recorded matched gated/ungated tests. The baseline operates only on isolated offline fixtures.

## Try the main demo

The reference date is fixed to **16 October 2026** for reproducibility. The synthetic retail business opens with CNY 42,000 and a calculated CNY 2,000 expected cash shortfall on 28 October, its payroll date. Manufacturing has a more serious shortage; services stays positive.

1. Accept the synthetic-data disclosure and select **Lantao Retail Supply**.
2. Inspect the 14-day forecast and payroll obligation.
3. Generate a recovery plan, inspect a reminder, approve it and execute it.
4. Check that delivery is recorded while confirmed cash stays unchanged.
5. Approve a flexible expense deferral and inspect the recalculated forecast. Payroll remains protected and the deferred expense remains payable.
6. In Evaluation lab, compare a changed-recipient or protected-payroll scenario across both configurations.
7. Inspect Audit trail. Optionally record a partial sandbox receipt in Approvals to see separate payment evidence update the ledger.

See the [five-minute demo script](submission/demo_script.md) for the full sequence.

<details>
<summary>More workspace screenshots</summary>

**Recovery workspace**

![Recovery actions with execution states and independent financial evidence](submission/screenshots/recovery-desktop.png)

**Matched policy evaluation**

![Evaluation metrics and gated versus ungated scenario evidence](submission/screenshots/evaluation-lab-desktop.png)

**Security center**

![Permissions, protected obligations, audit integrity and consumed mandates](submission/screenshots/security-center-desktop.png)

Screenshots show different stages of the synthetic demonstration. Additional desktop, tablet and mobile captures are in [submission/screenshots](submission/screenshots).

</details>

## How it works

```text
Financial records → deterministic forecast → proposed action
                                              ↓
                            owner approval of exact payload
                                              ↓
                          role + mandate + deterministic gate
                                              ↓
                                  sandbox execution
                                              ↓
                         independent financial verification
                                              ↓
                            hash-chained audit evidence
```

The LLM has propose-only authority. It cannot approve itself, write ledger entries or call an ungated execution endpoint. Monetary calculations use Python Decimal. Reminder delivery creates an event with zero cash received. Eligible deferrals change scheduled dates; explicit owner-recorded receipts change invoice balances and recorded cash.

The forecast range is an assumption-based scenario comparison, not a statistical confidence interval. Forward collection dates are illustrative scenario inputs rather than a fitted customer-history model.

| Layer | Implementation |
|---|---|
| Interface | Next.js App Router, TypeScript, Tailwind CSS, Radix, Recharts, Lucide |
| Backend | FastAPI, Pydantic, Python |
| Financial state | SQLite, SQLAlchemy, Decimal calculations |
| Agent | OpenRouter free-model adapter and labelled deterministic fallback |
| Audit | SHA-256 chain, append-only JSONL mirror and local checkpoint |
| Validation | pytest, Vitest, React Testing Library, Playwright |

## Recorded evaluation

The suite contains **28 frozen scenarios**: 8 legitimate operations, 8 authorization violations, 6 forced injection proposals and 6 false-resolution cases. Both arms receive identical proposal payloads and independent copies of the same state, and use the same sandbox executor. The ungated branch exists only in the isolated evaluator.

| Metric | With policy gate | Ungated offline baseline |
|---|---:|---:|
| Legitimate task completion | 8/8 | 8/8 |
| Unauthorized execution | 0/14 | 14/14 |
| False rejection | 0/14 | 0/14 |
| False financial resolution | 0/6 | 0/6 |

All 28 gated expectations matched. These are **self-authored forced-proposal tests**, not live-model task-completion or prompt-injection success rates. Six independent attack contributions remain pending. Both arms retain the outcome verifier, so the false-resolution result cannot be attributed to the policy gate.

Daily balance MAE against independently seeded synthetic receipt dates was **CNY 6,920.92**. This is a synthetic sensitivity check, not measured accuracy on real SMEs.

See the [scenario-level report](evaluation/reports/latest.md), [machine-readable evidence](evaluation/reports/latest.json), [methodology](docs/evaluation_methodology.md) and [contribution instructions](evaluation/README.md).

## Reproduce data, evaluation and checks

From the project root:

```powershell
# Generate the same seeded synthetic JSON; does not overwrite a running database.
.\backend\.venv\Scripts\python.exe -m backend.app.generator
# Stop the backend before resetting its synthetic database; preserves a local backup.
.\backend\.venv\Scripts\python.exe -m backend.app.reset --confirm
# Run the frozen paired scenarios and generate JSON/Markdown reports.
.\backend\.venv\Scripts\python.exe -m backend.app.evaluation
# Backend monetary, policy, workflow, audit and evaluation tests.
.\backend\.venv\Scripts\python.exe -m pytest backend/tests -q
```

Frontend checks:

```powershell
cd frontend
npm run lint
npm run typecheck
npm test
npm run build
npm run start -- --hostname 127.0.0.1
```

The latest UI revision passed **29 backend tests, 8 frontend tests and 4 read-only browser journeys**, plus lint, TypeScript and a production build. All eight screens were captured at 1440×900, 1280×800, 768×1024 and 390×844. The browser checks cover navigation, keyboard controls, filters, responsive layouts and a populated approval ledger using browser-only fixtures. See the [Ramp app typography analysis](docs/ramp-app-typography.md); earlier financial workflow validation is recorded in [UI validation](docs/ui-validation.md).

Browser tests change synthetic state, so use a fresh reset with both servers running. Installation and reproduction steps are in [scripts/browser/README.md](scripts/browser/README.md). See [validation evidence](submission/validation.md) for scope, warnings and unverified items.

## Containers

```powershell
docker compose up --build
```

The backend uses a persistent data volume. The frontend proxy is built against the backend service. Docker is unavailable in the development environment, so these definitions have not been runtime-verified. Do not expose the public demonstration identities on the internet.

## Project layout

```text
backend/app/          Financial engine, agent, policy, state, audit and API
backend/tests/        Backend unit and integration tests
frontend/             Connected workspace and component tests
data/                 Synthetic generator output and research notes
evaluation/           Frozen scenarios, paired runner inputs and reports
scripts/              Local startup and browser checks
docs/                 Architecture, financial model and security boundaries
submission/           Technical documentation, demo script and evidence
```

Start with [architecture](docs/architecture.md), [data methodology](docs/data_methodology.md), [financial model](docs/financial_model.md), [agent design](docs/agent_design.md) and [security model](docs/security_model.md). Submission materials include a [technical document](submission/technical_documentation.md), [security self-assessment](submission/security_self_assessment.md) and [presentation outline](submission/presentation_outline.md).

## Current limits

- All data and economic assumptions are synthetic or illustrative.
- Public demo identities provide role testing, not production authentication or tenant isolation.
- Successful live free-model inference and Docker runtime remain unverified.
- Forward collection dates are scenario inputs rather than estimated customer-payment histories.
- Six independent adversarial contributions are pending; there is no universal injection-resistance claim.
- Local audit checkpoints have no external anchor. A privileged full rewrite can defeat local tamper evidence.
- Five development-tool dependency advisories were reported during validation; the production dependency audit reported zero vulnerabilities.
- No real financing approvals, WeBank integration, regulatory certification or completed competition submission is claimed.

Read `evaluation/reports/latest.md` for computed results and `docs/evaluation_methodology.md` for denominators and experiment boundaries. The 28 scenarios use frozen proposals, not live-model generations. Six independent attack contributions remain pending. Both arms share financial verification; its benefit cannot be attributed to the gate ablation.

The prototype is ready for a local demonstration. [Research notes](data/sources/research_notes.md) distinguish sourced context from illustrative assumptions. Read [known limitations](submission/known_limitations.md) before presenting the evaluation or considering broader use.

UI component choices, source links and licenses are documented in [Component sources](docs/ui-component-sources.md). Branding uses the supplied FGS monogram; Lucide remains the only icon library.
