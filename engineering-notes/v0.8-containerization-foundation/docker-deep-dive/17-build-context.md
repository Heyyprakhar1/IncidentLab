Docker Build Context

1. What Is the Build Context?

The Docker build context is the set of files and directories made
available to the Docker build process.

For example:

docker build -t my-app .

The final:

.

specifies the build context.

Conceptually:

Project Directory
       ↓
Build Context
       ↓
Docker Build
       ↓
Dockerfile instructions
       ↓
Image

The build context is important because instructions such as:

COPY
ADD

normally work with files available inside that context.

2. Why Does the Build Context Exist?

Docker needs a defined set of files that the build is allowed to access.

Consider:

project/
├── Dockerfile
├── app.py
├── requirements.txt
├── src/
└── README.md

Running:

docker build -t my-app .

makes the project directory available as the build context.

Docker can then use files from that context:

COPY app.py /app/
COPY requirements.txt /app/

The build context therefore acts as an input boundary for the image
build.

3. Build Context vs Dockerfile

These are related but different concepts.

The Dockerfile contains the instructions:

FROM
COPY
RUN
CMD
...

The build context contains the files those instructions can use.

For example:

Dockerfile
    ↓
Instructions

Build Context
    ↓
Files available to those instructions

A Dockerfile can therefore be located separately from the directory used
as the build context.

For example:

docker build -f docker/Dockerfile .

Here:

-f docker/Dockerfile
       ↓
Dockerfile location

.
       ↓
Build context

This distinction becomes important in repositories with multiple
Dockerfiles or more complex project structures.

4. Basic Build Context Example

Consider:

project/
├── Dockerfile
├── app.py
├── requirements.txt
└── tests/
    └── test_app.py

Command:

docker build -t my-app .

The context is:

project/

A Dockerfile can use:

COPY app.py /app/
COPY requirements.txt /app/

The build context contains all of:

app.py
requirements.txt
tests/
Dockerfile

unless files are excluded through .dockerignore.

The important point is:

The build context is not automatically limited to the files you
eventually copy into the image.

5. Build Context and .dockerignore

A project may contain many files that the image does not need.

For example:

.git/
node_modules/
__pycache__/
logs/
.env
tests/

Sending all of these unnecessarily into the build context can increase
build overhead.

A .dockerignore file can exclude them:

.git
node_modules
__pycache__
logs
.env

The flow becomes:

Project Directory
       ↓
.dockerignore
       ↓
Filtered Build Context
       ↓
Docker Build

This is why build context and .dockerignore should be considered
together.

6. Why a Large Build Context Is a Problem

A large build context can increase the amount of data Docker needs to
process or transfer as part of the build.

For example:

Project
├── source code
├── dependencies
├── .git
├── large logs
├── local artifacts
└── node_modules

If everything is included unnecessarily:

Large Project
      ↓
Large Build Context
      ↓
More build overhead

A controlled context is generally better:

Project
      ↓
.dockerignore
      ↓
Relevant Build Context
      ↓
Build

This becomes especially important in CI/CD environments where build
context may be transferred to a remote or isolated builder.

7. Build Context Is Not the Final Image

This distinction is important.

Suppose the context contains:

app.py
tests/
README.md
.git/

That does not mean all of those files automatically become part of
the image.

The Dockerfile determines what gets added to the image.

For example:

COPY app.py /app/

only copies the relevant file.

Conceptually:

Build Context
├── app.py
├── tests/
├── README.md
└── .git/

        ↓ Dockerfile

Image
└── /app
    └── app.py

Therefore:

Build Context
    ≠
Image Contents

8. COPY Depends on the Build Context

A common example is:

COPY requirements.txt .

Docker looks for:

requirements.txt

within the available build context.

If the file is not available there, the build cannot copy it.

For example:

context/
└── src/
    └── app.py

while the Dockerfile contains:

COPY requirements.txt .

will fail if:

requirements.txt

is outside the context.

This is a common source of Docker build errors.

