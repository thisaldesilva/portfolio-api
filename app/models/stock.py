"""Stock model."""

from sqlalchemy import Column, String, Index
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class Stock(Base, TimestampMixin):
    """Stock entity with ticker symbol."""

    __tablename__ = "stocks"

    ticker = Column(String(10), primary_key=True)  # e.g., AAPL, GOOGL
    name = Column(String(255), nullable=False)
    exchange = Column(String(50), nullable=True)

    # Relationships
    portfolio_stocks = relationship("PortfolioStock", back_populates="stock")
    prices = relationship("StockPrice", back_populates="stock", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_stock_ticker", "ticker"),
    )

    def __repr__(self) -> str:
        return f"<Stock {self.ticker} - {self.name}>"
