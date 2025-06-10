.PHONY: venv install start alembic alembic-revision alembic-upgrade alembic-downgrade celery-worker clean-install docker-up docker-down docker-build docker-console-app docker-console-mysql docker-console-redis docker-console-celery docker-console-flower

venv:
	python3.11 -m venv env

clean-install: venv
	. env/bin/activate && \
	python3.11 -m pip install --upgrade pip && \
	pip install setuptools wheel && \
	pip uninstall -y bcrypt passlib && \
	pip install -r requirements.txt

install: clean-install

start:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create .env file first."; \
		exit 1; \
	fi
	. env/bin/activate && python3.11 app.py

alembic:
	. env/bin/activate && alembic init alembic

alembic-revision:
	. env/bin/activate && alembic revision --autogenerate -m "Add new table"

alembic-upgrade:
	. env/bin/activate && alembic upgrade head

alembic-downgrade:
	. env/bin/activate && alembic downgrade -1

mariadb-stop:
	sudo port unload mariadb-10.3-server
mariadb-start:
	sudo port load mariadb-10.3-server
# Docker commands
docker-build:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create .env file first."; \
		exit 1; \
	fi
	DOCKER_BUILDKIT=0 COMPOSE_HTTP_TIMEOUT=300 docker compose build

docker-up:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create .env file first."; \
		exit 1; \
	fi
	COMPOSE_HTTP_TIMEOUT=300 docker compose up -d

docker-down:
	COMPOSE_HTTP_TIMEOUT=300 docker compose down

# Docker console commands
docker-console-app:
	docker compose exec baseapi bash

# Combined commands
docker-start: docker-build docker-up
docker-restart: docker-down docker-up

celery-worker:
	celery -A core.celery_app worker --loglevel=info 