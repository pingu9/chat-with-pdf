# Default target
.DEFAULT_GOAL := up

# Project Variables
DOCKER_COMPOSE_FILE = docker-compose.yml
APP_NAME = my_app
DOCKER_IMAGE = my_app_image


# Environment variables
OPENAI_API_KEY ?= $(shell read -p "Enter your OpenAI API key: " key; echo $$key)
STREAMLIT_PORT ?= $(shell read -p "Enter the port for streamlit: " port; echo $$port)

# Help command
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  make             Build and start Docker containers"
	@echo "  make clean       Stop Docker containers and clean up"
	@echo "  make shell       Access the application shell in Docker"

# Docker targets

.PHONY: make
up:
	@echo "Starting Docker containers..."
	OPENAI_API_KEY=$(OPENAI_API_KEY) STREAMLIT_PORT=$(STREAMLIT_PORT) docker-compose -f $(DOCKER_COMPOSE_FILE) up -d --build

.PHONY: clean
clean:
	@echo "Stopping Docker containers and cleaning up..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) down
	rm -rf __pycache__ .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov

.PHONY: shell
shell:
	@echo "Accessing the application shell in Docker..."
	OPENAI_API_KEY=$(OPENAI_API_KEY) STREAMLIT_PORT=$(STREAMLIT_PORT) docker exec -it streamlit_service /bin/bash