Dockerfile Best Practices

1. What Are Dockerfile Best Practices?

Dockerfile best practices are engineering patterns that make container
images:

predictable

maintainable

secure

efficient to build

efficient to run

easier to troubleshoot

A Dockerfile is not just a list of commands that makes an image build
successfully.

A production-oriented Dockerfile should consider:

Build
 +
Security
 +
Caching
 +
Image Size
 +
Runtime Behaviour
 +
Maintainability

The goal is:

Build the smallest, safest, most predictable image that contains
everything the application actually needs.

2. Start With the Right Base Image

The FROM instruction determines the starting point for the image.

For example:

FROM python:3.12-slim

A common mistake is selecting a large base image simply because it
contains many tools.

For example:

Large general-purpose image
        ↓
More packages
        ↓
Larger attack surface
        ↓
Larger image
        ↓
More components to patch

A smaller, purpose-appropriate base can reduce unnecessary components.

However:

Smallest is not automatically best.

The base image still needs to support the application's runtime
requirements, debugging needs, compatibility, and operational model.

3. Pin Important Base Image Versions

Avoid relying blindly on:

FROM python:latest

because the meaning of latest can change over time.

A more controlled approach is:

FROM python:3.12-slim

For stronger reproducibility, an image digest can be used:

FROM python:3.12-slim@sha256:<digest>

The general principle is:

Controlled base image
        ↓
Predictable build input
        ↓
More reproducible image

Version control and image freshness still need to be balanced
operationally.

4. Keep the Build Context Focused

The Dockerfile is only one part of the build.

The build context also matters.

A good build flow is:

Repository
    ↓
.dockerignore
    ↓
Focused build context
    ↓
Dockerfile
    ↓
Image

Avoid unnecessarily sending:

.git
node_modules
local virtual environments
logs
temporary files
build artifacts
secrets

into the build context.

This improves build efficiency and reduces accidental exposure of
irrelevant files.

5. Use .dockerignore

A production-oriented .dockerignore commonly excludes files such as:

.git
.env
*.log
__pycache__
node_modules
.venv

The exact list should be project-specific.

Remember:

.dockerignore
    ↓
Controls build context

Dockerfile
    ↓
Controls image construction

.dockerignore is therefore part of Dockerfile/build design rather than
an unrelated cleanup file.

6. Use COPY for Normal File Copying

For ordinary application files, prefer:

COPY

over:

ADD

when no ADD-specific behaviour is required.

For example:

COPY requirements.txt .
COPY src/ ./src/

The intent is immediately clear:

COPY
  ↓
Copy these files

Use ADD when its additional behaviour is intentionally required, such
as appropriate local archive extraction.

7. Structure Instructions for Cache Efficiency

A common pattern is:

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

rather than:

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

Why?

Because dependency files usually change less frequently than application
source.

The desired flow is:

Stable dependency input
        ↓
Expensive dependency installation
        ↓
Cache
        ↓
Frequently changing source

This can significantly improve local and CI/CD build performance.

8. Minimize Unnecessary Cache Invalidation

Cache should be designed around meaningful inputs.

For example:

COPY package*.json .

RUN npm ci

COPY src/ ./src/

If only application source changes:

package*.json unchanged
        ↓
npm ci cache can remain reusable
        ↓
Only later work needs rebuilding

The goal is not to avoid cache misses completely.

The goal is:

Invalidate only the work that actually depends on the changed
input.

9. Combine Related Package Operations

For Debian/Ubuntu-based images, a common pattern is:

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

This keeps the package metadata update and installation in the same
build operation and removes package-list data that is no longer needed.

The broader principle is:

Install what you need
        ↓
Remove unnecessary build/package metadata
        ↓
Keep the resulting image lean

The exact package-management pattern depends on the base distribution.

10. Avoid Unnecessary Packages

Only install packages that the image actually needs.

For example, avoid turning a runtime image into:

Application
+
Compiler
+
Debugging tools
+
Package managers
+
Development dependencies
+
Unrelated utilities

when the application only needs:

Runtime
+
Required libraries
+
Application

Unnecessary packages increase:

image size

attack surface

patching requirements

dependency complexity

11. Use Multi-Stage Builds

Multi-stage builds separate build dependencies from runtime
dependencies.

Example:

FROM node:22 AS builder

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

The flow is:

Builder
   ↓
Compiler / build dependencies
   ↓
Build artifact
   ↓
Final runtime image
   ↓
Only required runtime content

