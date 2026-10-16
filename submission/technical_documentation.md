# FlowGuard Sentinel technical submission

FlowGuard Sentinel is an SME finance sandbox that forecasts a fixed 14-day cash position, proposes recovery actions, enforces exact owner approval and checks observed financial evidence after execution.

The prototype uses Next.js/TypeScript, FastAPI/Pydantic, SQLite/SQLAlchemy, Decimal monetary calculations and OpenRouter free-model integration with a labelled deterministic fallback. Synthetic retail, manufacturing and service datasets demonstrate different liquidity conditions. The language model proposes; deterministic code authorizes and calculates.

The functioning actions are simulated overdue-invoice reminders and eligible expense rescheduling. Three hypothetical financing options are calculated read-only. Reminder delivery does not imply payment. Payroll is protected. Scoped mandates, payload-bound approval, expiry and idempotency separate proposed intent from executable authority.

See `README.md` for startup, test and reset instructions; `docs/architecture.md`, `docs/financial_model.md` and `docs/security_model.md` for implementation boundaries. Source code is available at [FlowGuard-Sentinel](https://github.com/daudibrahimhasan/FlowGuard-Sentinel). The application has not been externally deployed.

Recorded paired evaluation results are in `evaluation/reports/latest.json` and `latest.md`. These are forced-proposal policy tests, not a live-model benchmark. The submission must include the known limitations and pending independent attacks alongside the results.
