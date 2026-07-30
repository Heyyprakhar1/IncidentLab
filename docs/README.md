# IncidentLab Documentation

This directory contains the architectural and product documentation for IncidentLab.

Documentation evolves alongside each architectural milestone and reflects the current state of the project.

---

# Current Release

**v0.6.0 – Dependency Injection Foundation**

This release introduces centralized dependency management using FastAPI's dependency injection system, improving separation of concerns and reducing coupling between application layers.

---

# Documentation Index

## Architecture

- `architecture.md`

Describes the overall system architecture, layering, component interactions, and dependency flow.

---

## Product Requirements

- `product-requirements.md`

Defines the long-term vision, functional goals, and planned platform capabilities.

---

## Roadmap

- `roadmap.md`

Tracks completed architectural milestones and future development phases.

---

## Changelog

- `changelog.md`

Records milestone-based release history.

---

## Architecture Decision Records (ADR)

Located in:

```text
docs/adr/
```

Current ADRs:

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | Repository Foundation | Accepted |
| ADR-002 | Persistence Foundation | Accepted |
| ADR-003 | Global Exception Handling | Accepted |
| ADR-004 | Dependency Injection Foundation | Accepted |

---

# Documentation Principles

IncidentLab documentation follows these principles:

- Architecture-first
- Incremental evolution
- Production-inspired design
- Single source of truth
- Milestone-driven documentation

---

# Repository Workflow

Every architectural milestone follows:

```text
ADR
    ↓
Implementation
    ↓
Architecture Review
    ↓
Documentation
    ↓
Release
```

Documentation is updated only after implementation has been completed and verified.
