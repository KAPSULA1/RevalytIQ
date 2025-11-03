 .PHONY: be-install be-run be-test be-lint fe-install fe-dev fe-build fe-test up down celery-worker celery-beat

be-install:
	@python -m pip install --upgrade pip
	@pip install -r backend/requirements.txt

be-run:
	cd backend && python manage.py runserver

be-test:
	cd backend && pytest -q --disable-warnings

be-lint:
	ruff check backend
	black --check backend
	mypy backend

fe-install:
	cd frontend && pnpm install

fe-dev:
	cd frontend && pnpm dev

fe-build:
	cd frontend && pnpm build

fe-test:
	cd frontend && pnpm test

fe-lint:
	cd frontend && pnpm lint
	cd frontend && pnpm format:check

up:
	docker-compose up -d

down:
	docker-compose down

celery-worker:
	cd backend && celery -A revalyt worker -l INFO

celery-beat:
	cd backend && celery -A revalyt beat -l INFO
