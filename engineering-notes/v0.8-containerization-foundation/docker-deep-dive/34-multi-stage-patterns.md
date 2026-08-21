Multi-Stage Build Patterns

1. Why Multi-Stage Builds Matter

A Docker image often needs tools during the build that are not required
when the application actually runs.

For example:

Build stage
    ↓
Compiler
Package manager
Build tools
Source code
    ↓
Application artifact
    ↓
Runtime stage
    ↓
Only what the application needs

Without multi-stage builds, build dependencies can remain inside the
final image.

Multi-stage builds let us separate:

Build environment
        from
Runtime environment

The core idea is:

Build with everything you need. Run with only what you need.

2. Basic Multi-Stage Structure

A multi-stage Dockerfile uses multiple FROM instructions.

Example:

FROM node:22 AS builder

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

The stages are:

builder
   ↓
Build application
   ↓
dist/
   ↓
runtime
   ↓
Serve application

The final image is based on:

FROM nginx:alpine

not the builder image.

3. Build Stage vs Runtime Stage

Think of the Dockerfile as two environments.

Build stage

Contains:

Source code
Compiler
Build tools
Package manager
Development dependencies

Runtime stage

Contains:

Runtime
Application artifact
Required runtime dependencies
Configuration

Conceptually:

┌──────────────────────┐
│ Build stage          │
│                      │
│ Source               │
│ Compiler             │
│ Build tools          │
│ Dependencies         │
└──────────┬───────────┘
           │
           │ artifact
           ↓
┌──────────────────────┐
│ Runtime stage        │
│                      │
│ Runtime              │
│ Application          │
└──────────────────────┘

4. Why Not Just Use One Stage?

A single-stage build might look like:

FROM node:22

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

CMD ["node", "server.js"]

The resulting image may contain:

Build tools
Development dependencies
Source code
Package manager
Application

If those build-time components are not needed at runtime, the final
image contains unnecessary material.

Multi-stage builds allow us to leave those components behind.

5. Final Image Contains Only What Is Copied Into It

This is one of the most important concepts.

Suppose:

FROM node:22 AS builder
...
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

The final stage starts from:

nginx:alpine

and explicitly copies:

/app/dist

from the builder.

Therefore:

builder compiler
builder source
builder node_modules

are not automatically included in the final image.

The final stage gets what it needs from its own base image plus the
files explicitly copied into it.

6. Named Stages

A stage can be named:

FROM node:22 AS builder

The name:

builder

can then be referenced later:

COPY --from=builder /app/dist /usr/share/nginx/html

This is clearer than referring to stages only by numeric index.

A useful convention is:

builder
test
runtime

or:

frontend-builder
backend-builder
runtime

depending on the project.

7. COPY --from

The key mechanism for moving artifacts between stages is:

COPY --from=builder /app/dist /app/dist

Conceptually:

builder stage
      ↓
/app/dist
      ↓
COPY --from
      ↓
runtime stage
      ↓
/app/dist

This creates an explicit boundary between the build environment and the
runtime image.

8. Stage Numbering

Stages can also be referenced by their position.

For example:

FROM node:22

RUN npm run build

FROM nginx:alpine

COPY --from=0 /app/dist /usr/share/nginx/html

Here:

Stage 0
   ↓
First FROM

is referenced using:

--from=0

Named stages are generally easier to maintain because inserting another
stage does not require updating numeric references.

9. Builder Pattern

The most common pattern is:

Builder
   ↓
Compile / package
   ↓
Artifact
   ↓
Runtime

Example:

FROM golang:1.24 AS builder

WORKDIR /src

COPY . .

RUN go build -o /app

FROM alpine:latest

COPY --from=builder /app /app

ENTRYPOINT ["/app"]

The Go compiler exists in:

builder

but the final runtime image only needs:

/app

and the runtime environment.

10. Compiled Application Pattern

Multi-stage builds are especially useful for compiled applications.

Common examples:

Go
Rust
C/C++
Java
.NET

The pattern is:

Source
   ↓
Compiler / build tools
   ↓
Binary / package
   ↓
Minimal runtime

For example:

Go source
   ↓
go build
   ↓
Static binary
   ↓
Small runtime image

This can significantly reduce the final image footprint.

11. Frontend Build Pattern

