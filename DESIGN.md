# Design direction

The user rejected both earlier versions. The pinned visual authority is now the supplied Ramp reporting and accounting PNGs. Use their compact grouped navigation, short utility bar, plain large page title, underlined tabs, period toolbar, equal reporting panels, ranked rows and dense accounting table.

Archive inspection: ramp.com.zip contains the public marketing site, not the working authenticated dashboard. Four small color declarations are extracted in frontend/app/ramp-reference.css: solar #e4f222, solarLight #f5ff78, text-primary #0c0a08 and text-hushed #0c0a0899. The app uses these values, FlowGuard's supplied black FGS logo, user-requested Poppins/Inter/IBM Plex Mono and original accessible controls. Do not claim that the reporting components were copied from the archive.

Overview shows confirmed cash and the actual fourteen-day forecast, ranked scheduled obligations, outstanding invoice bars and a stacked scheduled-spending chart. Lower ledger rows contain the actual invoice references, dates, amounts and status. The approval view uses a table with action, reference, amount, exact parameters, status and inspect controls. Charts must never replace real financial values with decorative curves. Scheduled spending is explicitly distinguished from historical spending.

Preserve the user's LLM code, environment and financial records. Verification here uses read-only browser interactions and labelled browser-only fixtures. All changes remain local, uncommitted and unpushed pending user review.

Application archive update: the user subsequently provided app.ramp.com.zip, which does contain compiled app bundles and Ryu design tokens. See docs/ramp-app-typography.md and docs/ramp-app-analysis.json. The actual app type scale and navigation metrics now guide frontend/app/typography.css; Poppins, Inter and IBM Plex Mono remain the approved fonts. Prior statements about the marketing archive do not describe this newer app archive.
