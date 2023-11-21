##
# Project Title
#
# @file
# @version 0.1

build:
	docker-compose build

up:
	docker-compose up -d

static:
	docker-compose run web python manage.py collectstatic --no-input

migrate:
	docker-compose run web python manage.py migrate

down:
	docker-compose down

farmeris: down static up

farmeris_full: build migrate down static up

# end
