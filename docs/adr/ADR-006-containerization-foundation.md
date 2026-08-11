# ADR-006: Containerization Foundation

- **Status:** Accepted
- **Date:** 2026-07-31
- **Version:** v0.8.0

---

# Context

IncidentLab has evolved into a layered backend platform with established architectural foundations including repository abstraction, persistence, exception handling, dependency injection, and authentication.

The application previously ran directly on the host operating system. While suitable for local development, this approach introduced inconsistencies across developer environments and did not provide a standardized runtime boundary.

As IncidentLab transitions into a DevOps and Platform Engineering learning project, the platform requires a standardized runtime environment that is portable, reproducible, and production-oriented.

Containerization serves as the first DevOps foundation before introducing CI/CD, Infrastructure as Code, Kubernetes, Observability, and DevSecOps.

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

IncidentLab adopts Docker as the standard containerization platform.

The containerization implementation uses Dockerfiles for API image creation and Docker Compose for orchestrating the local API and PostgreSQL services.

The implementation intentionally maintains both:

- A conventional Dockerfile
- A multi-stage Dockerfile

The multi-stage implementation separates build-time dependency generation from the final runtime environment.

The v0.8.0 implementation focuses on a single local development environment.

Production orchestration, multi-environment deployment, Kubernetes, Infrastructure as Code, CI/CD, and registry-based deployment are deferred to future milestones.

---

# Repository Layout

The implemented containerization structure is:

```text
IncidentLab/

├── apps/
│   └── api/
│       ├── Dockerfile
│       └── Dockerfile.multistage
│
├── compose.yaml
│
├── docs/
│   └── ...
│
├── engineering-notes/
│   └── v0.8-containerization-foundation/
│
└── ...
```

The API Dockerfiles are maintained alongside the API application because they define the runtime environment for that application.

The Compose definition is maintained at the repository root because it orchestrates multiple services belonging to the project.

---

# Architectural Principles

The Containerization Foundation follows these principles:

- Reproducible runtime environments
- Separation of build and runtime responsibilities
- Least-privilege container execution
- Single responsibility
- Incremental adoption
- Production-inspired design
- Environment consistency
- Layer and build-cache awareness
- Persistent data separation
- Application-level health verification

---

# Scope

This milestone introduces:

- Docker fundamentals
- Docker image creation
- Docker container execution
- Production-oriented Dockerfile design
- Multi-stage Docker builds
- Docker Compose
- FastAPI application containerization
- PostgreSQL container integration
- Persistent PostgreSQL storage
- Container networking
- Non-root runtime execution
- Docker healthchecks
- Runtime dependency isolation
- Docker image inspection and optimization
- Container validation

---

# Container Runtime Architecture

The API runs inside a dedicated Docker container.

The runtime architecture is:

```text
Docker Host
     │
     ▼
Docker Engine
     │
     ▼
IncidentLab API Container
     │
     ├── Python 3.12
     ├── Application
     ├── .venv
     ├── Uvicorn
     └── incidentlab user
```

The application listens on port:

```text
8000
```

The container runs the application using Uvicorn.

The runtime user is:

```text
incidentlab
```

The application therefore does not run as root.

---

# Multi-Stage Build Architecture

The multi-stage Dockerfile separates build-time responsibilities from runtime responsibilities.

```text
Builder Stage
     │
     ├── Python
     ├── uv
     ├── curl
     ├── pyproject.toml
     └── uv.lock
     │
     ▼
   uv sync
     │
     ▼
 /app/.venv
     │
     ▼
Runtime Stage
     │
     ├── Python
     ├── .venv
     ├── Application Source
     ├── Uvicorn
     └── incidentlab user
```

The builder generates the application's Python virtual environment.

The runtime stage receives the `.venv` artifact and application source.

Build-time utilities are therefore not required for normal application execution.

---

# Runtime Artifact Ownership

Runtime artifacts are copied with the correct ownership during the copy operation.

Example:

```dockerfile
COPY --from=builder \
    --chown=incidentlab:incidentlab \
    /app/.venv /app/.venv
```

Application source is similarly copied with explicit ownership:

```dockerfile
COPY --chown=incidentlab:incidentlab . .
```

This avoids requiring a later recursive ownership operation.

---

# Docker Compose Architecture

Docker Compose provides the local multi-container runtime.

The stack contains:

