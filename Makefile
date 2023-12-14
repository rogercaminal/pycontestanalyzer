APP_DIR ?= /opt/pycontestanalyzer
BUILD_TYPE = docker
DOCKER_OPTS ?=
DOCKER_IMAGE_NAME ?= pycontestanalyzer
DOCKER_IMAGE_NAME_TEST ?= pycontestanalyzer/test
SRC_DIR ?= pycontestanalyzer
TESTS_DIR ?= tests
UID ?= $(shell id -u)

define docker_run_cmd
	$(MAKE) .env
	docker run --rm \
		-v ${PWD}:${APP_DIR}  \
		-w ${APP_DIR} \
		-p 8050:8050 \
		--env-file .env \
		${DOCKER_IMAGE_NAME_TEST}
endef

define docker_run_sh
	$(MAKE) .env
	docker run -it --rm \
		-v ${PWD}:${APP_DIR} \
		-w ${APP_DIR} \
		-p 8050:8050 \
		--env-file .env \
		${DOCKER_IMAGE_NAME_TEST}
endef

.env: ## ensures environment file with secrets exists or create from template.
	@echo "Local .env file not found, creating from .env.example"
	cp .env.example .env

.PHONY: build-test
build-test: ## build image for testing purposes (test suite, linting and format checks)
	docker build \
		--build-arg APP_DIR=${APP_DIR}  \
		--build-arg SRC_DIR=${SRC_DIR} \
		--build-arg UID=${UID} \
		-t ${DOCKER_IMAGE_NAME_TEST} \
		-f Dockerfile \
		$(DOCKER_OPTS) \
		--target test \
		.

.PHONY: build
build: ## build main image used for production.
	docker build \
		--build-arg APP_DIR=${APP_DIR}  \
		--build-arg SRC_DIR=${SRC_DIR} \
		--build-arg UID=${UID} \
		-t ${DOCKER_IMAGE_NAME} \
		-f Dockerfile \
		-p 8050:8050 \
		$(DOCKER_OPTS) \
		--target final \
		.

.PHONY: buildtype
buildtype: ## display build type (currently docker supported)
	@echo $(BUILD_TYPE)

.PHONY: format-check
format-check: build-test ## check formatting and import sorting against diff.
	$(docker_run_cmd) ruff check --diff $(SRC_DIR) $(TESTS_DIR)
	$(docker_run_cmd) black --check --diff $(SRC_DIR) $(TESTS_DIR)

.PHONY: format
format: build-test ## apply formatting and import sorting rules.
	$(docker_run_cmd) ruff check --fix $(SRC_DIR) $(TESTS_DIR)
	$(docker_run_cmd) black $(SRC_DIR) $(TESTS_DIR)

.PHONY: help
help: ## display available recipes with descriptions.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:\n"
	@fgrep "##" Makefile | fgrep -v fgrep | sed 's/\(.*\):.*\(## .*\)/\1 \2/' | column -t -s '##'

.PHONY: install-dev
install-dev: ## install Python dependencies for testing purposes.
	pip install -r requirements_dev.txt

.PHONY: install-precommit-hooks
install-precommit-hooks: ## install precommit hooks (linting and formatting).
	@echo "Installing pre-commit hooks!"
	@echo "Make sure you have pre-commit installed on your system (`brew install pre-commit`)"
	pre-commit install

.PHONY: install
install: ## install Python dependencies for production.
	pip install -r requirements.txt

.PHONY: lint
lint: build-test ## apply linting rules to source code and tests.
	$(docker_run_cmd) pylint $(SRC_DIR)
	$(docker_run_cmd) pylint --disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,too-few-public-methods,redefined-outer-name,unused-argument $(TESTS_DIR)

.PHONY: local-setup
local-setup: .env install install-dev install-precommit-hooks ## install necessary dependencies for locat setup in current environment.
	@echo "Local setup completed!"
	@echo "It is recommended to restart you IDE/Editor."

.PHONY: local-setup-with-venv
local-setup-with-venv: .env install-precommit-hooks ## install necessary dependencies for locat setup in a new virtual environment.
	@echo "creating virtualenv ..."
	@read -p "Python version?: " PYTHONVERSION
	@pyenv global ${PYTHONVERSION}
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@./.venv/bin/pip install -r requirements.txt
	@./.venv/bin/pip install -r requirements_dev.txt
	@echo "Please run 'source .venv/bin/activate' to be able to activate the virtual environment you created for this local setup."


.PHONY: run-all-checks
run-all-checks: build-test format-check lint run-tests ## build test container, run format checks, linting and testing.
	@echo ok

.PHONY: run-sh
run-sh: build-test ## enter an intercative shell session inside test container for debugging.
	$(docker_run_sh) /bin/bash

.PHONY: run-tests
run-tests: build-test ## run test suite on source code and render coverage information.
	$(docker_run_cmd) /bin/bash -c " \
		coverage erase \
		&& coverage run -m pytest --doctest-modules --junitxml=junit/test-results.xml $(TESTS_DIR) \
		&& coverage xml -i"
