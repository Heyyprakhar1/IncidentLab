Production Docker Checklist

1. Why a Production Checklist?

A Dockerfile can build successfully and the container can run
successfully while still being poorly prepared for production.

Production readiness requires looking beyond:

docker build
    ↓
docker run

We need to consider:

Image
Dockerfile
Runtime
Security
Networking
Storage
Resources
Observability
CI/CD
Operations

The core question is:

Can this container be safely built, deployed, operated, monitored,
updated, and recovered?

2. Production Docker Mental Model

Think about a production container in layers:

Source
   ↓
Dockerfile
   ↓
Image
   ↓
Registry
   ↓
Runtime
   ↓
Network
   ↓
Storage
   ↓
Observability
   ↓
Operations

A production checklist should validate each layer.

3. Dockerfile Basics

Before deployment, verify:

FROM
WORKDIR
COPY
RUN
CMD / ENTRYPOINT
ENV / ARG
USER

Questions:

Is the base image appropriate?
Is the working directory intentional?
Are only required files copied?
Are build commands deterministic?
Is the startup command correct?
Are runtime defaults appropriate?
Does the application run as a non-root user?

4. Base Image

Check:

Is the base image maintained?
Is the version intentional?
Is it larger than necessary?
Does it contain unnecessary packages?
Is it compatible with the application?

Avoid casually using:

FROM some-image:latest

when predictable builds matter.

A production build should have a controlled base-image strategy.

5. Image Versioning

Production images should be identifiable.

Prefer meaningful tags such as:

my-app:1.4.2
my-app:2026.08.23
my-app:<commit-sha>

A strong CI/CD approach can associate:

Git commit
    ↓
Image tag
    ↓
Deployment

This makes rollback and incident investigation easier.

Tags alone are not immutable guarantees, so production systems should
also maintain content identity through image digests where appropriate.

6. Image Size

Check whether the image contains unnecessary:

Compilers
Build tools
Source code
Development dependencies
Package caches
Documentation
Temporary files

Use:

Multi-stage builds
Specific COPY instructions
.dockerignore
Appropriate runtime images

The objective is:

Minimal
+
Compatible
+
Maintainable

not simply:

Smallest possible

7. Build Context

Review the build context.

For:

docker build .

the . represents the build context.

Ask:

What files are being sent?
Are unnecessary directories included?
Are credentials present?
Are generated files present?
Is .git included?

A large or poorly controlled context can slow builds and introduce
unnecessary inputs.

8. .dockerignore

Use .dockerignore where appropriate.

Typical exclusions can include:

.git
node_modules
__pycache__
*.log
.env
coverage/

The exact list depends on the application.

The goals are:

Smaller build context
Fewer unnecessary inputs
Faster builds
Reduced accidental file inclusion

9. Layer and Cache Design

Review Dockerfile ordering.

Prefer:

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

over:

COPY . .
RUN pip install -r requirements.txt

when the dependency installation does not need the full source tree.

The goal is:

Stable inputs
    ↓
Expensive operations
    ↓
Frequently changing inputs

This improves cache reuse.

10. Build Cache

Check:

Which layers are expensive?
Which files invalidate them?
Is CI reusing cache?

Do not use:

docker build --no-cache .

as a routine solution to slow or poorly structured builds.

Instead:

Find first unexpected cache miss
        ↓
Identify changed input
        ↓
Fix Dockerfile/cache design

11. Multi-Stage Builds

For applications that require build tooling:

Builder
   ↓
Compile / build
   ↓
Artifact
   ↓
Runtime

The final image should contain only what is required to run the
application.

For example:

FROM node:22 AS builder
...
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

Do not copy the entire builder filesystem into the production image
unless there is a specific reason.

12. Runtime User

Check:

Who runs the application?

Prefer:

Non-root user

when the application does not require root privileges.

Example:

USER appuser

But verify:

File ownership
Volume permissions
Bind-mount permissions
Port requirements
Entrypoint permissions

A secure USER setting that makes the application unusable is not a
complete production configuration.

13. Least Privilege

Do not stop at:

USER appuser

Also consider:

Linux capabilities
Read-only filesystem
Security profiles
Mounted paths
Network exposure
Runtime permissions

The production security model should follow:

Minimum privileges
+
Minimum filesystem access
+
Minimum network exposure

14. Secrets

Never bake production credentials directly into:

ENV DB_PASSWORD=...

or:

ARG API_KEY=...

Treat secrets separately from image construction.

Use the secret-management capabilities provided by the deployment
environment.

The production model should be:

Image
   ↓
No production secret embedded

Runtime
   ↓
Secret injected securely

If a secret was accidentally embedded in an image, removing it from the
Dockerfile is not enough; affected artifacts and credentials may need to
be rotated.

15. Environment Configuration

Separate:

Image

from:

Environment-specific configuration

