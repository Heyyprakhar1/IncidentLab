# IncidentLab

A production-inspired backend platform for learning modern backend engineering through incremental architectural evolution.

Rather than building features first, IncidentLab focuses on establishing strong engineering foundations—including API design, persistence, exception handling, dependency management, and future production capabilities.

---

# Why IncidentLab Exists

IncidentLab demonstrates how backend systems evolve over time through small, well-defined architectural milestones.

Each release introduces a single foundational capability while preserving existing behavior and maintaining a clean architecture.

---

# Current Release

**v0.6.0 — Dependency Injection Foundation**

Current architectural foundations:

- API Foundation
- Persistence Foundation
- Error Handling Foundation
- **Dependency Injection Foundation**

---

# Implemented Foundations

## API Foundation

- FastAPI application bootstrap
- Versioned API routing
- Request lifecycle management
- Structured logging middleware

---

## Persistence Foundation

- SQLAlchemy Async ORM
- Alembic migrations
- Repository pattern
- PostgreSQL integration

---

## Error Handling Foundation

- Global exception handling
- Standardized API error responses
- Domain-specific exceptions
- Centralized error management

---

## Dependency Injection Foundation

- Dedicated dependency provider layer
- Repository dependency providers
- Service dependency providers
- Centralized object construction
- Improved separation of concerns
- FastAPI dependency injection

---

# High-Level Architecture

```text
                Client
                   │
                   ▼
            FastAPI Endpoints
                   │
                   ▼
      Dependency Injection Layer
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
   Application Services   Database Provider
         │
         ▼
    Repositories
         │
         ▼
     SQLAlchemy ORM
         │
         ▼
      PostgreSQL
```

---

# Repository Structure

```text
apps/
└── api/
    ├── app/
    │   ├── api/
    │   ├── core/
    │   ├── db/
    │   ├── dependencies/
    │   ├── exceptions/
    │   ├── middleware/
    │   ├── models/
    │   ├── repositories/
    │   ├── schemas/
    │   └── services/
    ├── migrations/
    └── tests/

docs/
├── adr/
├── architecture.md
├── changelog.md
├── product-requirements.md
└── roadmap.md
```

---

# Technology Stack

- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Pydantic v2
- Uvicorn

---

# Roadmap

Completed

- Repository Foundation
- Platform Operations Foundation
- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation

Upcoming

- Authentication & Authorization
- Configuration Management
- Testing Foundation
- Background Processing
- Event-Driven Architecture
- Observability Expansion

---

# Documentation

Project documentation is available under the `docs/` directory.

Key documents include:

- Architecture
- Product Requirements
- Roadmap
- ADRs
- Changelog

---

# Development Workflow

Each release follows a milestone-based workflow:

1. Create feature branch
2. Design (ADR)
3. Implementation
4. Architecture Review
5. Documentation
6. Merge into `main`
7. Release Tag

---

# Release History

| Version | Milestone |
|----------|-----------|
| v0.6.0 | Dependency Injection Foundation |
| v0.5.0 | Error Handling Foundation |
| v0.4.0 | Persistence Foundation |
| v0.3.0 | API Foundation |
| v0.2.0 | Platform Operations Foundation |
| v0.1.0 | Repository Foundation |

---

# Repository Status

Current development follows an architecture-first approach where each release introduces one foundational capability while maintaining backward compatibility and preserving existing application behavior.
