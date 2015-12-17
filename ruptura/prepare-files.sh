#!/bin/bash

dos2unix "$@"

for i in "$@"; do
    NEW_FILE_NAME="$(echo "$i" | sed 's/\(.*\)\/.*_\([0-9]*\)_\([0-9]*\)_\([0-9]*\).*/\1\/\4-\3-\2-ruptura/g')"
    mv "$i" "$NEW_FILE_NAME"
done