A useful pattern is:

One image
   ↓
Development configuration
Staging configuration
Production configuration

where appropriate.

Check:

Environment variables
Configuration files
Defaults
Secrets
Overrides

Do not hard-code environment-specific values unnecessarily into the
image.

16. CMD and ENTRYPOINT

Verify the startup model.

Ask:

What is the main process?
Is CMD correct?
Is ENTRYPOINT required?
Can runtime arguments be overridden safely?

Prefer exec form where appropriate:

CMD ["python", "app.py"]

rather than unnecessarily wrapping the application in a shell.

This improves predictable process and signal behaviour.

17. PID 1 and Graceful Shutdown

The container's main process becomes PID 1 within its process namespace.

Verify that:

SIGTERM
    ↓
Application
    ↓
Graceful shutdown

works correctly.

If an entrypoint script is used, ensure it eventually executes the
application appropriately, for example using:

exec "$@"

where applicable.

Test shutdown behaviour instead of assuming it works.

18. Health Checks

A production service should have a meaningful health strategy.

Depending on the platform, this can involve:

Docker HEALTHCHECK
Application health endpoint
Load-balancer health check
Kubernetes probes
External monitoring

A health check should answer a useful question.

For example:

Is the application process alive?

is different from:

Can the application actually serve requests?

Do not make health checks unnecessarily dependent on unrelated systems.

19. Logging

Containers should generally write application logs to a location that
the runtime/orchestrator can collect.

Check:

Are logs available?
Are they structured?
Do they contain useful context?
Can the platform collect them?
Are secrets accidentally logged?

Avoid relying on logs that disappear with an ephemeral container unless
the logging system captures them.

20. Logging and Troubleshooting

A production container should make failures diagnosable.

Useful information can include:

Timestamp
Request / correlation ID
Service
Severity
Error context
Relevant operation

Avoid:

Sensitive credentials
Tokens
Passwords
Unnecessary PII

The goal is:

Failure
   ↓
Observable evidence
   ↓
Diagnosis

21. Port Configuration

Verify:

Application listening port
Container port
Published port
External port

Remember:

EXPOSE
   ↓
Documents intended container port

-p / ports
   ↓
Creates host/container publishing

Do not publish ports that do not require external or host access.

22. Network Exposure

Ask:

Who actually needs to reach this service?

Prefer:

External entry point
      ↓
Application
      ↓
Internal network
      ↓
Database

instead of exposing every internal service.

For example:

Database :5432
Redis :6379
Broker :9092

do not automatically need to be published to the host.

23. Cloud Networking

When Docker runs on a cloud VM, container networking is only one layer.

For example:

Client
   ↓
Cloud Security Group
   ↓
Host networking
   ↓
Published Docker port
   ↓
Container
   ↓
Application

Troubleshoot each layer independently.

A correct Docker port mapping does not override a cloud
firewall/security group.

24. Storage

Identify whether the application needs persistent data.

If yes, decide intentionally between:

Writable container layer
Bind mount
Volume
External storage
Managed database

For persistent application data, use storage with an appropriate
independent lifecycle.

Remember:

Persistent
   ≠
Backed up

Backup and recovery must be designed separately.

25. Volume Safety

For volumes:

Is the data important?
Who owns it?
Who can write to it?
What happens when the container is removed?
How is it backed up?
How is it restored?

Avoid blindly running:

docker volume prune

in production environments.

Storage cleanup should follow explicit retention rules.

26. Resource Limits

A production container should not be allowed to consume resources
without consideration.

Review:

CPU
Memory
Process count
Storage

For example:

Container
   ↓
CPU / memory consumption
   ↓
Host capacity

Resource controls should be based on observed workload behaviour rather
than arbitrary numbers.

27. Memory Troubleshooting

If a container is repeatedly killed:

Check application logs
        ↓
Check container state
        ↓
Check memory usage
        ↓
Check configured limits
        ↓
Check host capacity
        ↓
Identify memory growth / workload cause

Do not immediately increase the memory limit without understanding why
usage increased.

28. CPU Troubleshooting

If latency increases:

Application latency
      ↓
CPU usage
      ↓
CPU limit / throttling
      ↓
Host capacity
      ↓
Application workload

CPU issues should be correlated with:

Request volume
Application behaviour
Container limits
Host contention

29. Image Security Scanning

Before deployment, scan images for known vulnerabilities.

A production pipeline can include:

Build
  ↓
Security scan
  ↓
Policy decision
  ↓
Push

Tools can include:

Trivy
Other approved vulnerability scanners

Scanning is useful, but:

A clean vulnerability scan does not prove an image is completely
secure.

It is one layer of defence.

30. Dependency Security

Review:

OS packages
Application dependencies
Base image
Build dependencies

Keep dependencies intentionally versioned and maintained.

Avoid assuming:

Small image
   =
