Defect Tracker API
Overview

Defect Tracker is a backend API designed to manage and track production defects in a structured, queryable system.

It models real-world quality workflows by supporting:

Defect creation

Status updates

Assignment tracking

Pagination and filtering

UUID-based identifiers

Layered architecture (routes → services → models)

This project focuses on clean backend structure and maintainable service-layer design.

Tech Stack

Python 3.14

FastAPI

SQLAlchemy

PostgreSQL (Dockerized)

Pydantic v2

UUID primary keys

Architecture

The project follows a layered architecture:

app/

db/

models.py (SQLAlchemy models)

session.py (DB session management)

api/

routes/

defects.py (HTTP layer)

services/

defects.py (business logic)

schemas/

defects.py (Pydantic request/response models)

main.py (application entry point)

Separation of concerns:

Routes handle HTTP + validation

Services handle business logic + DB interaction

Models define persistence structure

Schemas define API contracts

Features
Create Defect

POST /api/defects

Creates a new defect with:

reported_by

category

subcategory

description

absn

assigned_to

status

Returns full defect object with UUID and created_at timestamp.

List Defects (Paginated + Filtered)

GET /api/defects

Supports:

limit (default 50)

offset

status (optional filter)

Example:

/api/defects?status=open

Returns:

{
items: [...],
limit: 50,
offset: 0,
total: 3
}

Retrieve Defect by ID

GET /api/defects/{defect_id}

UUID validated automatically

Returns 404 if not found

Partial Update (PATCH)

PATCH /api/defects/{defect_id}

Supports partial updates using Pydantic's exclude_unset=True.

Allows updating:

status

assigned_to

description

category

subcategory

Returns updated defect object.

Design Decisions
UUID Primary Keys

Using UUIDs instead of integers for:

distributed system compatibility

non-sequential identifiers

production-style data modeling

Service Layer Pattern

Database queries are isolated in service functions to:

decouple HTTP layer from business logic

simplify testing

improve maintainability

Filtered Query Counting

Pagination total reflects filtered results, not full table size.

Running Locally
1. Start Postgres via Docker

docker compose up -d

2. Create virtual environment

python -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run API

uvicorn app.main:app --reload

5. Open Swagger Docs

http://localhost:8000/docs

Future Enhancements

updated_at and updated_by fields

Role-based authentication

Audit log table for defect status changes

Full-text search

Sorting support

Migration management (Alembic)