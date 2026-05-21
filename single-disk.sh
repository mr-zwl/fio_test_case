#!/bin/bash
set -euo pipefail

IOENGINE="libaio"
FILE_NAME="${FILE_NAME:-/dev/cbd3}"
NUMJOBS="${NUMJOBS:-1}"
IODEPTH="${IODEPTH:-1}"
DIRECT="${DIRECT:-1}"
SIZE="${SIZE:-260g}"
RUNTIME="${RUNTIME:-90}"
RAMP_TIME="${RAMP_TIME:-10}"
COOLDOWN="${COOLDOWN:-5}"

RW=(randwrite randread write read)
BS=(4k 8k 16k 32k 64k 128k)
MIXRW=(randrw rw)
RWMIXREAD=70

command -v fio >/dev/null 2>&1 || { echo "Error: fio not installed"; exit 1; }

if [ -b "$FILE_NAME" ]; then
    :
elif [ -d "$(dirname "$FILE_NAME")" ]; then
    DIRECT=0
else
    echo "Error: $FILE_NAME is not a block device and parent dir does not exist"
    exit 1
fi

cooldown() {
    sleep "$COOLDOWN"
    sync
    if [ -w /proc/sys/vm/drop_caches ]; then
        echo 3 > /proc/sys/vm/drop_caches
    fi
}

echo "Config: device=${FILE_NAME} numjobs=${NUMJOBS} iodepth=${IODEPTH} runtime=${RUNTIME}s ramp_time=${RAMP_TIME}s"

for rw_name in "${RW[@]}"; do
    for bs_size in "${BS[@]}"; do
        test_name="iscsi_${IOENGINE}_${NUMJOBS}_${IODEPTH}_${rw_name}_${bs_size}"
        echo "Running: ${test_name}"
        fio \
            --ioengine=${IOENGINE} \
            --numjobs=${NUMJOBS} \
            --direct=${DIRECT} \
            --size=${SIZE} \
            --iodepth=${IODEPTH} \
            --runtime=${RUNTIME} \
            --time_based \
            --ramp_time=${RAMP_TIME} \
            --rw=${rw_name} \
            --ba=${bs_size} \
            --bs=${bs_size} \
            --filename=${FILE_NAME} \
            --name="${test_name}" \
            --group_reporting \
            --output-format=json \
            --output="${test_name}.json"
        cooldown
    done
done

for rw_name in "${MIXRW[@]}"; do
    for bs_size in "${BS[@]}"; do
        test_name="iscsi_${IOENGINE}_${NUMJOBS}_${IODEPTH}_${rw_name}_${RWMIXREAD}_${bs_size}"
        echo "Running: ${test_name}"
        fio \
            --ioengine=${IOENGINE} \
            --numjobs=${NUMJOBS} \
            --direct=${DIRECT} \
            --size=${SIZE} \
            --iodepth=${IODEPTH} \
            --runtime=${RUNTIME} \
            --time_based \
            --ramp_time=${RAMP_TIME} \
            --rw=${rw_name} \
            --rwmixread=${RWMIXREAD} \
            --ba=${bs_size} \
            --bs=${bs_size} \
            --filename=${FILE_NAME} \
            --name="${test_name}" \
            --group_reporting \
            --output-format=json \
            --output="${test_name}.json"
        cooldown
    done
done

echo "Done: numjobs=${NUMJOBS} iodepth=${IODEPTH}"
