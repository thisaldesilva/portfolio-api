"""Portfolio service layer."""

from datetime import datetime, date
from typing import Dict, List
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models import Customer, PortfolioStock
from app.services.stock_service import StockService


class PortfolioService:
    """Service for portfolio operations."""

    @staticmethod
    def calculate_portfolio_return(
        db: Session,
        customer_id: UUID,
        start_date: date,
        end_date: date,
    ) -> Dict:
        """
        Calculate portfolio return for a customer over a date range.

        Args:
            db: Database session
            customer_id: Customer UUID
            start_date: Start date for calculation
            end_date: End date for calculation

        Returns:
            Dictionary with return details
        """
        # Get customer with portfolio
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer or not customer.portfolio:
            raise ValueError("Customer or portfolio not found")

        portfolio_stocks = customer.portfolio.portfolio_stocks

        if not portfolio_stocks:
            return {
                "customer_id": str(customer_id),
                "start_date": str(start_date),
                "end_date": str(end_date),
                "total_return": 0.0,
                "return_percentage": 0.0,
                "holdings": [],
            }

        holdings = []
        total_start_value = Decimal("0")
        total_end_value = Decimal("0")

        for portfolio_stock in portfolio_stocks:
            ticker = portfolio_stock.stock_ticker
            quantity = portfolio_stock.quantity

            # Get stock prices for the date range
            prices = StockService.get_stock_prices(db, ticker, start_date, end_date)

            if not prices:
                # Skip stocks with no price data
                continue

            # Get first and last prices
            start_price = prices[0].close_price
            end_price = prices[-1].close_price

            # Calculate values
            start_value = start_price * Decimal(str(quantity))
            end_value = end_price * Decimal(str(quantity))
            stock_return = end_value - start_value
            stock_return_pct = (
                (float(end_price - start_price) / float(start_price)) * 100
                if start_price > 0
                else 0.0
            )

            holdings.append(
                {
                    "ticker": ticker,
                    "quantity": quantity,
                    "start_price": float(start_price),
                    "end_price": float(end_price),
                    "start_value": float(start_value),
                    "end_value": float(end_value),
                    "return": float(stock_return),
                    "return_percentage": stock_return_pct,
                }
            )

            total_start_value += start_value
            total_end_value += end_value

        # Calculate total return
        total_return = total_end_value - total_start_value
        return_percentage = (
            (float(total_return) / float(total_start_value)) * 100
            if total_start_value > 0
            else 0.0
        )

        return {
            "customer_id": str(customer_id),
            "start_date": str(start_date),
            "end_date": str(end_date),
            "total_return": float(total_return),
            "return_percentage": return_percentage,
            "holdings": holdings,
        }