Secure image

Security requires:

Minimality
+
Updates
+
Scanning
+
Least privilege
+
Secure configuration

31. Image Provenance and Traceability

A production image should answer:

Which source commit created this?
Which build created it?
Which version is this?
Which dependencies/base image were used?

Useful metadata can include:

Commit SHA
Version
Build timestamp
Repository
Release identifier

This becomes extremely valuable during incidents and rollbacks.

32. Registry

Before deployment, verify:

Correct image repository
Correct tag
Correct digest
Authentication
Push permissions
Pull permissions
Retention policy

The registry is part of the production supply chain.

Do not assume:

docker build succeeded
   ↓
deployment is safe

The image must also be traceable and retrievable.

33. CI/CD Pipeline

A production Docker pipeline can follow:

Code
  ↓
Lint / Test
  ↓
Docker Build
  ↓
Security Scan
  ↓
Image Verification
  ↓
Push
  ↓
Deploy
  ↓
Health Verification

The exact pipeline depends on the organization.

The important principle is:

Do not make deployment the first place where production correctness
is tested.

34. Tagging Strategy

Avoid relying only on:

latest

for production deployments.

Prefer immutable or traceable identifiers such as:

app:<git-sha>
app:<release-version>

Then deployment can reference the exact artifact.

For example:

Commit abc123
      ↓
Image abc123
      ↓
Deployment

This makes rollback more deterministic.

35. Rollback

A production deployment is incomplete without a rollback strategy.

Ask:

What happens if the new image fails?
How do we identify the previous image?
Can we redeploy it?
How fast can we recover?

Conceptually:

Version N
   ↓
Deploy N+1
   ↓
Failure
   ↓
Rollback to N

Rollback depends on having immutable, traceable artifacts.

36. Health Verification After Deployment

Do not stop at:

Container started

Verify:

Container healthy
        ↓
Application responding
        ↓
Dependencies reachable
        ↓
Expected traffic flowing
        ↓
No abnormal errors

A running process does not necessarily mean a healthy service.

37. Observability

Production readiness requires visibility into:

Logs
Metrics
Traces
Health
Events

A useful flow is:

Container
   ├── Logs
   ├── Metrics
   ├── Traces
   └── Health
          ↓
Observability platform

This is especially important when containers are ephemeral.

38. Monitoring the Container

Useful signals can include:

CPU
Memory
Restart count
Network traffic
Filesystem usage
Request rate
Error rate
Latency

The exact metrics depend on the application.

The goal is to detect:

Failure
Degradation
Capacity problems
Abnormal behaviour

before they become larger incidents.

39. Restart Behaviour

Understand what happens when:

Application crashes
Container exits
Host reboots
Dependency becomes unavailable

Depending on the runtime/platform, configure appropriate restart or
orchestration behaviour.

But do not use endless restarts to hide an application failure.

A restart policy should support recovery while observability identifies
the underlying problem.

40. Production Troubleshooting Sequence

When a production container is failing:

1. Confirm the symptom
        ↓
2. Check container state
        ↓
3. Check logs
        ↓
4. Check health status
        ↓
5. Check application process
        ↓
6. Check resource usage
        ↓
7. Check configuration
        ↓
8. Check filesystem / storage
        ↓
9. Check container networking
        ↓
10. Check host networking
        ↓
11. Check cloud firewall/security controls
        ↓
12. Check external dependencies
        ↓
13. Identify root cause
        ↓
14. Apply targeted fix
        ↓
15. Verify recovery

This is much safer than changing multiple variables at once.

41. Security Checklist

Before production, ask:

[ ] Non-root user where possible
[ ] Minimal base image
[ ] No embedded secrets
[ ] Dependencies scanned
[ ] Image scanned
[ ] Unnecessary capabilities removed where appropriate
[ ] Unnecessary ports not published
[ ] Sensitive host paths not mounted
[ ] Read-only filesystem considered
[ ] Security profiles considered
[ ] Image provenance/traceability available

Security is a layered control system, not one Dockerfile instruction.

42. Runtime Checklist

[ ] Correct image
[ ] Correct tag/digest
[ ] Correct CMD/ENTRYPOINT
[ ] Correct user
[ ] Correct environment
[ ] Correct secrets
[ ] Correct ports
[ ] Correct network
[ ] Correct volumes
[ ] Resource expectations understood
[ ] Health checks configured
[ ] Logs available
[ ] Restart behaviour understood

43. Build Checklist

[ ] Base image intentionally selected
[ ] Dockerfile ordering reviewed
[ ] .dockerignore configured
[ ] Build context minimized
[ ] Dependencies separated from source where useful
[ ] Multi-stage build considered
[ ] Cache behaviour understood
[ ] Build reproducibility considered
[ ] Image vulnerability scanning configured
[ ] Image metadata/traceability available

44. Deployment Checklist

