# Getting Started

Welcome to the Customer Portfolio Management System! This guide will help you get started with the application.

## Quick Start (Local Development)

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd REST
```

2. Run the setup script:
```bash
./scripts/setup_dev.sh
```

3. Configure your environment:
```bash
# Edit .env file with your settings
nano .env
```

Required environment variables:
- `DATABASE_URL`: Your PostgreSQL connection string
- `POLYGON_API_KEY`: Your Polygon/Massive API key

4. Set up the database:
```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
alembic upgrade head
```

5. Start the application:
```bash
uvicorn app.main:app --reload
```

6. Access the API:
- Application: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Quick Start (Production Deployment)

### Prerequisites

- AWS Account with appropriate permissions
- Terraform (>= 1.0)
- Ansible
- SSH key pair for EC2

### Deployment Steps

1. **Configure AWS credentials:**
```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"
```

2. **Provision infrastructure:**
```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
terraform init
terraform plan
terraform apply
```

3. **Deploy application:**
```bash
cd ../ansible
cp inventory/production/hosts.example inventory/production/hosts
# Edit hosts file with EC2 IP and DB endpoint from Terraform
ansible-playbook -i inventory/production/hosts deploy.yml
```

4. **Access your application:**
- API: http://YOUR_EC2_IP:8000
- Documentation: http://YOUR_EC2_IP:8000/docs

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## API Usage Examples

### Create a Customer

```bash
curl -X POST http://localhost:8000/api/v1/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "address": "123 Main St, New York, NY 10001",
    "stocks": [
      {"ticker": "AAPL", "quantity": 10},
      {"ticker": "GOOGL", "quantity": 5}
    ]
  }'
```

### Get Customer Details

```bash
curl http://localhost:8000/api/v1/customers/{customer_id}
```

### Update Customer

```bash
curl -X PUT http://localhost:8000/api/v1/customers/{customer_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "address": "456 Oak Ave, Boston, MA 02101"
  }'
```

### Delete Customer

```bash
curl -X DELETE http://localhost:8000/api/v1/customers/{customer_id}
```

### Populate Stock Data

```bash
# Populate specific stock
curl -X POST http://localhost:8000/api/v1/stocks/populate/AAPL

# Populate Fortune 500 stocks (background job)
curl -X POST http://localhost:8000/api/v1/stocks/populate-fortune500
```

### Calculate Portfolio Returns

```bash
curl "http://localhost:8000/api/v1/portfolio/{customer_id}/returns?start_date=2024-01-01&end_date=2024-01-31"
```

## Project Structure

```
REST/
├── app/                      # Application code
│   ├── api/                 # REST endpoints
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── db/                  # Database utilities
│   ├── config.py            # Configuration
│   └── main.py              # FastAPI app
├── infrastructure/           # Infrastructure as Code
│   ├── terraform/           # AWS infrastructure
│   └── ansible/             # Configuration management
├── tests/                   # Test suite
├── docs/                    # Documentation
├── migrations/              # Database migrations
└── scripts/                 # Utility scripts
```

## Running Tests

```bash
# Run all tests with coverage
./scripts/run_tests.sh

# Run specific test file
pytest tests/test_customers.py -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

## Documentation

- [API Documentation](docs/API.md) - Detailed API reference
- [Database Schema](docs/DATABASE.md) - Database design and relationships
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [Architecture](docs/ARCHITECTURE.md) - System architecture overview

## Troubleshooting

### Database connection issues

Verify your DATABASE_URL is correct:
```bash
echo $DATABASE_URL
psql $DATABASE_URL -c "SELECT 1"
```

### Import errors

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### Migration issues

Reset database (CAUTION: This will delete all data):
```bash
alembic downgrade base
alembic upgrade head
```

## Next Steps

1. **Populate stock data:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/stocks/populate-fortune500
   ```

2. **Create your first customer:**
   Use the API documentation at `/docs` to create customers interactively

3. **Calculate portfolio returns:**
   Query portfolio performance over time

4. **Set up CI/CD:**
   Configure GitHub Actions for automated deployment

## Getting Help

- Check the [API Documentation](http://localhost:8000/docs) for endpoint details
- Review [docs/](docs/) for comprehensive guides
- Check application logs for errors
- Review the test suite for usage examples

## Contributing

When making changes:

1. Create a feature branch
2. Write tests for new features
3. Run linters: `black app/` and `flake8 app/`
4. Run test suite: `./scripts/run_tests.sh`
5. Update documentation as needed
6. Create a pull request

## License

MIT License - See LICENSE file for details
