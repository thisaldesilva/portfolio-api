"""Portfolio model."""

import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class Portfolio(Base, TimestampMixin):
    """Portfolio belonging to a customer."""

    __tablename__ = "portfolios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Relationships
    customer = relationship("Customer", back_populates="portfolio")
    portfolio_stocks = relationship(
        "PortfolioStock", back_populates="portfolio", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Portfolio {self.id} for Customer {self.customer_id}>"
