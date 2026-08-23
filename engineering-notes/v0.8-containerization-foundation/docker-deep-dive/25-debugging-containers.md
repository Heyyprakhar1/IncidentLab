Debugging Containers

1. Why Container Debugging Needs a Sequence

When a container fails, the first mistake is often changing the
Dockerfile immediately.

A better approach is to identify which layer is actually failing.

Use this mental model:

Image
  ↓
Container creation
  ↓
Container process
  ↓
Application
  ↓
Network / Storage / Dependencies

The troubleshooting goal is:

Find the first layer where expected behaviour becomes actual
failure.

2. The Core Troubleshooting Sequence

A practical sequence is:

1. Is the image correct?
        ↓
2. Was the container created?
        ↓
3. Is the container running?
        ↓
4. What is the container state?
        ↓
5. What is PID 1?
        ↓
6. What do the logs say?
        ↓
7. What is the exit code?
        ↓
8. Are environment variables correct?
        ↓
9. Are mounts correct?
        ↓
10. Is networking correct?
        ↓
11. Are resources sufficient?
        ↓
12. Is the application itself healthy?

This sequence prevents random debugging.

3. First: Verify the Image

Before debugging the running container, confirm that the expected image
exists.

docker image ls

You can inspect a specific image:

docker image inspect my-app:latest

Check:

Image tag
Image ID
Created time
Entrypoint
CMD
Working directory
User
Environment
Exposed ports
Healthcheck

Mental model:

Wrong image
    ↓
Wrong container
    ↓
Everything after this can be misleading

4. Check Whether the Container Exists

Use:

docker ps

This shows running containers.

If the application is missing, use:

docker ps -a

This also shows stopped containers.

The distinction is important:

docker ps
    ↓
Currently running

docker ps -a
    ↓
Running + stopped

A container that starts and immediately exits will appear in:

docker ps -a

but not in:

docker ps

5. Check Container State

Inspect the container:

docker inspect my-app

Look at the state information.

Useful fields include:

Status
Running
StartedAt
FinishedAt
ExitCode
Error
OOMKilled
Restarting

A useful question is:

Did the container fail to start, or did the application start and
then exit?

These are different failure classes.

6. Check the Logs Early

Use:

docker logs my-app

For a recent portion:

docker logs --tail 100 my-app

For timestamps:

docker logs -t my-app

Logs can reveal:

Configuration errors
Missing dependencies
Application exceptions
Database connection failures
Port binding problems
Permission errors
Startup failures

Do not change configuration before checking whether the application has
already explained the failure.

7. Container Exit Codes

If a container stops, inspect its exit code:

docker inspect \
  --format='{{.State.ExitCode}}' \
  my-app

An exit code provides a clue about how the process terminated.

For example:

0

generally indicates normal process completion.

A non-zero exit code generally indicates an error.

Do not interpret an exit code in isolation.

Use it together with:

Logs
+
Container state
+
Application behaviour

8. The Container Starts and Immediately Stops

This is a common beginner issue.

Example:

docker run my-app

The container starts:

Container
   ↓
PID 1
   ↓
Process exits
   ↓
Container stops

Remember:

A container normally lives as long as its primary process lives.

If the application process completes immediately, the container can stop
immediately.

9. Check CMD and ENTRYPOINT

If the container exits unexpectedly, inspect:

docker image inspect my-app

Check:

Entrypoint
Cmd

For example:

CMD ["python", "app.py"]

If:

app.py

does not exist, the process may exit immediately.

Another common problem is an incorrect executable:

CMD ["python3", "server.py"]

when the image does not contain:

python3

The debugging sequence is:

Container exits
    ↓
Check logs
    ↓
Check CMD / ENTRYPOINT
    ↓
Check executable
    ↓
Check required files

10. Check PID 1

If the container is running:

docker exec my-app ps

or, when available:

docker exec my-app ps aux

You want to understand:

What is the main process?
Is it actually the expected application?
Is a shell unexpectedly acting as PID 1?

The process model matters because:

PID 1
   ↓
Signals
   ↓
Graceful shutdown

Poor process setup can cause confusing runtime behaviour.

11. Check the Application Process

A container being Up does not prove that the expected application is
working.

For example:

Container: Running
Application: Broken

