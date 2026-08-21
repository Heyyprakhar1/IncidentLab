OCI Image Specification

1. What Is OCI?

OCI stands for Open Container Initiative.

The OCI project defines open standards around container images and
container runtimes.

The important idea is:

Container ecosystem
        ↓
Open standards
        ↓
Interoperable tools

Without common standards, different container tools would have to use
completely different image and runtime formats.

OCI helps establish common expectations for:

Image format
Image configuration
Runtime configuration
Runtime behaviour

2. Why Does OCI Exist?

Docker popularized containers, but the broader container ecosystem
includes many tools and platforms.

The industry benefits when tools can agree on common formats.

Conceptually:

Docker
Podman
containerd
Kubernetes
Registries
Other container tooling
        ↓
OCI standards

This allows container artifacts and runtime specifications to be shared
across compatible tooling.

The important principle is:

OCI provides open specifications so container technologies can
interoperate instead of depending on one proprietary format.

3. OCI Specifications

The OCI ecosystem is commonly understood through three major
specifications:

OCI Image Specification
OCI Runtime Specification
OCI Distribution Specification

They address different parts of the container ecosystem.

Image Specification

Defines how container images are represented.

Runtime Specification

Defines how a container runtime should execute a container.

Distribution Specification

Defines how container images and related artifacts can be distributed
through registries.

Mental model:

Build artifact
     ↓
Image Specification
     ↓
Registry
     ↓
Distribution Specification
     ↓
Runtime
     ↓
Runtime Specification

4. OCI Image Specification

The OCI Image Specification defines the structure and format of
container images.

A simplified mental model is:

OCI Image
   ├── Manifest
   ├── Configuration
   └── Layers

These components work together to describe:

What the image contains
How it should be configured
Which filesystem layers make up the image

5. Image Manifest

The image manifest describes the image's components.

Conceptually:

Manifest
   ├── Configuration descriptor
   └── Layer descriptors

Descriptors contain information such as:

Media type
Digest
Size

The digest identifies the referenced content.

For example, conceptually:

sha256:<digest>

The manifest therefore acts as a structured map of the image's content.

6. Content Addressability

OCI images make extensive use of content-addressed data.

The basic idea is:

Content
   ↓
Digest
   ↓
Reference content by digest

For example:

Layer
  ↓
sha256:abcd...

If the content changes:

Different content
      ↓
Different digest

This gives image systems a strong mechanism for:

Identity
Integrity checking
Deduplication
Caching

7. Image Configuration

The image configuration describes properties associated with the image
and its runtime behaviour.

It can contain information such as:

Environment
Entrypoint
CMD
Working directory
User
Volumes
Exposed ports
Labels
History
Root filesystem information

Conceptually:

Image
   ├── Manifest
   ├── Config
   └── Layers

This helps connect OCI concepts with the Dockerfile topics already
covered.

For example:

CMD
ENTRYPOINT
ENV
WORKDIR
USER
EXPOSE
VOLUME

can contribute to the resulting image configuration.

8. Root Filesystem and Layers

The image configuration identifies the root filesystem content through
layer information.

Conceptually:

Layer 1
   ↓
Layer 2
   ↓
Layer 3
   ↓
Root filesystem

The runtime can assemble these filesystem layers into the container's
root filesystem.

This connects directly with earlier Docker concepts:

Dockerfile
    ↓
Build
    ↓
Image layers
    ↓
OCI image representation

9. Layers Are Content Blobs

Image layers are stored as content blobs.

Conceptually:

Layer
   ↓
Compressed content
   ↓
Digest
   ↓
Registry / local content store

The manifest references these layers through descriptors.

This allows a registry or local content store to identify content
without relying only on human-readable tags.

10. Digest vs Tag

A Docker tag such as:

my-app:1.0

is a human-friendly reference.

A digest identifies specific content:

my-app@sha256:<digest>

Mental model:

Tag
 ↓
Movable reference

Digest
 ↓
Content-specific identity

This distinction is important for reproducible deployments.

A tag can be moved to another image.

A digest corresponds to the referenced content.

11. Media Types

OCI descriptors include media-type information.

Conceptually:

Descriptor
   ├── mediaType
   ├── digest
   └── size

The media type tells tooling what kind of content the descriptor refers
to.

Examples include content representing:

Image manifest
Image configuration
Filesystem layer
Image index

This allows consumers to interpret referenced content correctly.

12. Image Index

An OCI image index can reference multiple platform-specific image
manifests.

Conceptually:

Image Index
      ↓
 ┌────┴────┐
 ↓         ↓
amd64     arm64
Manifest  Manifest

This is the foundation for multi-platform image references.

For example:

linux/amd64
linux/arm64

can be associated with different manifests under a common image
reference.

13. Multi-Platform Images

A multi-platform image does not mean one identical binary works on every
architecture.

Instead:

Common image reference
        ↓
Image index
        ↓
Platform-specific manifest
        ↓
Platform-specific layers

For example:

my-app:latest
       ↓
Image Index
   ├── linux/amd64
   └── linux/arm64

The container tooling selects the appropriate platform-specific image
for the target environment.

14. OCI Image Layout

