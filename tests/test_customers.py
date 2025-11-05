"""Tests for customer API endpoints."""

import pytest
from uuid import UUID


def test_create_customer(client, sample_customer_data):
    """Test creating a new customer."""
    response = client.post("/api/v1/customers/", json=sample_customer_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == sample_customer_data["name"]
    assert data["address"] == sample_customer_data["address"]
    assert "id" in data
    assert UUID(data["id"])  # Verify it's a valid UUID


def test_get_customer(client, sample_customer_data):
    """Test retrieving a customer by ID."""
    # Create customer
    create_response = client.post("/api/v1/customers/", json=sample_customer_data)
    customer_id = create_response.json()["id"]

    # Get customer
    response = client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == sample_customer_data["name"]


def test_get_nonexistent_customer(client):
    """Test retrieving a non-existent customer."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/customers/{fake_id}")
    assert response.status_code == 404


def test_list_customers(client, sample_customer_data):
    """Test listing all customers."""
    # Create multiple customers
    client.post("/api/v1/customers/", json=sample_customer_data)
    client.post("/api/v1/customers/", json={**sample_customer_data, "name": "Jane Doe"})

    # List customers
    response = client.get("/api/v1/customers/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 2


def test_update_customer(client, sample_customer_data):
    """Test updating customer information."""
    # Create customer
    create_response = client.post("/api/v1/customers/", json=sample_customer_data)
    customer_id = create_response.json()["id"]

    # Update customer
    update_data = {"name": "John Smith", "address": "456 Oak Ave, Boston, MA 02101"}
    response = client.put(f"/api/v1/customers/{customer_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["address"] == update_data["address"]


def test_delete_customer(client, sample_customer_data):
    """Test deleting a customer."""
    # Create customer
    create_response = client.post("/api/v1/customers/", json=sample_customer_data)
    customer_id = create_response.json()["id"]

    # Delete customer
    response = client.delete(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/api/v1/customers/{customer_id}")
    assert get_response.status_code == 404


def test_update_customer_portfolio(client, sample_customer_data):
    """Test updating customer portfolio."""
    # Create customer
    create_response = client.post("/api/v1/customers/", json=sample_customer_data)
    customer_id = create_response.json()["id"]

    # Update portfolio
    update_data = {"stocks": [{"ticker": "MSFT", "quantity": 15}]}
    response = client.put(f"/api/v1/customers/{customer_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert len(data["portfolio_stocks"]) == 1
    assert data["portfolio_stocks"][0]["stock_ticker"] == "MSFT"
    assert data["portfolio_stocks"][0]["quantity"] == 15
