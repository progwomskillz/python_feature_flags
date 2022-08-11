include ./.env

down:
	docker compose down

build:
	docker compose build

up: build
	docker compose up -d

unit_tests: up
	docker exec -it $(APP_NAME) pytest -s --cov-report term-missing --cov=. ./tests/unit/

integration_tests: up
	docker exec -it $(APP_NAME) pytest -s --cov-report term-missing --cov=. ./tests/integration/

tests: up
	docker exec -it $(APP_NAME) pytest -s --cov-report term-missing --cov=. ./tests/
