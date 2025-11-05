#!/bin/bash
# Run tests with coverage

set -e

echo "Running tests with coverage..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run linters
echo "Running linters..."
black --check app/ || true
flake8 app/ --max-line-length=100 || true
mypy app/ --ignore-missing-imports || true

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v --cov=app --cov-report=html --cov-report=term

echo ""
echo "Coverage report generated in htmlcov/index.html"
