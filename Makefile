# Makefile for Optimization Algorithms Project
# This Makefile provides commands for common tasks like installation,
# testing, running examples, and code quality checks.

.PHONY: install dev-install test test-coverage run-examples run-knapsack run-tsp run-compare lint format clean docs help

# Python interpreter
PYTHON = python

# Directories
SRC_DIR = src
EXAMPLES_DIR = examples
DATA_DIR = data
RESULTS_DIR = $(DATA_DIR)/results

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Optimization Algorithms Project"
	@echo "==============================="
	@echo "Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install        Install the package and dependencies"
	@echo "  make dev-install    Install in development mode with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run tests"
	@echo "  make test-coverage  Run tests with coverage report"
	@echo ""
	@echo "Examples:"
	@echo "  make run-examples   Run all examples"
	@echo "  make run-knapsack   Run knapsack example"
	@echo "  make run-tsp        Run TSP example"
	@echo "  make run-compare    Run algorithm comparison"
	@echo ""
	@echo "Code quality:"
	@echo "  make lint           Run linters (flake8, pylint)"
	@echo "  make format         Format code (black, isort)"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs           Generate documentation"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove build artifacts and temporary files"

# Installation targets
install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install .

dev-install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install pytest pytest-cov flake8 pylint black isort sphinx

# Testing targets
test:
	$(PYTHON) -m pytest

test-coverage:
	$(PYTHON) -m pytest --cov=$(SRC_DIR) --cov-report=term --cov-report=html

# Example targets
$(RESULTS_DIR):
	mkdir -p $(RESULTS_DIR)

run-examples: $(RESULTS_DIR) run-knapsack run-tsp run-compare

run-knapsack: $(RESULTS_DIR)
	$(PYTHON) $(EXAMPLES_DIR)/example_knapsack.py

run-tsp: $(RESULTS_DIR)
	$(PYTHON) $(EXAMPLES_DIR)/example_tsp.py

run-compare: $(RESULTS_DIR)
	$(PYTHON) $(EXAMPLES_DIR)/compare_all.py

# Code quality targets
lint:
	$(PYTHON) -m flake8 $(SRC_DIR) $(EXAMPLES_DIR)
	$(PYTHON) -m pylint $(SRC_DIR) $(EXAMPLES_DIR)

format:
	$(PYTHON) -m black $(SRC_DIR) $(EXAMPLES_DIR)
	$(PYTHON) -m isort $(SRC_DIR) $(EXAMPLES_DIR)

# Documentation targets
docs:
	$(PYTHON) -m sphinx.cmd.quickstart -q -p "Optimization Algorithms" -a "Author" -v "0.1" docs
	$(PYTHON) -m sphinx.cmd.build -b html docs docs/_build

# Cleanup target
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf docs/_build/
