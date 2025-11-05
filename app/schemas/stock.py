"""Stock schemas."""

from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class StockBase(BaseModel):
    """Base stock schema."""

    ticker: str = Field(
        ..., min_length=1, max_length=10, description="Stock ticker symbol"
    )
    name: str = Field(..., min_length=1, max_length=255, description="Company name")
    exchange: str | None = Field(None, max_length=50, description="Stock exchange")


class StockCreate(StockBase):
    """Schema for creating a stock."""

    pass


class StockResponse(StockBase):
    """Schema for stock response."""

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StockPriceResponse(BaseModel):
    """Schema for stock price response."""

    stock_ticker: str
    date: date
    open_price: Decimal | None
    high_price: Decimal | None
    low_price: Decimal | None
    close_price: Decimal
    volume: Decimal | None

    model_config = ConfigDict(from_attributes=True)
