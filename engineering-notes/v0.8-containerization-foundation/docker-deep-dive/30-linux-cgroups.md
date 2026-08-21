Linux cgroups

1. What Are Linux cgroups?

cgroups, short for control groups, are a Linux kernel mechanism
used to organize processes and control or account for their resource
usage.

They solve a different problem from namespaces.

The simplest mental model is:

Namespaces
    ↓
What can the process see?

cgroups
    ↓
How much resource can the process use?

This distinction is fundamental to understanding how containers work
underneath Docker.

2. Why Do Containers Need cgroups?

Imagine one container consumes almost all available memory on the host:

Container A
    ↓
Consumes huge memory
    ↓
Other workloads affected

Resource control is therefore necessary.

With cgroups:

Container
    ↓
cgroup
    ↓
Resource controls
    ↓
CPU / Memory / PIDs / etc.

The goal is to prevent one workload from consuming uncontrolled amounts
of shared host resources.

3. cgroups vs Namespaces

These two concepts are often confused.

Namespaces

Namespaces provide isolation of resource views:

PID namespace
    ↓
Process visibility

Network namespace
    ↓
Network visibility

Mount namespace
    ↓
Filesystem view

cgroups

cgroups provide resource management:

CPU
Memory
PIDs
I/O

Therefore:

Namespaces → Isolation
cgroups    → Resource control

A container normally uses both.

4. cgroups Are Kernel-Level

cgroups are implemented by the Linux kernel.

The high-level relationship is:

Docker / containerd
        ↓
Container runtime
        ↓
cgroup configuration
        ↓
Linux kernel
        ↓
Resource enforcement/accounting

The runtime configures the desired resource constraints.

The kernel is responsible for enforcing the relevant controls.

This is similar to namespaces:

runc
  ↓
Linux kernel
  ↓
Isolation + resource controls

5. cgroup Hierarchy

cgroups organize processes into groups.

Conceptually:

cgroup hierarchy
       │
       ├── workload-A
       │
       ├── workload-B
       │
       └── workload-C

A process can belong to a cgroup, and the cgroup can have
resource-related configuration.

This makes it possible to manage resources for a group of processes
rather than configuring every process independently.

6. Processes and cgroups

A process is associated with a cgroup.

Conceptually:

Process A ──┐
Process B ──┼── cgroup: app
Process C ──┘

Resource controls applied to that cgroup can therefore affect the
processes within it.

For a container:

Container
    ↓
Container processes
    ↓
Associated cgroup
    ↓
Resource controls

This is one of the mechanisms that makes container resource limits
possible.

7. cgroup v1 vs cgroup v2

Linux has two major cgroup interfaces:

cgroup v1
cgroup v2

cgroup v1

Controllers were commonly organized into separate hierarchies.

cgroup v2

Uses a unified hierarchy and provides a more consistent
resource-management model.

Modern Linux distributions increasingly use:

cgroup v2

The exact version depends on the host operating system and
configuration.

For troubleshooting, always determine which cgroup version the host is
using rather than assuming.

8. Why cgroup Version Matters

Commands, filesystem paths, and controller behaviour can differ between:

cgroup v1

and:

cgroup v2

Therefore:

Container resource problem
        ↓
First identify cgroup version
        ↓
Then inspect relevant controls

A useful host check is:

stat -fc %T /sys/fs/cgroup/

The exact output depends on the system.

You can also inspect:

mount | grep cgroup

to understand how cgroups are mounted.

9. The cgroup Filesystem

Linux exposes cgroup configuration and accounting through a virtual
filesystem, commonly mounted under:

/sys/fs/cgroup/

Conceptually:

/sys/fs/cgroup/
       ↓
cgroup hierarchy
       ↓
Resource-control files

The exact files differ between cgroup versions.

This filesystem is one of the main places to investigate
resource-management behaviour on a Linux host.

10. Memory Control

Memory is one of the most important container resource controls.

Conceptually:

Container
    ↓
Memory cgroup
    ↓
Memory limit
    ↓
Kernel enforcement

For example, Docker can specify:

docker run --memory=512m my-app

The high-level intent is:

Container
    ↓
Memory limit ≈ 512 MB

The exact runtime and kernel behaviour around memory accounting and
reclaim depends on the host and cgroup configuration.

11. What Happens When Memory Is Exhausted?

Suppose:

Memory limit
     ↓
Application exceeds available memory

The kernel may reclaim memory or eventually invoke the out-of-memory
mechanisms associated with the cgroup.

From the container operator's perspective, this can appear as:

Application
    ↓
Memory pressure
    ↓
Process killed
    ↓
Container exits

