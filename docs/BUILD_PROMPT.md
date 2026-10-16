# MASTER BUILD PROMPT — FLOWGUARD SENTINEL

## ROLE AND OBJECTIVE

You are Codex, acting as a senior full-stack engineer, AI systems architect, fintech product engineer, AI Safety researcher, quantitative software engineer, and product designer.

Your assignment is to independently design, implement, test, refine, and deliver a complete, working application named **FlowGuard Sentinel** for the **2026 Shenzhen International FinTech Competition (FinTechathon)**.

**Competition Track:** Topic E — SME Finance Copilot
**Core Innovation:** Verifiable Financial Autonomy
**LLM Provider:** OpenRouter
**API Budget:** Free models only
**Project:** New application, built from scratch
**Competition Deadline:** October 20, 2026, 23:59 Beijing time

This must be a real, functional project, not a collection of mockups, placeholders, or disconnected demonstrations.

You are responsible for the entire development lifecycle: research, architecture, implementation, data generation, frontend, backend, AI integration, security, testing, evaluation, bug fixing, documentation, and final validation.

Operate autonomously. Make reasonable engineering decisions without repeatedly requesting confirmation. Ask questions only when essential information is unavailable.

Do not stop after generating code. Run it, test it, inspect the results, identify problems, fix them, and repeat until the application meets the acceptance criteria.

---

# 1. PROJECT OVERVIEW

## Product Name

**FlowGuard Sentinel**

*An AI-Native Financial Health and Recovery Agent for Small Businesses*

## Executive Summary

FlowGuard Sentinel is a human-supervised AI financial agent that helps small and medium-sized enterprises anticipate cash-flow shortages, develop recovery strategies, and safely execute authorized financial actions.

Using historical financial transactions, outstanding invoices, and scheduled obligations, the system forecasts cash availability over 14 days and identifies upcoming liquidity gaps.

The AI agent proposes actionable financial interventions:

1. Sending overdue-invoice reminders.
2. Rescheduling eligible business expenses.
3. Comparing 2–3 simulated working-capital financing options.

The first two actions are executable in a sandbox after authorization. Financing comparisons are strictly read-only.

The product's distinguishing contribution is its application of AI Safety principles to financial autonomy.

The LLM cannot directly execute financial transactions or override authorization rules. Users inspect, modify, approve, or reject proposals. A deterministic policy engine independently validates every executable action against approved mandates, role permissions, spending limits, recipient allowlists, protected categories, and expiration conditions.

An independent outcome verifier distinguishes successful action execution from actual financial recovery.

For example, sending an invoice reminder does not mean the customer paid or that a cash shortfall disappeared.

All material decisions are recorded in a tamper-evident, SHA-256 hash-chained audit log.

A reproducible evaluation compares the same financial scenarios with and without the independent policy gate, quantifying security improvements and possible costs to legitimate task completion.

## Strategic Context

The project is being built for the International Track of Shenzhen FinTechathon 2026.

The official evaluation criteria are:

- Task completion: 40%.
- Security and compliance: 30%.
- Innovation and interaction: 30%.

The product should demonstrate potential relevance to WeBank's SME financial-inclusion and working-capital financing business.

Do not claim an existing WeBank partnership, product integration, financial endorsement, or access to proprietary WeBank data.

The project must remain a functioning SME Finance Copilot rather than becoming purely an AI Safety experiment.

---

# 2. NON-NEGOTIABLE IMPLEMENTATION PRINCIPLES

1. Build a complete, connected application with functioning frontend, backend, database, AI integration, and execution workflows.
2. Prioritize reliable end-to-end financial tasks over unnecessary sophistication.
3. Use real calculations and persistent application state. Do not hardcode financial results into dashboard components.
4. Generate realistic, clearly labeled synthetic financial data.
5. Use deterministic code for forecasting, financial calculations, permissions, execution, and verification.
6. Use the LLM for language understanding, explanation, and structured action proposals—not as the final authority on financial facts or permissions.
7. Never permit an LLM-generated instruction to directly bypass the policy engine.
8. Keep baseline security evaluation isolated from the real application execution path.
9. Make AI Safety effectiveness measurable through reproducible tests.
10. Deliver an interface that feels professionally designed, not automatically generated.