Frontend applications often follow:

Node.js
   ↓
npm install
   ↓
npm run build
   ↓
dist/

But the runtime may only need:

Static HTML
CSS
JavaScript

A multi-stage pattern is therefore:

FROM node:22 AS builder

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

The final image does not need Node.js just to serve static files.

12. Backend Runtime Pattern

A backend application can also use separate build and runtime stages.

For example:

Builder
   ↓
Install/build dependencies
   ↓
Create application artifact
   ↓
Runtime
   ↓
Run application

The runtime image should contain:

Application
+
Required runtime dependencies
+
Runtime configuration

and not unnecessary development tooling.

13. Development Dependencies vs Runtime Dependencies

This distinction is important.

For example:

Development dependencies
    ↓
Testing
Linting
Compilers
Build tools

Runtime dependencies
    ↓
Libraries required by application

A good multi-stage design tries to prevent development-only components
from entering the runtime image when they are not required.

Conceptually:

dev dependencies
      ↓
builder only

runtime dependencies
      ↓
runtime image

14. Test Stage Pattern

Multi-stage builds can also include a dedicated testing stage.

For example:

FROM python:3.12 AS test

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN pytest

The test stage can validate the application without becoming the final
production image.

The architecture becomes:

Source
  ↓
Test stage
  ↓
Tests pass
  ↓
Production stage

15. Build + Test + Runtime

A more advanced structure can look like:

builder
   ↓
Build artifact
   ↓
tester
   ↓
Tests
   ↓
runtime
   ↓
Production image

Conceptually:

FROM ... AS builder
# build

FROM builder AS test
# test

FROM ... AS runtime
# copy artifact

This can create clear separation between:

Build
Test
Runtime

16. Reusing a Common Base Stage

A common base stage can reduce duplication.

For example:

FROM python:3.12 AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base AS test

COPY . .
RUN pytest

FROM base AS runtime

COPY . .
CMD ["python", "app.py"]

The conceptual structure is:

base
 ├── test
 └── runtime

This can be useful when multiple stages need the same common
environment.

17. Development and Production Targets

Multi-stage Dockerfiles can support different targets.

For example:

FROM node:22 AS base
...

FROM base AS development
CMD ["npm", "run", "dev"]

FROM base AS production
RUN npm run build
...

Then the build can target a particular stage.

Conceptually:

Dockerfile
    ↓
Multiple possible targets
    ├── development
    └── production

This allows one Dockerfile to describe multiple related image purposes.

18. --target

Docker can build a specific stage using:

docker build --target builder .

or:

docker build --target test .

This is useful for:

Debugging
Testing
Development workflows
CI pipelines

For example:

--target test
    ↓
Build test stage
    ↓
Run tests

The final production stage does not have to be the only stage you build.

19. Stages Are Build Boundaries

A useful mental model is:

Stage A
    ↓
Artifact boundary
    ↓
Stage B

Files do not automatically flow from every previous stage into the final
image.

You explicitly select what to copy.

For example:

COPY --from=builder /app/bin/myapp /usr/local/bin/myapp

This makes the boundary visible.

20. Multi-Stage Builds and Security

Smaller runtime images can reduce the amount of unnecessary software
present in production.

For example, a builder might contain:

Compiler
Git
Package manager
Debugging tools
Development libraries

If these are not needed at runtime, leaving them out can reduce:

Attack surface
Image size
Unnecessary packages

However:

A smaller image is not automatically a secure image.

You still need:

Minimal privileges
Dependency scanning
Secret management
Secure configuration
Up-to-date base images

21. Multi-Stage Builds and Secrets

Build-time credentials should not simply be copied into the final stage.

Avoid:

COPY .env .

or:

ARG SECRET=value

for sensitive production secrets.

Use appropriate BuildKit secret mechanisms when a build genuinely
requires temporary credentials.

The multi-stage boundary helps prevent accidental inclusion of files
that are never copied into the final stage, but secret handling still
needs deliberate design.

22. Multi-Stage Builds and Image Size

Suppose:

Single-stage image
    ↓
1.2 GB

and:

Multi-stage runtime image
    ↓
200 MB

The exact numbers are workload-dependent.

The improvement comes from removing components such as:

Compilers
Build caches
Development tools
Source files
Unused dependencies

