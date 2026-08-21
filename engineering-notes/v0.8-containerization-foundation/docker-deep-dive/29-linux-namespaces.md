Linux Namespaces

1. What Are Linux Namespaces?

Linux namespaces are a kernel feature that provides isolation of
system resources for processes.

They are one of the fundamental mechanisms behind containers.

A simplified model is:

Container
   ↓
Linux namespaces
   ↓
Process sees an isolated system view

Instead of giving every process access to the same global view of the
system, namespaces can provide separate views for resources such as:

Processes
Network
Mounts
Hostnames
IPC
Users

This is a key reason one container can behave as if it has its own
environment while still sharing the host kernel.

2. Why Do Containers Need Namespaces?

Without namespace isolation, a process inside a container could
potentially see host-level resources directly.

For example:

Without isolation

Host
 ├── Process A
 ├── Process B
 └── Container process

With namespaces:

Host
 ├── Host process namespace
 │
 └── Container
       └── Container process namespace

The container process receives an isolated view of selected kernel
resources.

The important principle is:

Namespaces isolate what a process can see.

3. Namespaces Are Not the Whole Container

A container is not created by namespaces alone.

A useful model is:

Container
   ├── Namespaces → Isolation
   ├── cgroups    → Resource control
   ├── Filesystem → Root filesystem
   ├── Capabilities → Privilege control
   └── Seccomp / security controls

So:

Namespaces
   ≠
Complete container

Namespaces provide one major part of the isolation mechanism.

The next topic, cgroups, covers a different problem:

Namespaces → What can the process see?
cgroups    → How much can it consume?

4. Namespace Types

Linux provides several namespace types.

The most important for container understanding are:

PID
NET
MNT
UTS
IPC
USER
CGROUP
TIME

Some are especially important when learning Docker internals:

PID
NET
MNT
UTS
IPC
USER

Each namespace isolates a different category of resources.

5. PID Namespace

The PID namespace isolates process IDs.

Without PID namespace isolation:

Container process
      ↓
Could see host process IDs

With PID namespaces:

Host PID namespace
       │
       ├── Host processes
       │
       └── Container PID namespace
              ├── PID 1
              ├── PID 2
              └── PID 3

The container can have its own process numbering.

This is why a process can appear as:

PID 1

inside the container while having a different PID on the host.

6. PID 1 Inside a Container

PID namespace isolation explains an important Docker concept.

Inside the container:

Container PID namespace
        ↓
Application
        ↓
PID 1

On the host, that same process can have another PID.

Conceptually:

Container view:

PID 1
 ↓
python app.py


Host view:

PID 18472
 ↓
python app.py

The process is the same process, but different PID namespaces provide
different PID views.

7. Parent and Child Processes

PID namespaces also affect process relationships.

A process inside a child PID namespace can see processes in its own
namespace according to the namespace hierarchy, while the host can
observe processes across the namespaces it controls.

This creates a useful model:

Host PID namespace
        ↓
Container PID namespace
        ↓
Container processes

This isolation is one reason a container can have its own process tree.

8. Network Namespace

The network namespace isolates networking resources.

A network namespace can have its own:

Network interfaces
IP addresses
Routing tables
Ports
Firewall-related network state

Conceptually:

Host network namespace
       │
       └── Container network namespace
              ├── eth0
              ├── IP address
              └── Routes

This is a major part of container networking.

9. Container Network View

A container can see its own network namespace:

ip addr

Inside the container, you may see:

eth0
lo

The host has its own network interfaces and routes.

The important distinction is:

Container network view
       ≠
Host network view

The container's network namespace is one reason containers can have
their own IP addresses and routing configuration.

10. How Docker Connects Network Namespaces

Docker can connect a container's network namespace to a Docker network.

Conceptually:

Container network namespace
          ↓
Virtual network interface
          ↓
Docker networking
          ↓
Host networking

For example:

Container A
   ↓
Network namespace
   ↓
veth
   ↓
Docker bridge
   ↓
veth
   ↓
Container B

The exact network implementation depends on the Docker network mode.

The important concept is that network namespaces provide the isolated
network view.

11. Mount Namespace

The mount namespace isolates the filesystem mount view available to a
process.

This is fundamental to container filesystems.

Conceptually:

Host mount namespace
       ↓
Host filesystem mounts

Container mount namespace
       ↓
Container root filesystem
       ↓
Container-specific mounts

