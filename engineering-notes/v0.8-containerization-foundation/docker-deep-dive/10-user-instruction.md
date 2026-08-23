USER Instruction

1. What Is USER?

USER specifies the user and optionally the group that subsequent
Dockerfile instructions and the container's default process should run
as.

Example:

USER appuser

Mental model:

Container process
      ↓
USER
      ↓
Non-root identity

This is one of the most important Dockerfile instructions for container
security.

2. Why Avoid Root?

By default, many Linux containers historically run processes as:

root

Root inside a container is not automatically harmless.

If an application is compromised, unnecessary privileges can increase
the potential impact.

A better principle is:

Run the application with the minimum privileges it needs.

This is the principle of least privilege.

3. Creating a User

For example:

FROM python:3.12

RUN useradd --create-home appuser

WORKDIR /app
COPY . .

USER appuser

CMD ["python", "app.py"]

The application now starts as:

appuser

rather than root.

4. USER Affects Subsequent Instructions

USER affects subsequent Dockerfile instructions where user identity
matters.

For example:

USER appuser

RUN whoami

will run the relevant command as:

appuser

This is important when:

Creating files
Installing software
Changing permissions
Running build commands

5. USER and Runtime

The final USER instruction also establishes the default user for the
container process.

For example:

USER appuser

CMD ["python", "app.py"]

Conceptually:

Container starts
      ↓
appuser
      ↓
python app.py

The process does not need to run as root simply because Docker itself
starts the container.

6. USER and File Permissions

This is where USER commonly creates production issues.

Suppose:

USER appuser

but:

/app/data

is owned by root and is not writable by appuser.

Then:

Application
   ↓
Write /app/data
   ↓
Permission denied

A secure container therefore needs both:

Correct user
+
Correct filesystem permissions

7. Creating Files Before Switching User

A common pattern is:

RUN useradd --create-home appuser

WORKDIR /app
COPY . .

RUN chown -R appuser:appuser /app

USER appuser

The sequence is:

Create user
    ↓
Prepare filesystem
    ↓
Set ownership
    ↓
Switch user
    ↓
Run application

This avoids requiring root at runtime.

8. USER and COPY

COPY behaviour around ownership should be understood carefully.

For example:

COPY . /app

may create files with ownership based on the build environment/default
image user.

If the final process runs as:

appuser

the application may not be able to modify those files.

Where appropriate, Docker supports:

COPY --chown=appuser:appuser . /app

This can make ownership explicit.

9. USER by Numeric UID

You can specify a numeric UID:

USER 10001

This can be useful when:

Host / orchestrator identity mapping

matters.

Numeric identities can also make container behaviour more predictable
across environments, but filesystem ownership still needs to be
configured correctly.

10. USER and Group

You can specify both user and group:

USER appuser:appgroup

or:

USER 10001:10001

Conceptually:

UID
 ↓
User identity

GID
 ↓
Group identity

Both can affect access to files and other resources.

11. USER and Bind Mounts

This becomes particularly important with bind mounts.

Suppose:

Host directory
   ↓
Bind mount
   ↓
/app/data

and the container runs as:

UID 10001

If the host directory is not writable by that UID:

Application
   ↓
Write
   ↓
Permission denied

This is why bind-mount troubleshooting must consider:

Host ownership
+
Container UID/GID
+
Filesystem permissions

12. USER and Volumes

Volumes can have similar ownership issues.

For example:

Named volume
    ↓
Container
    ↓
appuser

The application may need the volume contents to have appropriate
ownership.

A common initialization approach is:

Temporary privileged setup
       ↓
Prepare volume
       ↓
Drop privileges
       ↓
Application

The exact pattern depends on the application.

13. USER and Rootless Containers

Running the application as a non-root user inside the container is not
exactly the same as running Docker itself rootlessly.

These are different concepts:

Non-root container process
    vs
Rootless container engine/runtime

Both improve security in different ways.

Do not use the terms interchangeably.

14. USER and Capabilities

Changing:

USER appuser

reduces normal user privileges.

