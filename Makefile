# Project Title
# @file Makefile
# @version 0.1

# Common commands for both environments
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

# Development-specific commands
static-dev:
	docker-compose run web python manage.py collectstatic --no-input

migrate-dev:
	docker-compose run web python manage.py migrate
	docker-compose run web python manage.py makemigrations

# Production-specific commands using docker-compose.prod.yml
static-prod:
	docker-compose -f docker-compose.prod.yml run web python manage.py collectstatic --no-input

migrate-prod:
	docker-compose -f docker-compose.prod.yml run web python manage.py migrate

# Development environment targets
farmeris: down static-dev up

farmeris-full: build migrate-dev down static-dev up

# Production environment targets
farmeris-prod: down static-prod up

farmeris-full-prod:
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml run web python manage.py migrate
	docker-compose -f docker-compose.prod.yml run web python manage.py collectstatic --no-input
	docker-compose -f docker-compose.prod.yml up -d

# end
