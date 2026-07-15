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
- PostgreSQL
- Redis
- Docker

---

## Project Structure

```text
api/
├── app/
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Development Status

Current Phase:

**Sprint 1 — API Bootstrap**

The current objective is to establish a clean backend foundation before implementing business logic.
