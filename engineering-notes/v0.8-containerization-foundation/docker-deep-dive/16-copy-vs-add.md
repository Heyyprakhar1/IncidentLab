COPY vs ADD

1. Why COPY and ADD Matter

Both COPY and ADD are Dockerfile instructions used to place files
into an image.

At a basic level:

Host / Build Context
        ↓
COPY / ADD
        ↓
Image filesystem

For example:

COPY app.py /app/

or:

ADD app.py /app/

They can look interchangeable, but they have important differences.

The most useful production principle is:

Use COPY when simple file copying is all you need. Use ADD only
when one of its additional capabilities is intentionally required.

2. Basic Syntax

COPY

COPY <source> <destination>

Example:

COPY app.py /app/

ADD

ADD <source> <destination>

Example:

ADD app.tar.gz /app/

Both instructions can copy files and directories from the Docker build
context into the image.

3. The Core Difference

The simplest mental model is:

COPY
  ↓
Straightforward file / directory copying

ADD
  ↓
COPY
+
additional Docker-specific behaviour

ADD has capabilities that COPY does not provide in the same way,
particularly automatic extraction of local tar archives and support for
certain URL/Git sources.

Because of that additional behaviour, ADD can be less explicit.

For ordinary application files:

COPY . .

is usually the clearer choice.

4. Copying Files With COPY

Example:

WORKDIR /app

COPY requirements.txt .
COPY app.py .

The files are copied from the build context into the image.

Conceptually:

Build context
├── requirements.txt
└── app.py
       ↓
COPY
       ↓
Image
└── /app
    ├── requirements.txt
    └── app.py

This makes COPY a straightforward tool for moving application files
into the image.

5. Copying Directories With COPY

COPY can also copy directories.

For example:

COPY src/ /app/src/

This transfers the relevant directory content into the image.

Another common pattern is:

COPY . .

This copies the build-context contents that are not excluded by
.dockerignore.

That is convenient, but in production Dockerfiles it should still be
used deliberately because the build context may contain unnecessary
files.

6. ADD Can Also Copy Files

For ordinary local files:

ADD app.py /app/

can perform a similar basic copy operation.

So why not always use ADD?

Because the additional behaviour of ADD can make the Dockerfile less
explicit.

Compare:

COPY app.tar.gz /app/

with:

ADD app.tar.gz /app/

The second can have special archive-extraction behaviour.

When simple copying is intended, COPY communicates that intent more
clearly.

7. Automatic Local Tar Extraction

One of the important additional behaviours of ADD is automatic
extraction of certain local tar archives.

For example:

ADD app.tar.gz /app/

can cause the archive contents to be extracted into /app/.

This differs from:

COPY app.tar.gz /app/

which copies the archive as a file.

Conceptually:

COPY

app.tar.gz
    ↓
/app/app.tar.gz

while:

ADD

app.tar.gz
    ↓
extract
    ↓
/app/<archive contents>

This behaviour is one reason ADD should be used intentionally.

8. Why Automatic Extraction Can Be Useful

There are legitimate cases where automatic extraction is useful.

For example, an image may intentionally be built from a prepared local
archive:

ADD application.tar.gz /opt/application/

The archive can contain a known application structure.

In such a case:

Archive
   ↓
ADD
   ↓
Extracted application files

can be convenient.

However, if extraction is not explicitly desired, using ADD can create
surprising behaviour.

9. ADD and URLs

ADD historically supports remote sources such as URLs.

For example:

ADD https://example.com/file.tar.gz /tmp/

This is another capability that goes beyond straightforward local file
copying.

However, remote downloads inside Dockerfiles introduce additional
considerations around:

reproducibility

network availability

caching

integrity

security

build determinism

For many production builds, it is clearer to download external artifacts
explicitly with a controlled build step or package-management mechanism.

The key principle is:

Do not use ADD merely because it can download something. Use
remote downloads deliberately and with appropriate verification.

10. ADD and Git Sources

Modern Docker build tooling can also support Git-related sources for
ADD in appropriate build contexts.

The exact behaviour depends on the Docker builder and source format.

The important learning point is not to treat ADD as a general-purpose
source downloader.

For normal application source already present in the build context:

COPY . .

is clearer.

11. COPY and Build Context

COPY normally works with files available to the Docker build context.

For:

docker build -t my-app .

the:

.

represents the build context.

Therefore:

COPY app.py /app/

means Docker expects app.py to be available within that context.

Files excluded by .dockerignore are not available to ordinary
context-based copying.

The flow is:

Project directory
       ↓
.dockerignore
       ↓
Build context
       ↓
COPY
       ↓
Image

This is why .dockerignore and COPY are closely related.

12. Source Paths and Context Boundaries

Docker restricts ordinary build-context copying to files available
through the build context.

For example, if the build command is:

docker build -t my-app .

you cannot simply use:

COPY ../secret.txt /app/

to escape the build context.

The build context defines what files are available to the build.

This is an important security and reproducibility boundary.

13. COPY --chown

COPY can also set file ownership during the copy.

For example:

COPY --chown=appuser:appuser . /app/

This can be useful when the application is intended to run as a non-root
user.

Instead of:

COPY . /app/

RUN chown -R appuser:appuser /app

you can sometimes make ownership correct during the copy itself.

Conceptually:

COPY
   ↓
Files + correct ownership

This can avoid an additional recursive filesystem operation and fits
well with production Dockerfile optimization.

14. COPY --from and Multi-Stage Builds

COPY also has an important capability in multi-stage builds.

For example:

FROM node:22 AS builder

WORKDIR /build

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /build/dist /usr/share/nginx/html

Here:

COPY --from=builder ...

copies files from another build stage rather than from the local build
context.