```text
Docker Compose
     │
     ├───────────────┐
     ▼               ▼
    API              DB
Container        PostgreSQL
     │               │
     │               ▼
     │        Persistent Volume
     │
     ▼
 Healthcheck
```

The API and PostgreSQL services communicate through the Compose network.

The API is published to the host on port `8000`.

PostgreSQL remains an internal service of the Compose stack.

---

# Persistent Storage

PostgreSQL uses persistent storage through the named volume:

```text
incidentlab_postgres_data
```

The volume separates database data from the lifecycle of the PostgreSQL container.

The relationship is:

```text
PostgreSQL Container
        │
        ▼
incidentlab_postgres_data
        │
        ▼
Persistent Database Data
```

This allows the database container to be recreated without automatically discarding its stored data.

---

# Health Monitoring

The API includes a Docker healthcheck based on the application's health endpoint.

The health endpoint is:

```text
GET /api/v1/health
```

The architecture distinguishes between:

```text
Container Running
       ≠
Application Healthy
```

A running container only confirms that the container process is active.

The healthcheck provides an application-level signal that the API is responding correctly.

---

# Image Optimization

Docker image layers were inspected during the implementation using:

```bash
docker history incidentlab-api:multistage
```

The initial multi-stage implementation contained an unnecessary ownership layer caused by a recursive `chown` operation.

The problematic pattern was:

```text
COPY /app/.venv
       │
       ▼
Large filesystem layer
       │
       ▼
RUN chown -R ...
       │
       ▼
Another large filesystem layer
```

The ownership operation was replaced with `COPY --chown`.

This reduced the resulting API image from approximately:

```text
265 MB
```

to:

```text
192 MB
```

The optimization demonstrated that multi-stage builds alone do not guarantee minimal image size.

Docker layer behavior and filesystem operations must also be considered.

---

# Validation

The containerization implementation was validated through:

1. Docker image build
2. Standalone container startup
3. Docker healthcheck validation
4. API health endpoint validation
5. Non-root user verification
6. Runtime Python executable verification
7. Runtime dependency verification
8. Docker Compose startup
9. PostgreSQL health verification
10. API log inspection
11. PostgreSQL log inspection
12. Docker image history inspection

The standalone multi-stage image successfully reached:

```text
healthy
```

and the API health endpoint returned HTTP 200.

The complete Docker Compose stack also started successfully with healthy API and PostgreSQL services.

---

# Scope Boundaries

The v0.8.0 milestone establishes the container runtime foundation.

The following capabilities remain outside this milestone:

- Multi-environment deployment
- Kubernetes
- Helm
- Terraform
- CI/CD pipelines
- Container registry publishing
- Image signing
- Production deployment
- Full container orchestration
- Cloud deployment
- Production secrets management

These capabilities will be introduced through future architectural milestones.

---

# Consequences

## Positive Consequences

Containerization provides:

- Reproducible runtime environments
- Consistent application execution
- Isolated application dependencies
- Standardized local development
- Container health monitoring
- Persistent database storage
- Non-root runtime execution
- A foundation for CI/CD
- A foundation for Kubernetes
- A foundation for DevSecOps

The multi-stage implementation also separates build-time tooling from runtime responsibilities.

---

## Trade-offs

Containerization introduces additional complexity:

- Docker is required for the containerized workflow.
- Developers must understand image and container lifecycle.
- Docker Compose adds orchestration configuration.
- Persistent volumes require lifecycle awareness.
- Image optimization requires understanding Docker layers and caching.

These trade-offs are accepted because the project is intentionally designed to develop production-oriented engineering practices.

---

# Implementation Status

The Containerization Foundation has been implemented and validated.

The implementation includes:

```text
apps/api/Dockerfile
apps/api/Dockerfile.multistage
compose.yaml
```

The feature was developed on:

```text
feature/containerization-foundation
```

and merged into:

```text
main
```

using a fast-forward merge.

The working tree was verified clean after integration.

---

# Future Evolution

The Containerization Foundation prepares IncidentLab for:

- CI/CD Foundation
- Infrastructure as Code
- Kubernetes Foundation
- Observability Foundation
- DevSecOps Foundation
- Authorization (RBAC)

Each future milestone will build upon the containerized application without requiring fundamental changes to the existing layered application architecture.

---

# Related Components

- `apps/api/Dockerfile`
- `apps/api/Dockerfile.multistage`
- `compose.yaml`
- `apps/api/`
- `docs/architecture.md`
- `engineering-notes/v0.8-containerization-foundation/`
