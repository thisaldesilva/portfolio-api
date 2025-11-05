# Architecture Overview

## System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   GitHub    │────────▶│GitHub Actions│────────▶│   AWS EC2   │
│ Repository  │         │   CI/CD      │         │ Application │
└─────────────┘         └──────────────┘         └──────┬──────┘
                                                          │
                                                          │
                        ┌─────────────────────────────────┼──────────┐
                        │                                 │          │
                        ▼                                 ▼          ▼
                ┌───────────────┐              ┌─────────────┐  ┌────────┐
                │   AWS RDS     │              │  Polygon    │  │ Users  │
                │  PostgreSQL   │              │     API     │  │        │
                └───────────────┘              └─────────────┘  └────────┘
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15 (AWS RDS)
- **API Client**: httpx (async)
- **Validation**: Pydantic v2

### Infrastructure
- **Cloud Provider**: AWS
- **IaC**: Terraform
- **Configuration Management**: Ansible
- **CI/CD**: GitHub Actions

### Deployment
- **Application Server**: EC2 (Amazon Linux 2023)
- **Database**: RDS PostgreSQL (Multi-AZ for production)
- **Networking**: VPC with public/private subnets
- **Security**: Security Groups, IAM roles

## Application Layers

### 1. API Layer (`app/api/`)
- REST endpoints
- Request/response handling
- Input validation
- Error handling

### 2. Service Layer (`app/services/`)
- Business logic
- Data orchestration
- External API integration (Polygon)
- Portfolio calculations

### 3. Data Layer (`app/models/`)
- SQLAlchemy models
- Database schema
- Relationships
- Constraints

### 4. Schema Layer (`app/schemas/`)
- Pydantic models
- Request validation
- Response serialization
- Type safety

## Key Design Patterns

### 1. Dependency Injection
FastAPI's dependency injection system manages database sessions:

```python
@router.get("/customers/{id}")
def get_customer(id: UUID, db: Session = Depends(get_db)):
    # db session automatically managed
```

### 2. Repository Pattern
Services encapsulate data access logic:

```python
CustomerService.get_customer(db, customer_id)
```

### 3. Normalized Database Schema
Third Normal Form (3NF) ensures data integrity and reduces redundancy.

### 4. Async/Await
Non-blocking I/O for external API calls:

```python
async def fetch_stock_data(ticker: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

## Security Considerations

### Network Security
- VPC with isolated subnets
- Security groups with minimal permissions
- RDS in private subnet (not publicly accessible)
- EC2 in public subnet with restricted SSH access

### Application Security
- Environment variables for secrets
- HTTPS for production (add ALB/CloudFront)
- SQL injection prevention via ORM
- Input validation with Pydantic

### Database Security
- Encrypted storage (RDS encryption)
- Encrypted connections (SSL/TLS)
- Regular automated backups
- Point-in-time recovery enabled

## Scalability

### Horizontal Scaling
- EC2 Auto Scaling Group (future enhancement)
- Application Load Balancer (future enhancement)
- Multiple application instances

### Vertical Scaling
- Adjustable EC2 instance types
- RDS instance class upgrades
- Read replicas for database (future enhancement)

### Caching
- Future enhancement: Redis/ElastiCache
- Cache stock price data
- Cache portfolio calculations

## Monitoring & Observability

### Metrics
- Prometheus metrics endpoint (`/metrics`)
- Application performance metrics
- Database connection pool metrics

### Logging
- Structured JSON logging
- CloudWatch Logs integration
- Application and error logs

### Health Checks
- Health endpoint (`/health`)
- Database connectivity check
- Dependency health validation

## Data Flow

### Customer Creation
```
Client Request
    ↓
API Endpoint (validation)
    ↓
Customer Service (business logic)
    ↓
Database (persistence)
    ↓
Response (serialization)
    ↓
Client
```

### Portfolio Return Calculation
```
Client Request (customer_id, date range)
    ↓
API Endpoint (validation)
    ↓
Portfolio Service
    ├─→ Get customer portfolio from DB
    ├─→ Get stock prices for date range
    ├─→ Calculate returns for each stock
    └─→ Aggregate total returns
    ↓
Response (return data)
    ↓
Client
```

### Stock Data Population
```
API Request (trigger)
    ↓
Stock Service
    ├─→ Polygon API (fetch data)
    ├─→ Transform data
    └─→ Store in database
    ↓
Background processing
    ↓
Response (202 Accepted)
```

## CI/CD Pipeline

### Continuous Integration
1. Code push to GitHub
2. GitHub Actions triggered
3. Linting (black, flake8, mypy)
4. Unit tests with coverage
5. Integration tests

### Continuous Deployment
1. Merge to main branch
2. Terraform validates infrastructure
3. Terraform applies changes (if needed)
4. Ansible deploys application
5. Database migrations run
6. Application restart
7. Health check validation

## Future Enhancements

### Performance
- [ ] Add Redis caching layer
- [ ] Implement database read replicas
- [ ] Add CDN for static assets

### Scalability
- [ ] Auto Scaling Groups
- [ ] Application Load Balancer
- [ ] Container orchestration (ECS/EKS)

### Features
- [ ] User authentication & authorization
- [ ] Real-time portfolio updates (WebSockets)
- [ ] Historical portfolio performance charts
- [ ] Email notifications for price alerts
- [ ] Multi-currency support

### Observability
- [ ] Distributed tracing (AWS X-Ray)
- [ ] Application Performance Monitoring (APM)
- [ ] Custom CloudWatch dashboards
- [ ] Alerting and notifications

### Security
- [ ] WAF (Web Application Firewall)
- [ ] API rate limiting
- [ ] JWT authentication
- [ ] Role-based access control (RBAC)
- [ ] Secrets management (AWS Secrets Manager)
