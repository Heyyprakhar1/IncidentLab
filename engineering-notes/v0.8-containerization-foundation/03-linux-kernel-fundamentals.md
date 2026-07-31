# Linux Kernel Fundamentals

---

# Objective

Understand what an Operating System is, why a Kernel is needed, how applications communicate with hardware, and why the Linux Kernel is the foundation of Docker and Containers.

---

# Why Do We Need an Operating System?

Imagine using a computer without an Operating System.

If an application wanted to:

- Read a file
- Allocate memory
- Access the Internet
- Use the keyboard
- Display something on the screen

it would have to communicate directly with the hardware.

Every application would need to know how CPUs, RAM, SSDs, Keyboards, Mice and Network Cards work.

This would make software development almost impossible.

An Operating System solves this problem by acting as a bridge between applications and hardware.

---

# What is an Operating System?

An Operating System (OS) is system software that manages computer hardware and provides services for applications.

Instead of talking directly to hardware, applications communicate with the Operating System.

The Operating System ensures that hardware resources are shared safely and efficiently.

Examples:

- Ubuntu
- Debian
- Windows
- macOS

---

# Operating System Architecture

```
Applications
      │
Operating System
      │
Hardware
```

Applications never communicate directly with hardware.

The Operating System handles all communication.

---

# What is a Kernel?

The Kernel is the **core component** of an Operating System.

It is responsible for managing hardware resources and allowing applications to use them safely.

Think of the Kernel as the **brain** of the Operating System.

Every request made by an application eventually reaches the Kernel.

Without the Kernel, the Operating System cannot function.

---

# Kernel Architecture

```
Applications
      │
───────────────
 User Space
───────────────
      │
 System Calls
      │
───────────────
 Kernel Space
───────────────
      │
CPU
RAM
Storage
Network
Devices
```

The Kernel acts as the only trusted layer that can directly access hardware.

---

# Why Applications Cannot Access Hardware Directly

Imagine two applications trying to use the same RAM at the same time.

Or imagine an application trying to overwrite another application's memory.

Without a Kernel:

- Applications could corrupt each other.
- The system would frequently crash.
- Security would not exist.
- Hardware resources could not be shared properly.

The Kernel prevents these problems by controlling all hardware access.

---

# Responsibilities of the Kernel

The Kernel performs several important tasks.

---

## 1. Process Management

A process is simply a running program.

Examples:

- Chrome
- VS Code
- Docker
- Python

The Kernel:

- Creates processes
- Terminates processes
- Switches between processes
- Allocates CPU time

Without the Kernel, applications would fight for CPU resources.

---

## 2. Memory Management

Applications require memory to execute.

The Kernel:

- Allocates RAM
- Releases RAM
- Protects memory from other processes
- Prevents memory conflicts

Example:

Chrome cannot directly use memory allocated to VS Code.

The Kernel ensures complete isolation.

---

## 3. File System Management

Whenever an application reads or writes a file, it requests permission from the Kernel.

Examples:

- Reading a Python file
- Saving a Word document
- Creating a log file

The Kernel manages all file operations.

---

## 4. Device Driver Management

Hardware devices communicate through drivers.

Examples:

- Keyboard
- Mouse
- GPU
- SSD
- Printer
- Webcam

The Kernel loads and manages these drivers.

Applications do not communicate directly with hardware.

---

## 5. Networking

Whenever an application accesses the Internet, the request goes through the Kernel.

Examples:

- Opening Google Chrome
- Running curl
- Using Postman
- Docker pulling an image

The Kernel manages:

- Network Interfaces
- TCP/IP
- Packet Routing
- Ports
- Connections

---

## 6. Security & Permissions

The Kernel enforces security.

Examples:

- File permissions
- User permissions
- Process isolation
- Resource access

Applications cannot perform privileged operations without the Kernel.

---

# User Space vs Kernel Space

The Operating System is divided into two logical areas.

## User Space

Applications run here.

Examples:

- Chrome
- VS Code
- Python
- Docker CLI
- Jenkins

