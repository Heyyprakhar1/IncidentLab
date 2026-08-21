Shell Form vs Exec Form

1. What Are Shell Form and Exec Form?

Dockerfile instructions such as RUN, CMD, and ENTRYPOINT can use
different command forms.

The two important forms are:

Shell Form
Exec Form

For example:

Shell form

CMD python app.py

Exec form

CMD ["python", "app.py"]

They may appear similar, but Docker handles them differently.

The most important distinction is:

Shell Form
    ↓
Command is interpreted through a shell

Exec Form
    ↓
Executable and arguments are passed directly

Understanding this difference is especially important for CMD and
ENTRYPOINT.

2. Why Does the Difference Matter?

The form you choose affects:

shell interpretation

environment-variable expansion

signal handling

process hierarchy

argument handling

container shutdown behaviour

how ENTRYPOINT and CMD work together

A Dockerfile can therefore be syntactically valid while still having
undesirable runtime behaviour because the wrong form was chosen.

A useful mental model is:

Dockerfile command
       ↓
Which form?
       ├── Shell form → shell involved
       └── Exec form  → direct process execution

3. Shell Form

The shell form is written as a normal command string.

For example:

CMD python app.py

Docker uses a shell to interpret the command.

Conceptually:

Docker
  ↓
Shell
  ↓
python app.py

The shell can provide shell features such as:

variable expansion

command chaining

redirection

pipes

shell operators

For example:

CMD echo "Environment: $APP_ENV"

The shell can interpret:

$APP_ENV

as an environment-variable reference.

4. Exec Form

The exec form uses JSON-array syntax:

CMD ["python", "app.py"]

Here:

Executable = python
Argument 1 = app.py

Docker passes the executable and arguments directly rather than first
invoking a shell for normal command interpretation.

Conceptually:

Docker
  ↓
python
  ↓
app.py

This makes the intended process much more explicit.

5. Basic Comparison

Consider:

CMD python app.py

versus:

CMD ["python", "app.py"]

The first is:

Shell form

The second is:

Exec form

Mental model:

Shell form

Docker
  ↓
Shell
  ↓
Application


Exec form

Docker
  ↓
Application

The difference becomes particularly important when the container
receives operating-system signals.

6. Environment Variable Expansion

Shell form can use shell-based environment-variable expansion.

For example:

ENV APP_ENV=production

CMD echo "Running in $APP_ENV"

The shell can expand:

$APP_ENV

before executing the command.

With exec form:

ENV APP_ENV=production

CMD ["echo", "Running in $APP_ENV"]

the string:

$APP_ENV

is not automatically expanded by a shell because no shell is being
invoked for the command.

This is an important practical distinction.

If shell expansion is intentionally required, the shell can be invoked
explicitly:

CMD ["sh", "-c", "echo Running in $APP_ENV"]

Now the process is explicitly:

sh
  ↓
interprets command
  ↓
expands $APP_ENV
  ↓
executes command

7. Shell Features

Shell form is useful when actual shell functionality is required.

For example:

CMD echo "Starting" && python app.py

The shell can interpret:

&&

Similarly:

CMD python app.py | tee /tmp/app.log

uses shell pipeline behaviour.

Or:

CMD echo "Starting" > /tmp/startup.log

uses shell redirection.

These are shell features.

Exec form:

CMD ["python", "app.py"]

does not automatically interpret:

&&
|
>
$

as shell syntax.

8. Explicit Shell With Exec Form

Exec form does not mean shell syntax can never be used.

If shell functionality is required, invoke the shell explicitly:

CMD ["sh", "-c", "echo Starting && python app.py"]

This makes the shell dependency visible.

The mental model is:

Exec form
    ↓
sh
    ↓
shell command

This is often clearer than hiding shell behaviour inside a shell-form
instruction.

However, introducing a shell should be intentional because it also
affects process and signal behaviour.

9. Signal Handling

Signal handling is one of the most important production differences.

Suppose the container runs:

CMD python app.py

With shell form, the shell can become the process Docker launches, with
the application running beneath it.

Conceptually:

PID 1
  ↓
Shell
  ↓
Python
  ↓
Application

With exec form:

CMD ["python", "app.py"]

the application process can become the main container process:

PID 1
  ↓
Python
  ↓
Application

This matters because PID 1 has special responsibilities in a container,
including signal handling and child-process management.

For long-running production applications, direct process execution is
generally preferable when a shell is not actually required.

10. Why PID 1 Matters

The first process inside the container normally has PID 1.

For example:

Container
   ↓
PID 1
   ↓
Application

When Docker stops a container, it sends a termination signal to the
container's main process.

If the actual application is PID 1, the application can handle the
signal directly.

For example:

docker stop
     ↓
SIGTERM
     ↓
Application PID 1
     ↓
Graceful shutdown

If a shell sits between Docker and the application, signal propagation
can become more complicated.

This is one reason exec form is commonly preferred for application
startup commands.

11. Graceful Shutdown

A production application should ideally shut down gracefully.

For example:

SIGTERM
   ↓
Application receives signal
   ↓
Stop accepting new work
   ↓
Finish active work
   ↓
Close connections
   ↓
Exit

Exec form helps make the application the main container process:

CMD ["python", "app.py"]

This makes signal delivery and process ownership easier to reason about.

This becomes especially important in environments such as:

Docker Compose

Kubernetes

CI/CD test containers

production container platforms

12. ENTRYPOINT and Shell vs Exec Form

The distinction becomes even more important with ENTRYPOINT.

Shell form

ENTRYPOINT python app.py

Exec form

ENTRYPOINT ["python", "app.py"]

The exec form makes the application process explicit.

It also allows CMD to provide default arguments in a predictable way.

For example:

ENTRYPOINT ["python", "app.py"]

CMD ["--port", "8000"]

Conceptually:

ENTRYPOINT
    ↓
python app.py
    +
CMD
    ↓
--port 8000

The resulting process is effectively:

python app.py --port 8000

This pattern is useful when an image has a fixed executable with
configurable default arguments.

13. CMD and Shell vs Exec Form

CMD also supports both forms.

Shell:

CMD python app.py

Exec:

CMD ["python", "app.py"]

The exec form is usually preferred for normal application startup
because:

the executable is explicit

arguments are explicit

no implicit shell is required

process behaviour is easier to reason about

Shell form can still be appropriate when shell interpretation is
intentionally required.

14. RUN and Shell vs Exec Form

RUN can also use both forms.

Shell:

RUN apt-get update && apt-get install -y curl

Exec:

RUN ["executable", "arg1", "arg2"]

The shell form is common for build commands because package installation
and build operations often use shell operators such as:

&&
|
>

For example:

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

The shell is intentionally useful here.

This illustrates an important principle:

Do not choose exec form simply because it is "better"; choose the
form that matches the command's actual requirements.

15. Shell Form vs Exec Form: Practical Decision

A useful decision process is:

Do I need shell features?
        │
        ├── Yes
        │    ↓
        │  Shell form
        │  or explicit shell
        │
        └── No
             ↓
           Exec form

For application startup:

Need shell?
   ├── No → Exec form
   └── Yes → Explicit shell / deliberate shell form

For complex build commands:

Need &&, pipes, redirection, shell expansion?
   ├── Yes → Shell semantics may be appropriate
   └── No  → Exec form can be used

The decision should be based on behaviour, not a blanket rule.

16. Common Mistakes

Using shell form for every command

This can introduce an unnecessary shell into runtime process execution.

For a simple application:

CMD ["python", "app.py"]

is usually clearer than:

CMD python app.py

Expecting exec form to expand variables

This:

CMD ["echo", "$APP_ENV"]

does not automatically perform shell expansion.

If shell expansion is required:

CMD ["sh", "-c", "echo $APP_ENV"]

Using shell syntax in exec form

This does not mean what many beginners expect:

CMD ["python", "app.py", "&&", "echo", "done"]

Docker passes:

&&
echo
done

as arguments to Python.

The shell is not interpreting the operators.

Ignoring PID 1 behaviour