OCI also defines a standard layout for storing image content in a
directory structure.

A simplified conceptual structure is:

OCI Image Layout
├── oci-layout
├── index.json
└── blobs/
    └── sha256/
        ├── ...
        ├── ...
        └── ...

The exact contents and relationships are defined by the specification.

The important idea is:

index
  ↓
descriptors
  ↓
content blobs

This provides a standard way to represent an OCI image outside a
registry.

15. index.json

In an OCI image layout, index.json acts as the top-level index for the
stored content.

Conceptually:

index.json
    ↓
Manifest / Image Index
    ↓
Configuration + Layers

It uses descriptors to identify referenced content.

This is different from:

Dockerfile

A Dockerfile describes how to build an image.

The OCI layout describes already-produced image content.

16. oci-layout

The oci-layout file identifies the directory as an OCI image layout
and records the layout version.

Conceptually:

oci-layout
    ↓
"This directory follows OCI image-layout rules"

This allows tools to recognize the expected structure.

17. Blob Storage

OCI image content is represented through blobs.

The content-addressed structure can look conceptually like:

blobs/
  sha256/
    <digest>

Different objects can be represented as blobs:

Manifest
Config
Layer

The digest becomes the identifier for the content.

18. Image Manifest Relationship

A useful simplified relationship is:

Image Index
     ↓
Manifest
     ↓
Configuration
     ↓
Root filesystem
     ↓
Layers

For a single-platform image:

Image Reference
      ↓
Manifest
   ├── Config
   └── Layers

For a multi-platform image:

Image Reference
      ↓
Image Index
   ├── Manifest amd64
   └── Manifest arm64

This is one of the most important OCI mental models.

19. OCI Runtime Specification

The OCI Runtime Specification is separate from the Image Specification.

It describes how a container runtime should create and run a container
from a configured bundle.

Conceptually:

Image
  ↓
Runtime configuration
  ↓
OCI runtime
  ↓
Container process

This specification is concerned with runtime execution rather than
primarily describing image storage.

20. OCI Runtime Configuration

The runtime specification defines a runtime configuration format
commonly represented by:

config.json

This configuration describes how the runtime should create the
container.

It can cover concepts such as:

Process
User
Arguments
Environment
Filesystem
Mounts
Namespaces
Capabilities
Linux-specific settings
Resource controls

This connects directly with Linux container internals.

21. Image Spec vs Runtime Spec

Do not confuse:

OCI Image Specification

with:

OCI Runtime Specification

Image Specification

Answers:

"What is this container image?"

Runtime Specification

Answers:

"How should this container be executed?"

Mental model:

Image
   ↓
What to run

Runtime configuration
   ↓
How to run it

22. OCI Distribution Specification

The Distribution Specification deals with distributing container
artifacts through registries.

Conceptually:

Client
   ↓
Registry
   ↓
Manifest
   ↓
Config / Layers

It defines interactions needed for operations such as:

Push
Pull
Retrieve manifests
Retrieve blobs

This helps different container clients and registries communicate using
standardized mechanisms.

23. Registry Mental Model

When pushing an image:

Build
  ↓
Image
  ↓
Manifest
  ↓
Configuration
  ↓
Layers
  ↓
Registry

When pulling:

Registry
  ↓
Manifest / Index
  ↓
Config + Layers
  ↓
Local content
  ↓
Container

The registry is therefore a distribution system for content-addressed
container artifacts.

24. OCI and Docker

Docker and OCI are related but not identical concepts.

A useful mental model is:

Docker ecosystem
      ↓
Uses / supports OCI standards
      ↓
Container image + runtime ecosystem

OCI standards help ensure that container artifacts and runtime concepts
are not locked to a single tool.

This is why OCI knowledge is useful beyond Docker.

25. OCI and containerd

containerd is a container runtime ecosystem component that works with
OCI-compatible images and runtimes.

A simplified model is:

Docker / Kubernetes / other client
          ↓
       containerd
          ↓
     OCI-compatible
        runtime
          ↓
       Container

The exact architecture depends on the platform.

The key lesson is:

OCI provides standards; containerd and runtimes are
implementations/components that operate within that ecosystem.

26. OCI and Kubernetes

Kubernetes does not require the Docker CLI to run containers.

Modern Kubernetes nodes commonly use a container runtime such as
containerd that supports the required OCI/container runtime ecosystem.

Conceptually:

Kubernetes
    ↓
Container Runtime Interface
    ↓
containerd
    ↓
OCI runtime
    ↓
Linux kernel
    ↓
Container

The exact node implementation can vary.

OCI standards help make this ecosystem interoperable.

27. OCI and Image Portability

Suppose an image is built with one tool:

Build tool
    ↓
OCI-compatible image

and consumed by another compatible system:

OCI image
    ↓
Registry
    ↓
Different container platform

The standardized format improves portability.

This is one of the major practical benefits of open container standards.

28. OCI and Image Signing / Provenance

OCI's content-addressed model provides an important foundation for
supply-chain security.

Conceptually:

Image content
    ↓
Digest
    ↓
Artifact identity
    ↓
Signature / provenance
    ↓
Verification

