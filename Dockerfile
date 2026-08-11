# Copyright (C) 2025 Nobleo Autonomous Solutions B.V.

FROM python:3-slim
ARG RUNNER="pre-commit>=4,<5"

RUN apt-get update -qq \
    && apt-get install -qqy --no-install-recommends \
        git git-lfs \
    && rm -rf /var/lib/apt/lists \
    && pip install --no-cache-dir "${RUNNER}"

LABEL org.opencontainers.image.description="${RUNNER} Docker image"
LABEL org.opencontainers.image.source=https://github.com/nobleo/nobleo-pre-commit