9. Context Boundary

The build context creates an important boundary.

Suppose the directory structure is:

workspace/
├── project/
│   ├── Dockerfile
│   └── app.py
└── secret.txt

If the build is:

cd workspace/project
docker build -t my-app .

the context is:

workspace/project/

The Dockerfile cannot simply do:

COPY ../secret.txt /app/

to escape that context.

If a file is required, the build context must be designed so that the
required input is available to the build.

This is an important security and reproducibility boundary.

10. Choosing the Context Directory

The build context should be chosen deliberately.

For a simple project:

docker build -t my-app .

may be appropriate.

For a repository with several components:

repo/
├── backend/
├── frontend/
├── infrastructure/
└── docs/

you may not want the entire repository to become the context for every
image.

A backend image might use:

docker build -t backend ./backend

while a frontend image uses:

docker build -t frontend ./frontend

This keeps each build focused on the files it actually needs.

11. Dockerfile Location and Context Can Be Different

The Dockerfile does not have to be located at the root of the build
context.

For example:

repo/
├── docker/
│   └── Dockerfile
└── app/
    ├── app.py
    └── requirements.txt

A command can specify:

docker build \
  -f docker/Dockerfile \
  -t my-app \
  .

Here:

Dockerfile
    ↓
docker/Dockerfile

Context
    ↓
repo/

The Dockerfile and build context therefore have separate roles.

12. Build Context and Monorepos

In a monorepo, the context decision becomes more important.

Consider:

repo/
├── services/
│   ├── api/
│   ├── worker/
│   └── frontend/
├── shared/
├── docs/
└── infrastructure/

If the entire repository is used as the context:

docker build -t api .

the API build may have access to many unrelated files.

A more focused context can reduce unnecessary build input.

However, if the API genuinely needs files from:

shared/

then the context must include them.

The engineering decision is:

Small context
      +
Required dependencies available
      ↓
Useful build boundary

13. Build Context and CI/CD

Build context becomes particularly relevant in CI/CD.

A pipeline may:

Checkout repository
       ↓
Prepare build context
       ↓
Docker build
       ↓
Build image
       ↓
Push image

If the repository contains large or irrelevant files, they can
unnecessarily increase build work.

A well-designed .dockerignore and focused build context can help keep
CI builds efficient.

This is especially important when builds use:

remote builders

ephemeral runners

BuildKit

remote cache

multiple images from one repository

14. Build Context and BuildKit

Modern Docker builds commonly use BuildKit.

BuildKit provides more advanced build behaviour, but the concept of
build context still matters.

The general relationship remains:

Build Context
      ↓
Build Inputs
      ↓
BuildKit
      ↓
Build Instructions
      ↓
Image

BuildKit can also support more advanced build contexts and sources, but
the fundamental engineering principle remains:

A build should receive only the inputs it actually needs.

15. Multiple Build Contexts

Modern BuildKit-based workflows can support additional named build
contexts.

For example, a build can be supplied with another context and referenced
from the Dockerfile.

Conceptually:

Main Context
      +
Additional Context
      ↓
BuildKit
      ↓
Dockerfile

This can be useful for more advanced repository layouts.

However, this should not be confused with simply making the entire
repository the build context.

Additional contexts should still be intentional and controlled.

16. Build Context and Cache Behaviour

Build context and cache efficiency are closely connected.

Consider:

COPY . .

A broad copy instruction depends on a broad set of context files.

If an irrelevant file changes and that change affects the inputs
considered by the instruction, the cache for that step may become
invalid.

For example:

COPY . .
    ↓
Many context files
    ↓
Broad cache dependency

Whereas:

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

can separate stable and frequently changing inputs.

This connects:

Build Context
      +
COPY structure
      +
Cache strategy

into one optimization problem.

17. Common Mistakes

Using the entire repository as context by default

For example:

docker build -t my-app .

from a large monorepo may include many unrelated files.

The root directory is not automatically the best context.

Forgetting .dockerignore

