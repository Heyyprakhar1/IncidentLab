Container Security

1. What Is Container Security?

Container security is the practice of protecting container images,
containers, their runtime environment, and the supply chain used to
build and deploy them.

A useful mental model is:

Source
   ↓
Dockerfile
   ↓
Image
   ↓
Registry
   ↓
Container Runtime
   ↓
Application

Security needs to be considered across this entire path.

The goal is not simply:

"Is the container running?"

The better question is:

Can the image, build process, runtime, and application operate with
the minimum necessary risk and privilege?

2. Why Container Security Matters

Containers provide process and filesystem isolation, but a container is
not automatically secure just because it is a container.

A vulnerable or poorly configured image can still contain:

Vulnerable packages
Weak configuration
Secrets
Excessive privileges
Unnecessary tools
Unsafe permissions

A compromised application can also become more dangerous when the
container has unnecessary privileges.

The security model is therefore:

Secure image
    +
Secure runtime
    +
Least privilege
    +
Controlled supply chain
    +
Monitoring

3. Container Security Is a Lifecycle

Security should not be treated as a single scan performed at the end.

A stronger lifecycle is:

Code
  ↓
Build
  ↓
Scan
  ↓
Sign / verify where applicable
  ↓
Registry
  ↓
Deploy
  ↓
Runtime controls
  ↓
Monitor
  ↓
Patch / rebuild

This is particularly important in DevOps because the image is a
deployment artifact that moves through multiple systems.

4. Start With the Base Image

The base image is part of the application's attack surface.

For example:

FROM python:3.12-slim

contains the Python runtime and operating-system components required by
the application.

A larger image may contain many additional packages:

More packages
    ↓
More components
    ↓
More potential vulnerabilities
    ↓
Larger attack surface

Therefore, choose a base image appropriate for the application rather
than automatically choosing the largest or smallest possible image.

5. Keep the Image Minimal

A production image should contain only what the application needs at
runtime.

Avoid unnecessarily including:

Compilers
Debugging tools
Build toolchains
Source-control metadata
Development dependencies
Temporary files
Package caches

The principle is:

Build dependencies
      ↓
Builder stage

Runtime dependencies
      ↓
Final image

Multi-stage builds are a common way to achieve this separation.

6. Multi-Stage Builds for Security

Consider:

FROM node:22 AS builder

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

The final image does not need the entire Node.js build environment.

The security benefit is:

Build tools
    ↓
Stay in builder stage

Runtime image
    ↓
Contains only required runtime content

This can reduce the final attack surface.

7. Run as a Non-Root User

One of the most important runtime security practices is avoiding
unnecessary root privileges.

For example:

RUN useradd --create-home appuser

USER appuser

The principle is:

Application
    ↓
Non-root user
    ↓
Reduced privilege

If the application is compromised, the attacker does not automatically
receive the same privileges as a root process.

This does not eliminate the impact of a compromise, but it can
significantly reduce the available privileges.

8. Least Privilege

Least privilege means giving a process only the permissions it actually
needs.

This applies to:

User
Filesystem
Network
Linux capabilities
Container runtime
Cloud identity

For example:

Application
    ↓
Needs to read /app
    ↓
Grant read access

rather than:

Application
    ↓
Full filesystem write access

The same principle applies to cloud credentials and Kubernetes
permissions.

9. Avoid Privileged Containers

A container should not be given elevated privileges unless there is a
specific operational requirement.

Avoid casually using:

docker run --privileged ...

because privileged containers can receive broad access to host
resources.

The security principle is:

Normal container
    ↓
Minimum required privileges

Privileged container
    ↓
Only when explicitly justified

If an application requires a specific capability, prefer granting only
the required capability rather than broadly elevating the entire
container.

10. Linux Capabilities

Linux capabilities divide traditionally powerful root privileges into
smaller units.

Instead of thinking only:

Root
vs
Non-root

the model can be:

Process
   ↓
Specific capability
   ↓
Specific privileged operation

Where supported and appropriate, capabilities can be dropped or
restricted.

This is more precise than simply giving a container broad privileges.

11. Filesystem Permissions

Container security also includes filesystem permissions.

For example:

Application user
      ↓
Read required files
      ↓
Write only required directories

Avoid making everything writable without a reason.

Be especially careful with:

Secrets
Configuration
Application binaries
System directories
Mounted volumes

