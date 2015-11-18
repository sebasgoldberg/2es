#/bin/bash

for i in "$@"
do
  rm precios-venta."$i".*.json
  ./precios/read.py "data/$i"
  ./precios/calc.py "$i"
  ./precios/els/top_var.py "$i"
done
