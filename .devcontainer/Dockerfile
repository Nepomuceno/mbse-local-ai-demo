# Pick your Python image variant (3.10–3.12 available)
ARG VARIANT=3.12
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

# Install uv (Rust-powered package manager) and Git LFS
RUN pip install --no-cache-dir uv && \
    uv --version && \
    apt-get update && \
    apt-get install -y git-lfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install additional OS packages here if you need them
# RUN apt-get update && apt-get install -y <package list>