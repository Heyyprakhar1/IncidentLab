RUN Instruction

1. What Is RUN?

RUN executes a command during the Docker image build process.

For example:

RUN pip install --no-cache-dir -r requirements.txt

The command runs while Docker is building the image, and the resulting
filesystem changes become part of the image being constructed.

A simple mental model is:

Dockerfile
    ↓
RUN command
    ↓
Build-time execution
    ↓
Filesystem changes
    ↓
Image

This is fundamentally different from CMD and ENTRYPOINT, which
define what happens when the container runs.

2. Why Does RUN Exist?

A base image provides an initial environment, but applications often
need additional setup.

For example:

Base image
    ↓
Install dependencies
    ↓
Create required directories
    ↓
Install application tooling
    ↓
Prepare application environment
    ↓
Final image

RUN allows these build-time operations to be encoded in the Dockerfile
instead of performed manually after the container starts.

This makes the resulting image self-contained and reproducible.

3. Basic Usage

A common Python example is:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]

Here:

COPY requirements.txt
        ↓
RUN pip install
        ↓
Dependencies become available in the image

The pip install command runs during docker build, not when
docker run starts the container.

4. RUN Is a Build-Time Instruction

This distinction is critical.

Consider:

RUN echo "hello"
CMD ["echo", "hello"]

They do different things.

RUN

docker build
     ↓
RUN executes

CMD

docker run
     ↓
CMD executes

Mental model:

BUILD TIME
──────────
FROM
COPY
RUN
    ↓
Image


RUNTIME
───────
CMD
ENTRYPOINT
    ↓
Container process

Confusing these two stages is a common Docker troubleshooting mistake.

5. RUN and Image Layers

A RUN instruction can create a filesystem layer.

For example:

RUN apt-get update
RUN apt-get install -y curl

creates separate build steps.

Conceptually:

Layer 1 → apt metadata changes
Layer 2 → installed packages

The exact image/build implementation depends on the Docker builder, but
the important engineering concept is that Docker can cache build steps
and their filesystem results.

This makes the number and structure of RUN instructions relevant to:

image size

cache reuse

rebuild performance

cleanup strategy

6. Combining Related Commands

Consider:

RUN apt-get update
RUN apt-get install -y curl

A common production pattern is:

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

The purpose is not simply to reduce the number of lines.

The related package-management operations are kept together so that
package metadata can be cleaned within the same build step rather than
remaining in an earlier filesystem layer.

Conceptually:

Update package metadata
        ↓
Install required packages
        ↓
Clean package metadata
        ↓
Final layer contains required result

This is an important image-optimization pattern.

7. RUN and Build Cache

Docker can reuse cached build results when the relevant inputs and
instruction remain unchanged.

For example:

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

If only application source changes but requirements.txt remains
unchanged, the dependency-installation step can potentially be reused.

However, changing the inputs to an earlier step can invalidate later
cached steps.

For example:

requirements.txt changes
        ↓
RUN pip install changes
        ↓
Subsequent COPY/build steps may need to execute again

This is why Dockerfile instruction ordering matters.

8. RUN and Package Managers

A common use of RUN is installing operating-system packages.

For Debian/Ubuntu-based images:

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

For Alpine-based images:

RUN apk add --no-cache curl

The exact command depends on the base image.

This is another reason the FROM choice matters: the package manager
and available userspace are determined by the selected base environment.

9. Shell Form and Exec Form

RUN can be written using shell syntax:

RUN echo "hello"

or in exec-form JSON syntax:

RUN ["executable", "arg1", "arg2"]

The shell form is commonly used for command chains:

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

The important point is that RUN is still a build-time instruction
regardless of the syntax used.

10. Environment and Working Directory

RUN is affected by relevant Dockerfile configuration that precedes it.

For example:

WORKDIR /app

ENV APP_ENV=production

RUN pwd
RUN echo "$APP_ENV"

The commands execute with the configured working directory and
environment available to them.

This demonstrates how Dockerfile instructions build on one another:

FROM
 ↓
WORKDIR
 ↓
ENV
 ↓
RUN

The order therefore matters.

11. RUN and Multi-Stage Builds

RUN is frequently used in a builder stage.

For example:

FROM python:3.12 AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt

The build stage can contain tools and dependencies required to produce
the application output.

A later stage can copy only the required result:

FROM python:3.12-slim

COPY --from=builder /install /usr/local

Conceptually:

Builder
  ↓
RUN build/install operations
  ↓
Required output
  ↓
Final runtime image

This helps keep build tooling out of the final image.

12. Common Mistakes

Installing dependencies at container runtime

For example:

CMD ["pip", "install", "-r", "requirements.txt"]

This makes dependency installation part of container startup rather than
image construction.

Normally, dependencies that belong in the application image should be
installed during the build:

RUN pip install -r requirements.txt

Leaving package metadata behind

For example:

RUN apt-get update && apt-get install -y curl

without appropriate cleanup can leave unnecessary package metadata in
the resulting filesystem.

Where appropriate:

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

Using too many unrelated RUN commands

Splitting unrelated operations across many build steps can make
Dockerfiles harder to optimize and reason about.

The goal is not "one RUN instruction only"; it is to group operations
logically and understand their cache/layer implications.

Running build-only tools in the final image

Compilers, package-build tools, and other temporary dependencies may not
be required at runtime.

Multi-stage builds can separate these concerns.

13. Troubleshooting Mental Model

If a RUN instruction fails, first determine what kind of failure
occurred:

RUN command fails
       ↓
Is the command available?
       ↓
Does the base image provide the expected environment?
       ↓
Are required files present?
       ↓
Is WORKDIR correct?
       ↓
Are environment variables correct?
       ↓
Does the command require network/package access?
       ↓
Is the command syntax valid?

Useful debugging techniques include temporarily simplifying the command
or entering an equivalent base image interactively:

docker run --rm -it python:3.12-slim sh

Then test the relevant command manually.

This helps separate:

Dockerfile problem
    vs
Base-image problem
    vs
Command/environment problem

14. Production Relevance

RUN is one of the most important instructions for image construction
because it determines what build-time operations become part of the
resulting image.

Production-oriented use of RUN should consider:

deterministic dependency installation

cache efficiency

cleanup of temporary data

image size

security

build speed

separation of build and runtime dependencies

reproducibility

A well-structured RUN sequence can significantly improve image quality
and rebuild performance.

15. IncidentLab Connection

IncidentLab's Docker workflow uses build-time commands to prepare the
application environment before the container starts.

The pattern is:

FROM
  ↓
WORKDIR
  ↓
COPY dependency files
  ↓
RUN install dependencies
  ↓
COPY application
  ↓
Runtime command

This keeps dependency installation and other image preparation tasks
inside the build process rather than making container startup
responsible for preparing its own environment.

The same principle connects directly to the project's work around build
caching and image optimization.

16. Interview Takeaway

RUN executes commands during the Docker image build and records their
resulting filesystem changes as part of the image being constructed.

The key distinction is:

RUN
  ↓
Build time

CMD / ENTRYPOINT
  ↓
Container runtime

Important points:

RUN is executed during docker build.

It is commonly used to install dependencies and prepare the image.

Its placement affects build cache and rebuild performance.

Package-manager operations should be structured with appropriate
cleanup.

Build-only dependencies can be isolated using multi-stage builds.

RUN should not normally be used to prepare the application every
time a container starts.

A strong interview explanation is:

"I use RUN for build-time operations such as installing
dependencies or preparing the filesystem. Those changes become part of
the image, so the container can start with its environment already
prepared."
