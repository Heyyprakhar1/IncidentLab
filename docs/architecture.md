# System Architecture

IncidentLab follows a layered architecture that emphasizes separation of concerns, maintainability, and incremental architectural evolution.

Beginning with **v0.6.0 – Dependency Injection Foundation**, application components no longer construct their own dependencies. Instead, object creation is delegated to dedicated dependency providers managed through FastAPI's dependency injection system.

---

# Architectural Principles

The project follows these principles:

- Separation of Concerns
- Single Responsibility Principle
- Dependency Injection
- Repository Pattern
- Layered Architecture
- Incremental Evolution
- Production-Inspired Design

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
         ┌──────────┴──────────┐
         ▼                     ▼
 Application Services    Database Provider
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

# Layer Responsibilities

## API Layer

Location:

```text
app/api/
```

Responsibilities:

- HTTP request handling
- Request validation
- Response serialization
- Dependency resolution

The API layer contains no business logic and performs no manual object construction.

---

## Dependency Layer

Location:

```text
app/dependencies/
```

Responsibilities:

- Database dependency providers
- Repository dependency providers
- Service dependency providers

This layer centralizes object creation and manages dependency relationships across the application.

---

## Service Layer

Location:

```text
app/services/
```

Responsibilities:

- Business logic
- Application use cases
- Coordination between layers

Services consume repositories through dependency injection and remain independent of database session management.

---

## Repository Layer

Location:

```text
app/repositories/
```

Responsibilities:

- Data access
- SQLAlchemy queries
- ORM persistence
- Transaction interaction

Repositories receive database sessions through dependency providers.

---

## Database Layer

Location:

```text
app/core/
```

Responsibilities:

- Engine configuration
- Session creation
- Database lifecycle management

Database session creation remains centralized through `get_db()`.

---

# Dependency Flow

The dependency graph introduced in v0.6.0 is:

```text
API Endpoint
      │
      ▼
get_incident_service()
      │
      ▼
get_incident_repository()
      │
      ▼
get_db()
      │
      ▼
AsyncSession
```

Each layer depends only on the layer directly beneath it.

---

# Request Lifecycle

```text
Client Request
      │
      ▼
Endpoint
      │
      ▼
Dependency Injection
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
Endpoint
      │
      ▼
Client Response
```

---

# Exception Flow

```text
Repository
      │
      ▼
Service
      │
      ▼
Domain Exception
      │
      ▼
Global Exception Handler
      │
      ▼
Standardized Error Response
```

---

# Current Foundations

Implemented architectural foundations:

- Repository Foundation
- Platform Operations Foundation
- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation

---

# Future Evolution

The current architecture prepares IncidentLab for future milestones including:

- Authentication
- Authorization
- Configuration Providers
- Background Tasks
- Event-Driven Processing
- Caching
- Observability
- Comprehensive Testing

Each future capability will build upon the existing layered architecture while preserving separation of concerns and centralized dependency management.
