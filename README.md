# IncidentLab

A production-inspired backend platform for learning modern backend engineering through incremental architectural evolution.

Rather than building features first, IncidentLab focuses on establishing strong engineering foundations—including API design, persistence, dependency injection, authentication, exception handling, containerization, and future production capabilities.

---

# Why IncidentLab Exists

IncidentLab demonstrates how backend systems evolve over time through small, well-defined architectural milestones.

Each release introduces a single foundational capability while preserving existing behavior and maintaining a clean architecture.

The project follows an architecture-first approach where implementation decisions are documented, tested, and integrated incrementally.

---

# Current Release

**v0.8.0 — Containerization Foundation**

Current architectural foundations:

- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation
- Authentication Foundation
- Containerization Foundation

---

# Implemented Foundations

## API Foundation

- FastAPI application bootstrap
- Versioned API routing
- Request lifecycle management
- Structured logging middleware

---

## Persistence Foundation

- SQLAlchemy Async ORM
- Alembic migrations
- Repository pattern
- PostgreSQL integration

---

## Error Handling Foundation

- Global exception handling
- Standardized API error responses
- Domain-specific exceptions
- Centralized error management

---

## Dependency Injection Foundation

- Dedicated dependency provider layer
- Repository dependency providers
- Service dependency providers
- Centralized object construction
- Improved separation of concerns
- FastAPI dependency injection

---

## Authentication Foundation

- JWT-based authentication
- User registration
- User login
- Password hashing using Argon2
- HTTP Bearer authentication
- Protected API endpoints
- Current user dependency injection

---

## Containerization Foundation

IncidentLab is now containerized using Docker.

The API can run as an isolated container with:

- Python 3.12 slim base image
- Non-root runtime user
- Explicit application working directory
- Production-oriented Dockerfile
- Multi-stage Docker build
- Runtime dependency isolation
- Docker healthcheck
- Uvicorn-based application startup
- Docker Compose integration

The containerized stack consists of:

```text
IncidentLab
     │
     ▼
Docker Compose
     │
     ├───────────────┐
     ▼               ▼
FastAPI API      PostgreSQL
Container        Container
     │               │
     │               ▼
     │        Persistent Volume
     │
     ▼
Healthcheck
```

The API container is built using:

```text
apps/api/
├── Dockerfile
└── Dockerfile.multistage
```

The multi-stage Dockerfile is maintained as an alternative implementation to the conventional Dockerfile.

---

# Container Runtime

The API runtime uses a dedicated non-root user:

```text
incidentlab
```

The application listens on:

```text
8000
```

The runtime command is composed using:

```dockerfile
ENTRYPOINT ["uvicorn"]
```

with default arguments defined through `CMD`.

Conceptually:

```text
uvicorn
   +
app.main:app
   +
--host 0.0.0.0
   +
--port 8000
```

The container also includes an application healthcheck based on the API health endpoint.

---

# Multi-Stage Container Build

IncidentLab includes a multi-stage Docker build that separates build-time responsibilities from runtime responsibilities.

```text
Builder Stage
     │
     ├── uv
     ├── build dependencies
     ├── pyproject.toml
     ├── uv.lock
     │
     ▼
   /app/.venv
     │
     │ selected runtime artifact
     ▼
Runtime Stage
     │
     ├── .venv
     ├── application source
     ├── uvicorn
     └── incidentlab user
```

The builder generates the Python virtual environment using the project's dependency definitions.

The runtime stage receives the required runtime artifact rather than the complete builder environment.

Build-time utilities such as `uv` and `curl` are therefore not required as runtime application dependencies.

---

# Docker Compose

The development stack is orchestrated using Docker Compose.

The current Compose stack includes:

```text
services:

  api
   │
   └── IncidentLab FastAPI application

  db
   │
   └── PostgreSQL 16
```

PostgreSQL uses a persistent named volume:

```text
incidentlab_postgres_data
```

This allows database data to persist independently from the PostgreSQL container lifecycle.

---

# High-Level Architecture

