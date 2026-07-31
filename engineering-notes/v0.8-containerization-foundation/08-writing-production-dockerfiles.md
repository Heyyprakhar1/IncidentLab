# Writing Production Dockerfiles

---

# Objective

Learn how to write clean, secure, optimized, and production-ready Dockerfiles by following industry best practices instead of simply making the application work.

---

# Why Dockerfile Quality Matters

A Dockerfile is the blueprint used to build Docker Images.

A poorly written Dockerfile may still work, but it can result in:

- Large Image Sizes
- Slow Build Times
- Poor Cache Utilization
- Security Risks
- Difficult Maintenance

A production-ready Dockerfile focuses on:

- Performance
- Security
- Maintainability
- Small Image Size
- Fast Builds
- Reproducibility

---

# What is a Dockerfile?

A Dockerfile is a text file containing instructions that Docker follows to build an Image.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Docker executes every instruction from top to bottom.

---

# Dockerfile Build Flow

```
Dockerfile

      │

docker build

      │

Docker Layers

      │

Docker Image

      │

docker run

      │

Running Container
```

---

# Anatomy of a Production Dockerfile

A good Dockerfile generally follows this order.

```
FROM

↓

LABEL

↓

ENV

↓

WORKDIR

↓

COPY Dependency Files

↓

Install Dependencies

↓

COPY Application Code

↓

EXPOSE

↓

USER

↓

CMD / ENTRYPOINT
```

This order maximizes Docker Layer Caching.

---

# Example 1 – Poor Dockerfile

```dockerfile
FROM python:3.12

COPY . .

RUN pip install -r requirements.txt

CMD ["python","app.py"]
```

Problems:

- Copies unnecessary files.
- Poor cache utilization.
- Large base image.
- Runs as root.
- No working directory.
- Difficult to maintain.

Although it works, it is not production-ready.

---

# Example 2 – Better Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python","app.py"]
```

Improvements:

- Smaller base image.
- Better cache usage.
- Working directory defined.
- Smaller dependency cache.

---

# Example 3 – Production Dockerfile

```dockerfile
FROM python:3.12-slim

LABEL maintainer="your-name"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser

USER appuser

EXPOSE 8000

CMD ["python","app.py"]
```

This Dockerfile is significantly more secure and production-friendly.

---

# Understanding Each Instruction

---

## FROM

Defines the base Image.

Example:

```dockerfile
FROM python:3.12-slim
```

Always prefer smaller Images whenever possible.

Examples:

- alpine
- slim
- distroless (advanced)

---

## LABEL

Adds metadata.

Example:

```dockerfile
LABEL version="1.0"
LABEL maintainer="prakhar"
```

Useful for maintenance.

---

## ENV

Defines environment variables.

Example:

```dockerfile
ENV APP_ENV=production
```

Avoid storing secrets inside ENV.

---

## WORKDIR

Defines the working directory.

Instead of

```dockerfile
RUN cd app
```

use

```dockerfile
WORKDIR /app
```

Cleaner and reusable.

---

## COPY

Copies files into the Image.

Example

```dockerfile
COPY requirements.txt .
```

Copy dependency files before application code to maximize caching.

---

## RUN

Executes commands during Image build.

Example

```dockerfile
RUN pip install -r requirements.txt
```

Every RUN instruction creates a new Docker Layer.

Minimize unnecessary RUN instructions.

---

## EXPOSE

Documents the application's listening port.

Example

```dockerfile
EXPOSE 8000
```

It does **not** publish the port.

It only provides documentation.

---

## USER

By default,

Containers run as

```
root
```

Production applications should use a non-root user.

Example

```dockerfile
RUN useradd -m appuser

USER appuser
```

This reduces security risks.

---

## CMD

Defines the default command executed when the Container starts.

Example

```dockerfile
CMD ["python","app.py"]
```

Only one CMD should exist.

---

# Dockerfile Optimization Principles

Good Dockerfiles follow these rules.

- Use small base Images.
- Copy dependency files first.
- Install dependencies before application code.
- Keep frequently changing files near the bottom.
- Combine related RUN instructions.
- Remove unnecessary cache files.
- Use non-root users.
- Keep Images as small as possible.

---

# Choosing the Right Base Image

Large Image

```
python:3.12
```

Smaller

```
python:3.12-slim
```

Very Small

```
alpine
```

Production

```
distroless
```

Smaller Images:

- Build Faster
- Download Faster
- Consume Less Storage
- Reduce Attack Surface

---

# Why .dockerignore Matters

Without

```
.dockerignore
```

Docker copies unnecessary files.

Example

```
.git

node_modules

__pycache__

.env

logs

.idea

.vscode
```

Ignoring these files:

- Speeds up builds.
- Improves cache usage.
- Reduces Image size.

---

# Security Best Practices

Never:

- Store passwords inside Dockerfiles.
- Store API Keys.
- Store Tokens.
- Run applications as root.
- Install unnecessary packages.

Always:

- Use non-root users.
- Keep Images updated.
- Use trusted base Images.
- Scan Images for vulnerabilities.

---

# Common Mistakes

❌ Using latest tag

Prefer

```
python:3.12.4-slim
```

---

❌ Multiple unnecessary RUN commands

---

❌ Copying everything first

---

❌ Ignoring .dockerignore

---

❌ Running as root

---

❌ Using huge base Images

---

# Real World Example

Imagine packing luggage.

Bad packing

```
Everything

↓

Suitcase
```

Good packing

```
Essentials

↓

Clothes

↓

Documents

↓

Electronics
```

Organized packing saves space and makes travel easier.

Dockerfiles work similarly.

---

# Interview Explanation (90 Seconds)

A production-ready Dockerfile focuses on security, performance, maintainability, and reproducibility. It uses a minimal base image, optimizes Docker layer caching by copying dependency files before application code, minimizes image size, avoids unnecessary packages, uses a non-root user, includes a `.dockerignore` file, and follows a logical instruction order. These practices result in faster builds, smaller images, and more secure deployments.

---

# Production Checklist

✅ Small Base Image

✅ Layer Cache Optimized

✅ .dockerignore Present

✅ Non-root User

✅ No Secrets

✅ Pinned Image Version

✅ Minimal Packages

✅ Clean Dockerfile

---

# Connections

## Previous

- 06 Docker Layers
- 07 Docker Build Cache

## Next

- 09 Multi-stage Builds

---

# Key Takeaways

- Dockerfiles define Images.
- Instruction order matters.
- Cache optimization improves build speed.
- Smaller Images are better.
- Always use .dockerignore.
- Never run production containers as root.
- Security is part of Dockerfile design.

---

# My Understanding

A Dockerfile is the blueprint used to build a Docker Image. Writing a production-ready Dockerfile is not just about making the application run, but about making it secure, efficient, maintainable, and optimized. Proper instruction ordering improves Docker layer caching, while using smaller base images, non-root users, and a `.dockerignore` file results in faster, safer, and more reliable container deployments.

---

# Questions

- What is the difference between CMD and ENTRYPOINT?
- Why should production containers avoid running as root?
- Why is alpine not always the best choice?
- What are distroless images?
- How can Docker Images be scanned for vulnerabilities?

---

# Status

🟡 In Progress
