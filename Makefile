# Start the containers and apply migrations
up:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	docker-compose up -d

# Stop and remove containers
down:
	docker-compose down

# Rebuild the Docker containers
build:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	docker-compose build

# Run only the migrations without bringing up/down the containers
migrate:
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

# Access the shell inside the web container
bash:
	docker-compose exec web bash

# Install dependencies
install:
	poetry install

# Run pytest
test:
	poetry run pytest -v

# Run linter
lint:
	poetry run ruff check

# Run formatter
format:
	poetry run ruff check --select I --fix
	poetry run ruff format

# Run mypy
mypy:
	poetry run mypy .
