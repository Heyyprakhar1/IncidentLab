ADD Instruction

1. What Is ADD?

ADD is a Dockerfile instruction used to copy files or directories into
the image, similar to COPY, but with additional Docker-specific
behaviour.

Basic syntax:

ADD <source> <destination>

For example:

ADD app.tar.gz /app/

The important idea is:

ADD
 ↓
Copy content into image
 +
Additional source-handling behaviour

Because ADD has more behaviour than straightforward file copying, it
should be used deliberately.

2. Why Does ADD Exist?

Docker needs a way to bring application files and other build inputs
into an image.

COPY already handles ordinary file and directory copying.

ADD exists because it also supports additional behaviours, most
notably:

local archive extraction

supported remote source handling

This makes ADD more capable than COPY, but that additional behaviour
can also make Dockerfiles less explicit.

A useful mental model is:

COPY
  ↓
Straightforward copying

ADD
  ↓
Copying
+
Additional Docker-specific behaviour

3. Basic Local Copy

ADD can copy local files just like COPY.

For example:

ADD requirements.txt /app/

The source comes from the Docker build context.

With:

docker build -t my-app .

the . defines the build context.

Therefore:

Build context
      ↓
ADD
      ↓
/app/requirements.txt

For ordinary file copying, however, COPY is generally clearer.

4. Automatic Local Archive Extraction

One of the most important differences between ADD and COPY is
support for local archives.

For example:

ADD app.tar.gz /app/

When the source is a supported local archive, Docker can extract it into
the destination rather than simply copying the archive file itself.

Conceptually:

app.tar.gz
    ↓
ADD
    ↓
Extracted application files
    ↓
/app

This behaviour is one of the main reasons ADD exists as a distinct
instruction.

It also means that ADD can have side effects that are not obvious from
the word "copy" alone.

5. ADD and Remote Sources

ADD also supports certain remote source forms.

For example, Docker can retrieve supported remote content and add it to
the image.

However, remote retrieval inside a Dockerfile can make builds harder to
reason about because the Dockerfile now depends on an external resource.

A production-oriented Dockerfile should therefore use remote ADD
deliberately rather than treating it as a general download mechanism.

For most application dependencies, it is often clearer to:

Fetch dependencies explicitly
        ↓
Control versions
        ↓
Verify them where appropriate
        ↓
Build reproducibly

rather than hiding external downloads inside a generic image-building
instruction.

6. ADD vs COPY

This is the most important practical distinction.

COPY

Designed primarily for:

Files
Directories

from the build context, and for copying files between build stages with
--from.

ADD

Supports ordinary copying plus additional behaviours such as:

Local archive extraction
Remote source handling

A useful decision rule is:

Need ordinary file/directory copying?
        ↓
Use COPY

Need ADD-specific behaviour?
        ↓
Consider ADD

For example:

COPY app.tar.gz /app/

means the archive is copied as a file.

Whereas:

ADD app.tar.gz /app/

can extract a supported local archive.

7. Why COPY Is Usually Preferred

Using the more capable instruction is not automatically better.

A Dockerfile is easier to understand when each instruction has an
obvious purpose.

Compare:

ADD . /app

with:

COPY . /app

The second communicates a straightforward operation:

Copy these files into the image.

This makes the Dockerfile easier for another engineer to read and reason
about.

Therefore, a common production guideline is:

Use COPY for ordinary copying and reserve ADD for cases where
its additional behaviour is actually required.

8. ADD and Build Context

Local ADD sources follow the Docker build-context boundary.

For:

docker build -t my-app .

the current directory is the build context.

Therefore:

ADD config.yaml /app/

expects config.yaml to be available within that context.

It cannot arbitrarily reach unrelated files elsewhere on the host
filesystem.

This is similar to COPY and is important when troubleshooting:

File exists on host
        ↓
But is it inside build context?
        ↓
Is it excluded by .dockerignore?
        ↓
Can ADD access it?

9. ADD and .dockerignore

When local files are involved, .dockerignore still affects what enters
the build context.

For example:

.git
.env
node_modules
__pycache__

can be excluded.

The flow remains:

Host directory
      ↓
.dockerignore
      ↓
Build context
      ↓
ADD
      ↓
Image

This is important because an ADD instruction cannot copy a file that
never entered the build context.

10. ADD in Multi-Stage Builds

ADD can be used in a multi-stage Dockerfile, but it does not replace
the more common COPY --from pattern for transferring build output.

For example:

FROM builder AS build

# build application

FROM runtime

COPY --from=build /build/output /app

The COPY --from form is explicit about transferring files from another
stage.

If ordinary cross-stage copying is required, COPY --from is generally
the clearer choice.

11. Common Mistakes

Using ADD everywhere because it "does more"

More functionality does not mean better design.

For ordinary copying:

COPY . .

is usually clearer than:

ADD . .

Expecting COPY to extract an archive

For example:

COPY app.tar.gz /app/

copies the archive.

It does not provide the same automatic local-archive extraction
behaviour associated with ADD.

Using remote ADD as a general download mechanism

External downloads can introduce:

network dependency

reproducibility concerns

unexpected changes

harder troubleshooting

Dependencies should generally be handled through a deliberate and
controlled build process.

Forgetting the build context

A file being present somewhere on the host does not automatically make
it available to ADD.

The file must be accessible through the build context according to
Docker's build rules.

12. Troubleshooting Mental Model

If an ADD instruction behaves unexpectedly, first identify what kind
of source is being used:

What is the source?
        ↓
Local file/directory
        │
        ├── Is it in build context?
        ├── Is it ignored?
        └── Is the path correct?
        │
        ▼
Local archive?
        │
        └── Is automatic extraction expected?
        │
        ▼
Remote source?
        │
        ├── Is the source reachable?
        ├── Is the content what was expected?
        └── Is the build reproducible?

This is more useful than treating every ADD failure as a generic
Dockerfile syntax problem.

13. Production Relevance

ADD is useful, but its extra behaviour means it should be used
intentionally.

Production Dockerfiles benefit from:

explicit file operations

predictable builds

controlled dependencies

minimal hidden behaviour

clear Dockerfile intent

For most application source and configuration files, COPY provides the
clearer and more predictable choice.

ADD becomes appropriate when its additional semantics, such as
supported local archive extraction, are actually needed.

14. IncidentLab Connection

The IncidentLab containerization approach favours explicit and
production-oriented Dockerfile construction.

For ordinary application files and dependency definitions, the clearer
model is:

Build context
      ↓
COPY required files
      ↓
Install dependencies
      ↓
COPY application source
      ↓
Runtime image

ADD is therefore an important Dockerfile instruction to understand,
but it should not be introduced simply because it can perform more
operations than COPY.

This keeps the container build process easier to reason about and
troubleshoot.

15. Interview Takeaway

ADD can copy files and directories into a Docker image, while also
providing additional Docker-specific behaviour such as supported local
archive extraction and remote source handling.

The key distinction is:

COPY
  ↓
Explicit, straightforward copying

ADD
  ↓
Copying
+
Additional behaviour

A strong interview answer is:

"I generally prefer COPY for normal file and directory copying
because its behaviour is explicit. I use ADD when I specifically
need one of its additional capabilities, such as supported local
archive extraction."

The important point is not that ADD is bad; it is that the
Dockerfile should make its intent clear and predictable.
