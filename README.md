# Inventory Management REST API

A REST API built with FastAPI and PostgreSQL for managing product inventory.

This project demonstrates backend API development, PostgreSQL CRUD operations, request validation, error handling, automated testing, and Git workflow practices.

## Project Status

PostgreSQL CRUD integration completed.

## Features

- Product CRUD operations
  - Create products
  - Retrieve all products
  - Retrieve a product by ID
  - Fully update a product with PUT
  - Partially update a product with PATCH
  - Delete products
- PostgreSQL persistence
- Request validation with Pydantic
- 404 and 422 error handling
- Automated API testing with pytest
- Test database isolation with pytest fixtures

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- psycopg
- Pydantic
- pytest
- Uvicorn
- python-dotenv
- Git

## Project Structure

```text
inventory-management-api/
├── main.py
├── database.py
├── test_main.py
├─.env
├─.env.test
├─.env.example
├─.gitignore
└─README.md

main.py — Defines the FastAPI app, API routes, Pydantic request models, validation rules, and HTTP error handling.
database.py — Handles PostgreSQL connections and product CRUD operations using psycopg.
test_main.py — Contains automated API integration tests using FastAPI TestClient and pytest.
.env — Stores local development environment variables such as the development database URL.
.env.test — Stores test environment variables and points pytest to the isolated test database.
.env.example — Provides an example of the required environment variable format without exposing local secrets.
.gitignore — Excludes virtual environments, environment files, Python cache files, and other local-only files from Git.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check whether the API is running. |
| GET | `/version` | Retrieve the current API version. |
| GET | `/products` | Retrieve all products. |
| GET | `/products/{product_id}` | Retrieve a single product by ID. |
| POST | `/products` | Create a new product. |
| PUT | `/products/{product_id}` | Fully update an existing product. |
| PATCH | `/products/{product_id}` | Partially update an existing product. |
| DELETE | `/products/{product_id}` | Delete a product. |

## Environment Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
python -m pip install fastapi uvicorn "psycopg[binary]" python-dotenv pytest httpx2
```

Create a local environment file:

```bash
cp .env.example .env
```

Example `.env`:

```text
DATABASE_URL=postgresql://<username>@localhost:5432/inventory_management_db
```

Create a separate test environment file named `.env.test`.

Example `.env.test`:

```text
DATABASE_URL=postgresql://<username>@localhost:5432/inventory_management_test_db
```

> `.env` and `.env.test` are ignored by Git and should not contain credentials that are committed to the repository.

## Database Setup

Create the development database:

```bash
createdb inventory_management_db
```

Create the test database:

```bash
createdb inventory_management_test_db
```

Open the development database:

```bash
psql inventory_management_db
```

Create the `products` table:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    category TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

Create the same `products` table in the test database:

```bash
psql inventory_management_test_db
```

Then run the same `CREATE TABLE products (...)` statement.

The project uses two separate PostgreSQL databases:

- `inventory_management_db` — Used for local development.
- `inventory_management_test_db` — Used by pytest to keep automated tests isolated from development data.

## Running the Application

Start the FastAPI development server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

You can use the Swagger UI at `/docs` to inspect available endpoints and send API requests directly from the browser.

Example health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

## Running Tests

Run the full automated test suite with pytest:

```bash
python -m pytest
```

The test suite covers:

- Health and version endpoints
- Product creation
- Retrieve all products
- Retrieve a product by ID
- Full product updates with PUT
- Partial product updates with PATCH
- Product deletion
- 404 error handling for missing products
- 422 validation errors for invalid requests
- PATCH validation for explicit `null` values
- Verification that failed requests do not modify database data

Tests use a separate PostgreSQL test database defined in `.env.test`.

A pytest fixture automatically clears the `products` table before and after each test:

```sql
TRUNCATE TABLE products RESTART IDENTITY;
```

This keeps tests isolated and prevents one test from affecting another.

The current test suite contains 15 automated tests.

## Project Status

The core backend implementation is complete.

Completed functionality includes:

- FastAPI application setup
- Product CRUD REST API
- PostgreSQL persistence
- Pydantic request validation
- HTTP 404 and 422 error handling
- Partial updates with `PATCH`
- Dynamic PATCH field updates using `model_dump(exclude_unset=True)`
- PostgreSQL development and test databases
- Automated API integration testing with pytest
- Test isolation using pytest fixtures
- Git branch and merge workflow practice
- Git recovery practice with `restore`, `reset`, and `revert`

Current automated test result:

```text
15 passed
```

The project is currently in the documentation and repository finalization stage.

## Git Workflow

This project was developed with Git-based version control and included practice with both normal feature development and recovery workflows.

Git concepts used in this project include:

- Creating feature branches
- Committing small development milestones
- Fast-forward merges
- Merge commits after branch divergence
- Deleting merged feature branches
- Inspecting commit history with `git log`
- Discarding working directory changes with `git restore`
- Unstaging files with `git restore --staged`
- Reverting committed changes with `git revert`
- Rewriting local history with:
  - `git reset --soft`
  - `git reset --mixed`
  - `git reset --hard`

Example commit history:

```text
refactor: improve partial product updates
test: add API error path coverage
test: add isolated CRUD API tests
test: add basic API tests
feat: add health check endpoint
refactor: remove in-memory product data
feat: integrate PostgreSQL product deletion
feat: integrate PostgreSQL product updates
feat: integrate PostgreSQL product creation
feat: integrate PostgreSQL product queries
```

The project uses small, meaningful commits so that individual development milestones can be reviewed and recovered independently.

## Future Improvements

Potential future enhancements include:

- Add authentication and user accounts
- Add product categories and filtering
- Add pagination for product lists
- Add more advanced validation rules
- Add database migrations
- Add Docker support
- Add CI/CD for automated testing
- Deploy the API to a cloud environment
- Add frontend or mobile clients
- Add logging and production monitoring

These features are intentionally outside the current project scope and can be explored in later projects.

## What I Learned

Through this project, I practiced how a backend API is designed, implemented, tested, and version-controlled as a complete development workflow.

Key learning outcomes include:

- Designing REST API routes with FastAPI
- Understanding the difference between GET, POST, PUT, PATCH, and DELETE
- Using Pydantic models for request validation
- Handling HTTP errors such as 404 and 422
- Connecting Python applications to PostgreSQL with psycopg
- Writing parameterized SQL queries
- Using `RETURNING` to retrieve inserted, updated, or deleted rows
- Understanding the difference between `None`, JSON `null`, and SQL `NULL`
- Implementing precise partial updates with `model_dump(exclude_unset=True)`
- Dynamically building safe SQL update statements
- Writing automated API integration tests with pytest
- Using fixtures to prepare and clean test environments
- Separating development and test databases
- Applying Arrange → Act → Assert in automated tests
- Practicing Git branches, merges, commits, restore, reset, and revert
- Breaking development work into small, verifiable milestones
