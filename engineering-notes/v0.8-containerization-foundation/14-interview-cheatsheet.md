# Docker Interview Cheatsheet

---

# Objective

This document serves as a rapid revision guide for Docker interviews. It summarizes the most important concepts, commands, diagrams, and frequently asked interview questions covered throughout the Containerization Foundation.

---

# Docker in One Line

Docker is a containerization platform that packages an application along with its dependencies, runtime, and configuration into lightweight containers, ensuring consistent execution across different environments.

---

# Docker in 30 Seconds

Docker allows developers to package applications into portable containers that share the Host Linux Kernel. Containers are lightweight, start quickly, consume fewer resources than Virtual Machines, and provide consistent execution across development, testing, and production environments.

---

# Docker Architecture (60 Seconds)

```
User

↓

Docker CLI

↓

Docker API

↓

Docker Daemon

↓

containerd

↓

runc

↓

Linux Kernel

↓

Hardware
```

Remember:

- CLI sends commands.
- Daemon performs the work.
- containerd manages container lifecycle.
- runc creates containers.
- Linux Kernel manages hardware resources.

---

# Docker Workflow

```
Dockerfile

↓

docker build

↓

Docker Image

↓

docker run

↓

Docker Container
```

---

# Image vs Container

| Image | Container |
|--------|-----------|
| Blueprint | Running Instance |
| Read-only | Writable |
| Immutable | Temporary |
| Stored on Disk | Running Process |
| Creates Containers | Executes Applications |

---

# Virtual Machine vs Container

| Virtual Machine | Container |
|-----------------|-----------|
| Own Guest OS | Shares Host Kernel |
| Heavy | Lightweight |
| Slow Startup | Fast Startup |
| More Resource Usage | Lower Resource Usage |
| Strong Isolation | Process Isolation |

---

# Linux Kernel Responsibilities

- Process Management
- Memory Management
- File System Management
- Device Drivers
- Networking
- Security & Permissions

---

# Docker Network Types

| Driver | Purpose |
|---------|---------|
| Bridge | Default single-host networking |
| Host | Shares host network |
| None | No networking |
| Overlay | Multi-host networking |
| Macvlan | Direct physical network access |

---

# Docker Storage

```
Image

↓

Writable Layer

↓

Docker Volume

↓

Host Storage
```

Persistent data should always be stored inside Docker Volumes.

---

# Multi-stage Build Flow

```
Build Stage

↓

Compile Application

↓

COPY --from

↓

Runtime Stage

↓

Final Image
```

---

# Production Dockerfile Order

```
FROM

↓

LABEL

↓

ENV

↓

WORKDIR

↓

COPY Dependencies

↓

Install Dependencies

↓

COPY Source Code

↓

USER

↓

EXPOSE

↓

CMD
```

---

# Docker Build Cache

Docker compares every Dockerfile instruction.

If unchanged:

```
Reuse Cache
```

If changed:

```
Rebuild Layer

↓

Rebuild Remaining Layers
```

---

# Frequently Used Commands

## Images

```bash
docker images

docker pull

docker build

docker rmi
```

---

## Containers

```bash
docker run

docker ps

docker stop

docker start

docker restart

docker rm

docker exec -it

docker logs
```

---

## Volumes

```bash
docker volume create

docker volume ls

docker volume inspect

docker volume rm
```

---

## Networks

```bash
docker network ls

docker network create

docker network inspect

docker network rm
```

---

## Docker Compose

```bash
docker compose up

docker compose up -d

docker compose down

docker compose ps

docker compose logs

docker compose restart
```

---

# Top Interview Questions

## Beginner

- What is Docker?
- Why was Docker created?
- Difference between VM and Container?
- What is an Image?
- What is a Container?
- What is Dockerfile?
- What is Docker Compose?
- What is a Docker Volume?
- What is Docker Networking?
- What is Docker Hub?

---

## Intermediate

- Explain Docker Architecture.
- Explain Docker Layers.
- Explain Build Cache.
- What is Copy-on-Write?
- Why are Images immutable?
- Difference between CMD and ENTRYPOINT?
- Difference between COPY and ADD?
- What is .dockerignore?
- What is Multi-stage Build?
- Explain Named Volume vs Bind Mount.

---

## Advanced

- How does Docker communicate with the Linux Kernel?
- What is containerd?
- What is runc?
- What are Linux Namespaces?
- What are cgroups?
- Why are containers lightweight?
- How does Docker DNS work?
- Explain Overlay Network.
- How does Docker isolate containers?
- How does Docker BuildKit improve builds?

---

# Production Checklist

✅ Minimal Base Image

✅ Version Pinned

✅ Multi-stage Build

✅ Layer Cache Optimized

✅ .dockerignore

✅ Non-root User

✅ No Secrets

✅ Named Volumes

✅ Custom Networks

✅ Health Checks

✅ Monitoring

✅ Logging

✅ Image Scanning

---

# Common Mistakes

❌ Using latest tag

❌ Running as root

❌ Storing secrets inside images

❌ Large base images

❌ Copying everything before installing dependencies

❌ Ignoring .dockerignore

❌ Using default bridge for everything

❌ Storing databases inside containers

---

# Mental Models

Docker Image

↓

Blueprint

---

Docker Container

↓

Running Application

---

Dockerfile

↓

Recipe

---

Docker Compose

↓

Application Blueprint

---

Docker Volume

↓

External Hard Drive

---

Docker Network

↓

Private Office LAN

---

Linux Kernel

↓

Resource Manager

---

# My Personal Summary

Docker is not just a tool for running containers. It is an ecosystem that packages applications into portable, lightweight, and reproducible environments. Docker relies on the Linux Kernel for resource management while providing abstractions such as Images, Containers, Networks, Volumes, and Compose to simplify application deployment. Understanding Docker's architecture and the reasoning behind its design is more valuable than memorizing commands.

---

# Recommended Revision Order

1. Why Docker
2. VM vs Containers
3. Linux Kernel
4. Docker Architecture
5. Images vs Containers
6. Docker Layers
7. Docker Build Cache
8. Dockerfile
9. Multi-stage Builds
10. Docker Volumes
11. Docker Networking
12. Docker Compose
13. Production Best Practices

---

# Connections

## Previous

- 13 Production Best Practices

## Next

- 15 V0.8 Retrospective
