import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def test_connection():
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            print(result)



def get_all_products():
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name,
                    description,
                    price,
                    stock,
                    category,
                    created_at,
                    updated_at
                FROM products
                ORDER BY id;
            """)

            return cursor.fetchall()


def get_product_by_id(product_id: int):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    price,
                    stock,
                    category,
                    created_at,
                    updated_at
                FROM products
                WHERE id = %s;
                """,
                (product_id,)
            )

            return cursor.fetchone()
def create_product(name: str, price: int, stock: int):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO products (
                    name,
                    price,
                    stock
                )
                VALUES (%s, %s, %s)
                RETURNING
                    id,
                    name,
                    description,
                    price,
                    stock,
                    category,
                    created_at,
                    updated_at;
                """,
                (name, price, stock)
            )

            return cursor.fetchone()
def update_product(product_id: int, name: str, price: int, stock: int):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE products
                SET
                    name = %s,
                    price = %s,
                    stock = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING
                    id,
                    name,
                    description,
                    price,
                    stock,
                    category,
                    created_at,
                    updated_at;
                """,
                (name, price, stock, product_id)
            )

            return cursor.fetchone()

def patch_product(
    product_id: int,
    name: str | None,
    price: int | None,
    stock: int | None
):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE products
                SET
                    name = COALESCE(%s, name),
                    price = COALESCE(%s, price),
                    stock = COALESCE(%s, stock),
                    updated_at = NOW()
                WHERE id = %s
                RETURNING
                    id,
                    name,
                    description,
                    price,
                    stock,
                    category,
                    created_at,
                    updated_at;
                """,
                (name, price, stock, product_id)
            )

            return cursor.fetchone()

if __name__ == "__main__":
    print(
        patch_product(
            product_id=2,
            name=None,
            price=None,
            stock=50
        )
    )
