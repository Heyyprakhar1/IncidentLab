.dockerignore

1. What Is .dockerignore?

.dockerignore is a file used to exclude files and directories from the
Docker build context.

For example:

.git
.env
node_modules
__pycache__
logs

When running:

docker build -t my-app .

Docker uses the current directory as the build context, but
.dockerignore tells Docker which content should be excluded from that
context.

The basic flow is:

Project Directory
       ↓
.dockerignore
       ↓
Filtered Build Context
       ↓
Docker Build
       ↓
Image

2. Why Does .dockerignore Exist?

A project directory often contains files that the Docker image does not
need.

For example:

project/
├── app.py
├── requirements.txt
├── .git/
├── .env
├── node_modules/
├── __pycache__/
├── logs/
└── tests/

A container image may only need:

app.py
requirements.txt

.dockerignore helps prevent unnecessary files from becoming
build-context input.

The principle is:

Send only the build inputs that the image actually needs.

3. Basic Syntax

A .dockerignore file contains patterns describing files or directories
to exclude.

For example:

.git
.env
__pycache__
*.pyc
logs/

Each matching path is excluded from the build context.

A common production-oriented example is:

.git
.gitignore
.env
*.log
__pycache__/
*.pyc
node_modules/

The exact entries depend on the project.

4. .dockerignore vs .gitignore

These files solve different problems.

.gitignore

Controls what Git should generally ignore.

Project
   ↓
.gitignore
   ↓
Git tracking behaviour

.dockerignore

Controls what Docker should exclude from the build context.

Project
   ↓
.dockerignore
   ↓
Docker build context

A file ignored by Git is not automatically ignored by Docker.

Likewise, a file ignored by Docker does not automatically disappear from
Git.

Mental model:

.gitignore
    ↓
Git

.dockerignore
    ↓
Docker build

5. .dockerignore and Build Context

.dockerignore is directly connected to the build-context concept.

Without it:

Project
   ↓
Large build context
   ↓
Docker build

With it:

Project
   ↓
.dockerignore
   ↓
Relevant build context
   ↓
Docker build

This can reduce unnecessary build input.

The distinction remains important:

.dockerignore
    ↓
Controls build context

Dockerfile
    ↓
Controls what gets copied into the image

They work together but solve different problems.

6. Why Excluding .git Matters

A repository may contain:

.git/

with potentially large amounts of history and metadata.

There is usually no reason for a production application image to contain
the Git repository.

A common entry is:

.git

This helps keep source-control metadata out of the Docker build context
and prevents accidental copying through a broad instruction such as:

COPY . .

7. Why Excluding .env Matters

A local project may contain:

.env

with environment-specific configuration or secrets.

A common .dockerignore entry is:

.env

This reduces the risk of accidentally making those files available to
the build context.

However:

.dockerignore is not a complete secret-management solution.

Secrets should still be handled through appropriate secret-management
mechanisms.

The principle is:

Secrets
   ↓
Do not place them in the image
   ↓
Use appropriate runtime / build secret mechanisms

8. Excluding Dependencies That Are Reinstalled

For projects where dependencies are installed inside the image, local
dependency directories may not need to be included.

For example:

node_modules/

may be excluded when the Dockerfile performs:

COPY package*.json .
RUN npm ci

The flow becomes:

package.json
      ↓
Docker build
      ↓
Install dependencies
      ↓
Image dependencies

rather than:

Host node_modules
      ↓
Huge build context
      ↓
COPY into image

The correct choice depends on the application's build process.

9. Python Example

A Python project may contain:

project/
├── app.py
├── requirements.txt
├── __pycache__/
├── *.pyc
├── .venv/
├── .git/
└── .env

A reasonable .dockerignore might include:

.git
.env
.venv
__pycache__
*.pyc

Then:

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

can copy the relevant application source without bringing local Python
environment artifacts into the build context.

10. Node.js Example

A Node.js project commonly contains:

node_modules/
npm-debug.log
.git/
.env

A .dockerignore might include:

node_modules
npm-debug.log
.git
.env

If dependencies are installed during the image build:

COPY package*.json .

