# Project Variables
PYTHON_VERSION = 3.9.7
APP_NAME = my_app
DOCKER_COMPOSE_FILE = docker-compose.yml
DOCKER_IMAGE = my_app_image

# Pyenv settings
PYENV_ROOT := $(shell pyenv root)
VENV_PATH = $(PYENV_ROOT)/versions/$(APP_NAME)

# Docker settings
DOCKER_RUN = docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm $(APP_NAME)

# Environment variables
OPENAI_API_KEY ?= $(shell read -p "Enter your OpenAI API key: " key; echo $$key)
STREAMLIT_PORT ?= $(shell read -p "Enter the port for streamlit: " port; echo $$port)

# Help command
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  init             Setup the project using pyenv"
	@echo "  install          Install dependencies using pyenv"
	@echo "  run              Run the application using pyenv"
	@echo "  test             Run tests using pyenv"
	@echo "  docker-build     Build Docker containers"
	@echo "  docker-up        Start Docker containers"
	@echo "  docker-down      Stop Docker containers"
	@echo "  docker-shell     Access the application shell in Docker"
	@echo "  docker-test      Run tests in Docker containers"
	@echo "  clean            Clean up the environment"

# Pyenv targets
.PHONY: init
init:
	@echo "Setting up the project using pyenv..."
	pyenv install -s $(PYTHON_VERSION)
	pyenv virtualenv -f $(PYTHON_VERSION) $(APP_NAME)
	pyenv local $(APP_NAME)
	@echo "Virtual environment created at $(VENV_PATH)"

.PHONY: install
install: init
	@echo "Installing dependencies..."
	pip install -r requirements.txt

.PHONY: run
run: install
	@echo "Running the application..."
	OPENAI_API_KEY=$(OPENAI_API_KEY) python app/main.py

.PHONY: test
test:
	@echo "Running tests..."
	OPENAI_API_KEY=$(OPENAI_API_KEY) pytest tests/

# Docker targets

.PHONY: docker-up
docker-up:
	@echo "Starting Docker containers..."
	OPENAI_API_KEY=$(OPENAI_API_KEY) STREAMLIT_PORT=$(STREAMLIT_PORT) docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

.PHONY: docker-down
docker-down:
	@echo "Stopping Docker containers..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

.PHONY: docker-shell
docker-shell:
	@echo "Accessing the application shell in Docker..."
	OPENAI_API_KEY=$(OPENAI_API_KEY) STREAMLIT_PORT=$(STREAMLIT_PORT) $(DOCKER_RUN) /bin/bash

.PHONY: docker-test
docker-test:
	@echo "Running tests in Docker containers..."
	OPENAI_API_KEY=$(OPENAI_API_KEY) STREAMLIT_PORT=$(STREAMLIT_PORT) $(DOCKER_RUN) pytest tests/

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up the environment..."
	pyenv virtualenv-delete -f $(APP_NAME)
	rm -rf __pycache__ .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
