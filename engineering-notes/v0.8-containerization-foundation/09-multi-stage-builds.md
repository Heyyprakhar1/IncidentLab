# Multi-stage Builds

---

# Objective

Understand what Multi-stage Builds are, why they are used, and how they help create smaller, more secure, and production-ready Docker Images.

---

# Why Multi-stage Builds Exist

While writing Dockerfiles, developers often need tools that are required only during the build process.

Examples:

- Compiler
- Node.js
- Maven
- Gradle
- Go Compiler
- Build Dependencies

After the application is built, these tools are no longer required.

However, if they remain inside the final Docker Image, they:

- Increase Image Size
- Increase Security Risks
- Increase Attack Surface
- Waste Storage

Multi-stage Builds solve this problem.

---

# What is a Multi-stage Build?

A Multi-stage Build is a Docker build technique where multiple stages are defined in a single Dockerfile.

Each stage has its own purpose.

Typically:

- Build Stage
- Runtime Stage

Only the required output from the build stage is copied into the final runtime image.

---

# Single-stage Build

```
Dockerfile

      │

Base Image

      │

Install Compiler

      │

Install Dependencies

      │

Copy Source Code

      │

Build Application

      │

Run Application
```

Everything remains inside the final Image.

---

# Problems with Single-stage Builds

Final Image contains:

- Source Code
- Build Tools
- Compiler
- Package Manager
- Cache Files
- Runtime

Most of these are unnecessary in production.

---

# Multi-stage Build

```
Stage 1

Compiler

↓

Dependencies

↓

Build Application

↓

Generated Artifacts

----------------------------

Stage 2

Minimal Runtime

↓

Copy Built Files

↓

Run Application
```

Only the built application is copied.

Everything else is discarded.

---

# Example – Node.js Application

Single-stage Dockerfile

```dockerfile
FROM node:20

WORKDIR /app

COPY . .

RUN npm install

RUN npm run build

CMD ["npm","start"]
```

Problems:

- Node build tools remain.
- npm cache remains.
- Source code remains.
- Large image size.

---

# Multi-stage Version

```dockerfile
FROM node:20 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx","-g","daemon off;"]
```

Docker creates two independent stages.

Only the build output is copied into the runtime image.

---

# Understanding FROM

Every new

```dockerfile
FROM
```

starts a completely new build stage.

Example

```dockerfile
FROM node:20 AS builder
```

creates

Stage 1

Later

```dockerfile
FROM nginx:alpine
```

creates

Stage 2

These stages are isolated.

---

# Understanding AS

```
FROM node:20 AS builder
```

The keyword

```
AS builder
```

assigns a name to the build stage.

Later we can reference it.

Example

```dockerfile
COPY --from=builder
```

---

# COPY --from

Instead of copying files from the local machine,

Docker copies files directly from another build stage.

Example

```dockerfile
COPY --from=builder /app/dist /usr/share/nginx/html
```

Only the compiled application is copied.

Nothing else.

---

# Build Flow

```
Source Code

      │

Stage 1

Build

↓

Compile

↓

Generate Artifacts

      │

COPY --from

      │

Stage 2

Minimal Runtime

      │

Final Docker Image
```

---

# Benefits of Multi-stage Builds

- Smaller Images
- Faster Downloads
- Better Security
- Reduced Attack Surface
- Faster Deployment
- Cleaner Runtime Images
- Easier Maintenance

---

# Real World Example

Imagine constructing furniture.

Workshop

```
Wood

↓

Cutting

↓

Polishing

↓

Painting
```

Finished Chair

↓

Home

You don't move:

- Saw
- Drill
- Paint
- Workbench

to your living room.

You only move the finished chair.

Multi-stage Builds follow exactly the same principle.

---

# Image Size Comparison

Example

Single-stage

```
850 MB
```

Multi-stage

```
95 MB
```

The exact reduction depends on the application and base image.

---

# Security Benefits

Smaller Images contain:

- Fewer Packages
- Fewer Libraries
- Fewer Vulnerabilities

Removing build tools from production reduces the attack surface.

---

# Common Use Cases

Multi-stage Builds are widely used for:

- React
- Angular
- Vue
- Go
- Rust
- Java
- .NET
- Python (some cases)

---

# Interview Explanation (90 Seconds)

A Multi-stage Build uses multiple stages within a single Dockerfile to separate the build environment from the runtime environment. The first stage contains compilers and build tools, while the final stage contains only the files required to run the application. This approach reduces image size, improves security, lowers the attack surface, and creates cleaner production images.

---

# Common Misconceptions

❌ Every Dockerfile should have only one FROM instruction.

✅ A Dockerfile can have multiple FROM instructions.

---

❌ Multi-stage Builds make applications faster.

✅ They mainly reduce image size and improve security.

---

❌ COPY always copies files from the local machine.

✅ COPY --from copies files from another build stage.

---

# Production Best Practices

- Separate build and runtime stages.
- Use minimal runtime images.
- Copy only required artifacts.
- Remove unnecessary dependencies.
- Keep runtime images as small as possible.
- Name stages using AS.

---

# Connections

## Previous

- 08 Writing Production Dockerfiles

## Next

- 10 Docker Volumes

---

# Key Takeaways

- Multi-stage Builds separate build and runtime environments.
- Multiple FROM instructions create multiple stages.
- COPY --from copies artifacts between stages.
- Final images become smaller and more secure.
- Build tools should not exist in production images.

---

# My Understanding

A Multi-stage Build allows us to use different stages within a single Dockerfile for building and running an application. The build stage contains compilers, dependencies, and other tools required during development, while the final runtime stage contains only the files needed to run the application. This results in smaller, more secure, and production-ready Docker Images.

---

# Questions

- When should I use Multi-stage Builds?
- Can every application use Multi-stage Builds?
- What is a distroless runtime image?
- How many stages can a Dockerfile have?
- Does each stage have its own cache?

---

# Status

🟡 In Progress