A compromised process with unnecessary write access can have a larger
impact.

12. Read-Only Root Filesystem

Where practical, a container can use a read-only root filesystem.

Conceptually:

Container root filesystem
        ↓
Read-only
        ↓
Application writes only to
explicit writable locations

This can reduce the ability of a compromised process to modify the
container filesystem.

Applications that need temporary or runtime data may require specific
writable mounts.

The design becomes:

Read-only root
     +
Writable /tmp or application data mount

rather than making the entire filesystem writable.

13. Secrets Must Not Be Baked Into Images

Never intentionally place real credentials into the image.

Avoid:

ENV DB_PASSWORD=secret

or:

ARG API_TOKEN=secret

when these contain real credentials.

Image configuration and build metadata may be inspectable.

The preferred model is:

Secret manager
      ↓
Build-time temporary access
      or
Runtime secret injection
      ↓
Application

For BuildKit builds that genuinely require a secret:

RUN --mount=type=secret,id=token ...

can provide temporary build-time access without intentionally embedding
the secret in the resulting image.

14. Do Not Commit Secrets to the Build Context

A secret can be exposed before the Dockerfile even runs if it is present
in the build context.

For example:

.env
credentials.json
private-key.pem

should not casually be sent as build input.

Use:

.dockerignore

to exclude files that should not be part of the context.

But remember:

.dockerignore is a protection against accidental build-context
inclusion, not a replacement for proper secret management.

15. Scan Container Images

An image should be scanned for known vulnerabilities before deployment.

Conceptually:

Dockerfile
    ↓
Build image
    ↓
Vulnerability scan
    ↓
Policy decision
    ↓
Promote / reject

Scanners can identify vulnerabilities in areas such as:

Operating-system packages
Base image
Application dependencies
Language libraries

A scan is useful only when the organization has a policy for responding
to findings.

16. Vulnerability Severity

Not every vulnerability has the same practical impact.

A security workflow may classify findings by severity:

Critical
High
Medium
Low

But severity alone is not the complete decision.

Consider:

Severity
+
Exploitability
+
Exposure
+
Application usage
+
Available remediation

For example, a vulnerability in an unused component may have a different
operational priority from a remotely exploitable vulnerability in an
internet-facing service.

17. Keep Dependencies Updated

Security scanning should not be treated as a one-time activity.

A production image should be rebuilt regularly to receive:

Security patches
Base image updates
Dependency updates
OS package updates

The lifecycle becomes:

Build
  ↓
Scan
  ↓
Deploy
  ↓
New vulnerability discovered
  ↓
Update dependency/base image
  ↓
Rebuild
  ↓
Rescan

This is why immutable images still need continuous rebuilding.

18. Use Trusted Base Images

The source of the base image matters.

Prefer trusted, maintained image sources.

Consider:

Who publishes it?
How is it maintained?
How frequently is it updated?
What packages does it contain?
Can its provenance be verified?

A secure build starts with controlled inputs.

The supply-chain principle is:

Trusted source
    ↓
Known artifact
    ↓
Verified build

19. Image Provenance and Signing

Modern container supply chains can use image signing and provenance
mechanisms to establish information about an artifact.

Conceptually:

Build
  ↓
Artifact
  ↓
Metadata / provenance
  ↓
Signature
  ↓
Registry
  ↓
Verification
  ↓
Deployment

The purpose is to improve confidence that:

The image came from an expected source
+
The artifact was not unexpectedly modified

The exact tooling depends on the registry and CI/CD platform.

20. Registry Security

The container registry is part of the security boundary.

A production registry should have appropriate:

Authentication
Authorization
Access control
Encryption
Audit logging
Retention policies
Vulnerability scanning

Do not treat the registry as simply:

"Storage for Docker images"

It is also a critical supply-chain component.

21. Image Immutability and Tags

Tags such as:

latest
production
stable

can move over time.

For stronger deployment traceability, immutable image identifiers such
as digests can be used.

For example:

my-app@sha256:<digest>

Conceptually:

Tag
 ↓
Human-friendly reference

Digest
 ↓
Specific image content

This helps ensure that the exact artifact tested is the artifact
deployed.

22. Container Runtime Security

Image security is only one layer.

At runtime, consider:

User
Capabilities
Filesystem
Network
Secrets
Resource limits
System calls
Runtime permissions

The flow becomes:

Secure image
      +
Secure runtime configuration
      ↓
More secure container

A secure Dockerfile can still be undermined by insecure runtime
configuration.

23. Resource Limits

A container that consumes excessive resources can affect other
workloads.

Depending on the runtime/orchestrator, resource controls can limit:

CPU
Memory
Process count

The security relationship is:

Resource control
      ↓
Limit blast radius
      ↓
Improve workload isolation

Resource limits also improve operational predictability.

24. Network Security

Container networking should follow least privilege.

Ask:

Who needs to talk to this container?
Which ports are required?
Which services should be reachable?
Which traffic should be denied?

The mental model is:

Application
   ↓
Required network paths
   ↓
Only necessary communication

In Docker Compose, Kubernetes, and cloud environments, network controls
can be applied at different layers.

25. Logging and Monitoring

Security does not end when the container starts.

Monitor for:

Unexpected processes
Repeated failures
Suspicious network behaviour
Privilege changes
Unexpected file modifications
Authentication failures
Resource anomalies

The operational lifecycle is:

Deploy
  ↓
Observe
  ↓
Detect
  ↓
Investigate
  ↓
Remediate

This is especially important for incident-response workflows.

26. Container Security vs Host Security

Containers share the host kernel in typical container runtimes.

Therefore:

Container security
      +
Host security

are connected.

A compromised container should not be treated as completely isolated
from the host.

The host still needs:

Security updates
Access controls
Monitoring
Runtime hardening

This is one reason privileged containers are particularly sensitive.

27. Docker Socket Risk

Giving a container access to the Docker socket can be extremely
powerful.

For example:

/var/run/docker.sock

can allow interaction with the Docker daemon.

Because the Docker daemon typically has high host-level privileges,
exposing its socket to an untrusted container can significantly increase
risk.

The principle is:

Do not mount the Docker socket into containers unless the
operational requirement is understood and the security implications
are accepted.

28. Avoid Unnecessary Host Mounts

Host filesystem mounts can expose sensitive host data.

For example:

Host filesystem
      ↓
Container mount
      ↓
Application access

Only mount the paths the application actually needs.

Avoid broad mounts when a narrower path is sufficient.

This follows least privilege:

Required data
    ↓
Required path
    ↓
Required permissions

29. Container Security in Kubernetes

In Kubernetes, container security extends into workload configuration.

Important concepts include:

SecurityContext
Pod security
RunAsUser
RunAsNonRoot
Capabilities
Read-only root filesystem
Seccomp
NetworkPolicy
ServiceAccount
RBAC
Secrets

The security model becomes:

Container image
      +
Pod security configuration
      +
Kubernetes identity
      +
Network policy
      ↓
Runtime security

This is why Docker security fundamentals transfer directly into
Kubernetes security.

30. Runtime Identity and Cloud Permissions

A container running in a cloud environment may access cloud APIs through
an identity.

For example:

Application
    ↓
Cloud identity
    ↓
AWS API

That identity should follow least privilege.

Avoid:

Application
    ↓
Administrator-level permissions

when it only needs:

Specific S3 bucket access

Container security therefore intersects with IAM and workload identity.

31. Security Testing in CI/CD

Security checks should ideally happen before deployment.

A mature pipeline can look like:

Checkout
   ↓
Build
   ↓
Lint
   ↓
Unit tests
   ↓
Image scan
   ↓
Secret scan
   ↓
Policy validation
   ↓
Push
   ↓
Deploy

The exact sequence depends on the project.

The principle is:

Find security problems as early as practical, before the artifact
reaches production.

32. Security Gates

A pipeline can enforce policies such as:

Critical vulnerability?
   ↓
Reject

Running as root?
   ↓
Reject / review

Secret detected?
   ↓
Reject

Untrusted base image?
   ↓
Reject / review

The goal is not to block every build for every low-risk finding.

The goal is to automate organizational security requirements
consistently.

33. Common Container Security Mistakes

Running everything as root

USER root

without a requirement increases privilege.

Baking secrets into images

ENV API_KEY=...

creates unnecessary exposure.

Using privileged containers unnecessarily

docker run --privileged ...

broadens the container's privileges.

Mounting the Docker socket casually

/var/run/docker.sock

can expose powerful Docker daemon capabilities.

Using an unnecessarily large base image

More packages can mean more components to maintain and scan.