A missing or poorly designed .dockerignore can allow:

.git
.env
node_modules
logs
build artifacts

into the build context.

Confusing Dockerfile location with context

This:

docker build -f docker/Dockerfile .

means:

Dockerfile = docker/Dockerfile
Context     = .

The two are separate.

Trying to copy files outside the context

This does not bypass the context boundary:

COPY ../file.txt /app/

The build context must be designed correctly instead.

Assuming context equals image contents

The context is the input available to the build.

The Dockerfile determines what becomes part of the image.

18. Troubleshooting Mental Model

If Docker reports that a file cannot be copied:

COPY / ADD failure
       ↓
Is the file in the build context?
       ↓
Is it excluded by .dockerignore?
       ↓
Is the source path correct?
       ↓
Is the selected context correct?
       ↓
Is the correct Dockerfile being used?

If a build is unexpectedly slow:

Build slow
   ↓
How large is the context?
   ↓
Is .dockerignore effective?
   ↓
Is COPY . . too broad?
   ↓
Are unnecessary files included?
   ↓
Is CI transferring the context to a remote builder?

This sequence helps distinguish a Dockerfile problem from a
build-context problem.

19. Production Relevance

In production CI/CD, build context should be treated as an explicit
build input.

A good setup generally aims for:

Required source
+
Required build files
+
Required shared files
-
Unnecessary files

This can improve:

build performance

cache efficiency

security

reproducibility

CI/CD efficiency

maintainability

The build context is therefore part of the build architecture, not just
a command-line detail.

20. IncidentLab Connection

IncidentLab's repository contains multiple areas such as:

Application
Infrastructure
Documentation
CI/CD

A Docker build should not automatically need every repository file.

A focused context helps maintain the separation:

Repository
     ↓
Relevant application context
     ↓
.dockerignore
     ↓
Docker build
     ↓
Image

This connects directly with the earlier topics:

COPY vs ADD
      ↓
Build Context
      ↓
.dockerignore
      ↓
Build Cache

Understanding this relationship is important when the project eventually
builds images in GitHub Actions.

21. Interview Takeaway

A strong interview explanation is:

"The Docker build context is the set of files made available to the
Docker build. COPY and ADD normally operate on files inside that
context. I keep the context as focused as practical and use
.dockerignore to exclude unnecessary or sensitive files. This
improves build performance, reduces unnecessary input, and can improve
cache efficiency, especially in CI/CD."

The key mental model is:

Build Context
      ↓
Available Build Inputs
      ↓
Dockerfile
      ↓
Selected Files
      ↓
Image

22. Key Takeaways

The build context is an input boundary for a Docker build.

The final argument to docker build usually specifies the context.

Dockerfile location and build-context location are separate
concepts.

COPY and ADD normally use files available in the build context.

.dockerignore filters unnecessary files from the context.

Build context is not the same thing as image contents.

A smaller, focused context can improve build performance.

Context boundaries prevent ordinary Dockerfile copies from reaching
arbitrary parent directories.

Build context design matters in monorepos and CI/CD.

Broad COPY . . instructions can increase cache sensitivity.

BuildKit supports more advanced context mechanisms, but controlled
inputs remain important.

23. Connections

Previous

16-copy-vs-add.md

Next

18-dockerignore.md

24. My Understanding

The Docker build context is the collection of files that the build is
allowed to use as input.

The simplest mental model is:

Project
   ↓
Choose build context
   ↓
.dockerignore
   ↓
Filtered build input
   ↓
Dockerfile
   ↓
Image

The key lesson is that the context should be large enough to contain
everything the build genuinely needs, but no larger than necessary.

This becomes especially important in production CI/CD because build
context size, file selection, cache behaviour, and security are all
connected.

25. Questions for Further Exploration

How does BuildKit transfer and process build context internally?

How does .dockerignore differ from .gitignore?

How should build context be designed for a large monorepo?

How do named BuildKit contexts work in practice?

How can GitHub Actions optimize Docker build context and caching?
