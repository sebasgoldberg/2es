#!/bin/bash

ROOTDIR="$(cd "$(dirname "$0")" && pwd)"
SRCDIR="$ROOTDIR/src"
BULKDIR="$ROOTDIR/bulk"

rm "$BULKDIR/"*
cd "$SRCDIR"
"$ROOTDIR/read.py" *
cd "$ROOTDIR"
./upload.sh "$BULKDIR/"*