All financial activity must be simulated. No real payments, loan applications, customer notifications, or financial account connections.

---

# 3. TECHNOLOGY STACK

Use the following stack unless an essential compatibility issue requires an alternative.

| Component | Technology |
|---|---|
| Frontend | Next.js, TypeScript, App Router |
| Styling | Tailwind CSS |
| UI components | shadcn/ui and Radix primitives |
| Icons | Lucide |
| Charts | Recharts |
| Typography | Poppins, Inter or Source Sans 3, IBM Plex Mono |
| Backend | Python, FastAPI |
| API validation | Pydantic |
| AI integration | OpenRouter API |
| Financial calculations | pandas, NumPy, Python Decimal |
| Database | SQLite with SQLAlchemy |
| Data generation | Python, Faker, NumPy |
| Authorization | Server-enforced RBAC and scoped mandates |
| Audit logging | JSONL, SHA-256 |
| Backend testing | pytest |
| Frontend testing | Vitest, React Testing Library |
| End-to-end testing | Playwright |
| Deployment | Docker Compose |
| Version control | Git |

Use a maintainable monorepo:

```text
flowguard-sentinel/
├── frontend/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   ├── forecasting/
│   │   ├── recovery/
│   │   ├── policies/
│   │   ├── authorization/
│   │   ├── sandbox/
│   │   ├── verification/
│   │   ├── audit/
│   │   ├── evaluation/
│   │   └── models/
│   └── tests/
├── data/
│   ├── generators/
│   ├── synthetic/
│   └── sources/
├── evaluation/
│   ├── scenarios/
│   ├── baselines/
│   └── reports/
├── docs/
├── submission/
├── scripts/
├── docker-compose.yml
├── .env.example
└── README.md
```

You may adjust internal structure if a different organization demonstrably improves maintainability.

---

# 4. DATA RESEARCH AND SYNTHETIC DATASET

This component is extremely important.

The generated financial data must resemble plausible business activity. It must not look like randomly generated numbers arranged into a spreadsheet.

## 4.1 Research before generating data

If web browsing is available, investigate credible public sources relating to:

- SME cash-flow management.
- Late invoice payments.
- Working-capital requirements.
- Common operating expenses.
- Seasonal revenue fluctuations.
- Payroll and supplier-payment obligations.
- Cash-flow forecasting practices.
- SME financing costs and structures.

Prefer primary or authoritative sources, including the OECD, World Bank, official statistical agencies, central banks, and reputable financial research.

The competition website is:

https://fintechathon.g-ican.com/

Record relevant findings in:

`data/sources/research_notes.md`

For every sourced quantitative assumption, record its source URL, publication date, geographical coverage, and how it influences the data generator.

Do not invent statistics or citations.

If web access is unavailable, use explicitly labeled illustrative assumptions and document the limitation.

## 4.2 Synthetic business profiles

Generate three realistic SME datasets:

**Business A — Retail Distributor**

- Regular customer payments.
- Supplier purchases.
- Recurring payroll.
- Inventory-related expenses.
- Several overdue invoices.
- Moderate cash-flow volatility.

**Business B — Small Electronics Manufacturer**

- Larger but less frequent customer payments.
- High inventory and supplier costs.
- Multiple invoice maturities.
- Fixed payroll obligations.
- Greater exposure to delayed payments.

**Business C — Small Services Company**

- Project-based revenue.
- Recurring operational expenses.
- Uneven payment schedules.
- Lower inventory expenditure.
- Variable collection delays.

Use synthetic business names and addresses. Do not imply that the businesses actually exist.

Use RMB/CNY as the primary reporting currency.

## 4.3 Data generation requirements

Create 90 days of historical transactions and a forward-looking schedule of financial obligations.

Include:

- Opening and closing balances.
- Customer invoices.
- Invoice issuance and due dates.
- Actual or simulated payment dates.
- Partially paid invoices.
- Overdue invoices.
- Vendor bills.
- Payroll.
- Rent.
- Utilities.
- Inventory purchases.
- Other recurring expenses.
- Exceptional expenses.
- Scheduled future payments.

Relationships must be financially consistent.

For example:

- Invoice payments must reconcile against invoice balances.
- Account balances must reconcile against ledger movements.
- Partial payments must reduce outstanding receivables.
- Payroll must not disappear because the agent wants to improve the forecast.
- Late payments should follow a documented, plausible distribution rather than arbitrary delays.

