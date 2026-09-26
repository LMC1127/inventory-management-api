from fastapi import FastAPI


app = FastAPI()


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
