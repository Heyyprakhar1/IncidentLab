CMD Instruction

1. What Is CMD?

CMD defines the default command or default arguments that Docker uses
when a container starts.

Example:

CMD ["python", "app.py"]

Mental model:

Docker image
    ↓
Container starts
    ↓
Default CMD
    ↓
Application runs

CMD is primarily a runtime default, not a build instruction.

2. Why CMD Exists

An image can contain an application, but Docker still needs to know what
should normally happen when a container starts.

For example:

FROM python:3.12

WORKDIR /app
COPY . .

CMD ["python", "app.py"]

The image contains:

Application files

and CMD defines:

Default startup command

3. CMD Does Not Run During Build

Consider:

RUN pip install -r requirements.txt
CMD ["python", "app.py"]

The distinction is:

RUN
 ↓
Build time

CMD
 ↓
Container runtime

So:

docker build .

executes the RUN instruction during image construction.

The CMD is used later when a container is started.

4. Exec Form

The preferred form is usually the JSON/exec form:

CMD ["python", "app.py"]

This represents:

Executable
   ↓
python

Arguments
   ↓
app.py

It avoids introducing a shell as the command process.

This is especially important when process signals and PID 1 behaviour
matter.

5. Shell Form

CMD can also be written as:

CMD python app.py

This is the shell form.

Conceptually:

CMD
 ↓
Shell
 ↓
Application

The shell can affect:

Signal handling
Environment expansion
Process hierarchy

Therefore, understand which form the Dockerfile is using instead of
treating them as identical.

6. CMD Can Be Overridden

Suppose:

CMD ["python", "app.py"]

and run:

docker run my-app

Docker uses the default command.

But:

docker run my-app python worker.py

provides a runtime command.

Conceptually:

Image CMD
    ↓
Default

docker run ... COMMAND
    ↓
Runtime override

This is one of the most important properties of CMD.

7. CMD as Default Arguments

When combined with ENTRYPOINT, CMD has another useful role.

Example:

ENTRYPOINT ["python"]
CMD ["app.py"]

Conceptually:

ENTRYPOINT
    ↓
python

CMD
    ↓
app.py

Final process
    ↓
python app.py

Here CMD acts as the default argument list.

This pattern becomes especially useful when the executable should remain
fixed while the default arguments may change.

8. Only One Effective CMD

A Dockerfile can contain multiple CMD instructions syntactically, but
only the final CMD is effective.

For example:

CMD ["echo", "one"]

CMD ["echo", "two"]

The resulting image uses:

echo two

Therefore, do not use multiple CMD instructions as if Docker will
execute all of them.

9. CMD and Application Lifecycle

A container normally lives as long as its main process lives.

Therefore:

CMD
 ↓
Main application process
 ↓
Process exits
 ↓
Container stops

For example:

CMD ["python", "app.py"]

If:

app.py exits

the container normally exits too.

This connects CMD directly to container lifecycle.

10. CMD and PID 1

The main container process becomes PID 1 in the container's process
namespace.

For example:

Container
   ↓
PID 1
   ↓
Application

How the command is started affects:

Signal handling
Child process management
Shutdown behaviour

This is one reason exec-form commands are generally preferred for
long-running applications.

11. CMD vs RUN

Do not confuse:

RUN

with:

CMD

RUN

Build image
    ↓
Execute command
    ↓
Create image state

CMD

Start container
    ↓
Use default command

Mental model:

RUN → "Do this while building."

CMD → "Run this by default when starting."

12. CMD vs ENTRYPOINT

The difference becomes clearer when both are used.

CMD

Default command

and can be overridden.

ENTRYPOINT

Default executable

and is intended to be the main executable.

Example:

ENTRYPOINT ["python"]
CMD ["app.py"]

gives:

python app.py

while:

docker run my-app worker.py

results conceptually in:

python worker.py

The next topic covers ENTRYPOINT in depth.

13. Common Mistake: Expecting CMD to Run During Build

This will not run the application during:

docker build .

CMD ["python", "app.py"]

It is a runtime instruction.

If you need a command during image construction:

RUN ...

is the relevant instruction.

14. Troubleshooting CMD

If the container immediately exits:

1. Check docker ps -a
        ↓
2. Check docker logs
        ↓
3. Inspect CMD
        ↓
4. Check whether command exists
        ↓
5. Check working directory
        ↓
6. Check required files
        ↓
7. Check environment variables

A valid image can still produce a failed container if its default
command is incorrect.

15. Interview Takeaway

"CMD specifies the default command or default arguments used when a
container starts. It runs at container runtime, not image build time,
and it can be overridden when using docker run. When combined with
ENTRYPOINT, CMD commonly supplies default arguments to a fixed
executable."

Mental model:

CMD
 ↓
Default runtime behaviour