This allows a container to have a filesystem view that differs from the
host's mount view.

12. Container Root Filesystem

When a container starts, the process receives a configured root
filesystem.

Conceptually:

Image layers
    ↓
Container root filesystem
    ↓
Mount namespace
    ↓
Application

The application sees:

/

as the root of its filesystem view.

It does not simply see the host's normal root filesystem as its own /.

13. Mount Namespace and Volumes

Mount namespaces also help provide container-specific mount views.

For example:

Container
    ↓
/data
    ↓
Mounted volume

The container can see the mount at /data according to its mount
namespace.

The host has its own mount view.

This helps connect:

Docker volumes
+
Bind mounts
+
Container filesystem

with the underlying Linux namespace mechanism.

14. UTS Namespace

The UTS namespace isolates:

Hostname
Domain name

This is why a container can have its own hostname.

Conceptually:

Host
  ↓
hostname = docker-host

Container
  ↓
hostname = api

The processes can therefore see different hostname information depending
on their namespace.

15. IPC Namespace

IPC stands for Inter-Process Communication.

The IPC namespace isolates certain System V IPC and POSIX message-queue
resources.

Conceptually:

Host IPC namespace
       ↓
Host IPC resources

Container IPC namespace
       ↓
Container IPC resources

This prevents unrelated containers from automatically sharing the same
IPC resource view.

16. User Namespace

The user namespace isolates user and group IDs.

This is especially important for container security.

Conceptually:

Container view:
UID 0
 ↓
root

Host view:
Different mapped UID

With user namespace mapping, a process can appear as root inside its
namespace without necessarily being root with the same host-level
privileges.

This can reduce the impact of certain container escapes or
privilege-related failures when configured correctly.

17. Root Inside a Container

A common misconception is:

Container root
    =
Host root

This is not always true.

Without user namespace remapping, a root process in a container can have
significant host-level implications depending on the runtime
configuration and capabilities.

With user namespaces:

Container UID
      ↓
Mapped host UID

can provide an additional isolation layer.

The exact security posture depends on the runtime and configuration.

18. Cgroup Namespace

The cgroup namespace isolates the view of the cgroup hierarchy available
to processes.

This can affect what cgroup information a process sees.

Conceptually:

Host cgroup hierarchy
       ↓
Container cgroup namespace
       ↓
Container sees its relevant cgroup view

This is different from cgroups themselves.

Remember:

cgroup namespace
    ↓
Isolation of cgroup view

cgroups
    ↓
Resource control

19. Time Namespace

Modern Linux also supports time namespaces.

They can isolate certain clock values visible to processes.

This is useful for specialized environments and advanced
container/runtime use cases.

For foundational Docker knowledge, the most important namespaces remain:

PID
NET
MNT
UTS
IPC
USER

but knowing that Linux supports time namespaces completes the broader
picture.

20. Namespace Creation

Linux provides system calls and APIs for creating or joining namespaces.

Important mechanisms include:

clone()
unshare()
setns()

Conceptually:

clone()
   ↓
Create process with namespace isolation

unshare()
   ↓
Separate process from existing namespace

setns()
   ↓
Join an existing namespace

Container runtimes use these kernel mechanisms to establish the required
isolation.

You normally do not call them directly when using Docker.

21. nsenter

For troubleshooting, nsenter can be used to enter the namespaces of
another process.

Conceptually:

Host
  ↓
Target container process
  ↓
PID / NET / MNT / other namespaces
  ↓
nsenter

This is an advanced Linux troubleshooting technique.

It can help investigate:

Network namespace
Mount namespace
PID namespace

from the host.

Use it carefully because it operates at a lower level than normal Docker
commands.

22. Inspecting Namespace Information

Linux exposes namespace information through:

/proc/<pid>/ns/

For example:

ls -l /proc/1/ns/

You may see entries such as:

ipc
mnt
net
pid
uts
user
cgroup

Each entry represents a namespace association for that process.

A useful mental model is:

Process
   ↓
/proc/<pid>/ns/
   ↓
Namespace membership

23. Comparing Host and Container Namespaces

Suppose a container's process has PID 12345 on the host.

You can inspect:

ls -l /proc/12345/ns/

and compare it with another process.

If two processes share the same namespace inode for a namespace type,
they are associated with the same namespace instance.

Conceptually:

Process A
  ↓
net:[4026532000]

Process B
  ↓
