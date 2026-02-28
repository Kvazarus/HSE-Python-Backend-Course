PIP := app/venv/bin/pip
PYTHON3 := app/venv/bin/python3
MANAGE := ${PYTHON3} app/manage.py
DC := docker-compose -f storage/docker-compose.yml

.PHONY: clear venv reqs install db-up db-down migrations migrate run

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

db-down:
	${DC} down

migrations:
	${MANAGE} makemigrations

migrate:
	${MANAGE} migrate

run:
	${MANAGE} runserver