Check the process:

docker exec my-app ps aux

You can also inspect:

docker top my-app

This helps answer:

Which processes are actually running?

12. docker exec for a Running Container

When a container is running, you can execute a command inside it:

docker exec -it my-app sh

If Bash exists:

docker exec -it my-app bash

Use this to inspect:

Filesystem
Environment
Processes
DNS
Network connectivity
Permissions
Application files

But remember:

docker exec is an investigation tool, not normally a production
fix.

If you manually modify the running container, those changes are not
automatically reflected in the image.

13. What If the Container Exits Too Quickly?

If the container exits immediately:

docker exec

cannot be used because there is no running process to enter.

Instead:

docker logs
       ↓
docker inspect
       ↓
Exit code
       ↓
Image configuration

For deeper investigation, you can sometimes override the startup command
and launch a shell using an appropriate debugging approach.

The important principle is:

Do not assume docker exec is always available. It requires a
running container.

14. Environment Variable Problems

A container may run but fail because required configuration is missing.

For example:

DATABASE_HOST
DATABASE_USER
DATABASE_PASSWORD

may be required.

Inspect the runtime environment:

docker inspect my-app

or, inside a running container:

docker exec my-app env

Look for:

Missing variable
Wrong value
Unexpected environment

Be careful when displaying or sharing environment output because it may
contain secrets.

15. Build-Time vs Runtime Configuration

A common debugging mistake is confusing:

ARG

with:

ENV

Conceptually:

ARG
 ↓
Build-time

ENV
 ↓
Image/runtime environment

If a value is required by the application at runtime, verify that it is
actually available at runtime.

The debugging question is:

Was this value needed during the build, or when the container was
running?

16. Check File and Directory Permissions

A container can fail because the application user cannot access required
files.

For example:

Application user
       ↓
/app/config.yaml
       ↓
Permission denied

Inspect:

docker exec my-app ls -la /app

and:

docker exec my-app id

Check:

Current user
File owner
File permissions
Directory permissions
Mounted filesystem permissions

This is especially important when using:

USER appuser

17. Check Volume and Bind Mounts

If an application cannot read or write expected data, inspect mounts:

docker inspect my-app

Look at:

Mounts

Questions:

Is the mount present?
Is the source path correct?
Is the destination path correct?
Is it read-only?
Does the application user have permission?

Mental model:

Application
    ↓
/data
    ↓
Mount
    ↓
Actual storage

18. Data Disappears After Container Removal

If data disappears:

Was it written to the container writable layer?
        ↓
Container removed
        ↓
Data removed

If persistence is required, verify that the application writes to:

Volume
or
External persistent storage

rather than only to the container's writable layer.

19. Check Container Networking

If the application cannot reach another service, first inspect the
network configuration.

docker inspect my-app

Look for:

Networks
IP address
Network mode

Then determine:

Are both containers on the expected network?

For example:

api
 ↓
app-net
 ↓
db

If api and db are not connected to a common network, normal
container-to-container communication may fail.

20. Test DNS From Inside the Container

If the container is running, test the service name.

For example:

docker exec my-app getent hosts db

If available, other DNS tools may also help.

The sequence is:

Can DNS resolve the name?
       ↓
Yes → Check port/connectivity
No  → Investigate network/DNS

Avoid immediately using IP addresses as a workaround.

Container IPs can change.

21. Check the Correct Port

Suppose the database listens on:

5432

inside its container.

The application should normally use the service's container/network port
when communicating over the Docker network.

Do not confuse:

Host published port

with:

Container-to-container port

For example:

Host
 :15432
   ↓
Database container
 :5432

An application on the same Docker network would normally target:

db:5432

not:

localhost:15432

22. localhost Is a Common Networking Mistake

Inside a container:

localhost

usually means:

This same container

It does not automatically mean:

The host

or:

Another container

For example:

API container
    ↓
localhost:3306

means the API container itself.

If MySQL is in another container:

API
 ↓
mysql:3306

is the conceptual pattern on a user-defined network.

23. Check Port Publishing Separately

If the application works inside the container but cannot be reached from
the host:

Application
    ↓
Listening?
    ↓
Container port?
    ↓
Published host port?

Inspect:

docker port my-app