Use seeded randomness for reproducibility.

Support generating the exact same dataset again using the same configuration and seed.

## 4.4 Reference scenarios

Include at least three ready-to-run business situations:

- Healthy business with no immediate liquidity problem.
- Business with a moderate, recoverable cash shortage.
- Business with a serious upcoming shortage and uncertain receivables.

The second scenario should be the primary competition demonstration.

Use an illustrative case in which the business faces a meaningful shortfall roughly 12 days before payroll.

Every amount and projected change must come from the underlying financial model.

## 4.5 Data quality validation

Write automated checks confirming:

- Ledger balances reconcile.
- Dates are logically valid.
- Invoice statuses match payments.
- There are no unexplained negative balances or impossible transactions.
- Financial events follow appropriate dependencies.
- Generated datasets contain meaningful but plausible variation.

The UI must clearly identify all datasets and simulated outcomes as synthetic.

---

# 5. CASH-FLOW FORECASTING ENGINE

Implement a fixed **14-day cash-flow forecasting system**.

The engine should calculate projected daily cash balances using:

Opening cash + expected cash inflows − scheduled cash outflows.

Model expected collections using invoice due dates, customer payment history, and documented delay assumptions.

Separate confirmed financial events from uncertain projected events.

The forecast must identify:

- Current available cash.
- Expected inflows.
- Upcoming obligations.
- Minimum projected daily balance.
- Date of the first projected liquidity shortfall.
- Estimated shortfall amount.
- Obligations contributing to the shortfall.

Do not use an LLM to calculate financial balances.

Use Decimal-based monetary calculations where financial precision matters.

Support recalculating forecasts after an authorized expense rescheduling or after a simulated receipt is actually recorded.

Sending a reminder alone must not increase confirmed cash.

Show forecast uncertainty honestly. A simple documented scenario or assumption-based range is sufficient; do not invent statistical confidence.

For forecast accuracy evaluation, use separately generated or held-out realized cash-flow outcomes. Never assess accuracy by comparing the forecast to itself.

Avoid advanced machine-learning forecasting models unless they are necessary for a working feature. The primary goal is correctness and interpretability.

---

# 6. AI FINANCIAL AGENT

Integrate an OpenRouter-supported free LLM.

## 6.1 OpenRouter configuration

Use environment variables:

