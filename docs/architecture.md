System Architecture

IncidentLab follows a layered architecture that emphasizes separation of concerns, maintainability, and incremental architectural evolution.

Beginning with v0.7.0 – Authentication Foundation, the architecture introduced a dedicated authentication layer built on top of the Dependency Injection Foundation. Authentication is implemented using stateless JSON Web Tokens (JWT) and integrates with FastAPI's dependency injection system.

With v0.8.0 – Containerization Foundation, the existing application architecture is executed inside a standardized Docker runtime.

Containerization provides the runtime boundary around the application without changing the internal application layering.

Architectural Principles

The project follows these principles:

Separation of Concerns

Single Responsibility Principle

Dependency Injection

Repository Pattern

Layered Architecture

Stateless Authentication

Reproducible Runtime Environments

Least-Privilege Runtime

Incremental Evolution

Production-Inspired Design

Environment Consistency

High-Level System Architecture

The current architecture consists of two major boundaries:

Application Architecture — the internal layered FastAPI application.

Runtime Architecture — Docker and Docker Compose providing the execution environment.

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

Docker Compose manages the API and PostgreSQL services as a local containerized stack.

Application Architecture

The containerization layer does not replace the existing application architecture.

Inside the API container, IncidentLab continues to follow the established layered design:

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

The application remains responsible for business and data-access concerns, while Docker provides the standardized runtime environment.

Runtime Architecture

The runtime architecture is provided through Docker Compose.

Docker Compose
      │
      ├──────────────────────┐
      │                      │
      ▼                      ▼
 API Container          PostgreSQL
      │                   Container
      │                      │
      │                      ▼
      │             Persistent Volume
      │
      ▼
 FastAPI / Uvicorn
      │
      ▼
 Application Layers

The API container exposes port 8000.

PostgreSQL remains an internal service of the Compose stack and uses persistent storage through the named volume:

incidentlab_postgres_data

Container Runtime Boundary

The API application is executed inside a Docker container rather than directly on the host.

Host Operating System
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
        └── Uvicorn

The runtime uses a dedicated non-root user:

incidentlab

This establishes a least-privilege runtime boundary around the application.

API Container

The API container is responsible for running the IncidentLab FastAPI application.

Its runtime responsibilities include:

Starting Uvicorn.

Loading the FastAPI application.

Serving HTTP requests.

Executing application dependencies.

Communicating with PostgreSQL.

Reporting application health.

The application is started using:

ENTRYPOINT ["uvicorn"]

with the application target and runtime arguments supplied through CMD.

The effective command is conceptually:

uvicorn app.main:app --host 0.0.0.0 --port 8000

Application Health

The API exposes:

GET /api/v1/health

Docker uses the configured healthcheck to determine whether the application is healthy.

The architecture therefore distinguishes between:

Container Process Running
          ≠
Application Healthy

A container can be running while the application inside it is unable to serve requests correctly.

The healthcheck provides an application-level signal to the container runtime.

PostgreSQL Container

PostgreSQL is executed as a separate Compose service.

IncidentLab API
      │
      │ database connection
      ▼
PostgreSQL Container
      │
      ▼
Persistent Volume

The database container is responsible only for database execution and persistence.

The API communicates with PostgreSQL through the Docker Compose network rather than relying on host-level database configuration.

Persistent Storage

PostgreSQL uses the named volume:

incidentlab_postgres_data

The volume provides persistence across PostgreSQL container recreation.

The relationship is:

PostgreSQL Container
        │
        ▼
incidentlab_postgres_data
        │
        ▼
Persistent Database Data

Container lifecycle and database data lifecycle are therefore treated separately.

Application Layer Responsibilities

API Layer

Location:

app/api/

Responsibilities:

HTTP request handling

Request validation

Response serialization

Dependency resolution

The API layer contains no business logic and performs no manual object construction.

Authentication Layer

Locations:

app/auth/
app/dependencies/auth.py

