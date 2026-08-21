Layer Caching Internals

1. Why Layer Caching Matters

Docker builds are made up of filesystem-changing instructions such as:

COPY
RUN
ADD

Docker can reuse the result of previously completed build work when the
relevant inputs have not changed.

The basic mental model is:

Dockerfile
    ↓
Build instructions
    ↓
Build results
    ↓
Cache
    ↓
Reuse unchanged work

This is one of the most important mechanisms behind fast Docker builds.

2. What Is a Docker Image Layer?

A Docker image is built from a sequence of filesystem changes.

For example:

FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

Conceptually:

Base image
   ↓
WORKDIR
   ↓
COPY requirements.txt
   ↓
RUN pip install
   ↓
COPY application
   ↓
Final image

The exact internal representation is more sophisticated than simply
treating every Dockerfile line as an independent layer, but the layered
model is extremely useful for understanding Docker builds.

3. Cache Mental Model

A useful simplified model is:

Instruction
    +
Relevant build inputs
    ↓
Cache key / result

If Docker determines that the relevant inputs match a previously built
result:

Previous result
      ↓
Cache hit
      ↓
Reuse

If the inputs no longer match:

Previous result
      ↓
Cache miss
      ↓
Execute instruction again

This is why Dockerfile structure has a direct impact on build speed.

4. Cache Hit vs Cache Miss

Cache hit

A cache hit means Docker can reuse an existing build result.

Conceptually:

Instruction
    ↓
Inputs unchanged
    ↓
Cache hit
    ↓
Reuse result

Cache miss

A cache miss means Docker cannot safely reuse the previous result.

Instruction
    ↓
Relevant input changed
    ↓
Cache miss
    ↓
Execute again

The goal is not to avoid every cache miss.

The goal is to avoid unnecessary cache invalidation.

5. Example: Poorly Structured Dockerfile

Consider:

FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

Suppose only:

app.py

changes.

The broad:

COPY . .

depends on many files in the build context.

That can cause the following work to become invalid:

COPY . .
    ↓
RUN pip install

even though:

requirements.txt

did not change.

This is a common cache-efficiency problem.

6. Better Cache Structure

A more cache-friendly structure is:

FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

Now the dependency installation is separated from application source.

The flow becomes:

requirements.txt
      ↓
COPY
      ↓
RUN pip install
      ↓
Cacheable dependency layer

Then:

Application source
      ↓
COPY
      ↓
Final application layer

If only application code changes:

Dependency inputs unchanged
      ↓
Reuse dependency cache
      ↓
Rebuild application layer

This is one of the most practical Docker optimization patterns.

7. Cache Invalidation

Cache invalidation occurs when Docker determines that a build step can
no longer reuse its previous result.

For example:

COPY requirements.txt .

If:

requirements.txt

changes, the result of that COPY instruction changes.

That can invalidate subsequent dependent work:

COPY requirements.txt
       ↓
RUN pip install
       ↓
COPY application

The important concept is:

A cache miss can affect subsequent dependent instructions.

Therefore, the position of instructions matters.

8. Why Instruction Order Matters

Consider:

COPY . .
RUN pip install -r requirements.txt

versus:

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

The second arrangement isolates the relatively stable dependency input.

This creates:

Stable inputs
    ↓
Expensive work
    ↓
Frequently changing inputs
    ↓
Cheap final work

A useful production principle is:

Put stable inputs before expensive operations and frequently
changing inputs later when practical.

9. RUN Cache

Consider:

RUN apt-get update && apt-get install -y curl

If the relevant inputs and build state allow the step to be reused,
Docker may use the cached result.

However, commands that depend on external package repositories should be
designed carefully.

For example:

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

The Dockerfile should still be designed for reproducibility and
security.

Caching does not guarantee that an external package repository remains
unchanged forever.

10. COPY Cache

COPY cache behaviour depends on the source content and relevant build
context inputs.

For example:

COPY requirements.txt .

is tied to:

requirements.txt

Whereas:

COPY . .

has a much broader set of inputs.

Conceptually:

COPY requirements.txt
      ↓
Small input set

COPY .
      ↓
Large input set

This is why .dockerignore and focused COPY instructions matter.

11. Build Context and Cache

Cache efficiency cannot be separated from the build context.

Consider:

Repository
    ↓
.dockerignore
    ↓
Build Context
    ↓
COPY
    ↓
Cache Inputs

If unnecessary files are present in the context, broad copy operations
can become sensitive to irrelevant changes.

For example:

README.md changes
      ↓
COPY . .
      ↓
Input changes
      ↓
Potential cache invalidation