A container can appear to work normally while still having poor
signal-handling behaviour during shutdown.

This becomes visible in production when applications receive:

SIGTERM

and need to shut down gracefully.

Adding a shell unnecessarily

Using:

CMD ["sh", "-c", "python app.py"]

when no shell feature is required adds another process layer without a
clear benefit.

17. Troubleshooting Mental Model

When a container does not stop gracefully:

docker stop
     ↓
Which process is PID 1?
     ↓
Shell?
     ↓
Application?
     ↓
Where does SIGTERM go?
     ↓
Does the application handle SIGTERM?
     ↓
Does the application exit cleanly?

When environment variables are not expanding:

Is the command shell form?
        ↓
Yes → shell expansion may occur

No
        ↓
Exec form
        ↓
No implicit shell expansion
        ↓
Need shell?
        ↓
Use explicit sh -c if appropriate

When arguments behave unexpectedly:

CMD / ENTRYPOINT
       ↓
Shell form or exec form?
       ↓
Is a shell modifying the command?
       ↓
How are arguments being passed?

This structured approach is much more useful than simply changing syntax
until the container appears to work.

18. Production Relevance

Shell vs exec form becomes especially important in production because
containers are expected to:

start predictably

receive signals correctly

shut down gracefully

handle arguments consistently

behave correctly under orchestration

For a long-running application, a common pattern is:

ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]

This gives:

Explicit executable
        +
Explicit arguments
        +
Predictable process model

Shell form remains useful where shell behaviour is genuinely required.

The goal is not to eliminate shell usage completely.

The goal is to avoid implicit shell behaviour when it is
unnecessary.

19. IncidentLab Connection

IncidentLab's containerized services are long-running application
processes, so predictable startup and shutdown behaviour matter.

For example:

CMD ["python", "app.py"]

keeps the application process explicit.

If the application later needs configurable startup arguments:

ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]

provides a clear separation between:

Fixed executable
     ↓
ENTRYPOINT

Default arguments
     ↓
CMD

This connects directly with the project's troubleshooting focus around:

Process
PID 1
Signals
Graceful shutdown
Container lifecycle

20. Interview Takeaway

Shell form runs a command through shell semantics, while exec form
passes the executable and arguments directly.

A strong interview explanation is:

"For normal application startup, I prefer exec form because it makes
the process explicit and avoids an unnecessary shell. This is
important for PID 1 and signal handling, especially for graceful
shutdown. I use shell form when I actually need shell features such as
variable expansion, pipes, redirection, or command chaining."

The key mental model is:

Shell Form
    ↓
Shell
    ↓
Command

Exec Form
    ↓
Executable
    ↓
Arguments

21. Key Takeaways

Shell form and exec form are different command representations.

Shell form invokes shell semantics.

Exec form passes the executable and arguments directly.

Shell form is useful when shell features are required.

Exec form is generally preferred for simple application startup.

Exec form makes PID 1 and signal handling easier to reason about.

Exec form does not automatically expand environment variables.

sh -c can be used explicitly when shell behaviour is required.

CMD and ENTRYPOINT are especially important areas for this
distinction.

RUN can use either form depending on build-command requirements.

The correct form depends on the intended behaviour, not a blanket
"one is always better" rule.

22. Connections

Previous

14-healthcheck-instruction.md

Next

16-copy-vs-add.md

23. My Understanding

The shell-vs-exec distinction is fundamentally about how Docker
launches and interprets a command.

The simplest mental model is:

Shell Form
    ↓
Shell interprets command
    ↓
Application

Exec Form
    ↓
Docker launches executable directly
    ↓
Application

For production application containers, exec form is often the cleaner
choice because the application can become the main process and receive
lifecycle signals more predictably.

Shell form is still valuable when shell functionality is actually
required.

24. Questions for Further Exploration

Why is PID 1 behaviour different from a normal Linux process?

How exactly does docker stop interact with the container's main
process?

How do ENTRYPOINT and CMD combine in shell and exec forms?

What happens when a shell script is used as an entrypoint?

How does Kubernetes signal handling depend on the container's PID 1?
