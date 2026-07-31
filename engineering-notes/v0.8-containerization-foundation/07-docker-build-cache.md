# Docker Build Cache

---

# Objective

Understand how Docker Build Cache works internally, how Docker decides whether to reuse a layer or rebuild it, and how proper cache optimization significantly improves build performance in local development and CI/CD pipelines.

---

# Why Build Cache Matters

Imagine your application takes 10 minutes to build.

Now suppose you only changed one line of code.

Should Docker rebuild everything?

No.

That would waste:

- Time
- CPU
- Network Bandwidth
- CI/CD Resources

Docker solves this using **Build Cache**.

Instead of rebuilding every layer, Docker reuses previously built layers whenever possible.

---

# What is Docker Build Cache?

Docker Build Cache is a mechanism that stores previously built image layers.

During the next build, Docker compares each Dockerfile instruction with its cached version.

If nothing has changed, Docker reuses the cached layer instead of rebuilding it.

---

# Build Process

Suppose we have the following Dockerfile.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

First Build

```
FROM
↓

WORKDIR

↓

COPY requirements.txt

↓

RUN pip install

↓

COPY source code

↓

CMD
```

Everything executes.

Docker stores every generated layer in the local cache.

---

# Second Build (No Changes)

Nothing has changed.

Docker checks every instruction.

```
FROM                ✅ Cache

WORKDIR             ✅ Cache

COPY requirements   ✅ Cache

RUN pip install     ✅ Cache

COPY source         ✅ Cache

CMD                 ✅ Cache
```

No layer is rebuilt.

The build completes almost instantly.

---

# Third Build (Application Code Changed)

Suppose only

```
app.py
```

has changed.

Docker performs:

```
FROM                ✅ Cache

WORKDIR             ✅ Cache

COPY requirements   ✅ Cache

RUN pip install     ✅ Cache

COPY source         ❌ Rebuild

CMD                 ❌ Rebuild
```

Everything before the changed layer is reused.

Everything after the changed layer is rebuilt.

---

# Cache Invalidation

Docker cache works sequentially.

As soon as one layer changes,

every layer after it becomes invalid.

Example

```
Layer 1 ✅

Layer 2 ✅

Layer 3 ❌ Changed

Layer 4 ❌ Rebuilt

Layer 5 ❌ Rebuilt

Layer 6 ❌ Rebuilt
```

Docker never skips ahead.

---

# Why Dockerfile Order Matters

Poor Dockerfile

```dockerfile
COPY . .

RUN pip install -r requirements.txt
```

Every code change forces dependency installation again.

Very slow.

---

Better Dockerfile

```dockerfile
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
```

Now dependency installation is cached.

Only application code rebuilds.

---

# Cache Keys

Docker does not simply compare filenames.

It compares:

- Dockerfile instruction
- File contents
- Previous Layer ID
- Build Context

If any of these change,

the cache becomes invalid.

---

# Build Context

When you execute

```bash
docker build .
```

everything inside the build context is sent to Docker.

Even unnecessary files affect cache efficiency.

Examples:

- .git/
- node_modules/
- __pycache__/
- logs/
- build artifacts

These should be excluded using

```
.dockerignore
```

---

# Why .dockerignore Matters

Without

```
.dockerignore
```

Docker sends unnecessary files during every build.

This increases:

- Build Time
- Cache Invalidations
- Disk Usage

A proper `.dockerignore` keeps builds smaller and faster.

---

# BuildKit

Modern Docker uses **BuildKit**.

BuildKit improves:

- Parallel Builds
- Better Cache Management
- Faster Image Builds
- Secret Management
- Advanced Mount Options

BuildKit is now the recommended build engine for Docker.

---

# Cache Mounts

BuildKit supports cache mounts.

Example

```
RUN --mount=type=cache,target=/root/.cache/pip
```

Instead of downloading packages repeatedly,

Docker reuses cached package files.

This significantly speeds up dependency installation.

---

# Remote Cache

Large organizations often share Docker cache between CI/CD runners.

Instead of rebuilding everything,

new runners download cache metadata.

Benefits:

- Faster CI/CD Pipelines
- Lower Infrastructure Cost
- Reduced Build Time

Examples:

- GitHub Actions Cache
- GitLab CI Cache
- AWS CodeBuild Cache

---

# Cache Busting

Sometimes Docker should ignore the cache.

Example:

```dockerfile
RUN apt update
```

Docker may reuse an old cached layer.

To force rebuilding,

developers intentionally invalidate the cache.

Common approaches:

- Modify a build argument
- Change the Dockerfile instruction
- Use

```bash
docker build --no-cache
```

---

# Build Flow

```
Dockerfile

      │

Instruction

      │

Layer Exists?

      │

Yes ───────────────► Reuse Cache

No

      │

Create New Layer

      │

Store in Cache

      │

Continue
```

---

# Real World Example

Imagine preparing tea.

```
Boil Water

↓

Add Tea Leaves

↓

Add Milk

↓

Add Sugar
```

If you only change the amount of sugar,

you don't boil the water again.

Docker Build Cache works exactly the same way.

Only the affected step and everything after it is repeated.

---

# Interview Explanation (90 Seconds)

Docker Build Cache stores previously built image layers and reuses them during future builds. Docker evaluates Dockerfile instructions sequentially. If an instruction and its inputs remain unchanged, Docker reuses the cached layer. Once a layer changes, all subsequent layers are rebuilt. Proper Dockerfile ordering and the use of `.dockerignore` significantly improve cache efficiency and reduce build times. Modern Docker uses BuildKit for advanced caching, parallel builds, and better performance.

---

# Production Best Practices

- Keep frequently changing instructions near the bottom.
- Install dependencies before copying application code.
- Use `.dockerignore`.
- Enable BuildKit.
- Reuse dependency layers.
- Use cache mounts where possible.
- Keep build context small.
- Avoid unnecessary cache invalidation.

---

# Common Misconceptions

❌ Docker compares only filenames.

✅ Docker compares instructions, file contents, previous layers, and build context.

---

❌ Every Docker build starts from scratch.

✅ Docker aggressively reuses cached layers.

---

❌ `.dockerignore` is optional.

✅ It is essential for efficient builds.

---

❌ BuildKit only improves speed.

✅ It also introduces advanced caching and build features.

---

# Key Takeaways

- Docker Build Cache speeds up builds.
- Cache works layer by layer.
- Cache invalidation affects all following layers.
- Dockerfile order directly impacts performance.
- `.dockerignore` improves cache efficiency.
- BuildKit provides modern caching capabilities.
- Production CI/CD pipelines rely heavily on Docker Build Cache.

---

# Connections

## Previous

- 06 Docker Layers

## Next

- 08 Writing Production Dockerfiles

---

# My Understanding

Docker Build Cache allows Docker to reuse previously built image layers instead of rebuilding everything from scratch. Docker checks each Dockerfile instruction sequentially, and if nothing has changed, it reuses the cached layer. Once a layer changes, Docker rebuilds that layer and all the layers after it. Writing Dockerfiles in the correct order and using `.dockerignore` helps maximize cache efficiency and significantly reduces build times.

---

# Questions

- How does BuildKit improve caching?
- What are cache mounts?
- How is cache shared across CI/CD runners?
- How does Docker generate layer IDs?
- When should cache intentionally be disabled?

---

# Status

🟡 In Progress
