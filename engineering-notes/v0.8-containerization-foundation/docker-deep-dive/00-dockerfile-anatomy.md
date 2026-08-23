Dockerfile Anatomy

1. What Is a Dockerfile?

A Dockerfile is a declarative text file that defines the instructions
Docker uses to build a container image.

Instead of manually creating a container and configuring it step by
step, we describe the required filesystem, runtime configuration,
dependencies, and startup behaviour in a Dockerfile.

A simplified flow is:

Dockerfile
    ↓
Docker Build
    ↓
Docker Image
    ↓
Container

The Dockerfile therefore acts as the build-time definition of an
image, while the container is the runtime instance created from that
image.

2. Why Does the Dockerfile Exist?

Without a Dockerfile, an application environment could be created
manually:

Create environment
    ↓
Install runtime
    ↓
Install dependencies
    ↓
Copy application
    ↓
Configure environment
    ↓
Configure startup command

The problem with this approach is that the process becomes:

manual

difficult to reproduce

easy to configure inconsistently

difficult to version

difficult to automate in CI/CD

A Dockerfile turns these requirements into a version-controlled build
definition.

Dockerfile
    ↓
Same build instructions
    ↓
Reproducible image

This is one of the reasons Docker fits naturally into CI/CD pipelines.

3. Anatomy of a Dockerfile

A Dockerfile is composed of instructions.

A simplified example:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

USER 1000

CMD ["python", "app.py"]

Each instruction has a specific responsibility.

FROM
 ↓
WORKDIR
 ↓
COPY
 ↓
RUN
 ↓
COPY
 ↓
EXPOSE
 ↓
USER
 ↓
CMD

The instructions are not random configuration lines. Together they
describe how the image should be constructed and how the resulting
container should behave.

4. Build-Time vs Runtime Instructions

One of the most important things to understand is that Dockerfile
instructions do not all serve the same purpose.

Some instructions primarily affect image construction:

FROM
RUN
COPY
ADD

Others describe runtime configuration or behaviour:

WORKDIR
ENV
EXPOSE
USER
CMD
ENTRYPOINT

This distinction matters when troubleshooting.

For example:

RUN pip install -r requirements.txt

runs while the image is being built.

Whereas:

CMD ["python", "app.py"]

defines what should happen when a container is started from that image.

5. Instruction Order Matters

Docker processes Dockerfile instructions sequentially.

For example:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

The application source is copied only after the dependency installation.

This ordering can be intentional because Docker builds images in layers
and can reuse previously built layers when their inputs have not
changed.

A common production-oriented pattern is therefore:

Copy dependency definition
        ↓
Install dependencies
        ↓
Copy application source

instead of:

Copy everything
        ↓
Install dependencies

This becomes especially important when working with Docker build cache.

6. Common Dockerfile Instructions

Instruction     Primary purpose

FROM          Defines the base image
WORKDIR       Sets the working directory
COPY          Copies files from build context into the image
ADD           Copies files with additional Docker-specific behaviour
RUN           Executes commands during image build
CMD           Provides the default container command
ENTRYPOINT    Defines the executable entrypoint
ENV           Defines environment variables
ARG           Defines build-time variables
USER          Defines the user used by the container
LABEL         Adds metadata to the image
EXPOSE        Documents the intended container port
VOLUME        Declares a mount point for persistent/external data
HEALTHCHECK   Defines container health-check behaviour

Each instruction has a different role and should be understood
independently.

7. Dockerfile Is Not the Container

A Dockerfile is a build instruction set.

It is not the running application itself.

The relationship is:

Dockerfile
    │
    │ docker build
    ▼
Docker Image
    │
    │ docker run
    ▼
Container

For example:

docker build -t my-app .

uses the Dockerfile and build context to create an image.

Then:

docker run my-app

creates a container from that image.

This distinction is important because an issue can occur at different
stages:

Dockerfile problem
      ↓
Build failure

Image problem
      ↓
Image exists but is incorrectly constructed

Runtime problem
      ↓
Container starts but application fails

Troubleshooting therefore starts by identifying which stage is
actually failing.

8. Dockerfile and Build Context

A Dockerfile does not automatically have access to every file on the
host.

Docker builds operate using a build context.

For example:

docker build -t my-app .

The . specifies the current directory as the build context.

A Dockerfile instruction such as:

COPY . .

copies files from that build context into the image.

This is why .dockerignore is important.

Unnecessary files such as:

.git/
__pycache__/
node_modules/
.env

should generally not be sent as part of the build context when they are
not required.

Reducing the build context can improve build efficiency and also prevent
sensitive or unnecessary files from entering the build process.

9. Dockerfile and Image Layers

Many Dockerfile instructions contribute filesystem changes that become
part of the image's layered structure.

For example:

FROM python:3.12-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

Conceptually:

Application layer
      ↓
Dependency layer
      ↓
Base image layers

This layered model is one reason instruction ordering matters.

If an earlier layer remains reusable, Docker can avoid repeating work
during subsequent builds.

However, Dockerfile layering also means that poorly structured
instructions can increase image size or reduce cache efficiency.

10. Production Considerations

A Dockerfile should not only make the application run.

It should also consider:

minimal and appropriate base images

dependency installation efficiency

build-cache behaviour

unnecessary files in the image

non-root execution

predictable startup behaviour

health checking where appropriate

image size

security

reproducibility

For example, running an application as a non-root user is generally
preferable to running the application process as root when root
privileges are unnecessary.

11. Common Misconceptions

EXPOSE publishes a port

Not by itself.

EXPOSE 8000

documents the intended port used by the container.

Actual host-to-container port publishing is configured when the
container is run, for example:

docker run -p 8000:8000 my-app

CMD runs during docker build

No.

CMD defines the default command for the container runtime.

Build-time commands are handled by instructions such as:

RUN

Dockerfile = Container

No.

Dockerfile → Image → Container

These are three different stages/entities.

COPY . . means copy everything from the host

Not exactly.

It copies from the Docker build context, subject to .dockerignore.

12. Troubleshooting Mental Model

When a Dockerized application fails, first identify the stage:

Is the image failing to BUILD?
        │
        ├── Dockerfile
        ├── build context
        ├── dependencies
        └── build cache
        │
        ▼
Does the container START?
        │
        ├── CMD / ENTRYPOINT
        ├── environment
        ├── permissions
        └── filesystem
        │
        ▼
Does the APPLICATION work?
        │
        ├── networking
        ├── dependencies
        ├── configuration
        └── application logs

This prevents treating every Docker problem as a generic "container
issue."

13. IncidentLab Connection

IncidentLab's containerization work follows the same Dockerfile model:

Application source
       ↓
Dockerfile
       ↓
Docker image
       ↓
Container
       ↓
Application runtime

The Dockerfile therefore becomes part of the application's reproducible
infrastructure rather than a collection of manual setup commands.

The deeper Docker concepts documented in this section --- images,
layers, build cache, runtime configuration, networking, storage,
security, and multi-stage builds --- build on this basic Dockerfile
model.

14. Interview Takeaway

A Dockerfile is a version-controlled set of instructions used to build a
Docker image.

The important mental model is:

Dockerfile
   ↓ build
Image
   ↓ run
Container

The order and choice of Dockerfile instructions matter because they
affect:

image construction

layer structure

build-cache reuse

image size

security

runtime behaviour

Understanding the anatomy of a Dockerfile therefore provides the
foundation for understanding Docker image optimization, caching,
security, debugging, and production containerization.