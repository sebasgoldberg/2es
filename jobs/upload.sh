#!/bin/bash

WORKDIR="/home/cerebro/evopre/jobs"
FILE="$1"

cd "$WORKDIR"
rm -rf jobs.*
dos2unix "$FILE"
./read.py "$FILE"
../els/upload.sh jobs.* > /dev/null
