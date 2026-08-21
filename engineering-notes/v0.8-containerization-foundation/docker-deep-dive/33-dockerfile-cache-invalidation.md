Dockerfile Cache Invalidation

1. Why Cache Matters

Docker image builds are made of ordered build steps.

A simplified build looks like:

Dockerfile
    ↓
Step 1
    ↓
Step 2
    ↓
Step 3
    ↓
Final image

When Docker can reuse the result of a previous step, the build becomes
faster.

Conceptually:

Previous build
    ↓
Cached layer / result
    ↓
Reuse
    ↓
Faster build

But cache reuse is only safe when Docker determines that the relevant
inputs have not changed.

This is where cache invalidation becomes important.

2. The Core Mental Model

The simplest way to think about Docker build caching is:

Build step
   +
Inputs to that step
   ↓
Cache decision

If the relevant inputs still match:

Cache hit
   ↓
Reuse previous result

If they no longer match:

Cache miss
   ↓
Execute the step again

The important lesson is:

Docker does not simply ask, "Have I run this command before?" It
needs to determine whether the result can still be reused for the
current build inputs.

3. Dockerfile Instructions Are Ordered

Consider:

FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

The build has a logical sequence:

FROM
  ↓
WORKDIR
  ↓
COPY requirements.txt
  ↓
RUN pip install
  ↓
COPY source
  ↓
CMD

Changes in an earlier relevant step can affect later steps.

This is why Dockerfile instruction ordering has a direct relationship
with cache efficiency.

4. Cache Hit

Suppose the Dockerfile and relevant inputs have not changed:

Dockerfile
   ↓
Same build inputs
   ↓
Existing cache
   ↓
Cache hit

Docker can reuse the previously computed result instead of executing the
instruction again.

For example:

RUN pip install -r requirements.txt

can potentially be reused when:

requirements.txt

has not changed and the preceding build state remains compatible.

5. Cache Miss

A cache miss means Docker cannot safely reuse the previous result.

Conceptually:

Current build inputs
        ≠
Cached build inputs
        ↓
Cache miss
        ↓
Execute instruction again

For example:

requirements.txt

changes:

COPY requirements.txt .
        ↓
Different input
        ↓
Cache invalidated for this step
        ↓
RUN pip install again

6. The Important Cascade

One of the most important cache concepts is that invalidation can affect
subsequent instructions.

Consider:

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

If:

requirements.txt

changes:

COPY requirements.txt .
        ↓
Cache miss
        ↓
RUN pip install
        ↓
Must be evaluated again
        ↓
COPY .
        ↓
Later build state also changes

The exact implementation details depend on the builder, but the
operational mental model is:

Once an earlier build step can no longer reuse its cached result,
later dependent steps generally cannot simply continue using the old
chain.

7. Why Instruction Order Matters

Compare these two Dockerfiles.

Less cache-friendly

COPY . .

RUN pip install -r requirements.txt

A source-code change can change the input to:

COPY . .

which can force later steps to be rebuilt.

More cache-friendly

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

Now:

Source code changes
       ↓
COPY requirements.txt
       ↓
Still unchanged
       ↓
pip install can potentially remain cached
       ↓
COPY . changes

This is one of the most practical Docker caching patterns.

8. Dependencies vs Application Source

A common optimization is to separate relatively stable dependency inputs
from frequently changing source code.

For example:

COPY package*.json .

RUN npm ci

COPY . .

The mental model is:

Dependency files
      ↓
Install dependencies
      ↓
Application source

If only application code changes:

Dependency files unchanged
      ↓
Dependency installation can potentially use cache
      ↓
Source copied again

This can significantly reduce build time.

9. Cache Invalidation Is Not the Same as "Everything Rebuilds"

When one instruction misses the cache, do not think:

One change
   ↓
Everything starts from zero

A better mental model is:

Earlier cached steps
       ↓
Reuse where valid

First invalidated step
       ↓
Execute

Subsequent dependent steps
       ↓
Rebuild / reevaluate

The exact cache behaviour depends on the build engine and instruction.

The important point is to identify the first step that stopped
matching the cache.

10. COPY and Cache Invalidation

COPY is one of the most important instructions for understanding cache
invalidation.

For example:

COPY package.json .

and:

COPY . .

have very different cache implications.

A broad:

COPY . .

can be affected by many files in the build context.

A narrow:

COPY package.json .

has a much smaller input set.

