#/bin/bash
rm precios-venta.*.json
#dos2unix data/B*
time (./clear.py && ./read.py data/B* && ./calc.py && ./els/top_var.py)
