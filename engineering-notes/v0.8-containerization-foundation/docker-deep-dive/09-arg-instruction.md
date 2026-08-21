ARG Instruction

1. What Is ARG?

ARG defines a build-time variable that can be supplied to the Docker
build process.

Example:

ARG APP_VERSION=1.0

Mental model:

docker build
    ↓
ARG
    ↓
Build instructions

ARG is primarily about image construction, not container runtime
configuration.

2. Basic Example

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}

Then:

docker build --build-arg PYTHON_VERSION=3.13 .

can provide another value.

Conceptually:

Build argument
    ↓
Dockerfile
    ↓
Build configuration

3. ARG vs ENV

This is one of the most important distinctions.

ARG

Build-time

ENV

Image/container environment

Example:

ARG VERSION=1.0
ENV APP_VERSION=$VERSION

The flow is:

ARG
 ↓
Build
 ↓
ENV
 ↓
Runtime environment

An ARG does not automatically become a runtime environment variable.

4. Supplying an ARG

Build with:

docker build \
  --build-arg APP_VERSION=2.0 \
  .

Docker provides:

APP_VERSION=2.0

to the build where that argument is declared and available.

5. Default ARG Value

You can define:

ARG APP_VERSION=1.0

If the build does not provide another value:

APP_VERSION
    ↓
1.0

If the build provides:

--build-arg APP_VERSION=2.0

then:

APP_VERSION
    ↓
2.0

6. ARG Scope

ARG has important scope rules.

An ARG declared before the first FROM can be used in the FROM
instruction.

For example:

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}

But an argument declared in one build stage is not automatically
available in every later stage.

For example:

FROM alpine AS builder

ARG APP_VERSION

does not automatically make APP_VERSION available in a separate later
stage.

Declare it where it is needed.

7. Global ARG and Stage ARG

A common pattern is:

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION} AS builder

ARG APP_VERSION

The first ARG is available for the relevant FROM.

The second ARG is declared inside the stage.

This distinction becomes important in multi-stage builds.

8. ARG in FROM

One of the most useful cases is:

ARG NODE_VERSION=22

FROM node:${NODE_VERSION}

This allows the base image version to be changed during the build.

For example:

docker build --build-arg NODE_VERSION=24 .

The Dockerfile can therefore support controlled build-time variation.

9. ARG and Reproducibility

Build arguments can improve flexibility, but excessive variability can
reduce reproducibility.

For example:

Build A
NODE_VERSION=22

Build B
NODE_VERSION=24

can produce different images.

Production builds should therefore use:

Explicit values
+
Version control
+
Traceable build configuration

rather than arbitrary build arguments.

10. ARG and Cache

Changing an ARG can affect build cache behaviour when that argument is
used by a relevant build instruction.

Conceptually:

ARG value changes
      ↓
Relevant instruction input changes
      ↓
Cache may be invalidated

For example:

ARG APP_VERSION=1.0
RUN echo $APP_VERSION

Changing:

APP_VERSION=2.0

changes the build input for that instruction.

This connects ARG directly with Docker build caching.

11. ARG and Secrets

Do not use ARG as a secure secret mechanism.

Avoid:

docker build --build-arg API_KEY=secret .

for sensitive credentials.

Build arguments can become observable through build metadata/history
depending on how they are used.

For secret material, use an appropriate BuildKit secret mechanism.

The principle is:

ARG
 ↓
Build configuration

Not:
ARG
 ↓
Secret storage

12. ARG vs Runtime Environment

Suppose:

ARG APP_ENV=production

This does not mean a running container automatically receives:

APP_ENV=production

If runtime configuration is required, use:

ENV APP_ENV=production

or provide it at runtime.

Conceptually:

ARG
 ↓
Build

ENV
 ↓
Runtime

13. Passing ARG to ENV

You can intentionally bridge them:

ARG APP_VERSION=1.0
ENV APP_VERSION=$APP_VERSION

Now:

Build argument
      ↓
Image environment variable
      ↓
Container

For example:

docker build --build-arg APP_VERSION=2.0 .

can result in:

APP_VERSION=2.0

inside the resulting image environment.

This is useful for build metadata that genuinely belongs in runtime
configuration.

14. ARG and Labels

Build arguments can also help construct image metadata.

For example:

ARG VERSION=1.0

LABEL org.opencontainers.image.version=$VERSION

This can make the image carry traceable version information.

A CI/CD pipeline can provide the release version during the build.

15. ARG and Multi-Stage Builds

Each stage has its own scope considerations.

For example:

ARG NODE_VERSION=22

FROM node:${NODE_VERSION} AS builder

ARG APP_VERSION=1.0

FROM nginx:alpine AS runtime

ARG APP_VERSION=1.0

If the runtime stage needs an argument, declare it there.

Do not assume stage-local variables automatically carry forward.

16. Common Error: ARG Not Available

Suppose:

FROM alpine AS builder

ARG APP_VERSION

RUN echo $APP_VERSION

FROM alpine AS runtime

RUN echo $APP_VERSION

The second stage should not be assumed to inherit the first stage's
stage-local ARG.

Declare it where needed:

FROM alpine AS runtime

ARG APP_VERSION
RUN echo $APP_VERSION

This makes the scope explicit.

17. Common Error: Expecting ARG at Runtime

Suppose:

ARG PORT=8080

and the container is started:

docker run my-app

The application should not be expected to receive:

PORT=8080

unless that value was explicitly transferred to runtime configuration,
such as:

ENV PORT=$PORT

or supplied with:

docker run -e PORT=8080 my-app

18. Debugging ARG

When a build behaves differently between environments:

1. Check --build-arg values
        ↓
2. Check Dockerfile ARG defaults
        ↓
3. Check ARG scope
        ↓
4. Check where ARG is used
        ↓
5. Check cache impact
        ↓
6. Check whether the value was transferred to ENV

This is particularly useful in CI/CD where build arguments may come from
pipeline variables.

19. ARG in CI/CD

A pipeline can build an image with:

docker build \
  --build-arg APP_VERSION="$GITHUB_SHA" \
  .

The build can then embed traceability into:

Labels
Application metadata
Build artifacts

But be deliberate about what gets embedded.

Do not pass secrets through build arguments simply because CI makes them
available.

20. ARG and Base Image Versioning

A common pattern is:

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}

This makes the base version configurable.

For production, combine flexibility with controlled version management.

For example:

Source-controlled Dockerfile
        +
CI-defined approved version
        ↓
Reproducible build

21. Interview Takeaway

"ARG defines a build-time variable. It can be provided with
docker build --build-arg and is useful for things such as selecting
a base image version or injecting build metadata. ARG is different
from ENV because it is not automatically available as a runtime
environment variable. I also avoid using ARG for secrets because build
arguments can be exposed through build metadata or history."

Mental model:

ARG
 ↓
Build-time input