A smaller image can improve:

Registry transfer
Pull time
Startup time
Storage usage

but image size should not be optimized blindly at the expense of
maintainability.

23. Multi-Stage Builds and Cache

Multi-stage builds also interact with Docker build caching.

Example:

FROM node:22 AS builder

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

If only source code changes:

COPY package*.json
    ↓
Cached

npm ci
    ↓
Cached

COPY .
    ↓
Rebuild

npm run build
    ↓
Rebuild

runtime COPY
    ↓
Updated artifact

This combines two important concepts:

Multi-stage architecture
+
Cache-aware Dockerfile ordering

24. Multi-Stage Builds and CI/CD

In CI/CD, multi-stage builds are useful because the pipeline can
produce:

Source
   ↓
Docker build
   ↓
Test/build stages
   ↓
Production runtime image
   ↓
Registry

The same Dockerfile can encode part of the build process.

A CI pipeline can then:

Build
 ↓
Test
 ↓
Build runtime image
 ↓
Scan
 ↓
Push

This creates a consistent path from source to deployable image.

25. Multi-Stage Build in GitHub Actions

A simplified workflow can be:

Git push
   ↓
GitHub Actions
   ↓
docker build
   ↓
Multi-stage Dockerfile
   ↓
Production image
   ↓
Security scan
   ↓
Registry

The build environment can contain everything required to compile the
application without those tools becoming part of the runtime image.

This is especially useful in DevSecOps pipelines.

26. Multi-Stage and Docker Build Context

Multi-stage builds do not remove the need for a good build context.

You still want:

.dockerignore
+
Specific COPY instructions

For example:

.git
node_modules
.env
logs

should generally not become unnecessary build inputs.

The mental model is:

Build context
    ↓
Builder stage
    ↓
Artifact
    ↓
Runtime stage

27. Multi-Stage and COPY --from

A common mistake is confusing:

COPY . .

with:

COPY --from=builder ...

COPY . .

Copies files from the build context.

Host build context
       ↓
Current stage

COPY --from=builder

Copies files from another build stage.

Builder stage
       ↓
Current stage

This distinction is extremely important.

28. Multi-Stage and External Images

COPY --from can also reference an image rather than only a local build
stage.

Conceptually:

COPY --from=some-image /path/to/file /destination

The exact use case depends on the image and artifact.

The broader idea is:

Source artifact
   ↓
Copy into current stage

This can be useful for advanced image construction patterns.

29. Debugging a Multi-Stage Build

When a multi-stage build fails:

1. Identify failing stage
        ↓
2. Identify failing instruction
        ↓
3. Check stage inputs
        ↓
4. Check artifact path
        ↓
5. Check COPY --from source
        ↓
6. Check runtime dependencies
        ↓
7. Build target stage separately if useful

For example:

docker build --target builder .

can help isolate whether the problem is:

Build stage

or:

Runtime stage

30. Common Error: Artifact Missing

Suppose:

COPY --from=builder /app/dist /usr/share/nginx/html

fails because:

/app/dist

does not exist.

Do not immediately modify the runtime stage.

Check:

Did the builder complete?
        ↓
Did the build command run?
        ↓
Where did it create the artifact?
        ↓
Is the path correct?

The problem may be:

Wrong artifact path

rather than a runtime issue.

31. Common Error: Runtime Dependency Missing

A build may succeed:

Builder
   ↓
Success

but the application may fail at runtime:

Runtime
   ↓
Missing shared library / runtime dependency

This happens when the runtime stage contains the artifact but not
everything required to execute it.

The troubleshooting sequence is:

Build artifact
      ↓
Identify runtime requirements
      ↓
Check runtime base image
      ↓
Check required libraries
      ↓
Check configuration

Multi-stage builds make the boundary explicit, so runtime dependencies
must be deliberately included.

32. Common Error: Copying Too Much

A technically valid Dockerfile can still defeat the purpose of
multi-stage builds:

COPY --from=builder /app /app

If /app contains:

Source
node_modules
Build cache
Tests
Documentation
Artifact

then the final image may contain much more than necessary.

A more intentional approach is:

COPY --from=builder /app/dist /app/dist

The principle is:

Copy the runtime artifact, not the entire build environment.

33. Runtime Base Image Selection

