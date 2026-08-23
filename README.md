# IncidentLab

A backend platform I'm building to practice how real engineering teams design, containerize, and operate cloud-native systems, not just how they ship features.

Most tutorials show you how to stand up an API. Fewer show you what it takes to keep that API alive in production: how it's structured, how it's deployed, how someone debugs it at 2 AM when it breaks. IncidentLab is my attempt to close that gap for myself, one architectural milestone at a time, instead of jumping straight to "add more tech to the resume."

```
IncidentLab/
├── apps/api/           FastAPI backend (the actual application)
├── docs/               Project-level docs: vision, architecture, roadmap, ADRs
├── engineering-notes/  The learning that went into each milestone
├── compose.yaml        Local dev stack (API + Postgres)
└── .github/workflows/  CI/CD experiments (v0.9.0, in progress)
```

## Where it stands

**v0.8.0 — Containerization Foundation** is done. Everything below it was built one milestone at a time, each with its own ADR, its own branch, and its own docs update before it got merged.

| Foundation | Status |
|---|---|
| Repository | Done |
| Platform operations (config, logging, lifespan) | Done |
| API (versioned routing, health checks) | Done |
| Persistence (SQLAlchemy + Alembic + Postgres) | Done |
| Error handling (global exception handling) | Done |
| Dependency injection | Done |
| Authentication (JWT + Argon2) | Done |
| Containerization | Done |
| CI/CD | In progress (v0.9.0) |
| Infrastructure as Code | Planned |
| Kubernetes | Planned |
| Observability | Planned |
| DevSecOps | Planned |

I'm on **v0.9.0 — CI/CD Foundation** right now, working through GitHub Actions fundamentals: jobs, parallel jobs, matrix builds, conditions, permission scoping, before wiring up a real build-test-publish pipeline. What's in `.github/workflows/` today is that practice, not a finished pipeline, so don't expect it to be production-ready yet.

## Architecture

The application is layered, and containerization wraps around it as a runtime boundary rather than replacing it:

```
Client
  │
  ▼
Docker Host :8000
  │
  ▼
┌────────────────────────┐
│   IncidentLab API       │
│   Uvicorn → FastAPI     │
│   Auth → DI → Services  │
│   → Repository layer    │
└───────────┬─────────────┘
            │
            ▼
     PostgreSQL (Docker)
            │
            ▼
  incidentlab_postgres_data
```

A request comes in with a JWT bearer token, passes through FastAPI's dependency injection layer, hits a service, and the service talks to Postgres through a repository, never directly.

Two Dockerfiles live under `apps/api/`: a conventional one and `Dockerfile.multistage`, which keeps build tooling like `uv` and `curl` out of the final image. Dropping a redundant `RUN chown -R` in favor of `COPY --chown` took the image from about 265 MB down to 192 MB. Small thing, but it's the kind of detail you only notice once you're staring at `docker history` output.

## Stack

| Layer | Tech |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI + Uvicorn |
| ORM / migrations | SQLAlchemy (async) + Alembic |
| Database | PostgreSQL 16 |
| Auth | PyJWT + Argon2 (via `pwdlib`) |
| Package manager | uv |
| Containers | Docker, Docker Compose, multi-stage builds |

## Running it locally

You'll need Docker and Docker Compose installed.

```bash
# from the repo root
cp apps/api/.env.example apps/api/.env   # adjust DB_* and JWT_SECRET_KEY as needed
docker compose up -d --build
```

Check that things actually came up healthy:

```bash
docker ps
docker compose logs api
curl http://localhost:8000/api/v1/health
```

To build the multi-stage image on its own, outside Compose:

```bash
docker build -f apps/api/Dockerfile.multistage -t incidentlab-api:multistage apps/api
```

## API

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/api/v1/health` | No auth required |
| POST | `/api/v1/auth/register` | Create a user |
| POST | `/api/v1/auth/login` | Returns a JWT |
| GET | `/api/v1/auth/me` | Requires bearer token |
| POST | `/api/v1/incidents` | Requires bearer token |
| GET | `/api/v1/incidents` | Requires bearer token |
| GET | `/api/v1/incidents/{incident_id}` | Requires bearer token |

Swagger UI is available at `/docs` once the API is running, and ReDoc at `/redoc`.

## docs/

This is where I keep the project-level "why" and "what," separate from the code itself:

| File | What's in it |
|---|---|
| `vision.md` | Why this project exists and where it's headed long-term |
| `product-requirements.md` | Scope, functional and non-functional requirements |
| `architecture.md` | Current system design, in more depth than this README |
| `roadmap.md` | Completed, current, and planned milestones |
| `changelog.md` | What actually changed in each release |
| `release-history.md` | The fuller story behind each release, including how it was validated |
| `adr/` | Architectural Decision Records: the reasoning behind each major call |

If `docs/` and this README ever disagree, trust `docs/`. That's the one I keep in sync with what's built.

## engineering-notes/

Separate from the project docs, this is where I kept the actual learning behind each milestone: not just the outcome, but the concepts that led to it.

`v0.8-containerization-foundation/` has sixteen notes, `00` through `15`, walking through containers from first principles: why Docker exists, how it's different from a VM, the Linux kernel basics underneath it, image layers, build caching, multi-stage builds, volumes, networking, and Compose, finishing with an interview cheatsheet and an honest retrospective on the milestone.

Inside that, `docker-deep-dive/` goes another level down: one note per Dockerfile instruction (`FROM`, `COPY`, `RUN`, `USER`, `HEALTHCHECK`, and so on), plus the internals behind them: namespaces, cgroups, the OCI image spec, containerd and runc. It's more depth than the implementation strictly needed. I wrote it anyway because that's how I actually retain this stuff instead of just copy-pasting a Dockerfile that works.

## What's next

CI/CD Foundation now, then Infrastructure as Code (Terraform), Kubernetes, Observability (Prometheus, Grafana, Loki), and DevSecOps (Trivy, Gitleaks, Bandit). Each one gets its own milestone, its own ADR, and its own engineering notes before it's considered done. Full detail lives in `docs/roadmap.md`.

## License

No license file yet. This is a personal learning project for now, not something meant to be reused as-is.

---

Built and maintained by Prakhar Srivastava.
