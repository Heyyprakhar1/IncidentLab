# System Architecture

IncidentLab follows a layered architecture that emphasizes separation of concerns, maintainability, and incremental architectural evolution.

Beginning with **v0.7.0 – Authentication Foundation**, the architecture introduces a dedicated authentication layer built on top of the Dependency Injection Foundation. Authentication is implemented using stateless JSON Web Tokens (JWT) and integrates seamlessly with FastAPI's dependency injection system.

---

# Architectural Principles

The project follows these principles:

- Separation of Concerns
- Single Responsibility Principle
- Dependency Injection
- Repository Pattern
- Layered Architecture
- Stateless Authentication
- Incremental Evolution
- Production-Inspired Design

---

# High-Level Architecture

```text
                  Client
                     │
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

## Authentication Layer

Location:

```text
app/auth/
app/dependencies/auth.py
```

Responsibilities:

- Password hashing
- Password verification
- JWT generation
- JWT validation
- Current user resolution

Authentication is implemented using HTTP Bearer tokens and integrated through FastAPI dependency injection.

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
- Authentication dependency providers

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
- User authentication
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

Authentication requests follow the dependency graph below:

```text
Protected Endpoint
        │
        ▼
get_current_user()
        │
        ▼
decode_access_token()
        │
        ▼
get_user_repository()
        │
        ▼
get_db()
        │
        ▼
AsyncSession
```

Application services continue to follow:

```text
API Endpoint
      │
      ▼
get_service()
      │
      ▼
get_repository()
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
Authentication
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
- Authentication Foundation

---

# Future Evolution

The current architecture prepares IncidentLab for future milestones including:

- Containerization
- CI/CD
- Infrastructure as Code
- Kubernetes
- Observability
- DevSecOps
- Authorization (RBAC)

Each future capability will build upon the existing layered architecture while preserving separation of concerns, centralized dependency management, and a secure authentication model.
