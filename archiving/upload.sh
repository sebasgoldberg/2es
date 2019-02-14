#!/bin/bash

WORKDIR="/home/cerebro/evopre/archiving"
SPACE_INFO="$1"

cd "$WORKDIR"
rm -rf archiving.*
dos2unix "$SPACE_INFO"
./read.py config/Archiving-Objects-SAP-Tables.xls "$SPACE_INFO"
../els/upload.sh archiving.* > /dev/null
