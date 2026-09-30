import os

from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

from fastapi.testclient import TestClient
from main import app
import pytest
import psycopg

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_products_table():
    with psycopg.connect(os.getenv("DATABASE_URL")) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE products RESTART IDENTITY;"
            )

    yield

    with psycopg.connect(os.getenv("DATABASE_URL")) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE products RESTART IDENTITY;"
            )


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "1.0.0"}    

def test_get_product_invalid_id():
    response = client.get("/products/ff")

    assert response.status_code == 422

def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "price": 1000,
            "stock": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Product"
    assert data["price"] == 1000
    assert data["stock"] == 5

def test_get_all_products():
    # Arrange
    client.post(
        "/products",
        json={
            "name": "Test Product",
            "price": 1000,
            "stock": 5
        }
    )

    # Act
    response = client.get("/products")

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Test Product"
    assert data[0]["price"] == 1000
    assert data[0]["stock"] == 5

def test_get_product_by_id():
    # Arrange
    create_response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "price": 1000,
            "stock": 5
        }
    )

    product_id = create_response.json()["id"]

    # Act
    response = client.get(f"/products/{product_id}")

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Test Product"
    assert data["price"] == 1000
    assert data["stock"] == 5

def test_update_product():
    # Arrange
    create_response = client.post(
        "/products",
        json={
            "name": "Old Product",
            "price": 1000,
            "stock": 5
        }
    )

    product_id = create_response.json()["id"]

    # Act
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Product",
            "price": 1500,
            "stock": 10
        }
    )

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Updated Product"
    assert data["price"] == 1500
    assert data["stock"] == 10

def test_patch_product():
    # Arrange
    create_response = client.post(
        "/products",
        json={
            "name": "Original Product",
            "price": 1000,
            "stock": 5
        }
    )

    product_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/products/{product_id}",
        json={
            "stock": 20
        }
    )

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Original Product"
    assert data["price"] == 1000
    assert data["stock"] == 20

def test_delete_product():
    # Arrange
    create_response = client.post(
        "/products",
        json={
            "name": "Delete Product",
            "price": 1000,
            "stock": 5
        }
    )

    product_id = create_response.json()["id"]

    # Act
    response = client.delete(f"/products/{product_id}")

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Delete Product"

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_get_product_not_found():
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_update_product_not_found():
    response = client.put(
        "/products/999",
        json={
            "name": "Updated Product",
            "price": 1500,
            "stock": 10
        }
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_patch_product_not_found():
    response = client.patch(
        "/products/999",
        json={
            "stock": 20
        }
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_delete_product_not_found():
    response = client.delete("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_create_product_missing_price():
    response = client.post(
        "/products",
        json={
            "name": "Missing Price Product",
            "stock": 5
        }
    )

    assert response.status_code == 422

    get_response = client.get("/products")

    assert get_response.status_code == 200
    assert get_response.json() == []

def test_patch_product_rejects_null():
    # Arrange
    create_response = client.post(
        "/products",
        json={
            "name": "Original Product",
            "price": 1000,
            "stock": 5
        }
    )

    product_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/products/{product_id}",
        json={
            "stock": None
        }
    )

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "stock"]
    assert "Field cannot be null" in data["detail"][0]["msg"]
    get_response = client.get(f"/products/{product_id}")

    data = get_response.json()

    assert data["stock"] == 5