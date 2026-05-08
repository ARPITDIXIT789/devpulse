# DevPulse - Developer Productivity Dashboard

DevPulse is a full-stack productivity dashboard for developers to track daily tasks, streaks, and weekly progress.

## Features
- JWT-based signup/login
- Task CRUD (add/edit/delete)
- Dashboard stats API
- GitHub commits integration (live from GitHub API)
- Daily streak tracking
- Weekly progress chart data
- Dark/Light mode toggle
- Mobile responsive UI
- Profile page with productivity stats
- Docker + Docker Compose support
- Kubernetes manifests
- Monitoring files (Prometheus + Grafana)
- Self-healing script stub
- Telegram alerting on health down/recovery
- GitHub Actions CI/CD pipeline

## Folder Structure

```text
devpulse/
  backend/
    app.py
    config.py
    requirements.txt
    models/
    routes/
    utils/
  frontend/
    package.json
    vite.config.js
    index.html
    src/
      App.js
      main.jsx
      styles.css
      pages/
      components/
      api/
  k8s/
  monitoring/
  healing/
  docker-compose.yml
  Dockerfile.backend
  Dockerfile.frontend
  .env.example
  .github/workflows/ci-cd.yml
```

## Tech Stack
- Frontend: React + Vite + Recharts + Axios
- Backend: Flask + Flask-JWT-Extended + SQLAlchemy
- Database: PostgreSQL
- Container: Docker + Docker Compose
- Orchestration: Kubernetes
- Monitoring: Prometheus + Grafana config

## Environment Variables
Copy `.env.example` to `.env` and update values.

Backend:
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `JWT_EXPIRES_HOURS`
- `PORT`
- `GITHUB_API_URL`
- `GITHUB_TOKEN`
- `GITHUB_USERNAME`
- `GITHUB_REPOS`

Frontend:
- `VITE_API_BASE_URL`

Optional (healing/alerts extension):
- `HEALTH_URL`
- `CHECK_INTERVAL`
- `REQUEST_TIMEOUT`
- `ALERT_COOLDOWN_SECONDS`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## Ports
- Frontend (Vite): `5173`
- Backend (Flask/Gunicorn): `5000`
- PostgreSQL: `5432`

## Local Setup (Without Docker)

### Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

## Run with Docker Compose
```bash
docker compose up --build
```

## API Endpoints

Auth:
- `POST /api/auth/signup`
- `POST /api/auth/login`

Tasks:
- `GET /api/tasks`
- `POST /api/tasks`
- `PUT /api/tasks/:id`
- `DELETE /api/tasks/:id`

Dashboard:
- `GET /api/dashboard/stats`

Profile:
- `GET /api/profile`

Health:
- `GET /health`

## Kubernetes
Apply manifests:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## CI/CD
GitHub Actions workflow file: `.github/workflows/ci-cd.yml`
- Installs backend deps
- Runs backend smoke test
- Installs frontend deps
- Builds frontend

## Notes
- GitHub commit count is calculated for the current UTC day across repos in `GITHUB_REPOS`, filtered by `GITHUB_USERNAME`.
- Telegram alerts are sent when health goes down and when service recovers, with cooldown controlled by `ALERT_COOLDOWN_SECONDS`.
