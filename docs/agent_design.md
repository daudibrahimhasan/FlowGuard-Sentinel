# Financial agent

The agent explains records, suggests reminders for overdue outstanding invoices and proposes moving flexible expenses. All financial computations and execution permissions remain deterministic. The recovery workspace pairs explanatory text with inspectable structured actions.

OpenRouter configuration is backend-only: `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, and `OPENROUTER_BASE_URL`. The official `openrouter/free` route was verified in public documentation during this build. A configured free model must remain free; the application never intentionally falls back to a paid model. Availability and provider-specific schema support can change.

Model requests use bounded input, timeouts, bounded retries, structured output and strict validation. External invoice text is untrusted data. A schema-valid malicious proposal still cannot execute without approval and the independent gate. Input isolation helps frame the task; the policy boundary is the authority.

Without a key or a usable free endpoint, deterministic demonstration mode generates inspectable proposals from the same underlying records. It is labelled as demonstration mode. This preserves the financial workflow without pretending a live model answered.

Live free-model inference requires a user-provided API key. No key was provided for this build, so documentation and tests distinguish adapter/error-path validation from a successful live inference. Only synthetic context should be sent during this demonstration.
