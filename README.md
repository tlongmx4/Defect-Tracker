Defect Tracker (v2)

Defect Tracker is a modular backend system designed for manufacturing environments to manage quality defects, safety incidents, and operational workflows with structured lifecycle control and role-based access.

Built with FastAPI, SQLAlchemy, and PostgreSQL.

Architecture

FastAPI for API layer

SQLAlchemy ORM for domain modeling

PostgreSQL for persistence

JWT Authentication

Database-driven RBAC (Users → Roles → Scopes)

Service layer pattern (routers → services → models)

Enum-backed workflow state machines

Audit logging for lifecycle transitions

The system separates HTTP concerns from business logic using a service layer to enforce domain rules and workflow integrity.

Modules
Quality Module (Defects)

Create and manage manufacturing defects

Status tracking

Filtering and pagination

Scope-based access control

Safety Module (Incidents) — v2

Implements structured safety incident tracking with enforced workflow rules.

Features:

Incident creation with:

Severity (Near Miss, First Aid, Recordable, PSIF)

Location

Department

Shift

Description

Controlled status transitions:

OPEN → INVESTIGATING → CORRECTIVE_ACTION → CLOSED

Business rule enforcement:

Incidents cannot be closed without a documented corrective action

Full audit trail:

Every status change is recorded

Tracks old status, new status, user, and timestamp

Scope-based authorization:

safety:incidents:read

safety:incidents:write

This module demonstrates lifecycle-driven domain modeling rather than simple CRUD behavior.

Authentication & Authorization

OAuth2 + JWT-based authentication

Role-based access control stored in the database

Scope enforcement at the route level

Separation of read and write permissions

Current Status

Quality Module complete

Safety Module complete (workflow + audit logging)

RBAC fully implemented

Ready for additional domain modules

Planned Enhancements

Production / Downtime Tracking module

Reporting and export features

Analytics and dashboard layer

Frontend UI integration