[ ] Image pushed successfully
[ ] Registry permissions verified
[ ] Exact artifact identified
[ ] Deployment configuration reviewed
[ ] Network access verified
[ ] Health checks verified
[ ] Logs visible
[ ] Metrics visible
[ ] Rollback artifact available
[ ] Post-deployment verification completed

45. What Production Readiness Really Means

Production readiness is not:

docker build → success
docker run   → success

It is:

Build
  ↓
Secure
  ↓
Traceable
  ↓
Deployable
  ↓
Observable
  ↓
Recoverable
  ↓
Maintainable

A production container should be treated as an operational component,
not just an image.

46. IncidentLab Connection

This checklist connects almost every Docker concept studied so far:

Dockerfile
   ↓
Image
   ↓
Layers / cache
   ↓
Multi-stage build
   ↓
Runtime user
   ↓
Container lifecycle
   ↓
Namespaces / cgroups
   ↓
Networking
   ↓
Volumes
   ↓
Health
   ↓
Logs / metrics
   ↓
CI/CD
   ↓
Incident response

When an incident happens, the checklist becomes a troubleshooting map.

47. Production Docker Review

Before approving an image for production, ask:

Build

Can I reproduce this image?
Can I identify its source?
Can I explain its layers?

Security

Does it run with minimum privileges?
Are secrets outside the image?
Has it been scanned?

Runtime

Does it start correctly?
Does it shut down gracefully?
Does it have the right configuration?

Networking

Which ports are exposed?
Which ports are actually published?
Who can reach them?

Storage

What data must persist?
Where does it live?
How is it backed up?

Operations

Can I observe it?
Can I troubleshoot it?
Can I roll it back?

48. The Production Decision Flow

A useful decision flow is:

1. What does the application need to build?
             ↓
2. What does it need to run?
             ↓
3. What can be removed from the runtime image?
             ↓
4. Which user should run it?
             ↓
5. Which ports need exposure?
             ↓
6. Which data must persist?
             ↓
7. Which resources does it need?
             ↓
8. How will we observe it?
             ↓
9. How will we secure it?
             ↓
10. How will we deploy and rollback it?

This turns Docker from:

"How do I run this container?"

into:

"How do I operate this workload safely?"

49. Interview Takeaway

A strong interview explanation is:

"Before putting a Docker image into production, I review the
complete lifecycle: base image and Dockerfile quality, image size and
caching, multi-stage builds, non-root execution, secrets, ports and
network exposure, persistent storage, resource requirements, health
checks, logging and monitoring, image scanning, traceability, CI/CD,
and rollback. If something fails, I troubleshoot layer by layer from
the application and container state through resources, storage,
networking, host controls, and external dependencies rather than
changing multiple things at once."

The key mental model is:

Build
 ↓
Secure
 ↓
Run
 ↓
Observe
 ↓
Recover

50. Key Takeaways

Production Docker is broader than writing a Dockerfile.

Choose the base image intentionally.

Keep images minimal but compatible and maintainable.

Use .dockerignore.

Design Dockerfile layers for useful cache reuse.

Use multi-stage builds when build tooling is not required at
runtime.

Run applications as non-root where practical.

Apply least privilege beyond just USER.

Never embed production secrets into images.

Separate image defaults from environment-specific runtime
configuration.

Understand CMD, ENTRYPOINT, and PID 1 behaviour.

Verify graceful shutdown.

Expose and publish only the ports actually required.

Keep internal services internal where possible.

Remember cloud firewall/security controls when Docker runs on cloud
infrastructure.

Choose persistent storage deliberately.

Persistence is not the same as backup.

Define CPU/memory/resource expectations.

Scan images and dependencies.

Keep image provenance and deployment traceability.

Prefer traceable/immutable artifact identifiers over relying only on
latest.

Design rollback before deployment.

Make logs, metrics, health, and other observability signals
available.

Treat restart behaviour as recovery support, not a substitute for
root-cause analysis.

Troubleshoot systematically from application → container → resources
→ storage → networking → host/cloud → dependencies.

Production readiness means the workload is secure, traceable,
deployable, observable, recoverable, and maintainable.

51. Connections

Previous

34-multi-stage-patterns.md

Main Docker Foundation Complete

00 → 35

This checklist consolidates the major Docker concepts covered throughout
the sequence.

52. My Understanding

A production Docker workload should be thought of as:

Source
   ↓
Dockerfile
   ↓
Optimized Image
   ↓
Security checks
   ↓
Registry
   ↓
Runtime
   ↓
Networking + Storage
   ↓
Health + Observability
   ↓
Deployment
   ↓
Rollback / Recovery

The final lesson is:

A container being able to start is only the beginning. Production
readiness means knowing what is running, under which identity, with
which resources, exposed to whom, storing what data, observed by which
systems, and recoverable when something goes wrong.
