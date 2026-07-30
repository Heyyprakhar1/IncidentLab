# ADR-004: Dependency Injection Foundation

- **Status:** Accepted
- **Date:** 2026-07-30
- **Release:** v0.6.0 – Dependency Injection Foundation

---

# Context

As IncidentLab has evolved through multiple architectural milestones, application components are currently instantiated manually within the API layer.

Endpoints are responsible for creating service instances, while services construct their own repository dependencies.

Although this approach is sufficient for a small codebase, it introduces unnecessary coupling between layers and makes future enhancements such as testing, authentication, caching, and observability more difficult.

To continue evolving IncidentLab as a production-inspired backend, dependency creation should become a responsibility of the framework rather than individual application components.

---

# Problem Statement

The current implementation has several architectural limitations:

- API endpoints manually instantiate services.
- Services manually instantiate repositories.
- Dependency creation logic is duplicated.
- Components are tightly coupled.
- Unit testing requires manual dependency construction.
- Replacing implementations becomes increasingly difficult as the application grows.

These issues reduce maintainability and limit future extensibility.

---

# Decision

IncidentLab adopts **FastAPI's dependency injection system** as the standard mechanism for managing application dependencies.

Application components will no longer create their own dependencies.

Instead, dependency providers will be responsible for constructing and supplying:

- Database sessions
- Repository instances
- Service instances

The API layer will receive fully constructed dependencies through FastAPI's `Depends()` mechanism.

---

# Architecture Before

Current dependency flow:

```text
Client
   │
   ▼
API Endpoint
   │
   ▼
IncidentService()
   │
   ▼
IncidentRepository()
   │
   ▼
Database Session
```

Each layer is responsible for creating the next layer.

---

# Architecture After

Dependency providers become responsible for object construction.

```text
Client
   │
   ▼
API Endpoint
   │
   ▼
Depends(get_incident_service)
   │
   ▼
Depends(get_incident_repository)
   │
   ▼
Depends(get_db)
   │
   ▼
Database Session
```

Business components focus solely on business responsibilities while the framework manages dependency creation.

---

# Rationale

Dependency Injection improves the architecture by separating **object creation** from **object usage**.

This provides several benefits:

- Reduced coupling
- Cleaner API endpoints
- Reusable dependency providers
- Easier testing
- Improved maintainability
- Better scalability
- Consistent dependency management

This architectural change also prepares the platform for future capabilities that rely on dependency injection.

---

# Alternatives Considered

## Manual Instantiation

Each endpoint creates service objects directly.

**Rejected because:**

- High coupling
- Repeated construction logic
- Poor scalability
- Difficult testing

---

## Global Singleton Objects

Create shared service instances during application startup.

**Rejected because:**

- Unsuitable for request-scoped dependencies
- Makes lifecycle management more difficult
- Limits flexibility for future enhancements

---

# Consequences

## Positive

- Cleaner endpoint implementations
- Centralized dependency management
- Improved separation of concerns
- Easier mocking during tests
- Better architectural consistency
- Reduced duplication

## Trade-offs

- Introduces additional dependency provider modules.
- Requires familiarity with FastAPI's dependency system.
- Slightly increases the number of application components.

These trade-offs are acceptable because they significantly improve long-term maintainability.

---

# Implementation

This decision introduces a dedicated dependency layer responsible for constructing application components.

The dependency layer provides:

- `get_db()` (re-exported from `app.core.database`)
- `get_incident_repository()`
- `get_incident_service()`

API endpoints consume these providers through FastAPI's dependency injection mechanism instead of manually constructing services.

Database session lifecycle management remains centralized within `app.core.database`, ensuring a single source of truth for database session creation.

---

# Future Impact

This foundation enables future milestones including:

- Authentication
- Authorization
- Configuration providers
- Repository abstraction
- Service abstraction
- Unit testing with dependency overrides
- Background tasks
- Event-driven workflows

Dependency Injection becomes the standard pattern for introducing new application services.

---

# Related Components

Primary areas affected by this decision include:

- `app/api/`
- `app/core/`
- `app/dependencies/`
- `app/repositories/`
- `app/services/`

---

# Related Documentation

- `README.md`
- `docs/architecture.md`
- `docs/roadmap.md`
- `docs/changelog.md`

---

# Status

This decision establishes Dependency Injection as the standard mechanism for managing application dependencies throughout IncidentLab.

Beginning with **v0.6.0 – Dependency Injection Foundation**, all new application components should receive their dependencies through dedicated providers rather than constructing them directly.