Therefore:

Smaller relevant input set
        ↓
More predictable cache reuse

11. Build Context Matters

When you run:

docker build .

the final . represents the build context.

Files in the context can become inputs to COPY and ADD instructions.

If unnecessary files are included:

Large build context
       ↓
More files available to build
       ↓
More opportunities for irrelevant changes

This is one reason .dockerignore matters.

12. .dockerignore and Cache Efficiency

A .dockerignore file can exclude files from the build context.

For example:

.git
node_modules
__pycache__
.env
*.log

Conceptually:

Project directory
      ↓
.dockerignore
      ↓
Build context
      ↓
Docker build

This helps:

Reduce build context
Reduce unnecessary file transfer
Reduce irrelevant inputs
Improve build efficiency

It can also reduce accidental inclusion of sensitive or unnecessary
files.

13. Broad COPY Can Hurt Caching

Suppose:

COPY . .
RUN npm ci

and the repository contains:

src/
package.json
package-lock.json
README.md
docs/
tests/

Changing:

README.md

can change the input to the broad COPY.

That can cause:

COPY . .
    ↓
Cache miss
    ↓
RUN npm ci
    ↓
Re-execution

even though the dependency files did not change.

A better arrangement is:

COPY package*.json .
RUN npm ci
COPY . .

Now documentation changes do not necessarily invalidate the dependency
installation step.

14. RUN and Cache

Consider:

RUN apt-get update && apt-get install -y curl

If the builder determines that the instruction and its relevant prior
state match the cached build state, it may reuse the cached result.

Changing the instruction:

RUN apt-get update && apt-get install -y curl git

changes the build step.

Therefore:

Changed RUN instruction
        ↓
Cache miss
        ↓
Instruction executes again

15. Why "Same Command" Is Not Enough

A common misconception is:

Same RUN command
    ↓
Always cached

Not necessarily.

Cacheability depends on the build instruction and the state/input it
depends on.

For example:

COPY requirements.txt .
RUN pip install -r requirements.txt

Even though:

RUN pip install -r requirements.txt

did not change textually, changing:

requirements.txt

changes the relevant build input.

Therefore the cached result may no longer be valid.

16. ADD and Cache

ADD can also participate in cache invalidation because it introduces
content into the build.

For example:

ADD app.tar.gz /app/

Changing the source content can change the build input.

Because ADD has additional behaviour compared with COPY, it should
be used intentionally.

For normal local file copying:

COPY

is often the clearer choice.

17. RUN After COPY

A useful pattern is:

COPY dependency-files .
RUN install-dependencies
COPY source .
RUN build-application

The dependency step is separated from source changes.

Conceptually:

Stable inputs
    ↓
Expensive dependency installation
    ↓
Frequently changing inputs
    ↓
Application build

This is a general cache-optimization principle:

Put stable inputs before expensive operations and frequently
changing inputs later when practical.

18. Cache Invalidation and Package Managers

Package installation is often expensive.

Examples:

pip install
npm ci
mvn dependency:resolve
go mod download
apt-get install

If these steps are unnecessarily invalidated:

Source change
    ↓
Dependency installation again
    ↓
Longer build

A better structure is:

Dependency manifest
    ↓
Install dependencies
    ↓
Source code

This keeps dependency caching independent from most application source
changes.

19. Cache Invalidation and Base Images

The base image is also part of the build chain.

For example:

FROM python:3.12

If the effective base image changes:

FROM
   ↓
Different base state
   ↓
Downstream build state affected

This can cause subsequent build steps to need reevaluation.

Therefore, the base image is an important part of reproducibility and
cache behaviour.

20. Mutable Tags and Cache Reasoning

Consider:

FROM python:3.12

A tag is a human-friendly reference.

The underlying image content can change as the tag is updated.

This means:

Tag
 ↓
Current referenced image

and:

Digest
 ↓
Specific content identity

are different concepts.

For production reproducibility, pinning a base image by digest can
provide stronger content identity.

21. --no-cache

Docker can be instructed not to use existing build cache:

docker build --no-cache .

Conceptually:

Existing cache
      ↓
Ignored
      ↓
Build steps execute again

This can be useful for troubleshooting or intentionally forcing a fresh
build.

But:

--no-cache is not a normal fix for poor Dockerfile cache design.

If every build requires --no-cache, the underlying build structure
should be investigated.

22. --pull vs --no-cache

