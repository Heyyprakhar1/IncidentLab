# Docker Volumes

---

# Objective

Understand why Docker Volumes are needed, how containers store data, what happens when a container is deleted, and how Docker Volumes provide persistent storage for production applications.

---

# Why Do Docker Volumes Exist?

Containers are designed to be **ephemeral**.

An ephemeral container means:

- It can be created anytime.
- It can be stopped anytime.
- It can be deleted anytime.

If an application stores its data only inside the container, deleting the container also deletes the data.

For stateless applications this is acceptable.

For databases, logs, uploaded files, and user-generated content, this is unacceptable.

Docker Volumes solve this problem.

---

# The Problem Without Volumes

Suppose we run a MySQL container.

```
MySQL Container

│

Database Files
```

Everything is stored inside the container filesystem.

Now imagine running:

```bash
docker rm mysql-container
```

Container is deleted.

Result:

```
Container ❌

Database ❌
```

The data is lost.

---

# What is a Docker Volume?

A Docker Volume is a persistent storage mechanism managed by Docker.

Unlike the container filesystem, volumes exist independently of containers.

Even if a container is removed, the volume remains.

---

# Architecture

Without Volume

```
Application

↓

Container Filesystem

↓

Container Deleted

↓

Data Deleted
```

---

With Volume

```
Application

↓

Container

↓

Docker Volume

↓

Host Storage
```

Deleting the container does not remove the volume.

---

# Container Writable Layer vs Volume

Container

```
Image Layers

↓

Writable Layer
```

All changes are stored in the writable layer.

This layer is deleted when the container is removed.

---

With Volume

```
Image Layers

↓

Writable Layer

↓

Docker Volume

↓

Host Disk
```

Persistent data is stored in the Docker Volume instead of the writable layer.

---

# Creating a Volume

Create a volume.

```bash
docker volume create mysql-data
```

List available volumes.

```bash
docker volume ls
```

Inspect a volume.

```bash
docker volume inspect mysql-data
```

Delete a volume.

```bash
docker volume rm mysql-data
```

---

# Using a Volume

Example

```bash
docker run \
-d \
--name mysql \
-v mysql-data:/var/lib/mysql \
mysql:8
```

Explanation

```
mysql-data
```

Docker Volume

↓

Mounted to

```
/var/lib/mysql
```

inside the container.

MySQL stores all database files in this directory.

---

# Named Volumes

Example

```bash
-v mysql-data:/var/lib/mysql
```

Characteristics:

- Managed by Docker.
- Recommended for production.
- Portable.
- Easy to backup.
- Easy to reuse.

---

# Anonymous Volumes

Example

```bash
-v /var/lib/mysql
```

Docker automatically creates a random volume name.

Characteristics:

- Temporary.
- Harder to manage.
- Usually not recommended.

---

# Bind Mounts

Example

```bash
-v /home/prakhar/project:/app
```

Host Directory

↓

Mounted directly inside the container.

Characteristics:

- Useful during development.
- Immediate file synchronization.
- Depends on host filesystem.

---

# Volume Types

```
Docker Storage

├── Named Volume
├── Anonymous Volume
└── Bind Mount
```

---

# Data Flow

```
Application

↓

Container

↓

Docker Volume

↓

Host Disk
```

The container accesses the volume.

Docker manages where the volume is physically stored.

---

# Real World Example

Imagine renting a furnished apartment.

The apartment represents the container.

Your personal locker represents the Docker Volume.

If you move to another apartment,

your locker still exists.

You simply reconnect it.

Containers work the same way.

---

# Common Use Cases

Docker Volumes are commonly used for:

- MySQL
- PostgreSQL
- MongoDB
- Redis Persistence
- Uploaded Images
- Application Logs
- Backup Data
- Shared Configuration

---

# Production Best Practices

- Use Named Volumes for persistent data.
- Avoid storing databases in the writable layer.
- Backup important volumes regularly.
- Separate application code from persistent data.
- Remove unused volumes periodically.
- Encrypt sensitive storage when required.

---

# Common Misconceptions

❌ Docker Volumes are inside containers.

✅ Volumes exist independently of containers.

---

❌ Removing a container removes its volume.

✅ Volumes remain unless explicitly removed.

---

❌ Bind Mounts and Volumes are the same.

✅ They serve different purposes.

---

❌ Containers are suitable for storing permanent data.

✅ Persistent data should be stored in Docker Volumes.

---

# Interview Explanation (90 Seconds)

Docker Volumes provide persistent storage for containers. Normally, any data written inside a container's writable layer is lost when the container is removed. Volumes solve this by storing data outside the container lifecycle. They are managed by Docker and can be mounted into multiple containers. Named Volumes are generally preferred in production because they provide portability, persistence, and easier management.

---

# Key Takeaways

- Containers are ephemeral.
- The writable layer is temporary.
- Docker Volumes provide persistent storage.
- Named Volumes are recommended for production.
- Bind Mounts are mainly useful during development.
- Volumes survive container deletion.

---

# My Understanding

Docker Volumes separate application data from the container itself. Instead of storing important files inside the container's writable layer, Docker stores them in a persistent volume managed outside the container lifecycle. This allows data such as databases, logs, and uploaded files to remain available even if the container is stopped, recreated, or deleted.

---

# Questions

- Where are Docker Volumes stored on the host?
- Can multiple containers share the same volume?
- When should I use a Bind Mount instead of a Named Volume?
- How are Docker Volumes backed up?
- What are Volume Drivers?

---

# Connections

## Previous

- 09 Multi-stage Builds

## Next

- 11 Docker Networking
