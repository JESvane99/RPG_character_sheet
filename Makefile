.PHONY: help build up down logs shell migrate init-db clean dev prod

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the Docker image
	docker-compose build

up: ## Start the application in production mode
	docker-compose up -d

down: ## Stop the application
	docker-compose down

logs: ## Show application logs
	docker-compose logs -f app

shell: ## Open a shell in the running container
	docker-compose exec app bash

migrate: ## Run database migrations
	docker-compose exec app /docker-entrypoint.sh migrate

init-db: ## Initialize the database
	docker-compose exec app /docker-entrypoint.sh init-db

alembic: ## Run alembic commands (usage: make alembic ARGS="revision --autogenerate -m 'message'")
	docker-compose exec app /docker-entrypoint.sh alembic $(ARGS)

clean: ## Remove containers, networks, and images
	docker-compose down -v --rmi all

dev: ## Start in development mode with code reload
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

dev-build: ## Build and start in development mode
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

prod: ## Start in production mode
	docker-compose up -d

restart: ## Restart the application
	docker-compose restart app

status: ## Show container status
	docker-compose ps
