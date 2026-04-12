Defect Tracker (v2)

Defect Tracker is a modular backend system designed for manufacturing environments to manage quality defects, safety incidents, and operational workflows with structured lifecycle control and role-based access.

Design Decisions
This project started as an exercise in mimicking real Cummins manufacturing quality processes in code. Working on the X15 line gave me a lot of opinions about how defect tracking, safety reporting, and authorization should work — and a lot of frustrations with how brittle most off-the-shelf tools are when business rules collide with reality. The choices below reflect that perspective.
Service layer instead of fat routers. Routers in this project do exactly two things: validate the request shape and call into a service. All business rules — who can do what, which state transitions are legal, when an audit entry gets written — live in the service layer. The reason is simple: in a real quality system, the same rule has to hold whether the action came from a web request, a scheduled job, or a CLI script. Putting the rules in the routers means duplicating them every time a new entry point shows up, and duplicated rules drift. Putting them in the service layer means there's one place a rule lives and one place it can be wrong.
Database-driven RBAC instead of hardcoded role decorators. A lot of FastAPI tutorials show role checks as decorators with the role name baked in: @requires_role("admin"). That works until the day someone in the plant needs a permission their role doesn't have, and now you're shipping code to production to fix an org chart. In manufacturing, roles and responsibilities shift constantly — a tech gets promoted, a supervisor takes on a new line, a quality engineer rotates departments. Storing roles and scopes in the database, with users mapped to roles and roles mapped to scopes, means access changes are configuration, not deployments. The route layer just asks "does this user have the safety:incidents:write scope?" and the answer comes from the data, not the code.
Enum-backed state machines instead of a status string field. A defect or incident isn't really a record with a status column — it's a workflow with legal and illegal transitions. An incident in OPEN can move to INVESTIGATING, but it can't jump straight to CLOSED. A "status" field as a free string lets any caller write any value, and the database happily stores nonsense. Modeling status as an enum and the transitions as an explicit map of allowed moves means the invalid states are unrepresentable — the service layer rejects the transition before it ever touches the database. This is the same logic that lives inside Cummins quality processes: a defect doesn't get closed without a documented containment and corrective action, and the system enforces that, not the person filling out the form.
Business rules enforced at the service layer, not in the database. The incident module won't let you close an incident without a documented corrective action. That rule could live as a database constraint, but database constraints give you opaque errors and no good way to explain why the operation failed. Enforcing it in the service layer means the API can return a clear, structured error that a frontend (or another service) can act on. The database is still the source of truth for what is; the service layer is the source of truth for what's allowed.
Audit logging on every lifecycle transition. Every status change writes an audit row capturing the old status, the new status, the user who made the change, and the timestamp. This isn't a nice-to-have for a quality system — it's the entire point. When something goes wrong on the floor, the question isn't "what's the current state of this defect," it's "who decided to close it, when, and what was the state before they touched it." Without that history, root cause analysis becomes guesswork. With it, the timeline is reconstructable. Putting the audit write inside the same service method that performs the transition means there's no path where the state changes without an audit entry — they're atomic from the API's perspective.
Separation of read and write scopes. Most people in a plant need to see defects and incidents — line techs, supervisors, engineers, leadership. Far fewer should be able to modify them. Splitting safety:incidents:read from safety:incidents:write (and the same for the quality module) means the default safe answer for a new role is "give them read access," and write access is something you grant deliberately. It's a small thing, but it makes the principle of least privilege the path of least resistance instead of an extra step.

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