```text
                         Client
                            │
                            ▼
                    Docker Host :8000
                            │
                            ▼
                  ┌───────────────────┐
                  │   IncidentLab API │
                  │     Container     │
                  │                   │
                  │      Uvicorn      │
                  │         │         │
                  │      FastAPI      │
                  │         │         │
                  │ Authentication    │
                  │         │         │
                  │ Dependency Layer  │
                  │         │         │
                  │ Application       │
                  │ Services          │
                  │         │         │
                  │ Repository Layer  │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    PostgreSQL     │
                  │     Container     │
                  └─────────┬─────────┘
                            │
                            ▼
                  incidentlab_postgres_data
```

The containerization layer surrounds the existing application architecture rather than replacing it.

The application remains internally organized using layered architecture.

---

# Application Architecture

Inside the API container, the application follows the existing layered design:

```text
                  Client
                     │
                     ▼
      Authorization: Bearer <JWT>
                     │
                     ▼
             FastAPI Endpoints
                     │
                     ▼
      Authentication Dependency
                     │
                     ▼
       Dependency Injection Layer
          ┌──────────┴──────────┐
          ▼                     ▼
 Application Services     Database Provider
          │
          ▼
     Repository Layer
          │
          ▼
     SQLAlchemy Async ORM
          │
          ▼
        PostgreSQL
```

Containerization provides the runtime boundary around this application architecture.

---

# Repository Structure

```text
IncidentLab/
│
├── apps/
│   └── api/
│       ├── app/
│       │   ├── api/
│       │   ├── auth/
│       │   ├── core/
│       │   ├── db/
│       │   ├── dependencies/
│       │   ├── exceptions/
│       │   ├── middleware/
│       │   ├── models/
│       │   ├── repositories/
│       │   ├── schemas/
│       │   └── services/
│       │
│       ├── migrations/
│       ├── tests/
│       ├── Dockerfile
│       └── Dockerfile.multistage
│
├── docs/
│   ├── adr/
│   ├── architecture.md
│   ├── changelog.md
│   ├── product-requirements.md
│   └── roadmap.md
│
├── compose.yaml
└── ...
```
# API Endpoints

## Health

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| GET    | `/api/v1/health` | Application health check |

## Authentication

| Method | Endpoint                | Description                       |
| ------ | ----------------------- | --------------------------------- |
| POST   | `/api/v1/auth/register` | Register a new user               |
| POST   | `/api/v1/auth/login`    | Authenticate user and receive JWT |
| GET    | `/api/v1/auth/me`       | Retrieve authenticated user       |

## Incidents

| Method | Endpoint                 | Description                                         |
| ------ | ------------------------ | --------------------------------------------------- |
| POST   | `/api/v1/incidents`      | Create incident *(Authentication Required)*         |
| GET    | `/api/v1/incidents`      | List incidents *(Authentication Required)*          |
| GET    | `/api/v1/incidents/{id}` | Retrieve incident by ID *(Authentication Required)* |

---

# Technology Stack

## Application

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Pydantic v2
- PyJWT
- pwdlib (Argon2)
- Uvicorn

## Containerization

- Docker
- Docker Compose
- Python 3.12 slim
- uv
- Multi-stage Docker builds
- Docker Healthcheck

---

# Running IncidentLab

## Run the API Directly

The API can still be executed directly during application development using the project's Python environment.

---

## Run with Docker Compose

Build and start the complete containerized stack:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

The expected services are:

```text
incidentlab-api
incidentlab-db
```

Check API logs:

```bash
docker compose logs api
```

Check database logs:

```bash
docker compose logs db
```

---

# Health Verification

The API exposes a health endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "IncidentLab API",
  "version": "0.7.0",
  "environment": "development"
}
```

Docker also monitors the application through its configured healthcheck.

A running container and a healthy application are treated as separate operational states.

---

# Docker Image

The multi-stage API Image can be built directly with:

```bash
docker build \
  -f apps/api/Dockerfile.multistage \
  -t incidentlab-api:multistage \
  apps/api
```

The resulting runtime Image contains the application and required runtime dependencies without carrying the complete builder environment.

---

# Runtime Security

The API container does not run the application as root.

The runtime user is:

```text
incidentlab
```

This follows the principle of least privilege and reduces unnecessary container runtime privileges.

The runtime environment also avoids requiring build-time utilities such as `uv` and `curl` during normal application execution.

---

# Container Development Workflow

Containerization follows the project's architecture-first development workflow:

```text
Requirements
     │
     ▼
