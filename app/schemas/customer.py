"""Customer schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.portfolio import PortfolioStockResponse


class CustomerBase(BaseModel):
    """Base customer schema."""

    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    address: str = Field(
        ..., min_length=1, max_length=500, description="Customer address"
    )


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""

    stocks: Optional[List[dict]] = Field(
        default=None,
        description="Initial stocks for portfolio. Format: [{'ticker': 'AAPL', 'quantity': 10}]",
    )


class CustomerUpdate(BaseModel):
    """Schema for updating customer (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    stocks: Optional[List[dict]] = Field(
        None,
        description="Update portfolio stocks. Format: [{'ticker': 'AAPL', 'quantity': 10}]",
    )


class CustomerResponse(CustomerBase):
    """Schema for customer response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerWithPortfolio(CustomerResponse):
    """Schema for customer with portfolio details."""

    portfolio_stocks: List[PortfolioStockResponse] = []

    model_config = ConfigDict(from_attributes=True)
