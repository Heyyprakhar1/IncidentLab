HEALTHCHECK Instruction

1. What Is HEALTHCHECK?

HEALTHCHECK defines a command that Docker can use to determine whether
a running container is healthy.

For example:

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

The basic idea is:

Container
    ↓
Application process
    ↓
Health check
    ↓
Healthy / Unhealthy

The important distinction is:

A running container is not necessarily a healthy application.

A process can still exist while the application is unable to serve
requests correctly.

2. Why Does HEALTHCHECK Exist?

Consider a web application:

Container = running
Process   = running
Application = not responding

From a simple process perspective, the container is alive.

But operationally, the application may be unavailable.

A health check provides an additional signal:

Container running
       ↓
Health check executes
       ↓
Application responds correctly?
       ├── Yes → Healthy
       └── No  → Unhealthy

This is useful for detecting application-level failures.

3. Basic Syntax

The basic syntax is:

HEALTHCHECK CMD <command>

For example:

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

The command should return:

exit 0 → healthy
non-zero → unhealthy

The exact command depends on the application.

For example:

HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

can be used when the image does not contain curl.

4. Health Is Different From Process Existence

This distinction is fundamental.

A container can be:

Running

while the application is:

Broken

For example:

Application process
       ↓
deadlocked
       ↓
Process still exists
       ↓
Container still running

A suitable health check may detect that the application endpoint is no
longer responding correctly.

Mental model:

Running
  ↓
"Is the container process alive?"

Healthy
  ↓
"Is the application functioning as expected?"

These are related but different questions.

5. Health Check Exit Codes

A health check command communicates its result through an exit code.

The basic model is:

exit 0
   ↓
Healthy

non-zero
   ↓
Unhealthy

For example:

curl -f http://localhost:8000/health

returns success when the endpoint responds successfully.

Adding:

|| exit 1

makes the failure explicit.

The command should therefore be designed so that its success or failure
actually represents application health.

6. Configuring Health Check Timing

Docker allows health-check behaviour to be configured.

For example:

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

The important options are:

--interval
    How often the check runs

--timeout
    How long an individual check may take

--retries
    Consecutive failures before unhealthy status

A startup grace period can also be configured with:

--start-period

The values should be chosen according to how quickly the application
normally starts and how expensive the health check is.

7. --interval

Example:

HEALTHCHECK --interval=30s CMD ...

This means Docker performs the health check periodically according to
the configured interval.

Conceptually:

Start
  ↓
Health check
  ↓
Wait
  ↓
Health check
  ↓
Wait
  ↓
Health check

The interval should not be unnecessarily aggressive.

A health check that runs too frequently can create unnecessary
application and system load.

8. --timeout

Example:

HEALTHCHECK --timeout=5s CMD ...

This limits how long Docker waits for an individual check.

Mental model:

Health check starts
       ↓
Application responds?
       │
       ├── Quickly → Continue
       │
       └── Too slow → Check fails

The timeout should be long enough for normal application response time
but short enough to detect genuine problems.

9. --retries

Example:

HEALTHCHECK --retries=3 CMD ...

A temporary failure does not necessarily mean the application is
permanently unhealthy.

For example:

Check 1 → fail
Check 2 → fail
Check 3 → fail
        ↓
Unhealthy

The retry count helps prevent a single transient failure from
immediately producing an unhealthy state.

The appropriate value depends on the application's expected behaviour.

10. --start-period

Some applications need time to initialize.

For example:

Container starts
      ↓
Application initializes
      ↓
Database connection
      ↓
Application ready

A health check running immediately may fail during legitimate startup.

--start-period provides a startup grace period.

Example:

HEALTHCHECK \
    --start-period=20s \
    --interval=30s \
    --timeout=5s \
    --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

The goal is to distinguish:

Expected startup delay
        vs
Actual application failure

11. Choosing a Good Health Check

A health check should test something meaningful.

For a web API:

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

may be appropriate.

A weak health check might only test whether a process exists.

For example:

"Is python running?"

does not necessarily answer:

"Can the API serve requests?"

The best check is usually:

Application-specific
        +
Lightweight
        +
Reliable

12. Liveness vs Readiness Thinking

Health checks become easier to understand when we separate two concepts.

Liveness

"Is the application still alive?"

Readiness

"Is the application ready to receive traffic?"

Docker's HEALTHCHECK provides a health signal, but the exact meaning
of that signal depends on what command you define.

For example:

/health

might mean:

Application process is functioning

while:

/ready

might mean:

Application is ready to serve traffic

The endpoint design should match the operational purpose.

13. Health Check Should Be Lightweight

A health check can execute repeatedly.

Therefore, avoid expensive operations such as:

Large database queries
Full application test suites
Heavy filesystem scans
Complex external API calls

A better pattern is:

Health check
    ↓
Small request
    ↓
Quick response
    ↓
Meaningful signal

For example:

curl -f http://localhost:8000/health

is usually preferable to running a large diagnostic operation every 30
seconds.

14. Localhost and Container Networking

A health check runs in the container's environment.

Therefore, a command such as:

curl -f http://localhost:8000/health

targets the application from inside the container.

This is useful because the check can verify that the application itself
is reachable from the container environment.

It also means the health check does not necessarily prove that:

External client
      ↓
Load balancer
      ↓
Network
      ↓
Application

is working.

It mainly answers:

"Can this container reach its own application?"

External connectivity requires additional network-level checks.

15. HEALTHCHECK vs EXPOSE

These instructions solve different problems.

EXPOSE

EXPOSE 8000

documents the application's intended container port.

HEALTHCHECK

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

tests whether the application is responding as expected.

Mental model:

