# IncidentLab

A production-inspired backend platform for learning modern backend engineering through incremental architectural evolution.

Rather than building features first, IncidentLab focuses on establishing strong engineering foundations—including API design, persistence, dependency injection, authentication, exception handling, and future production capabilities.

---

# Why IncidentLab Exists

IncidentLab demonstrates how backend systems evolve over time through small, well-defined architectural milestones.

Each release introduces a single foundational capability while preserving existing behavior and maintaining a clean architecture.

---

# Current Release

**v0.7.0 — Authentication Foundation**

Current architectural foundations:

- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation
- Authentication Foundation

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

## Authentication Foundation

- JWT-based authentication
- User registration
- User login
- Password hashing using Argon2
- HTTP Bearer authentication
- Protected API endpoints
- Current user dependency injection

---

# High-Level Architecture

```text
                  Client
                     │
                     ▼
      Authorization: Bearer <JWT>
                     │
                     ▼
             FastAPI Endpoints
                     │
                     ▼
      Authentication Dependency
                     │
                     ▼
       Dependency Injection Layer
          ┌──────────┴──────────┐
          ▼                     ▼
 Application Services     Database Provider
          │
          ▼
     Repository Layer
          │
          ▼
     SQLAlchemy Async ORM
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
    │   ├── auth/
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

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Authenticate user and receive JWT |
| GET | `/api/v1/auth/me` | Retrieve authenticated user |

## Incidents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/incidents` | Create incident *(Authentication Required)* |
| GET | `/api/v1/incidents` | List incidents *(Authentication Required)* |
| GET | `/api/v1/incidents/{id}` | Retrieve incident by ID *(Authentication Required)* |

---

# Technology Stack

- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Pydantic v2
- PyJWT
- pwdlib (Argon2)
- Uvicorn

---

# Roadmap

## Completed

- Repository Foundation
- Platform Operations Foundation
- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation
- Authentication Foundation

## Upcoming

- Containerization
- CI/CD Foundation
- Infrastructure as Code
- Kubernetes
- Observability
- DevSecOps
- Authorization (RBAC)

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

Each release follows an architecture-first workflow:

1. Requirements
2. Architecture Decision Record (ADR)
3. Implementation (Feature Branch)
4. Testing
5. Merge into `main`
6. Documentation
7. Release Tag

---

# Release History

| Version | Milestone |
|----------|-----------|
| v0.7.0 | Authentication Foundation |
| v0.6.0 | Dependency Injection Foundation |
| v0.5.0 | Error Handling Foundation |
| v0.4.0 | Persistence Foundation |
| v0.3.0 | API Foundation |
| v0.2.0 | Platform Operations Foundation |
| v0.1.0 | Repository Foundation |

---

# Repository Status

IncidentLab follows an architecture-first, milestone-driven development approach where each release introduces one foundational capability while maintaining backward compatibility and preserving clean software architecture.

The project is currently focused on evolving into a production-grade cloud-native backend platform through incremental engineering milestones.
