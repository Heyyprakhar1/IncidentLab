Container Lifecycle

1. What Is the Container Lifecycle?

A container is not simply:

Created → Running

It moves through different states as it is created, started, stopped,
restarted, and eventually removed.

A useful mental model is:

Image
  ↓
Create
  ↓
Created
  ↓
Start
  ↓
Running
  ↓
Stop
  ↓
Exited
  ↓
Remove
  ↓
Deleted

Understanding this lifecycle is essential for:

troubleshooting

deployments

restart behaviour

persistent storage

CI/CD

incident response

2. Image vs Container Lifecycle

An image is the artifact.

A container is an instance created from that artifact.

Image
  ↓
docker create
  ↓
Container
  ↓
docker start
  ↓
Running process

The image can remain available even after the container is removed:

Image
 ├── Container A → removed
 ├── Container B → running
 └── Container C → stopped

This distinction is fundamental.

Removing a container does not automatically mean removing its
image.

3. docker create

The docker create command creates a container without starting its
main process.

Example:

docker create --name api my-app:latest

Conceptually:

Image
  ↓
docker create
  ↓
Created container
  ↓
Not running yet

At this stage Docker has created the container's configuration and
runtime metadata, but the main process has not started.

This is useful when you want to separate:

Container creation
from
Container startup

4. Created State

After:

docker create --name api my-app:latest

you can see the container with:

docker ps -a

The container is typically shown as:

Created

It has configuration such as:

Image
Command
Entrypoint
Environment
Network configuration
Mount configuration

but the application process is not running yet.

5. docker start

To start an existing created or stopped container:

docker start api

The lifecycle becomes:

Created
   ↓
docker start
   ↓
Container process starts
   ↓
Running

If the main process exits:

Running
   ↓
Process exits
   ↓
Exited

The same container can often be started again:

docker start api

6. docker run

docker run is commonly used when you want to create and start a
container in one operation.

Conceptually:

docker run my-app:latest

is approximately:

docker create
      ↓
docker start

with additional runtime configuration applied during creation.

Mental model:

Image
  ↓
Create container
  ↓
Start container
  ↓
Running

This is why docker run is so common in everyday Docker usage.

7. Running State

When the container's main process is running:

Container
    ↓
Running
    ↓
PID 1
    ↓
Application

You can see running containers with:

docker ps

A running container can have:

Logs
Network
Mounted storage
Processes
Resource usage
Health status

The container remains running as long as its primary process remains
alive, unless the runtime terminates it for another reason.

8. Container Health Is a Separate Concept

A container can be:

Running

while its application is unhealthy.

For example:

Container
   ↓
PID 1 alive
   ↓
Application cannot connect to database

If a health check is configured:

Running
+
Healthcheck
   ↓
Healthy / Unhealthy

Therefore:

Running
   ≠
Healthy

This distinction becomes particularly important in production
deployments.

9. docker stop

To stop a running container:

docker stop api

The normal lifecycle is:

Running
   ↓
Stop requested
   ↓
Termination signal
   ↓
Application shutdown
   ↓
Exited

The application should ideally handle the termination signal gracefully.

For example:

Stop accepting work
      ↓
Finish active requests
      ↓
Close connections
      ↓
Flush required state
      ↓
Exit

10. Graceful Shutdown

Graceful shutdown matters in production.

Suppose an API is processing a request:

Request
   ↓
Application
   ↓
Long-running operation

If the process is terminated immediately:

Request
   ↓
Process killed
   ↓
Incomplete operation

With graceful shutdown:

Stop signal
   ↓
Application stops accepting new work
   ↓
Existing work completes
   ↓
Connections close
   ↓
Process exits

This is why correct signal handling and PID 1 behaviour matter.

11. docker kill

docker kill is different from a normal graceful stop.

Example:

docker kill api

It is intended for immediate termination using a signal, with the
default being SIGKILL in common Docker usage.

Conceptually:

Running
   ↓
docker kill
   ↓
Process terminated
   ↓
Exited

Because the process may not get an opportunity to perform graceful
cleanup, docker kill should not be treated as the normal shutdown
mechanism for healthy applications.

12. docker pause

Docker can pause the processes in a container:

docker pause api

Conceptually:

Running
   ↓
Paused
   ↓
Processes suspended

Then:

docker unpause api

resumes the processes.

The lifecycle becomes:

Running
   ↓
Pause
   ↓
Paused
   ↓
Unpause
   ↓
Running

Pause is different from stop:

Pause
  ↓
Processes suspended

Stop
  ↓
Processes terminated

13. docker restart

Docker can restart an existing container:

docker restart api

Conceptually:

Running
   ↓
Stop
   ↓
Start
   ↓
Running

This is useful for controlled restarts.

However:

Restarting a container is not the same as fixing the underlying
problem.

If the application is misconfigured:

Restart
   ↓
Failure
   ↓
Restart
   ↓
Failure

the root cause remains.

14. Restart Policies

Docker supports restart policies such as:

no
on-failure
always
unless-stopped