EXPOSE
   ↓
"What port does the application use?"

HEALTHCHECK
   ↓
"Is the application healthy?"

One does not replace the other.

16. HEALTHCHECK vs CMD

These are also different.

CMD

CMD ["python", "app.py"]

starts the application.

HEALTHCHECK

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

checks the application after it is running.

The flow is:

Container starts
      ↓
CMD / ENTRYPOINT
      ↓
Application starts
      ↓
HEALTHCHECK
      ↓
Health status

A health check does not replace the startup command.

17. Inspecting Container Health

You can inspect the container:

docker inspect <container>

Docker records health information in the container state when a health
check is configured.

A useful operational flow is:

Container
    ↓
docker inspect
    ↓
Health status
    ↓
Health-check output

This can help determine whether failures are:

Application startup
      vs
Application health
      vs
Container networking

18. Docker Compose and Health Checks

Health checks can also be used with Docker Compose.

For example:

services:
  api:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

Compose can then use health information when coordinating services.

For example, a dependent service may need to wait until another service
is considered healthy rather than merely started.

This becomes especially useful in local multi-container environments.

19. Health Checks and Dependencies

Consider:

API
 ↓
Database

The API container may start before the database is actually ready.

A health check can help distinguish:

Database container started
        vs
Database ready to accept connections

However, health checks should not be used as a replacement for proper
application retry and dependency-handling logic.

A resilient application should still handle temporary dependency
failures.

The broader pattern is:

Health check
      +
Application retry logic
      +
Orchestration
      ↓
More resilient system

20. Common Mistakes

Checking only whether the process exists

A running process can still be broken.

Making the check too expensive

Health checks run repeatedly.

Avoid turning them into full diagnostic tests.

Using an endpoint that always returns success

If:

/health

always returns HTTP 200 even when important application components are
unavailable, the health check may provide a misleading signal.

The endpoint should represent the health condition you actually care
about.

Checking external dependencies blindly

A health check that requires every external service to respond may mark
the application unhealthy because of a temporary dependency issue.

Whether dependencies belong in the check depends on the operational
meaning of "healthy."

Forgetting startup time

Applications that need time to initialize may appear unhealthy
immediately after startup.

Use an appropriate --start-period and retry strategy.

21. Troubleshooting Mental Model

If a container is marked unhealthy:

Container running?
      ↓
Health check configured?
      ↓
What exact command is executing?
      ↓
Can the command run inside the image?
      ↓
Is the application listening?
      ↓
Is the application listening on the expected port?
      ↓
Is the endpoint correct?
      ↓
Does the endpoint return success?
      ↓
Are timeout / interval / retries appropriate?

For example, if the health check uses:

curl -f http://localhost:8000/health

but the image does not contain curl, the health check itself will fail
even if the application is healthy.

This is a classic Docker troubleshooting trap.

22. Production Relevance

Health checks become important when containers are managed
automatically.

A production platform may need to know:

Should this container receive traffic?
Should it be considered healthy?
Should it be restarted?

The exact behaviour depends on the platform.

Docker's health status is one signal.

In Kubernetes, for example, readiness and liveness probes provide more
explicit orchestration semantics.

The important engineering principle is:

Health signalling should represent an operationally meaningful
condition, not simply container existence.

23. IncidentLab Connection

IncidentLab is designed around incident simulation and troubleshooting,
making health signalling particularly relevant.

A containerized API can expose a lightweight health endpoint:

/health

and the Dockerfile can use:

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

The resulting flow is:

IncidentLab API
      ↓
Application starts
      ↓
Health endpoint
      ↓
Docker HEALTHCHECK
      ↓
Healthy / Unhealthy
      ↓
Operational signal

This fits naturally into the project's broader troubleshooting and
observability direction.

24. Interview Takeaway

HEALTHCHECK defines a command Docker can use to determine whether a
running container is healthy.

A strong interview explanation is:

"I use HEALTHCHECK to verify application-level health rather than
relying only on the fact that the container process is running. For
example, for an API I can check a lightweight health endpoint and
configure an appropriate interval, timeout, retries, and startup
period. The check should be cheap and meaningful."

The key mental model is:

Container running
       ↓
Application running
       ↓
Health check
       ↓
Healthy / Unhealthy

25. Key Takeaways

HEALTHCHECK defines an application health test.

A running container is not necessarily healthy.

Health checks communicate success or failure through command exit
status.

--interval, --timeout, --retries, and --start-period control
health-check behaviour.

Checks should be lightweight and meaningful.

The health endpoint should represent the condition you actually care
about.

HEALTHCHECK is different from CMD, ENTRYPOINT, and EXPOSE.

A container health check mainly tests the application from the
container environment.

Health checks are useful in Compose and container orchestration.

Health checks do not replace application retry logic or a complete
monitoring strategy.

26. Connections

Previous

13-volume-instruction.md

Next

15-shell-vs-exec-form.md

27. My Understanding

HEALTHCHECK adds an application-level health signal to a Docker
container.

The simplest mental model is:

Container exists
      ↓
Container is running
      ↓
Is the application actually working?
      ↓
HEALTHCHECK
      ↓
Healthy / Unhealthy

The important lesson is that process existence and application health
are not the same thing.

A good health check is small, reliable, representative of the
application's operational health, and configured with enough tolerance
for normal startup and transient failures.

28. Questions for Further Exploration

What is the difference between Docker health checks and Kubernetes
liveness/readiness probes?

How should health endpoints treat database and external-service
dependencies?

What happens when a health check repeatedly fails?

How can health-check failures be integrated with monitoring and
alerting?

How should health checks be designed for applications with slow
startup times?
