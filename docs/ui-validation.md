# UI redesign validation

The redesign follows the inspected references documented in [ui-reference-analysis.md](ui-reference-analysis.md). The application retains its existing financial model, roles, owner approval, policy gate, sandbox executor, outcome verifier, audit chain and isolated paired evaluation.

## What changed

- Grouped, collapsible navigation and a keyboard navigation palette (Ctrl/Cmd+K).
- A utility header with business and identity selection, operational page titles and consistent tokens.
- An overview metric band, calculated cash chart, sorted obligations, outstanding invoice table, financial verification and real recent audit activity.
- Expected/conservative chart controls, invoice search and status filters, approval status filters and audit event-type filters.
- A focused side drawer for exact-payload inspection, editing, authorization, execution and current financial verification.
- Read-only saved-proposal forecast previews. These calculate on a copy of financial state, never grant approval, and reject protected or invalid deferrals. Current/with-proposal minima and zero confirmed cash change are explicit.
- Readable standing limits, consumed/active mandates, permitted vendors and recipient allowlists, with expandable raw evidence.
- Plain-language policy-denial errors, retryable financial reads, mobile navigation and reduced-motion support.

The underlying policy and forecast engine was not rewritten. The only backend feature addition is `GET /api/proposals/{id}/preview`, tested for no business/audit mutation and no execution authority.

## Verification

Final results are recorded in the delivery report and machine evidence:

| Check | Result |
|---|---|
| Backend pytest | 29 passed |
| Frontend component/API tests | 8 passed |
| ESLint | Passed without lint warnings |
| TypeScript | Passed |
| Production Next.js build | Passed |
| Playwright workflow tests | 7 passed |
| Primary-screen layout review | 32 captures: 8 screens × 4 viewports, zero document overflow, page exceptions or visible request errors |

The viewports are exactly 1440×900, 1280×800, 768×1024 and 390×844. Tables intentionally scroll within their own panels on small screens. Review screenshots are in [submission/ui-review](../submission/ui-review/), with observations in [results.json](../submission/ui-review/results.json). Browser workflow evidence is in [browser-results.json](../submission/browser-results.json).

Browser journeys cover business switching, shortfall inspection, reminder delivery without cash, forecast preview, modified approval invalidation, expense execution, rejection, partial receipts, current verification, a changed-recipient policy block, Security center evidence, paired evaluation, audit, invoice filters, chart controls, command navigation, collapse/mobile navigation and recovery from a failed API read.

Saved screenshots show different synthetic workflow stages. After preserving action evidence, the app is reset to its original payroll-shortfall story. The startup script now waits for both backend and frontend readiness. The production frontend and backend remain available on localhost with no model key needed.

## Limits

Live OpenRouter inference, independent attack contributions, production identity/authentication, Docker runtime and empirical forecast accuracy remain outside this visual validation. Existing notices remain visible. Non-failing toolchain warnings include the Starlette/httpx test-client deprecation and Vitest's future native-config-loader notice. No claim of production banking readiness or regulatory certification is added.

The designer MCP server was unavailable. Its local reference guidance was used, followed by screenshot review and actual browser checks; no automated design-gate score is claimed.
