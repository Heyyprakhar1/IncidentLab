# IncidentLab Documentation

This directory contains the engineering documentation for IncidentLab.

Each document has a single responsibility and answers one specific question about the platform. Together, these documents describe the project's vision, architecture, implementation approach, and engineering roadmap.

The documentation is maintained alongside the source code and reflects the current state of the `main` branch.

---

# Documentation Structure

| Document | Purpose |
|----------|---------|
| [vision.md](vision.md) | Explains why IncidentLab exists and the long-term vision of the platform. |
| [product-requirements.md](product-requirements.md) | Defines the product scope, functional goals, and engineering requirements. |
| [architecture.md](architecture.md) | Describes the current system architecture, design principles, and application structure. |
| [roadmap.md](roadmap.md) | Tracks completed milestones and planned engineering sprints. |
| [release-history.md](release-history.md) | Records platform releases and the capabilities introduced in each version. |

---

# Documentation Principles

The documentation follows a few guiding principles to remain useful as the platform evolves.

## Single Responsibility

Each document focuses on one topic.

Concepts should be documented once and referenced where appropriate instead of being duplicated across multiple files.

---

## Current State First

Documentation always reflects the latest stable implementation available on the `main` branch.

Experimental work in feature branches is intentionally excluded until it becomes part of an official release.

---

## Architecture Over Implementation

The documentation explains **why** the platform is designed the way it is before explaining **how** it is implemented.

Implementation details belong in the source code.

Architectural decisions belong in the documentation.

---

## Incremental Evolution

IncidentLab is developed through small engineering milestones.

As new capabilities are introduced, the documentation evolves alongside the platform while preserving a consistent structure.

---

# Documentation Lifecycle

Every engineering sprint follows the same documentation workflow.

```text
Feature Development
        │
        ▼
Code Review
        │
        ▼
Merge into develop
        │
        ▼
Validation
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

Documentation is updated only after implementation has been merged into the `main` branch.

This ensures that every published document accurately reflects the official project state.

---

# Versioning

Documentation is versioned together with the source code.

Every tagged release represents a stable combination of:

- Source code
- Engineering documentation
- Architecture
- Project roadmap

Current documentation version:

**v0.3.0**

---

# Contributing

When introducing a new architectural capability:

1. Implement the feature in a dedicated feature branch.
2. Merge the implementation into `develop`.
3. Validate the integration.
4. Merge into `main`.
5. Update the relevant documentation.
6. Create a new release tag.

Following this workflow ensures that code and documentation remain synchronized throughout the evolution of the platform.
