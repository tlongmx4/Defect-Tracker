Defect Tracker API

A backend service for tracking manufacturing defects, including authenticated updates, status transition auditing, and query filtering.

This project demonstrates layered backend architecture, API design best practices, and controlled data integrity using FastAPI and PostgreSQL.

🚀 Features

Create, read, and update defects

API key authentication for write operations

Enum validation for defect status (open, repaired)

Filtering by status and category

Validated sorting (ascending / descending)

Pagination support (limit, offset)

Automatic lifecycle timestamps (created_at, updated_at)

Actor tracking via updated_by

Audit logging for defect status transitions

Endpoint for retrieving audit history per defect

🏗 Architecture Overview

The service follows a clean layered architecture:

routes/        → HTTP layer (FastAPI endpoints)
schemas/       → Pydantic request/response models
services/      → Business logic and domain rules
db/models.py   → SQLAlchemy ORM models
PostgreSQL     → Persistent storage


Key design decisions:

Business logic lives in the service layer (not routes).

Status transitions trigger audit events inside the update service.

Authentication is implemented via dependency injection.

Sorting is validated against a controlled field map to prevent unsafe queries.

PATCH uses exclude_unset=True to support partial updates correctly.

🔐 Authentication

Write operations require an API key sent via header:

X-API-Key: <your_api_key>


Protected endpoints:

POST /api/defects

PATCH /api/defects/{defect_id}

Read operations are currently public.

📡 API Endpoints
List Defects
GET /api/defects


Query parameters:

limit

offset

status

category

sort_by (supports -field for descending)

Example:

GET /api/defects?status=open&sort_by=-updated_at

Create Defect (Auth Required)
POST /api/defects

Update Defect (Auth Required)
PATCH /api/defects/{defect_id}


Automatically:

Updates updated_at

Sets updated_by

Creates an audit log entry if status changes

Get Defect Audit History
GET /api/defects/{defect_id}/audit


Returns status transition history ordered by most recent change.

🧾 Example Response
{
  "id": "81c99e5d-0282-43fa-84d8-ca9ebf6c67e9",
  "created_at": "2026-02-15T00:20:05.286848Z",
  "updated_at": "2026-02-15T00:20:05.286848Z",
  "reported_by": "audit 3",
  "category": "loose",
  "subcategory": "not torqued",
  "description": "loose flywheel",
  "absn": "3540",
  "assigned_to": "assem-tool",
  "status": "open",
  "updated_by": "Demo User"
}

🗂 Audit Log Model

Each status change creates an audit entry containing:

defect_id

changed_by

old_status

new_status

changed_at

This ensures traceability of state transitions.

🛠 Tech Stack

FastAPI

SQLAlchemy

PostgreSQL

Docker

Pydantic

🔮 Future Enhancements

Role-based authorization

Soft deletes

Full-text search

Alembic migrations

CI/CD integration

🎯 Purpose

This project demonstrates backend architecture fundamentals:

Clean separation of concerns

Safe query construction

Authentication and identity tracking

Event-driven audit logging

Correct HTTP semantics

Controlled domain validation