Docker can expose useful state information such as:

OOMKilled

when inspecting a container.

The important troubleshooting lesson is:

A crashing container may be a resource-limit problem rather than an
application-code problem.

12. CPU Control

cgroups can also control CPU usage.

Conceptually:

Container
    ↓
CPU cgroup
    ↓
CPU allocation / limits
    ↓
Kernel scheduler

Docker can specify CPU-related constraints such as:

docker run --cpus=1 my-app

The exact CPU-control mechanism depends on the cgroup version and
runtime configuration.

The practical goal is:

Prevent one workload
from consuming uncontrolled CPU

13. CPU Limit vs CPU Usage

A CPU limit does not mean:

"Application will always use exactly 1 CPU."

It means the workload is constrained according to the configured CPU
control.

Actual usage can vary:

Idle
 ↓
Moderate usage
 ↓
Heavy usage
 ↓
Constrained by configured limit

Therefore, when troubleshooting CPU performance, distinguish:

Requested / configured limit
vs
Actual usage

14. CPU Shares / Weight

Linux cgroups can also influence how CPU is distributed among competing
workloads.

The exact terminology differs between cgroup versions.

The conceptual model is:

Container A ──┐
Container B ──┼── Compete for CPU
Container C ──┘
       ↓
Relative scheduling / weighting

This is different from a hard maximum.

A relative weight generally describes how CPU is shared when there is
contention.

15. Process Count Limits

cgroups can also control the number of processes/tasks in a workload.

Conceptually:

Container
    ↓
Process count limit
    ↓
Maximum task/process population

This can help reduce certain resource-exhaustion scenarios such as
uncontrolled process creation.

In Docker, an example is:

docker run --pids-limit=100 my-app

The exact enforcement is performed through Linux cgroup mechanisms.

16. I/O Control

cgroups can also participate in controlling or accounting for I/O
resources, depending on the kernel, storage stack, and cgroup
configuration.

Conceptually:

Container
    ↓
I/O control
    ↓
Storage workload

This is useful when multiple workloads compete heavily for disk
resources.

The exact controls available depend on:

Kernel version
cgroup version
Storage subsystem
Runtime configuration

Therefore, do not assume every Docker storage option maps identically
across every Linux host.

17. cgroup Resource Accounting

cgroups are not only about limits.

They can also provide resource accounting and usage information.

Conceptually:

Workload
    ↓
cgroup
    ↓
Usage metrics

This can help answer:

How much memory is the workload using?
How much CPU time has it consumed?
How many processes does it have?

This information is useful for:

Monitoring
Troubleshooting
Capacity planning

18. Docker Resource Limits and cgroups

When you run:

docker run \
  --memory=512m \
  --cpus=1 \
  --pids-limit=100 \
  my-app

the high-level Docker configuration is translated into runtime/kernel
resource controls.

Conceptually:

Docker CLI
    ↓
Docker Engine
    ↓
containerd
    ↓
OCI runtime
    ↓
cgroup configuration
    ↓
Linux kernel

This connects the previous containerd/runc topic directly with cgroups.

19. Checking Container Resource Configuration

At the Docker layer:

docker inspect my-app

can help identify configured resource-related settings.

For live usage:

docker stats my-app

is useful.

It can show information such as:

CPU %
Memory usage
Memory limit
Network I/O
Block I/O
PIDs

This gives two different views:

docker inspect
    ↓
Configuration

docker stats
    ↓
Observed usage

20. Resource Troubleshooting Sequence

If a container is slow or repeatedly restarting:

1. Check container state
        ↓
2. Check logs
        ↓
3. Check docker stats
        ↓
4. Check configured limits
        ↓
5. Check OOMKilled / exit state
        ↓
6. Check host capacity
        ↓
7. Inspect cgroup configuration
        ↓
8. Determine whether the application or limit is the root cause

This avoids assuming:

"Application is broken"

when the actual issue is:

"Container has an insufficient resource limit."

21. Example: Memory-Limited Container

Suppose:

docker run --memory=256m my-app

The application normally requires around:

400 MB

The lifecycle could become:

Application starts
      ↓
Memory usage increases
      ↓
Memory pressure
      ↓
cgroup limit reached
      ↓
Kernel OOM handling
      ↓
Process killed
      ↓
Container exits

If a restart policy exists:

Container exits
      ↓
Restart
      ↓
Application consumes memory
      ↓
Killed again

This creates a restart loop.

The correct fix may be:

Optimize application memory
or
Set an appropriate resource limit

rather than endlessly restarting the container.

22. Example: CPU-Constrained Application

Suppose:

docker run --cpus=0.5 my-app

