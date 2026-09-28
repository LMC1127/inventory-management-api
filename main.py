from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import (
    get_all_products,
    get_product_by_id,
    create_product as create_product_in_db,
    update_product as update_product_in_db,
    patch_product as patch_product_in_db,
    delete_product as delete_product_in_db
)


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

@app.get("/products")
def get_products():
    return get_all_products() 


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.post("/products")
def create_product(product: ProductCreate):
    return create_product_in_db(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    updated_product = update_product_in_db(
        product_id=product_id,
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product

@app.patch("/products/{product_id}")
def patch_product(product_id: int, product: ProductPatch):
    updated_product = patch_product_in_db(
        product_id=product_id,
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    deleted_product = delete_product_in_db(product_id)

    if deleted_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return deleted_product
