#!/bin/bash


./single-disk.sh

sed -i 's/IODEPTH=1/IODEPTH=2/g' single-disk.sh
sed -i 's/NUMJOBS=1/NUMJOBS=2/g' single-disk.sh
./single-disk.sh

sed -i 's/IODEPTH=2/IODEPTH=4/g' single-disk.sh
sed -i 's/NUMJOBS=2/NUMJOBS=4/g' single-disk.sh
./single-disk.sh

sed -i 's/IODEPTH=4/IODEPTH=8/g' single-disk.sh
sed -i 's/NUMJOBS=4/NUMJOBS=4/g' single-disk.sh
./single-disk.sh

sed -i 's/IODEPTH=8/IODEPTH=16/g' single-disk.sh
sed -i 's/NUMJOBS=4/NUMJOBS=4/g' single-disk.sh
./single-disk.sh

sed -i 's/IODEPTH=16/IODEPTH=8/g' single-disk.sh
sed -i 's/NUMJOBS=4/NUMJOBS=8/g' single-disk.sh
./single-disk.sh

sed -i 's/IODEPTH=8/IODEPTH=16/g' single-disk.sh
sed -i 's/NUMJOBS=8/NUMJOBS=8/g' single-disk.sh
./single-disk.sh

sed -i 's/IODEPTH=16/IODEPTH=32/g' single-disk.sh
sed -i 's/NUMJOBS=8/NUMJOBS=8/g' single-disk.sh
./single-disk.sh

sed -i 's/IODEPTH=32/IODEPTH=1/g' single-disk.sh
sed -i 's/NUMJOBS=8/NUMJOBS=1/g' single-disk.sh
