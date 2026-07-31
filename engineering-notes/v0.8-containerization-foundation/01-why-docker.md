# Why Docker?

---

## Objective

Understand why Docker was created and what real-world problem it solves.

---

## Problem Statement

Before Docker, developers only shared application code.

However, an application is much more than just source code. It also depends on the runtime environment, programming language version, system libraries, operating system, environment variables, database configuration, and many other dependencies.

As a result, the same application often behaved differently across development, testing, and production environments.

This led to one of the most common software engineering problems:

> "It works on my machine."

---

## Why Existing Solutions Were Not Enough

Virtual Machines solved environment isolation, but they were expensive in terms of CPU, memory, storage, and startup time.

Each virtual machine required its own complete operating system, making development and deployment slower.

Teams needed a lighter and more portable solution.

---

## Core Concept

Docker packages an application together with everything it needs to run.

Instead of sharing only the source code, Docker shares a reproducible runtime environment so that the application behaves consistently across different machines.

The goal is consistency, portability, and reproducibility.

---

## Mental Model

Think of application code as a recipe.

Without Docker:

Recipe is shared.

Everyone gathers their own ingredients and uses a different kitchen.

Results may vary.

With Docker:

The recipe, ingredients, and kitchen are packaged together.

Anyone using the package gets the same result.

---

## IncidentLab Example

Without Docker, running IncidentLab on a new machine requires:

- Installing Git
- Installing the correct Python version
- Installing uv
- Installing project dependencies
- Creating environment variables
- Installing and configuring PostgreSQL
- Running database migrations
- Starting the application

Docker allows this environment to be recreated in a consistent and repeatable way.

---

## Interview Explanation (60 Seconds)

Docker was created to solve environment inconsistency.

Instead of sharing only application code, Docker packages the application's runtime environment along with its dependencies, allowing the application to run consistently across development, testing, and production environments.

Unlike traditional deployment approaches, Docker focuses on reproducibility and portability.

---

## Common Misconceptions

❌ Docker only packages application code.

✅ Docker packages the application's runtime environment.

---

❌ Docker was created primarily for performance.

✅ Docker was created primarily to provide consistent and reproducible environments.

---

❌ Docker replaces Virtual Machines.

✅ Docker complements Virtual Machines and solves a different problem.

---

## Key Takeaways

- Applications depend on more than just source code.
- Environment inconsistency causes deployment problems.
- Docker packages the runtime environment along with the application.
- Docker's primary goal is consistency and reproducibility.

---

## My Understanding

Docker is often defined as a containerization platform that packages an application along with its dependencies. However, I think the real reason Docker exists is to solve the problem of environment mismatches, which was a major challenge before Docker. The same application could behave differently across development, testing, and production environments because of differences in operating systems, libraries, runtime versions, configurations, or other dependencies.

Docker addresses this by packaging not just the application code and its dependencies, but the complete runtime environment required to run the application consistently. This ensures that the application behaves the same way regardless of where it is deployed.
---

## Questions

- If Virtual Machines already solved environment isolation, why was Docker created?
- How does Docker package an environment without installing a complete operating system?
- What exactly is a container internally?
- How does Docker ensure the same application behaves consistently on different machines?
- What is the difference between an image and a container?
