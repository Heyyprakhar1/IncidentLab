# Changelog

All notable changes to IncidentLab are documented in this file.

The project follows an incremental engineering approach where every release introduces one architectural capability while preserving maintainability, operational ownership, and documentation quality.

---

# Release History

## v0.5.0 — Error Handling Foundation

**Release Date:** TBD

### Added

- Global exception handling framework
- Centralized exception registration
- Custom application exception hierarchy
- `IncidentNotFoundException`
- Standardized `ErrorResponse` model
- `ErrorDetail` model
- Consistent API error responses
- Production-oriented API failure handling

### Improved

- Centralized HTTP error formatting
- Consistent error handling across application layers
- Improved API reliability and maintainability

### Documentation

- Updated project documentation for v0.5.0
- Added Architecture Decision Record for Global Exception Handling
- Updated engineering roadmap
- Updated architecture documentation

---

## v0.4.0 — Persistence Foundation

### Added

- SQLAlchemy ORM integration
- Repository layer
- Alembic migrations
- Database session management
- Incident creation workflow
- Incident listing workflow

### Improved

- Clear separation between business logic and persistence
- Foundation for future data operations

---

## v0.3.0 — API Foundation

### Added

- Versioned API routing
- Modular router composition
- Typed request schemas
- Typed response schemas
- Service layer architecture

### Improved

- Separation of HTTP handling from business logic
- Maintainable API structure

---

## v0.2.0 — Platform Operations Foundation

### Added

- Centralized logging
- HTTP request logging middleware
- Startup lifecycle logging
- Shutdown lifecycle logging
- Configurable log levels

### Improved

- Operational visibility
- Platform observability foundation

---

## v0.1.0 — Repository Foundation

### Added

- Initial repository structure
- FastAPI application bootstrap
- Environment-based configuration
- Health endpoint
- Initial engineering documentation

### Established

- Project vision
- Engineering principles
- Incremental development strategy

---

# Versioning Strategy

IncidentLab follows milestone-based versioning.

Each release represents a stable combination of:

- Source code
- Architecture
- Documentation
- Engineering decisions

New versions are released only after:

1. Feature implementation is complete.
2. Validation is successful.
3. Documentation is updated.
4. Architectural decisions are recorded (when applicable).
5. The release is tagged from the `main` branch.
