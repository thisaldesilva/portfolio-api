# Database Schema

## Overview

The database uses PostgreSQL with a normalized schema to efficiently store customer, portfolio, and stock data.

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────┐       ┌──────────────────┐       ┌────────┐
│  Customer   │──1:1──│  Portfolio   │──M:N──│ Portfolio_Stock  │──M:1──│ Stock  │
└─────────────┘       └──────────────┘       └──────────────────┘       └────────┘
                                                                              │
                                                                             1:M
                                                                              │
                                                                         ┌────────────┐
                                                                         │StockPrice  │
                                                                         └────────────┘
```

## Tables

### customers

Stores customer information.

| Column     | Type      | Constraints                 | Description          |
|------------|-----------|-----------------------------|----------------------|
| id         | UUID      | PRIMARY KEY, DEFAULT uuid() | Customer unique ID   |
| name       | VARCHAR(255) | NOT NULL              | Customer name        |
| address    | VARCHAR(500) | NOT NULL              | Customer address     |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now()     | Creation timestamp   |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now()     | Last update timestamp|

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `name`

### portfolios

Stores portfolios (one per customer).

| Column      | Type | Constraints                         | Description           |
|-------------|------|-------------------------------------|-----------------------|
| id          | UUID | PRIMARY KEY, DEFAULT uuid()         | Portfolio unique ID   |
| customer_id | UUID | FOREIGN KEY → customers.id, UNIQUE  | Customer reference    |
| created_at  | TIMESTAMP | NOT NULL, DEFAULT now()        | Creation timestamp    |
| updated_at  | TIMESTAMP | NOT NULL, DEFAULT now()        | Last update timestamp |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `customer_id`
- FOREIGN KEY on `customer_id` → `customers.id` (CASCADE DELETE)

### stocks

Stores stock information.

| Column     | Type         | Constraints     | Description          |
|------------|--------------|-----------------|----------------------|
| ticker     | VARCHAR(10)  | PRIMARY KEY     | Stock ticker symbol  |
| name       | VARCHAR(255) | NOT NULL        | Company name         |
| exchange   | VARCHAR(50)  | NULL            | Stock exchange       |
| created_at | TIMESTAMP    | NOT NULL        | Creation timestamp   |
| updated_at | TIMESTAMP    | NOT NULL        | Last update timestamp|

**Indexes:**
- PRIMARY KEY on `ticker`

### portfolio_stocks

Junction table linking portfolios to stocks with quantities.

| Column       | Type    | Constraints                          | Description           |
|--------------|---------|--------------------------------------|-----------------------|
| id           | UUID    | PRIMARY KEY, DEFAULT uuid()          | Record unique ID      |
| portfolio_id | UUID    | FOREIGN KEY → portfolios.id          | Portfolio reference   |
| stock_ticker | VARCHAR(10) | FOREIGN KEY → stocks.ticker      | Stock reference       |
| quantity     | INTEGER | NOT NULL, DEFAULT 0                  | Number of shares      |
| created_at   | TIMESTAMP | NOT NULL, DEFAULT now()            | Creation timestamp    |
| updated_at   | TIMESTAMP | NOT NULL, DEFAULT now()            | Last update timestamp |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(portfolio_id, stock_ticker)`
- FOREIGN KEY on `portfolio_id` → `portfolios.id` (CASCADE DELETE)
- FOREIGN KEY on `stock_ticker` → `stocks.ticker` (CASCADE DELETE)

### stock_prices

Stores historical stock price data.

| Column       | Type         | Constraints                      | Description           |
|--------------|--------------|----------------------------------|-----------------------|
| id           | UUID         | PRIMARY KEY, DEFAULT uuid()      | Price record ID       |
| stock_ticker | VARCHAR(10)  | FOREIGN KEY → stocks.ticker      | Stock reference       |
| date         | DATE         | NOT NULL                         | Price date            |
| open_price   | NUMERIC(10,2)| NULL                             | Opening price         |
| high_price   | NUMERIC(10,2)| NULL                             | High price            |
| low_price    | NUMERIC(10,2)| NULL                             | Low price             |
| close_price  | NUMERIC(10,2)| NOT NULL                         | Closing price         |
| volume       | NUMERIC(20,0)| NULL                             | Trading volume        |
| created_at   | TIMESTAMP    | NOT NULL, DEFAULT now()          | Creation timestamp    |
| updated_at   | TIMESTAMP    | NOT NULL, DEFAULT now()          | Last update timestamp |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `(stock_ticker, date)`
- COMPOSITE INDEX on `(stock_ticker, date)` for query optimization
- FOREIGN KEY on `stock_ticker` → `stocks.ticker` (CASCADE DELETE)

## Relationships

1. **Customer ↔ Portfolio**: One-to-One
   - Each customer has exactly one portfolio
   - Deleting a customer cascades to delete their portfolio

2. **Portfolio ↔ Stock**: Many-to-Many (via portfolio_stocks)
   - A portfolio can contain multiple stocks
   - A stock can be in multiple portfolios
   - The junction table stores the quantity for each stock in each portfolio

3. **Stock ↔ StockPrice**: One-to-Many
   - Each stock can have multiple price records (one per day)
   - Deleting a stock cascades to delete all its price records

## Normalization

The schema follows Third Normal Form (3NF):

- **1NF**: All attributes contain atomic values
- **2NF**: No partial dependencies (all non-key attributes depend on the entire primary key)
- **3NF**: No transitive dependencies (all non-key attributes depend only on the primary key)

## Example Queries

### Get customer with portfolio

```sql
SELECT c.*, p.id as portfolio_id
FROM customers c
LEFT JOIN portfolios p ON c.id = p.customer_id
WHERE c.id = 'customer-uuid';
```

### Get portfolio holdings with stock details

```sql
SELECT
    ps.quantity,
    s.ticker,
    s.name,
    ps.created_at
FROM portfolio_stocks ps
JOIN stocks s ON ps.stock_ticker = s.ticker
WHERE ps.portfolio_id = 'portfolio-uuid';
```

### Get stock prices for date range

```sql
SELECT
    date,
    close_price,
    volume
FROM stock_prices
WHERE stock_ticker = 'AAPL'
  AND date BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY date ASC;
```

### Calculate portfolio value on a specific date

```sql
SELECT
    SUM(ps.quantity * sp.close_price) as portfolio_value
FROM portfolio_stocks ps
JOIN stock_prices sp ON ps.stock_ticker = sp.stock_ticker
WHERE ps.portfolio_id = 'portfolio-uuid'
  AND sp.date = '2024-01-31';
```

## Migrations

Database migrations are managed with Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Performance Considerations

1. **Indexes**: Properly indexed on frequently queried columns
2. **Connection Pooling**: Configured for optimal performance
3. **Cascade Deletes**: Automatic cleanup of related records
4. **Composite Indexes**: Optimized for date range queries on stock prices
5. **Numeric Precision**: NUMERIC(10,2) for prices ensures accurate calculations