A controlled context helps reduce unnecessary dependencies.

12. .dockerignore and Cache

.dockerignore does not directly create image layers.

Instead, it controls what enters the build context.

That affects what is available to instructions such as:

COPY . .

The relationship is:

.dockerignore
      ↓
Build context
      ↓
COPY inputs
      ↓
Cache behaviour

Therefore, .dockerignore is indirectly an important cache optimization
tool.

13. Cache Is Not Just About Image Size

A common misconception is:

"Better caching means a smaller image."

Not necessarily.

Caching primarily affects:

Build time
Build resource usage
CI/CD efficiency

Image size is influenced by:

Base image
Installed packages
Application files
Build artifacts
Number and contents of layers
Multi-stage design

So:

Cache optimization
    ≠
Image-size optimization

They can support each other, but they are different goals.

14. Cache and Multi-Stage Builds

Consider:

FROM node:22 AS builder

WORKDIR /app

COPY package*.json .

RUN npm ci

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

The build stage has its own build operations:

Dependencies
    ↓
Build
    ↓
Artifacts

The final stage contains only the runtime content.

Caching can allow expensive dependency installation and build operations
to be reused when their relevant inputs remain unchanged.

This makes multi-stage builds useful for both:

Image optimization
+
Build efficiency

15. Cache and ARG

Build arguments can affect build instructions.

For example:

ARG VERSION=1.0
RUN echo "Building $VERSION"

Changing the build argument can affect the relevant build step and
therefore its cache result.

Conceptually:

ARG
 ↓
Instruction input
 ↓
Cache decision

This is another reason to distinguish:

Build-time inputs
vs
Runtime configuration

16. Cache and ENV

Environment configuration can also influence subsequent build
instructions.

For example:

ENV APP_ENV=production

RUN echo "$APP_ENV"

Changing an environment setting used by subsequent build logic can
affect the build result.

The exact cache behaviour depends on how the instruction and its inputs
are represented by the builder.

The practical lesson is:

Changes to build configuration can invalidate dependent build
work.

17. Cache Mounts vs Image Layers

BuildKit introduced advanced cache mounts.

For example:

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

This is different from normal image-layer caching.

Image-layer cache

Build step
    ↓
Resulting image filesystem state
    ↓
Reusable build result

Cache mount

Build step
    ↓
Temporary / reusable build cache
    ↓
Not intended as final application data

A package manager's downloaded artifacts can be cached without becoming
part of the final runtime filesystem.

18. External Dependencies and Cache

Caching external dependencies can improve build speed, but introduces an
important consideration:

Cached dependency
    vs
Current dependency source

For example:

Package repository
      ↓
Download
      ↓
Cache

A later build may reuse cached data depending on the build
configuration.

Production builds should therefore consider:

Version pinning
+
Integrity verification
+
Trusted repositories
+
Controlled cache

Caching should not become an excuse for uncontrolled dependencies.

19. Cache and Reproducibility

Fast builds are useful, but reproducibility is also important.

A good build should aim for:

Same source
+
Same controlled inputs
      ↓
Predictable image

If a build depends on:

Latest package
Latest base image
Uncontrolled external download

cache behaviour alone does not solve reproducibility.

A mature build strategy combines:

Good cache structure
+
Pinned inputs
+
Controlled dependencies
+
Trusted base images

20. Cache Busting

Sometimes a build intentionally needs to invalidate cache.

A common pattern is to introduce an explicit build argument:

ARG CACHE_BUST=1

RUN echo "$CACHE_BUST"

Then:

docker build \
  --build-arg CACHE_BUST=2 \
  -t my-app .

changes the input to that step.

However, cache busting should be used deliberately.

Blindly invalidating large parts of a Dockerfile defeats the purpose of
caching.

A better approach is:

Identify stale input
      ↓
Invalidate only required work

21. --no-cache

Docker can also disable normal build cache reuse.

For example:

docker build --no-cache -t my-app .

This forces the build to execute without using the normal cached
results.

This can be useful when troubleshooting or intentionally rebuilding from
scratch.

But it is not normally the best default for every CI/CD build because it
can make builds significantly slower.

Mental model:

Normal build
   ↓
Reuse cache where valid

--no-cache
   ↓
Do not reuse normal cached build results

22. Cache and CI/CD

Caching becomes especially valuable in CI/CD because runners may be
ephemeral.

Without reusable cache:

New CI runner
      ↓
Download dependencies
      ↓
Build everything
      ↓
Push image

With reusable cache:

New CI runner
      ↓
Restore build cache
      ↓
Reuse unchanged work
      ↓
Build only what changed
      ↓
