Docker Image Inspection

1. What Is Image Inspection?

Docker image inspection is the process of examining an image's metadata,
configuration, layers, and other build-related information to understand
what the image actually contains and how it is configured.

A common command is:

docker image inspect <image>

For example:

docker image inspect incidentlab:latest

The basic mental model is:

Docker Image
      ↓
docker image inspect
      ↓
Metadata + Configuration
      ↓
Understand / Troubleshoot / Verify

Image inspection is especially useful when the Dockerfile alone does not
tell us what ended up in the built image.

2. Why Does Image Inspection Matter?

A Dockerfile describes how an image should be built.

Inspection tells us what the resulting image actually contains or is
configured to do.

For example, we may need to verify:

Which user does the container run as?
Which command starts it?
Which environment variables exist?
Which ports are declared?
Which volumes are declared?
Which labels are attached?
Which architecture does the image target?

The engineering flow becomes:

Dockerfile
    ↓
Build
    ↓
Docker Image
    ↓
Inspect
    ↓
Verify actual image configuration

This is an important troubleshooting habit:

Do not assume the image contains what the Dockerfile appears to
describe. Inspect the artifact when the configuration matters.

3. Basic Inspection Command

The primary command is:

docker image inspect <image>

For example:

docker image inspect my-app:latest

Docker returns structured information about the image.

The output can contain information related to:

Image identity
Configuration
Architecture
OS
Environment
Entrypoint
Command
Labels
Volumes
Exposed ports
Root filesystem
Layers

The exact output depends on the Docker version and image.

4. Image Name and Tag Matter

Before inspecting an image, make sure you are inspecting the correct
image reference.

For example:

docker images

can help identify local images.

You might see:

REPOSITORY   TAG      IMAGE ID
incidentlab  latest   ...
incidentlab  0.8.0    ...

Inspecting:

docker image inspect incidentlab:latest

is not necessarily the same as:

docker image inspect incidentlab:0.8.0

This becomes particularly important during troubleshooting when multiple
versions exist locally.

The mental model is:

Wrong image
    ↓
Correct inspection output
    ↓
Wrong conclusion

Always verify the image reference first.

5. Inspecting Image Configuration

One of the most useful parts of image inspection is the configuration
section.

It can reveal settings such as:

Entrypoint
Cmd
Env
WorkingDir
User
ExposedPorts
Volumes
Labels
Healthcheck

Conceptually:

Image
  ↓
Config
  ├── User
  ├── WorkingDir
  ├── Env
  ├── Entrypoint
  ├── Cmd
  ├── ExposedPorts
  ├── Volumes
  └── Healthcheck

This allows us to verify whether the image's runtime configuration
matches our expectations.

6. Inspecting ENTRYPOINT

Suppose the Dockerfile contains:

ENTRYPOINT ["python", "app.py"]

Image inspection can help verify the resulting entrypoint configuration.

Conceptually:

Dockerfile
    ↓
ENTRYPOINT
    ↓
Image Config
    ↓
Inspect
    ↓
Verify

This is useful when a container starts with an unexpected process.

A troubleshooting question becomes:

What does the image actually have configured as its entrypoint?

7. Inspecting CMD

Similarly, if the Dockerfile contains:

CMD ["--port", "8000"]

or:

CMD ["python", "app.py"]

inspection can help verify the configured command.

This becomes especially useful when ENTRYPOINT and CMD are combined.

For example:

ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]

The image configuration can be inspected to confirm both values.

8. Inspecting Environment Variables

The image configuration can also contain environment variables defined
through:

ENV

For example:

ENV APP_ENV=production

Inspection can reveal the image-level environment configuration.

This is useful for verifying:

Was the ENV instruction applied?
Is the expected value present?
Am I inspecting the correct image?

However, inspection also reinforces an important security principle:

Do not put secrets into image environment variables.

Image configuration can be inspected by users who have access to the
image.

9. Inspecting the User

If the Dockerfile contains:

USER appuser

image inspection can help verify that the resulting image is configured
to run under the intended user.

This is useful for production security validation.

Conceptually:

Dockerfile
    ↓
USER appuser
    ↓
Image configuration
    ↓