This helps verify host-to-container port mappings.

Remember:

Application listening
      ≠
Host port published

Both need to be correct for host access.

24. Check Whether the Application Is Listening

Inside a container, use an available networking/process tool to check
listening sockets.

For example, if ss exists:

docker exec my-app ss -lntp

You want to know:

Is the application listening?
Which port?
Which address?

A frequent issue is an application listening only on:

127.0.0.1

instead of:

0.0.0.0

For a containerized web service that must accept connections through the
container network, the application commonly needs to bind to an
appropriate non-loopback interface.

25. Check Health Status

If the image defines a health check:

docker ps

may show:

healthy

or:

unhealthy

You can inspect the health details:

docker inspect my-app

The important distinction is:

Running
   ≠
Healthy

If the container is running but unhealthy:

Check healthcheck command
        ↓
Run the same check manually
        ↓
Check application logs
        ↓
Check dependency connectivity

26. Resource Problems

A container can fail because it is running out of resources.

Check:

docker stats my-app

Look at:

CPU
Memory
Network I/O
Block I/O

If the container is repeatedly killed, inspect:

docker inspect my-app

and check relevant state information such as:

OOMKilled

A common pattern is:

Memory limit
    ↓
Application exceeds limit
    ↓
Process killed
    ↓
Container exits/restarts

27. Restart Loops

A container repeatedly restarting can look like:

Starting
   ↓
Crash
   ↓
Restart
   ↓
Crash
   ↓
Restart

Do not treat the restart itself as the root cause.

Investigate:

Exit code
Logs
Application startup
Environment
Dependencies
Resources

A restart policy may only be exposing an underlying application problem
more frequently.

28. Check Dependencies

Applications often depend on:

Database
Redis
External API
Message broker
Filesystem
DNS
Cloud service

If startup fails:

Application
    ↓
Dependency unavailable
    ↓
Application exits

Check the dependency separately.

For example:

DNS
 ↓
Port
 ↓
Authentication
 ↓
Application protocol

A successful TCP connection does not necessarily prove that
authentication or the application protocol is working.

29. Debugging With docker inspect

docker inspect is one of the most valuable troubleshooting tools.

Use:

docker inspect my-app

to investigate:

State
Image
Command
Entrypoint
Environment
Mounts
Networks
Port bindings
Restart policy
Healthcheck
User

The principle is:

Inspect the actual container instead of assuming the Dockerfile is
exactly how the container was started.

Runtime flags, Compose configuration, or orchestration settings can
change behaviour.

30. Compare Image Configuration With Container Configuration

A useful troubleshooting distinction is:

Image configuration
        ↓
What the image defines

Container configuration
        ↓
What this specific instance received

For example:

Image CMD
       +
Runtime command override
       ↓
Actual container command

Similarly:

Image ENV
       +
Runtime environment
       ↓
Actual environment

This distinction is critical when debugging CI/CD or Compose
deployments.

31. Debugging a Docker Compose Application

For multi-container applications:

docker compose ps

shows service state.

Logs can be viewed with:

docker compose logs

or for one service:

docker compose logs api

The troubleshooting flow becomes:

Compose project
    ↓
Which service failed?
    ↓
Service logs
    ↓
Service dependencies
    ↓
Network
    ↓
Volumes
    ↓
Environment

Do not debug every service simultaneously.

Start with the first failed dependency in the chain.

32. Find the First Failure

Suppose:

frontend
   ↓
api
   ↓
database

and the frontend is failing.

Do not immediately debug the frontend.

Check:

Is database healthy?
        ↓
Is API healthy?
        ↓
Can API reach database?
        ↓
Can frontend reach API?

The first failure in the dependency chain is often the most useful
starting point.

33. Common Error Patterns

exec format error

Possible causes include:

Wrong CPU architecture
Incorrect binary
Incompatible executable

Investigate:

Image architecture
Host architecture
Binary architecture
Multi-platform build

permission denied

Investigate:

User
File ownership
File permissions
Mounted filesystem
Executable permissions

connection refused

Usually means the target address was reached but nothing accepted the
connection on that port.

Investigate:

Is service running?
Is application listening?
Correct port?
Correct address?

connection timed out

Investigate:

