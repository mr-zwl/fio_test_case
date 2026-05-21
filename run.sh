#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SINGLE_DISK="${SCRIPT_DIR}/single-disk.sh"

if [ ! -x "$SINGLE_DISK" ]; then
    echo "Error: ${SINGLE_DISK} not found or not executable"
    exit 1
fi

# iodepth:numjobs
DEFAULT_CASES="1:1 2:2 4:4 8:4 16:4 8:8 16:8 32:8"
read -ra CASES <<< "${CASES:-$DEFAULT_CASES}"

TOTAL=${#CASES[@]}
CURRENT=0

for case in "${CASES[@]}"; do
    IFS=: read -r iodepth numjobs <<< "$case"
    CURRENT=$((CURRENT + 1))
    echo "============================================"
    echo "  [${CURRENT}/${TOTAL}] IODEPTH=${iodepth} NUMJOBS=${numjobs}"
    echo "============================================"
    IODEPTH="$iodepth" NUMJOBS="$numjobs" "$SINGLE_DISK"
done

echo ""
echo "All fio tests completed. Parsing results..."
echo ""
echo "=== Pure IO Results ==="
python3 "${SCRIPT_DIR}/result-1.py"
echo ""
echo "=== Mixed RW Results ==="
python3 "${SCRIPT_DIR}/result-rw-1.py"