Applications running in User Space cannot directly access hardware.

---

## Kernel Space

The Kernel runs here.

Only the Kernel has direct access to:

- CPU
- RAM
- Disk
- Network
- Devices

Applications must request access through the Kernel.

---

# What are System Calls?

A System Call is a request made by an application to the Kernel.

Whenever an application needs hardware resources, it performs a System Call.

Examples:

- Open a file
- Allocate memory
- Create a process
- Send network packets

The Kernel receives the request and performs the operation.

---

# Example 1 – Chrome Opening a Website

```
Chrome
   │
Open https://google.com
   │
System Call
   │
Linux Kernel
   │
Network Driver
   │
Internet
```

Chrome never communicates directly with the Network Card.

The Kernel handles everything.

---

# Example 2 – Python Reading a File

```
Python Script
      │
open("data.txt")
      │
System Call
      │
Linux Kernel
      │
File System
      │
SSD
```

Again, Python never communicates directly with the SSD.

The Kernel performs the operation.

---

# Example 3 – Docker Container Requesting Memory

```
Container
      │
Needs 512 MB RAM
      │
System Call
      │
Linux Kernel
      │
Memory Manager
      │
RAM
```

Docker does **not** allocate RAM.

The Linux Kernel does.

---

# Why Containers Share the Host Kernel

Unlike Virtual Machines, Containers do not include a separate operating system.

Instead, every Container shares the Host Machine's Linux Kernel.

This makes Containers:

- Lightweight
- Faster
- More Efficient

Because they reuse the existing Kernel instead of running a new one.

---

# Why Docker Works Best on Linux

Docker relies heavily on Linux Kernel features.

Some important features include:

- Namespaces
- cgroups
- Overlay Filesystem

These features provide process isolation, resource management and filesystem layering.

We will study each of these in later chapters.

---

# Mental Model

Imagine a company.

Applications are employees.

Hardware is the office building.

The Kernel is the office manager.

Whenever an employee needs:

- A meeting room
- A computer
- Internet
- Office supplies

They ask the manager.

Employees never manage office resources themselves.

Similarly, applications never manage hardware directly.

The Kernel manages everything.

---

# Interview Explanation (60 Seconds)

The Linux Kernel is the core component of the Operating System responsible for managing hardware resources such as CPU, memory, storage, networking and devices. Applications cannot access hardware directly, so they communicate with the Kernel using System Calls. Docker containers share the Host Linux Kernel, making them lightweight and efficient because they do not require separate operating systems.

---

# Common Misconceptions

❌ Operating System and Kernel are the same.

✅ The Kernel is the core part of the Operating System.

---

❌ Applications directly communicate with hardware.

✅ Applications communicate with the Kernel.

---

❌ Docker manages CPU and RAM.

✅ The Linux Kernel manages system resources.

---

❌ Every Container has its own Kernel.

✅ All Containers running on the same host share the Host Kernel.

---

# Key Takeaways

- The Kernel is the core of the Operating System.
- Applications never access hardware directly.
- System Calls allow applications to communicate with the Kernel.
- The Kernel manages CPU, Memory, Storage, Devices, Networking and Security.
- Docker depends on Linux Kernel features.
- Containers share the Host Linux Kernel.
- Docker is not an Operating System.

---

# Connections

## Previous

- 01 Why Docker
- 02 Virtual Machines vs Containers

## Next

- 04 Docker Architecture
- 05 Docker Images vs Containers

---

# My Understanding

The Linux Kernel is the core component of an Operating System that acts as a bridge between applications and hardware. Applications cannot directly access hardware, so they communicate with the Kernel using System Calls. The Kernel manages CPU, memory, storage, networking, devices and security. Docker containers rely on the Host Linux Kernel instead of having their own, which makes them lightweight and efficient.

---

# Questions

- What are Namespaces?
- What are cgroups?
- How does Docker isolate Containers while sharing the same Kernel?
- Why does Docker Desktop require WSL2 on Windows?
- How does the Kernel schedule CPU for multiple Containers?

---

# Status

🟡 In Progress
