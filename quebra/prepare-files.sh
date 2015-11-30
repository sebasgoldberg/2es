#!/bin/bash

for i in "$@"
do
  /usr/bin/dos2unix "$i"
  /bin/sed -i '/"Resultado"/d' "$i"
  /bin/sed -i '/"Resultado global"/d' "$i"
done
