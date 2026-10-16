# Research notes
Checked 2026-10-16. All businesses, amounts, delays, interest rates and seasonal factors in this prototype are illustrative synthetic assumptions, not estimates calibrated to Chinese SMEs.

| Source | Publication / coverage | Finding and implementation use |
|---|---|---|
| OECD, Financing SMEs and Entrepreneurs 2024, https://www.oecd.org/en/publications/financing-smes-and-entrepreneurs-2024_fa521246-en/full-report.html | 13 March 2024; nearly 50 economies, official data mainly through 2022 | Financing conditions and payment delays vary across economies. Generator separates receivables, scheduled obligations and realized collections; no numerical parameter copied into the generator. |
| OECD Scoreboard 2023 highlights, https://www.oecd.org/content/dam/oecd/en/publications/reports/2023/03/oecd-financing-smes-and-entrepreneurs-scoreboard-2023-highlights_6060c026/a8d13e55-en.pdf | 2023; participating Scoreboard economies, data through 2021 | Reports a cross-country median payment delay of 12 days in 2021 versus 14 in 2020. Context only: not a China-specific delay distribution and not used as a fitted parameter. |
| OpenRouter free router, https://openrouter.ai/openrouter/free | Undated live documentation; global service | Official free router supports feature-aware selection among free endpoints. Use zero-cost routes only, schema validation, bounded retries and explicit deterministic fallback. |
| OpenRouter structured outputs, https://openrouter.ai/docs/guides/features/structured-outputs | Undated live documentation; endpoint-specific | JSON schema support varies by provider. Request supported parameters and validate returned data independently. |
| OpenRouter pricing, https://openrouter.ai/pricing | Undated live page | Free models have limits; availability is not guaranteed. No paid fallback. Do not hardcode capacity promises. |

Competition site https://fintechathon.g-ican.com/ returned a JavaScript-only shell in research retrieval. Topic, deadline and judging weights are supplied by the user's brief, not independently verified competition rules.

## Modelling choices
The model uses business-specific recurring payroll, rent, inventory or service expenditure, invoices with issuance/due/payment dates and partial receipts, and deterministic seeded variation. Exact amounts, seasonality and delay distributions are documented with the generator. There is no claim that a synthetic sample reproduces a population distribution. CNY is reporting currency, with no FX conversion. Interest comparisons use explicit hypothetical simple-interest assumptions, not actual lender offers.

Receivable collections remain uncertain. A reminder creates a delivery record, not a receipt. Expense deferral changes timing, not total liabilities. Payroll remains protected. A range constructed from delayed/no collections is an assumption-based scenario range, not a confidence interval.