For example:

docker run \
  --restart unless-stopped \
  my-app

The runtime can restart the container according to the configured
policy.

A useful mental model is:

Application exits
      ↓
Restart policy evaluated
      ↓
Restart or remain stopped

Restart policy behaviour depends on the reason and state of the
container.

15. Restart Loop

A restart loop looks like:

Start
  ↓
Application crashes
  ↓
Restart
  ↓
Application crashes
  ↓
Restart

This can create an incident where the container appears to be:

Restarting

The correct response is not simply:

docker restart api

Instead:

Check state
   ↓
Check exit code
   ↓
Check logs
   ↓
Identify startup failure
   ↓
Fix root cause

16. Exit State

When the main process terminates:

Running
   ↓
Process exits
   ↓
Exited

The container still exists.

You can see it with:

docker ps -a

For example:

CONTAINER ID
NAME
STATUS

might show:

Exited (1)

The container's state can therefore provide useful information during
troubleshooting.

17. Exit Code

An exited container has an exit code.

Inspect it with:

docker inspect \
  --format='{{.State.ExitCode}}' \
  api

A common interpretation is:

0
  ↓
Normal process completion

Non-zero
  ↓
Some form of failure / abnormal completion

Do not diagnose solely from the number.

Combine:

Exit code
+
Logs
+
Application behaviour

18. Container Removal

To remove a stopped container:

docker rm api

Conceptually:

Exited
   ↓
docker rm
   ↓
Container metadata/state removed

The image normally remains:

Image
   ↓
Still available

This distinction is important when cleaning up failed deployments.

19. docker rm -f

A running container normally needs to be stopped before removal.

The force option:

docker rm -f api

can force removal of a running container.

Conceptually:

Running
   ↓
Force removal
   ↓
Container removed

Because this bypasses a normal graceful shutdown flow, use it
intentionally rather than as the default cleanup command.

20. Container Removal vs Volume Removal

Removing a container does not necessarily remove a separately managed
Docker volume.

For example:

Container
   ↓
Volume

If the container is removed:

Container → deleted
Volume    → can remain

This is one reason persistent data can survive container replacement.

However, volume lifecycle and cleanup behaviour should always be
verified for the exact command and deployment tooling being used.

21. Anonymous vs Named Volumes

Named volume:

docker volume create app-data

has an explicit name:

app-data

An anonymous volume can be created without explicitly choosing a name.

For production workflows, named volumes or external storage are often
easier to identify and manage.

The important lifecycle concept is:

Container lifecycle
      ≠
Persistent storage lifecycle

22. Container Lifecycle and Immutable Images

A strong deployment pattern is:

Build image
   ↓
Push image
   ↓
Create container
   ↓
Run
   ↓
Replace container when needed

Rather than manually modifying the running container.

The principle is:

Treat the image as the deployment artifact and the container as a
disposable runtime instance.

If the application changes:

Source
   ↓
New image
   ↓
New container

rather than:

Running container
   ↓
Manual modification

23. Container Replacement

Suppose version v1 is running:

Image v1
   ↓
Container v1

A new version is built:

Image v2
   ↓
New container v2

The deployment can then move traffic or replace the old instance
according to the deployment platform.

Conceptually:

v1 running
    ↓
v2 validated
    ↓
v2 starts
    ↓
v1 removed

This is one of the foundations of immutable deployment patterns.

24. Container Lifecycle and Persistent Data

Containers should generally be treated as replaceable.

Persistent state should live outside the disposable container layer.

For example:

Container
   ↓
Application
   ↓
Database / Volume / External Storage

rather than:

Container
   ↓
Only copy of important data

This separation makes:

Restart
Replacement
Scaling
Deployment
Recovery

much safer.

25. Container Lifecycle in CI/CD

A typical CI/CD flow is:

Code
  ↓
Build image
  ↓
Test image
  ↓
Scan image
  ↓
Push registry
  ↓
Deploy new container
  ↓
Health check
  ↓
Promote

If deployment fails:

New container
    ↓
Startup failure
    ↓
Logs
    ↓
Diagnose
    ↓
Fix source/configuration
    ↓
Build new image

This is preferable to manually patching a failed production container.

26. Container Lifecycle and Health Checks

A deployment system may use health information to determine whether a
container is ready to serve traffic.

Conceptually:

Container starts
      ↓
Health check
      ↓
Healthy?
   ↙       ↘
 No         Yes
 ↓           ↓
Investigate  Serve traffic

A health check should represent meaningful application health.

For example:

HTTP /health

may verify that the application process is alive and able to respond.

27. Container Lifecycle and Dependencies

A container can start before its dependency is actually ready.

For example:

API starts
   ↓
Database not ready
   ↓
API fails

A robust application may handle this through:

Retry logic
Health checks
Dependency readiness
Orchestration

Do not assume:

Container started
    =
Dependency ready

Startup ordering and readiness are separate concepts.

28. Container Lifecycle and Signals

The lifecycle is strongly connected to signals:

Running
   ↓
SIGTERM / stop request
   ↓