The runtime base image should match the application's runtime
requirements.

For example:

Static frontend
    ↓
nginx/alpine or another appropriate static server

Go binary
    ↓
Minimal runtime compatible with binary requirements

Python application
    ↓
Python runtime image

Do not select the smallest possible image blindly.

The correct target is:

Minimal
+
Compatible
+
Maintainable
+
Secure

34. Distroless Runtime Pattern

Some applications can use distroless-style runtime images.

Conceptually:

Builder
   ↓
Application binary
   ↓
Distroless runtime
   ↓
Application

These images contain fewer general-purpose operating-system tools.

This can reduce attack surface, but troubleshooting can be less
convenient because tools such as:

shell
curl
ps

may not be available.

Therefore:

Security / minimalism
        vs
Operational debugging convenience

is a real engineering trade-off.

35. Multi-Stage vs Multi-Container

These concepts should not be confused.

Multi-stage build

One Dockerfile
   ↓
Multiple build stages
   ↓
Usually one final image

Multi-container architecture

Frontend container
API container
Database container
Redis container

The first is about:

Image construction

The second is about:

Application architecture

36. Multi-Stage vs Multiple Dockerfiles

You can also build separate images using separate Dockerfiles.

For example:

Dockerfile.frontend
Dockerfile.backend

Multi-stage builds solve a different problem:

One image build
   ↓
Multiple internal stages
   ↓
Controlled final artifact

The choice depends on the architecture and deployment model.

37. IncidentLab Connection

For IncidentLab, multi-stage builds introduce another layer in the
troubleshooting sequence.

Suppose:

Production container fails

Do not assume the source code is the problem.

Separate:

Build stage
    ↓
Artifact
    ↓
Runtime stage
    ↓
Container

Then investigate:

Was the artifact built correctly?
        ↓
Was the correct artifact copied?
        ↓
Does the runtime image contain required dependencies?
        ↓
Is the command correct?
        ↓
Is configuration correct?

This prevents build-time and runtime failures from being mixed together.

38. Interview Takeaway

A strong interview explanation is:

"Multi-stage builds let us use different stages for building,
testing, and running an application. The builder stage can contain
compilers, development dependencies, and other build tools, while the
final runtime stage starts from an appropriate runtime image and
copies only the required artifact using COPY --from. This reduces
final image size, avoids carrying unnecessary build tooling into
production, and creates a clear build-to-runtime boundary."

The simplest mental model is:

Build with everything
        ↓
Produce artifact
        ↓
Run with only what is required

39. Key Takeaways

Multi-stage builds use multiple FROM instructions.

Each FROM begins a separate build stage.

Stages can be named using AS.

COPY --from transfers selected artifacts between stages.

The final stage determines the final image base.

Build tools do not automatically enter the final stage.

Multi-stage builds separate build-time and runtime concerns.

They are useful for compiled applications and frontend builds.

Dedicated test stages can validate code without becoming the
production image.

Common base stages can reduce duplication.

--target can build a specific stage.

Multi-stage builds can reduce final image size and unnecessary
attack surface.

Smaller images are not automatically more secure.

Runtime dependencies must still be included deliberately.

Copy only the artifacts needed by the runtime stage.

Multi-stage builds work especially well with cache-aware Dockerfile
ordering.

.dockerignore is still important.

Multi-stage builds are useful in CI/CD and DevSecOps pipelines.

Build-time secrets should use appropriate secret mechanisms.

Multi-stage builds are about image construction, not multi-container
architecture.

Distroless runtimes are an optional advanced pattern with
operational trade-offs.

Debugging should separate build-stage failures from runtime-stage
failures.

40. Connections

Previous

33-dockerfile-cache-invalidation.md

Next

35-docker-buildkit.md

41. My Understanding

Multi-stage builds are best understood as:

Stage 1
Builder
   ↓
Source + build tools
   ↓
Artifact
   ↓
Stage 2
Runtime
   ↓
Artifact + runtime requirements
   ↓
Final image

The important boundary is:

Build environment
        ≠
Runtime environment

For example:

FROM node:22 AS builder

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

Here:

Node.js + npm + source
        ↓
Builder only

dist/
        ↓
Runtime image

The key lesson is:

A production image should contain what the application needs to run,
not everything that was needed to build it.
