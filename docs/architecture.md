# Architecture

FlowGuard Sentinel is a local competition prototype. Next.js serves the workspace and proxies `/api` to FastAPI. FastAPI owns the synthetic business state, proposals, approvals, policy checks, execution and verification. SQLite stores persistent records using SQLAlchemy. There are no banking connections or outbound customer notifications.

The normal action path is: financial records → deterministic forecast → proposed action → owner approval of payload hash → active scoped mandate → deterministic gate → sandbox executor → independent financial verification → audit event. Editing an approved action invalidates the approval. Financing comparison has no execution path.

The language model receives bounded financial context and returns validated proposals and explanations. It has no database handle, approval capability or executor tool. Missing credentials, unavailable free endpoints, invalid output and request failures produce an explicitly labelled deterministic demonstration response.

The evaluation runner loads frozen fixtures into fresh copies for both arms and calls the same sandbox implementation. Its ungated branch exists only inside the offline runner, with no production bypass parameter. The lab displays those recorded runs. Passing this suite does not establish general prompt-injection resistance.

`backend/app/engine.py` contains the monetary model and policy boundary; `generator.py` owns reproducible fixtures; `storage.py` owns SQLAlchemy state and audit; `agent.py` owns model interaction; `main.py` exposes the API; `evaluation.py` runs the isolated comparison. `frontend/app/page.tsx` connects the workspace to these APIs. This compact structure is intentional for the prototype.
