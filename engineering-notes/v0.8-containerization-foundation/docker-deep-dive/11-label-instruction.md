LABEL Instruction

1. What Is LABEL?

LABEL adds metadata to a Docker image.

For example:

LABEL maintainer="team@example.com"

The label becomes metadata associated with the image.

A simple mental model is:

Docker image
     ↓
LABEL
     ↓
Image metadata

Unlike COPY or RUN, LABEL is not primarily about changing the
application's filesystem.

It describes the image.

2. Why Does LABEL Exist?

Docker images often need information that helps people and tools
understand what an image represents.

For example:

Who owns it?
What project does it belong to?
What version is it?
What environment is it intended for?
Where is the source repository?

Instead of putting this information into application files, it can be
attached directly as image metadata.

Example:

LABEL org.opencontainers.image.title="IncidentLab"
LABEL org.opencontainers.image.description="Production-inspired incident simulation platform"

The image can then carry descriptive information with it.

3. Basic Syntax

The basic form is:

LABEL <key>=<value>

For example:

LABEL version="1.0"

Multiple labels can be defined:

LABEL maintainer="platform-team@example.com"
LABEL version="1.0"
LABEL environment="production"

Modern Dockerfiles can also group related labels:

LABEL maintainer="platform-team@example.com" \
      version="1.0" \
      environment="production"

The exact formatting is a readability choice.

The important part is that each label is a key-value pair.

4. Labels Are Metadata

A label should be thought of as descriptive metadata, not application
configuration.

For example:

LABEL version="1.4.2"

does not automatically make the application behave as version 1.4.2.

It simply records:

Image metadata
    ↓
version = 1.4.2

This distinction is important.

Compare:

LABEL
  ↓
Metadata about the image

ENV
  ↓
Environment variable available to processes

They solve different problems.

5. Inspecting Labels

Docker provides image inspection capabilities that can expose label
metadata.

For example:

docker image inspect my-app

The output contains image configuration and metadata, including labels.

You can conceptually inspect:

Image
 ├── ID
 ├── Config
 ├── Architecture
 └── Labels

This makes labels useful when troubleshooting or inventorying images.

6. Useful Label Categories

A production image can use labels to describe information such as:

Project
Version
Source repository
Documentation URL
Vendor
Description
License
Build information

For example:

LABEL org.opencontainers.image.title="IncidentLab" \
      org.opencontainers.image.description="Incident simulation platform" \
      org.opencontainers.image.version="0.8.0" \
      org.opencontainers.image.source="repository-location"

These labels provide standardized descriptive information that tools can
consume.

7. OCI Image Labels

The Open Container Initiative (OCI) defines commonly used image
annotations.

A widely used naming convention is:

org.opencontainers.image.*

For example:

LABEL org.opencontainers.image.title="IncidentLab"
LABEL org.opencontainers.image.version="0.8.0"
LABEL org.opencontainers.image.description="Production-inspired incident simulation platform"

Common OCI-oriented metadata includes concepts such as:

title
description
version
source
url
documentation
vendor
licenses
revision
created

Using consistent metadata naming makes images easier for external
tooling and registries to understand.

8. Labels and Image Versioning

Labels can describe an image version:

LABEL org.opencontainers.image.version="0.8.0"

This can be useful for image inspection and inventory.

However, labels do not replace image tags.

For example:

docker build -t incidentlab:0.8.0 .

and:

LABEL org.opencontainers.image.version="0.8.0"

serve different purposes.

Conceptually:

Image tag
   ↓
Reference used to identify/select the image

Label
   ↓
Metadata describing the image

Both can be useful together.

9. Labels and Automation

Labels become particularly useful when infrastructure or tooling needs
to identify images based on metadata.

For example, an organization may want to identify:

team = platform
application = incidentlab
environment = production

Then external tooling can inspect image metadata and use those values
for inventory, reporting, or policy decisions.

The important architectural principle is:

Image
   ↓
Metadata
   ↓
Automation / inventory / tooling

Labels therefore become more valuable as the number of images and
services grows.

10. Labels vs ENV

This is a common interview distinction.

LABEL

LABEL team="platform"

is metadata attached to the image.

ENV

ENV APP_ENV=production

defines an environment variable that can be available to later build
instructions and container processes.

Mental model:

LABEL
  ↓
Describes the image

ENV
  ↓
Configures the environment

Do not use LABEL as a replacement for application runtime
configuration.

11. Labels vs ARG

ARG and LABEL can also appear together during image builds.

For example:

ARG VERSION=dev

LABEL org.opencontainers.image.version=$VERSION

Here:

ARG
  ↓
Build-time value
  ↓
LABEL
  ↓
Image metadata

This can be useful when CI/CD provides build information that should
become part of the image metadata.

For example:

Git commit
Build version
Release identifier

can be passed during the build and recorded in labels.

12. Build Information in Labels

A CI/CD pipeline can provide build metadata.

For example:

docker build \
  --build-arg VERSION=0.8.1 \
  -t incidentlab:0.8.1 .

