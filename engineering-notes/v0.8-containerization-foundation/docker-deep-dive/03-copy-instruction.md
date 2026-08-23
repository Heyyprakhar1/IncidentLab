COPY Instruction

1. What Is COPY?

COPY copies files or directories from the Docker build context
into the filesystem of the image being built.

A common example is:

COPY . .

This means:

Build context
     ↓
COPY
     ↓
Image filesystem

COPY is primarily used to bring application source code, dependency
files, configuration files, and other required build inputs into the
image.

2. Why Does COPY Exist?

A Docker image starts from a base image, but the base image does not
contain your application's source code.

For example:

python:3.12-slim
       ↓
Base runtime
       ↓
COPY application files
       ↓
Application image

COPY provides the bridge between the files in the Docker build context
and the filesystem being constructed inside the image.

Without it, the Dockerfile could install a runtime and dependencies but
would have no application source to execute.

3. Basic Syntax

The basic form is:

COPY <source> <destination>

For example:

COPY requirements.txt /app/requirements.txt

This copies:

requirements.txt

from the build context into:

/app/requirements.txt

With a working directory:

WORKDIR /app

COPY requirements.txt .

the destination . refers to the current working directory:

/app/requirements.txt

4. COPY and the Build Context

One of the most important concepts around COPY is the build
context.

Consider:

docker build -t my-app .

The . specifies the build context.

Conceptually:

Current directory
       │
       │ build context
       ▼
docker build
       │
       ▼
Dockerfile
       │
       ▼
COPY source files
       │
       ▼
Image filesystem

COPY can copy files from this build context.

It cannot arbitrarily access unrelated files anywhere on the host
filesystem.

This boundary is important for both understanding Docker builds and
troubleshooting missing-file errors.

5. COPY with WORKDIR

WORKDIR and COPY are commonly used together.

For example:

WORKDIR /app

COPY requirements.txt .
COPY src/ ./src/
COPY config.yaml .

The resulting structure can look like:

/app/
├── requirements.txt
├── config.yaml
└── src/

The source paths come from the build context, while relative destination
paths are resolved using the current WORKDIR.

This gives a predictable relationship:

Build context
     ↓
   source
     ↓
   COPY
     ↓
WORKDIR-based destination

6. COPY . .

One of the most common Dockerfile patterns is:

COPY . .

With:

WORKDIR /app

this generally means:

Build context
     ↓
copy its allowed contents
     ↓
/app

However, COPY . . does not mean every file on the host machine is
copied.

It is limited by:

the build context

.dockerignore

Docker's path and copy rules

Therefore, .dockerignore plays an important role when using broad copy
patterns.

7. .dockerignore and COPY

A build context may contain files that the image does not need.

For example:

.git/
__pycache__/
node_modules/
.env

A .dockerignore file can exclude such files from the build context.

Example:

.git
__pycache__
*.pyc
.env

Then:

COPY . .

does not bring those ignored files into the build context for the build.

This is useful for:

reducing build-context size

improving build performance

preventing unnecessary files from entering the image

reducing the risk of accidentally including sensitive files

A useful mental model is:

Host directory
      ↓
.dockerignore filtering
      ↓
Build context
      ↓
COPY
      ↓
Image

8. COPY and Image Layers

COPY can contribute a filesystem layer to the image.

For example:

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

The order matters because changes to copied files can affect build-cache
reuse.

A common optimization pattern is:

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

rather than:

COPY . .
RUN pip install -r requirements.txt

Why?

If application source code changes but requirements.txt does not,
Docker can potentially reuse the dependency-installation layer.

Conceptually:

requirements.txt
      ↓
dependency layer
      ↓
application source

This reduces unnecessary dependency installation during rebuilds.

9. Copying Specific Files vs Everything

A more controlled Dockerfile may copy only what is required.

For example:

COPY requirements.txt .
COPY app.py .
COPY src/ ./src/

instead of:

COPY . .

The explicit approach makes the image contents more obvious and can
reduce accidental inclusion of unnecessary files.

However, COPY . . can still be appropriate when the project structure
and .dockerignore are well controlled.

