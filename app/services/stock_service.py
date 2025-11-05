"""Stock service layer."""

from datetime import datetime, timedelta, date
from typing import List, Optional
from decimal import Decimal
import httpx
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import Stock, StockPrice
from app.config import get_settings

settings = get_settings()


class StockService:
    """Service for stock operations."""

    FORTUNE_500_TICKERS = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B",
        "UNH", "JNJ", "XOM", "V", "WMT", "JPM", "PG", "MA", "CVX", "HD",
        "MRK", "ABBV", "PEP", "KO", "AVGO", "COST", "MCD", "PFE", "TMO",
        "CSCO", "ACN", "ABT", "LLY", "DHR", "NKE", "NEE", "CRM", "VZ",
        "ADBE", "TXN", "CMCSA", "DIS", "PM", "WFC", "NFLX", "UPS", "BMY",
        "ORCL", "HON", "INTC", "QCOM", "UNP", "LOW", "RTX", "AMGN", "IBM",
        # Add more Fortune 500 stocks as needed
    ]

    @staticmethod
    async def fetch_stock_data_from_polygon(ticker: str, days: int = 14) -> List[dict]:
        """
        Fetch stock data from Polygon/Massive API.

        Args:
            ticker: Stock ticker symbol
            days: Number of days of historical data to fetch

        Returns:
            List of stock price data
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        # Polygon API endpoint for aggregates (bars)
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"

        params = {"apiKey": settings.polygon_api_key, "adjusted": "true", "sort": "asc"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()

            # Polygon API returns "OK" for real-time data or "DELAYED" for delayed data
            # Both are valid responses
            if data.get("status") not in ["OK", "DELAYED"] or not data.get("results"):
                return []

            return data["results"]

    @staticmethod
    async def populate_stock_data(db: Session, ticker: str) -> Stock:
        """
        Fetch and populate stock data from Polygon API.

        Args:
            db: Database session
            ticker: Stock ticker symbol

        Returns:
            Stock object with populated prices
        """
        # Get or create stock
        stock = db.query(Stock).filter(Stock.ticker == ticker).first()
        if not stock:
            stock = Stock(ticker=ticker, name=ticker)  # Name can be updated later
            db.add(stock)
            db.flush()

        # Fetch price data from Polygon
        price_data = await StockService.fetch_stock_data_from_polygon(ticker)

        # Store price data
        for bar in price_data:
            price_date = datetime.fromtimestamp(bar["t"] / 1000).date()

            # Check if price already exists
            existing_price = (
                db.query(StockPrice)
                .filter(
                    and_(
                        StockPrice.stock_ticker == ticker,
                        StockPrice.date == price_date,
                    )
                )
                .first()
            )

            if existing_price:
                # Update existing price
                existing_price.open_price = Decimal(str(bar["o"]))
                existing_price.high_price = Decimal(str(bar["h"]))
                existing_price.low_price = Decimal(str(bar["l"]))
                existing_price.close_price = Decimal(str(bar["c"]))
                existing_price.volume = Decimal(str(bar["v"]))
            else:
                # Create new price record
                stock_price = StockPrice(
                    stock_ticker=ticker,
                    date=price_date,
                    open_price=Decimal(str(bar["o"])),
                    high_price=Decimal(str(bar["h"])),
                    low_price=Decimal(str(bar["l"])),
                    close_price=Decimal(str(bar["c"])),
                    volume=Decimal(str(bar["v"])),
                )
                db.add(stock_price)

        db.commit()
        db.refresh(stock)
        return stock

    @staticmethod
    async def populate_fortune500_stocks(db: Session) -> List[Stock]:
        """Populate data for all Fortune 500 stocks."""
        stocks = []
        for ticker in StockService.FORTUNE_500_TICKERS:
            try:
                stock = await StockService.populate_stock_data(db, ticker)
                stocks.append(stock)
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                continue

        return stocks

    @staticmethod
    def get_stock_prices(
        db: Session, ticker: str, start_date: date, end_date: date
    ) -> List[StockPrice]:
        """Get stock prices for a date range."""
        return (
            db.query(StockPrice)
            .filter(
                and_(
                    StockPrice.stock_ticker == ticker,
                    StockPrice.date >= start_date,
                    StockPrice.date <= end_date,
                )
            )
            .order_by(StockPrice.date)
            .all()
        )
