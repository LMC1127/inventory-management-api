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


if __name__ == "__main__":
    print(
        create_product(
            name="Wireless Mouse",
            price=1200,
            stock=25
        )
    )
