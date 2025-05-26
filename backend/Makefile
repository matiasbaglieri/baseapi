.PHONY: install start

install:
	python3 -m pip install -r requirements.txt

start:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Please create .env file first."; \
		exit 1; \
	fi
	python3 app.py 