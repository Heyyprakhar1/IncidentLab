# Architecture

## Purpose

This document describes the current software architecture of IncidentLab.

It explains how the platform is organized, how responsibilities are separated, and how application components collaborate to deliver business capabilities.

Unlike the Product Requirements document, this document focuses on implementation structure and architectural decisions rather than product goals.

---

# Architectural Overview

IncidentLab follows a **layered architecture** designed to promote maintainability, modularity, and clear separation of concerns.

Each layer owns a single responsibility and communicates only with the adjacent layer.

The architecture intentionally isolates HTTP handling from business logic and persistence, allowing the platform to evolve without widespread structural changes.

---

# Architecture Principles

The platform is built around several architectural principles.

## Single Responsibility

Every module should own one responsibility.

Examples include:

- API routers own HTTP routing.
- Services own business use cases.
- Repositories own database interaction.
- Models define persisted entities.
- Schemas define API contracts.
- Configuration manages application settings.

Responsibilities should not overlap.

---

## Separation of Concerns

Business rules should remain independent of HTTP handling and database implementation.

Each architectural layer has a clearly defined purpose.

---

## Layered Design

Application behavior flows through dedicated layers.

```text
HTTP Request
      │
      ▼
API Router
      │
      ▼
Application Service
      │
      ▼
Repository
      │
      ▼
SQLAlchemy ORM
      │
      ▼
Database
```

Each layer performs one responsibility before delegating work to the next layer.

---

## Dependency Direction

Dependencies always flow downward.

```text
API
 │
 ▼
Services
 │
 ▼
Repositories
 │
 ▼
Database
```

Lower layers never depend on higher layers.

This keeps business logic reusable and minimizes coupling between application components.

---

# Application Structure

The current API application is organized as follows.

```text
app/

├── api/
│   └── v1/
│       ├── endpoints/
│       └── router.py
│
├── core/
│
├── db/
│
├── middleware/
│
├── models/
│
├── repositories/
│
├── schemas/
│
├── services/
│
├── config.py
├── lifespan.py
├── logging_config.py
└── main.py
```

Each directory represents a distinct architectural responsibility.

---

# Layer Responsibilities

## API Layer

The API layer receives HTTP requests and returns HTTP responses.

Responsibilities include:

- Route registration
- Request validation
- Response serialization
- Dependency injection
- Delegating work to application services

The API layer contains no business logic.

---

## Service Layer

The service layer represents application use cases.

Responsibilities include:

- Coordinating business operations
- Constructing domain entities
- Calling repositories
- Returning API response models

The service layer does not perform database queries directly.

---

## Repository Layer

Repositories encapsulate all persistence operations.

Responsibilities include:

- Creating records
- Retrieving records
- Updating records
- Deleting records
- Managing ORM queries

Repositories isolate SQLAlchemy usage from the rest of the application.

---

## Model Layer

Models represent persisted database entities.

Responsibilities include:

- Database table definitions
- ORM mappings
- Entity representation

Models do not contain business logic.

---

## Schema Layer

Schemas define the public API contract.

Responsibilities include:

- Request validation
- Response serialization
- Data transformation

Schemas are independent of database implementation.

---

## Database Layer

The database layer provides persistence infrastructure.

Current responsibilities include:

- SQLAlchemy ORM configuration
- Declarative model registration
- Database session management
- Alembic migration support

This layer provides a stable foundation for future persistence requirements.

---

# Request Lifecycle

A typical request follows the workflow below.

```text
Client
   │
   ▼
Router
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
Repository
   │
   ▼
Service
   │
   ▼
Response Schema
   │
   ▼
Client
```

Each layer contributes one clearly defined responsibility.

---

# Current Architectural Capabilities

The current implementation provides:

## Platform Foundation

- FastAPI application bootstrap
- Typed configuration
- Lifecycle management
- Structured logging

---

## API Foundation

- Versioned routing
- Modular router composition
- Typed request schemas
- Typed response schemas
- Service layer architecture

---

## Persistence Foundation

- SQLAlchemy ORM
- Alembic migrations
- Repository pattern
- Database session management
- Persistent Incident entities

---

# Architectural Benefits

The current architecture provides several engineering advantages.

## Maintainability

Components remain small, focused, and independently understandable.

---

## Testability

Business logic can be tested independently from HTTP routing and persistence.

---

## Extensibility

New capabilities can be introduced by extending existing layers rather than restructuring the application.

---

## Consistency

Every feature follows the same architectural workflow from request to persistence.

---

# Future Evolution

Future milestones are expected to build upon the current layered architecture.

Planned additions include:

- Global exception handling
- Authentication
- Authorization
- Incident lifecycle management
- Audit logging
- Background processing
- Event-driven workflows
- Observability enhancements

These capabilities will integrate into the existing architecture without changing the established layer boundaries.

---

# Summary

IncidentLab currently follows a modular layered architecture that separates HTTP handling, business logic, persistence, and database concerns into dedicated components.

This architecture provides a stable foundation for incremental platform evolution while preserving maintainability, operational clarity, and long-term scalability.