Inspect
    ↓
Verify non-root runtime

If a security requirement says:

Application must not run as root

inspection can provide evidence of the image's configured user.

10. Inspecting WORKDIR

If the Dockerfile contains:

WORKDIR /app

inspection can help verify the resulting working directory.

This matters when the application uses relative paths.

For example:

Expected:
    /app

Actual:
    /

can cause:

File not found
Configuration not found
Wrong relative path

Inspection helps distinguish a Dockerfile configuration problem from an
application problem.

11. Inspecting Exposed Ports

If the image contains:

EXPOSE 8000

inspection can reveal the declared exposed port metadata.

This helps verify:

Expected container port
        vs
Actual image metadata

Remember:

EXPOSE
    ↓
Container port metadata

-p
    ↓
Runtime port publishing

Inspection of ExposedPorts does not prove that the host is publishing
that port.

12. Inspecting Volumes

If the Dockerfile contains:

VOLUME ["/data"]

image inspection can reveal the declared volume path.

This can help answer:

Does this image declare /data as a volume?

Again, distinguish:

Image metadata
    vs
Actual runtime volume mount

For runtime mount information, inspect the container as well.

13. Inspecting Labels

If the Dockerfile contains:

LABEL org.opencontainers.image.version="0.8.0"

image inspection can verify the metadata.

This is useful for:

Version tracking
Ownership
Source information
Build metadata
Release traceability

The flow becomes:

CI/CD
  ↓
Build metadata
  ↓
LABEL
  ↓
Image
  ↓
Inspect
  ↓
Traceability

14. Inspecting Healthcheck Configuration

If the Dockerfile defines:

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

image inspection can help verify that a health-check configuration
exists.

This is useful when debugging:

Container running
      ↓
Expected health check
      ↓
Is it actually configured?

Remember that image inspection verifies the configuration.

Runtime health status is a container-level concern.

For actual health status, inspect the running container.

15. Image Layers and Root Filesystem Information

Image inspection also provides information related to the image's root
filesystem and layers.

This can help answer questions such as:

What layer information does this image contain?
What is the image's filesystem structure?
What image configuration is associated with it?

A related command is:

docker history <image>

which is often easier for understanding image-layer history.

Mental model:

docker image inspect
    ↓
Structured image metadata/configuration

docker history
    ↓
Layer/history-oriented view

Use the command that matches the question you are trying to answer.

16. docker image inspect vs docker inspect

Docker provides both:

docker image inspect <image>

and:

docker inspect <container>

They answer different questions.

Image inspection

docker image inspect my-app:latest

asks:

"What is configured in this image?"

Container inspection

docker inspect my-app-container

asks:

"How is this specific container configured and running?"

The container may add runtime information such as:

Network settings
Mounts
Container state
IP address
Runtime configuration

This distinction is extremely important during troubleshooting.

17. Image vs Container Troubleshooting

Suppose an application cannot find a file.

Start with:

Image
  ↓
Does the image contain the expected configuration?

Then:

Container
  ↓
Was the correct image actually used?

Then:

Runtime
  ↓
Was a volume mounted over the expected path?

A useful sequence is:

Image configuration
       ↓
Container configuration
       ↓
Runtime state
       ↓
Application behaviour

This prevents mixing build-time and runtime problems.

18. Formatting Inspection Output

The raw output of:

docker image inspect my-app

can be large.

Docker supports formatted output using:

docker image inspect \
  --format '{{.Config.User}}' \
  my-app

This can extract a specific field.

For example, depending on the image:

docker image inspect \
  --format '{{.Config.WorkingDir}}' \
  my-app

can help verify the working directory.

The broader principle is:

Large inspection output
       ↓
Select relevant field
       ↓
Faster troubleshooting

This is especially useful in scripts and CI/CD checks.

19. Image Inspection in CI/CD

Image inspection can also be part of automated validation.

A pipeline can build an image and then verify properties such as:

Expected user
Expected labels
Expected entrypoint
Expected working directory
Expected exposed ports

Conceptually:

Build image
    ↓
Inspect image
    ↓
Validate metadata
    ↓
Pass / Fail pipeline