Container security can go further with Linux capabilities and other
runtime security controls.

Conceptually:

Non-root user
      +
Reduced capabilities
      +
Read-only filesystem where possible
      +
Security profiles

provides stronger defence in depth.

USER is one layer, not the entire security model.

15. USER and Ports

A non-root process may have restrictions around binding to privileged
ports depending on the Linux environment and capabilities.

A common application design is:

Application inside container
      ↓
8080

rather than requiring:

80

inside the process.

Then Docker or an external proxy/load balancer can handle the externally
visible port.

For example:

Host:80
   ↓
Container:8080

This can allow the application to remain non-root.

16. USER and ENTRYPOINT

If:

USER appuser
ENTRYPOINT ["/entrypoint.sh"]

then the entrypoint normally starts under the configured user.

Therefore, the entrypoint script must itself be executable and able to
perform its initialization without unnecessary root privileges.

This is another reason to inspect:

File permissions
Ownership
Process identity

when debugging startup failures.

17. USER and CMD

Likewise:

USER appuser
CMD ["python", "app.py"]

means the application process starts using the configured user.

So:

USER
 ↓
CMD process identity

The command itself does not automatically switch back to root.

18. USER Placement

A common secure pattern is:

FROM python:3.12

RUN useradd --create-home appuser

WORKDIR /app

COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "app.py"]

The important ordering is:

Privileged setup
    ↓
Filesystem preparation
    ↓
Drop privileges
    ↓
Application

Avoid switching users too early if later build steps genuinely require
privileges.

19. USER and Package Installation

Suppose:

USER appuser

RUN apt-get update

This will generally fail because package installation requires
privileges.

The correct pattern is usually:

USER root

RUN apt-get update && apt-get install -y ...

USER appuser

The principle is:

Use elevated privileges only where required, then drop them before
the application runs.

20. USER and Multi-Stage Builds

Multi-stage builds can use different users in different stages.

For example:

Builder
   ↓
Build tools / required privileges

Runtime
   ↓
Non-root application user

The final production stage should be designed independently for runtime
security.

A builder running as root does not mean the final application must run
as root.

21. USER and Kubernetes

In Kubernetes, the container user can also be controlled through
Pod/container security settings.

Conceptually:

Dockerfile USER
       +
Kubernetes securityContext
       ↓
Runtime identity

The orchestrator can apply additional security controls.

Therefore, do not assume the Dockerfile is the only place where runtime
identity is configured.

22. Common Error: Container Works as Root but Not Non-Root

Suppose:

Root container
    ↓
Works

Non-root container
    ↓
Permission denied

This often indicates an application dependency on privileged access.

Investigate:

1. Which file/path fails?
2. Who owns it?
3. What UID/GID is running?
4. What permissions exist?
5. Does the application need write access?
6. Is a mounted volume involved?
7. Is the application trying to bind a restricted port?

Do not immediately revert to root.

Fix the actual permission requirement.

23. Troubleshooting Sequence

For a non-root container failure:

1. Check process user
        ↓
2. Check failing operation
        ↓
3. Check file ownership
        ↓
4. Check file permissions
        ↓
5. Check mounted storage
        ↓
6. Check required capabilities
        ↓
7. Check port binding
        ↓
8. Check entrypoint permissions
        ↓
9. Check runtime security configuration

This produces a much better diagnosis than simply saying:

"Run it as root."

24. Security Principle

The production goal is not:

Never use root anywhere.

The better principle is:

Use root only where required
        ↓
Perform privileged setup
        ↓
Drop privileges
        ↓
Run application with least privilege

This is practical least-privilege engineering.

25. Interview Takeaway

"The USER instruction sets the user and optionally group for
subsequent Dockerfile operations and the default container process.
For production containers I prefer running the application as a
non-root user, but I also make sure filesystem ownership, mounted
volumes, capabilities, and ports are compatible with that user. I
don't simply switch back to root when something fails; I investigate
the permission requirement."

Mental model:

USER
 ↓
Who runs the application?
 ↓
Least privilege