Dockerfile:

ARG VERSION

LABEL org.opencontainers.image.version=$VERSION

The resulting image can carry:

version = 0.8.1

This creates a useful connection between:

Git / CI pipeline
       ↓
Build argument
       ↓
Docker image
       ↓
Image metadata

The label records information about how or what was built without making
that metadata part of the application's runtime configuration.

13. Labels and Security

Labels should not contain secrets.

Avoid:

LABEL api_key="secret-value"

or:

LABEL password="secret-value"

Image metadata can be inspected.

The same principle used for image contents applies here:

Labels
  ↓
Metadata
  ↓
Potentially visible to image consumers

Therefore, labels are appropriate for descriptive information, not
credentials.

14. Labels and Image Inspection

When troubleshooting an image, labels can help answer questions such as:

Which application is this?
Which version is it?
Which repository produced it?
Which team owns it?
Which revision was built?

A practical command is:

docker image inspect <image>

This makes labels useful alongside the other image-inspection
information.

For example:

Image inspection
      ↓
Metadata
      ↓
Labels
      ↓
Build / ownership / version context

15. Common Mistakes

Using labels for runtime configuration

Avoid:

LABEL APP_ENV="production"

when the application actually needs:

ENV APP_ENV=production

Labels describe the image; they are not a general runtime configuration
mechanism.

Putting secrets in labels

Never treat labels as a secure storage mechanism.

Avoid:

LABEL token="..."

Treating labels as image tags

These are different concepts:

Tag
  ↓
Image reference

Label
  ↓
Image metadata

A label does not replace a meaningful image-tagging strategy.

Adding meaningless metadata

Labels are most useful when they answer a real operational question.

Do not add large amounts of arbitrary metadata simply because the
Dockerfile supports it.

16. Troubleshooting Mental Model

If image metadata appears incorrect:

Inspect image
      ↓
Check Labels
      ↓
Is the LABEL instruction correct?
      ↓
Was the expected ARG value supplied?
      ↓
Was the image rebuilt after changing metadata?
      ↓
Are you inspecting the correct image/tag?

For example:

docker image inspect incidentlab:0.8.0

This helps distinguish:

Wrong Dockerfile
    vs
Wrong build argument
    vs
Old image
    vs
Wrong image/tag being inspected

17. Production Relevance

Labels become increasingly valuable in environments with many images.

They can support:

image inventory

ownership identification

release tracking

build provenance metadata

registry organization

automation

troubleshooting

operational visibility

A production image should ideally carry useful, consistent metadata
without turning labels into a dumping ground for arbitrary information.

18. IncidentLab Connection

IncidentLab follows a release-oriented engineering structure with
versions, tags, and documented milestones.

Labels can connect an image to that release context.

For example:

LABEL org.opencontainers.image.title="IncidentLab" \
      org.opencontainers.image.version="0.8.0" \
      org.opencontainers.image.description="Production-inspired incident simulation platform"

A CI/CD pipeline could also inject the current release or commit
revision:

Git release/tag
      ↓
CI/CD build
      ↓
Docker build argument
      ↓
LABEL
      ↓
Image metadata

This creates traceability between the source repository, build process,
and resulting container image.

19. Interview Takeaway

LABEL adds metadata to a Docker image.

A strong explanation is:

"I use LABEL to attach descriptive metadata to an image, such as
application name, version, source repository, ownership, or OCI
metadata. It helps with image inventory, traceability, and automation,
but it should not be used for runtime configuration or secrets."

The key distinction is:

LABEL
  ↓
Image metadata

ENV
  ↓
Environment configuration

ARG
  ↓
Build-time value

20. Key Takeaways

LABEL adds metadata to a Docker image.

Labels use key-value pairs.

Labels describe the image rather than changing application
behaviour.

docker image inspect can be used to inspect image metadata.

OCI provides commonly used org.opencontainers.image.* metadata
conventions.

Labels can improve ownership, version, and build traceability.

ARG values can be used to populate build-time image metadata.

Labels should never be used to store secrets.

Labels are different from image tags.

Labels are different from runtime ENV variables.

Useful labels become more valuable as image and service inventories
grow.

21. Connections

Previous

10-user-instruction.md

Next

12-expose-instruction.md

22. My Understanding

LABEL is an image-metadata mechanism.

It allows us to attach useful information to an image without confusing
that information with runtime configuration or application data.

The simplest mental model is:

Docker image
     ↓
LABEL
     ↓
"What is this image?"

For a production-oriented workflow, labels can provide traceability
from:

Source / Release
      ↓
CI/CD Build
      ↓
Docker Image
      ↓
Image Metadata

That makes them useful for operations, inventory, troubleshooting, and
automation.

23. Questions for Further Exploration

Which OCI image labels are most useful in production?

How should CI/CD populate image revision and version labels?

How can image labels be used by registry or deployment tooling?

What is the difference between image labels and Kubernetes labels?

How should image metadata support software supply-chain
traceability?
