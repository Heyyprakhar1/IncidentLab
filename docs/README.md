# IncidentLab Documentation

This directory contains the engineering documentation for IncidentLab.

Each document has a defined responsibility and explains one specific aspect of the platform — from product vision and architecture decisions to implementation evolution and engineering roadmap.

The documentation is maintained alongside the source code and represents the current stable state of the `main` branch.

---

# Documentation Structure

| Document                                           | Purpose                                                                                  |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [vision.md](vision.md)                             | Explains why IncidentLab exists and the long-term platform vision.                       |
| [product-requirements.md](product-requirements.md) | Defines product objectives, functional scope, and engineering requirements.              |
| [architecture.md](architecture.md)                 | Describes the current system architecture, design principles, and application structure. |
| [roadmap.md](roadmap.md)                           | Tracks completed milestones and future engineering capabilities.                         |
| [release-history.md](release-history.md)           | Records platform releases and architectural evolution.                                   |
| [adr/](adr/)                                       | Contains Architecture Decision Records explaining important technical decisions.         |

---

# Documentation Principles

The documentation follows several principles to remain useful as IncidentLab evolves.

---

## Single Responsibility

Each document answers one specific question.

Examples:

* Vision → Why does IncidentLab exist?
* Product Requirements → What should the platform achieve?
* Architecture → How is the platform structured?
* Roadmap → How will the platform evolve?
* ADRs → Why were important decisions made?

Information should have one primary location instead of being duplicated across multiple documents.

---

## Current State First

Documentation reflects the latest stable implementation available on the `main` branch.

Experimental changes inside feature branches are intentionally excluded until they become part of an official release.

This keeps documentation aligned with the actual platform state.

---

## Architecture Over Implementation

Documentation explains architectural decisions and system boundaries.

Implementation details remain inside the source code.

Examples:

Architecture documentation explains:

* Layer responsibilities
* Component boundaries
* Design decisions
* System evolution

Source code explains:

* Functions
* Classes
* Internal implementation details

---

## Incremental Evolution

IncidentLab evolves through small engineering milestones.

Each milestone introduces a focused capability while preserving:

* Maintainability
* Clear ownership
* Operational quality
* Architectural consistency

Documentation evolves together with every stable platform milestone.

---

# Current Platform State

Current release:

**v0.3.0 — API Foundation**

The platform currently includes:

## Application Foundation

* FastAPI application bootstrap
* Typed configuration
* Environment-based settings
* Lifecycle management
* Health endpoint

---

## Platform Operations Foundation

* Centralized logging
* Startup lifecycle logging
* Shutdown lifecycle logging
* HTTP request logging middleware
* Configurable logging levels

---

## API Foundation

* Versioned API routing
* Modular router composition
* Request schemas
* Response schemas
* Service layer architecture
* Separation of HTTP and business logic

---

## Persistence Foundation

* SQLAlchemy ORM integration
* Database models
* Alembic migrations
* Repository layer
* Database session management
* Incident creation workflow
* Incident listing workflow

---

# Documentation Lifecycle

Every engineering milestone follows the same workflow:

```text
Feature Development
        │
        ▼
Code Review
        │
        ▼
Integration Validation
        │
        ▼
Merge into main
        │
        ▼
Documentation Update
        │
        ▼
Release Tag
```

Documentation is updated only after implementation becomes part of the stable `main` branch.

This ensures that published documentation represents the official platform state.

---

# Architecture Decision Records

Architectural decisions are documented separately using ADRs.

ADRs capture:

* Context behind decisions
* Alternatives considered
* Technical trade-offs
* Long-term impact

Current decisions:

| ADR     | Decision                         |
| ------- | -------------------------------- |
| ADR-001 | Monorepo Strategy                |
| ADR-002 | Layered Application Architecture |

---

# Versioning

Documentation is versioned together with the source code.

Each release represents a stable combination of:

* Source code
* Architecture
* Documentation
* Engineering decisions

Current documentation version:

**v0.3.0**

---

# Contribution Workflow

When introducing a new capability:

1. Create a dedicated feature branch.
2. Implement the required changes.
3. Validate the implementation.
4. Merge the feature into the stable development flow.
5. Merge into `main`.
6. Update documentation.
7. Create a release tag.

This workflow ensures that implementation and documentation remain synchronized.

---

# Documentation Philosophy

IncidentLab treats documentation as part of engineering, not as an afterthought.

A capability is considered complete only when:

* The implementation exists.
* The architecture is understood.
* The decision-making process is documented.
* The roadmap reflects the new capability.

The objective is to build a platform that remains understandable as it grows.

