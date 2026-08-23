FROM Instruction

1. What Is FROM?

FROM defines the base image from which a Docker image build
starts.

It establishes the initial filesystem, operating-system userspace,
installed packages, and other contents that subsequent Dockerfile
instructions build upon.

A simplified model is:

Base Image
    ↓
FROM
    ↓
Your Dockerfile instructions
    ↓
Application Image

For example:

FROM python:3.12-slim

means the image starts from the existing python:3.12-slim image rather
than from an empty filesystem.

2. Why Does FROM Exist?

An application usually needs an execution environment before its own
code can run.

For example, a Python application needs things such as:

Linux userspace
    ↓
Python runtime
    ↓
System libraries
    ↓
Application dependencies
    ↓
Application code

Building all of this manually inside every Dockerfile would be
inefficient and difficult to maintain.

A base image provides a reusable starting point.

Existing Base Image
        ↓
Add application-specific requirements
        ↓
Application Image

This is one of the core ideas behind Docker image reuse.

3. Anatomy of a FROM Statement

A common form is:

FROM python:3.12-slim

The reference can be understood as:

python
  │
  └── image/repository

3.12-slim
  │
  └── tag

So:

python:3.12-slim

identifies a particular tagged image reference.

The tag usually communicates the intended version or variant, but it
should not be treated as the same thing as an immutable digest.

4. Common Forms of FROM

Using a tagged image

FROM python:3.12-slim

This is common when the application needs a specific runtime family and
image variant.

Using an image by digest

FROM python@sha256:<digest>

A digest identifies an immutable image content reference.

This is useful when stronger reproducibility is required because the
reference points to a specific image rather than relying only on a
mutable tag.

Using scratch

FROM scratch

scratch represents an empty base.

It is useful for specially designed minimal images, but it does not
provide a normal Linux userspace, shell, package manager, or runtime by
itself.

Therefore, using scratch requires the application and its required
runtime characteristics to be suitable for such an image.

5. Base Image Is a Design Decision

Choosing a base image is not simply a syntax decision.

The base image affects:

image size

available system libraries

package management

security surface

debugging convenience

compatibility

build behaviour

runtime characteristics

For example:

FROM python:3.12

and:

FROM python:3.12-slim

represent different trade-offs.

A smaller image can reduce unnecessary packages and attack surface,
while a fuller image can provide more tools and libraries that may be
useful during development or troubleshooting.

The correct choice depends on the application's requirements.

6. FROM and Image Layers

The base image becomes the starting point of the resulting image's layer
structure.

Conceptually:

Application layers
        ↓
Your Dockerfile changes
        ↓
Base image layers

For example:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]

The application image builds on top of the layers provided by the base
image.

This is why understanding images and layers is important when reasoning
about image size, caching, and rebuild behaviour.

7. FROM and Reproducibility

A Dockerfile can use a tag:

FROM python:3.12-slim

Tags are convenient and readable, but a tag may point to different image
content over time.

For environments where stronger reproducibility is required, a digest
can be used:

FROM python@sha256:<digest>

The trade-off is operational convenience.

A tag is easier to update intentionally, while a digest gives stronger
control over exactly which image content is used.

This means base-image versioning should be treated as part of dependency
management.

8. Multiple FROM Instructions

A Dockerfile can contain more than one FROM.

This is commonly used for multi-stage builds.

For example:

FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

CMD ["python", "app.py"]

The first stage can contain tools and dependencies required to build the
application.

The final stage can contain only what is required to run it.

Conceptually:

Builder Stage
    ↓
Build dependencies / tooling
    ↓
Required output
    ↓
Final Runtime Stage
    ↓
Smaller production image

The important point is that multiple FROM instructions create separate
build stages; they do not simply stack unrelated base images into one
stage.

9. FROM and Build Context

FROM is different from instructions such as COPY.

For example:

FROM python:3.12-slim
COPY . .

FROM obtains the base image used by the build, while COPY works with
files available from the Docker build context.

FROM
  ↓
Base image

COPY
  ↓
Build context → image

Keeping this distinction clear helps when troubleshooting image-pull
problems versus missing files in the build context.

10. Common Mistakes

Using an unnecessarily large base image

For example, selecting a full development-oriented image when the
application only needs a smaller runtime environment can increase:

image size

download time

storage usage

security surface

The smallest image is not automatically the correct image, but
unnecessary content should be avoided.

Using an ambiguous or inappropriate version

For production builds, the base image should be selected deliberately.

A Dockerfile should make the intended runtime version clear enough that
another engineer can understand what environment the application
expects.

Assuming a tag is immutable

A tag is a human-friendly reference.

It does not provide the same immutability guarantee as a digest.

When strict reproducibility matters, digest pinning can be considered.

Choosing scratch without understanding runtime requirements

scratch provides no normal userspace.

An application that expects:

shell
package manager
system libraries
CA certificates
DNS-related files

may require additional runtime considerations.

A minimal image is only useful when the application can actually operate
correctly within that minimal environment.

11. Troubleshooting FROM

When a Docker build fails around FROM, first separate the problem into
a few categories.

Image cannot be resolved or pulled

Possible areas to investigate:

Image name
    ↓
Registry
    ↓
Authentication
    ↓
Network connectivity

Wrong image variant

The image may exist but not provide the expected:

runtime version

architecture

libraries

package manager

system behaviour

Build works locally but fails elsewhere

Check:

Base image reference
    ↓
Tag / digest
    ↓
Platform / architecture
    ↓
Registry access

Do not immediately assume the application code is responsible for a
failure that occurs while resolving the base image.

12. Production Relevance

In production environments, FROM should be treated as an
infrastructure and dependency decision.

A good base-image strategy considers:

supported runtime versions

security updates

image maintenance

required system dependencies

image size

reproducibility

target architecture

update strategy

The base image is part of the application's software supply chain.

Changing it can affect the application even when no application source
code changes.

13. IncidentLab Connection

IncidentLab's containerization work uses Dockerfiles to define
reproducible application environments.

The FROM instruction establishes the runtime foundation before
IncidentLab-specific layers are added.

The resulting model is:

Base Runtime
     ↓
Dependencies
     ↓
Application Files
     ↓
Runtime Configuration
     ↓
IncidentLab Container

This makes the choice of base image relevant to the same production
concerns already explored in the containerization milestone: image size,
security, caching, reproducibility, and runtime behaviour.

14. Interview Takeaway

FROM defines the base image from which a Docker image is built.

The key mental model is:

FROM
  ↓
Base environment
  ↓
Dockerfile instructions
  ↓
Application image

Important points to remember:

FROM establishes the starting point of a build.

The base image affects the resulting image's contents and
characteristics.

Tags are convenient references; digests provide stronger
immutability.

Multiple FROM instructions enable multi-stage builds.

Base-image selection is a production engineering decision, not just
Dockerfile syntax.

A build failure at FROM should first be investigated as a
base-image, registry, authentication, network, or platform issue.
