import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from psycopg import sql


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
    updates: dict
):
    allowed_fields = {"name", "price", "stock"}

    invalid_fields = set(updates) - allowed_fields

    if invalid_fields:
        raise ValueError(f"Invalid fields: {invalid_fields}")

    if not updates:
        return get_product_by_id(product_id)

    set_clauses = [
        sql.SQL("{} = %s").format(sql.Identifier(field))
        for field in updates
    ]

    values = list(updates.values())
    values.append(product_id)

    query = sql.SQL("""
        UPDATE products
        SET
            {set_clauses},
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
    """).format(
        set_clauses=sql.SQL(", ").join(set_clauses)
    )

    with psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

            return cursor.fetchone()

def delete_product(product_id: int):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM products
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
                (product_id,)
            )

            return cursor.fetchone()

if __name__ == "__main__":
    print(delete_product(3))