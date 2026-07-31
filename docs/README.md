# IncidentLab Documentation

This directory contains the architectural and product documentation for IncidentLab.

Documentation evolves alongside each architectural milestone and reflects the current state of the project.

---

# Current Release

**v0.7.0 – Authentication Foundation**

This release introduces stateless JWT-based authentication, secure password hashing using Argon2, user authentication workflows, and protected API endpoints while extending the existing Dependency Injection Foundation.

---

# Documentation Index

## Architecture

- `architecture.md`

Describes the overall system architecture, layering, component interactions, authentication flow, and dependency graph.

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

## Release History

- `release-history.md`

Documents the engineering evolution of IncidentLab across each architectural milestone.

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
| ADR-002 | Layered Application Architecture | Accepted |
| ADR-003 | Global Exception Handling | Accepted |
| ADR-004 | Dependency Injection Foundation | Accepted |
| ADR-005 | Authentication Foundation | Accepted |

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
Requirements
      ↓
Architecture Decision Record (ADR)
      ↓
Implementation (Feature Branch)
      ↓
Testing
      ↓
Merge into main
      ↓
Documentation
      ↓
Release Tag
```

Documentation is updated only after implementation has been completed, reviewed, and merged into the main branch.