This can reduce the final image size and attack surface.

12. Separate Build and Runtime Responsibilities

A production image should not necessarily contain everything required to
compile the application.

For example:

Build stage
    ├── compiler
    ├── development dependencies
    └── build tools

Runtime stage
    ├── runtime
    ├── application
    └── required runtime libraries

This separation is one of the strongest Docker image optimization
patterns.

13. Run as a Non-Root User

Avoid running the application as root when the application does not
require it.

For example:

RUN useradd --create-home appuser

USER appuser

The mental model is:

Container
    ↓
Application
    ↓
Non-root identity
    ↓
Reduced privilege

Running as a non-root user can reduce the impact of certain container
compromises.

The user must still have appropriate permissions for:

Application files
Working directory
Ports
Volumes
Runtime operations

14. Set File Ownership Intentionally

If an application runs as:

USER appuser

the application files need appropriate ownership or permissions.

Instead of copying files and then recursively changing everything:

COPY . /app/

RUN chown -R appuser:appuser /app

COPY --chown can sometimes make the intent clearer:

COPY --chown=appuser:appuser . /app/

This can also avoid an additional recursive filesystem operation.

15. Use WORKDIR

Prefer:

WORKDIR /app

instead of repeatedly relying on:

RUN cd /app

The latter changes the directory only for that particular shell command.

WORKDIR establishes the working directory for subsequent instructions
and runtime behaviour.

The mental model is:

WORKDIR /app
      ↓
Consistent working location
      ↓
COPY / RUN / CMD / ENTRYPOINT

16. Use Exec Form for Application Startup

For a simple long-running application:

CMD ["python", "app.py"]

is generally preferable to:

CMD python app.py

when shell functionality is not required.

Exec form makes the executable and arguments explicit and generally
gives clearer process and signal behaviour.

The distinction is:

Shell form
    ↓
Shell semantics

Exec form
    ↓
Direct executable + arguments

Use shell semantics intentionally when they are actually needed.

17. Make Runtime Configuration Explicit

Use the appropriate Docker mechanism for the appropriate purpose.

For example:

ARG
 ↓
Build-time input

ENV
 ↓
Environment configuration

LABEL
 ↓
Image metadata

VOLUME
 ↓
Storage mount point

EXPOSE
 ↓
Container-port metadata

Avoid mixing these responsibilities.

For example, do not use:

LABEL APP_ENV="production"

when the application actually needs a runtime environment variable:

ENV APP_ENV=production

18. Do Not Put Secrets in the Image

Avoid:

ENV DATABASE_PASSWORD=secret

or:

ARG API_TOKEN=secret

when these contain real credentials.

Image configuration and build history can be inspected.

For builds that genuinely require temporary credentials, BuildKit secret
mounts are a safer mechanism:

RUN --mount=type=secret,id=token ...

For runtime credentials, use the deployment platform's secret-management
mechanism.

The principle is:

Secret
   ↓
Secret management
   ↓
Runtime / temporary build access
   ↓
Not baked into image

19. Keep Health Checks Meaningful

A health check should answer an operationally useful question.

For example:

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

A good health check should be:

Lightweight
+
Reliable
+
Application-specific

Avoid expensive operations or checks that always return success
regardless of application state.

Remember:

Container running
    ≠
Application healthy

20. Use EXPOSE as Documentation

For an application listening on port 8000:

EXPOSE 8000

documents the intended container port.

It does not publish the port to the host.

Runtime publishing is separate:

docker run -p 8000:8000 my-app

Mental model:

EXPOSE
    ↓
Container port metadata

-p / Compose / orchestration
    ↓
Actual networking

21. Keep Images Focused

A production image should contain:

Application
+
Required runtime dependencies
+
Required configuration

and avoid:

Source-control metadata
Build caches
Temporary files
Development-only tools
Unnecessary dependencies
Secrets

This supports:

Smaller image
+
Smaller attack surface
+
Faster transfer
+
Faster startup
+
Easier maintenance

22. Be Careful With Shell Scripts

A shell entrypoint can be useful:

COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

But the script should be designed carefully.

If it starts the actual application, using:

exec "$@"

can replace the shell process with the application process.

Conceptually:

Entrypoint shell
      ↓
exec
      ↓
Application
      ↓
PID 1

This can improve signal handling and graceful shutdown behaviour.

23. Keep Dockerfile Instructions Readable

A production Dockerfile should be understandable during an incident.

Prefer clear structure:

FROM ...

WORKDIR ...

COPY dependency-files ...

RUN install-dependencies

COPY application ...

USER ...

EXPOSE ...

HEALTHCHECK ...

ENTRYPOINT ...

Avoid unnecessarily clever shell commands that make troubleshooting
difficult.

The Dockerfile is operational documentation as well as a build
definition.

24. Avoid Running Unnecessary Processes

A container should generally have a clear primary responsibility.

For example:

API container
    ↓
API process

rather than:

API
+
SSH server
+
cron
+
unrelated background services

unless there is a deliberate architectural reason.

This keeps:

Process ownership
+
Health
+
Logging
+
Scaling

easier to reason about.

25. Logging Should Follow Container Principles

Containers should generally write application logs to standard output
and standard error when appropriate:

stdout
stderr

rather than requiring engineers to inspect arbitrary internal log files.

The flow becomes:

Application
    ↓
stdout / stderr
    ↓
Container runtime
    ↓
Logging system

This works naturally with Docker and orchestration platforms.

The exact production logging architecture depends on the platform.

26. Avoid Baking Environment-Specific Configuration

Avoid building separate images merely because:

dev
staging
production

need different runtime configuration values.

A better model is often:

Same application image
       ↓
Environment-specific runtime configuration
       ↓
Dev / Staging / Production

For example:

Image
  ↓
APP_ENV / endpoint / credentials
  ↓
Runtime environment

This supports immutable image promotion through environments.

27. Build Once, Promote the Same Artifact

A strong CI/CD pattern is:

Source
   ↓
Build image
   ↓
Test / Scan
   ↓
Registry
   ↓
Promote same image
   ↓
Staging
   ↓
Production

Avoid rebuilding the same source separately for every environment when
possible.

The principle is:

Build once, verify the artifact, then promote that same artifact.

This improves traceability and reduces environment-specific build
differences.

28. Add Useful Image Metadata

Useful OCI-oriented labels can provide:

Version
Source
Revision
Title
Description
Vendor
Documentation

For example:

LABEL org.opencontainers.image.title="IncidentLab" \
      org.opencontainers.image.version="0.8.0" \
      org.opencontainers.image.description="Incident simulation platform"

Labels should remain descriptive.

Do not store:

Passwords
API keys
Tokens

in image metadata.

29. Use Deterministic and Controlled Dependencies

Where practical, control dependency versions.

For example:

requirements.txt
package-lock.json
poetry.lock
go.sum

can help make dependency installation more predictable.

The exact mechanism depends on the language ecosystem.

The broader principle is:

Controlled dependency input
      ↓
Predictable build
      ↓
Traceable artifact

This should be combined with trusted registries and appropriate security
scanning.

30. Scan the Resulting Image

A Dockerfile can follow good practices and still produce an image
containing vulnerable dependencies.

Therefore, image security should include scanning.

Conceptually:

Build
  ↓
Image
  ↓
Vulnerability scan
  ↓
Secret / configuration checks
  ↓
Policy
  ↓
Promote or reject

Tools such as vulnerability scanners can identify known issues in:

Base image
OS packages
Application dependencies

Scanning complements Dockerfile best practices; it does not replace
them.

31. Inspect the Final Artifact

After building:

docker image inspect my-app:latest

can help verify:

User
WorkingDir
Entrypoint
CMD
Labels
Ports
Volumes
Healthcheck
Environment

A useful production mindset is:

Dockerfile says
      ↓
Build
      ↓
Inspect artifact
      ↓
Verify

This is especially valuable in CI/CD.

32. Test the Image as a Runtime Artifact

Do not stop after:

docker build

Test the resulting image.

For example:

Build
 ↓
Run
 ↓
Health check
 ↓
Application request
 ↓
Shutdown

Validate:

Does it start?
Does the application respond?
Does it use the expected user?
Does networking work?
Does it shut down cleanly?
Does persistent data behave correctly?

A successful build only proves that the image could be constructed.

33. Common Anti-Patterns

FROM latest

FROM python:latest

can make the build input less predictable.

Copying the entire repository blindly

COPY . .

without a suitable .dockerignore can introduce unnecessary inputs.

Running as root unnecessarily

USER root

should not be the default runtime assumption when the application does
not need it.

Baking secrets into the image

ENV PASSWORD=...

is unsafe for real credentials.

Installing development tools into runtime images

Compiler
Debugger
Build toolchain

may not belong in the final image.

Using shell form without needing shell features

