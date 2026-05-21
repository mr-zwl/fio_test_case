FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends fio python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /test
COPY run.sh single-disk.sh result-1.py result-rw-1.py ./
RUN chmod +x run.sh single-disk.sh

WORKDIR /output
