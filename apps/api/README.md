# IncidentLab API

## Overview

The IncidentLab API is the backend service that powers the IncidentLab platform.

It is built using **FastAPI** and follows a modular, layered architecture that emphasizes maintainability, operational visibility, and incremental evolution.

The current implementation establishes the platform foundation through configuration management, lifecycle orchestration, structured logging, request middleware, versioned routing, typed response models, and a dedicated service layer.

---

# Current Features

The API currently provides the following capabilities.

## Platform Foundation

- FastAPI application bootstrap
- Environment-based configuration
- Typed settings management
- Application lifecycle management
- Structured logging

---

## Observability

- HTTP request logging middleware
- Startup logging
- Shutdown logging
- Configurable log levels

---

## API Foundation

- Versioned API routing
- Modular router composition
- Health endpoint
- Service layer architecture
- Typed response schemas

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13 |
| Framework | FastAPI |
| ASGI Server | Uvicorn |
| Configuration | Pydantic Settings |
| Validation | Pydantic v2 |
| Package Manager | uv |

---

# Project Structure

```text
apps/api/

├── app/
│
├── api/
│   └── v1/
│       ├── endpoints/
│       │   └── health.py
│       └── router.py
│
├── middleware/
│   └── request_logging.py
│
├── schemas/
│   └── health.py
│
├── services/
│   └── health.py
│
├── config.py
├── lifespan.py
├── logging_config.py
└── main.py
```

Each module has a single responsibility and should remain focused on its architectural role.

---

# Running the API

## Install dependencies

```bash
uv sync
```

---

## Start the development server

```bash
uv run uvicorn app.main:app --reload
```

By default, the API runs on:

```
http://127.0.0.1:8000
```

---

# Available Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/health` | Returns the current health status of the API. |

---

# Interactive API Documentation

FastAPI automatically exposes interactive API documentation.

| Page | URL |
|------|-----|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |
| OpenAPI Specification | `http://127.0.0.1:8000/openapi.json` |

---

# Environment Configuration

Application configuration is centralized through `config.py`.

Supported environment variables include:

| Variable | Default |
|----------|---------|
| APP_ENV | development |
| APP_NAME | IncidentLab API |
| APP_DESCRIPTION | Cloud Incident Simulation Platform |
| APP_VERSION | 0.3.0 |
| LOG_LEVEL | INFO |

Configuration is loaded from the `.env` file when present.

---

# Request Lifecycle

Every request follows the same execution path.

```text
Client

↓

Request Logging Middleware

↓

API Router

↓

Endpoint

↓

Service Layer

↓

Response Schema

↓

JSON Response
```

This separation keeps HTTP handling independent from business logic.

---

# Architectural Responsibilities

## main.py

Application composition.

Responsible for:

- Creating the FastAPI application
- Registering middleware
- Registering routers
- Connecting the lifespan handler

---

## api/

Defines the public HTTP interface.

Contains:

- API versioning
- Router composition
- Endpoint organization

---

## endpoints/

Owns request handling.

Endpoints should:

- Validate incoming requests
- Call services
- Return typed responses

Endpoints should not contain business logic.

---

## services/

Contains application business logic.

Current service:

- HealthService

Future services will encapsulate additional platform behavior while remaining independent of HTTP concerns.

---

## schemas/

Defines API contracts using Pydantic models.

Current schema:

- HealthResponse

Future request and response models should be placed here.

---

## middleware/

Contains cross-cutting functionality shared across requests.

Current middleware:

- Request logging

Future middleware may include:

- Authentication
- Correlation IDs
- Metrics
- Rate limiting
- Audit logging

---

## config.py

Provides centralized application configuration.

All modules consume the shared settings object rather than reading environment variables directly.

---

## lifespan.py

Owns startup and shutdown orchestration.

Future platform resources such as databases, caches, and cloud clients will be initialized here.

---

# Development Guidelines

To maintain architectural consistency:

- Keep endpoints thin.
- Place business logic inside services.
- Define public API contracts using schemas.
- Centralize configuration in `config.py`.
- Keep middleware focused on cross-cutting concerns.
- Avoid circular dependencies between modules.
- Introduce new architectural layers only when justified.

---

# Current Development Status

Implemented:

- Application bootstrap
- Configuration management
- Lifecycle management
- Structured logging
- HTTP request logging middleware
- Versioned routing
- Service layer
- Typed response schemas
- Health endpoint

In Progress:

- Global exception handling
- Dependency injection
- Standard API error responses

Planned:

- Database integration
- Repository layer
- Authentication & authorization
- Incident management
- Audit logging
- Metrics and tracing
- Background workers
- Cloud integrations

---

# Engineering Philosophy

The API evolves through small, focused engineering milestones.

Each sprint introduces a single architectural capability while preserving modularity, readability, and maintainability.

The objective is to build a production-inspired backend that demonstrates sound engineering practices rather than maximizing feature count.
