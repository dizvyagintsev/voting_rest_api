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

# Run pytest
test:
	pytest

# Run linter
lint:
	ruff check

# Run formatter
format:
	ruff check --select I --fix
	ruff format