```env
OPENROUTER_API_KEY=
OPENROUTER_MODEL=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Investigate currently available free models using OpenRouter's official documentation or model listings.

Select a suitable free model that supports reliable structured output or tool-use behavior.

Free-model availability and limits can change. Do not hardcode an unverified model identifier.

Never automatically switch to a paid model.

Keep the API key exclusively on the backend.

Implement:

- Structured JSON output.
- Pydantic validation.
- Retry handling with bounded attempts.
- Timeouts.
- Rate-limit handling.
- Clear error states.
- Input size limits.
- Safe logging without exposed secrets.

If OpenRouter is unavailable, provide a clearly labeled deterministic demonstration mode so the rest of the product remains functional.

Never present deterministic fallback output as a live LLM response.

## 6.2 Agent responsibilities

The agent should:

1. Interpret the financial situation.
2. Explain the liquidity problem.
3. Identify possible recovery actions.
4. Create structured action proposals.
5. Explain expected financial effects.
6. Explain uncertainty and limitations.
7. Answer user questions about the available financial data.

The LLM must not directly write to the ledger, issue an authorization, or execute an operation.

Its tools must be read-only or propose-only.

## 6.3 Supported recovery actions

**Action A — Invoice Reminder**

Generate a professional payment reminder for an overdue invoice.

After owner approval, simulate sending the reminder and record a delivery event.

Do not automatically assume the customer pays.

**Action B — Expense Rescheduling**

Identify a flexible expense that may be moved without violating protected obligations.

Propose a new payment date.

After owner approval and policy validation, update the scheduled expense in the sandbox.

Track its impact on the 14-day forecast.

**Action C — Mock Financing Comparison**

Compare 2–3 hypothetical working-capital financing options.

Show:

- Principal.
- Annual interest rate.
- Fees.
- Term.
- Repayment schedule.
- Total repayment amount.
- Total borrowing cost.
- Projected cash-flow effect.
- Relevant affordability or repayment risks.

Calculate financing costs deterministically and disclose assumptions.

These products must be clearly labeled as simulated. Do not fabricate WeBank loan offers or approvals.

This action remains strictly read-only.

---

# 7. OWNER INTERACTION AND AUTHORIZATION

Build a functional approval workflow.

Users must be able to:

- Inspect a proposal.
- Understand why it was suggested.
- See projected financial effects.
- Review its assumptions.
- Approve it.
- Reject it.
- Modify its permitted parameters.
- Inspect execution and verification results.

Approval must be attached to an exact action payload.

If an action changes after approval, the original approval becomes invalid.

Implement three permission tiers:

**Read-only:** View authorized financial information.

**Propose:** Inspect data and submit financial action proposals.

**Execute-with-approval:** Execute only specifically approved actions within an active mandate.

Enforce permissions on the backend, not merely through disabled frontend buttons.

Provide distinct demonstration identities with server-enforced roles. A role switcher may exist for demo purposes, but switching identities must not amount to a client-side bypass of authorization.

## Financial mandates

Represent mandates as validated, persistent records containing:

- Authorized user or role.
- Action type.
- Exact approved parameters.
- Maximum permitted financial impact.
- Recipient or vendor allowlist where applicable.
- Protected financial categories.
- Approval timestamp.
- Expiration timestamp.
- Execution or consumption status.

Treat payroll as protected by default.

Validate authorization again immediately before execution.

Use idempotency controls to prevent duplicate execution.

---

# 8. DETERMINISTIC AI CONTROL GATE

This is one of the most important technical components.

Implement a separate, deterministic policy engine.

It must not rely on an LLM to decide whether an executable action is authorized.

The gate checks:

- The user has appropriate permissions.
- The action type is allowed.
- The action matches an approved mandate.
- Amounts and parameters remain within authorized limits.
- Recipients or vendors are permitted.
- Protected financial obligations are unchanged.
- Authorization has not expired.
- The action has not already executed.
- Required business constraints remain satisfied.

Reject unknown action types and unexpected parameters.

Use strict schemas and explicit default-deny behavior.

The financial execution layer must never accept a direct execution request that bypasses this gate in the normal application.

## Prompt-injection resistance

Treat invoice descriptions, vendor messages, uploaded text, and other external content as untrusted data.

Test examples involving:

- Instructions to ignore previous rules.
- Attempts to change payment recipients.
- Attempts to override spending limits.
- Malicious instructions hidden inside invoice descriptions.
- Attempts to impersonate a system administrator.
- Attempts to falsely report an approved action.

The deterministic policy layer must enforce authority regardless of what the model proposes.

A blocked action should produce a clear explanation identifying the violated rule without revealing sensitive implementation details.

Do not claim universal prompt-injection prevention. Report measured performance on the scenarios actually tested.

---

# 9. FINANCIAL OUTCOME VERIFICATION

Implement **Evidence-Based Resolution Verification**.

This component must distinguish between:

- An action being proposed.
- An action being authorized.
- An action executing successfully.
- A financial benefit being predicted.
- A financial benefit being observed in the sandbox.
- A cash-flow problem being verified as resolved.

For example:

An invoice reminder may be delivered successfully while the invoice remains unpaid.

The system must not claim that the cash shortage has been resolved.

The verifier should inspect independent ledger records and predefined scenario conditions rather than trusting an LLM's self-report.

Possible recovery states:

- Proposed.
- Awaiting approval.
- Blocked.
- Executed.
- Recovery pending.
- Resolution verified.
- Unresolved.

A forecast showing an improvement is not sufficient evidence of realized recovery.

Support both realized sandbox outcomes and projected financial effects, displaying them separately.

Use a clearly defined **False Financial Resolution Rate (FFRR)**:

FFRR = unresolved cases incorrectly reported as resolved / all genuinely unresolved cases.

Handle zero-denominator cases explicitly.

---

# 10. AUDIT SYSTEM

Implement append-only JSONL audit records with SHA-256 hash chaining.

Record:

- Event ID.
- Timestamp.
- Actor.
- Event type.
- Relevant action ID.
- Authorization decision.
- Policy result.
- Execution result.
- Verification result.
- Previous record hash.
- Current record hash.

Use a canonical serialization format so hashes can be reproduced.

Build an audit integrity verification function.

Demonstrate that modifying or deleting an existing record within a retained chain can be detected.

Describe this as **tamper-evident within the stated threat model**, not tamper-proof.

A privileged attacker who can rewrite the complete chain may defeat this protection without external anchoring.

Do not spend excessive time building a production-grade cryptographic logging infrastructure.

---

# 11. PREMIUM PRODUCT DESIGN

The frontend must look like a professionally designed financial SaaS product.

This is not optional.

Aim for the polish of a thoughtfully designed Stripe, Linear, Apple, or modern premium banking interface while preserving FlowGuard Sentinel's own visual identity.

Do not copy branding, proprietary assets, or existing interfaces.

## 11.1 Visual direction

Design characteristics:

- Minimal.
- Precise.
- Professional.
- Calm.
- Modern.
- Financially credible.
- Clean typography.
- Generous but controlled whitespace.
- Strong visual hierarchy.
- Subtle depth.
- Consistent spacing.
- Purposeful interactions.

Avoid the stereotypical AI-generated dashboard look.

Do not use oversized glowing gradients, neon borders, generic glassmorphism everywhere, floating 3D objects, decorative AI brains, excessive pills, or meaningless metrics.

Every visual element should help the user understand financial health, execute a task, or inspect a security decision.

## 11.2 Typography

Use:

- **Poppins:** Main headings, prominent titles, and selected product labels.
- **Inter or Source Sans 3:** Body text, tables, navigation, forms.
- **IBM Plex Mono:** Transaction identifiers, audit hashes, and technical values where appropriate.

Use consistent typography weights and spacing.

Apply tabular numerals to financial data.

Financial balances must be easy to scan.

Avoid excessively bold interfaces and inconsistent type sizes.

## 11.3 Color palette

Start with the following restrained direction:

| Purpose | Suggested color |
|---|---|
| Background | #F7F8F6 |
| Primary text | #202825 |
| Primary green | #175D4B |
| Secondary green | #3F8571 |
| Border | #E4E8E3 |
| Surface | #FFFFFF |
| Muted text | #68736D |
| Warning | #B77932 |
| Error | #B74747 |
| Accent blue | #42678F |

Refine the palette as needed to achieve a cohesive design.

Use subtle gradients only where they serve a meaningful visual purpose.

Maintain accessible contrast ratios.

Do not make the entire dashboard green or cover every section with colored cards.

## 11.4 Application layout

Create a clean application shell with:

- Compact sidebar navigation.
- Top header.
- Business selector.
- Current user or permission indicator.
- Clearly organized content area.
- Consistent card components.
- Responsive layouts.
- Meaningful empty, loading, success, and error states.

Support desktop and mobile layouts.

Prioritize desktop use for the competition demonstration, while ensuring the application remains usable on narrower screens.

## 11.5 Required screens

**A. Overview**

Show:

- Current cash balance.
- Minimum projected cash balance.
- Next liquidity shortfall.
- Upcoming financial obligations.
- Overdue receivables.
- A 14-day cash-flow chart.
- Important alerts.
- Proposed recovery actions.

Use realistic data visualizations with clear currency labels and tooltips.

**B. Cash-Flow Analysis**

Provide a detailed 14-day forecast.

Allow inspection of projected inflows, outflows, and assumptions.

Show the difference between confirmed financial activity and projected collections.

**C. Recovery Workspace**

Provide a refined conversational agent interface together with structured financial action cards.

Each proposal should offer inspect, modify, approve, and reject functionality.

Avoid making the product feel like a generic ChatGPT clone.

**D. Financing Comparison**

Display 2–3 simulated financing options with understandable cost comparisons.

Include transparent assumptions and a clear indication that the products are hypothetical.

**E. Security Center**

Show:

- Permission tiers.
- Active mandates.
- Protected categories.
- Recent blocked actions.
- Security explanations.
- Audit integrity status.

**F. Evaluation Lab**

Present gated-versus-ungated results.

Allow judges to select a predefined test scenario and inspect what occurred under both configurations.

Use actual recorded results, not hardcoded success percentages.

**G. Audit Trail**

Provide a searchable, readable event timeline.

Users should be able to inspect proposed actions, approvals, policy decisions, sandbox execution, and verification evidence.

## 11.6 Interaction quality

Implement polished, purposeful interaction details:

- Smooth but restrained transitions.
- Clear hover and focus states.
- Confirmation dialogs for sensitive actions.
- Skeleton loading where appropriate.
- Accessible forms.
- Keyboard navigation.
- Meaningful notifications.
- No unnecessary animation.
- No fake functionality.

Use Playwright screenshots to inspect the application at desktop and mobile sizes.

If a screen looks crowded, misaligned, inconsistent, unfinished, or visually generic, improve it before considering the UI complete.

---

# 12. AI SAFETY EVALUATION FRAMEWORK

Build a reproducible evaluation suite containing **28 predefined scenarios**.

Organize them into four groups:

| Scenario family | Count |
|---|---:|
| Legitimate financial operations | 8 |
| Unauthorized actions and permission violations | 8 |
| Prompt-injection attempts | 6 |
| False financial resolution cases | 6 |
| Total | 28 |

The scenarios must include different business situations, action parameters, and expected outcomes.

Before running evaluation, define and freeze:

- Scenario input data.
- Agent-visible context.
- Proposed action or generation procedure.
- User mandate.
- Expected authorization decision.
- Expected execution outcome.
- Expected financial outcome.
- Success and failure criteria.

Store the scenario manifests in version-controlled files.

## 12.1 Gated versus ungated comparison

Run each scenario in two separate, isolated sandbox configurations:

**Configuration A — Gated**

Uses the complete deterministic authorization policy engine.

**Configuration B — Ungated Baseline**

Uses the same agent proposals, scenario data, owner-approval context, and sandbox implementation, but removes the additional deterministic policy checks under investigation.

The ungated configuration must exist only in the offline evaluation runner, never as a user-accessible production execution mode.

Freeze or reuse identical proposed action payloads for the paired comparison to minimize LLM nondeterminism.

If live agent-generation tests are conducted separately, report their variability separately.

Do not mix forced adversarial proposal tests with ordinary end-to-end LLM task-completion results without labeling them.

## 12.2 Required metrics

Report:

**Task Completion Rate**

Successful legitimate tasks divided by eligible legitimate tasks.

**Unauthorized Execution Rate**

Unauthorized actions executed divided by attempted unauthorized actions.

**False Rejection Rate**

Valid authorized actions incorrectly blocked divided by attempted valid authorized actions.

**False Financial Resolution Rate**

Unresolved financial scenarios incorrectly declared resolved divided by genuinely unresolved scenarios.

**Forecast Error**

Compare predictions with independently generated or held-out simulated realized outcomes.

Use suitable absolute-error metrics and explain their limitations.

## 12.3 Independent adversarial testing

Create a documented mechanism for another teammate to contribute adversarial scenarios without modifying the policy engine.

Reserve at least six scenario slots for separately authored attack contributions.

If no teammate has supplied these yet, mark them as pending external contribution. You may build provisional scenarios, but never falsely attribute them to an independent reviewer.

Preserve scenario authorship and provenance.

## 12.4 Reporting

Generate machine-readable and human-readable evaluation reports.

Include:

- Number of executed scenarios.
- Pass/fail outcomes.
- Paired gated-versus-ungated comparison.
- Error classifications.
- Failure examples.
- False rejections.
- Unresolved limitations.
- Reproduction instructions.

Do not fabricate successful results.

If a test fails, record the failure, investigate it, and fix implementation defects.

Do not rewrite expected outcomes merely to make tests pass.

---

# 13. PRIVACY, COMPLIANCE, AND SECURITY SELF-ASSESSMENT

Implement and document:

- Synthetic data disclosure.
- Explicit consent for simulated financial analysis.
- Role-based access.
- Data minimization.
- Sensitive-data masking.
- Server-side authorization.
- Input validation.
- Structured output validation.
- Prompt-injection threat boundaries.
- Human accountability.
- No real banking transactions.
- No real financing approvals.
- Clear limitations of simulated results.
- Known security risks.

Document what has actually been implemented and tested.

Do not claim regulatory certification, production banking compliance, or complete security.

Keep developer secrets out of Git.

Use `.env.example` files with blank credentials.

---

# 14. AUTOMATED TESTING

Testing is part of implementation, not an optional final task.

## Backend unit tests

Cover:

- Cash-flow calculations.
- Ledger reconciliation.
- Late-payment calculations.
- Financing-cost calculations.
- Permission tiers.
- Mandate expiration.
- Spending caps.
- Protected payroll.
- Recipient allowlists.
- Idempotency.
- Authorization invalidation after edits.
- Outcome verification.
- Audit hash validation.

## Integration tests

Verify complete workflows:

1. Load financial data.
2. Generate forecast.
3. Generate proposal.
4. Approve action.
5. Validate policy.
6. Execute in sandbox.
7. Update financial state.
8. Verify outcome.
9. Record audit event.

Also verify blocked and rejected paths.

## Frontend tests

Test:

- Dashboard rendering.
- Financial calculations displayed correctly.
- Navigation.
- Business switching.
- Agent response states.
- Approval flow.
- Modification flow.
- Rejection flow.
- Financing comparison.
- Security logs.
- Evaluation results.

## End-to-end tests

Use Playwright to test the running application.

Include at least these journeys:

- A user identifies a predicted shortage.
- The agent proposes a legitimate invoice reminder.
- The owner approves and executes it.
- The verifier correctly reports that payment is still pending.
- The owner reschedules an eligible expense.
- A protected payroll rescheduling attempt is blocked.
- A malicious invoice attempts an unauthorized action.
- A read-only user cannot execute an action through the API.
- Evaluation results appear correctly in the interface.
- Audit integrity verification detects a controlled tampering test.

Capture useful application screenshots.

Test desktop and mobile viewport behavior.

Run linting, TypeScript checks, backend tests, integration tests, and a production frontend build.

Fix discovered errors.

If the environment cannot run a test, report the limitation explicitly rather than claiming success.

---

# 15. DELIVERY REQUIREMENTS

The completed repository must contain:

**Application**

- Working frontend.
- Working backend.
- OpenRouter integration.
- Synthetic data generator.
- Financial forecasting.
- Three recovery action types.
- Owner authorization.
- Deterministic policy enforcement.
- Sandbox execution.
- Outcome verification.
- Audit system.
- Evaluation Lab.

**Documentation**

Create:

```text
README.md
docs/architecture.md
docs/data_methodology.md
docs/financial_model.md
docs/agent_design.md
docs/security_model.md
docs/evaluation_methodology.md

