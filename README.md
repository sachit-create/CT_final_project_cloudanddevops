# Beginner Microservices Full Stack Project (Docker Compose)

This project demonstrates a simple **microservices-style full stack app** with three containers:

- `frontend`: Static HTML + JavaScript served by Nginx
- `backend`: Python Flask REST API
- `database`: PostgreSQL

The goal is clarity for DevOps beginners.

## 1) Architecture

```text
Browser --> Frontend (Nginx, port 3000 on host)
              |
              | /api requests proxied internally
              v
          Backend (Flask, port 5000 on host)
              |
              | uses DB_* environment variables
              v
          Database (PostgreSQL, internal only)
```

### Why this is microservices-oriented

- Each component runs as an independent service/container.
- Services communicate over Docker Compose internal networking.
- You can update/rebuild one service without changing the others.

## 2) Role of Docker and Docker Compose

- **Docker** packages each service with its runtime and dependencies.
- **Docker Compose** defines and runs multi-container applications from one file (`docker-compose.yml`).
- Compose provides internal DNS so services can talk via service names (like `backend` or `database`).

## 3) How services communicate

- Frontend Nginx has a reverse proxy in `frontend/nginx.conf`:
  - `location /api/` forwards requests to `http://backend:5000`
- Backend receives DB connection info from environment variables:
  - `DB_HOST=database`, `DB_PORT=5432`, etc.
- Database is internal because no host port is mapped for it.

## 4) Project structure

```text
.
├── backend
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## 5) Run locally (step by step)

### Prerequisites

- Docker
- Docker Compose (v2 plugin)

### Commands

1. Build and start everything:

```bash
docker compose up --build
```

2. Open frontend in browser:

- http://localhost:3000

3. Test backend directly (optional):

```bash
curl http://localhost:5000/api/health
```

4. Stop services:

```bash
docker compose down
```

5. Stop and remove DB volume too (reset data):

```bash
docker compose down -v
```

## 6) API endpoint

- `GET /api/health`
- Returns backend status and DB-related environment values (for learning/debugging).

## 7) Deploying this on AWS EC2 (simple path)

1. Launch an EC2 instance (Ubuntu is common).
2. Open security group ports:
   - `22` (SSH)
   - `3000` (frontend)
   - `5000` (optional if you want direct backend access)
3. SSH into EC2 and install Docker + Docker Compose plugin.
4. Copy project files to the instance (`git clone` or SCP).
5. From project root, run:

```bash
docker compose up -d --build
```

6. Access app via:

- `http://<EC2_PUBLIC_IP>:3000`

### Production notes (next step)

- Use real secrets management (not plain text in compose).
- Put Nginx/ALB + HTTPS in front.
- Restrict backend port exposure if not needed publicly.

---

This setup intentionally avoids Kubernetes and CI/CD to keep learning focused on Docker basics.