Signing and provenance systems involve additional specifications and
tooling.

The important distinction is:

OCI image format
    ≠
Complete security system

OCI provides standardized artifact structures that security tooling can
build upon.

29. Inspecting OCI-Oriented Image Information

Docker can expose useful image information through commands such as:

docker image inspect my-app:latest

For deeper OCI-level investigation, container tooling can inspect:

Manifest
Config
Layers
Digests
Platform
Media types

The exact command depends on the tool being used.

The important troubleshooting principle is:

Human-friendly tag
        ↓
Resolve image reference
        ↓
Inspect manifest/index
        ↓
Inspect config/layers

30. OCI and Layer Caching

OCI's content-addressed layers also support efficient storage and
transfer.

If two images reference the same layer:

Image A ──┐
          ├── Shared layer
Image B ──┘

the same content can potentially be reused.

This connects OCI concepts with the caching topics already documented:

Content
   ↓
Digest
   ↓
Layer identity
   ↓
Reuse

The exact cache implementation is handled by the image store/build
system.

31. Common Misconceptions

OCI is Docker

Not exactly.

Docker
   ↓
Container ecosystem/tooling

OCI
   ↓
Open container specifications

OCI is only an image format

OCI includes more than the Image Specification.

The ecosystem also includes:

Image
Runtime
Distribution

specifications.

OCI runtime means containerd

Not exactly.

OCI
   ↓
Standards

containerd
   ↓
Runtime ecosystem component

runc / other runtime
   ↓
OCI runtime implementation

They occupy different roles.

A Docker tag identifies immutable content

Not necessarily.

Tags can move.

Digests provide content-specific identity.

32. Troubleshooting OCI-Level Problems

If an image works on one platform but not another:

Check image index
       ↓
Check target platform
       ↓
Check platform-specific manifest
       ↓
Check layers
       ↓
Check binary architecture

If an image cannot be pulled:

Check registry
       ↓
Check manifest
       ↓
Check referenced blobs
       ↓
Check authentication
       ↓
Check digest/content availability

If a runtime cannot start the image:

Check image compatibility
       ↓
Check runtime configuration
       ↓
Check OCI runtime support
       ↓
Check host/kernel capabilities

33. Production Relevance

OCI matters in production because modern container environments are
rarely just:

Docker CLI
+
Docker daemon

Real environments may involve:

CI/CD
Registries
Docker
containerd
Kubernetes
OCI runtimes
Image scanners
Signing tools
Artifact stores

OCI standards provide common interfaces and formats across this
ecosystem.

34. IncidentLab Connection

IncidentLab's Docker documentation can now be connected to the deeper
container stack:

Dockerfile
    ↓
Docker Build / BuildKit
    ↓
OCI Image
    ↓
Registry
    ↓
containerd / runtime
    ↓
Linux namespaces + cgroups
    ↓
Container process

This is an important transition in the learning sequence.

Earlier topics focused on:

How to build and optimize an image

OCI introduces:

What the image actually looks like underneath

That prepares the ground for:

containerd
runc
namespaces
cgroups

35. Interview Takeaway

A strong interview explanation is:

"OCI, the Open Container Initiative, defines open standards for
container images, runtimes, and distribution. The OCI Image
Specification describes how image manifests, configuration, and layers
are represented. The Runtime Specification describes how a runtime
executes a container from its configuration, while the Distribution
Specification standardizes registry interactions. OCI is important
because it enables interoperability across Docker, containerd,
Kubernetes, registries, and other container tooling."

The most useful mental model is:

OCI
├── Image Specification
├── Runtime Specification
└── Distribution Specification

36. Key Takeaways

OCI stands for Open Container Initiative.

OCI defines open standards for the container ecosystem.

OCI Image Specification describes container image structure.

OCI Runtime Specification describes container execution
configuration and behaviour.

OCI Distribution Specification covers distribution through
registries.

OCI images use manifests, configuration, descriptors, and layers.

OCI uses content-addressed digests to identify content.

Tags are human-friendly references and can move.

Digests provide content-specific identity.

Image indexes support multi-platform images.

OCI image layouts provide a standardized filesystem representation
of image content.

OCI standards improve interoperability between container tools.

Docker and OCI are related but not the same thing.

containerd and OCI runtimes are implementation components, not OCI
itself.

OCI provides a foundation for modern container supply-chain tooling.

OCI knowledge becomes especially useful when moving from Docker
commands into container internals.

37. Connections

Previous

26-container-lifecycle.md

Next

28-containerd-and-runc.md

38. My Understanding

OCI is best understood as the standardization layer of the container
ecosystem.

The mental model is:

                  OCI
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      Image      Runtime   Distribution
        ↓          ↓          ↓
     What it    How it     How it is
     contains   runs       distributed

This creates a useful bridge from the Docker abstraction:

docker build
docker run
docker push

to the deeper infrastructure:

OCI image
   ↓
Registry
   ↓
containerd
   ↓
OCI runtime
   ↓
Linux kernel

The key lesson is:

Docker is one part of the container ecosystem; OCI provides the open
standards that allow many container tools and platforms to work with
compatible images, runtimes, and distribution mechanisms.
