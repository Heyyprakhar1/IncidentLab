# Docker Layers

---

# Objective

Understand what Docker Layers are, why Docker uses them, how layer caching works, and how this knowledge helps write efficient and production-ready Dockerfiles.

---

# Why Do Docker Layers Exist?

Imagine you have a Python application.

Every time you make a small code change, should Docker rebuild the entire image from scratch?

Probably not.

Rebuilding everything every time would be slow and inefficient.

Docker solves this problem using **Layers**.

Each instruction in a Dockerfile creates a separate layer, allowing Docker to reuse unchanged layers during future builds.

---

# What is a Docker Layer?

A Docker Layer is an immutable, read-only filesystem created by a Dockerfile instruction.

Instead of storing the entire image as one large file, Docker stores it as multiple stacked layers.

These layers together form the final Docker Image.

---

# Docker Layer Architecture

```
+----------------------------+
| Application Source Code    |
+----------------------------+
| Python Dependencies        |
+----------------------------+
| Python Runtime             |
+----------------------------+
| Ubuntu Base Image          |
+----------------------------+
```

Each block represents a separate Docker Layer.

---

# How Layers are Created

Consider the following Dockerfile.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Docker creates one layer for almost every instruction.

```
Layer 1 → FROM python:3.12-slim

Layer 2 → WORKDIR /app

Layer 3 → COPY requirements.txt .

Layer 4 → RUN pip install

Layer 5 → COPY . .

Layer 6 → CMD
```

These layers together become the Docker Image.

---

# Layer Stack

```
Layer 6 → CMD

Layer 5 → Application Code

Layer 4 → Python Packages

Layer 3 → requirements.txt

Layer 2 → Working Directory

Layer 1 → Base Image
```

Docker combines all layers to build one final filesystem.

---

# Why Layers are Read-Only

Docker Images are immutable.

Instead of modifying an existing layer, Docker creates a new layer whenever something changes.

This ensures:

- Consistency
- Reproducibility
- Versioning
- Efficient storage

---

# Layer Caching

Suppose this Dockerfile exists.

```dockerfile
FROM python:3.12-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
```

First Build

```
FROM
↓

COPY requirements

↓

RUN pip install

↓

COPY Source Code
```

Everything executes.

---

Now suppose you only modify **app.py**.

During the next build:

```
FROM              ✅ Cache Used

COPY requirements ✅ Cache Used

RUN pip install   ✅ Cache Used

COPY Source Code  ❌ Rebuilt
```

Docker rebuilds only the changed layer and everything after it.

This is called **Layer Caching**.

---

# Why Instruction Order Matters

Consider these two Dockerfiles.

## Dockerfile A

```dockerfile
COPY . .

RUN pip install -r requirements.txt
```

Whenever any file changes,

Docker must reinstall every dependency.

Very slow.

---

## Dockerfile B

```dockerfile
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
```

If only application code changes,

Docker reuses the dependency layer.

Much faster.

---

# Layer Reuse

Docker can reuse layers between different Images.

Example

Image A

```
Ubuntu

↓

Python

↓

Flask
```

Image B

```
Ubuntu

↓

Python

↓

FastAPI
```

Docker stores identical layers only once.

This saves disk space.

---

# Copy-on-Write

Containers do not modify Image layers.

Instead,

Docker creates a small writable layer on top of the Image.

```
Writable Layer
------------------------
Image Layer
Image Layer
Image Layer
Image Layer
```

All file changes happen only inside the writable layer.

The original Image remains unchanged.

---

# Relationship Between Images, Layers and Containers

```
Dockerfile

      │

docker build

      │

Layers

      │

Docker Image

      │

docker run

      │

Writable Layer

      │

Container
```

Layers create Images.

Images create Containers.

Containers add a writable layer.

---

# Real World Example

Think of building a burger.

```
Bottom Bun

↓

Patty

↓

Cheese

↓

Vegetables

↓

Top Bun
```

Each ingredient is added separately.

If you change only the vegetables,

you don't rebuild the entire burger from scratch.

Docker Layers work similarly.

---

# Interview Explanation (60 Seconds)

Docker Images are built from multiple immutable layers. Each Dockerfile instruction typically creates a new layer. Docker caches these layers so that unchanged layers are reused during future builds, significantly improving build performance. When a container starts, Docker adds a writable layer on top of the read-only image layers, allowing the application to modify files without changing the original image.

---

# Common Misconceptions

❌ Docker Images are one large file.

✅ Docker Images consist of multiple layers.

---

❌ Every build starts from scratch.

✅ Docker reuses cached layers whenever possible.

---

❌ Containers modify Images.

✅ Containers write only to their writable layer.

---

❌ Dockerfile instruction order does not matter.

✅ Instruction order directly affects build performance.

---

# Key Takeaways

- Every Dockerfile instruction usually creates a layer.
- Layers are immutable.
- Docker caches unchanged layers.
- Instruction order affects cache efficiency.
- Containers use Copy-on-Write.
- Images remain unchanged even when Containers modify files.

---

# Connections

## Previous

- 04 Docker Architecture
- 05 Docker Images vs Containers

## Next

- 07 Docker Build Cache
- 08 Writing Production Dockerfiles

---

# My Understanding

Docker Layers divide an image into multiple read-only parts instead of storing everything as a single file. Each Dockerfile instruction usually creates a new layer, and Docker reuses unchanged layers during future builds through layer caching. When a container starts, Docker adds a writable layer on top of these read-only layers, allowing changes without modifying the original image.

---

# Questions

- How does Docker decide whether to reuse a cached layer?
- What exactly is Copy-on-Write?
- Why are layers immutable?
- How are layers stored on disk?
- What is OverlayFS?

---

# Status

🟡 In Progress