RUN npm ci

COPY . .

the container receives a clean dependency installation appropriate to
the image rather than relying on the developer's local node_modules.

11. Excluding Logs and Temporary Files

Local development environments may generate:

logs/
*.log
tmp/
.cache/

These files generally should not be part of an application image.

For example:

logs/
*.log
tmp/

can be excluded.

This keeps the build input focused and avoids accidentally baking
environment-specific runtime artifacts into the image.

12. .dockerignore and COPY . .

This is one of the most important relationships to understand.

Consider:

COPY . .

The . refers to the available build context.

It does not mean:

"Copy absolutely everything on my computer."

It means approximately:

Copy the relevant contents of the build context
that are not excluded by .dockerignore.

The flow is:

Project
   ↓
.dockerignore
   ↓
Build Context
   ↓
COPY . .
   ↓
Image

Therefore, a broad COPY . . instruction makes a well-designed
.dockerignore particularly important.

13. .dockerignore and Build Cache

.dockerignore also connects directly with Docker build caching.

A broad build context can introduce unnecessary inputs into broad copy
operations.

For example:

COPY . .

may depend on many application files.

If irrelevant files are present in the build context, changes to those
files can contribute to unnecessary cache invalidation for affected
build steps.

A controlled context helps keep build inputs focused:

Relevant files
      ↓
.dockerignore
      ↓
COPY
      ↓
More focused cache dependency

This connects:

.dockerignore
+
COPY
+
Build Context
+
Build Cache

into one optimization strategy.

14. .dockerignore and Image Size

A common misconception is:

"If .dockerignore makes the build context smaller, the image
automatically becomes smaller."

Not necessarily.

For example:

.dockerignore
    ↓
Controls build context

while:

COPY
    ↓
Controls files copied into the image

If a file is excluded from the build context, it cannot normally be
copied into the image through ordinary context-based COPY or ADD.

So .dockerignore can indirectly reduce image contents by preventing
unnecessary files from being available to copy.

But image size also depends on:

base image

installed packages

layers

build artifacts

multi-stage design

The two concepts should not be treated as identical.

15. Negation Patterns

.dockerignore supports pattern-based exclusion and can use negation
patterns in appropriate cases.

For example:

*.log
!important.log

Conceptually:

*.log
    ↓
Ignore log files

!important.log
    ↓
Exception for this file

This can be useful when most files matching a pattern should be excluded
but one specific file is intentionally required.

However, complex ignore rules should be kept understandable.

The goal is a predictable build context, not a puzzle.

16. Directory Patterns

Directories can be excluded explicitly.

For example:

node_modules/
__pycache__/
logs/

This is useful for common generated or environment-specific directories.

The exact pattern behaviour depends on Docker's .dockerignore matching
rules, so production teams should test important ignore patterns rather
than assuming Git and Docker interpret every pattern identically.

17. What .dockerignore Does Not Do

.dockerignore does not:

delete files from your local project

delete files from Git

remove files already present in an existing image

replace Dockerfile design

replace secret management

replace dependency management

automatically make an image secure

It controls the build context.

The mental model is:

Local project
    ↓
.dockerignore
    ↓
Docker build input

It does not modify the source project itself.

18. Common Mistakes

Copying .gitignore into .dockerignore blindly

The two files have different purposes.

Some entries may overlap, but Docker-specific build requirements should
determine .dockerignore.

Forgetting secrets

A project may contain:

.env
credentials.json
local keys

These should be carefully excluded from the build context and, more
importantly, should not be baked into images.

Ignoring the wrong files

If the Dockerfile genuinely needs a file and .dockerignore excludes
it:

.dockerignore
    ↓
File excluded
    ↓
COPY fails

This is a common build failure.

Assuming ignored files are deleted

They are not.

The files remain in the project directory.

They are simply excluded from the Docker build context.

Using an excessively broad ignore file

Overly aggressive patterns can exclude files that the build actually
requires.

A good .dockerignore is:

Focused
+
Understandable
+
Tested

19. Troubleshooting Mental Model

If a Docker build says:

COPY failed

and the source file definitely exists locally:

