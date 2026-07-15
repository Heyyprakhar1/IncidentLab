# IncidentLab API

The IncidentLab API powers the backend of the IncidentLab platform.

It is responsible for exposing APIs that simulate cloud incidents, orchestrate infrastructure operations, manage incident workflows, and provide observability data to the frontend.

---

## Responsibilities

- Expose REST APIs
- Manage incident lifecycle
- Coordinate cloud operations
- Generate simulation events
- Integrate with AWS services
- Publish logs and metrics
- Support observability workflows

---

## Technology Stack

- Python
- FastAPI
- uv
- Pydantic Settings
- Docker

---

## Current Phase

**Sprint 2 — Platform Operations Foundation**

---

## Current Capabilities

The backend currently provides:

- FastAPI application bootstrap
- Typed configuration using Pydantic Settings
- Health endpoint
- Application lifecycle management
- Centralized logging configuration
- Configurable log levels
- HTTP request logging middleware

---

## Project Structure

```text
api/
├── app/
│   ├── config.py
│   ├── lifespan.py
│   ├── logging_config.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── request_logging.py
│   └── main.py
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Operational Capabilities

Current observability includes:

- Startup logging
- Shutdown logging
- HTTP request logging
- Request duration logging
- Client IP logging
- Configurable log levels

Future iterations will introduce:

- Structured JSON logging
- Correlation IDs
- Distributed tracing
- Metrics
- Dashboards
- Alerting
