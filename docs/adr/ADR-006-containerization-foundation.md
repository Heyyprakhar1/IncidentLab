# ADR-006: Containerization Foundation

- **Status:** Proposed
- **Date:** 2026-07-31
- **Version:** v0.8.0

---

# Context

IncidentLab has evolved into a layered backend platform with established architectural foundations including repository abstraction, persistence, exception handling, dependency injection, and authentication.

The application currently runs directly on the host operating system. While suitable for local development, this approach introduces inconsistencies across developer environments and does not reflect modern deployment practices.

As IncidentLab transitions into a DevOps and Platform Engineering learning project, the platform requires a standardized runtime environment that is portable, reproducible, and production-oriented.

Containerization will serve as the first DevOps foundation before introducing CI/CD, Infrastructure as Code, Kubernetes, Observability, and DevSecOps.

---

# Problem Statement

Running the application directly on the host machine creates several challenges:

- Environment-specific configuration
- Dependency inconsistencies
- Manual runtime setup
- Non-portable development environments
- Deployment complexity
- Differences between development and production systems

A standardized runtime environment is required to ensure the application behaves consistently regardless of where it is executed.

---

# Decision

IncidentLab will adopt Docker as the standard containerization platform.

Containerization assets will be maintained under the `infra/` directory because they represent deployment and runtime infrastructure rather than application business logic.

The initial implementation will focus on a **single development environment**.

Production optimizations, multi-environment support, orchestration, and Infrastructure as Code are intentionally deferred to future milestones.

---

# Initial Repository Layout

```text
IncidentLab/

├── apps/
│   └── api/
│
├── infra/
│   ├── compose.yaml
│   │
│   └── docker/
│       ├── Dockerfile
│       └── .dockerignore
│
├── docs/
├── scripts/
├── services/
└── tools/
```

---

# Architectural Principles

The Containerization Foundation follows these principles:

- Infrastructure separated from application code
- Reproducible runtime environments
- Single responsibility
- Incremental adoption
- Production-inspired design
- Environment consistency

---

# Scope

This milestone introduces:

- Docker fundamentals
- Docker image creation
- Docker container execution
- Docker Compose
- Application containerization
- PostgreSQL container integration
- Persistent volumes
- Container networking

---

# Out of Scope

The following capabilities are intentionally excluded from v0.8.0:

- Multi-environment configuration
- Kubernetes
- Helm
- Terraform
- CI/CD pipelines
- Container registry publishing
- Image signing
- Image vulnerability scanning
- Production deployment
- Container orchestration

These capabilities will be introduced in future architectural milestones.

---

# Future Evolution

The Containerization Foundation prepares IncidentLab for:

- CI/CD Foundation
- Infrastructure as Code
- Kubernetes Foundation
- Observability Foundation
- DevSecOps Foundation

Each future milestone will build upon the containerized application without requiring fundamental architectural changes.

---

# Implementation Plan

The Containerization Foundation will be implemented in the following order:

1. Containerization fundamentals
2. Docker runtime architecture
3. Dockerfile design
4. Image build process
5. Container execution
6. Docker Compose
7. PostgreSQL container integration
8. Persistent storage
9. Networking
10. Testing
11. Documentation
12. Release v0.8.0

---

# Related Components

- `infra/docker/`
- `infra/compose.yaml`
- `apps/api/`
- `docs/`