Responsibilities:

Password hashing

Password verification

JWT generation

JWT validation

Current user resolution

Authentication is implemented using HTTP Bearer tokens and integrated through FastAPI dependency injection.

Dependency Layer

Location:

app/dependencies/

Responsibilities:

Database dependency providers

Repository dependency providers

Service dependency providers

Authentication dependency providers

This layer centralizes object creation and manages dependency relationships across the application.

Service Layer

Location:

app/services/

Responsibilities:

Business logic

Application use cases

User authentication

Coordination between layers

Services consume repositories through dependency injection and remain independent of database session management.

Repository Layer

Location:

app/repositories/

Responsibilities:

Data access

SQLAlchemy queries

ORM persistence

Transaction interaction

Repositories receive database sessions through dependency providers.

Database Layer

The database layer uses:

SQLAlchemy Async ORM

PostgreSQL

Alembic migrations

The database provider is injected into repositories rather than being constructed directly inside application services.

Containerization Components

The current repository contains the containerization assets directly alongside the API application:

IncidentLab/
│
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
└── ...

The initial ADR proposed an infra/ directory for containerization assets, but the implemented v0.8 architecture places the API Dockerfiles under apps/api/ and the Compose definition at the repository root.

The architecture documentation reflects the implemented repository state.

Dockerfile Architecture

IncidentLab maintains two Dockerfile implementations:

apps/api/
├── Dockerfile
└── Dockerfile.multistage

The conventional Dockerfile provides the standard container build.

The multi-stage Dockerfile provides a separated builder and runtime architecture.

Both remain part of the project intentionally.

Multi-Stage Build Architecture

The multi-stage implementation separates build-time responsibilities from runtime responsibilities.

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
                  Selected Artifact
                       │
                       ▼
                 Runtime Stage
                       │
                       ├── Python
                       ├── .venv
                       ├── Application
                       ├── Uvicorn
                       └── incidentlab user

The builder generates the runtime dependency environment.

The runtime stage receives the required .venv artifact instead of the complete builder environment.

Build-time utilities are therefore separated from the application runtime.

Runtime Artifact Selection

The multi-stage build explicitly selects the runtime artifact:

COPY --from=builder     --chown=incidentlab:incidentlab     /app/.venv /app/.venv

The runtime does not require the complete builder filesystem.

The conceptual flow is:

Builder Environment
        │
        ├── uv
        ├── curl
        ├── dependency definitions
        └── .venv
              │
              ▼
       Selected Artifact
              │
              ▼
      Runtime Environment

This keeps build responsibilities separate from runtime responsibilities.

Runtime Ownership

Application files and runtime artifacts are copied with explicit ownership:

COPY --chown=incidentlab:incidentlab . .

and:

COPY --from=builder     --chown=incidentlab:incidentlab     /app/.venv /app/.venv

This allows the container to run as:

incidentlab

without requiring a later recursive ownership operation.

Image Optimization Architecture

Docker image construction is treated as a layered filesystem process.

During the v0.8 implementation, the multi-stage image was inspected using:

docker history incidentlab-api:multistage

The initial implementation contained an unnecessary ownership layer:

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

The recursive ownership operation was removed in favor of COPY --chown.

This reduced the resulting image from approximately:

265 MB

to:

192 MB

The optimization demonstrates that image architecture and filesystem-layer behavior must both be considered when designing containerized systems.

Docker Compose Architecture

The local containerized environment is orchestrated through:

compose.yaml

The stack consists of:

Compose Project
      │
      ├── api
      │     │
      │     └── IncidentLab FastAPI
      │
      └── db
            │
            └── PostgreSQL 16

The API and database operate as separate services.

Docker Compose provides the service-level networking required for communication between them.

Network Architecture

The Compose stack provides an isolated network for its services.

Docker Compose Network
        │
        ├──────────────┐
        │              │
        ▼              ▼
   API Service      DB Service
        │              │
        └──────┬───────┘
               │
        Internal Service
        Communication

