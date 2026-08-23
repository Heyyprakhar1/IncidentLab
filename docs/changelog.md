Changelog

All notable changes to IncidentLab are documented in this file.

The project follows an architecture-first, milestone-driven development approach. Each release introduces a foundational capability while maintaining backward compatibility and a clean layered architecture.

v0.8.0 — Containerization Foundation

Release Date: 2026-08-11

Added

Containerization

Docker-based API containerization

Production-oriented API Dockerfile

Multi-stage Docker build

Runtime dependency isolation

Python 3.12 slim base image

Dedicated non-root runtime user

Docker healthcheck

Uvicorn-based container startup

Docker Compose

Docker Compose development stack

FastAPI API service

PostgreSQL 16 service

Compose service networking

Persistent PostgreSQL volume

API healthcheck integration

Multi-Stage Build

Dedicated builder stage

Dedicated runtime stage

uv dependency installation in the builder stage

pyproject.toml and uv.lock based dependency resolution

.venv generated as the runtime dependency artifact

Runtime .venv copied from the builder stage

Build-time tooling separated from the runtime environment

Runtime Security

Non-root incidentlab runtime user

Explicit file ownership using COPY --chown

Build-time utilities kept outside the runtime environment

Least-privilege container execution

Changed

IncidentLab can now run as a reproducible Docker-based application stack.

The API runtime is no longer dependent on the host's Python environment when executed through Docker.

PostgreSQL is now available as a containerized service through Docker Compose.

The existing layered application architecture remains unchanged inside the API container.

Containerization now provides the runtime boundary around the existing FastAPI application architecture.

Containerization assets are implemented as:

apps/api/Dockerfile

apps/api/Dockerfile.multistage

compose.yaml

Improved

Runtime Reproducibility

The application runtime is now standardized through Docker.

The container provides:

Python
   +
Application
   +
Runtime Dependencies
   +
Uvicorn

This reduces dependency differences between host environments.

Build and Runtime Separation

The multi-stage build separates:

Build Environment
       │
       ▼
Dependency Artifact
       │
       ▼
Runtime Environment

Build-time tools such as uv and curl are not required by the normal application runtime.

Image Optimization

Docker image layers were inspected using:

docker history incidentlab-api:multistage

The initial implementation contained an unnecessary large filesystem layer caused by a recursive ownership operation.

The implementation was changed from a separate ownership mutation to:

COPY --chown=incidentlab:incidentlab ...

This removed the unnecessary recursive ownership layer.

The resulting API image size was reduced from approximately:

265 MB

to:

192 MB

Runtime Security

The API container now executes using:

incidentlab

instead of the default root user.

Application files and runtime artifacts are copied with explicit ownership.

Validation

The containerization implementation was validated through:

Successful Docker image build

Successful standalone multi-stage container startup

Docker healthcheck transition from starting to healthy

API health endpoint returning HTTP 200

Runtime user verification

Runtime Python executable verification

Runtime dependency verification

Docker Compose stack startup

PostgreSQL health verification

API log inspection

PostgreSQL log inspection

Docker image history inspection

Standalone API Validation

docker run -d \
  --name incidentlab-multistage-test \
  -p 8001:8000 \
  incidentlab-api:multistage

Health Endpoint Validation

curl http://localhost:8001/api/v1/health

Runtime User Validation

docker exec incidentlab-multistage-test whoami

Expected result:

incidentlab

Runtime Python Validation

docker exec incidentlab-multistage-test \
  python -c "import sys; print(sys.executable)"

Expected result:

/app/.venv/bin/python

Docker Compose Validation

docker compose up -d --build

The resulting stack successfully started:

incidentlab-api-1
incidentlab-db-1

Both services reached a healthy state.

Infrastructure

PostgreSQL 16 container

Persistent PostgreSQL volume

Docker Compose network

API-to-database service communication

Application-level healthcheck

Container runtime health monitoring

Git Integration

The containerization implementation was developed on:

feature/containerization-foundation

The completed implementation was merged into:

main

using a fast-forward merge.

The merge introduced:

apps/api/Dockerfile.multistage
compose.yaml

The updated main branch was pushed to the remote repository.

The feature branch was subsequently removed after successful integration.

Cleanup

Temporary Docker resources created during development and validation were cleaned after verification.

Unused BuildKit cache was reclaimed using:

docker builder prune

Approximately 3.12 GB of unused builder cache was reclaimed.

Persistent application resources such as the PostgreSQL data volume were retained.

Architectural Outcome

v0.8.0 establishes the Containerization Foundation for IncidentLab.

The platform now has:

Layered Application Architecture
             │
             ▼
       Docker Runtime
             │
       ┌─────┴─────┐
       ▼           ▼
      API           DB
   Container     Container
                    │
                    ▼
             Persistent Data

This provides the runtime foundation required for future:

CI/CD

Infrastructure as Code

Kubernetes

Observability

DevSecOps

v0.7.0 — Authentication Foundation

Release Date: 2026-07-30

Added

Authentication

JWT-based authentication

User registration endpoint

User login endpoint

Authenticated user endpoint (/auth/me)

HTTP Bearer authentication

Current user dependency injection

User Management

User database model

User repository

Authentication service

Authentication schemas

Security

Password hashing using Argon2

JWT access token generation

JWT validation

Protected incident endpoints

Infrastructure

Authentication dependency providers

Authentication module

Database migration for users table

Changed

Incident APIs now require authentication.

Dependency Injection layer extended to support authentication services.

Project architecture now includes an Authentication Foundation.

Security

Passwords are securely hashed before storage.

Plaintext passwords are never persisted.

Protected endpoints return 401 Unauthorized for unauthenticated requests.

JWT secret is loaded from application configuration.

v0.6.0 — Dependency Injection Foundation

Introduced centralized dependency injection for repositories and services, improving modularity, testability, and separation of concerns.

v0.5.0 — Error Handling Foundation

Introduced centralized exception handling with standardized API error responses and domain-specific exception management.

v0.4.0 — Persistence Foundation

Introduced SQLAlchemy Async ORM, Alembic migrations, PostgreSQL integration, and the Repository pattern.

v0.3.0 — API Foundation

Established FastAPI application structure, versioned routing, middleware, and request lifecycle management.

v0.2.0 — Platform Operations Foundation

Established the operational project structure and backend platform organization.

v0.1.0 — Repository Foundation

Introduced the Repository pattern as the first architectural foundation of IncidentLab.