Architecture Decision Record
     │
     ▼
Implementation
     │
     ▼
Feature Branch
     │
     ▼
Docker Build
     │
     ▼
Container Validation
     │
     ▼
Compose Integration
     │
     ▼
Testing
     │
     ▼
Documentation
     │
     ▼
Merge into main
     │
     ▼
Release Tag
```

---

# Docker Validation

The containerization milestone was validated through:

- Successful Docker Image build
- Successful standalone container startup
- Docker healthcheck transition to `healthy`
- API health endpoint returning HTTP 200
- Runtime user verification
- Runtime Python executable verification
- Runtime dependency verification
- Docker Compose startup
- PostgreSQL health verification
- API and PostgreSQL log inspection

The standalone multi-stage Image was tested using:

```bash
docker run -d \
  --name incidentlab-multistage-test \
  -p 8001:8000 \
  incidentlab-api:multistage
```

The container transitioned from:

```text
health: starting
```

to:

```text
healthy
```

The API was then verified independently:

```bash
curl http://localhost:8001/api/v1/health
```

The response confirmed:

```json
{
  "status": "healthy",
  "service": "IncidentLab API",
  "version": "0.7.0",
  "environment": "development"
}
```

The runtime user was verified with:

```bash
docker exec incidentlab-multistage-test whoami
```

Result:

```text
incidentlab
```

The runtime executable path was also verified:

```bash
docker exec incidentlab-multistage-test \
  sh -c 'which uv || true; which curl || true; which uvicorn'
```

Result:

```text
/app/.venv/bin/uvicorn
```

This confirmed that `uv` and `curl` were not required in the runtime environment while `uvicorn` was available through the application's virtual environment.

The Python executable was verified with:

```bash
docker exec incidentlab-multistage-test \
  python -c "import sys; print(sys.executable)"
```

Result:

```text
/app/.venv/bin/python
```

---

# Docker Compose Validation

The complete stack was validated using:

```bash
docker compose up -d --build
```

The resulting stack contained:

```text
incidentlab-api-1
incidentlab-db-1
```

Both containers reached a healthy state.

The API logs confirmed successful startup:

```text
Started server process
Waiting for application startup
Application startup complete
Uvicorn running on http://0.0.0.0:8000
GET /api/v1/health HTTP/1.1" 200 OK
```

The PostgreSQL logs confirmed:

```text
database system is ready to accept connections
```

This validated the multi-stage API Image as part of the actual IncidentLab Compose stack rather than only as an isolated container.

---

# Docker Image Optimization

During the multi-stage implementation, Image layers were inspected using:

```bash
docker history incidentlab-api:multistage
```

The first implementation showed an unnecessary large ownership layer.

The problematic flow was conceptually:

```text
COPY /app/.venv
       │
       ▼
~72.7 MB layer
       │
       ▼
RUN chown -R ...
       │
       ▼
Another ~72.7 MB layer
```

The problem was not the size of `.venv` itself.

The problem was that a recursive ownership change created another large filesystem layer.

The runtime implementation was changed to establish ownership during the copy operation:

```dockerfile
COPY --from=builder \
    --chown=incidentlab:incidentlab \
    /app/.venv /app/.venv
```

and:

```dockerfile
COPY --chown=incidentlab:incidentlab . .
```

The unnecessary recursive `chown` operation was removed.

The resulting Image size decreased from approximately:

```text
265 MB
```

to:

```text
192 MB
```

This demonstrated that multi-stage builds alone do not guarantee minimal Image size.

Understanding Docker filesystem layers and build behavior remains essential for optimization.

---

# Docker Cleanup

After the implementation was merged and pushed, temporary Docker resources were cleaned carefully.

The final application Image was retained:

```text
incidentlab-api:latest
```

The PostgreSQL Image was retained:

```text
postgres:16
```

The persistent PostgreSQL volume was retained:

```text
incidentlab_postgres_data
```

Temporary anonymous volumes were inspected before removal.

Unused BuildKit cache was cleaned using:

```bash
docker builder prune
```

Approximately 3.12 GB of unused builder cache was reclaimed.

Default Docker networks were preserved:

```text
bridge
host
none
```

The goal was to remove temporary build/test resources without deleting application Images or persistent database data.

---

# Git Integration

The containerization implementation was developed on the feature branch:

```text
feature/containerization-foundation
```

The completed implementation was merged into `main` using a fast-forward merge:

```text
750e686
   ↓
