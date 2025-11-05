"""Customer API endpoints."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerWithPortfolio,
)
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "/",
    response_model=CustomerWithPortfolio,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new customer with optional initial portfolio stocks.

    - **name**: Customer name (required)
    - **address**: Customer address (required)
    - **stocks**: Optional list of initial stocks in format [{"ticker": "AAPL", "quantity": 10}]
    """
    try:
        new_customer = CustomerService.create_customer(db, customer)
        return new_customer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating customer: {str(e)}",
        )


@router.get(
    "/{customer_id}",
    response_model=CustomerWithPortfolio,
    summary="Get customer by ID",
)
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve a customer by their UUID along with their portfolio.
    """
    customer = CustomerService.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )
    return customer


@router.get(
    "/",
    response_model=List[CustomerWithPortfolio],
    summary="List all customers",
)
def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retrieve all customers with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    customers = CustomerService.get_customers(db, skip=skip, limit=limit)
    return customers


@router.put(
    "/{customer_id}",
    response_model=CustomerWithPortfolio,
    summary="Update customer",
)
def update_customer(
    customer_id: UUID,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
):
    """
    Update customer information and/or portfolio.

    All fields are optional:
    - **name**: Update customer name
    - **address**: Update customer address
    - **stocks**: Replace portfolio stocks with new list
    """
    updated_customer = CustomerService.update_customer(db, customer_id, customer)
    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )
    return updated_customer


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete customer",
)
def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a customer and their associated portfolio (cascade delete).
    """
    deleted = CustomerService.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found",
        )
    return None
