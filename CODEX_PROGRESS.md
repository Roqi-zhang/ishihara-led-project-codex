⚠️ NOTE

This file is a progress log and execution record.

It is NOT the source of truth for system logic or tasks.

The ONLY current task definition is:

→ docs/spec/TASK.md

If any historical entry conflicts with TASK.md:

→ ALWAYS follow TASK.md

---

# CODEX Progress

## Current Phase

→ PUBLIC DEPLOYMENT PHASE

---

## Current Goal

Deploy the system to public internet so that:

- users can access via public URL
- upload images
- LED display works
- messages can be submitted
- Supabase stores data correctly
- full flow works end-to-end

---

## System baseline (DO NOT CHANGE)

### Core flow

- Upload MUST happen on Page 4
- Message submission happens on Page 5
- Page 6 does NOT upload
- LED display uses /next_image + /mark_shown

### Backend endpoints (frozen)

- POST /upload_generated
- POST /update_message
- GET /next_image
- POST /mark_shown
- GET /queue

### Frontend structure

- 6 HTML pages must remain unchanged
- No UI / layout / structure changes allowed

---

## Allowed scope

Only minimal deployment-related work:

- backend deployment (Render / Railway)
- frontend deployment (Vercel / Netlify)
- requirements.txt fixes
- gunicorn setup
- Flask production config
- CORS enabling
- backend URL configuration

---

## Forbidden scope

- no refactor
- no UI change
- no flow change
- no endpoint change
- no DB schema change
- no Supabase modification

---

## Environment requirement

Frontend must support:

localStorage["ISHIHARA_BACKEND_URL"]

After deployment, this should be:

https://your-backend.onrender.com

---

## Task log

---

### Task 1

Status: COMPLETED

What was done:
- Added missing direct runtime dependencies to backend/requirements.txt:
  - supabase==2.28.3
  - python-dotenv==1.2.2
  - httpx==0.28.1

Why:
- backend/app.py directly imports and uses supabase, dotenv, and httpx at startup.
- Public deployment installs from requirements.txt, so these packages must be listed explicitly.

Files changed:
- backend/requirements.txt
- CODEX_PROGRESS.md

How to verify:
- Run: pip install -r backend/requirements.txt
- Run: python -c "import httpx; from dotenv import load_dotenv; from supabase import create_client"
- Confirm Flask / flask-cors / gunicorn lines remain unchanged in backend/requirements.txt
- Confirm no business logic or API code was modified

Constraint:
- NO logic change
- NO API modification

---

### Task 2

Status: COMPLETED

What was done:
- Added frontend/vercel.json with a root path rewrite from / to /1前端页面.html

Why:
- The frontend directory did not have a root entry mapping for static hosting.
- This deployment-only config makes the public frontend root URL open Page 1 directly on Vercel.

Files changed:
- frontend/vercel.json
- CODEX_PROGRESS.md

How to verify:
- Confirm frontend/vercel.json exists and only contains the approved rewrites config
- Deploy with frontend/ as the Vercel Root Directory
- Visit the public frontend root URL /
- Confirm / opens 1前端页面.html directly
- Confirm no HTML, frontend logic, backend logic, or API logic was modified

Constraint:
- NO logic change
- NO API modification

---

### Task 3

Status: COMPLETED

What was done:
- Added a deployment-only script to frontend/1前端页面.html that seeds localStorage["ISHIHARA_BACKEND_URL"] with the Render backend URL.
- The script only runs on https://ishihara-led-project-codex.vercel.app and does not overwrite an existing value.

Why:
- First-time public users on the Vercel frontend need the correct backend URL automatically.
- This keeps the existing frontend fetch logic unchanged while providing the deployment address as configuration.

Files changed:
- frontend/1前端页面.html
- CODEX_PROGRESS.md

How to verify:
- Open https://ishihara-led-project-codex.vercel.app/ for the first time
- In DevTools Console, run: localStorage.getItem("ISHIHARA_BACKEND_URL")
- Confirm the value is https://ishihara-led-project-codex.onrender.com
- Pre-set a different ISHIHARA_BACKEND_URL value and refresh; confirm it is not overwritten
- Open the page locally or on a LAN host; confirm the production Render URL is not auto-written
- Confirm the existing page transition from Page 1 to Page 2 still works unchanged

Constraint:
- NO logic change
- NO API modification

---

## Execution protocol

For every task:

1. Ask mode first
2. One minimal change only
3. Wait for approval
4. Implement
5. Update this file
6. Report and stop

---

## Risk awareness

- CORS issues
- HTTPS mixed content
- Supabase latency
- mobile network instability

These must NOT lead to logic changes unless confirmed

---

END