net:[4026532000]

Same network namespace

Whereas:

Process A
  ↓
net:[4026532000]

Process C
  ↓
net:[4026532500]

Different network namespaces

24. Namespace Isolation Is Selective

A container does not necessarily receive a completely isolated copy of
every kernel resource.

Isolation is applied by namespace type.

For example:

PID namespace
   ↓
Process view

NET namespace
   ↓
Network view

MNT namespace
   ↓
Mount view

This means container isolation is a collection of mechanisms rather than
one single switch.

25. Host Network Mode

Docker can run a container with host networking.

Conceptually:

Normal mode:

Container
   ↓
Own network namespace


Host network mode:

Container
   ↓
Host network namespace

This changes the network isolation model.

The container does not get the same level of separate network namespace
isolation.

This is why network mode is a security and architecture decision, not
just a connectivity setting.

26. PID Namespace and Host Visibility

By default, a container's process view is isolated from the host's full
process namespace.

The host can still inspect container processes because:

Host
   ↓
Parent / higher-level PID namespace
   ↓
Container PID namespace

This illustrates an important point:

Namespace isolation is not necessarily symmetric.

A process in a parent namespace can generally observe processes in
descendant namespaces more easily than a process inside a child
namespace can observe the full parent namespace.

27. --pid=host

Docker can share the host PID namespace:

docker run --pid=host my-app

Conceptually:

Container
    ↓
Host PID namespace

The container then sees the host's process view rather than receiving an
isolated PID namespace.

This should be used intentionally because it reduces process isolation.

28. Namespace Sharing Between Containers

Containers can sometimes be configured to share specific namespaces.

For example, a container can be configured to share another container's
network namespace.

Conceptually:

Container A
    ↓
Network namespace
    ↑
Container B

Both processes then operate within the same network namespace.

This can be useful for specific architectural patterns, but it changes
the isolation boundary.

29. Namespaces and Security

Namespaces contribute to container security by reducing what a process
can see.

For example:

PID namespace
    ↓
Limits process visibility

NET namespace
    ↓
Limits network visibility

MNT namespace
    ↓
Limits filesystem mount visibility

But namespace isolation alone is not sufficient.

A secure container also depends on:

Capabilities
Seccomp
AppArmor / SELinux
User namespaces
Filesystem permissions
cgroups
Runtime configuration

30. Namespace Escape vs Normal Isolation

A namespace is a kernel isolation mechanism, not an absolute security
guarantee.

Security depends on:

Kernel correctness
Runtime configuration
Capabilities
Privileges
Mounted resources
Security policies

This is why:

Privileged container

can weaken the isolation boundary significantly.

The correct mental model is:

Namespaces
    ↓
Strong isolation mechanism
    +
Other security controls

31. Namespaces and --privileged

A privileged container receives significantly broader capabilities and
access than a normal container.

That can weaken the intended isolation model.

Conceptually:

Normal container
   ↓
Restricted capabilities
   ↓
Namespaces + security controls


Privileged container
   ↓
Broader access
   ↓
Much larger security boundary

Therefore, namespace isolation should always be considered together with
privilege configuration.

32. Namespace Troubleshooting

Suppose two containers unexpectedly cannot communicate.

Start at the network layer:

Container A
    ↓
Network namespace
    ↓
Interface
    ↓
Route
    ↓
Docker network
    ↓
Container B

If they are unexpectedly isolated:

Check network mode
      ↓
Check network namespace
      ↓
Check Docker network membership
      ↓
Check interface
      ↓
Check route
      ↓
Check DNS

This gives a more precise troubleshooting sequence than simply saying:

"Network is broken."

33. Namespace Troubleshooting With the Host

For advanced debugging:

Container process
       ↓
Find host PID
       ↓
Inspect /proc/<pid>/ns/
       ↓
Compare namespaces
       ↓
Determine isolation relationship

This can answer questions such as:

Are two processes in the same network namespace?
Does this container have its own PID namespace?
Which mount namespace does the process use?

This is particularly useful when Docker-level information is not enough.

34. Connection to runc

The previous topic covered:

containerd
   ↓
runc
   ↓
Linux kernel

Namespaces fit directly into that stack:

containerd
    ↓
runc
    ↓
Namespace configuration
    ↓
Linux kernel
    ↓
Isolated process

The runtime creates the container environment by asking the kernel to
establish the required isolation.

This is the bridge from:

