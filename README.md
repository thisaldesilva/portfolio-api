# Customer Portfolio Management System

A production-grade REST API for managing customer portfolios with real-time stock data integration.

## Architecture

- **Application**: Python FastAPI REST API
- **Database**: AWS RDS (PostgreSQL)
- **Hosting**: AWS EC2
- **Infrastructure**: Terraform
- **Configuration Management**: Ansible
- **CI/CD**: GitHub Actions

## Project Structure

```
.
├── app/                    # Application code
│   ├── api/               # REST API endpoints
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── db/                # Database utilities
│   └── config.py          # Configuration
├── infrastructure/        # Infrastructure as Code
│   ├── terraform/        # AWS infrastructure
│   └── ansible/          # Configuration management
├── .github/              # CI/CD pipelines
│   └── workflows/
├── tests/                # Test suite
├── migrations/           # Database migrations (Alembic)
└── scripts/              # Utility scripts
```

## Features

- Customer CRUD operations with UUID identification
- Portfolio management with multiple stocks
- Real-time stock data from Polygon/Massive API
- Portfolio return calculations for date ranges
- Normalized database schema
- Production-ready infrastructure
- Automated deployment pipeline

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload
```

### Deploy to AWS

```bash
# Provision infrastructure
cd infrastructure/terraform
terraform init
terraform plan
terraform apply

# Deploy application
cd ../ansible
ansible-playbook -i inventory/production deploy.yml
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `POLYGON_API_KEY`: Polygon/Massive API key
- `AWS_REGION`: AWS region for deployment
- `ENVIRONMENT`: dev/staging/production

## License

MIT
