ENV Instruction

1. What Is ENV?

ENV defines environment variables that become part of the image
configuration and are available to processes in containers created from
that image.

Example:

ENV APP_ENV=production

Mental model:

Docker image
    ↓
ENV
    ↓
Container process
    ↓
Environment variable

2. Why Use ENV?

Applications commonly need configuration such as:

APP_ENV
PORT
LOG_LEVEL
APP_HOME

Instead of hard-coding every value into application logic, environment
variables can provide runtime configuration.

For example:

ENV PORT=8080

and the application can read:

PORT

3. ENV Is Not a Secret Store

Do not treat:

ENV DB_PASSWORD=secret

as secure secret management.

Values placed in an image configuration can become discoverable through
image/container inspection and related metadata.

Therefore:

Configuration
    ≠
Secrets

Sensitive credentials should be supplied through an appropriate
secret-management mechanism.

4. ENV Persists Into Containers

Consider:

ENV APP_ENV=production

A container created from that image can see:

APP_ENV=production

The variable is available to processes launched in the container unless
overridden.

Conceptually:

Image
  ↓
ENV APP_ENV=production
  ↓
Container
  ↓
Process environment

5. ENV Can Be Overridden at Runtime

Suppose:

ENV APP_ENV=production

You can provide another value when starting the container:

docker run -e APP_ENV=staging my-app

The runtime value takes precedence for that container.

Conceptually:

Image default
    ↓
APP_ENV=production

Runtime override
    ↓
APP_ENV=staging

This is useful for environment-specific configuration.

6. ENV vs ARG

These instructions are frequently confused.

ARG

Build-time variable

ENV

Environment variable available to the image/container

Example:

ARG VERSION=1.0
ENV APP_VERSION=$VERSION

Here:

ARG
 ↓
Build-time input

ENV
 ↓
Persisted image environment configuration

Do not assume an ARG automatically exists at container runtime.

7. ENV During Build

An ENV variable can also be available to later Dockerfile
instructions.

For example:

ENV APP_HOME=/app

WORKDIR $APP_HOME

The later instruction can use the environment variable.

Conceptually:

ENV
 ↓
Build instruction environment
 ↓
Later instructions

It also becomes part of the resulting image configuration.

8. ENV and RUN

Example:

ENV APP_HOME=/app

RUN mkdir -p $APP_HOME

The variable can be used by the shell executing the RUN instruction.

But remember:

RUN
 ↓
Build-time execution

while:

ENV
 ↓
Image/container configuration

The variable can therefore affect both the build process and later
runtime depending on how it is used.

9. ENV and Shell Expansion

For shell-form commands, variables can be expanded by the shell.

For example:

ENV APP_HOME=/app

RUN echo $APP_HOME

The shell receives:

/app

For exec-form instructions, variable handling differs because Docker
does not invoke a shell automatically.

Therefore:

Shell form
    ↓
Shell expansion

Exec form
    ↓
No automatic shell

This distinction is important when debugging environment-variable
behaviour.

10. ENV and CMD

Consider:

ENV PORT=8080

CMD ["python", "app.py"]

The application can read:

PORT=8080

at runtime.

If the container is started with:

docker run -e PORT=9000 my-app

the application sees:

PORT=9000

This makes ENV useful for default configuration.

11. ENV and Configuration Strategy

A useful production model is:

Image
   ↓
Safe defaults
   ↓
Runtime environment
   ↓
Environment-specific values

For example:

ENV LOG_LEVEL=info

Then production can override:

-e LOG_LEVEL=warn

This keeps one image usable across multiple environments.

12. ENV and Immutability

A useful container principle is:

Same image
   ↓
Different runtime configuration

For example:

Image
 ├── development config
 ├── staging config
 └── production config

is generally less desirable than:

One image
   ↓
Runtime configuration
   ├── dev
   ├── staging
   └── production

Environment variables can support this model.

13. ENV and Secrets

Never assume:

ENV API_KEY=...

is safe simply because the container filesystem does not contain the
key.

The value is part of image configuration.

For sensitive values, use:

Secret manager
Docker secrets where applicable
CI/CD secret storage
Runtime secret injection

The principle is:

Build an image without embedding production credentials whenever
possible.

14. ENV and Image Reuse

Suppose an image contains:

ENV APP_ENV=production

That image can still be run with:

docker run -e APP_ENV=staging my-app

This makes runtime overrides useful for:

Development
Staging
Production

However, environment variables should represent configuration, not
radically change the application's architecture.

15. ENV and Docker Compose

Compose can provide environment variables:

services:
  api:
    image: my-api
    environment:
      APP_ENV: production
      LOG_LEVEL: info

The Dockerfile may define defaults:

ENV APP_ENV=production

while Compose can provide environment-specific values.

Conceptually:

Dockerfile
   ↓
Defaults

Compose / runtime
   ↓
Deployment configuration

16. Environment Variables and Precedence

When troubleshooting configuration, ask:

Where was the variable defined?

Possible sources include:

Dockerfile ENV
docker run -e
Compose environment
Orchestrator configuration
Shell / CI environment
Secret/config systems

The exact precedence depends on the tool and deployment method.

Do not assume the Dockerfile value is necessarily the final runtime
value.

17. ENV and Filesystem Paths

ENV is often useful for standard application paths.

Example:

ENV APP_HOME=/opt/app
WORKDIR $APP_HOME

This centralizes the path.

Conceptually:

APP_HOME
   ↓
WORKDIR
   ↓
Application

It can improve readability when the same value is reused across multiple
instructions.

18. ENV and PATH

A common example is:

ENV PATH="/opt/app/bin:${PATH}"

This can make executables available without specifying their full path.

However, modifying PATH should be done carefully so that existing
system paths are not accidentally removed.

19. ENV and Debugging

If an application behaves differently between environments:

Check environment variables

Useful commands include:

docker exec my-app env

or:

docker exec my-app printenv

You can also inspect the container configuration:

docker inspect my-app

The troubleshooting sequence is:

Expected value
      ↓
Actual container value
      ↓
Application reads it?
      ↓
Correct behaviour?

20. Common Error: Variable Is Empty

Suppose:

ENV API_URL=http://api:8080

but the application sees an empty value.

Investigate:

1. Was the container started from the expected image?
2. Was ENV overridden?
3. Is the variable name correct?
4. Is the application reading the same name?
5. Is a Compose/orchestrator setting replacing it?

Do not immediately rebuild the image.

21. Common Error: Secret Embedded in ENV

If:

ENV DB_PASSWORD=...

was used during an image build, changing the Dockerfile later does not
automatically erase the secret from every previously built image or
registry copy.

Treat the credential as potentially exposed and rotate it when
necessary.

The correct principle is:

Remove secret from source
+
Remove/rebuild affected artifacts
+
Rotate credential

22. ENV and Image Layers

Environment configuration becomes part of the image
configuration/history associated with the build.

Therefore:

ENV SOME_VALUE=...

should be treated as information that may persist beyond a single build
step.

This is another reason not to put sensitive values in ENV.

23. Interview Takeaway

"ENV defines environment variables that become part of the image
configuration and are available to processes in containers created
from that image. They are useful for defaults and runtime
configuration, and can be overridden at runtime. I would not use ENV
for secrets because image configuration can expose those values. I
distinguish ENV from ARG: ARG is primarily a build-time variable,
while ENV is available to the resulting container environment."

Mental model:

ENV
 ↓
Default environment configuration
 ↓
Container process