Ignoring image vulnerabilities

A successful build does not mean the resulting image is secure.

Assuming .dockerignore is secret management

It helps prevent accidental inclusion but should not replace a proper
secret-management system.

Using mutable image tags for critical deployments

latest

can point to different image content over time.

34. Troubleshooting Security Issues

When a container security issue is reported, use a structured sequence.

1. Identify image
        ↓
2. Identify image source
        ↓
3. Inspect image configuration
        ↓
4. Scan image
        ↓
5. Check container user
        ↓
6. Check capabilities / privileges
        ↓
7. Check mounts
        ↓
8. Check network exposure
        ↓
9. Check secrets / credentials
        ↓
10. Check runtime / host configuration

This prevents focusing only on the Dockerfile while ignoring the
runtime.

35. Production Security Mental Model

A production container should be approached as:

Controlled source
      ↓
Trusted base image
      ↓
Secure build
      ↓
Minimal image
      ↓
Vulnerability scan
      ↓
Signed / traceable artifact
      ↓
Secure registry
      ↓
Least-privilege runtime
      ↓
Monitoring
      ↓
Continuous patching

No single control provides complete container security.

Security comes from the combination.

36. IncidentLab Connection

IncidentLab's DevSecOps workflow can connect container security controls
across the pipeline:

Source
   ↓
Gitleaks
   ↓
Build
   ↓
Hadolint
   ↓
Trivy
   ↓
Image validation
   ↓
Registry
   ↓
Kubernetes
   ↓
Runtime monitoring

The project already uses multiple security layers, so container security
is not just a Dockerfile concern.

It becomes:

Code security
+
Build security
+
Image security
+
Runtime security
+
Cloud / Kubernetes security

This aligns directly with the project's broader DevSecOps architecture.

37. Interview Takeaway

A strong interview explanation is:

"I treat container security as a lifecycle rather than just an image
scan. I start with a trusted and minimal base image, keep secrets out
of the image, use multi-stage builds, run as non-root, restrict
capabilities and privileges, control filesystem and network access,
scan the image for vulnerabilities, secure the registry and deployment
identity, and monitor the container at runtime. In CI/CD, I automate
the checks and enforce security gates based on organizational
policy."

If asked for the core principle:

Least privilege
+
Minimal attack surface
+
Trusted supply chain
+
Continuous verification

38. Key Takeaways

Container security covers build, image, registry, runtime, and
application layers.

Use trusted and appropriately sized base images.

Keep runtime images minimal.

Use multi-stage builds to separate build and runtime dependencies.

Run applications as non-root where practical.

Apply least privilege to users, capabilities, filesystem, network,
and cloud identities.

Avoid privileged containers unless explicitly required.

Keep secrets out of images and build contexts.

Use appropriate BuildKit secret mechanisms for temporary build
credentials.

Scan images for vulnerabilities.

Keep base images and dependencies patched.

Secure the registry and control access.

Prefer immutable image references for critical deployments.

Apply runtime controls such as read-only filesystems and resource
limits where appropriate.

Protect the Docker socket and avoid unnecessary host mounts.

Extend container security into Kubernetes security controls.

Automate security checks in CI/CD.

Monitor containers after deployment.

Treat security as a continuous lifecycle rather than a one-time
scan.

39. Connections

Previous

22-dockerfile-best-practices.md

Next

24-container-runtime.md

40. My Understanding

Container security is best understood as a layered system:

Source
  ↓
Build
  ↓
Image
  ↓
Registry
  ↓
Runtime
  ↓
Application

Every layer has different risks and controls.

The strongest mental model is:

Minimal image
      +
Least privilege
      +
Secure secrets
      +
Trusted supply chain
      +
Continuous scanning
      +
Runtime controls
      +
Monitoring

The key lesson is:

A secure container is not created by one Dockerfile instruction or
one vulnerability scan. It is the result of reducing unnecessary
privileges and attack surface throughout the complete container
lifecycle.

41. Questions for Further Exploration

How do Linux capabilities work internally?

How does seccomp restrict container system calls?

How does Docker's default security profile protect containers?

How should Trivy findings be converted into CI/CD security gates?

How do Kubernetes SecurityContext, RBAC, and NetworkPolicy combine
with image security?

What is the security impact of mounting /var/run/docker.sock?

How can container image signing and provenance be implemented in
GitHub Actions?
