# RevalytIQ

[![CI Backend](https://github.com/OWNER/REPO/actions/workflows/backend.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/backend.yml)
[![CI Frontend](https://github.com/OWNER/REPO/actions/workflows/frontend.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/frontend.yml)
[![Deploy Backend](https://render.com/deploy)](#deployment)
[![Deploy Frontend](https://vercel.com/button)](#deployment)

Enterprise analytics platform delivering revenue insights via a Django REST API and a modern Next.js dashboard. Authentication is powered by JWT (SimpleJWT), while background analytics leverage Celery and Redis.

## Architecture

```mermaid
flowchart LR
  subgraph Client["Next.js 16 (Turbopack)"]
    UI["React UI"]
    State["Zustand / React Query"]
    Auth["JWT Tokens"]
  end

  subgraph Backend["Django REST Framework (module: revalyt)"]
    API["/api/auth/*\\n/ api/analytics/*"]
    Tasks["Celery Workers"]
    Metrics["KPI Services"]
  end

  subgraph Data["Data & Messaging"]
    DB["PostgreSQL"]
    Cache["Redis"]
    Queue["Celery Broker"]
  end

  subgraph Observability["Metrics Pipeline"]
    Logs["Structured Logs"]
    Alerts["Sentry / Dashboards"]
  end

  UI -->|JWT Login| Auth
  Auth -->|Token Exchange| API
  State -->|Fetch KPIs / Orders| API
  API --> DB
  API --> Cache
  API --> Tasks
  Tasks --> Queue
  Tasks --> DB
  Tasks --> Observability
  Observability --> State
```

## Features

- Secure JWT authentication (SimpleJWT) with refresh tokens.
- Real-time analytics dashboard with KPI and orders visualisations.
- Polished signup and login flows with REST back-end integration.
- Configurable CORS/CSRF for Next.js + Django pairing.
- Production-ready Docker Compose, CI/CD, and deployment manifests.

## Tech Stack

- **Frontend:** Next.js 16, TypeScript, Tailwind CSS, Axios, Zustand, React Query.
- **Backend:** Django 5.2, Django REST Framework, SimpleJWT, Celery.
- **Data:** PostgreSQL, Redis.
- **Tooling:** Jest, Pytest, GitHub Actions, Docker, Render, Vercel.

## Screenshots

| View | Preview |
| --- | --- |
| Dashboard | ![Dashboard](docs/screenshots/dashboard.png) |
| Signup Flow | ![Signup](docs/screenshots/signup.png) |
| KPIs | ![KPIs](docs/screenshots/kpis.png) |

> Screenshots live in `docs/screenshots/`. Replace with actual captures as the UI evolves.

## Quick Start

### Backend (Django / DRF)

```bash
cp backend/.env.example backend/.env
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (Next.js)

```bash
cp frontend/.env.example frontend/.env.local
cd frontend
pnpm install
pnpm dev
```

### Using the Makefile

```bash
make be-install
make fe-install
make up   # optional docker-compose
```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Example |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | Django settings module | `revalyt.settings.base` |
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DATABASE_URL` | PostgreSQL connection URL | `postgres://user:pass@localhost:5432/revalyt` |
| `REDIS_URL` | Redis cache URL | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/1` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated origins | `http://localhost:3000` |
| `JWT_ACCESS_LIFETIME` | Minutes | `5` |
| `JWT_REFRESH_LIFETIME` | Days | `7` |
| `TIME_ZONE` | Server timezone | `UTC` |

### Frontend (`frontend/.env.local`)

| Variable | Description | Example |
| --- | --- | --- |
| `NEXT_PUBLIC_API_URL` | Base URL of the backend API | `http://127.0.0.1:8000` |
| `NEXT_PUBLIC_APP_NAME` | Application branding | `RevalytIQ` |
| `NEXT_PUBLIC_SENTRY_DSN` | Optional Sentry DSN | *(leave blank or provide DSN)* |

## Testing

- **Backend:** `make be-test` (runs `pytest -q --disable-warnings`).
- **Frontend:** `make fe-test` (runs `pnpm test -- --watch=false`).
- Coverage reports are uploaded automatically in CI.

## Docker (Optional)

```bash
make up
# once services are healthy
make down
```

Ensure `.env` files are populated before running Compose.

## Deployment

- **Backend (Render):** Uses `render.yaml` to provision a Web Service plus managed PostgreSQL and Redis add-ons. Build installs backend requirements and collects static assets. Start command runs `gunicorn revalyt.wsgi:application --bind 0.0.0.0:8000`.
- **Frontend (Vercel):** Deploy with the included `vercel.json`. Configure `NEXT_PUBLIC_API_URL` in project settings (point preview deployments to the Render preview URL if needed).

## Troubleshooting

- **JWT issues:** Ensure system clocks are synced; adjust `JWT_ACCESS_LIFETIME`/`JWT_REFRESH_LIFETIME`.
- **CORS errors:** Double-check `CORS_ALLOWED_ORIGINS` and `NEXT_PUBLIC_API_URL`.
- **Database connections:** Verify `DATABASE_URL` matches Render/Postgres settings.
- **Celery tasks not running:** Confirm Redis broker is reachable and worker processes are deployed.

## License & Contact

Released under the MIT License. For questions or partnership inquiries, reach out to the project maintainers via `support@example.com`.

## Notes

- Django project module name: `revalyt`.
- Authentication endpoints live under `/api/auth/`.
- Analytics endpoints live under `/api/analytics/`.

## Final Verification Checklist

| Item | Status |
| --- | --- |
| README.md | ✅ |
| backend/.env.example | ✅ |
| frontend/.env.example | ✅ |
| .github/workflows/backend.yml | ✅ |
| .github/workflows/frontend.yml | ✅ |
| render.yaml | ✅ |
| vercel.json | ✅ |
| Makefile | ✅ |
| CONTRIBUTING.md | ✅ |
| SECURITY.md | ✅ |
| CODE_OF_CONDUCT.md | ✅ |
| CHANGELOG.md | ✅ |

### Runbooks

- **Local setup:** `make be-install && make be-run` and `make fe-install && make fe-dev`.
- **CI validation:** Push to GitHub; both backend and frontend workflows execute automatically.
- **Render deploy:** Apply `render.yaml`, supply environment variables, run migrations (`python manage.py migrate`).
- **Vercel deploy:** Import repo in Vercel, set env, trigger build.

