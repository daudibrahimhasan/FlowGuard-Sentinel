# Interface component sources

Reviewed 16 October 2026. Lucide remains the sole icon system: 20 px navigation, 16–20 px controls, 1.75 stroke. Security icons describe policy; branding uses the supplied emerald FGS monogram. Both original PNGs are preserved in frontend/public/brand. CSS frames their existing whitespace without changing the source assets.

| Source | Decision | License checked |
| --- | --- | --- |
| [shadcn/ui Command](https://ui.shadcn.com/docs/components/radix/command) | Reuse its cmdk composition inside the existing Radix dialog, with FlowGuard CSS. No CLI or second styling framework. | MIT, official repository LICENSE.md |
| [cmdk](https://github.com/dip/cmdk) | Keyboard selection, filtering, listbox semantics and empty state. | MIT, installed package license retained in docs/licenses |
| [Radix](https://www.radix-ui.com/primitives/docs/components/tooltip) | Existing dialogs retained; tooltips added for collapsed navigation, including keyboard focus. | MIT, installed package license retained |
| [Lucide](https://lucide.dev/license) | Existing icon dependency retained; no alternative icon packages needed. | Installed ISC/MIT notices retained |
| [Magic UI](https://magicui.design/) / [Aceternity](https://ui.aceternity.com/) | Reviewed collections; decorative effects do not improve financial workflows here. No code or paid assets used. | No components selected |
| [HyperUI](https://www.hyperui.dev/) / [Flowbite](https://flowbite.com/docs/getting-started/introduction/) | Reviewed collections; existing tables, native filters and buttons already cover these needs without another theme/runtime. | No components selected |
| [Tremor](https://www.tremor.so/) | Reviewed charts/dashboard collection; retain the existing Recharts forecast and its financial semantics. | No components selected |

Tabler, Phosphor, Heroicons and Iconify are unnecessary for the current icon coverage. No code/assets were imported from them. Native selects retain browser keyboard behavior. Fonts remain self-hosted Poppins, Inter and IBM Plex Mono.

License notices for selected runtime packages are in docs/licenses and their installed packages. shadcn composition is adapted from its documented usage; its MIT notice is included alongside those notices. These licenses allow use and modification with their notices retained. User-supplied branding is separate from library licensing.

## Validation

Eight frontend tests and eight Playwright journeys passed, plus lint, TypeScript and production build. The new browser coverage checks arrow-key selection, an empty search, Escape focus restoration, the supplied logo and keyboard-triggered collapsed-navigation tooltips. All eight screens were captured at four viewport sizes (32 screenshots); no page errors, request failures or document overflow were detected. Desktop, mobile and collapsed navigation screenshots were inspected.

Browser financial workflows run with OPENROUTER_API_KEY empty in the test server environment so the documented deterministic scenarios are reproducible. The normal local server was restarted afterward with the workspace configuration restored. This run does not certify live model behavior.

Installed additions: cmdk 1.1.1 and @radix-ui/react-tooltip 1.4.1. Production dependency audit: zero reported vulnerabilities. Full audit still reports five high-severity findings in the existing ESLint/Next development dependency chain; no forced framework downgrade was applied.
