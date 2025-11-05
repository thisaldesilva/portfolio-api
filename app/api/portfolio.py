"""Portfolio API endpoints."""

from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.portfolio import PortfolioReturnResponse
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get(
    "/{customer_id}/returns",
    response_model=PortfolioReturnResponse,
    summary="Calculate portfolio returns",
)
def calculate_portfolio_returns(
    customer_id: UUID,
    start_date: str = Query(
        ...,
        description="Start date in YYYY-MM-DD format",
        regex=r"^\d{4}-\d{2}-\d{2}$",
    ),
    end_date: str = Query(
        ...,
        description="End date in YYYY-MM-DD format",
        regex=r"^\d{4}-\d{2}-\d{2}$",
    ),
    db: Session = Depends(get_db),
):
    """
    Calculate portfolio returns for a customer over a date range.

    - **customer_id**: Customer UUID
    - **start_date**: Start date in YYYY-MM-DD format
    - **end_date**: End date in YYYY-MM-DD format

    Returns total portfolio value change and individual stock performance.

    Example: `/portfolio/{customer_id}/returns?start_date=2024-01-01&end_date=2024-01-31`
    """
    try:
        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start > end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must be before end_date",
            )

        # Calculate returns
        result = PortfolioService.calculate_portfolio_return(
            db, customer_id, start, end
        )
        return result

    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format or data: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating returns: {str(e)}",
        )
