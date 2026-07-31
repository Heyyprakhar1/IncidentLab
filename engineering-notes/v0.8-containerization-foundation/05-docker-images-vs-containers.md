# Docker Images vs Containers

---

# Objective

Understand the difference between Docker Images and Containers, how they are related, and why both are essential in the Docker ecosystem.

---

# Why This Concept Matters

One of the most common beginner misconceptions is thinking that an Image and a Container are the same thing.

They are closely related but serve completely different purposes.

Understanding this difference is essential before learning Docker Layers, Dockerfiles, and Image Optimization.

---

# What is a Docker Image?

A Docker Image is a **read-only blueprint** used to create one or more containers.

It contains everything required to run an application.

This includes:

- Application Code
- Runtime
- Libraries
- Dependencies
- Environment Variables
- Configuration Files

An Image is **not running**.

Think of it as a packaged application waiting to be executed.

---

# Characteristics of Docker Images

Docker Images are:

- Read-only
- Immutable
- Reusable
- Versioned
- Portable

An Image cannot execute code by itself.

It must first be converted into a Container.

---

# What is a Docker Container?

A Docker Container is a **running instance of a Docker Image**.

When Docker starts an Image, it creates an isolated environment called a Container.

The Container becomes a running process on the Host Machine.

Unlike Images, Containers can:

- Execute code
- Read and write files
- Communicate over the network
- Consume CPU and Memory
- Start and Stop

---

# Image to Container

```
Docker Image
      │
docker run
      │
      ▼
Docker Container
```

The Image acts as the source.

The Container is the running application.

---

# Real World Analogy

Imagine a cake recipe.

The recipe itself is not edible.

It only contains instructions.

```
Recipe
   │
Follow Instructions
   │
Cake
```

Similarly,

```
Docker Image
      │
docker run
      │
Docker Container
```

The Image is the recipe.

The Container is the actual cake.

---

# Another Analogy

Think about Object-Oriented Programming.

```
Class
   │
Object
```

A Class defines what an object should look like.

The Object is the actual running instance.

Docker follows the same idea.

```
Image
   │
Container
```

Image = Blueprint

Container = Running Instance

---

# One Image, Multiple Containers

A single Docker Image can create multiple Containers.

Example:

```
              Ubuntu Image

           /       |        \

Container A   Container B   Container C
```

Every Container is independent.

Stopping one Container does not affect the others.

---

# Lifecycle

Docker Image

↓

docker run

↓

Running Container

↓

Stopped Container

↓

Removed Container

The Image still exists.

Containers come and go.

Images remain available until they are explicitly removed.

---

# Image Storage

Images are stored locally inside Docker.

Example:

```
docker images
```

Docker checks the local Image cache before downloading from Docker Hub.

If the Image does not exist locally, Docker pulls it automatically.

---

# Container Storage

Containers contain a small writable layer.

Everything written inside this layer exists only while the Container exists.

If the Container is removed, the writable layer is also removed.

Persistent data should therefore be stored in Docker Volumes.

(Volumes will be covered later.)

---

# Image vs Container

| Docker Image | Docker Container |
|---------------|------------------|
| Blueprint | Running Instance |
| Read-only | Writable |
| Immutable | Temporary |
| Cannot Execute | Executes Applications |
| Stored on Disk | Running Process |
| Can Create Many Containers | Created From One Image |

---

# Relationship Between Image and Container

The relationship is simple.

```
Build

Dockerfile

      │

docker build

      │

Docker Image

      │

docker run

      │

Docker Container
```

Dockerfiles create Images.

Images create Containers.

Containers run Applications.

---

# What Happens Internally?

Suppose you execute:

```bash
docker run nginx
```

Docker performs the following steps.

```
Docker CLI

      │

Docker Daemon

      │

Image Available?

      │

No

      │

Pull Image

      │

Create Writable Layer

      │

Create Container

      │

Start Process

      │

Running Container
```

---

# Important Observations

A Container never exists without an Image.

One Image can create many Containers.

Deleting a Container does not delete its Image.

Deleting an Image does not automatically stop running Containers.

---

# Interview Explanation (60 Seconds)

A Docker Image is a read-only template that contains an application's code, runtime, libraries, dependencies, and configuration. It cannot execute by itself.

A Docker Container is a running instance of that Image. Containers execute applications, consume system resources, and maintain a temporary writable layer while sharing the Host Linux Kernel.

---

# Common Misconceptions

❌ Image and Container are the same thing.

✅ A Container is created from an Image.

---

❌ Images execute applications.

✅ Containers execute applications.

---

❌ Every Container needs its own Image.

✅ One Image can create multiple Containers.

---

❌ Deleting a Container deletes the Image.

✅ Images remain unless explicitly removed.

---

# Key Takeaways

- Images are blueprints.
- Containers are running instances.
- Images are immutable.
- Containers are temporary.
- One Image can create many Containers.
- Containers share the Host Linux Kernel.
- Images are created using Dockerfiles.

---

# Connections

## Previous

- 01 Why Docker
- 02 Virtual Machines vs Containers
- 03 Linux Kernel Fundamentals
- 04 Docker Architecture

## Next

- 06 Docker Layers
- 07 Docker Build Cache

---

# My Understanding

A Docker Image is a read-only blueprint that contains everything required to run an application, but it cannot run by itself. When Docker starts an Image, it creates a Container, which is the running instance of that Image. One Image can create multiple independent Containers, and while Containers can be created or removed, the original Image remains unchanged.

---

# Questions

- Why are Docker Images immutable?
- What is the writable layer of a Container?
- How are Images actually built?
- Why does Docker use Layers instead of one large Image?

---

# Status

🟡 In Progress
