"""Stock API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.stock import StockResponse
from app.services.stock_service import StockService

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.post(
    "/populate/{ticker}",
    response_model=StockResponse,
    summary="Populate stock data for a ticker",
)
async def populate_stock_data(
    ticker: str,
    db: Session = Depends(get_db),
):
    """
    Fetch and store stock data from Polygon API for a specific ticker.

    - **ticker**: Stock ticker symbol (e.g., AAPL, GOOGL)

    This will fetch the last 14 days of closing prices.
    """
    try:
        stock = await StockService.populate_stock_data(db, ticker.upper())
        return stock
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching stock data: {str(e)}",
        )


@router.post(
    "/populate-fortune500",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Populate Fortune 500 stock data",
)
async def populate_fortune500_stocks(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Fetch and store stock data for Fortune 500 companies.

    This is a long-running operation and runs in the background.
    Returns immediately with status 202 Accepted.
    """

    async def fetch_all_stocks():
        await StockService.populate_fortune500_stocks(db)

    background_tasks.add_task(fetch_all_stocks)

    return {
        "message": "Fortune 500 stock data population started in background",
        "status": "processing",
    }


@router.get(
    "/{ticker}",
    response_model=StockResponse,
    summary="Get stock information",
)
def get_stock(
    ticker: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve stock information by ticker symbol.
    """
    from app.models import Stock

    stock = db.query(Stock).filter(Stock.ticker == ticker.upper()).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {ticker} not found. Use /stocks/populate/{ticker} to add it.",
        )
    return stock
