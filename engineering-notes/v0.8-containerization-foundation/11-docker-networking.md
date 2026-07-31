# Docker Networking

---

# Objective

Understand how Docker enables communication between containers, how Docker Networks work internally, and why networking is essential for multi-container applications.

---

# Why Docker Networking Exists

Containers are isolated by design.

Suppose we have:

- Backend API
- PostgreSQL Database

If these containers cannot communicate,

the application cannot function.

Docker Networking provides a mechanism that allows isolated containers to communicate securely and efficiently.

---

# The Problem Without Networking

```
Backend Container

(No Communication)

Database Container
```

Backend cannot access the database.

Requests fail.

---

# Docker Networking Solution

```
Backend Container

        │

Docker Network

        │

Database Container
```

Docker creates a virtual network between containers.

Containers communicate using this network.

---

# What is a Docker Network?

A Docker Network is a virtual communication layer managed by Docker.

Every container connected to the same Docker Network can communicate with other containers using their container names.

Docker automatically handles:

- IP Address Allocation
- DNS Resolution
- Network Isolation
- Packet Routing

---

# High-Level Architecture

```
Container A

      │

Docker Bridge Network

      │

Container B

      │

Linux Bridge

      │

Host Network Interface

      │

Internet
```

---

# Default Bridge Network

Whenever Docker is installed,

it automatically creates a default network called

```
bridge
```

Containers launched without specifying a network are attached here.

Example

```bash
docker network ls
```

Typical output

```
bridge

host

none
```

---

# Types of Docker Networks

Docker supports multiple network drivers.

```
Docker Networks

├── Bridge
├── Host
├── None
├── Overlay
└── Macvlan
```

Each serves a different purpose.

---

# Bridge Network

The default network driver.

Characteristics

- Containers communicate with each other.
- Containers have private IP addresses.
- Suitable for single-host applications.
- Most commonly used.

Example

```
Frontend

↓

Bridge Network

↓

Backend

↓

PostgreSQL
```

---

# Host Network

The container shares the host's network stack.

There is no network isolation.

Characteristics

- Better performance.
- No port mapping required.
- Limited isolation.

Mostly used when maximum network performance is required.

---

# None Network

The container has no network connectivity.

Characteristics

- No Internet.
- No Container Communication.
- Maximum Isolation.

Useful for highly restricted workloads.

---

# Overlay Network

Designed for multiple Docker Hosts.

Used in:

- Docker Swarm
- Multi-node environments

Containers communicate even when running on different physical machines.

---

# Macvlan Network

Allows containers to appear as physical devices on the network.

Each container receives its own MAC Address.

Useful when applications require direct access to the physical network.

---

# How Containers Communicate

Containers connected to the same Docker Network communicate using DNS.

Example

Backend

↓

Database

Instead of

```
192.168.x.x
```

the Backend simply connects to

```
postgres
```

Docker automatically resolves the container name.

---

# DNS Resolution

Suppose

```
Container Name

postgres
```

Docker automatically maps

```
postgres

↓

172.x.x.x
```

Applications never need to know the actual IP.

---

# Port Mapping

Containers have their own isolated network namespace.

Ports inside the container are not accessible from outside unless explicitly published.

Example

```bash
docker run -p 8000:8000 app
```

Meaning

```
Host Port

8000

↓

Container Port

8000
```

Requests from the host are forwarded to the container.

---

# Internal vs External Communication

Internal

```
Frontend

↓

Backend

↓

Database
```

No published ports required.

---

External

```
Browser

↓

Host Port

↓

Container Port
```

Requires port publishing.

---

# Linux Bridge

Docker Bridge Network internally relies on the Linux Bridge.

The Linux Kernel forwards packets between connected containers.

Docker automates this entire process.

---

# Network Namespace

Every container receives its own Network Namespace.

This means every container has:

- Own IP Address
- Own Routing Table
- Own Network Interfaces
- Own Port Space

Even though they share the Host Kernel,

their networking remains isolated.

---

# Real World Example

Imagine an office building.

Each employee has:

- Their own cabin.
- Their own extension number.

The office network connects everyone.

Employees communicate using extension numbers,

not physical wiring.

Docker Networks work similarly.

---

# Common Use Cases

Docker Networking is used for:

- Frontend ↔ Backend
- Backend ↔ Database
- API Gateway ↔ Services
- Microservices
- Monitoring Stack
- Reverse Proxy
- Message Brokers

---

# Production Best Practices

- Create custom bridge networks.
- Avoid using the default bridge in production.
- Publish only required ports.
- Keep databases private.
- Use container names instead of IP addresses.
- Separate application tiers using different networks.

---

# Interview Explanation (90 Seconds)

Docker Networking enables communication between isolated containers. Docker creates virtual networks that provide automatic IP allocation, DNS resolution, and network isolation. Containers connected to the same network communicate using container names rather than IP addresses. Docker supports multiple network drivers such as Bridge, Host, None, Overlay, and Macvlan, each designed for different deployment scenarios. Internally, Docker relies on Linux networking features like network namespaces and Linux Bridge to isolate and route container traffic.

---

# Common Misconceptions

❌ Containers automatically communicate.

✅ They must be connected to a Docker Network.

---

❌ Containers should communicate using IP addresses.

✅ Container names should be used.

---

❌ Every port inside a container is publicly accessible.

✅ Ports must be explicitly published.

---

❌ Host Network provides better security.

✅ Host Network reduces network isolation.

---

# Key Takeaways

- Docker Networks enable container communication.
- Bridge is the default network driver.
- Containers communicate using DNS.
- Port Mapping exposes container ports.
- Network Namespaces isolate container networking.
- Docker relies on Linux networking internally.

---

# Connections

## Previous

- 10 Docker Volumes

## Next

- 12 Docker Compose

---

# My Understanding

Docker Networking allows isolated containers to communicate with each other through virtual networks managed by Docker. Instead of using fixed IP addresses, containers communicate using their names because Docker provides built-in DNS resolution. Different network drivers such as Bridge, Host, Overlay, and Macvlan are available for different use cases. Docker internally uses Linux networking features like network namespaces and Linux Bridge to provide communication while maintaining isolation.

---

# Questions

- What is a Linux Bridge?
- What is a veth pair?
- How does Docker DNS work internally?
- How does Kubernetes networking differ from Docker networking?
- What is a CNI plugin?

