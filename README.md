# RevalytIQ

## 🚀 Project Overview

RevalytIQ is a production-grade analytics platform delivering revenue insights via a Django REST API and a modern Next.js dashboard. Authentication is powered by JWT (SimpleJWT), while background analytics leverage Celery and Redis, and WebSockets keep dashboards current in real time.

> 🆓 **Live Demo**  
- Backend (Render): https://revalytiq-backend.onrender.com  
- Frontend (Vercel): https://revalyt-iq.vercel.app  
- Demo credentials: `demo@revalytiq.com` / `password123`

The live demo runs in **Demo Mode** on Render’s free tier: Celery tasks execute synchronously, Redis is stubbed with in-memory backends, and deterministic demo data is seeded on every deploy. Production deployments can re-enable Redis + worker tiers without code changes.

## 🧩 Tech Topics / Tags

`django` `nextjs` `dashboard` `analytics` `celery` `redis` `jwt` `realtime` `websocket`

[![CI](https://github.com/KAPSULA1/RevalytIQ/actions/workflows/ci.yml/badge.svg)](https://github.com/KAPSULA1/RevalytIQ/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-70%25-brightgreen)](#testing)
[![Deploy Backend](https://render.com/deploy)](#deployment)
[![Deploy Frontend](https://vercel.com/button)](#deployment)

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

> **Demo mode note:** On Render free tier, the Celery/Redis components above are executed inline (synchronously) while the rest of the architecture remains unchanged. Production deployments can flip the feature flags back on to restore dedicated workers.
```

## Features

- Secure JWT authentication (SimpleJWT) with refresh tokens.
- End-to-end auth flows: signup with confirmation, login redirects, protected dashboard, password reset, and profile management.
- Real-time analytics dashboard with KPI and orders visualisations.
- Polished signup and login flows with REST back-end integration.
- Configurable CORS/CSRF for Next.js + Django pairing.
- Production-ready Docker Compose, CI/CD, and deployment manifests.
- Demo mode runs on free Render + Vercel tiers with automatic data seeding, while production mode enables Redis/Celery workers for background analytics.

## Tech Stack

- **Frontend:** Next.js 16, TypeScript, Tailwind CSS, Axios, Zustand, React Query.
- **Backend:** Django 5.2, Django REST Framework, SimpleJWT, Celery.
- **Data:** PostgreSQL, Redis.
- **Tooling:** Jest, Pytest, GitHub Actions, Docker, Render, Vercel.

## 💡 Why This Stack

- **Type-safe UI:** Next.js 16 + TypeScript deliver fast iteration with React Server Components and predictable DX.
- **Battle-tested API:** Django REST Framework keeps business logic explicit while SimpleJWT + cookie auth align with modern security guidance.
- **Data freshness:** Celery workers, Redis, and scheduled KPI aggregation keep dashboards fast without blocking API traffic.
- **Operational polish:** Docker Compose, Render, and Vercel manifests provide copy/paste infrastructure for portfolio or production rollouts.

## 🧠 API Documentation

- **Swagger UI:** http://127.0.0.1:8010/api/docs/ powered by drf-spectacular, including JWT cookie auth for live testing.
- **ReDoc:** http://127.0.0.1:8010/api/redoc/ delivers the same OpenAPI schema with human-friendly navigation.
- **Postman Collection:** Import `docs/postman/RevalytIQ.postman_collection.json` to explore endpoints with ready-made examples.

## Screenshots

| View | Preview |
| --- | --- |
| Dashboard | ![Dashboard](docs/screenshots/dashboard.png) |
| Signup Flow | ![Signup](docs/screenshots/signup.png) |
| KPIs | ![KPIs](docs/screenshots/kpis.png) |
| Swagger UI | ![Swagger](docs/screenshots/swagger.png) |
| Postman Collection | ![Postman](docs/screenshots/postman.png) |

> Screenshots live in `docs/screenshots/`. Replace with actual captures as the UI evolves.

## Quick Start

### All-in-one (Docker Compose)

```bash
cp backend/.env.example backend/.env          # optional for local dev
cp frontend/.env.example frontend/.env.local  # optional for local dev
docker compose up -d --build
```

- The Compose stack reads `backend/.env.docker` for container defaults. Edit this
  file (or export environment variables) if you need different values inside Docker.
- Use `backend/.env` only for running Django locally (e.g. with
  `ENVIRONMENT=local` and `DJANGO_SETTINGS_MODULE=revalyt.settings.local`).
- Frontend: http://localhost:3100
- API + docs: http://127.0.0.1:8010
- Healthcheck: http://127.0.0.1:8010/health/

### Backend (Django / DRF)

```bash
cp backend/.env.example backend/.env
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

> Ensure `backend/.env` sets `DJANGO_SETTINGS_MODULE=revalyt.settings.local` and
> includes `STATIC_ROOT=staticfiles` (the directory is created automatically when
> settings load).

### Frontend (Next.js)

```bash
cp frontend/.env.example frontend/.env.local
cd frontend
pnpm install
pnpm dev --port 3100
```

### Using the Makefile

```bash
make be-install
make fe-install
make up
# optional: make celery-worker | make celery-beat
```

## 🧪 Demo / Seed Data

- In demo mode, the Render deployment runs `python manage.py seed_demo --fail-safe` on every boot, ensuring fresh analytics data and a demo login (`demo@revalytiq.com` / `password123`).
- To reseed locally, run `python manage.py seed_demo --fail-safe` after migrations.

## 💓 Healthcheck

The `/health/` endpoint reports JSON status for the PostgreSQL database, Redis cache, and Celery workers, enabling automated uptime probes and observability dashboards.

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Example |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | Django settings module | `revalyt.settings.local` |
| `ENVIRONMENT` | Runtime environment label | `local` |
| `DJANGO_DEBUG` | Toggle Django debug mode | `True` |
| `DJANGO_SECRET_KEY` | Django secret key | `django-insecure-...` |
| `STATIC_ROOT` | Target directory for collected static assets | `staticfiles` |
| `STATIC_URL` | Public URL prefix for static assets | `/static/` |
| `DATABASE_URL` | PostgreSQL connection URL | `postgres://user:pass@localhost:5432/revalyt` |
| `REDIS_URL` | Redis cache URL | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/1` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated origins | `http://localhost:3100` |
| `JWT_ACCESS_LIFETIME` | Minutes | `5` |
| `JWT_REFRESH_LIFETIME` | Days | `7` |
| `TIME_ZONE` | Server timezone | `UTC` |
| `ENABLE_DEMO_SEED` | Auto-seed demo data (demo mode) | `True` |
| `CELERY_TASK_ALWAYS_EAGER` | Run Celery tasks inline | `True` |
| `CELERY_BROKER_URL` | Demo broker override | `memory://` |
| `CELERY_RESULT_BACKEND` | Demo result backend override | `cache+memory://` |

### Local Demo (`demo.env`)

Spin up a free-tier equivalent environment locally:

```bash
cat <<'EOF' > demo.env
DJANGO_SETTINGS_MODULE=revalyt.settings.demo
ENVIRONMENT=demo
ENABLE_DEMO_SEED=True
CELERY_TASK_ALWAYS_EAGER=True
CELERY_BROKER_URL=memory://
CELERY_RESULT_BACKEND=cache+memory://
EOF

cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
env $(cat ../demo.env | xargs) python manage.py seed_demo --fail-safe
env $(cat ../demo.env | xargs) python manage.py runserver 0.0.0.0:8010
```

Frontend (Vercel dev):

```bash
cp frontend/.env.example frontend/.env.local
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8010" >> frontend/.env.local
cd frontend && pnpm dev --port 3100
```

### Frontend (`frontend/.env.local`)

| Variable | Description | Example |
| --- | --- | --- |
| `NEXT_PUBLIC_API_URL` | Base URL of the backend API | `http://127.0.0.1:8010` |
| `NEXT_PUBLIC_APP_NAME` | Application branding | `RevalytIQ` |
| `NEXT_PUBLIC_SENTRY_DSN` | Optional Sentry DSN | *(leave blank or provide DSN)* |

## Testing

- **Backend:** `make be-test` (`pytest --cov --cov-fail-under=70`).
- **Frontend:** `make fe-test` (`pnpm test -- --coverage --runInBand`).
- **Lint & types:** `make be-lint` | `make fe-lint` ensure ruff/black/mypy and ESLint/Prettier stay green.
- Coverage summaries are published from CI artifacts and surfaced via the badge above.

## Docker (Optional)

```bash
make up
# once services are healthy
make down
```

Ensure `.env` files are populated before running Compose.

## ⚙️ Deployment Shortcuts

| Target | Shortcut |
| --- | --- |
| Backend (Render) | [![Deploy to Render](https://render.com/deploy)](https://render.com/deploy) |
| Frontend (Vercel) | [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/import/git) |

## Deployment

- **Backend (Render):** Uses `render.yaml` to provision a Web Service plus managed PostgreSQL and Redis add-ons. Build installs backend requirements and collects static assets. Start command runs `gunicorn revalyt.wsgi:application --bind 0.0.0.0:8000`.
- **Frontend (Vercel):** Deploy with the included `vercel.json`. Configure `NEXT_PUBLIC_API_URL` in project settings (point preview deployments to the Render preview URL if needed).

## Troubleshooting

- **Ports already in use:** update `.env` overrides or stop conflicting services if `3100` / `8010` are occupied.
- **JWT issues:** Ensure system clocks are synced; adjust `JWT_ACCESS_LIFETIME`/`JWT_REFRESH_LIFETIME`.
- **CORS errors:** Double-check `CORS_ALLOWED_ORIGINS` and `NEXT_PUBLIC_API_URL` match the new port mapping.
- **Database connections:** Verify `DATABASE_URL` matches Render/Postgres settings.
- **Celery tasks not running:** Confirm Redis broker is reachable and worker processes are deployed (`make celery-worker`).

## 🛡️ Security & Maintenance

- Automated dependency updates are handled by Dependabot across Python and JavaScript packages.
- CodeQL static analysis runs in CI to flag vulnerabilities before deployment.
- GitHub Actions pipelines cover tests, linting, and deployment checks for the Django backend and Next.js frontend.

## 📜 License

This project is released under the [MIT License](./LICENSE), enabling commercial and open-source use with attribution.

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
