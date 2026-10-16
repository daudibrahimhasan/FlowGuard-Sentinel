# Known limitations

- All businesses and outcomes are synthetic; economic parameters are illustrative rather than calibrated to Chinese SMEs.
- The reference date is fixed to 16 October 2026 for reproducible demonstration.
- Public demo identities exercise server roles but provide no production authentication. Use localhost.
- No API key was supplied. Live OpenRouter inference remains unverified; deterministic mode and adapter/error behavior are testable without paid services.
- Free endpoint availability, schema support and rate limits can change. There is no paid fallback.
- The evaluation uses 28 self-authored frozen proposals. Six independent attack contributions are pending. Results do not estimate real-world attack prevalence or live-model injection susceptibility.
- Forecast accuracy is tested against independently seeded synthetic receipts, not real business data.
- Forward collection dates are explicit scenario assumptions; a fitted customer-payment-history estimator is not implemented.
- Hash chains lack external anchoring. A privileged full rewrite or tail truncation can evade local verification.
- Docker is not installed in this environment. Container definitions are supplied, but a Compose build and runtime must be verified on a Docker-equipped machine.
- Source code is available at [FlowGuard-Sentinel](https://github.com/daudibrahimhasan/FlowGuard-Sentinel). No public application deployment, lender integration or competition submission has been created. Submission packaging remains subject to the official portal's current requirements.
- Dependency auditing reported five development-tool advisories. The production dependency audit reported zero vulnerabilities at validation time.
