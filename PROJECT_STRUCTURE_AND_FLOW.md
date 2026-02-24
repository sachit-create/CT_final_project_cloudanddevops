# Project Structure and Flow (Beginner Notes)

This file explains the whole project in simple terms, including architecture, flow, and a rough diagram.

## Big Picture

This is a 3-service microservices-style full stack project with a live monitoring dashboard:

1. `frontend` container: Nginx serves dashboard UI on host port `3000`
2. `backend` container: Flask API serves monitoring endpoints on host port `5000`
3. `database` container: PostgreSQL for data storage (internal only, no public port)

## Rough Diagram

```text
Your Browser
    |
    | http://localhost:3000
    v
+-------------------------+
| Frontend (Nginx)        |
| container: demo-frontend|
| listens: 80             |
+-------------------------+
    |
    | proxy /api/*  ---> http://backend:5000
    | (Docker internal DNS: "backend")
    v
+-------------------------+
| Backend (Flask)         |
| container: demo-backend |
| listens: 5000           |
+-------------------------+
    |
    | reads /var/run/docker.sock (read-only)
    | to inspect running containers
    |
    +-------> Docker daemon info (same host)
    |
    | uses env vars:
    | DB_HOST=database
    | DB_PORT=5432 ...
    v
+-------------------------+
| Database (PostgreSQL)   |
| container: demo-database|
| listens: 5432 internal  |
+-------------------------+
```

## Project Structure

```text
CandDevOps_finalProj/
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── index.html
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── docker-compose.yml
└── README.md
```

## How Each File Fits

1. `docker-compose.yml`
- Defines all services together.
- Creates one shared internal network automatically.
- Maps ports:
  - `3000:80` for frontend
  - `5000:5000` for backend
- Mounts Docker socket into backend:
  - `/var/run/docker.sock:/var/run/docker.sock:ro`
- No `ports` under database, so DB is private/internal.

2. `frontend/Dockerfile`
- Builds Nginx image with your `index.html` and custom `nginx.conf`.

3. `frontend/nginx.conf`
- Serves static page.
- Proxies `/api/...` calls to `http://backend:5000` (service name-based communication).

4. `frontend/index.html`
- Live dashboard UI.
- Calls `/api/dashboard` every 10 seconds and renders:
  - backend health
  - Docker container statuses
  - machine/system info

5. `backend/Dockerfile`
- Builds Python runtime image, installs Flask, starts `app.py`.

6. `backend/app.py`
- Exposes:
  - `GET /api/health`
  - `GET /api/containers`
  - `GET /api/system`
  - `GET /api/dashboard`
- Reads DB env vars.
- Reads Docker daemon info through Docker SDK.

7. `backend/requirements.txt`
- Python dependencies:
  - Flask
  - Docker SDK
  - psutil

8. `README.md`
- Explains architecture, flow, run steps, and EC2 path.

## Request Flow (Step by Step)

1. You open `http://localhost:3000`.
2. Request goes to frontend container (Nginx).
3. UI loads and auto-requests `/api/dashboard` every 10 seconds.
4. Browser calls `/api/dashboard` on same frontend host.
5. Nginx sees `/api/` path and forwards to backend container.
6. Flask collects health, container statuses, and system info, then returns one JSON payload.
7. UI renders cards/table from returned data.
8. Backend talks to DB using `DB_HOST=database` and inspects Docker state via socket mount.

## Important Concepts to Remember

1. Each service has its own container.
2. Docker Compose gives automatic internal DNS by service name.
3. Database is containerized in this setup.
4. Database is not publicly exposed because no host port mapping is defined.
5. Frontend and backend are exposed for browser/testing (`3000`, `5000`).
6. Docker socket access is powerful; keep it for learning/demo, harden for production.
