#!/bin/bash
set -x

#SHELL_FOLDER=$(dirname "$0")
#source ${SHELL_FOLDER}/common_variable_iscsi

IOENGINE="libaio"

FILE_NAME="/dev/cbd3"

RW=(randwrite randread write read)
BS=(4k 8k 16k 32k 64k 128k)

NUMJOBS=1
DIRECT=1
SIZE="260g"
IODEPTH=1
RUNTIME=90

for rw_name in ${RW[@]}
do
  for bs_size in ${BS[@]}
  do
    fio -ioengine=${IOENGINE} -numjobs=${NUMJOBS} -direct=${DIRECT} -size=${SIZE} -iodepth=${IODEPTH} -runtime=${RUNTIME} -rw=${rw_name} -ba=${bs_size} -bs=${bs_size} -filename=${FILE_NAME} -name="iscsi_${IOENGINE}_${NUMJOBS}_${IODEPTH}_${rw_name}_${bs_size}" -group_reporting > iscsi_${IOENGINE}_${NUMJOBS}_${IODEPTH}_${rw_name}_${bs_size}.log
    sleep 1
  done
done

MIXRW=(randrw rw)
RWMIXREAD=70

for rw_name in ${MIXRW[@]}
do
  for bs_size in ${BS[@]}
  do
    fio -ioengine=${IOENGINE} -numjobs=${NUMJOBS} -direct=${DIRECT} -size=${SIZE} -iodepth=${IODEPTH} -runtime=${RUNTIME} -rw=${rw_name} -rwmixread=${RWMIXREAD} -ba=${bs_size} -bs=${bs_size} -filename=${FILE_NAME} -name="iscsi_${IOENGINE}_${NUMJOBS}_${IODEPTH}_${rw_name}_${RWMIXREAD}_${bs_size}" -group_reporting > iscsi_${IOENGINE}_${NUMJOBS}_${IODEPTH}_${rw_name}_${RWMIXREAD}_${bs_size}.log
    sleep 1
  done
done
