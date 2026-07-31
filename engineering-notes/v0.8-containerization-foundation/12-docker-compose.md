# Docker Compose

---

# Objective

Understand why Docker Compose was created, how it simplifies multi-container applications, and how it enables developers to define an application's entire infrastructure using a single YAML file.

---

# Why Docker Compose Exists

Most modern applications consist of multiple services.

For example, IncidentLab requires:

- FastAPI Backend
- PostgreSQL Database
- Redis (Future)
- Prometheus (Future)
- Grafana (Future)

Without Docker Compose, each service must be started individually.

Example:

```
docker network create

↓

docker volume create

↓

docker run postgres

↓

docker run backend

↓

docker run redis

↓

docker run prometheus

↓

docker run grafana
```

Managing multiple containers manually becomes difficult and error-prone.

Docker Compose solves this problem.

---

# What is Docker Compose?

Docker Compose is a tool that allows you to define and manage multi-container Docker applications using a single YAML configuration file.

Instead of executing multiple `docker run` commands, all services are described in one file.

Docker Compose then creates and manages the complete application stack.

---

# Compose Architecture

```
docker-compose.yml

          │

docker compose up

          │

Docker Compose

          │

──────────────────────────────

Backend Container

Database Container

Redis Container

Volumes

Networks

──────────────────────────────

          │

Running Application
```

---

# Why YAML?

Docker Compose uses YAML because it is:

- Human-readable
- Easy to maintain
- Declarative
- Widely used for Infrastructure as Code

Instead of describing **how** to start containers, you describe **what** the application should look like.

---

# Basic Compose File

```yaml
services:

  backend:
    image: incidentlab-api

  postgres:
    image: postgres:16
```

This defines two services.

Docker Compose creates both and connects them automatically.

---

# Core Components

A Compose file commonly contains:

- services
- image
- build
- ports
- environment
- volumes
- networks
- depends_on
- restart

These are the building blocks of a Compose application.

---

# Services

Every container is represented as a service.

Example

```yaml
services:

  api:

  postgres:

  redis:
```

Each service runs independently.

---

# Build vs Image

Existing Image

```yaml
image: postgres:16
```

Docker downloads an existing image.

---

Local Dockerfile

```yaml
build: .
```

Docker builds an image from the current project.

---

# Ports

Example

```yaml
ports:
  - "8000:8000"
```

Meaning

```
Host

8000

↓

Container

8000
```

---

# Environment Variables

Example

```yaml
environment:
  DATABASE_URL: postgres://...
```

Compose injects these variables into the container.

---

# Volumes

Example

```yaml
volumes:

- postgres-data:/var/lib/postgresql/data
```

The database survives container recreation.

---

# Networks

Compose automatically creates an isolated network.

```
API

↓

Compose Network

↓

PostgreSQL
```

Containers communicate using service names.

Example

```
postgres
```

instead of

```
172.x.x.x
```

---

# depends_on

Suppose

Backend

↓

Database

The backend depends on PostgreSQL.

Example

```yaml
depends_on:

- postgres
```

Docker starts PostgreSQL before starting the backend.

---

# Restart Policies

Example

```yaml
restart: unless-stopped
```

If the container crashes,

Docker automatically restarts it.

---

# Compose Workflow

```
docker-compose.yml

        │

docker compose up

        │

Images

        │

Containers

        │

Volumes

        │

Networks

        │

Running Stack
```

---

# Compose Commands

Start

```bash
docker compose up
```

Detached Mode

```bash
docker compose up -d
```

Stop

```bash
docker compose down
```

View Containers

```bash
docker compose ps
```

Logs

```bash
docker compose logs
```

Restart

```bash
docker compose restart
```

---

# Real World Example

IncidentLab

```
Frontend

        │

FastAPI

        │

PostgreSQL

        │

Redis

        │

Prometheus

        │

Grafana
```

Instead of starting six containers manually,

Docker Compose starts the complete application using one command.

---

# Production Considerations

Docker Compose is excellent for:

- Local Development
- Testing
- Small Deployments
- Proof of Concepts

Large production environments generally use:

- Kubernetes
- Docker Swarm
- Amazon ECS
- Nomad

Compose often serves as the bridge between local development and production orchestration.

---

# Interview Explanation (90 Seconds)

Docker Compose is a tool used to define and manage multi-container Docker applications using a declarative YAML file. It allows developers to describe services, networks, volumes, environment variables, and dependencies in one place. Instead of manually running multiple containers, Docker Compose creates the complete application stack with a single command, making local development and testing significantly easier.

---

# Production Best Practices

- Use Compose for development.
- Keep configuration readable.
- Use Named Volumes.
- Avoid hardcoded secrets.
- Separate development and production Compose files.
- Use service names instead of IP addresses.
- Keep services loosely coupled.

---

# Common Misconceptions

❌ Docker Compose replaces Kubernetes.

✅ Compose is primarily a development orchestration tool.

---

❌ Compose runs everything inside one container.

✅ Every service runs in its own container.

---

❌ Compose automatically scales applications.

✅ Scaling is limited compared to Kubernetes.

---

# Key Takeaways

- Docker Compose manages multi-container applications.
- Compose uses YAML.
- One service equals one container.
- Compose automatically creates networks.
- Services communicate using service names.
- Compose simplifies development workflows.

---

# Connections

## Previous

- 11 Docker Networking

## Next

- 13 Production Best Practices

---

# My Understanding

Docker Compose is a tool that allows multiple containers to be managed as a single application using a declarative YAML file. Instead of manually creating networks, volumes, and containers, Docker Compose automates the entire process. Each service runs in its own container while sharing networks and volumes where required, making development and testing much simpler.

---

# Questions

- What is the difference between Compose and Kubernetes?
- How should production Compose files differ from development files?
- Can Compose scale services?
- How are secrets managed in Compose?
- How does Compose create default networks?