Push image

This can significantly reduce:

Pipeline duration
Network usage
CPU usage
Dependency download time

BuildKit's advanced cache import/export mechanisms are particularly
useful here.

23. Remote Cache

Modern Docker BuildKit workflows can store cache data externally.

Conceptually:

CI Runner A
    ↓
Build
    ↓
Export cache
    ↓
Remote cache

CI Runner B
    ↓
Import cache
    ↓
Reuse previous work

This is useful when:

Runners are temporary
+
Builds happen frequently
+
Images are large
+
Dependencies are expensive

The exact cache backend depends on the Docker/build environment.

24. Troubleshooting Cache Problems

When a Docker build unexpectedly rebuilds an expensive step:

Which step missed cache?
        ↓
What are its inputs?
        ↓
Did a previous instruction change?
        ↓
Did COPY include additional files?
        ↓
Did .dockerignore change?
        ↓
Did ARG / build configuration change?
        ↓
Is the cache available?
        ↓
Is the correct builder being used?

When a build is unexpectedly using stale results:

Is the cache valid?
        ↓
Are dependencies pinned?
        ↓
Is the expected input actually part of the cache key?
        ↓
Should this specific step be rebuilt?

The goal is to identify the exact invalidation point rather than simply
running:

docker build --no-cache

every time.

25. Production Relevance

Layer caching is one of the core techniques for making production image
pipelines efficient.

A mature Docker build generally tries to:

Keep stable inputs stable
        ↓
Cache expensive operations
        ↓
Place frequently changing inputs later
        ↓
Reuse results in CI/CD

For example:

COPY dependency-files .
RUN install-dependencies

COPY source-code .
RUN build-application

can provide a better cache boundary than:

COPY . .
RUN install-everything

The exact structure depends on the application.

26. IncidentLab Connection

IncidentLab's container builds can benefit directly from this approach.

The desired flow is:

Dependency definitions
        ↓
Install dependencies
        ↓
Cache expensive dependency work
        ↓
Application source
        ↓
Build / package application
        ↓
Runtime image

This connects the documentation sequence:

Build Context
      ↓
.dockerignore
      ↓
COPY vs ADD
      ↓
BuildKit
      ↓
Layer Caching
      ↓
Multi-stage / Production Optimization

The goal is not simply "make Docker faster."

It is:

Predictable inputs
+
Efficient caching
+
Reproducible builds
+
Small production images

27. Interview Takeaway

A strong interview explanation is:

"Docker caching allows previously completed build work to be reused
when the relevant inputs have not changed. I structure Dockerfiles so
stable inputs, such as dependency manifests, are copied before
expensive installation steps, while frequently changing application
source is copied later. This reduces unnecessary cache invalidation
and makes CI/CD builds faster. With BuildKit, I can also use cache
mounts and remote cache mechanisms for more advanced build
optimization."

The key mental model is:

Instruction
    +
Relevant inputs
    ↓
Cache result
    ↓
Reuse or rebuild

28. Key Takeaways

Docker builds can reuse previously completed work through caching.

Cache hits reuse valid previous results.

Cache misses cause affected work to execute again.

Changes can invalidate subsequent dependent build steps.

Instruction order has a major impact on cache efficiency.

Stable dependency files should often be separated from frequently
changing source.

.dockerignore helps control build-context inputs.

COPY . . can create broad cache dependencies.

Cache optimization and image-size optimization are different goals.

BuildKit provides advanced cache mechanisms such as cache mounts and
remote cache.

--no-cache is useful for specific troubleshooting or clean rebuild
scenarios.

Good caching should be combined with controlled and reproducible
build inputs.

29. Connections

Previous

20-buildkit.md

Next

22-dockerfile-best-practices.md

30. My Understanding

Docker layer caching is best understood as:

Build instruction
       +
Its relevant inputs
       ↓
Cached build result
       ↓
Reuse when valid

The most important practical lesson is that cache performance is
largely influenced by Dockerfile structure.

A good Dockerfile creates useful cache boundaries:

Stable inputs
    ↓
Expensive work
    ↓
Frequently changing inputs

BuildKit makes caching more powerful, but the fundamental principle
remains the same:

Design the build so that changes invalidate only the work that
actually needs to be rebuilt.

31. Questions for Further Exploration

How does Docker determine the cache key for each instruction?

Why does changing one instruction invalidate later dependent
instructions?

How do BuildKit cache mounts differ from normal layer cache?

How does registry-backed remote cache work in GitHub Actions?

How should cache strategy change for monorepos?

How can cache behaviour be debugged without blindly using
--no-cache?
