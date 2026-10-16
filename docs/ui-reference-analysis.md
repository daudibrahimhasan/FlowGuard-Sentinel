# UI reference analysis

Reviewed on 16 October 2026 before implementation. Sources were read from the user-provided locations; all extracted inspection assets stay in the project's ignored `.cache/ui-references/` directory. No computer-use skill or native UI control was used.

## What was actually inspected

The inspiration folder contains three website archives, not authenticated application exports: `ramp.com.zip` (610 files), `mercury.com.zip` (435), and `linear.app.zip` (651). The inventory in `ui-reference-inventory.json` records each archive entry. Root HTML, headings and available CSS were inspected; raster content was decoded by file signature, including images saved with `.html` extensions. Contact sheets covered 8 Ramp, 25 Mercury and 9 Linear qualifying raster assets, and the financial product screenshots were inspected at larger sizes. Scripts, trackers and server/API captures were not executed.

The four supplied PNGs were also opened. All four show Ramp or Ramp-style financial product screens: a monitor/mobile product photograph, reporting with a chart and adjacent ranked table, a reimbursements table with a contextual selection bar, and a dense card-transactions review table. They provide stronger evidence of financial workspace structure than the marketing archives. No supplied PNG was attributed to Mercury or Linear.

## Reusable observations

| Reference | Observed pattern | Application to FlowGuard |
|---|---|---|
| Ramp reporting PNG | Compact warm-grey navigation, ordinary page title, thin underlined tabs, chart and adjacent data panel, subtle rectangular borders | Group the sidebar by finance/operations/trust, use operational page titles, separate chart analysis from actionable obligations |
| Ramp reimbursements/transactions PNGs | Search/filter toolbar, aligned numeric columns, status near the affected row, lightweight row dividers, contextual actions | Search and filter real invoices and approvals, expose exact action state, keep tables useful without decorative cards |
| Ramp archive cash/treasury image | Balances adjacent to chart, approval rows directly below financial context | Compact metric band, chart-first overview, actionable recovery rows rather than a promotional assistant tile |
| Mercury archive dashboard/invoicing/team assets | Fine borders, restrained account amounts, coherent grouping, concise forms and permission language | White working surfaces, generous measured spacing, readable money, understandable mandate details |
| Linear archive issue lists/assignment menu/mobile inbox | Compact hierarchical rows, local status, deliberate selected states and small contextual menus | Keyboard navigation palette, collapsible sidebar, consistent 180ms interactions and accessible detail drawer |

Marketing artwork, customer portraits, logos, bank-card graphics, Ramp's yellow brand accent and Linear's dark marketing treatment are not copied. No proprietary reference asset is shipped in the application. Motion quality cannot be inferred from a static PNG; the implemented timing is our design decision, not a claim about the references.

## Committed direction

Product register, restrained premium system. A business owner checks payroll exposure at a daylight desk: warm-grey navigation, white content, charcoal text, deep-emerald actions and amber risk. Ramp supplies approximately 70% of the structural influence; Mercury 20% of the surface/type restraint; Linear 10% of interaction discipline. These are qualitative weights, not copied layouts or measured similarity.

Use a 224px collapsible navigation rail, 60px utility header, 32px content gutters, 24px Poppins page titles, 13px Inter tables/body, 12px supporting labels, IBM Plex Mono identifiers, 6px control radii and 8px panel radii. Financial numerals are tabular. Metric bands and flat tables are distinct from bordered analysis panels. The financial chart uses actual 14-day backend data and a zero-cash reference. No hero copy, giant assistant card, neon, stock illustration or decorative AI artwork.

## Implementation and validation checklist

- [x] Inspect references and existing API/workflow boundaries.
- [x] Rebuild shared shell and tokens; refine all eight existing views.
- [x] Add useful record filters, navigation shortcuts and readable evidence details.
- [x] Validate permissions, edit/approve/reject/execute, verifier and evaluation flows.
- [x] Inspect all primary views and 1440×900, 1280×800, 768×1024, 390×844 layouts.
- [x] Run lint, TypeScript, component/browser tests and production build.

The financial backend and its security authority stay intact. Any pending external validation remains documented separately from visual completion.
