#!/bin/bash

for i in "$@"
do
  dos2unix "$i"
  sed -i '/"Resultado"/d' "$i"
  sed -i '/"Resultado global"/d' "$i"
done
