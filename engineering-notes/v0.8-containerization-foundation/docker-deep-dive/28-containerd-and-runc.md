containerd and runc

1. Why containerd and runc Matter

When learning Docker, it is easy to think the architecture is simply:

docker run
    ↓
container

Underneath that abstraction are multiple components.

A simplified model is:

Docker CLI
    ↓
Docker Engine / daemon
    ↓
containerd
    ↓
runc
    ↓
Linux kernel
    ↓
Container process

The exact architecture can vary by environment, but this model explains
an important production concept:

Docker is not the only component involved in running a container.

2. What Is containerd?

containerd is a container runtime ecosystem component responsible for
managing the lifecycle of containers and related resources.

Conceptually:

Image
   ↓
containerd
   ↓
Container lifecycle

It can manage activities such as:

Image operations
Container creation
Container startup
Container execution
Container deletion
Storage
Networking integration
Runtime management

containerd provides a higher-level container management layer above the
low-level runtime.

3. What Is runc?

runc is a low-level OCI runtime implementation.

Its job is much closer to:

Container configuration
        ↓
Linux process

It uses Linux kernel features to create the isolated container
environment.

Conceptually:

containerd
    ↓
runc
    ↓
Namespaces
Cgroups
Capabilities
Filesystem
    ↓
Container process

The important distinction is:

containerd
   ↓
Manages container lifecycle

runc
   ↓
Creates/runs the container process

4. The Layered Architecture

A useful mental model is:

                    Docker CLI
                        ↓
                 Docker Engine
                        ↓
                    containerd
                        ↓
                      runc
                        ↓
                  Linux kernel
                        ↓
                 Container process

Each layer has a different responsibility.

Docker CLI

Human-facing command interface:

docker run
docker ps
docker stop

Docker Engine

Provides Docker's higher-level API and orchestration around Docker
resources.

containerd

Manages container lifecycle and image/runtime operations.

runc

Creates and executes the actual container process according to OCI
runtime configuration.

Linux kernel

Provides the isolation and resource-control mechanisms.

5. What Happens During docker run?

Consider:

docker run nginx

A simplified flow is:

docker CLI
    ↓
Docker Engine
    ↓
containerd
    ↓
OCI runtime
    ↓
runc
    ↓
Linux kernel
    ↓
nginx process

At a conceptual level:

Find image
   ↓
Prepare root filesystem
   ↓
Prepare container configuration
   ↓
Create isolated environment
   ↓
Start process

The exact implementation contains additional components and
communication paths, but this model is enough to understand the
architecture.

6. containerd's Role in the Lifecycle

containerd sits between higher-level container management and the
low-level runtime.

A simplified lifecycle is:

Create
  ↓
containerd
  ↓
Runtime
  ↓
Start
  ↓
Running container
  ↓
Stop
  ↓
Delete

This connects directly with the previous topic:

26-container-lifecycle.md

The commands you use at the Docker layer ultimately result in lifecycle
operations being handled by lower-level components.

7. containerd and OCI

containerd works with OCI-compatible container images and runtimes.

The relationship can be visualized as:

OCI standards
      ↓
containerd
      ↓
OCI-compatible runtime
      ↓
Linux container

This is why the previous topic on OCI matters.

OCI defines standards.

containerd implements container-management functionality around those
standards.

runc is one implementation of the OCI runtime specification.

8. containerd vs runc

This distinction is extremely important.

Component       Main responsibility

Docker Engine   Higher-level Docker container management
containerd      Container lifecycle and runtime management
runc            Low-level container process creation
Linux kernel    Isolation and resource-control mechanisms

A simple interview explanation is:

containerd manages
        ↓
runc executes
        ↓
kernel isolates

This is simplified, but it is a very useful mental model.

9. Why Do We Need Both?

A natural question is:

Why not just use runc directly?

Because container management involves more than creating one Linux
process.

A higher-level component needs to coordinate:

Images
Containers
Snapshots
Storage
Runtime
Lifecycle
Events

A low-level runtime should focus on:

Creating
Starting
Stopping
Deleting

the container process according to the runtime specification.

This separation creates a cleaner architecture.

10. runc and the OCI Runtime Specification

The OCI Runtime Specification describes how a runtime should create and
run containers.

runc implements that specification.

Conceptually:

OCI Runtime Specification
          ↓
       runc
          ↓
Linux container process

The runtime receives the appropriate container configuration and uses
Linux kernel facilities to create the isolated process environment.

11. config.json

OCI runtime bundles traditionally contain a runtime configuration such
as:

config.json

This describes how the container should be executed.

Conceptually:

config.json
    ↓
Process
User
Environment
Mounts
Namespaces
Capabilities
Resources
    ↓
runc
    ↓
Container

You normally do not manually create this file when using Docker.

