# ADR-005: Authentication Foundation

- **Status:** Accepted
- **Date:** 2026-07-30
- **Version:** v0.7.0

---

# Context

IncidentLab currently exposes public API endpoints without any identity or authentication mechanism.

Previous architectural milestones established the foundational backend layers:

- Repository Foundation
- Platform Operations Foundation
- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation

With these foundations in place, the application is ready to introduce user authentication while preserving separation of concerns and maintaining a layered architecture.

Authentication should integrate naturally with the existing dependency injection system introduced in v0.6.0.

---

# Problem Statement

The application currently cannot:

- Identify users.
- Authenticate requests.
- Protect API endpoints.
- Associate resources with authenticated users.

A standardized authentication architecture is required before implementing authorization or role-based access control.

---

# Decision

IncidentLab will introduce a stateless authentication system based on JSON Web Tokens (JWT).

Authentication responsibilities will be isolated into a dedicated authentication module responsible for:

- Password hashing
- Password verification
- JWT generation
- JWT validation
- Current user resolution

Application endpoints will not perform authentication logic directly. Instead, authentication will be provided through FastAPI dependency injection.

---

# Architecture

```
                    Client
                       │
                       ▼
             POST /api/v1/auth/login
                       │
                       ▼
              Authentication Service
                       │
            Password Verification
                       │
                       ▼
                 JWT Generation
                       │
                       ▼
                Access Token
                       │
                       ▼
        Authorization: Bearer <JWT>
                       │
                       ▼
           get_current_user()
                       │
                       ▼
              Protected Endpoint
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

---

# Authentication Flow

1. Client submits email and password.
2. Credentials are validated.
3. Password hash is verified.
4. JWT access token is generated.
5. Client stores the access token.
6. Protected requests include the Bearer token.
7. Authentication dependency validates the token.
8. Authenticated user is injected into the endpoint.

---

# Directory Structure

```
app/
├── auth/
│   ├── hashing.py
│   ├── jwt.py
│   ├── security.py
│   └── dependencies.py
│
├── api/
│   └── v1/
│       └── endpoints/
│           └── auth.py
│
├── models/
│   └── user.py
│
├── repositories/
│   └── user.py
│
├── services/
│   └── user.py
│
└── schemas/
    └── user.py
```

---

# Authentication Components

## User Model

Stores application users.

Responsibilities:

- User identity
- Login credentials
- Account status

---

## Authentication Service

Responsible for:

- User authentication
- Password verification
- Token generation

No HTTP-specific logic.

---

## Authentication Dependencies

Provides reusable dependencies such as:

- `get_current_user()`
- `get_current_active_user()`

Endpoints consume these dependencies through FastAPI's dependency injection system.

---

## JWT Module

Responsible for:

- Token creation
- Token decoding
- Token validation

---

## Password Hashing Module

Responsible for:

- Password hashing
- Password verification

Passwords are never stored in plaintext.

---

# Guiding Principles

The Authentication Foundation follows:

- Stateless Authentication
- Separation of Concerns
- Dependency Injection
- Layered Architecture
- Single Responsibility Principle
- Secure Password Storage

---

# Consequences

## Benefits

- Centralized authentication logic.
- Reusable authentication dependencies.
- Secure password storage.
- Stateless authentication.
- Scalable architecture for future authorization features.

## Trade-offs

- Additional authentication layer increases implementation complexity.
- JWT revocation is not supported in this milestone.
- User management capabilities remain intentionally minimal.

---

# Out of Scope

The following capabilities are intentionally excluded from v0.7.0:

- Role-Based Access Control (RBAC)
- Permissions
- OAuth / Social Login
- Refresh Tokens
- Email Verification
- Password Reset
- Multi-Factor Authentication
- Session Management
- Audit Logging

These features will be introduced in future architectural milestones.

---

# Implementation Plan

The Authentication Foundation will be implemented in the following order:

1. User database model
2. Alembic migration
3. User schemas
4. User repository
5. User service
6. Password hashing
7. JWT utilities
8. Authentication service
9. Login endpoint
10. Authentication dependencies
11. Protected endpoints
12. Tests
13. Documentation
14. Release v0.7.0

---

# Related Components

- `app/auth/`
- `app/api/`
- `app/models/`
- `app/repositories/`
- `app/services/`
- `app/schemas/`
- `app/dependencies/`
