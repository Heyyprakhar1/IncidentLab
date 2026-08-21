ENTRYPOINT Instruction

1. What Is ENTRYPOINT?

ENTRYPOINT defines the executable that a container is intended to run.

Example:

ENTRYPOINT ["python"]

Mental model:

Container starts
    ↓
ENTRYPOINT
    ↓
Main executable

It is commonly used when the image represents a specific executable or
service.

2. ENTRYPOINT vs CMD

The simplest distinction is:

ENTRYPOINT
    ↓
What executable should run?

CMD
    ↓
What default arguments should it receive?

Example:

ENTRYPOINT ["python"]
CMD ["app.py"]

results in:

python app.py

3. Overriding CMD

Given:

ENTRYPOINT ["python"]
CMD ["app.py"]

running:

docker run my-app

uses:

python app.py

But:

docker run my-app worker.py

changes the arguments:

python worker.py

The ENTRYPOINT remains the executable.

4. Overriding ENTRYPOINT

Docker also allows the entrypoint to be replaced at runtime.

For example:

docker run --entrypoint /bin/sh my-app

This is useful for:

Debugging
Troubleshooting
Administrative tasks

It also demonstrates that ENTRYPOINT is a strong default, not an
absolute security boundary.

5. Exec Form

The preferred form for executable entrypoints is:

ENTRYPOINT ["python", "app.py"]

or:

ENTRYPOINT ["python"]
CMD ["app.py"]

Exec form avoids an unnecessary shell layer.

This matters for:

PID 1
Signals
Graceful shutdown
Child processes

6. Shell Form

Shell form is:

ENTRYPOINT python app.py

This introduces shell behaviour.

The difference can affect:

Signal propagation
Process hierarchy
Environment handling
Shutdown behaviour

For production services, understand the process tree created by the
chosen form.

7. PID 1 and ENTRYPOINT

The main container process occupies PID 1 in the container's PID
namespace.

Conceptually:

Container
   ↓
PID 1
   ↓
ENTRYPOINT process
   ↓
Application

PID 1 has special responsibilities around signal handling and
child-process reaping.

This is why a poorly designed entrypoint wrapper can cause shutdown
problems.

8. ENTRYPOINT Wrapper Scripts

A wrapper script can be useful:

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

The script may perform:

Initialization
Configuration
Validation
Then exec application

The important detail is:

exec "$@"

when appropriate.

Using exec replaces the shell process with the application process,
helping the application receive signals correctly.

9. Why exec Matters

Without proper exec behaviour:

PID 1
 ↓
Shell script
 ↓
Application

With:

exec "$@"

the process becomes:

PID 1
 ↓
Application

This can improve:

SIGTERM handling
Graceful shutdown
Process lifecycle

10. ENTRYPOINT and Container Lifecycle

The entrypoint is directly tied to the container's main process.

ENTRYPOINT
    ↓
Application starts
    ↓
Application exits
    ↓
Container exits

Therefore, if an entrypoint script completes without starting a
long-running process, the container may stop immediately.

11. Common Mistake: ENTRYPOINT Script Finishes

Suppose:

ENTRYPOINT ["/entrypoint.sh"]

and the script contains only:

echo "Starting..."

Then:

Script exits
   ↓
PID 1 exits
   ↓
Container stops

A startup script must eventually launch or exec the intended
long-running process when the container is supposed to remain running.

12. ENTRYPOINT + CMD Pattern

A very common pattern is:

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["server"]

The relationship is:

ENTRYPOINT
    ↓
Fixed startup executable

CMD
    ↓
Default argument

This allows:

docker run image

to use the default:

entrypoint.sh server

while still allowing:

docker run image worker

to use:

entrypoint.sh worker

13. CMD Alone vs ENTRYPOINT + CMD

CMD alone

CMD ["python", "app.py"]

The entire default command can be replaced.

ENTRYPOINT + CMD

ENTRYPOINT ["python"]
CMD ["app.py"]

The executable is separated from the default arguments.

Mental model:

CMD alone
   ↓
Default command

ENTRYPOINT + CMD
   ↓
Executable + default arguments

14. Use Cases

ENTRYPOINT is useful when:

Image represents one main executable
A fixed startup executable is desirable
Default arguments should remain configurable
Initialization logic is required

Examples include:

CLI tools
Workers
Application services
Custom startup wrappers

15. Troubleshooting ENTRYPOINT

If a container fails immediately:

1. Inspect ENTRYPOINT
        ↓
2. Inspect CMD
        ↓
3. Check executable exists
        ↓
4. Check permissions
        ↓
5. Check working directory
        ↓
6. Check script interpreter
        ↓
7. Check line endings
        ↓
8. Check logs

A classic issue with shell scripts created on Windows is incorrect line
endings.

For example:

/bin/sh^M

can cause an entrypoint script to fail on Linux.

16. ENTRYPOINT and Permissions

If:

ENTRYPOINT ["/app/entrypoint.sh"]

but the script is not executable:

Permission denied

The image build may succeed while the container fails at runtime.

Check:

ls -l /app/entrypoint.sh

and ensure the runtime permissions are appropriate.

17. ENTRYPOINT and Security

An entrypoint should not blindly trust environment variables or external
input.

For example:

Environment variable
       ↓
Shell command construction
       ↓
Potential command injection

Avoid unsafe patterns where user-controlled values are interpolated into
shell commands.

Prefer:

Explicit arguments
+
Safe process execution

where possible.

18. Interview Takeaway

"ENTRYPOINT defines the executable a container is intended to run.
When combined with CMD, ENTRYPOINT commonly provides the fixed
executable while CMD supplies default arguments. I prefer exec form
for production processes because signal handling and PID 1 behaviour
matter for graceful shutdown."

Mental model:

ENTRYPOINT
    ↓
Executable

CMD
    ↓
Default arguments
