FROM python:3

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update -qq \
    && apt-get install -qqy \
        build-essential \
        git \
    && apt-get clean \
    && python3 -m venv "$VIRTUAL_ENV" \
    && pip install --no-cache-dir "pre-commit>=4,<5"

LABEL org.opencontainers.image.description="pre-commit Docker image"
LABEL org.opencontainers.image.source=https://bitbucket.org/nobleo/nobleo-pre-commit
