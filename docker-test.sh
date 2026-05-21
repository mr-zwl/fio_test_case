#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
IMAGE_NAME="fio-test"

echo "==> Building Docker image..."
docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"

echo ""
echo "==> Running fio tests in container (small params for validation)..."
echo "    SIZE=64m  RUNTIME=3s  RAMP_TIME=1s  COOLDOWN=1s"
echo "    CASES=1:1 2:2"
echo ""

docker run --rm \
    -e FILE_NAME=/tmp/fio_testfile \
    -e SIZE=64m \
    -e RUNTIME=3 \
    -e RAMP_TIME=1 \
    -e COOLDOWN=1 \
    -e CASES="1:1 2:2" \
    "$IMAGE_NAME" \
    /test/run.sh

echo ""
echo "==> Docker black-box test PASSED"