The correct choice depends on the application and build requirements.

10. COPY and File Ownership

Files copied into an image may need appropriate ownership when the
application runs as a non-root user.

For example:

COPY --chown=appuser:appgroup . .

This can set the ownership of copied files as part of the copy
operation.

This can be preferable to:

COPY . .
RUN chown -R appuser:appgroup /app

because a separate recursive ownership change can create additional
filesystem changes and unnecessary work.

This relates directly to image-layer optimization and non-root container
execution.

11. COPY in Multi-Stage Builds

COPY can also transfer files from one build stage to another.

For example:

FROM python:3.12 AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

CMD ["python", "app.py"]

Here:

Builder stage
     │
     │ COPY --from
     ▼
Final stage

The final image can receive only the required output from the builder
rather than inheriting all of the builder's tooling and intermediate
files.

This is one of the main mechanisms behind multi-stage image
optimization.

12. COPY vs ADD

Both can copy files into an image, but they should not automatically be
treated as interchangeable.

COPY is intentionally focused on copying files and directories.

ADD provides additional Docker-specific behaviour, such as archive
handling and other supported source semantics.

For straightforward file and directory copying, COPY is generally the
clearer choice.

A practical rule is:

Need straightforward copying?
        ↓
Use COPY

Use ADD only when its additional behaviour is actually required.

13. Common Mistakes

Assuming COPY can access any host path

It cannot arbitrarily copy files outside the build context.

If a required file is outside the context, reconsider the build context
or project layout rather than trying to bypass Docker's build boundary.

Forgetting .dockerignore

A broad:

COPY . .

without an appropriate .dockerignore can send unnecessary files into
the build context and potentially into the image.

Copying source before dependency files

For example:

COPY . .
RUN pip install -r requirements.txt

can make dependency installation less cache-efficient when source files
change frequently.

A common alternative is:

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

Fixing ownership with unnecessary recursive commands

Instead of:

COPY . .
RUN chown -R appuser:appgroup /app

consider:

COPY --chown=appuser:appgroup . .

when appropriate.

14. Troubleshooting Mental Model

If a file is missing inside the container, work through the path
systematically:

Does the file exist?
        ↓
Is it inside the build context?
        ↓
Is it excluded by .dockerignore?
        ↓
Is the COPY source path correct?
        ↓
Is the COPY destination correct?
        ↓
Is WORKDIR affecting the relative destination?
        ↓
Is the file present in the resulting image?

Useful checks include:

docker build -t my-app .

and inspecting the resulting image/container:

docker run --rm -it my-app sh

Then:

pwd
ls -la

This helps distinguish:

Build-context problem
      vs
.dockerignore problem
      vs
COPY path problem
      vs
Runtime path problem

15. Production Relevance

COPY is more than a simple file-transfer instruction.

Its placement and usage can affect:

image contents

image size

build context size

build-cache efficiency

security

file ownership

reproducibility

multi-stage build design

A production Dockerfile should therefore copy only what the image
actually needs and should structure copies deliberately.

16. IncidentLab Connection

IncidentLab's containerization workflow uses COPY to move application
and dependency files from the build context into the image.

The same pattern supports the production-oriented concerns already
explored in the containerization milestone:

Build context
     ↓
.dockerignore
     ↓
COPY required files
     ↓
Dependency installation
     ↓
Application image

The ordering of dependency files and application source is particularly
important when optimizing rebuild performance.

The use of ownership-aware copying also connects COPY with the
non-root execution and image-layer optimization practices used in the
project.

17. Interview Takeaway

COPY copies files or directories from the Docker build context into
the image filesystem.

The key mental model is:

Build Context
     ↓
.dockerignore
     ↓
COPY
     ↓
Image Filesystem

Important points to remember:

COPY works with the Docker build context.

.dockerignore controls what enters that context.

WORKDIR affects relative destination paths.

Copy ordering can affect build-cache efficiency.

COPY --chown can help avoid unnecessary ownership-fix layers.

COPY --from is important for multi-stage builds.

COPY is generally preferred over ADD for straightforward file
copying.
