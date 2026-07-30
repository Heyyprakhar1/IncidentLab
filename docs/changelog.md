# Changelog

All notable architectural changes to IncidentLab are documented in this file.

IncidentLab follows a milestone-driven release model where each version introduces a single foundational capability while preserving existing application behavior.

---

# v0.6.0 — Dependency Injection Foundation

**Release Date:** 2026-07-30

## Added

- Introduced a dedicated dependency provider layer.
- Added repository dependency providers.
- Added service dependency providers.
- Added database dependency re-export provider.
- Added ADR-004 documenting the Dependency Injection architecture.

## Changed

- API endpoints now receive services through FastAPI dependency injection.
- Services now receive repositories through dependency injection.
- Repository construction has been centralized.
- Object creation responsibilities have been removed from business components.

## Improved

- Reduced coupling between API, service, and repository layers.
- Improved separation of concerns.
- Established a scalable dependency graph for future features.
- Preserved application behavior while improving internal architecture.

---

# v0.5.0 — Error Handling Foundation

## Added

- Global exception handling.
- Standardized API error responses.
- Custom domain exceptions.
- Centralized exception handlers.

## Improved

- Consistent error responses.
- Cleaner controller logic.
- Better separation of concerns.

---

# v0.4.0 — Persistence Foundation

## Added

- SQLAlchemy Async ORM.
- Alembic migrations.
- Repository pattern.
- PostgreSQL persistence layer.

---

# v0.3.0 — API Foundation

## Added

- FastAPI application bootstrap.
- Versioned API routing.
- Request logging middleware.
- Structured application lifecycle.

---

# v0.2.0 — Platform Operations Foundation

## Added

- Containerized development environment.
- Docker support.
- Environment configuration.
- Initial project structure.

---

# v0.1.0 — Repository Foundation

## Added

- Initial repository.
- Documentation structure.
- Project vision.
- Development roadmap.

---

# Versioning Strategy

IncidentLab follows milestone-based versioning.

Each release introduces one architectural capability, validates its implementation, updates documentation, and creates a tagged release before moving to the next milestone.
