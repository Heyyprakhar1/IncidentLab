IncidentLab

A production-inspired backend platform for learning modern backend and cloud-native engineering through incremental architectural evolution.

Rather than building features first, IncidentLab focuses on strong engineering foundations, clean architecture, operational ownership, and documented engineering decisions.

Implementation establishes the capability. Documentation records the capability.

Why IncidentLab Exists

IncidentLab demonstrates how systems evolve through small, well-defined architectural milestones.

Each release introduces a focused capability while preserving existing behavior and maintaining a clean architecture.

The project is intentionally built as an engineering system rather than a collection of unrelated technology demonstrations.

Current Release

v0.8.0 — Containerization Foundation

Completed foundations:

Repository

Platform Operations

API

Persistence

Error Handling

Dependency Injection

Authentication

Containerization

Current milestone: v0.9.0 — CI/CD Foundation (Ongoing)

Current CI/CD work includes GitHub Actions, jobs, parallel jobs, matrix jobs, conditions, permissions, and workflow validation.

For the complete milestone history and current roadmap, see docs/roadmap.md.

Current Architecture

IncidentLab uses a layered application architecture surrounded by a containerized runtime.

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

The containerization layer provides the runtime boundary without replacing the internal application architecture.

Implemented Foundations

API

FastAPI

Versioned API routing

Request lifecycle management

Structured logging middleware

Persistence

SQLAlchemy Async ORM

PostgreSQL

Alembic

Repository pattern

Reliability

Global exception handling

Standardized API error responses

Domain-specific exceptions

Dependency Injection

Centralized dependency providers

Repository and service providers

FastAPI dependency injection

Authentication

JWT authentication

User registration and login

Argon2 password hashing

HTTP Bearer authentication

Protected API endpoints

Containerization

Docker-based API runtime

Python 3.12 slim

Non-root incidentlab user

Docker healthcheck

Docker Compose

PostgreSQL 16 container

Persistent database volume

Conventional and multi-stage Dockerfiles

Runtime dependency isolation

Container Runtime

The API is containerized using:

apps/api/
├── Dockerfile
└── Dockerfile.multistage

The multi-stage implementation separates build-time dependencies from the runtime environment.

Builder Stage
     │
     ├── uv
     ├── pyproject.toml
     ├── uv.lock
     │
     ▼
   /app/.venv
     │
     ▼
Runtime Stage
     │
     ├── .venv
     ├── application
     ├── uvicorn
     └── incidentlab user

The local stack is orchestrated through:

Docker Compose
     │
     ├── API
     │
     └── PostgreSQL
            │
            ▼
   incidentlab_postgres_data

API Endpoints

Method

Endpoint

Purpose

GET

/api/v1/health

Application health

POST

/api/v1/auth/register

Register user

POST

/api/v1/auth/login

Authenticate user

GET

/api/v1/auth/me

Current authenticated user

POST

/api/v1/incidents

Create incident

GET

/api/v1/incidents

List incidents

GET

/api/v1/incidents/{id}

Retrieve incident

Incident endpoints require authentication.

Technology Stack

Application

Python 3.12

FastAPI

SQLAlchemy 2.x

PostgreSQL

Alembic

Pydantic v2

PyJWT

pwdlib / Argon2

Uvicorn

Containerization

Docker

Docker Compose

Python 3.12 slim

uv

Multi-stage builds

Docker Healthcheck

Running IncidentLab

Docker Compose

docker compose up -d --build

Check services:

docker ps

Check API logs:

docker compose logs api

Check database logs:

docker compose logs db

Verify the API:

curl http://localhost:8000/api/v1/health

Build the Multi-Stage Image

docker build \
  -f apps/api/Dockerfile.multistage \
  -t incidentlab-api:multistage \
  apps/api

Engineering Workflow

Each milestone follows an architecture-first workflow:

Requirements
     ↓
Architecture Decision Record
     ↓
Implementation
     ↓
Feature Branch
     ↓
Testing / Validation
     ↓
Integration
     ↓
main Branch
     ↓
Documentation
     ↓
Release Tag

Documentation

The detailed project documentation lives under docs/.

Document

Purpose

docs/vision.md

Long-term platform vision

docs/product-requirements.md

Product scope and requirements

docs/architecture.md

Current architecture and runtime design

docs/roadmap.md

Completed, ongoing, and future milestones

docs/changelog.md

Engineering and implementation changes

docs/release-history.md

Release evolution

docs/adr/

Architectural Decision Records

Deep technical learning notes are maintained separately under engineering-notes/.

Roadmap

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

Completed: v0.1.0 → v0.8.0

Ongoing: v0.9.0 — CI/CD Foundation

Next: v0.10.0 — Infrastructure as Code Foundation

See docs/roadmap.md for the authoritative roadmap.

Project Status

IncidentLab is evolving from a backend foundation into a production-inspired cloud-native engineering platform.

The current focus is not simply adding technologies, but establishing the engineering practices required to build, operate, investigate, and continuously improve modern systems.

For architecture, decisions, requirements, releases, and future direction, use the docs/ directory as the authoritative project documentation.

License

See the repository for project licensing information.
