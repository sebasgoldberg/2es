#/bin/bash

for i in "$@"
do
  rm precios-venta."$i".*.json
  ./read.py "data/$i.txt"
  ./calc.py "$i"
  ./els/top_var.py "$i"
done
