# Changelog

All notable changes to IncidentLab are documented in this file.

The project follows an architecture-first, milestone-driven development approach. Each release introduces a single foundational capability while maintaining backward compatibility and a clean layered architecture.

---

# v0.7.0 — Authentication Foundation

**Release Date:** 2026-07-30

## Added

### Authentication

- JWT-based authentication
- User registration endpoint
- User login endpoint
- Authenticated user endpoint (`/auth/me`)
- HTTP Bearer authentication
- Current user dependency injection

### User Management

- User database model
- User repository
- Authentication service
- Authentication schemas

### Security

- Password hashing using Argon2
- JWT access token generation
- JWT validation
- Protected incident endpoints

### Infrastructure

- Authentication dependency providers
- Authentication module
- Database migration for users table

---

## Changed

- Incident APIs now require authentication.
- Dependency Injection layer extended to support authentication services.
- Project architecture now includes an Authentication Foundation.

---

## Security

- Passwords are securely hashed before storage.
- Plaintext passwords are never persisted.
- Protected endpoints return `401 Unauthorized` for unauthenticated requests.
- JWT secret is loaded from application configuration.

---

# v0.6.0 — Dependency Injection Foundation

Introduced centralized dependency injection for repositories and services, improving modularity, testability, and separation of concerns.

---

# v0.5.0 — Error Handling Foundation

Introduced centralized exception handling with standardized API error responses and domain-specific exception management.

---

# v0.4.0 — Persistence Foundation

Introduced SQLAlchemy Async ORM, Alembic migrations, PostgreSQL integration, and the Repository pattern.

---

# v0.3.0 — API Foundation

Established FastAPI application structure, versioned routing, middleware, and request lifecycle management.

---

# v0.2.0 — Platform Operations Foundation

Established the operational project structure and backend platform organization.

---

# v0.1.0 — Repository Foundation

Introduced the Repository pattern as the first architectural foundation of IncidentLab.
