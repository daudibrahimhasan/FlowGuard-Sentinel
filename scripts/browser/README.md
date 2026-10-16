# Browser checks

Run the backend and frontend first. The owner journey changes synthetic demo state, so reset the backend before rerunning from a clean demo.

From the project root, install the browser tooling locally:

```powershell
npm install --prefix scripts/browser --cache scripts/browser/.npm-cache
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path (Get-Location) '.cache/ms-playwright'
node scripts/browser/node_modules/@playwright/test/cli.js install chromium
Push-Location scripts/browser
node node_modules/@playwright/test/cli.js test --config playwright.config.cjs
Pop-Location
```

Screenshots are written under `submission/screenshots/`, and machine results to `submission/browser-results.json`. Backend tests additionally cover denied policy paths, exact approval invalidation, protected payroll, receipt reconciliation and controlled audit tampering without damaging the demonstration audit trail.

To capture all eight primary screens at the four UI review viewports, run `node scripts/browser/ui-review.cjs` from the project root with the same project-local PLAYWRIGHT_BROWSERS_PATH. The read-only review writes screenshots and results to `submission/ui-review/`. It is separate from the state-changing workflow tests.
