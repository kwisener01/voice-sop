.PHONY: help install setup run docker-up docker-down test clean

help:
	@echo "Voice SOP Generator - Available Commands"
	@echo "========================================="
	@echo "install      - Install dependencies"
	@echo "setup        - Run initial setup"
	@echo "run          - Run the application locally"
	@echo "docker-up    - Start Docker containers"
	@echo "docker-down  - Stop Docker containers"
	@echo "test         - Run tests"
	@echo "clean        - Clean temporary files"

install:
	pip install -r requirements.txt

setup:
	python setup.py

run:
	python app.py

celery:
	celery -A celery_tasks worker --loglevel=info

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

test:
	pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
