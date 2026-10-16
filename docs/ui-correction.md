# UI correction, local review

The previous presentation was rejected by the user. Passing functional tests did not establish visual similarity. Do not push or commit this correction without renewed user authorization.

Pinned references remain Ramp reporting and accounting composition, Mercury restraint and typography, and Linear keyboard behavior. Poppins/Inter/IBM Plex Mono and supplied FGS branding are retained. The old green-tinted dashboard is not visual authority.

Correction: neutral white canvas and warm-grey compact sidebar; 45 px utility header; flat panels with 3 px corner radii and thin neutral dividers; dark primary action; blue-grey forecast. Cash figures belong inside the forecast panel, with obligations alongside and receivables/approval evidence below. The large detached KPI strip is removed. Financial navigation tabs work. Shared table, proposal, dialog and control styling follows the same system.

Work is limited to UI and read-only checks. Existing local LLM integration, environment settings and financial records are preserved. No new LLM requests, approved actions, receipts or dataset resets are part of this correction.

Validation of this local revision: lint, production compilation/TypeScript and eight frontend tests passed. Three read-only Playwright journeys passed (financial navigation and recorded scenarios; invoice filtering/chart/mobile navigation; command keyboard/focus/tooltips). All eight views were captured at 1440×900, 1280×800, 768×1024 and 390×844 in submission/ui-correction; the result contains no document overflow, page exceptions or displayed request errors. The desktop/mobile overview and financial-table screenshots were visually inspected. Full financial mutation tests were intentionally not rerun against the user's live-provider workspace.

The revised interface is available on the local production server at http://localhost:3000. These changes remain uncommitted and unpushed for user review.

## Latest direction after the user supplied the Ramp screenshots again

The interim neutral-panel revision was also rejected. The latest local build follows the provided reporting screenshot directly: a short utility bar, compact grouped navigation, large plain title, underlined reporting tabs, bordered period label, equal analytical panels, ranked obligations, receivable bars and an actual stacked category chart. Approvals now use a ledger table instead of proposal cards.

Archive inspection confirmed ramp.com/index.html is the public marketing page (title: Spend Management, Corporate Cards & Accounts Payable Solutions). Its five CSS files include marketing styles, IBM Plex Sans/Lausanne font declarations and public-site design tokens. No working authenticated reporting/accounting React application was found. The implementation extracts four small CSS color declarations into frontend/app/ramp-reference.css; reporting structure is rebuilt from the user-provided PNGs and connected to existing FlowGuard APIs. No marketing trackers or external application scripts were imported.

Latest validation: production build/TypeScript, lint, eight frontend tests, four read-only browser journeys and 32 viewport/view captures pass. A populated approval table was checked using explicitly labelled browser-only fixtures; no proposals were added to the server and no LLM requests were made. The mobile ledger scrolls within its own table container. Final captures are in submission/ramp-rebuild. This is a local revision for user visual review, not a claim of pixel-identical Ramp source reuse. No commit or push was made.