CMD python app.py

can introduce unnecessary shell semantics.

Rebuilding separately for every environment

Build dev
Build staging
Build production

can create artifact drift.

Prefer:

Build once
    ↓
Promote same image

when the architecture permits it.

34. Troubleshooting Checklist

When a Docker image behaves unexpectedly, use a sequence instead of
random changes.

1. Verify image/tag
        ↓
2. Inspect image configuration
        ↓
3. Run container
        ↓
4. Check container state
        ↓
5. Check logs
        ↓
6. Check process / PID 1
        ↓
7. Check network
        ↓
8. Check mounts / permissions
        ↓
9. Check application configuration
        ↓
10. Reproduce the failure

This follows the same engineering principle used throughout Docker
troubleshooting:

Move from image → container → runtime → application instead of
changing multiple variables at once.

35. Production Dockerfile Mental Model

A strong production Dockerfile can be thought of as:

1. Controlled base image
        ↓
2. Focused build context
        ↓
3. Efficient cache structure
        ↓
4. Minimal required dependencies
        ↓
5. Multi-stage build where useful
        ↓
6. Non-root runtime
        ↓
7. Explicit process startup
        ↓
8. Meaningful health signal
        ↓
9. Useful metadata
        ↓
10. Secure, tested artifact

The goal is not to mechanically apply every rule.

The goal is to make deliberate engineering decisions.

36. IncidentLab Connection

IncidentLab's production-oriented Docker workflow can combine the
concepts covered so far:

Repository
    ↓
.dockerignore
    ↓
Focused build context
    ↓
Dockerfile
    ↓
Efficient COPY ordering
    ↓
BuildKit cache
    ↓
Multi-stage build
    ↓
Non-root runtime
    ↓
HEALTHCHECK
    ↓
Image inspection
    ↓
Security scanning
    ↓
Registry
    ↓
Deployment

This is the connection between individual Dockerfile instructions and
the complete DevOps workflow.

The objective is not simply to create an image.

It is to create a repeatable, secure, traceable deployment artifact.

37. Interview Takeaway

A strong interview explanation is:

"For a production Dockerfile, I start with a controlled and
appropriate base image, keep the build context small with
.dockerignore, structure COPY instructions for cache efficiency,
use multi-stage builds where appropriate, avoid unnecessary packages,
run as a non-root user, use exec form for the main process, keep
secrets out of the image, add meaningful health checks and metadata,
and validate and scan the resulting image before promotion."

If asked why these practices matter:

Security
+
Performance
+
Reproducibility
+
Maintainability
+
Operational reliability

are the main goals.

38. Key Takeaways

Choose a controlled, appropriate base image.

Keep the build context focused.

Use .dockerignore.

Prefer COPY for ordinary file copying.

Structure Dockerfile instructions for useful cache boundaries.

Avoid unnecessary packages.

Use multi-stage builds when they improve the final image.

Run applications as non-root where practical.

Use WORKDIR for consistent paths.

Prefer exec form for simple application startup.

Keep secrets out of image layers and metadata.

Use meaningful HEALTHCHECK configuration.

Treat EXPOSE as container-port documentation.

Add useful OCI-oriented metadata.

Control dependency versions where practical.

Scan and inspect the resulting image.

Test the image as a runtime artifact.

Prefer building once and promoting the same artifact across
environments.

Keep the Dockerfile readable enough to troubleshoot during an
incident.

39. Connections

Previous

21-layer-caching-internals.md

Next

23-container-security.md

40. My Understanding

Dockerfile best practices are not a checklist to follow blindly.

They are a way of designing the image around several engineering goals:

Controlled inputs
      +
Efficient build
      +
Minimal runtime
      +
Least privilege
      +
Predictable process
      +
Secure artifact
      +
Operational visibility

A production Dockerfile should therefore answer:

What are we building?
What inputs does it need?
What should the final image contain?
Who should run the application?
How should it start?
How do we know it is healthy?
How do we verify and secure the artifact?

The strongest Dockerfiles make these decisions explicit rather than
accidental.

41. Questions for Further Exploration

When should a team choose Alpine, Debian/Ubuntu slim, distroless, or
another base image?

How should Dockerfile practices change for stateful applications?

Which Dockerfile security checks should be enforced automatically in
CI/CD?

How should image size, security, and debugging capability be
balanced?

How can Dockerfile best practices be converted into automated policy
checks?

How should the IncidentLab Docker build be hardened before
production deployment?