The API communicates with PostgreSQL through the Compose service network.

The host-facing API port is published separately.

The application therefore has two distinct networking concerns:

Host → API

and:

API → PostgreSQL

Port Architecture

The API listens on:

8000

The Docker Image declares:

EXPOSE 8000

The Compose configuration publishes the API to the host.

Conceptually:

Host :8000
    │
    ▼
API Container :8000

EXPOSE documents the container port; Compose port mapping is responsible for host publication.

PostgreSQL remains an internal service and does not need to be exposed to the host for normal API operation.

Build and Runtime Flow

The complete v0.8 runtime flow is:

Dockerfile
     │
     ▼
docker build
     │
     ▼
Docker Image
     │
     ▼
Docker Compose
     │
     ├───────────────┐
     ▼               ▼
API Container     DB Container
     │               │
     │               ▼
     │          Persistent Volume
     │
     ▼
Healthcheck
     │
     ▼
Healthy Application

For the multi-stage build:

Dockerfile.multistage
        │
        ▼
Builder Stage
        │
        ▼
.venv Artifact
        │
        ▼
Runtime Stage
        │
        ▼
Final API Image

Runtime Security Architecture

The v0.8 runtime applies a least-privilege approach.

Build Environment
      │
      ├── Build tooling
      ├── Dependency resolution
      └── Artifact generation
               │
               ▼
Runtime Environment
      │
      ├── Application
      ├── Runtime dependencies
      ├── Uvicorn
      └── Non-root user

The application does not require the builder's tooling during normal execution.

The runtime user is:

incidentlab

This reduces unnecessary privileges within the application container.

Architectural Scope

The v0.8 Containerization Foundation introduces:

Docker image creation

Docker container execution

Production-oriented Dockerfile design

Multi-stage Docker builds

Docker Compose

PostgreSQL container integration

Persistent volumes

Container networking

Runtime healthchecks

Non-root runtime execution

Runtime artifact selection

Out of Scope

The following capabilities remain outside the current containerization architecture:

Kubernetes

Helm

Terraform

CI/CD pipelines

Container registry publishing

Image signing

Production deployment

Full container orchestration

Multi-environment deployment architecture

These capabilities will be introduced through future architectural milestones.

Architectural Evolution

The architecture has evolved through the following foundations:

Repository Foundation
        ↓
Platform Operations Foundation
        ↓
API Foundation
        ↓
Persistence Foundation
        ↓
Error Handling Foundation
        ↓
Dependency Injection Foundation
        ↓
Authentication Foundation
        ↓
Containerization Foundation
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

Each milestone builds on the previous architecture while preserving separation of concerns.

v0.8 Architectural Outcome

The Containerization Foundation establishes a standardized runtime boundary around IncidentLab.

The platform now has:

A containerized FastAPI API

A containerized PostgreSQL database

Persistent database storage

Docker Compose orchestration

Non-root API execution

Application health monitoring

Conventional and multi-stage Dockerfile implementations

Explicit runtime artifact selection

A reproducible local container stack

The application architecture remains layered while the runtime architecture has become containerized.

Application Architecture
        │
        ▼
FastAPI
        │
        ▼
Services
        │
        ▼
Repositories
        │
        ▼
PostgreSQL
        ▲
        │
Runtime Architecture
        │
        ▼
Docker Compose
        │
        ├── API Container
        └── PostgreSQL Container

Future Evolution

The Containerization Foundation prepares IncidentLab for:

CI/CD Foundation

Infrastructure as Code

Kubernetes Foundation

Observability Foundation

DevSecOps Foundation

Authorization (RBAC)

Future milestones will build upon the containerized application without requiring fundamental changes to the existing layered application architecture.

Related Components

apps/api/

apps/api/Dockerfile

apps/api/Dockerfile.multistage

compose.yaml

docs/adr/ADR-006-containerization-foundation.md
