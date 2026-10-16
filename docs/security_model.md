# Security model

This is a local sandbox with three public demonstration identities. The backend maps owner, analyst and viewer to execution-with-approval, propose and read-only permissions. The switcher intentionally impersonates demo identities. It is not production authentication, and the app should remain bound to localhost unless real authentication is added.

An owner approves an exact action payload. The gate independently checks role, allowed action type, approval match, active mandate, expiry, consumption, financial cap, recipient/vendor scope, target state and protected categories. Unknown executable actions and unexpected parameters fail closed. Editing invalidates approval; repeat execution is prevented by persistent state. Payroll is protected.

The LLM cannot issue mandates, approve itself or write ledger records. Reminder delivery is simulated and cannot increase cash. Expense rescheduling can move only eligible obligations. Financing remains read-only. Sandbox receipts are explicit owner operations rather than model claims.

Audit events are hash chained with canonical serialization and exported as JSONL. Integrity checks detect edits within the retained chain. Without an external checkpoint, a privileged attacker who can rewrite the entire chain or remove its tail may defeat detection. This is tamper evidence within that boundary, not tamper proof storage.

The isolated evaluation baseline deliberately bypasses additional policy checks to measure their effect. It does not change the application's normal execution route. Forced malicious proposals test enforcement given a proposal, not the frequency with which a live model follows injections.

Known risks include public demo identities, single-machine storage, lack of external audit anchoring, model-provider availability/privacy differences and limited synthetic evaluation. No regulatory certification, WeBank integration or production banking compliance is claimed.
