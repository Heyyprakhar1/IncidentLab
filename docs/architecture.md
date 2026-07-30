# IncidentLab Architecture

This document describes the current architecture of IncidentLab and the engineering principles that guide its evolution.

Rather than focusing on implementation details, this document explains the platform's architectural structure, component responsibilities, and design decisions.

Current Architecture Version:

**v0.5.0 — Error Handling Foundation**

---

# Architectural Goals

IncidentLab is designed around the following principles:

- Layered Architecture
- Separation of Concerns
- Single Responsibility
- Operational Ownership
- Incremental Evolution
- Documentation-Driven Development

Each engineering milestone strengthens one architectural capability while preserving maintainability and clear component boundaries.

---

# High-Level Architecture

```
                Client
                   │
                   ▼
             API Endpoints
                   │
                   ▼
            Service Layer
                   │
                   ▼
          Repository Layer
                   │
                   ▼
              PostgreSQL
```

Every request flows through clearly defined application layers, ensuring business logic remains independent from persistence and HTTP concerns.

---

# Layer Responsibilities

## API Layer

Responsible for:

- HTTP routing
- Request validation
- Response serialization
- Delegating work to services

The API layer contains no business logic.

---

## Service Layer

Responsible for:

- Business workflows
- Validation
- Application rules
- Coordinating repositories

Services are independent of HTTP-specific behavior.

---

## Repository Layer

Responsible for:

- Database interaction
- Query execution
- Persistence operations
- ORM abstraction

Repositories isolate persistence from business logic.

---

## Database Layer

Responsible for:

- Data storage
- Entity relationships
- Transaction persistence

SQLAlchemy models represent the database schema while Alembic manages schema evolution.

---

# Error Handling Architecture

Beginning with **v0.5.0**, IncidentLab adopts centralized exception handling.

Instead of constructing HTTP error responses throughout the application, domain-specific exceptions are propagated to a global exception handler.

```
Exception Raised
        │
        ▼
Global Exception Handler
        │
        ▼
Standardized Error Response
```

This approach provides:

- Consistent API responses
- Centralized error formatting
- Reduced duplication
- Better separation of concerns
- Easier extensibility

Implementation details and rationale are documented in **ADR-003 – Global Exception Handling**.

---

# Request Lifecycle

Normal request flow:

```
Client
   │
   ▼
API Endpoint
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
Database
   │
   ▼
Response
```

Error flow:

```
Any Layer
    │
    ▼
Application Exception
    │
    ▼
Global Exception Handler
    │
    ▼
Standardized Error Response
```

This separation keeps business logic focused on application behavior while the exception handler manages HTTP-specific error responses.

---

# Repository Structure

```
apps/api/

├── api/
├── models/
├── schemas/
├── repositories/
├── services/
├── exceptions/
├── middleware/
├── migrations/
├── config.py
├── lifespan.py
├── logging_config.py
└── main.py
```

Each package owns a single responsibility and communicates through well-defined interfaces.

---

# Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `api/` | HTTP endpoints and routing |
| `services/` | Business logic |
| `repositories/` | Database access |
| `models/` | Database entities |
| `schemas/` | Request and response contracts |
| `exceptions/` | Exception hierarchy and handlers |
| `middleware/` | Cross-cutting concerns |
| `config.py` | Configuration management |
| `lifespan.py` | Application lifecycle |
| `logging_config.py` | Logging configuration |

---

# Engineering Foundations

The platform currently consists of the following completed foundations:

- ✅ Repository Foundation
- ✅ Application Foundation
- ✅ Platform Operations Foundation
- ✅ API Foundation
- ✅ Persistence Foundation
- ✅ Error Handling Foundation

Each foundation represents a stable architectural milestone.

---

# Design Principles

## Layered Architecture

Each layer owns a single responsibility and communicates only with adjacent layers.

---

## Separation of Concerns

Business logic, persistence, configuration, logging, and error handling remain independent to improve maintainability.

---

## Single Responsibility

Every package and module exists for one clearly defined purpose.

---

## Incremental Evolution

Architectural capabilities are introduced through small, stable milestones rather than large redesigns.

---

# Future Architecture

Future engineering milestones will extend the platform with:

- Dependency injection
- Authentication and authorization
- Incident lifecycle management
- Root Cause Analysis (RCA)
- Runbooks
- Audit history
- Metrics and observability
- Distributed tracing
- Kubernetes integrations
- Event-driven workflows
- Automated remediation

These capabilities will build upon the existing architectural foundations without changing the core layered design.

---

# Related Documentation

- `README.md`
- `docs/product-requirements.md`
- `docs/roadmap.md`
- `docs/changelog.md`
- `docs/adr/`

---

# Summary

IncidentLab follows a production-inspired layered architecture where each engineering milestone introduces one architectural capability while preserving maintainability, operational ownership, and documentation quality.

The architecture is intentionally designed to evolve incrementally, ensuring that future capabilities can be introduced without compromising the stability or clarity of the existing platform.
