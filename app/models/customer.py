"""Customer model."""

import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class Customer(Base, TimestampMixin):
    """Customer entity with portfolio."""

    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    address = Column(String(500), nullable=False)

    # Relationships
    portfolio = relationship(
        "Portfolio",
        back_populates="customer",
        uselist=False,
        cascade="all, delete-orphan",
    )

    @property
    def portfolio_stocks(self):
        """Get portfolio stocks from the customer's portfolio."""
        if self.portfolio:
            return self.portfolio.portfolio_stocks
        return []

    def __repr__(self) -> str:
        return f"<Customer {self.name} ({self.id})>"
