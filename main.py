from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int


products = [
    {
        "id": 1,
        "name": "Mechanical Keyboard",
        "price": 2500,
        "stock": 10
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "price": 1200,
        "stock": 25
    }
]


@app.get("/products")
def get_products():
    return products
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Product not found"}
@app.post("/products")
def create_product(product: ProductCreate):
    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return new_product
