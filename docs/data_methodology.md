# Synthetic data methodology

All names, addresses, invoices, counterparties, records and outcomes are fictional. Reporting currency is CNY. The reference date is 16 October 2026, fixed to keep the competition story reproducible. Each business has a historical ledger, linked invoices and receipts, outstanding receivables and scheduled obligations. Seed 41 is the default; regenerate with `python -m app.generator` from `backend` using its local environment.

The three profiles represent retail distribution, electronics manufacturing and professional services. They demonstrate moderate, serious and healthy liquidity situations. These categories are intended scenarios rather than labels inferred from population data. The moderate case is the main demonstration, with payroll due 12 days after the reference date.

Amounts, collection-delay distributions, expense timing and seasonality are illustrative modelling decisions. Their implementation is directly inspectable in `backend/app/generator.py`. They are not fitted to confidential data or claimed to reproduce Chinese SME statistics. Public research and its use are recorded in `data/sources/research_notes.md`.

The default generator uses 30 retail, 12 manufacturing and 18 services historical invoices, with a 14-day contractual term. Historical delays are sampled from 0, 3, 7 and 14 days with weights 45%, 30%, 20% and 5%. A monthly sine factor varies invoice amounts by up to 12%. These choices are invented illustrative distributions, not sourced statistics. Historical invoices are placed far enough before the reference date to settle; three explicit open invoices create the forward collection scenario. Their expected dates are scenario assumptions rather than a fitted customer-history predictor. That is a simplification of the requested history-informed collection model.

The final retail fixture has CNY 42,000 recorded cash and a CNY 2,000 expected shortfall on 28 October, the payroll date. The manufacturing fixture has a CNY 27,350 minimum expected deficit, and services stays positive. These are calculated outputs covered by regression tests, not dashboard constants.

Invoice receipts reduce outstanding balances, and receipts refer to their source invoice. Historical opening cash plus ledger movements reconciles to current cash. Owner funding/draw events, where present, are explicitly labelled synthetic capital movements. Scheduled payroll remains an obligation regardless of proposals. Future expected collections are separate from historical receipts.

Automated checks cover reproducibility, ledger reconciliation, running balances, invoice receipt totals and logical dates. Future forecasts can go negative as a warning; the historical dataset must not contain unexplained overdrafts. A generated dataset passing these checks is internally consistent, not externally validated economic evidence.