Higher-level tooling prepares the required runtime configuration.

12. Linux Kernel Features

runc does not create isolation from nothing.

It uses Linux kernel mechanisms such as:

Namespaces
Cgroups
Capabilities
Filesystem isolation
Seccomp

The relationship is:

runc
  ↓
Linux kernel APIs
  ↓
Isolation + resource controls
  ↓
Container process

This prepares us for the next deeper topics:

29-linux-namespaces.md
30-linux-cgroups.md

13. Namespaces

Linux namespaces provide isolation for different types of resources.

Examples include:

PID
Network
Mount
UTS
IPC
User

Conceptually:

Container
   ↓
Namespace isolation
   ↓
Processes see an isolated environment

For example, a container can have its own network namespace.

The host and another container can have different network views.

14. Cgroups

Control groups, or cgroups, provide resource control.

They can be used to control resources such as:

CPU
Memory
Process count

Conceptually:

Container
   ↓
cgroup
   ↓
Resource constraints

This connects container runtime architecture with the resource-limit
concepts already covered.

15. Container Root Filesystem

The runtime needs a root filesystem for the container process.

Conceptually:

Image layers
    ↓
Snapshot / root filesystem
    ↓
Container
    ↓
runc
    ↓
Process

The exact snapshot and storage implementation is handled by the
higher-level runtime ecosystem.

The low-level runtime then starts the process with the configured root
filesystem.

16. containerd and Storage

containerd is involved in managing container image and
filesystem-related resources.

A simplified model is:

Image
   ↓
Content
   ↓
Snapshots
   ↓
Container root filesystem

This is another reason containerd is more than a simple process
launcher.

It coordinates container-related resources needed before the low-level
runtime can execute the process.

17. containerd and Image Management

When an image is pulled:

Registry
    ↓
containerd
    ↓
Image content
    ↓
Local content store

The image contains:

Manifest
Configuration
Layers

containerd can manage the required image content and make it available
for container creation.

The exact image-store architecture can vary, but the key idea is:

containerd participates in the lifecycle between image distribution
and container execution.

18. Snapshotters

containerd uses snapshotters to manage filesystem snapshots used by
containers.

Conceptually:

Image layers
      ↓
Snapshotter
      ↓
Container root filesystem

A snapshotter provides the filesystem view needed by the container.

Different environments can use different snapshotter implementations.

For Docker users, this is normally hidden behind the higher-level
tooling.

19. Why Docker Users Rarely See containerd

When you run:

docker run nginx

you do not normally need to think about:

containerd
runc
namespaces
cgroups
snapshots

Docker hides those implementation details.

This is useful because:

High-level interface
      ↓
Simple commands

But understanding the underlying layers becomes valuable when:

Troubleshooting
Performance analysis
Kubernetes operations
Runtime failures
Security investigation

are involved.

20. Kubernetes and containerd

Modern Kubernetes environments commonly use containerd as a container
runtime component.

A simplified node architecture is:

Kubernetes
    ↓
kubelet
    ↓
CRI
    ↓
containerd
    ↓
OCI runtime
    ↓
Linux kernel
    ↓
Container

The important point is:

Kubernetes
   ≠
Docker CLI

Kubernetes can interact with a container runtime through the Container
Runtime Interface (CRI).

21. CRI and containerd

CRI stands for Container Runtime Interface.

It provides a standardized interface through which Kubernetes can
communicate with a container runtime.

Conceptually:

kubelet
   ↓
CRI
   ↓
containerd
   ↓
OCI runtime
   ↓
Container

This allows Kubernetes to work with supported runtime implementations
without requiring the Docker CLI.

The exact runtime stack can vary, but this architecture is common.

22. Docker Engine vs Kubernetes Runtime Stack

A useful comparison:

Docker workflow

docker CLI
    ↓
Docker Engine
    ↓
containerd
    ↓
runc
    ↓
container

Kubernetes workflow

kubelet
   ↓
CRI
   ↓
containerd
   ↓
runc / other OCI runtime
   ↓
container

This explains why learning containerd and runc is valuable for DevOps
engineers working with Kubernetes.

23. containerd Is Not the Same as Docker

A common misconception is:

containerd = Docker

Not correct.

Docker provides a broader user-facing ecosystem.

containerd focuses more directly on container lifecycle and runtime
management.

Conceptually:

Docker
  ↓
Higher-level developer/operator experience

containerd
  ↓
Container management layer

runc
  ↓
Low-level runtime

24. runc Is Not a Full Container Platform

Another misconception is:

runc = Docker replacement

Not exactly.

runc is a low-level runtime.

It is designed to execute containers according to the OCI runtime model.

It does not provide the same complete experience as:

Docker

or:

containerd

Its responsibility is narrower.

25. Runtime Failure Troubleshooting

Suppose:

Container fails to start.

