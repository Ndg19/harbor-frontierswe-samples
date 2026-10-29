FROM --platform=linux/amd64 python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7
RUN apt-get update && apt-get install -y --no-install-recommends bash git tmux procps asciinema patch && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY upstream.tar.gz /tmp/upstream.tar.gz
RUN mkdir -p /app/repo /app/submission && tar -xzf /tmp/upstream.tar.gz -C /app && rm /tmp/upstream.tar.gz && chmod 777 /app/submission
COPY FRAMING_SPEC.md /app/FRAMING_SPEC.md
COPY data /app/data
ENV PYTHONPATH=/app/repo