Graceful shutdown
   ↓
Process exit
   ↓
Exited

If the application does not handle signals properly:

Stop
   ↓
Application does not shut down cleanly
   ↓
Forced termination may occur

This can cause:

Dropped requests
Unflushed data
Unclosed connections
Long shutdown times

29. Debugging Lifecycle Problems

If a container repeatedly exits:

1. docker ps -a
        ↓
2. docker inspect
        ↓
3. Check exit code
        ↓
4. docker logs
        ↓
5. Check CMD / ENTRYPOINT
        ↓
6. Check environment
        ↓
7. Check dependencies
        ↓
8. Check resources
        ↓
9. Reproduce
        ↓
10. Fix root cause

If it is restarting:

Check restart policy
+
Check why the process exits

If it cannot be stopped gracefully:

Check PID 1
+
Check signal handling

30. Common Lifecycle Mistakes

Treating containers as permanent servers

A container should generally be replaceable.

Storing important data in the writable layer

Container-local writable storage is not a reliable persistence strategy.

Using docker kill for every shutdown

Forceful termination can bypass graceful cleanup.

Using restart policies as a fix

Restarting a broken application does not remove the underlying failure.

Manually patching running containers

Manual changes disappear when the container is replaced.

Build a corrected image instead.

Confusing running with healthy

A process can be alive while the application is broken.

Removing containers without understanding storage

Persistent volumes can have a different lifecycle from containers.

31. Practical Lifecycle Commands

Create

docker create --name api my-app:latest

Start

docker start api

Run

docker run --name api my-app:latest

Stop

docker stop api

Kill

docker kill api

Pause

docker pause api

Unpause

docker unpause api

Restart

docker restart api

Remove

docker rm api

Force remove

docker rm -f api

The important part is understanding why each command is used, not
memorizing commands independently.

32. Production Lifecycle Mental Model

A production-oriented lifecycle can be represented as:

Image
  ↓
Create
  ↓
Start
  ↓
Running
  ↓
Healthy
  ↓
Serve traffic
  ↓
Stop / Replace
  ↓
Exited
  ↓
Remove

Persistent state follows a separate path:

Application
    ↓
Volume / Database / External storage
    ↓
Survives container replacement

This separation is fundamental to reliable container operations.

33. IncidentLab Connection

IncidentLab's troubleshooting approach can use lifecycle state as an
early diagnostic signal.

For example:

Incident:
Container unavailable
        ↓
Is container:
Created?
Running?
Exited?
Restarting?
Paused?
        ↓
Check state
        ↓
Check logs
        ↓
Check process
        ↓
Check dependencies
        ↓
Find root cause

For a deployment incident:

New image
   ↓
New container
   ↓
Startup
   ↓
Health
   ↓
Traffic

If failure occurs at:

Startup

investigate process/configuration.

If failure occurs at:

Health

investigate application readiness/dependencies.

If failure occurs at:

Traffic

investigate networking and exposure.

34. Interview Takeaway

A strong interview explanation is:

"A Docker container lifecycle starts with an image and moves through
creation, startup, running, stopping, exiting, and removal.
docker run typically creates and starts a container, while
docker create and docker start separate those operations. I
distinguish process state from application health, use graceful stop
and signal handling for shutdown, and treat containers as replaceable
runtime instances while keeping persistent data outside the container
writable layer."

The most important production principle is:

Immutable image
      ↓
Disposable container
      ↓
Persistent external state

35. Key Takeaways

An image is the artifact; a container is a runtime instance.

docker create creates without starting the main process.

docker start starts an existing container.

docker run generally combines creation and startup.

A running container depends on its primary process remaining alive.

docker stop provides a normal shutdown path.

docker kill is intended for forceful termination.

docker pause suspends container processes without
stopping/removing the container.

docker restart performs a stop/start cycle.

Exited containers still exist until removed.

docker rm removes the container, not normally its image.

Persistent volumes have a lifecycle separate from containers.

Restart policies can improve availability but do not fix root
causes.

Health is different from process state.

Containers should generally be treated as replaceable.

Important persistent state should live outside the disposable
container layer.

CI/CD should build and deploy new images rather than manually patch
running containers.

Signal handling and PID 1 behaviour affect graceful shutdown.

Lifecycle state is an important troubleshooting signal.

36. Connections

Previous

25-debugging-containers.md

Next

27-oci-image-specification.md

37. My Understanding

The Docker container lifecycle is best understood as:

Image
  ↓
Create
  ↓
Start
  ↓
Running
  ↓
Stop / Process exit
  ↓
Exited
  ↓
Remove

with additional runtime states such as:

Paused
Restarting
Healthy / Unhealthy

The most important operational distinction is:

Image
   ↓
Immutable deployment artifact

Container
   ↓
Disposable runtime instance

Persistent storage
   ↓
Independent lifecycle

This model makes deployments, troubleshooting, scaling, and recovery
much easier to reason about.

Treat containers as replaceable. Keep important state outside them.
Build a new image when the application changes.