Does the file exist?
      ↓
Is it inside the build context?
      ↓
Is it excluded by .dockerignore?
      ↓
Is the pattern matching unexpectedly?
      ↓
Is the Dockerfile using the expected context?

If the build context is unexpectedly large:

Build context large
      ↓
Check .dockerignore
      ↓
.git?
node_modules?
logs?
build artifacts?
local environments?
large files?
      ↓
Reduce unnecessary inputs

If a file unexpectedly appears in the image:

Why is file present?
      ↓
Was it in build context?
      ↓
Was it excluded?
      ↓
Does COPY / ADD include it?
      ↓
Was it introduced by a dependency/build step?

20. Production Relevance

A production .dockerignore should be treated as part of the Docker
build design.

A good setup generally excludes:

Source-control metadata
Local environments
Secrets
Generated artifacts
Dependency directories that are rebuilt
Logs
Caches
Temporary files

while retaining:

Application source
Dependency definitions
Required build files
Required configuration templates

The exact list should be project-specific.

The objective is:

Minimal required build context
        +
Predictable Dockerfile inputs
        ↓
Efficient and safer build

21. CI/CD Relevance

.dockerignore becomes particularly valuable in CI/CD.

A typical pipeline may look like:

Git checkout
    ↓
Docker build
    ↓
Build context
    ↓
BuildKit
    ↓
Image
    ↓
Registry

If the repository contains large or irrelevant files, they can increase
build overhead.

A well-designed .dockerignore helps keep the build input controlled.

This is particularly useful with:

GitHub Actions

ephemeral runners

remote builders

multi-stage builds

remote cache

22. IncidentLab Connection

IncidentLab contains source code, infrastructure files, engineering
documentation, CI/CD configuration, and other repository content.

The Docker build should not automatically treat the entire repository as
application input.

A project-specific .dockerignore helps establish:

IncidentLab repository
       ↓
Exclude irrelevant repository content
       ↓
Application build context
       ↓
Dockerfile
       ↓
Image

This supports the same engineering principles already covered:

Build Context
      ↓
.dockerignore
      ↓
COPY
      ↓
Cache efficiency
      ↓
Production image

It also becomes important when the project's Docker builds are executed
through GitHub Actions.

23. Interview Takeaway

A strong interview explanation is:

".dockerignore controls which files are excluded from the Docker
build context. I use it to keep unnecessary files, source-control
metadata, local environments, secrets, logs, and generated artifacts
out of the build input. This reduces build overhead and helps keep
broad COPY operations and cache dependencies focused. It is
different from .gitignore, because it controls Docker rather than
Git."

The key mental model is:

Project
   ↓
.dockerignore
   ↓
Filtered Build Context
   ↓
Dockerfile
   ↓
Image

24. Key Takeaways

.dockerignore filters files from the Docker build context.

It is different from .gitignore.

It does not delete local files.

It does not automatically remove files from existing images.

It is especially important when using COPY . ..

It can reduce unnecessary build-context overhead.

It can help reduce accidental inclusion of sensitive or irrelevant
files.

It connects directly with Docker build caching.

Overly aggressive patterns can break builds by excluding required
files.

The correct .dockerignore is project-specific.

.dockerignore is part of Docker build design, not merely cleanup.

25. Connections

Previous

17-build-context.md

Next

19-image-inspection.md

26. My Understanding

.dockerignore controls what Docker receives as build-context input.

The simplest mental model is:

Project
   ↓
.dockerignore
   ↓
Only relevant build inputs
   ↓
Docker build
   ↓
Image

The most important distinction is:

.dockerignore
    ↓
Controls build context

Dockerfile
    ↓
Controls image construction

Used together, they make Docker builds more focused, predictable,
efficient, and less likely to accidentally include irrelevant or
sensitive project content.

27. Questions for Further Exploration

How exactly are .dockerignore patterns evaluated?

How does .dockerignore differ from .gitignore in edge cases?

How can a .dockerignore file be tested safely in CI?

How does .dockerignore interact with BuildKit named contexts?

What files should be excluded from an IncidentLab production Docker
build?
