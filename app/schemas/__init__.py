"""Pydantic schemas for request/response validation."""

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerWithPortfolio,
)
from app.schemas.stock import StockCreate, StockResponse, StockPriceResponse
from app.schemas.portfolio import PortfolioStockCreate, PortfolioStockResponse

__all__ = [
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "CustomerWithPortfolio",
    "StockCreate",
    "StockResponse",
    "StockPriceResponse",
    "PortfolioStockCreate",
    "PortfolioStockResponse",
]