1e88ffe
```

The merge introduced:

```text
apps/api/Dockerfile.multistage
compose.yaml
```

The updated `main` branch was then pushed to the remote repository.

After successful verification, the feature branch was removed both locally and remotely.

Final Git state:

```text
main
develop
origin/main
origin/develop
```

The working tree was clean after the merge and push.

---

# Containerization Milestone Outcome

The v0.8 containerization milestone established a reproducible local container runtime for IncidentLab.

The milestone now provides:

```text
Dockerfile
     │
     ├── Conventional single-stage build
     │
     └── Multi-stage build
              │
              ▼
         Runtime Image
              │
              ▼
       Docker Compose
          ┌───┴───┐
          ▼       ▼
         API      DB
          │       │
          │       ▼
          │   Persistent Data
          │
          ▼
      Healthcheck
```

The implementation was built, executed, inspected, optimized, integrated with Compose, validated, merged, pushed, and cleaned.

---

# Current Architecture Foundations

Implemented architectural foundations:

- Repository Foundation
- Platform Operations Foundation
- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation
- Authentication Foundation
- Containerization Foundation

---

# Roadmap

## Completed

- Repository Foundation
- Platform Operations Foundation
- API Foundation
- Persistence Foundation
- Error Handling Foundation
- Dependency Injection Foundation
- Authentication Foundation
- Containerization Foundation

## Upcoming

- CI/CD Foundation
- Infrastructure as Code
- Kubernetes
- Observability
- DevSecOps
- Authorization (RBAC)

Containerization establishes the runtime foundation for the upcoming CI/CD, Infrastructure as Code, Kubernetes, and DevSecOps milestones.

---

# Documentation

Project documentation is available under the `docs/` directory.

Key documents include:

- Architecture
- Product Requirements
- Roadmap
- ADRs
- Changelog
- Release History

Engineering learning notes are maintained separately under:

```text
engineering-notes/
```

---

# Development Workflow

Each release follows an architecture-first workflow:

1. Requirements
2. Architecture Decision Record (ADR)
3. Implementation (Feature Branch)
4. Testing
5. Merge into `main`
6. Documentation
7. Release Tag

Each milestone is expected to leave the repository in a clean and reproducible state before the next architectural capability begins.

---

# Release History

| Version | Milestone                       |
| ------- | ------------------------------- |
| v0.8.0  | Containerization Foundation     |
| v0.7.0  | Authentication Foundation       |
| v0.6.0  | Dependency Injection Foundation |
| v0.5.0  | Error Handling Foundation       |
| v0.4.0  | Persistence Foundation          |
| v0.3.0  | API Foundation                  |
| v0.2.0  | Platform Operations Foundation  |
| v0.1.0  | Repository Foundation           |

---

# Repository Status

IncidentLab follows an architecture-first, milestone-driven development approach where each release introduces one foundational capability while maintaining backward compatibility and preserving clean software architecture.

With v0.8.0, the platform has moved from a host-based development runtime to a standardized containerized runtime.

The API and PostgreSQL components can now be executed as a reproducible local container stack using Docker Compose.

The project is now positioned for the next stage of evolution:

```text
Repository
    ↓
Platform Operations
    ↓
API
    ↓
Persistence
    ↓
Error Handling
    ↓
Dependency Injection
    ↓
Authentication
    ↓
Containerization
    ↓
CI/CD
    ↓
Infrastructure as Code
    ↓
Kubernetes
    ↓
Observability
    ↓
DevSecOps
```

The long-term goal remains to evolve IncidentLab into a production-grade cloud-native backend platform through incremental, documented, and testable engineering milestones.