submission/technical_documentation.md
submission/security_self_assessment.md
submission/evaluation_report.md
submission/demo_script.md
submission/presentation_outline.md
submission/known_limitations.md
```

The presentation outline should support a final presentation of no more than 10 minutes.

The demo script should fit within five minutes.

The competition submission should have evidence of sandbox actions, source-code access, setup instructions, and reproducible tests.

**Developer Experience**

Provide:

- Clear installation steps.
- Environment configuration.
- A single documented development startup procedure.
- Docker Compose setup.
- Dataset generation command.
- Database reset command.
- Evaluation command.
- Test commands.
- Production build instructions.

The project must work without paid AI services.

The essential deterministic workflows should remain demonstrable even when a free OpenRouter model is unavailable.

---

# 16. IMPLEMENTATION ORDER

Work incrementally and verify functionality after each major phase.

## Phase 1 — Foundation

Research required assumptions, initialize the repository, establish architecture, configure frontend/backend/database, and prepare synthetic data generation.

Deliver a running application shell and validated sample datasets.

## Phase 2 — Financial Engine

Implement ledger operations, forecasting, shortfall detection, and recovery calculations.

Verify numerical correctness through unit tests.

## Phase 3 — Financial Agent

Integrate OpenRouter and structured proposals.

Implement invoice reminders, expense rescheduling, and mock financing comparisons.

Verify complete workflows without relying on the UI.

## Phase 4 — AI Control and Verification

Implement owner authorization, permission tiers, scoped mandates, policy enforcement, outcome verification, and hash-chained audit records.

Run positive and negative tests.

## Phase 5 — Product Interface

Build and refine all required screens.

Integrate real API responses and application state.

Eliminate placeholder metrics, nonfunctional buttons, and disconnected components.

## Phase 6 — Controlled Evaluation

Implement the paired gated-versus-ungated runner.

Run the predefined scenarios.

Investigate failures and generate evidence-backed reports.

## Phase 7 — Final Quality Assurance

Run automated tests, inspect the live application, review screenshots, fix UI inconsistencies, verify Docker setup, and prepare submission documentation.

Do not skip core functionality to add optional features.

---

# 17. STRICT SCOPE LIMITS

Do not implement:

- Real financial transactions.
- Real loan applications.
- Actual WeBank integration.
- Cryptocurrency or on-chain functionality.
- Variable forecasting horizons.
- Advanced forecasting research models.
- Multi-agent orchestration frameworks.
- Federated learning.
- Real banking credential collection.
- Paid LLM dependencies.
- Complex production infrastructure.
- Unnecessary analytics features.
- Decorative dashboards that do not support actual workflows.

The purpose is to deliver a coherent, high-quality competition prototype under a tight deadline.

---

# 18. DEFINITION OF DONE

The project is complete only when all the following are true:

- The application starts successfully from documented instructions.
- The frontend and backend communicate correctly.
- Generated synthetic financial data is internally consistent.
- The 14-day forecast is calculated from underlying records.
- A real OpenRouter-supported free model can generate valid proposals when available.
- The no-API demonstration mode is clearly labeled and functional.
- Users can inspect, modify, approve, and reject actions.
- Role and mandate restrictions are enforced server-side.
- Invoice reminders and eligible expense rescheduling execute in the sandbox.
- Mock financing comparisons calculate and display transparent costs.
- Unauthorized actions are rejected by the deterministic gate.
- Financial recovery cannot be declared verified solely because an action executed.
- Audit entries form a verifiable hash chain.
- The same evaluation scenarios run in isolated gated and ungated configurations.
- Evaluation reports accurately reflect executed tests.
- All essential UI components work.
- Automated tests pass, or remaining failures are clearly disclosed.
- Documentation reflects the actual implementation.
- No fake integrations, benchmarks, or unsupported security claims appear anywhere.
- The product is suitable for a professional live demonstration.

---

# 19. FINAL COMPETITION DEMONSTRATION

The main demo should tell one compelling story:

A small business is approaching a payroll deadline.

FlowGuard Sentinel discovers a projected liquidity shortfall before it occurs.

The agent identifies overdue receivables, upcoming expenses, and possible recovery strategies.

The owner approves an invoice reminder. The agent executes it, but the verifier correctly reports that no customer payment has yet been received.

The owner then approves rescheduling an eligible expense, and the system recalculates its financial forecast.

Next, an invoice containing malicious instructions attempts to induce an unauthorized financial action.

The deterministic policy engine blocks the action and explains why.

Finally, the Evaluation Lab displays matched results from the same scenarios with and without independent policy enforcement, showing measured security outcomes rather than unsupported claims.

The closing message of the demo is:

**FlowGuard Sentinel doesn't just help financial agents take action. It verifies what they were authorized to do, what they actually did, and whether the financial problem was resolved.**

---

# 20. YOUR OPERATING INSTRUCTIONS

Begin by inspecting the available environment.

Then:

1. Briefly state your implementation strategy.
2. Create and maintain a task checklist.
3. Initialize the project.
4. Implement the system phase by phase.
5. Run the relevant commands and tests yourself.
6. Inspect failures and correct them.
7. Open or inspect the application using available browser tools.
8. Refine the interface based on actual visual results.
9. Run the complete evaluation.
10. Prepare the documentation and competition evidence.
11. Perform a final end-to-end review.

Do not stop after producing a plan.

Do not ask me to implement missing sections.

Do not replace real functionality with fake demonstrations without explicitly labeling the substitution.

Do not mark tasks complete unless you have verified them.

If external access, model availability, browser automation, or installed dependencies prevent a requirement from being fulfilled, identify the blocker and implement the most faithful safe fallback. Document exactly what remains unverified.

Make decisions that maximize demonstrable functionality, correctness, clarity, security, and presentation quality.

Use available parallel execution where it genuinely accelerates independent tasks without creating integration conflicts.

At completion, provide a concise delivery report containing:

- Implemented features.
- Application startup commands.
- Test results.
- Evaluation results.
- Screenshots or their verified paths.
- Remaining limitations.
- Competition submission readiness.

**The final objective is a complete, professional, testable, and defensible FinTechathon submission—not merely generated code.**

Start building now.
