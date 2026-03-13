PIP := app/venv/bin/pip
PYTHON3 := app/venv/bin/python3
MANAGE := ${PYTHON3} app/manage.py
DC := docker-compose -f storage/docker-compose.yml

.PHONY: clear venv reqs install db-up db-down db-down-hard migrations migrate run superuser test docker-up docker-down

clear:
	rm -rf app/venv

venv:
	python3 -m venv app/venv

install:
	${PIP} install -r app/requirements.txt

reqs:
	${PIP} freeze > app/requirements.txt

db-up:
	${DC} up -d --build

superuser:
	${MANAGE} createsuperuser

db-down:
	${DC} down

db-down-hard:
	${DC} down -v

migrations:
	${MANAGE} makemigrations

migrate:
	${MANAGE} migrate

run:
	${MANAGE} runserver

test:
	${MANAGE} test blogs

# Запустить весь проект целиком в Docker (база + бэкенд)
docker-up:
	docker-compose up -d --build

# Остановить весь проект
docker-down:
	docker-compose down

# Создать суперюзера в докере
docker-superuser:
	docker-compose exec web python manage.py createsuperuser