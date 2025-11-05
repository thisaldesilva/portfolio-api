"""Portfolio schemas."""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PortfolioStockCreate(BaseModel):
    """Schema for adding stock to portfolio."""

    ticker: str = Field(..., min_length=1, max_length=10)
    quantity: int = Field(..., gt=0, description="Number of shares")


class PortfolioStockResponse(BaseModel):
    """Schema for portfolio stock response."""

    stock_ticker: str
    quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioReturnRequest(BaseModel):
    """Schema for portfolio return calculation request."""

    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="End date (YYYY-MM-DD)")


class PortfolioReturnResponse(BaseModel):
    """Schema for portfolio return calculation response."""

    customer_id: str
    start_date: str
    end_date: str
    total_return: float = Field(..., description="Total portfolio return in dollars")
    return_percentage: float = Field(..., description="Return as percentage")
    holdings: list[dict] = Field(..., description="Individual stock returns")
