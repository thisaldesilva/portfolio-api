"""Portfolio-Stock association model (many-to-many with quantity)."""

import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class PortfolioStock(Base, TimestampMixin):
    """Association table linking portfolios to stocks with quantity."""

    __tablename__ = "portfolio_stocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
    )
    stock_ticker = Column(
        String(10), ForeignKey("stocks.ticker", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, nullable=False, default=0)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="portfolio_stocks")
    stock = relationship("Stock", back_populates="portfolio_stocks")

    __table_args__ = (
        UniqueConstraint("portfolio_id", "stock_ticker", name="uq_portfolio_stock"),
    )

    def __repr__(self) -> str:
        return f"<PortfolioStock {self.portfolio_id} - {self.stock_ticker} x{self.quantity}>"