Network path
Firewall / filtering
Incorrect destination
Service availability

no such host

Investigate:

DNS
Network membership
Service/container name
Docker network configuration

34. Do Not Debug by Randomly Changing Everything

A poor debugging process looks like:

Change Dockerfile
Change port
Change network
Change user
Change command
Restart everything

This destroys the ability to identify the actual cause.

A stronger approach is:

Observe
   ↓
Form hypothesis
   ↓
Run one targeted check
   ↓
Compare result
   ↓
Narrow scope
   ↓
Fix root cause
   ↓
Verify

This is the same troubleshooting discipline used in production
infrastructure.

35. A Practical Incident Example

Problem

API container keeps restarting.

Step 1 --- Check state

docker ps -a

Result:

Restarting

Step 2 --- Check logs

docker logs api

Result:

Connection refused to db:5432

Step 3 --- Check database

docker ps

Database is not running.

Step 4 --- Inspect database logs

docker logs db

Suppose the database failed because of a permissions problem on its
mounted data directory.

Now the investigation becomes:

API restart
    ↓
DB unavailable
    ↓
DB startup failure
    ↓
Volume permission issue
    ↓
Root cause

This is much better than changing the API Dockerfile.

36. Production Troubleshooting Mental Model

For a production container incident:

Symptom
   ↓
Container state
   ↓
Exit code
   ↓
Logs
   ↓
Process
   ↓
Configuration
   ↓
Storage
   ↓
Network
   ↓
Resources
   ↓
Dependencies
   ↓
Application
   ↓
Root cause

The exact order can vary depending on the symptom, but the principle
remains:

Move from observable infrastructure state toward the application
instead of guessing.

37. IncidentLab Connection

IncidentLab is specifically designed around incident and troubleshooting
thinking.

Container debugging fits naturally into that model:

Incident
   ↓
Identify failing component
   ↓
Container state
   ↓
Logs
   ↓
Runtime configuration
   ↓
Network / Storage
   ↓
Dependencies
   ↓
Application
   ↓
Root Cause

For CI/CD-created containers, also compare:

What the Dockerfile defines
        vs
What CI/CD actually runs
        vs
What the runtime actually received

This distinction becomes extremely important when troubleshooting
deployment failures.

38. Interview Takeaway

A strong interview explanation is:

"When debugging a Docker container, I don't immediately modify the
Dockerfile. I first check whether the expected image and container
exist, inspect the container state and exit code, check logs, verify
PID 1 and the startup command, then move through environment
variables, mounts, networking, resources, dependencies, and
application health. I try to identify the first failing layer and make
one targeted change at a time."

The key principle is:

Observe
   ↓
Isolate
   ↓
Test
   ↓
Fix
   ↓
Verify

39. Key Takeaways

Start with the actual symptom instead of changing configuration
randomly.

Verify the image before debugging the container.

Use docker ps -a to find containers that already exited.

Check container state and exit code.

Read logs early.

Understand PID 1 and the container's main process.

Verify CMD and ENTRYPOINT.

Use docker exec only when the container is running.

Inspect environment variables carefully.

Check user and filesystem permissions.

Verify volumes and bind mounts.

Check network membership and DNS.

Do not confuse localhost with another container.

Do not confuse container ports with published host ports.

Check application listening sockets.

Distinguish Running from Healthy.

Investigate CPU and memory usage.

Treat restart loops as symptoms, not root causes.

Check dependencies in the correct order.

Use docker inspect to understand actual runtime configuration.

Find the first failure in a multi-container dependency chain.

Make one targeted change at a time.

Verify the fix after applying it.

40. Connections

Previous

24-image-optimization.md

Next

26-container-lifecycle.md

41. My Understanding

Container debugging is fundamentally a layer-isolation problem.

The mental model is:

Image
  ↓
Container
  ↓
Process
  ↓
Configuration
  ↓
Network / Storage / Resources
  ↓
Application

When something fails, the goal is not to change everything until it
works.

The goal is to answer:

Where does the expected behaviour stop?

Then:

Observe
   ↓
Form hypothesis
   ↓
Run targeted check
   ↓
Find root cause
   ↓
Fix
   ↓
Verify

The most important lesson is:

Good container troubleshooting is systematic, not experimental
guessing.