The flow is:

Builder stage
      ↓
Build output
      ↓
COPY --from
      ↓
Final stage

This is one of the key patterns behind multi-stage production images.

15. ADD vs COPY: Practical Decision

A useful decision process is:

Do I simply need to copy files?
        │
        ├── Yes
        │    ↓
        │  COPY
        │
        └── No
             ↓
        Do I intentionally need
        ADD-specific behaviour?
             │
             ├── Yes → ADD
             └── No  → COPY

For most ordinary application files:

COPY

is the default choice.

ADD should have a specific reason.

16. Common Mistakes

Using ADD everywhere

For example:

ADD . .

is often used simply because it works.

But if the intent is ordinary file copying:

COPY . .

is clearer.

Accidentally extracting an archive

If you intend to preserve:

app.tar.gz

as an archive:

COPY app.tar.gz /app/

is more explicit.

Using ADD may trigger archive extraction behaviour when the source
qualifies.

Downloading arbitrary URLs with ADD

Remote downloads can introduce:

Network dependency
+
Reproducibility concerns
+
Integrity concerns

External artifacts should be handled deliberately and verified
appropriately.

Forgetting .dockerignore

Using:

COPY . .

without controlling the build context can unintentionally include:

.git
.env
logs
node_modules
temporary files

This can increase build size, leak unwanted content, and affect cache
behaviour.

Using RUN unnecessarily to copy files

Avoid patterns such as:

RUN cp app.py /app/

when:

COPY app.py /app/

directly expresses the operation.

Dockerfile instructions should communicate intent clearly.

17. COPY vs ADD and Caching

Both instructions participate in Docker's build process and can affect
cache reuse.

For example:

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

separates stable dependency input from frequently changing application
source.

Changing:

app.py

does not necessarily invalidate:

COPY requirements.txt
RUN pip install

when the relevant inputs remain unchanged.

This connects COPY directly with the earlier build-cache topic.

18. COPY vs ADD and Security

Neither instruction should be treated as a secret-management mechanism.

Avoid copying sensitive files into images:

COPY .env .

when .env contains credentials.

Also remember that remote sources and extracted archives require
appropriate trust and integrity considerations.

A production image should contain only the files it actually needs.

The broader principle is:

Build context
     ↓
Controlled files
     ↓
COPY / ADD
     ↓
Intentional image contents

19. Troubleshooting Mental Model

If a file is missing from an image:

Does the source exist?
      ↓
Is it inside the build context?
      ↓
Is it excluded by .dockerignore?
      ↓
Is the COPY / ADD source path correct?
      ↓
Is the destination path correct?
      ↓
Was the correct image rebuilt?
      ↓
Are you inspecting the correct image/tag?

If an archive behaves unexpectedly:

Was COPY used?
      ↓
Archive remains a file

Was ADD used?
      ↓
Check whether automatic extraction applies

If a multi-stage file is missing:

Is COPY --from using the correct stage?
      ↓
Does the source path exist in that stage?
      ↓
Is the final destination correct?

20. Production Relevance

For production Dockerfiles, COPY is usually the default for ordinary
local application files because it is explicit and predictable.

ADD remains useful when its additional semantics are actually needed.

A production-oriented mindset is:

Simple requirement
      ↓
Use the simplest instruction

Special requirement
      ↓
Use the instruction that provides it

This keeps Dockerfiles easier to review, troubleshoot, and maintain.

21. IncidentLab Connection

The IncidentLab Dockerfile structure uses the same production-oriented
principle:

Dependency files
      ↓
COPY
      ↓
Install dependencies
      ↓
Application source
      ↓
COPY

This supports both:

Clear intent
+
Build-cache efficiency

The COPY --from pattern also becomes important when the project uses
multi-stage builds:

Builder
   ↓
Build artifact
   ↓
COPY --from
   ↓
Runtime image

This connects COPY with the earlier topics of:

Build Context
Build Cache
Production Dockerfiles
Multi-Stage Builds

22. Interview Takeaway

A strong interview explanation is:

"I generally prefer COPY for normal application files because it
has straightforward and explicit semantics. ADD provides additional
behaviour, such as automatic extraction of qualifying local tar
archives and support for certain remote sources, so I use it only when
I intentionally need those capabilities."

The key mental model is:

COPY
  ↓
Predictable file copying

ADD
  ↓
File copying
+
additional behaviour

23. Key Takeaways

Both COPY and ADD can place files into an image.

COPY is generally the default for ordinary application files.

ADD has additional Docker-specific behaviour.

ADD can automatically extract qualifying local tar archives.

ADD can support certain remote sources depending on the build
context/tooling.

Remote downloads introduce reproducibility and integrity
considerations.

COPY --chown can set file ownership during copying.

COPY --from is central to multi-stage builds.

.dockerignore controls what is available in the build context.

Neither COPY nor ADD should be used for secrets.

The correct choice depends on the intended behaviour, not on a
blanket rule.

24. Connections

Previous

15-shell-vs-exec-form.md

Next

17-build-context.md

25. My Understanding

The simplest way to remember the distinction is:

COPY
  ↓
"I want to copy these files."

ADD
  ↓
"I want to copy these files and I intentionally need
 ADD's additional behaviour."

For production Dockerfiles, choosing COPY by default makes the intent
obvious.

When ADD is used, there should be a clear reason for using its
additional capabilities.

26. Questions for Further Exploration

How does Docker determine whether a local archive should be
automatically extracted?

How does .dockerignore affect COPY . .?

How does COPY --from interact with build cache?

When is downloading an artifact during the build preferable to
adding it from the build context?

How should external artifacts be verified for integrity in a
production CI/CD pipeline?