and the application requires substantial CPU during startup.

The sequence may be:

Application starts
      ↓
CPU demand increases
      ↓
CPU constrained
      ↓
Startup becomes slow
      ↓
Health check may fail

This can produce a misleading symptom:

"Application is unhealthy."

when the underlying issue is:

Insufficient CPU allocation

Therefore, resource troubleshooting should include both:

Application metrics
+
Container resource metrics

23. cgroups and OOM Troubleshooting

When investigating an apparent memory crash:

Container stopped
      ↓
docker inspect
      ↓
Check OOMKilled

If it indicates an OOM-related termination, investigate:

Configured memory limit
        ↓
Actual memory usage
        ↓
Application memory behaviour
        ↓
Host memory pressure

Then decide whether the correct action is:

Increase appropriate limit
+
Fix application memory behaviour

rather than blindly increasing memory forever.

24. cgroups and Kubernetes

Kubernetes also relies heavily on cgroups for resource management.

A simplified model is:

Pod / Container
      ↓
Resource requests / limits
      ↓
Container runtime
      ↓
cgroups
      ↓
Linux kernel

For example:

resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "1"
    memory: "512Mi"

Kubernetes uses these resource definitions as part of scheduling and
runtime resource management.

The exact behaviour depends on Kubernetes version, runtime, and cgroup
configuration.

25. Requests vs Limits

Kubernetes introduces an important distinction:

Request
   ↓
Resource amount used for scheduling / expected allocation

Limit
   ↓
Maximum resource boundary enforced at runtime

This is different from simply saying:

"Container gets 512 MB."

The platform uses resource information for both:

Scheduling
+
Runtime enforcement

Understanding cgroups makes the runtime side of this model easier to
understand.

26. cgroups and Kubernetes QoS

Kubernetes can classify Pods into QoS categories based on their resource
requests and limits.

The major categories are:

Guaranteed
Burstable
BestEffort

The exact classification rules are defined by Kubernetes.

The connection to cgroups is:

Kubernetes resource configuration
        ↓
Runtime configuration
        ↓
cgroups
        ↓
Linux kernel

This becomes important during node resource pressure and
troubleshooting.

27. cgroups and the Kubernetes Node

On a Kubernetes node:

Node
 ├── Pod A
 │     ├── Container 1
 │     └── Container 2
 │
 ├── Pod B
 │     └── Container 1
 │
 └── System processes

Resource management can be represented through hierarchical cgroup
structures.

This allows the system to reason about:

Pod resources
Container resources
System resources

The exact hierarchy depends on runtime and Kubernetes configuration.

28. cgroup v2 and Unified Hierarchy

In cgroup v2, controllers are managed through a unified hierarchy.

A simplified model is:

/sys/fs/cgroup/
      ↓
Unified hierarchy
      ↓
Workload cgroups

This provides a more consistent model than the multiple-controller
hierarchy commonly associated with cgroup v1.

However, exact controller availability and configuration still depend
on:

Kernel
Host distribution
Runtime
System configuration

29. cgroup v2 Files

On a cgroup v2 system, files such as:

cpu.max
memory.max
memory.current
pids.max

can provide resource-control and accounting information.

For example, conceptually:

memory.max
    ↓
Memory limit

memory.current
    ↓
Current memory usage

The exact contents should be checked on the target host.

Do not blindly copy paths from a cgroup v2 system to a cgroup v1 system.

30. cgroup v1 Files

cgroup v1 uses separate controller hierarchies.

You may encounter paths such as:

/sys/fs/cgroup/memory/

or:

/sys/fs/cgroup/cpu/

depending on the host configuration.

This is one reason older troubleshooting guides can appear different
from modern Linux systems.

Always establish:

Which cgroup version?
Which controller?
Which runtime?
Which distribution?

before interpreting paths.

31. cgroup Namespace vs cgroups

These concepts should not be mixed up.

cgroups

Control and account for resources:

CPU
Memory
PIDs
I/O

cgroup namespace

Controls the cgroup hierarchy view exposed to a process.

Mental model:

cgroups
   ↓
Resource management

cgroup namespace
   ↓
Isolation of cgroup view

This is similar to the distinction between:

Network namespace

and:

Network configuration itself.

32. cgroups and Container Security

Resource controls also have a security and availability dimension.

Without appropriate resource controls:

Container
    ↓
Resource exhaustion
    ↓
Other workloads affected

With resource controls:

Container
    ↓
Bounded resources
    ↓
Reduced blast radius

cgroups therefore contribute to:

Reliability
Isolation
Capacity management
Security

But they are not a complete security boundary by themselves.

33. cgroups Do Not Prevent Application Bugs

