#!/bin/bash
curl -XDELETE 10.151.1.21:9200/precios/?pretty
curl -XPUT 10.151.1.21:9200/precios/?pretty
curl -XPUT 10.151.1.21:9200/precios/_mapping/venta?pretty --data-binary @mapping.json