These options solve different problems.

--no-cache

Do not reuse existing build cache

--pull

Attempt to pull a newer version of the referenced base image

Conceptually:

--no-cache
   ↓
Cache behaviour

--pull
   ↓
Base image freshness

They are not interchangeable.

A build can use:

docker build --pull .

without disabling all cache reuse.

23. Cache Mounts vs Layer Cache

Modern BuildKit supports cache mounts for certain build-time caches.

For example, package-manager caches can be mounted during a RUN step.

Conceptually:

Build layer cache
       +
Package-manager cache
       ↓
Faster rebuilds

These are different concepts.

Layer cache

Reuse result of a build step

Cache mount

Reuse files produced by a tool during builds

A cache mount can remain useful even when the RUN instruction itself
needs to execute again.

24. Example: pip Cache

Conceptually:

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

The RUN step may still execute, but the package manager can reuse
downloaded package artifacts from the cache mount.

So:

Layer cache
   ↓
Skip whole RUN step

Cache mount
   ↓
RUN executes, but tool reuses cached data

This distinction is important for advanced BuildKit optimization.

25. Cache Invalidation and Secrets

Secrets should not be copied into images merely to make a build work.

Avoid patterns like:

COPY .env .
RUN ...

because:

Secret
   ↓
Build context
   ↓
Image/build history risk

BuildKit provides dedicated secret mechanisms for build-time secrets.

The broader lesson is:

Do not solve cache or build problems by putting credentials into
normal build inputs.

26. Cache Invalidation and Git Metadata

A repository often contains files that do not affect the application
build:

.git/
README.md
docs/
local files
logs

If these are unnecessarily included in broad build-context operations:

Unrelated file changes
        ↓
Broader COPY input changes
        ↓
Cache miss

Using:

.dockerignore
+
Specific COPY instructions

helps make cache behaviour more predictable.

27. Debugging Cache Behaviour

When a build is unexpectedly slow:

1. Identify the first cache miss
        ↓
2. Identify the instruction
        ↓
3. Identify its inputs
        ↓
4. Ask what changed
        ↓
5. Check whether the instruction is too broad
        ↓
6. Check Dockerfile ordering
        ↓
7. Check build context / .dockerignore
        ↓
8. Check base image changes
        ↓
9. Check whether BuildKit cache mounts would help

Do not start by randomly adding:

--no-cache

The goal is to understand why the cache missed.

28. Reading Build Output

A Docker build output can show whether steps are being reused.

Conceptually:

CACHED

indicates reuse of a cached build result.

Whereas:

RUN ...

or an executed build step indicates that the step is being performed.

The exact output format varies with BuildKit and Docker versions.

The important troubleshooting question is:

Which is the first step that stopped being cached?

29. Example: Poor Dockerfile

Consider:

FROM node:22

WORKDIR /app

COPY . .

RUN npm ci

RUN npm run build

Now change:

README.md

Potential consequence:

COPY . .
    ↓
Input changed
    ↓
Cache miss
    ↓
npm ci
    ↓
Runs again
    ↓
npm run build
    ↓
Runs again

The source change had nothing to do with dependencies, but the broad
COPY made it part of the cache input for the dependency installation
step.

30. Example: Better Dockerfile

A more cache-friendly structure is:

FROM node:22

WORKDIR /app

COPY package*.json .

RUN npm ci

COPY . .

RUN npm run build

Now:

README.md changes
       ↓
COPY package*.json
       ↓
Still cached
       ↓
npm ci
       ↓
Still cached
       ↓
COPY . .
       ↓
Re-executes
       ↓
npm run build

This is better because the expensive dependency installation is
protected from unrelated source/documentation changes.

31. Example: Python

Less cache-friendly:

COPY . .

RUN pip install -r requirements.txt

More cache-friendly:

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

Mental model:

requirements.txt changes
      ↓
Dependencies rebuild

source.py changes
      ↓
Dependencies stay cached

This is one of the most reusable Dockerfile optimization patterns.

32. Cache Invalidation and Multi-Stage Builds

Multi-stage builds also have cache implications.

For example:

FROM node:22 AS builder

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

A source-code change may invalidate:

COPY . .

and:

RUN npm run build

while the dependency installation can remain cached if its inputs did
not change.

This is another reason to structure stages and instructions
intentionally.

33. Cache Is a Performance Optimization

Cache should improve:

Build speed
Developer feedback
CI/CD throughput
Resource consumption