The troubleshooting stack can be:

Application
    ↓
Container configuration
    ↓
containerd
    ↓
OCI runtime
    ↓
Linux kernel

At the Docker level, start with:

docker ps -a
docker logs <container>
docker inspect <container>

If the error suggests a runtime-level problem, investigate:

containerd logs
runc/runtime errors
kernel messages

The exact commands depend on the host distribution and runtime
installation.

26. Example: runc Error

Suppose a container reports an error related to:

OCI runtime create failed

This is a useful signal.

It means the failure may have occurred around the runtime/container
creation layer rather than inside the application itself.

The investigation becomes:

Docker/container manager
      ↓
Runtime creation error
      ↓
OCI configuration
      ↓
Mounts / namespaces / permissions
      ↓
Kernel

Do not immediately assume the application code is broken.

27. Example: Permission Problem

Suppose a container fails during startup with a mount or
permission-related error.

A useful sequence is:

Container creation
      ↓
Runtime error
      ↓
Check mount
      ↓
Check host path
      ↓
Check permissions
      ↓
Check security controls

Potential areas include:

Filesystem permissions
SELinux/AppArmor
Mount configuration
User namespace
Capabilities

The exact cause must be established from the error rather than guessed.

28. Example: Resource Problem

Suppose a container is repeatedly killed because of memory pressure.

The conceptual stack is:

Application
    ↓
Container
    ↓
cgroup
    ↓
Linux kernel

The runtime configures the relevant resource controls.

The kernel enforces them.

This distinction is important:

runc
   ↓
Configures / creates container environment

Kernel
   ↓
Enforces kernel-level isolation and resource controls

29. Why This Matters for DevOps

A DevOps engineer troubleshooting:

Docker
Kubernetes
EKS
Containerd
CI/CD

should understand that a container is not one monolithic component.

The deeper stack is:

Application
   ↓
Container
   ↓
OCI runtime
   ↓
containerd
   ↓
Kernel

This helps narrow incidents correctly.

For example:

Application error
    ≠
Runtime error
    ≠
Kernel error

30. IncidentLab Connection

The IncidentLab troubleshooting philosophy can now extend below the
Docker CLI:

Symptom
   ↓
Docker container state
   ↓
Container configuration
   ↓
containerd
   ↓
OCI runtime / runc
   ↓
Namespaces / cgroups
   ↓
Linux kernel

This is particularly useful for advanced incidents.

For example:

"Container won't start"

should not immediately become:

"Rebuild the image."

Instead:

Is image valid?
      ↓
Is container configuration valid?
      ↓
Is runtime creation failing?
      ↓
Is a mount failing?
      ↓
Is a namespace/cgroup operation failing?
      ↓
Is the kernel/security layer rejecting it?

This is the deeper troubleshooting mindset we want.

31. Interview Takeaway

A strong interview explanation is:

"containerd is a higher-level container runtime component that
manages container lifecycle, image content, and related resources,
while runc is a low-level OCI runtime that creates and runs the
container process using Linux kernel features. In a simplified Docker
stack, Docker Engine talks to containerd, containerd invokes an OCI
runtime such as runc, and the runtime uses namespaces, cgroups,
mounts, and other kernel mechanisms to create the isolated process."

The simplest mental model is:

Docker
   ↓
containerd
   ↓
runc
   ↓
Linux kernel

32. Key Takeaways

containerd is a container-management/runtime ecosystem component.

runc is a low-level OCI runtime implementation.

Docker can use containerd underneath its higher-level interface.

containerd manages more than simply launching a process.

runc is focused on creating and running the container process.

OCI standards define common container image and runtime concepts.

config.json is associated with OCI runtime configuration.

Linux namespaces provide isolation.

Linux cgroups provide resource control.

containerd participates in image and filesystem/snapshot management.

Snapshotters help provide container filesystem views.

Kubernetes commonly uses containerd through the CRI ecosystem.

Kubernetes does not require the Docker CLI to run containers.

OCI runtime create failed can indicate a failure below the
application layer.

Runtime troubleshooting should distinguish application, container
manager, OCI runtime, and kernel failures.

Understanding containerd and runc makes Docker and Kubernetes
internals much easier to reason about.

33. Connections

Previous

27-oci-image-specification.md

Next

29-linux-namespaces.md

34. My Understanding

The container execution stack can be simplified to:

Docker / Kubernetes
        ↓
containerd
        ↓
runc
        ↓
Linux kernel
        ↓
Container process

Each layer has a different responsibility:

containerd
    ↓
Manage

runc
    ↓
Create / execute

Kernel
    ↓
Isolate / enforce

The most important lesson is:

A container is the result of several cooperating layers.
Understanding containerd and runc gives us the bridge from high-level
Docker commands to the Linux kernel mechanisms that actually make
containers work.
