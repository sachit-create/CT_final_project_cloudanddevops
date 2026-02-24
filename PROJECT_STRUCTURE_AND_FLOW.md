# Project Structure and Flow (Beginner Notes)

This file explains the whole project in simple terms, including architecture, flow, and a rough diagram.

## Big Picture

This is a 3-service microservices-style full stack project:

1. `frontend` container: Nginx serves `index.html` on host port `3000`
2. `backend` container: Flask API serves `/api/health` on host port `5000`
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
- No `ports` under database, so DB is private/internal.

2. `frontend/Dockerfile`
- Builds Nginx image with your `index.html` and custom `nginx.conf`.

3. `frontend/nginx.conf`
- Serves static page.
- Proxies `/api/...` calls to `http://backend:5000` (service name-based communication).

4. `frontend/index.html`
- Simple UI button.
- Calls `/api/health`, shows JSON response.

5. `backend/Dockerfile`
- Builds Python runtime image, installs Flask, starts `app.py`.

6. `backend/app.py`
- Exposes `GET /api/health`.
- Reads DB env vars so you learn config-by-environment.

7. `backend/requirements.txt`
- Python dependencies (Flask).

8. `README.md`
- Explains architecture, flow, run steps, and EC2 path.

## Request Flow (Step by Step)

1. You open `http://localhost:3000`.
2. Request goes to frontend container (Nginx).
3. UI loads, you click `Check Backend Health`.
4. Browser calls `/api/health` on same frontend host.
5. Nginx sees `/api/` path and forwards to backend container.
6. Flask handles endpoint and returns JSON.
7. UI prints returned JSON.
8. Backend can talk to DB using `DB_HOST=database` (container name on internal network).

## Important Concepts to Remember

1. Each service has its own container.
2. Docker Compose gives automatic internal DNS by service name.
3. Database is containerized in this setup.
4. Database is not publicly exposed because no host port mapping is defined.
5. Frontend and backend are exposed for browser/testing (`3000`, `5000`).
