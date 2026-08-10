#1 Select the Base Image
FROM python:3.12-slim

#2 Set the Container Working Directory
WORKDIR /app

#3 Pin the UV installer version
ARG UV_VERSION=0.12.2

#4 Install and Verify UV
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | \
    env UV_INSTALL_DIR="/usr/local/bin" sh && \
    uv --version && \
    rm -rf /var/lib/apt/lists/*

#5 Copy Dependency Definition Files
COPY pyproject.toml uv.lock .

#6 Install Project Dependencies
RUN uv sync --locked

#7 Create the Non-Root Application User
RUN useradd --create-home --uid 1000 incidentlab

#8 Copy the Application Source Code
COPY . .

#9 Switch to the Non-Root Runtime User
USER incidentlab

#10 Make the Virtual Environment Available in PATH
ENV PATH="/app/.venv/bin:/usr/local/bin:${PATH}"

#11 Define the Fixed Executable
ENTRYPOINT ["uvicorn"]

#12 Define Default Runtime Arguments
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#13 Document the Application Port
EXPOSE 8000

#14 Define the Container Health Check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1
