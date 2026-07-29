# ADR-002: Layered Application Architecture

**Status:** Accepted

**Date:** 29 July 2026

**Decision Makers:** Prakhar Srivastava

---

# Context

As IncidentLab evolved beyond a simple HTTP service, the application began introducing persistent business workflows.

The platform now includes API endpoints, business services, database repositories, ORM models, and typed request and response schemas.

Without clear architectural boundaries, application logic, HTTP concerns, and database operations would gradually become tightly coupled, making the platform harder to maintain as additional capabilities are introduced.

A consistent architectural structure is therefore required before expanding the platform with authentication, incident lifecycle management, and operational intelligence.

---

# Decision

IncidentLab adopts a **Layered Application Architecture**.

Application responsibilities are divided into dedicated layers.

```
HTTP Request
      │
      ▼
Router
      │
      ▼
Endpoint
      │
      ▼
Service
      │
      ▼
Repository
      │
      ▼
ORM Model
      │
      ▼
Database
```

Each layer owns a single responsibility and communicates only with its adjacent layer.

---

# Layer Responsibilities

## API Layer

Responsible for:

- Versioned routing
- HTTP request handling
- Request validation
- Response serialization

---

## Service Layer

Responsible for:

- Business workflows
- Application use cases
- Coordination between layers

The service layer contains business logic and remains independent of HTTP implementation details.

---

## Repository Layer

Responsible for:

- Database interaction
- ORM persistence
- Query execution
- Transaction management

Repositories encapsulate SQLAlchemy operations so that services never communicate directly with the database.

---

## Domain Layer

Responsible for:

- ORM entity definitions
- Database mappings
- Persistent application models

---

## Schema Layer

Responsible for:

- Request validation
- Response serialization
- Public API contracts

Schemas define how data enters and leaves the application.

---

# Rationale

A layered architecture aligns with the engineering goals of IncidentLab.

It provides:

- Clear separation of responsibilities.
- Improved maintainability.
- Better testability.
- Easier refactoring.
- Consistent request handling.
- Reusable business logic.
- Scalable application structure.
- Simplified future feature development.

This approach supports incremental platform evolution while preventing architectural drift.

---

# Alternatives Considered

## Fat Route Handlers

Business logic, validation, and database operations remain inside API endpoints.

### Advantages

- Simple for small applications.
- Fewer files.

### Disadvantages

- Tight coupling.
- Difficult testing.
- Poor maintainability.
- Limited scalability.

---

## Active Record Style

ORM models own both persistence and business logic.

### Advantages

- Less abstraction.
- Faster initial development.

### Disadvantages

- Mixed responsibilities.
- Difficult to evolve.
- Business logic tightly coupled to persistence.

Given IncidentLab's long-term goals, these trade-offs outweigh the benefits.

---

# Consequences

## Positive

- Clear architectural boundaries.
- Consistent application structure.
- Independent evolution of layers.
- Improved code readability.
- Easier onboarding.
- Better long-term maintainability.
- Simpler feature expansion.

## Negative

- More modules than a simple CRUD application.
- Additional abstraction.
- Slightly higher initial development effort.

These trade-offs are acceptable because they improve long-term engineering quality.

---

# Scope

This decision applies to:

- API endpoints
- Services
- Repositories
- ORM models
- Request schemas
- Response schemas
- Database interactions

Future platform capabilities should follow the same layered architecture.

---

# Review

This decision should be revisited only if:

- The platform adopts a distributed microservice architecture.
- Domain complexity requires an alternative architectural style.
- Operational requirements justify significant architectural changes.

Until then, the Layered Application Architecture remains the preferred application structure.

---

# Related Documents

- architecture.md
- product-requirements.md
- roadmap.md
- ADR-001-monorepo-strategy.md

---

# Decision Summary

IncidentLab adopts a Layered Application Architecture to separate HTTP handling, business logic, persistence, and data models into dedicated responsibilities, enabling maintainable and scalable platform evolution.
