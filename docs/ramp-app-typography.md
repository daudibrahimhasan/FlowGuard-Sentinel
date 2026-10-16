# Ramp application archive and typography

Inspected the user-provided app.ramp.com.zip (12,947,665 bytes, 789 entries). Unlike the earlier ramp.com archive, this capture contains compiled application bundles, DashboardNavigation, Ryu components, app design tokens and app font declarations. Static copies used for inspection stay under ignored .cache/ramp-app. No captured authentication/API payloads were executed or imported into FlowGuard.

The type scale extracted from application-Omqrq55a.js is recorded with a bundle hash in ramp-app-analysis.json:

| Token | Font size | Line height | Weight |
| --- | --- | --- | --- |
| xs | 12px | 16px | 400 |
| s | 14px | 20px | 400 |
| m | 16px | 24px | 400 |
| l | 20px | 28px | 400 |
| xl | 28px | 32px | 400 |
| xxl | 36px | 40px | 400 |

The RyuNavigationBaseButton bundle uses font-size s and line-height s: 14/20px. Text colors include primary #1A1919 and hushed #6E6A68. A separate legacy app entry also contains a light-weight variant; the existence of both variants is not evidence that every Ramp screen uses the same typography.

FlowGuard now has one explicit typography owner, frontend/app/typography.css, loaded after base styles. It uses the extracted scale with the user's requested Poppins, Inter and IBM Plex Mono. Lausanne assets in the archive are not shipped. Body, navigation and normal ledger text are 14px on desktop; supporting labels are generally 12px; headings are 36/40px with 28/32px mobile headings. Dense chart labels and metadata have explicit smaller exceptions. Tables retain tabular figures, and monospace is limited to identifiers. Secondary text was darkened instead of leaving the earlier faint 9–10px labels.

Validation: production build/TypeScript and lint pass; eight frontend tests and four read-only Playwright journeys pass. All eight views were captured at 1440×900, 1280×800, 768×1024 and 390×844 (32 captures) in submission/app-ramp-typography. No page overflow, page exception or displayed request error was detected. Desktop/mobile reporting, the recovery form and financial ledger were visually inspected. The mechanical design detector flags Inter as common; it is deliberately retained because the user requested it.

The local LLM code, environment and financial records were not modified. No commit or push was made.
