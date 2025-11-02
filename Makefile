.PHONY: be-install be-run be-test be-lint fe-install fe-dev fe-build fe-test up down

be-install:
	@python -m pip install --upgrade pip
	@pip install -r backend/requirements.txt

be-run:
	cd backend && python manage.py runserver

be-test:
	cd backend && pytest -q --disable-warnings

be-lint:
	@command -v black >/dev/null 2>&1 && black backend || echo "black not installed"
	@command -v isort >/dev/null 2>&1 && isort backend || echo "isort not installed"
	@command -v flake8 >/dev/null 2>&1 && flake8 backend || echo "flake8 not installed"

fe-install:
	cd frontend && pnpm install

fe-dev:
	cd frontend && pnpm dev

fe-build:
	cd frontend && pnpm build

fe-test:
	cd frontend && pnpm test -- --watch=false

up:
	docker-compose up -d

down:
	docker-compose down