Docker / containerd

to:

Linux internals

35. Connection to Docker Networking

Docker networking becomes easier to understand once network namespaces
are clear.

The simplified model is:

Container
    ↓
Network namespace
    ↓
eth0
    ↓
veth pair
    ↓
Docker bridge
    ↓
Host network

Docker provides the higher-level networking abstraction.

Linux namespaces provide the isolated network environment in which the
container operates.

36. Connection to Container Filesystems

Docker filesystem behaviour also becomes easier to understand through
mount namespaces.

The model is:

Image layers
    ↓
Root filesystem
    ↓
Mount namespace
    ↓
Container process

Volumes and bind mounts then appear as mounts within the container's
filesystem view.

This connects the Docker abstraction to Linux's underlying mount
architecture.

37. Connection to Kubernetes

Kubernetes workloads also ultimately rely on Linux isolation mechanisms.

A simplified path is:

Kubernetes
   ↓
containerd
   ↓
OCI runtime
   ↓
Linux namespaces
   ↓
Container process

Therefore, understanding namespaces is useful when troubleshooting:

Pod networking
Process isolation
Filesystem mounts
Security contexts
Runtime behaviour

38. IncidentLab Connection

IncidentLab's troubleshooting sequence can now descend below the Docker
abstraction:

Incident
   ↓
Container state
   ↓
Runtime configuration
   ↓
containerd
   ↓
runc
   ↓
Namespaces
   ↓
cgroups
   ↓
Linux kernel

For a networking incident:

Application
   ↓
Container
   ↓
Network namespace
   ↓
Interface
   ↓
Route
   ↓
Docker network
   ↓
Host

For a process-isolation incident:

Application
   ↓
PID namespace
   ↓
Container process tree
   ↓
Host process

This layered approach is exactly what allows troubleshooting to move
from:

Symptom

toward:

Root cause

instead of changing configuration randomly.

39. Interview Takeaway

A strong interview explanation is:

"Linux namespaces are kernel-level isolation mechanisms used by
containers to provide separate views of system resources. PID
namespaces isolate process IDs, network namespaces isolate interfaces
and routing, mount namespaces isolate filesystem mount views, UTS
isolates hostnames, IPC isolates IPC resources, and user namespaces
isolate user and group IDs. Container runtimes such as runc configure
these namespaces when creating the container process. Namespaces
provide isolation, while mechanisms such as cgroups provide resource
control."

The simplest mental model is:

Namespaces
   ↓
What the process can see

Cgroups
   ↓
What resources the process can consume

40. Key Takeaways

Linux namespaces are a fundamental container-isolation mechanism.

They provide isolated views of selected kernel resources.

PID namespaces isolate process IDs and process views.

Network namespaces isolate interfaces, IP addresses, routes, and
related network state.

Mount namespaces isolate filesystem mount views.

UTS namespaces isolate hostname/domain information.

IPC namespaces isolate certain IPC resources.

User namespaces isolate user and group IDs.

Cgroup namespaces isolate the process view of cgroup hierarchies.

Time namespaces can isolate certain clock values.

Namespaces are only one part of container isolation.

cgroups solve a different problem: resource control.

clone(), unshare(), and setns() are important Linux namespace
mechanisms.

nsenter can help with advanced namespace troubleshooting.

/proc/<pid>/ns/ exposes namespace membership information.

Sharing host namespaces changes the container's isolation boundary.

Privileged containers can significantly weaken isolation.

Namespaces connect Docker's high-level abstraction to Linux kernel
internals.

Understanding namespaces is essential for deeper Docker, containerd,
runc, and Kubernetes troubleshooting.

41. Connections

Previous

28-containerd-and-runc.md

Next

30-linux-cgroups.md

42. My Understanding

Linux namespaces are best understood as:

Kernel isolation
       ↓
Separate resource views
       ↓
Container process

The key categories are:

PID  → Processes
NET  → Networking
MNT  → Filesystem mounts
UTS  → Hostname
IPC  → IPC resources
USER → User / group IDs

The most important distinction is:

Namespaces
   ↓
What can I see?

Cgroups
   ↓
How much can I use?

This is the bridge between the Docker commands we use every day and the
Linux kernel mechanisms that actually create container isolation.

A container is not a tiny VM. It is a normal Linux process placed
into isolated namespaces, given controlled resources, and provided
with a specific filesystem and security configuration.