This turns Dockerfile expectations into automated checks.

For example, an organization could enforce:

Runtime user != root

as part of an image-validation stage.

20. Common Mistakes

Inspecting the wrong image

Multiple tags or image versions can exist locally.

Always verify:

docker images

before drawing conclusions.

Confusing image configuration with container state

An image may declare:

EXPOSE 8000

but a specific container may have:

different port publishing
different mounts
different network configuration

Inspect the appropriate object.

Treating inspection as a security scan

docker image inspect shows configuration and metadata.

It does not replace:

Vulnerability scanning
Secret scanning
Dependency scanning
Runtime security analysis

Assuming image metadata proves application health

An image can have:

HEALTHCHECK configured

while the running application is still unhealthy.

Configuration and runtime state are different.

21. Troubleshooting Mental Model

When a container behaves unexpectedly:

What am I troubleshooting?
        ↓
Image?
        │
        └── docker image inspect
        ↓
Container?
        │
        └── docker inspect
        ↓
Layers?
        │
        └── docker history
        ↓
Runtime logs?
        │
        └── docker logs

A more complete sequence is:

Image
  ↓
Container configuration
  ↓
Network / mounts / process
  ↓
Logs
  ↓
Application

This keeps troubleshooting systematic.

22. Production Relevance

Image inspection is valuable in production because the image is a
deployment artifact.

Before an image is promoted, teams may want to verify:

Correct version
Correct user
Correct entrypoint
Correct labels
Correct healthcheck
Correct runtime configuration

This becomes particularly useful in CI/CD pipelines where the same image
moves through:

Build
  ↓
Test
  ↓
Scan
  ↓
Validate
  ↓
Registry
  ↓
Deployment

Inspection can therefore become part of artifact validation.

23. IncidentLab Connection

IncidentLab's troubleshooting-oriented workflow makes image inspection
particularly useful.

When a container does not behave as expected, the investigation can
start with:

Docker image
      ↓
docker image inspect
      ↓
Verify configuration
      ↓
docker inspect
      ↓
Verify runtime configuration
      ↓
docker logs
      ↓
Verify application behaviour

This reinforces the broader troubleshooting principle used throughout
the project:

Start with the layer where the problem can logically exist, then
move forward instead of changing configuration randomly.

24. Interview Takeaway

A strong interview explanation is:

"I use docker image inspect to verify the configuration and
metadata of the image artifact itself --- things like user, working
directory, environment, entrypoint, command, labels, exposed ports,
volumes, and health-check configuration. If I need runtime information
such as mounts, networking, or container state, I inspect the
container instead."

The key distinction is:

docker image inspect
        ↓
Image configuration

docker inspect <container>
        ↓
Container runtime configuration

25. Key Takeaways

docker image inspect examines an image's metadata and
configuration.

It helps verify what the built image actually contains or is
configured to do.

Useful fields include user, WORKDIR, ENV, ENTRYPOINT, CMD,
ports, volumes, labels, and health checks.

Image inspection is different from container inspection.

docker history provides a complementary layer/history view.

Formatted output can extract specific fields.

Inspection can be used in CI/CD artifact validation.

Image inspection is not a replacement for security or vulnerability
scanning.

Always verify the image tag/reference before troubleshooting.

A systematic inspection workflow helps separate image problems from
runtime problems.

26. Connections

Previous

18-dockerignore.md

Next

20-buildkit.md

27. My Understanding

Image inspection is the process of examining the built Docker image
rather than relying only on the Dockerfile.

The simplest mental model is:

Dockerfile
    ↓
Build
    ↓
Image Artifact
    ↓
docker image inspect
    ↓
Verify actual configuration

The most important troubleshooting distinction is:

Image problem
    ↓
docker image inspect

Container/runtime problem
    ↓
docker inspect

This helps turn Docker troubleshooting from guesswork into a structured
investigation of the actual artifact and its runtime state.

28. Questions for Further Exploration

Which docker image inspect fields are most useful during
production incidents?

How can image inspection be automated in GitHub Actions?

How does docker history complement image inspection?

How can image metadata be validated against organizational policies?

What is the difference between image configuration, image layers,
and container runtime configuration?