Suppose an application has a memory leak:

Memory leak
    ↓
Memory usage continuously increases

A cgroup limit can constrain the damage:

Memory usage
    ↓
cgroup boundary
    ↓
OOM handling

But it does not fix the leak.

The correct approach is:

Resource control
+
Application diagnosis

This is an important production mindset.

34. cgroups and Host Resource Pressure

A container limit does not automatically mean the host has unlimited
resources.

Consider:

Host
 ├── Container A
 ├── Container B
 └── Container C

If the host itself is under heavy memory pressure:

Host memory pressure
      ↓
Kernel memory management
      ↓
Workload impact

Therefore, troubleshooting should distinguish:

Container-level limit
vs
Host-level capacity

Both can produce resource-related symptoms.

35. Resource Limits and Observability

Good observability should answer:

Configured limit?
Actual usage?
Historical usage?
Host capacity?
Application behaviour?

A useful model is:

Configuration
    +
Runtime metrics
    +
Application metrics
    +
Host metrics

Without these views, resource incidents can be difficult to diagnose.

36. IncidentLab Connection

IncidentLab's troubleshooting sequence becomes especially useful for
resource incidents.

Suppose:

Container keeps restarting

The investigation should be:

Container state
      ↓
Logs
      ↓
Exit code
      ↓
OOMKilled?
      ↓
docker stats
      ↓
Configured limits
      ↓
Host capacity
      ↓
cgroup configuration
      ↓
Application memory / CPU behaviour
      ↓
Root cause

This prevents the common mistake of treating:

Restarting

as the root cause.

It is only the symptom.

37. Connection to the Previous Topics

The deeper container stack now looks like:

Docker / Kubernetes
        ↓
containerd
        ↓
runc
        ↓
┌─────────────────────┐
│ Linux kernel        │
│                     │
│ Namespaces → view   │
│ cgroups    → usage  │
└─────────────────────┘
        ↓
Container process

This connects the previous two topics:

29-linux-namespaces.md
        +
30-linux-cgroups.md

Together they explain two of the most important kernel mechanisms behind
containers.

38. Interview Takeaway

A strong interview explanation is:

"Linux cgroups, or control groups, are a kernel mechanism used to
organize processes and control or account for their resource usage.
Containers use cgroups for things like CPU, memory, process-count, and
other resource controls. Namespaces isolate what a process can see,
while cgroups control how much of shared resources the workload can
consume. In troubleshooting, I check the configured limits, actual
usage, OOM state, and host capacity before deciding whether the issue
is the application or the resource configuration."

The simplest mental model is:

Namespaces
    ↓
Isolation

cgroups
    ↓
Resource control

39. Key Takeaways

cgroups means control groups.

cgroups are implemented by the Linux kernel.

They organize processes into resource-management groups.

They can control or account for CPU, memory, process count, and
other resources.

Namespaces and cgroups solve different problems.

Namespaces provide isolated resource views.

cgroups provide resource management and accounting.

Linux has cgroup v1 and cgroup v2.

Modern Linux systems increasingly use cgroup v2.

/sys/fs/cgroup/ is a key location for inspecting cgroup
configuration.

Docker resource limits are implemented through the runtime/kernel
resource-control stack.

docker stats shows useful live resource-usage information.

docker inspect helps inspect container configuration and state.

OOM-related container exits can be caused by memory limits.

CPU constraints can affect application performance and health
checks.

Process-count limits can reduce uncontrolled process creation.

Kubernetes resource requests and limits connect to runtime resource
management and cgroups.

cgroup namespaces are different from cgroups themselves.

cgroups reduce resource-exhaustion blast radius but do not fix
application bugs.

Always distinguish container-level limits from host-level resource
pressure.

40. Connections

Previous

29-linux-namespaces.md

Next

31-bind-mount-vs-volume.md

41. My Understanding

cgroups are best understood as the resource-control layer of
containers.

The mental model is:

Container process
       ↓
cgroup
       ↓
CPU / Memory / PIDs / I/O
       ↓
Linux kernel
       ↓
Resource enforcement / accounting

Together with namespaces:

Namespaces
   ↓
What can the process see?

cgroups
   ↓
How much can the process use?

This gives us a much deeper understanding of what happens underneath:

docker run --memory=512m --cpus=1 my-app

The command is only the high-level interface.

Underneath it:

Docker
   ↓
containerd
   ↓
runc
   ↓
Linux cgroups
   ↓
Linux kernel
   ↓
Container process

The key lesson is:

Containers share the host's resources, so cgroups provide the
mechanism for controlling and accounting for how workloads consume
those shared resources.
