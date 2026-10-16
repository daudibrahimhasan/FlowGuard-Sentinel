# API contract and delivery checklist
All work and installs remain in this project directory. Backend port 8000, frontend 3000. Next rewrites /api/* to backend /api/*. Monetary JSON numbers are CNY, backend Decimal internally. Synthetic as-of 2026-10-16. Demo identities: owner, analyst, viewer via X-Demo-User header; server maps roles. Demo only, no real auth claims.

GET /api/businesses -> [{id,name,sector,scenario}]
GET /api/businesses/{id}/dashboard -> {business,current_cash,minimum_balance,shortfall_date,shortfall_amount,overdue_total,forecast:[{date,inflow,outflow,balance,conservative_balance}],invoices:[],expenses:[],verification:{status,message},proposals:[]}
Invoice fields: id,customer,recipient,amount,paid,due_date,status,description. Expense: id,vendor,amount,date,category,flexible.
Proposal: id,business_id,type (invoice_reminder|expense_reschedule),target_id,recipient nullable,new_date nullable,amount,reason,message,status (proposed|approved|executed|rejected), execution nullable.
POST /api/businesses/{id}/proposals -> generates proposals; body {question?:string}; returns {mode,message,proposals:[]}
PATCH /api/proposals/{id} body {new_date?:str,message?:str,recipient?:str} -> proposal; invalidate approval
POST /api/proposals/{id}/approve -> proposal
POST /api/proposals/{id}/reject -> proposal
POST /api/proposals/{id}/execute -> {proposal,verification,policy}
POST /api/businesses/{id}/receipts body {invoice_id,amount} -> dashboard (owner sandbox event)
GET /api/businesses/{id}/financing -> {options:[{name,principal,annual_rate,fee,term_days,interest,total_repayment,total_cost,repayment_schedule,risk}],assumptions}
GET /api/proposals/{id}/preview -> read-only saved-action forecast on a copy: {available,current_minimum,proposed_minimum,change,confirmed_cash_change:0,note,approval_granted:false}; invalid/protected/terminal actions return {available:false,reason}. No execution or approval capability.
GET /api/security -> {identities,mandates,blocked,protected_categories,audit_integrity}
GET /api/audit?q= -> {events:[],integrity:{valid,count}} events id,timestamp,event,business_id,details,hash,previous_hash
GET /api/evaluation -> persisted report or unavailable; POST /api/evaluation/run -> run isolated evaluation report
Evaluation owns backend/app/evaluation.py and backend/tests/test_evaluation.py; backend agent owns other backend files. Evaluation may import app.engine policy_check and forecast after coordination.

- [x] Foundation and sourced assumptions (illustrative parameters documented)
- [x] Backend financial state, policy, agent adapter, audit and tests (live key unavailable)
- [x] Frontend eight connected screens
- [x] Paired evaluation and reports (six external contributions pending)
- [x] Browser checks, production build, documentation (Docker unavailable; see validation)
