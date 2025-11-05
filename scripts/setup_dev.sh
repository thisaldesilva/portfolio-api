#!/bin/bash
# Development environment setup script

set -e

echo "Setting up development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
required_version="3.11"

if [[ "$python_version" < "$required_version" ]]; then
    echo "Error: Python $required_version or higher is required"
    exit 1
fi

echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update .env with your configuration"
fi

# Setup database (if using local PostgreSQL)
echo ""
echo "Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your configuration (especially DATABASE_URL and POLYGON_API_KEY)"
echo "2. Start PostgreSQL database"
echo "3. Run migrations: alembic upgrade head"
echo "4. Start the application: uvicorn app.main:app --reload"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
