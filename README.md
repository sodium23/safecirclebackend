# SaferCircle Backend

Backend-only API service for **SaferCircle: Confidence & Safety Operating System for Women**.
This repo is intentionally frontend-agnostic so mobile/web clients can call its APIs.

## Stack
- FastAPI
- Pydantic
- Gemini API integration (`google-generativeai`)

## What is implemented (MVP API surface)
- Health and service metadata
- Daily power ritual scenario endpoint
- Freeze breaker (`Ground Me`) endpoint
- Mentor coaching endpoint (Tough Older Sister tone)
- Decision consequence simulator endpoint

## API Endpoints
- `GET /` - service banner
- `GET /health` - health check
- `GET /training/ground-me` - freeze-breaker tool
- `GET /training/daily-scenario` - daily scenario ritual
- `POST /mentor/coach` - structured mentor response
- `POST /mentor/decision-simulator` - option consequence mapping

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Railway deployment (important)
This repository is Python-only. If Railway tries `npm install`, your service is using the wrong builder/settings.

Included deploy files:
- `nixpacks.toml` (forces Python toolchain and relies on Nixpacks default Python install flow)
- `railway.json` (explicit start command + healthcheck)
- `Procfile` (web process fallback)
- `requirements.txt` (dependency source for deploy)

### Railway service settings to verify
1. **Builder**: `NIXPACKS`
2. **Root Directory**: repository root (where `requirements.txt` exists)
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Remove any old **Build Command** like `npm install`
5. Make sure command is **`app.main:app`** (not `main:app`)

### If build fails around pip/ensurepip
Use this repository root as service root, keep builder as `NIXPACKS`, and avoid custom pre-build commands.
The project now relies on Railway/Nixpacks default Python dependency install flow from `requirements.txt`.

### If Railway is still using an old repository
This is a Railway project-link issue (not backend code). Do this in Railway UI:
1. Open the service → **Settings** → **Source**.
2. Disconnect current GitHub repo.
3. Reconnect and select the correct repository + branch.
4. Confirm **Root Directory** is this backend repo root.
5. In **Variables/Settings**, remove stale custom Build/Start overrides copied from the old repo.
6. Trigger **Redeploy** (or "Deploy Latest Commit").

Tip: if the deploy log references files you do not have in this repo, Railway is still linked to the wrong source or root directory.

## Gemini configuration
Create a `.env` file:
```bash
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash
```

If no API key is provided, the backend returns deterministic fallback responses so frontend integration can proceed.

## Suggested next backend milestones
1. Authentication and tenant-safe user identity
2. Persistent storage for scenario logs, people patterns, and streaks
3. Event telemetry for retention loops
4. Guardian Lite workflows (SOS contacts, check-ins)
5. Secure evidence vault encryption + export pipeline
