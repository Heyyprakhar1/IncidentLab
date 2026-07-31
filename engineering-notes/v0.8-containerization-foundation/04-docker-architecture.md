# Docker Architecture

---

# Objective

Understand how Docker works internally, the role of each Docker component, and how a Docker command travels from the terminal to a running container.

---

# Why Understanding Docker Architecture Matters

Most developers use Docker by executing commands such as:

```bash
docker build
docker run
docker pull
docker ps
```

However, understanding **what happens behind these commands** is essential for debugging, troubleshooting, performance optimization, and production deployments.

Docker Architecture explains how different Docker components work together to build, manage, and run containers.

---

# High-Level Docker Architecture

```
                    User

                     │

             Docker CLI (Client)

                     │

          Docker API (REST Requests)

                     │

            Docker Daemon (dockerd)

      ┌──────────┬──────────┬──────────┐
      │          │          │          │
 Images      Containers   Networks   Volumes
      │          │          │          │
      └──────────┴──────────┴──────────┘

                     │

             containerd Runtime

                     │

                  runc

                     │

              Linux Kernel

                     │

               Physical Hardware
```

---

# Core Components

Docker consists of multiple components working together.

Each component has a specific responsibility.

---

# 1. Docker CLI

Docker CLI (Command Line Interface) is the tool that users interact with.

Examples:

```bash
docker build
docker run
docker pull
docker logs
docker ps
```

The CLI does **not** create containers.

Its only responsibility is to send requests to the Docker Daemon.

Think of Docker CLI as a **remote control**.

---

# 2. Docker API

The Docker CLI communicates with Docker Daemon through the Docker REST API.

Every Docker command is converted into an API request.

Example:

```
docker run nginx
```

becomes

```
Create Container
Start Container
Attach Network
Mount Volumes
```

which are API requests handled by Docker Daemon.

---

# 3. Docker Daemon (dockerd)

Docker Daemon is the heart of Docker.

It runs as a background service on the host machine.

Responsibilities include:

- Building Images
- Running Containers
- Managing Networks
- Managing Volumes
- Pulling Images
- Pushing Images
- Container Lifecycle Management

The Docker Daemon performs all the actual work.

---

# 4. Docker Images

A Docker Image is a read-only blueprint used to create containers.

An Image contains:

- Application Code
- Runtime
- Libraries
- Dependencies
- Configuration

Images are immutable.

Every container starts from an image.

---

# 5. Docker Containers

A Container is a running instance of a Docker Image.

Think of it as a live application created from an image.

One image can create multiple containers.

Example:

```
Ubuntu Image
        │
 ┌──────┴──────┐
 │             │
Container 1  Container 2
```

Containers have their own:

- Process Space
- Network Namespace
- Filesystem
- Resource Limits

But they share the Host Linux Kernel.

---

# 6. Docker Networks

Networks allow containers to communicate.

Examples:

- Bridge Network
- Host Network
- Overlay Network
- None Network

Without networking, containers cannot communicate with each other.

---

# 7. Docker Volumes

Containers are temporary.

When a container is deleted, its internal writable data is also removed.

Volumes provide persistent storage.

They allow data to survive container recreation.

Examples:

- PostgreSQL Database
- MySQL Data
- Uploaded Files
- Application Logs

---

# 8. containerd

Docker Daemon does not directly run containers.

It delegates container management to **containerd**.

containerd is responsible for:

- Image Management
- Container Lifecycle
- Snapshot Management
- Storage Management

Think of containerd as Docker's execution manager.

---

# 9. runc

containerd delegates the actual container creation to **runc**.

runc interacts directly with the Linux Kernel.

It creates:

- Processes
- Namespaces
- cgroups

using Linux Kernel capabilities.

---

# 10. Linux Kernel

The Linux Kernel is responsible for:

- CPU Scheduling
- Memory Allocation
- Process Isolation
- Networking
- Storage
- Security

Docker does **not** perform these tasks.

Docker relies on the Linux Kernel.

---

# Complete Request Flow

Suppose you execute:

```bash
docker run nginx
```

The sequence is:

```
User

   │

Docker CLI

   │

Docker API

   │

Docker Daemon

   │

Checks Local Image

   │

Image Exists?
   │
 ┌─┴──────────────┐
 │                │
Yes              No
 │                │
 │          Pull Image
 │                │
 └──────┬─────────┘
        │

containerd

        │

runc

        │

Linux Kernel

        │

Container Starts
```

---

# Real World Example

Imagine ordering food from a restaurant.

```
Customer
     │
Waiter
     │
Kitchen Manager
     │
Chef
     │
Ingredients
```

Docker Architecture is similar.

Customer → User

Waiter → Docker CLI

Kitchen Manager → Docker Daemon

Chef → containerd + runc

Kitchen → Linux Kernel

Ingredients → Images

Prepared Food → Running Container

---

# Important Observations

Docker CLI does not create containers.

Docker Daemon creates containers.

Docker Daemon does not directly interact with hardware.

Linux Kernel manages hardware.

Docker only orchestrates the process.

---

# Interview Explanation (90 Seconds)

Docker follows a client-server architecture.

The user interacts with Docker using the Docker CLI, which sends requests to the Docker Daemon through the Docker API. The Docker Daemon manages images, containers, networks, and volumes. For container execution, it delegates work to containerd, which further uses runc to create isolated processes using Linux Kernel features such as namespaces and cgroups. The Linux Kernel ultimately manages CPU, memory, storage, networking, and process isolation.

---

# Common Misconceptions

❌ Docker CLI creates containers.

✅ Docker Daemon creates containers.

---

❌ Docker manages CPU and RAM.

✅ Linux Kernel manages system resources.

---

❌ Images are running applications.

✅ Images are templates.

Containers are running instances.

---

❌ Docker is a Virtual Machine.

✅ Docker is a container platform.

---

# Key Takeaways

- Docker follows a client-server architecture.
- Docker CLI sends commands.
- Docker Daemon performs the work.
- Images are blueprints.
- Containers are running instances.
- containerd manages container execution.
- runc creates containers using Linux Kernel features.
- Docker depends on the Linux Kernel.

---

# Connections

## Previous

- 01 Why Docker
- 02 Virtual Machines vs Containers
- 03 Linux Kernel Fundamentals

## Next

- 05 Docker Images vs Containers
- 06 Docker Layers

---

# My Understanding

Docker follows a client-server architecture where the Docker CLI sends commands to the Docker Daemon through the Docker API. The Docker Daemon manages images, containers, networks, and volumes, while containerd and runc handle container execution. Instead of managing hardware directly, Docker relies on the Linux Kernel to provide resources like CPU, memory, storage, and networking.

---

# Questions

- Why does Docker use both containerd and runc?
- What happens if the Docker Daemon stops?
- How does Docker communicate with containerd?
- What is the OCI Runtime Specification?

---

# Status

🟡 In Progress
