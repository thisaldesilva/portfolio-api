"""Customer service layer."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload

from app.models import Customer, Portfolio, PortfolioStock
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """Service for customer operations."""

    @staticmethod
    def get_customer(db: Session, customer_id: UUID) -> Optional[Customer]:
        """Get customer by ID with portfolio."""
        return (
            db.query(Customer)
            .options(
                joinedload(Customer.portfolio).joinedload(Portfolio.portfolio_stocks)
            )
            .filter(Customer.id == customer_id)
            .first()
        )

    @staticmethod
    def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers with pagination."""
        return (
            db.query(Customer)
            .options(
                joinedload(Customer.portfolio).joinedload(Portfolio.portfolio_stocks)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
        """Create a new customer with portfolio."""
        # Create customer
        customer = Customer(name=customer_data.name, address=customer_data.address)
        db.add(customer)
        db.flush()  # Get customer ID

        # Create portfolio for customer
        portfolio = Portfolio(customer_id=customer.id)
        db.add(portfolio)
        db.flush()

        # Add stocks to portfolio if provided
        if customer_data.stocks:
            for stock_data in customer_data.stocks:
                portfolio_stock = PortfolioStock(
                    portfolio_id=portfolio.id,
                    stock_ticker=stock_data["ticker"],
                    quantity=stock_data["quantity"],
                )
                db.add(portfolio_stock)

        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def update_customer(
        db: Session, customer_id: UUID, customer_data: CustomerUpdate
    ) -> Optional[Customer]:
        """Update customer information."""
        customer = CustomerService.get_customer(db, customer_id)
        if not customer:
            return None

        # Update basic fields
        if customer_data.name is not None:
            customer.name = customer_data.name
        if customer_data.address is not None:
            customer.address = customer_data.address

        # Update portfolio stocks if provided
        if customer_data.stocks is not None:
            # Clear existing portfolio stocks
            db.query(PortfolioStock).filter(
                PortfolioStock.portfolio_id == customer.portfolio.id
            ).delete()

            # Add new portfolio stocks
            for stock_data in customer_data.stocks:
                portfolio_stock = PortfolioStock(
                    portfolio_id=customer.portfolio.id,
                    stock_ticker=stock_data["ticker"],
                    quantity=stock_data["quantity"],
                )
                db.add(portfolio_stock)

        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def delete_customer(db: Session, customer_id: UUID) -> bool:
        """Delete a customer (cascade deletes portfolio and stocks)."""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return False

        db.delete(customer)
        db.commit()
        return True
