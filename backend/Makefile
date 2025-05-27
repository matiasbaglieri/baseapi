.PHONY: venv install start run alembic alembic-revision alembic-upgrade alembic-downgrade celery celery-beat

venv:
	python3 -m venv env

install: venv
	. env/bin/activate && \
	python3 -m pip install --upgrade pip && \
	pip3 install setuptools wheel && \
	pip3 install -r requirements.txt && \
	pip3 install alembic python-dotenv passlib[bcrypt] celery redis

start run:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create .env file first."; \
		exit 1; \
	fi
	. env/bin/activate && python3 app.py

alembic:
	. env/bin/activate && alembic init alembic

alembic-revision:
	. env/bin/activate && alembic revision --autogenerate -m "Add new table"

alembic-upgrade:
	. env/bin/activate && alembic upgrade head

alembic-downgrade:
	. env/bin/activate && alembic downgrade -1

celery:
	. env/bin/activate && celery -A core.celery_app worker --loglevel=info

celery-beat:
	. env/bin/activate && celery -A core.celery_app beat --loglevel=info