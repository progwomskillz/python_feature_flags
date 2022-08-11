down:
	docker-compose down

build:
	docker-compose build

up: build
	docker-compose up -d

unit_tests: up
	docker-compose exec -T $(APP_NAME) pytest -s ./tests/unit/

integration_tests: up
	docker-compose exec -T $(APP_NAME) pytest -s ./tests/integration/

tests: up
	docker-compose exec -T $(APP_NAME) pytest -s ./tests/
