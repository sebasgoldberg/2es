#!/bin/bash
curl -XDELETE 10.151.1.21:9200/precos/?pretty
curl -XPUT 10.151.1.21:9200/precos/?pretty
curl -XPUT 10.151.1.21:9200/precos/_mapping/venda?pretty --data-binary @precios/mapping.json

