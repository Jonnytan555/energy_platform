uv run uvicorn app.main:app --reload

# Energy Platform — Runbook (Local / Dev / Staging / Prod)

This README explains how to run the project in **four environments**:

1. **local** — no Docker, API + local Postgres + local frontend (Celery optional via flag)
2. **dev** — Docker Compose (Postgres + Redis + API + Worker + Flower + optional UI)
3. **staging** — no Docker, no Celery/Redis; server runs API only (prod settings)
4. **prod** — Docker Compose on Ubuntu (Postgres + Redis + API + Worker + Flower + Nginx)

---

## 0) Prereqs

### Local machine (Windows)
- Python 3.11
- Postgres installed locally (or a remote Postgres you can reach)
- Node 18+ (if running frontend locally)
- (Optional) Redis installed locally if you want to test Celery without Docker

### Servers (Ubuntu)
- Python 3.11 + venv (staging)
- Docker + Docker Compose plugin (prod)

---

## 1) Environment files (how we switch configs)

We use **one env file per environment**, and optionally a boolean flag for Celery.

Recommended files:
- `.env.local`  (local dev on your machine)
- `.env.dev`    (docker dev)
- `.env.prod`   (staging + prod)

The app chooses an env file via the `ENV_FILE` environment variable.

### Windows PowerShell
```powershell
$env:ENV_FILE=".env.local"
uvicorn app.main:app --reload

Windows CMD
set ENV_FILE=.env.local
uvicorn app.main:app --reload

Linux/macOS
ENV_FILE=.env.local uvicorn app.main:app --reload

2) Example .env.local (API-only by default)

Local is API + local Postgres + local frontend.
Redis/Celery is optional by flipping CELERY_ENABLED.

ENV=local

# Toggle Celery locally when you want
CELERY_ENABLED=false

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=energy_db
DATABASE_USER=postgres
DATABASE_PASSWORD="Winter1963#"

# Optional local Redis/Celery testing
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

CORS_ORIGINS=http://localhost:5173,http://localhost:3000

3) LOCAL: run without Docker (API + Postgres + Frontend)
3.1 Create venv + install deps

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt


If you use Pydantic EmailStr, install:

pip install email-validator


If you have from retry import retry, ensure you have:

pip install retry


If you have a private wheel (scraper):

pip install .\wheels\scraper-0.1.2-py3-none-any.whl

3.2 Run DB migrations (local Postgres)
$env:ENV_FILE=".env.local"
alembic upgrade head

3.3 Run API
$env:ENV_FILE=".env.local"
uvicorn app.main:app --reload


Open:

API docs: http://localhost:8000/docs

Health: http://localhost:8000/health

3.4 Run Frontend locally (Vite/React)

From frontend/:

npm install
npm run dev


Frontend:

http://localhost:5173

4) LOCAL: optionally enable Celery + Redis (still no Docker)
4.1 Start Redis locally

If you have Redis running as a service, just verify:

redis-cli ping

4.2 Enable Celery in .env.local
CELERY_ENABLED=true
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

4.3 Run API
$env:ENV_FILE=".env.local"
uvicorn app.main:app --reload

4.4 Run Celery worker (new terminal)
$env:ENV_FILE=".env.local"
python -m celery -A app.celery_app:celery_app worker --loglevel=INFO -E


(Optional) Flower (new terminal):

$env:ENV_FILE=".env.local"
python -m celery -A app.celery_app:celery_app flower --port=5555


Open:

Flower: http://localhost:5555

5) DEV: run with Docker Compose (Postgres + Redis + API + Worker + Flower)
5.1 Use compose overlays + env file

Example:

docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up --build

5.2 Run only API (to test quickly)
docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up --build api


Or run only API + dependencies:

docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up --build postgres redis api


Open:

API docs: http://localhost:8000/docs

Flower: http://localhost:5555

Tip: if your compose file doesn’t define api, you’ll get no such service: api.
Run docker compose config --services to see the actual service names.

6) STAGING: no Docker, no Celery, no Redis (server runs API only)
6.1 On Ubuntu server
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv
git clone <your-repo>
cd energy_platform

python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt


Install private wheel (if needed):

pip install ./wheels/scraper-0.1.2-py3-none-any.whl


Set env file:

export ENV_FILE=.env.prod


Run migrations:

alembic upgrade head


Run API:

uvicorn app.main:app --host 0.0.0.0 --port 8000


On staging .env.prod, set:

CELERY_ENABLED=false

7) PROD: Docker Compose on Ubuntu (full stack)
7.1 Pull latest + run
git pull
docker compose --env-file .env.prod up -d --build

7.2 View logs
docker compose logs -f api
docker compose logs -f worker