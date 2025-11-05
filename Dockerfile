FROM python:3-alpine

RUN apk --no-cache update \
    && apk --no-cache add git bash
RUN pip install --no-cache-dir "pre-commit>=4,<5"

LABEL org.opencontainers.image.description="pre-commit Docker image"
LABEL org.opencontainers.image.source=https://bitbucket.org/nobleo/nobleo-pre-commit
