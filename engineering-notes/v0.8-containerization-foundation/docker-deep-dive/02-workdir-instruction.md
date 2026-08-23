WORKDIR Instruction

1. What Is WORKDIR?

WORKDIR sets the current working directory for subsequent
Dockerfile instructions and for the container's default runtime working
directory.

For example:

WORKDIR /app

establishes /app as the working directory.

A simple mental model is:

WORKDIR /app
     ↓
"From here, work inside /app"

2. Why Does WORKDIR Exist?

Without an explicit working directory, Dockerfile instructions and
application commands may operate relative to an unexpected location.

For example:

COPY . .
RUN pip install -r requirements.txt

is less explicit than:

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

With WORKDIR, the location of the application inside the image becomes
clear and predictable.

This improves:

readability

consistency

reproducibility

troubleshooting

runtime behaviour

3. Basic Usage

A common pattern is:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]

After:

WORKDIR /app

relative paths in subsequent instructions are evaluated from /app.

Therefore:

COPY requirements.txt .

places the file at:

/app/requirements.txt

and:

COPY . .

copies the application into:

/app

4. WORKDIR Affects Subsequent Instructions

WORKDIR is not limited to the command that immediately follows it.

For example:

WORKDIR /app

COPY . .

RUN ls
RUN python app.py

The later instructions operate with /app as their working directory
where the instruction supports a working directory context.

This makes the Dockerfile easier to reason about:

WORKDIR /app
     ↓
COPY
     ↓
RUN
     ↓
CMD

The same directory context is carried forward unless another WORKDIR
changes it.

5. WORKDIR and Runtime Containers

WORKDIR also affects the default working directory when a container is
started from the image.

For example:

FROM python:3.12-slim

WORKDIR /app

CMD ["python", "app.py"]

When the container starts, the application process runs with /app as
its working directory.

Conceptually:

Dockerfile
   ↓
WORKDIR /app
   ↓
Image configuration
   ↓
Container starts
   ↓
Process working directory = /app

This is why WORKDIR should be treated as both a build-time
path-management instruction and a runtime configuration
instruction.

6. Relative Paths Become Easier to Understand

Without WORKDIR, Dockerfiles can become filled with absolute paths:

COPY requirements.txt /app/requirements.txt
COPY . /app
RUN cd /app && pip install -r requirements.txt

With WORKDIR:

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

The second version expresses the intent more clearly.

The directory is declared once, and subsequent instructions use relative
paths where appropriate.

7. Multiple WORKDIR Instructions

A Dockerfile can contain multiple WORKDIR instructions.

For example:

WORKDIR /app

WORKDIR /app/config

The second instruction changes the current working directory for
subsequent instructions.

This can be useful when a build genuinely needs to operate in different
directories, but unnecessary changes can make a Dockerfile harder to
follow.

A common production pattern is to establish one clear application
directory and keep the Dockerfile consistent around it.

8. Relative WORKDIR Paths

WORKDIR can also use a relative path.

For example:

WORKDIR /app
WORKDIR src

The second instruction is interpreted relative to the current working
directory:

/app
  ↓
/app/src

This is valid, but absolute paths are often easier to understand in
production Dockerfiles because the intended location is immediately
visible.

9. Directory Creation Behaviour

If the specified working directory does not already exist in the image,
Docker creates it.

For example:

FROM python:3.12-slim

WORKDIR /app

does not require a separate:

RUN mkdir -p /app

This is one reason WORKDIR is preferable to manually creating and
changing directories.

Instead of:

RUN mkdir -p /app
RUN cd /app

use:

WORKDIR /app

10. WORKDIR vs RUN cd

This distinction is important.

Consider:

RUN cd /app
RUN pwd

The directory change made by the first RUN does not become the
persistent working directory for the next Dockerfile instruction.

Each RUN instruction executes in its own build step.

Instead, use:

WORKDIR /app

RUN pwd

Now /app is the working directory for the subsequent instructions.

Mental model:

RUN cd /app
     ↓
temporary command context

WORKDIR /app
     ↓
persistent Dockerfile working-directory configuration

This is a common Dockerfile misconception and an important
troubleshooting point.

11. WORKDIR and COPY

WORKDIR makes relative destination paths easier to understand.

For example:

WORKDIR /app

COPY requirements.txt .
COPY src/ ./src/

results conceptually in:

/app/
├── requirements.txt
└── src/

The source paths for COPY still come from the Docker build context,
while the relative destination is resolved using the current working
directory.

This distinction matters:

Build context
     ↓
source files

WORKDIR
     ↓
destination path context

12. WORKDIR and CMD / ENTRYPOINT

The runtime command also inherits the configured working directory.

For example:

WORKDIR /app

CMD ["python", "app.py"]

is effectively asking the container to run:

working directory = /app
command = python app.py

Therefore, if the application expects files relative to its current
directory, changing WORKDIR can change runtime behaviour.

For example:

open("config.yaml")

depends on the process's current working directory.

A change from:

/app

to:

/

could therefore cause the application to stop finding relative files.

13. Common Mistakes

Using RUN cd instead of WORKDIR

RUN cd /app

does not establish a persistent working directory for later
instructions.

Use:

WORKDIR /app

instead.

Assuming WORKDIR only affects build commands

It can also define the runtime working directory for the container.

This matters for commands such as:

CMD ["python", "app.py"]

and:

ENTRYPOINT ["./start.sh"]

Changing directories unnecessarily

Multiple WORKDIR instructions can make a Dockerfile harder to
understand if they are not required.

Prefer a clear and predictable directory structure.

Confusing WORKDIR with PATH

WORKDIR changes the current working directory.

It does not modify the executable search path.

For example:

WORKDIR /app

does not mean that /app has been added to $PATH.

14. Troubleshooting Mental Model

If an application cannot find a file, first check the working directory.

For example:

Application says:
"config.yaml not found"
        ↓
Check container working directory
        ↓
docker inspect / container shell
        ↓
Is WORKDIR what the application expects?
        ↓
Check where COPY placed the file
        ↓
Check relative path used by application

Useful commands include:

docker inspect <container>

and, when an interactive shell is available:

docker exec -it <container> sh

Then:

pwd
ls -la

This helps distinguish:

Wrong WORKDIR
     vs
Wrong COPY destination
     vs
Wrong application-relative path

15. Production Relevance

A deliberate WORKDIR improves the predictability of containerized
applications.

It helps establish:

consistent application paths

readable Dockerfiles

predictable runtime behaviour

easier troubleshooting

fewer path-related assumptions

It is generally better to explicitly define the intended working
directory rather than relying on an image's inherited default.

16. IncidentLab Connection

IncidentLab's containerized application uses a dedicated application
directory inside the container.

The Dockerfile can establish that directory with:

WORKDIR /app

After that, application files, dependency installation, and runtime
commands can consistently operate relative to /app.

Conceptually:

Base Image
    ↓
WORKDIR /app
    ↓
Application files
    ↓
Dependencies
    ↓
Runtime command

This keeps the container filesystem layout predictable and makes the
runtime behaviour easier to reason about.

17. Interview Takeaway

WORKDIR sets the working directory for subsequent Dockerfile
instructions and establishes the default working directory for the
container.

The key distinction is:

RUN cd /app
    ≠
WORKDIR /app

RUN cd is limited to that command's execution context, while WORKDIR
becomes part of the Dockerfile's build and runtime configuration.

A strong interview explanation is:

"I use WORKDIR to explicitly define the application directory
inside the image. It provides a consistent path for subsequent
Dockerfile instructions and also sets the container's default working
directory, which makes builds and runtime behaviour more
predictable."
