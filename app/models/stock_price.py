"""Stock price model for historical data."""

import uuid
from datetime import date
from sqlalchemy import Column, ForeignKey, Date, Numeric, Index, UniqueConstraint, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class StockPrice(Base, TimestampMixin):
    """Historical stock price data."""

    __tablename__ = "stock_prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stock_ticker = Column(
        String(10), ForeignKey("stocks.ticker", ondelete="CASCADE"), nullable=False
    )
    date = Column(Date, nullable=False, index=True)
    open_price = Column(Numeric(10, 2), nullable=True)
    high_price = Column(Numeric(10, 2), nullable=True)
    low_price = Column(Numeric(10, 2), nullable=True)
    close_price = Column(Numeric(10, 2), nullable=False)
    volume = Column(Numeric(20, 0), nullable=True)

    # Relationships
    stock = relationship("Stock", back_populates="prices")

    __table_args__ = (
        UniqueConstraint("stock_ticker", "date", name="uq_stock_price_date"),
        Index("idx_stock_price_ticker_date", "stock_ticker", "date"),
    )

    def __repr__(self) -> str:
        return f"<StockPrice {self.stock_ticker} {self.date}: ${self.close_price}>"
