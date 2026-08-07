#1 Select the Base Image
FROM python:3.12-slim 

#2 Set the Container Working Directory
WORKDIR /app

#3 Install and Verify the UV Package Manager
RUN apt-get update && \
    apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ~/.local/bin/uv --version

#4 Make UV Available System-wide
ENV PATH="/root/.local/bin:${PATH}"	

#5 Copy Dependency Definition Files
COPY pyproject.toml uv.lock .

#6 Install Project Dependencies
RUN uv sync

#7 Copy the Application Source Code
COPY . .

#8 Define the Fixed Executable
ENTRYPOINT ["uv","run","uvicorn"]

#9 Define Default Runtime Arguments
CMD ["app.main:app","--host","0.0.0.0","--port","8000"]

#10 Document the Application Port
EXPOSE 8000
