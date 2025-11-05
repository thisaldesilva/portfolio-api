# API Documentation

## Base URL

- **Local Development**: `http://localhost:8000`
- **Production**: `http://YOUR_EC2_IP:8000`

## Interactive Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Authentication

Currently, the API does not require authentication. For production use, implement JWT or API key authentication.

## Endpoints

### Health Check

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### Customers

#### POST /api/v1/customers/

Create a new customer with optional initial portfolio.

**Request Body:**
```json
{
  "name": "John Doe",
  "address": "123 Main St, New York, NY 10001",
  "stocks": [
    {
      "ticker": "AAPL",
      "quantity": 10
    },
    {
      "ticker": "GOOGL",
      "quantity": 5
    }
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "address": "123 Main St, New York, NY 10001",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "portfolio_stocks": [...]
}
```

#### GET /api/v1/customers/{customer_id}

Retrieve a customer by UUID.

**Response:** `200 OK`

#### GET /api/v1/customers/

List all customers with pagination.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

#### PUT /api/v1/customers/{customer_id}

Update customer information and/or portfolio.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "address": "456 Oak Ave, Boston, MA 02101",
  "stocks": [
    {
      "ticker": "MSFT",
      "quantity": 15
    }
  ]
}
```

#### DELETE /api/v1/customers/{customer_id}

Delete a customer (cascade deletes portfolio).

**Response:** `204 No Content`

### Stocks

#### POST /api/v1/stocks/populate/{ticker}

Fetch and store stock data from Polygon API.

**Parameters:**
- `ticker`: Stock ticker symbol (e.g., AAPL, GOOGL)

**Response:** `200 OK`

#### POST /api/v1/stocks/populate-fortune500

Fetch and store data for all Fortune 500 stocks (background job).

**Response:** `202 Accepted`

#### GET /api/v1/stocks/{ticker}

Get stock information by ticker.

### Portfolio

#### GET /api/v1/portfolio/{customer_id}/returns

Calculate portfolio returns over a date range.

**Query Parameters:**
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

**Example:**
```
GET /api/v1/portfolio/550e8400-e29b-41d4-a716-446655440000/returns?start_date=2024-01-01&end_date=2024-01-31
```

**Response:** `200 OK`
```json
{
  "customer_id": "550e8400-e29b-41d4-a716-446655440000",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "total_return": 1250.50,
  "return_percentage": 8.5,
  "holdings": [
    {
      "ticker": "AAPL",
      "quantity": 10,
      "start_price": 150.00,
      "end_price": 165.00,
      "start_value": 1500.00,
      "end_value": 1650.00,
      "return": 150.00,
      "return_percentage": 10.0
    }
  ]
}
```

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```