But correctness comes first.

A build should never rely on stale output being reused when the relevant
inputs changed.

The correct priority is:

Correctness
    ↓
Reproducibility
    ↓
Cache efficiency
    ↓
Build speed

34. Cache Is Not a Deployment Artifact

A build cache is an optimization mechanism.

Do not treat:

Build cache

as the application's final artifact.

The actual image should be:

Versioned
Traceable
Reproducible
Scannable
Deployable

Cache simply helps produce it efficiently.

35. CI/CD Cache Considerations

In CI/CD:

Developer
   ↓
Git push
   ↓
CI runner
   ↓
Docker build

the runner may not have the same cache as a developer laptop.

Therefore:

Local build
   ≠
CI build cache

CI pipelines often configure remote or registry-backed cache mechanisms
to improve reuse.

The exact approach depends on the CI platform and builder.

36. Registry Cache

BuildKit can use external cache storage, including registry-backed cache
configurations.

Conceptually:

CI Runner A
    ↓
Build cache
    ↓
Registry / external cache

CI Runner B
    ↓
Reuse compatible cache

This is especially useful when CI runners are ephemeral.

The important production idea is:

Ephemeral build agents need an external strategy if you want cache
reuse across separate runners.

37. IncidentLab Connection

For IncidentLab CI/CD troubleshooting, a slow Docker build should be
investigated systematically.

Example:

CI build suddenly slower
        ↓
Find first cache miss
        ↓
Identify Dockerfile instruction
        ↓
Check changed files
        ↓
Check build context
        ↓
Check .dockerignore
        ↓
Check dependency layer ordering
        ↓
Check base image
        ↓
Check CI cache availability
        ↓
Root cause

Possible root causes include:

Dockerfile change
Broad COPY
Dependency manifest change
Base image change
Missing CI cache
Cache configuration change

38. Interview Takeaway

A strong interview explanation is:

"Docker build caching reuses the result of build steps when the
relevant instruction and build inputs still match. Cache invalidation
happens when those inputs change or when a previous build state can no
longer be reused. Because later steps depend on the state produced by
earlier steps, an early cache miss can cause subsequent steps to
execute again. That is why I separate stable dependency files from
frequently changing source code, use .dockerignore, and place
expensive operations after stable inputs."

The simplest mental model is:

Instruction
    +
Relevant inputs
    ↓
Cache decision
    ↓
Hit → reuse
Miss → execute

39. Key Takeaways

Docker build cache exists primarily to avoid unnecessary repeated
work.

Cache decisions depend on build instructions and their relevant
inputs.

A cache hit reuses a previous build result.

A cache miss causes the affected instruction to execute again.

An early invalidation can affect subsequent dependent build steps.

Dockerfile instruction ordering strongly affects cache efficiency.

Separate stable dependency files from frequently changing source
code.

Avoid unnecessarily broad COPY . . before expensive dependency
installation.

.dockerignore reduces unnecessary build-context inputs.

Changing dependency manifests should invalidate dependency
installation when appropriate.

Base image changes can affect downstream build state.

--no-cache disables reuse of existing build cache; it is not a
substitute for good Dockerfile design.

--pull addresses base-image freshness and is different from
--no-cache.

BuildKit cache mounts are different from normal layer caching.

Cache mounts can speed up a RUN step even when the step itself
executes.

Build caches should not be treated as final application artifacts.

CI runners may require external/registry-backed caching for reuse
across ephemeral environments.

When debugging a slow build, identify the first unexpected cache
miss.

Correctness and reproducibility come before cache optimization.

40. Connections

Previous

32-expose-vs-publish.md

Next

34-buildkit-and-buildx.md

41. My Understanding

Docker cache is best understood as:

Build instruction
      +
Relevant input state
      ↓
Can previous result be reused?
      ↓
       ┌───────────┐
       │           │
      YES          NO
       ↓           ↓
    Cache hit   Cache miss
       ↓           ↓
     Reuse      Execute

The practical Dockerfile pattern is:

Stable dependency files
        ↓
Expensive dependency installation
        ↓
Frequently changing source
        ↓
Application build

For example:

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

So when:

app.py changes

we want:

pip install
   ↓
Cached

while:

COPY .
   ↓
Re-executes

The key lesson is:

Good Dockerfile design is not only about producing the correct
image; it is also about controlling which changes invalidate expensive
build steps.
