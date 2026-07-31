# Virtual Machines vs Containers

---

# Objective

Understand how Virtual Machines and Containers work, why they were created, how they differ architecturally, and when each approach should be used.

---

# Why Virtual Machines Were Created

Before virtualization, organizations typically deployed one operating system on one physical server.

Although this approach worked, it created several problems.

- Hardware resources were underutilized.
- Running one application per server became expensive.
- Scaling infrastructure required purchasing additional hardware.
- Managing hundreds of physical servers was difficult.

Virtualization solved these problems by allowing multiple isolated operating systems to run on a single physical machine.

---

# What is a Virtual Machine?

A Virtual Machine (VM) is a software-defined computer that behaves like a real physical computer.

Each Virtual Machine contains its own:

- Operating System
- Kernel
- Filesystem
- Libraries
- Applications
- Virtual CPU
- Virtual Memory
- Virtual Storage

To the application running inside the VM, it appears as if it is running on dedicated hardware.

---

# Virtual Machine Architecture

```
+--------------------------------------+
| Application                          |
+--------------------------------------+
| Guest Operating System               |
+--------------------------------------+
| Hypervisor                           |
+--------------------------------------+
| Host Operating System                |
+--------------------------------------+
| Physical Hardware                    |
+--------------------------------------+
```

---

# Components

## Physical Hardware

The actual machine that provides:

- CPU
- Memory
- Storage
- Network Interface

---

## Host Operating System

The operating system installed directly on the physical hardware.

Examples:

- Windows
- Ubuntu
- macOS

---

## Hypervisor

A Hypervisor creates and manages Virtual Machines.

It allocates hardware resources to every VM while ensuring isolation between them.

Examples:

- VMware ESXi
- Oracle VirtualBox
- Microsoft Hyper-V
- KVM

---

## Guest Operating System

Every Virtual Machine installs a complete operating system.

Examples:

- Ubuntu
- Debian
- Windows Server

Each Guest OS has its own kernel and operates independently from the Host OS.

---

# Why Virtual Machines are Heavy

Every Virtual Machine includes an entire operating system.

As a result, every VM consumes additional:

- CPU
- Memory
- Disk Space
- Boot Time

As more Virtual Machines are created, resource consumption increases significantly.

---

# Why Containers Were Introduced

Although Virtual Machines solved environment isolation, most applications did not require an entire operating system.

For example, a Python application usually needs:

- Python Runtime
- Required Libraries
- Application Code

It does **not** require:

- A complete desktop environment
- Device drivers
- A separate operating system

Running an entire operating system for every application became unnecessary overhead.

Containers were introduced to provide process isolation while sharing the host operating system's kernel.

---

# What is a Container?

A Container is an isolated runtime environment for an application.

Unlike Virtual Machines, containers do not install a complete operating system.

Instead, they package:

- Application Code
- Runtime
- Libraries
- Dependencies
- Configuration

Containers share the Host Kernel while remaining isolated from one another.

---

# Container Architecture

```
+--------------------------------------+
| Application                          |
+--------------------------------------+
| Runtime & Libraries                  |
+--------------------------------------+
| Container Runtime (Docker)           |
+--------------------------------------+
| Host Operating System                |
+--------------------------------------+
| Host Kernel                          |
+--------------------------------------+
| Physical Hardware                    |
+--------------------------------------+
```

---

# How Containers Achieve Isolation

Containers do not create separate operating systems.

Instead, they isolate applications while sharing the Host Kernel.

Docker relies on Linux kernel features to achieve this isolation.

Examples include:

- Namespaces
- cgroups

These topics will be explored later.

---

# Virtual Machines vs Containers

| Virtual Machines | Containers |
|------------------|------------|
| Hardware-level virtualization | OS-level virtualization |
| Complete Guest Operating System | Shared Host Operating System |
| Own Kernel | Shared Host Kernel |
| Heavy | Lightweight |
| Higher Resource Consumption | Lower Resource Consumption |
| Slower Startup | Faster Startup |
| Larger Disk Usage | Smaller Images |
| Strong Hardware Isolation | Process Isolation |
| Minutes to Boot | Seconds to Start |

---

# Mental Model

Imagine building houses.

### Virtual Machines

Every family builds an independent house.

Each house has:

- Foundation
- Electricity
- Water
- Walls
- Roof

Everything is independent.

---

### Containers

Imagine a large apartment building.

Every family has its own apartment.

The building shares:

- Foundation
- Electricity
- Water
- Elevators

Each apartment remains isolated while sharing common infrastructure.

---

# Real World Example

Suppose a server has:

- 32 GB RAM
- 8 CPU Cores

Running five Virtual Machines means each VM requires its own operating system.

Running five Containers allows all applications to share the Host Kernel while consuming significantly fewer resources.

---

# When to Use Virtual Machines

Use Virtual Machines when:

- Running different operating systems
- Strong isolation is required
- Legacy applications require dedicated operating systems
- Infrastructure-level virtualization is needed

---

# When to Use Containers

Use Containers when:

- Packaging applications
- Building microservices
- Creating CI/CD pipelines
- Running cloud-native applications
- Ensuring environment consistency

---

# Interview Explanation (60 Seconds)

Virtual Machines virtualize hardware by running multiple complete operating systems on the same physical machine. Every Virtual Machine includes its own kernel, operating system, and resources, making it highly isolated but relatively heavy.

Containers virtualize the operating system by sharing the Host Kernel while packaging only the application and its runtime dependencies. This makes containers lightweight, portable, and much faster to start.

---

# Common Misconceptions

❌ Containers are Virtual Machines.

✅ Containers and Virtual Machines use different architectures.

---

❌ Containers contain a complete operating system.

✅ Containers share the Host Kernel.

---

❌ Docker replaced Virtual Machines.

✅ Docker complements Virtual Machines. Many production Kubernetes clusters run inside Virtual Machines on cloud providers.

---

# Key Takeaways

- Virtual Machines virtualize hardware.
- Containers virtualize the operating system.
- Every Virtual Machine has its own operating system.
- Containers share the Host Kernel.
- Virtual Machines provide stronger isolation.
- Containers are lighter and start faster.
- Both technologies solve different problems and often work together.

---

# My Understanding

Both Virtual Machines and Containers are used to isolate applications.

A Virtual Machine behaves like a separate computer because it has its own operating system and kernel, making it heavier and slower.

A Container does not need a separate operating system. It shares the host kernel and packages only the application with its runtime and dependencies. This makes containers lightweight, faster, and more efficient.

In short, Virtual Machines virtualize hardware, while Containers virtualize the operating system.

---

# Questions

- What exactly is the Linux Kernel?
- How do containers share the Host Kernel?
- What are Namespaces?
- What are cgroups?
- Why are containers much faster than Virtual Machines?

---
