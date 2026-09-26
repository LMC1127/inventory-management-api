from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int

class ProductUpdate(BaseModel):
    name: str
    price: int
    stock: int

class ProductPatch(BaseModel):
    name: str | None = None
    price: int | None = None
    stock: int | None = None

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
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    for index, existing_product in enumerate(products):
        if existing_product["id"] == product_id:
            updated_product = {
                "id": product_id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }

            products[index] = updated_product

            return updated_product

    return {"message": "Product not found"}
@app.patch("/products/{product_id}")
def patch_product(product_id: int, product: ProductPatch):
    for existing_product in products:
        if existing_product["id"] == product_id:
            if product.name is not None:
                existing_product["name"] = product.name

            if product.price is not None:
                existing_product["price"] = product.price

            if product.stock is not None:
                existing_product["stock"] = product.stock

            return existing_product

    return {"message": "Product not found"}
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, existing_product in enumerate(products):
        if existing_product["id"] == product_id:
            deleted_product = products.pop(index)
            return deleted_product

    return {"message": "Product not found"}
