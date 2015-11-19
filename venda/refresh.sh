#!/bin/bash
curl -XDELETE 10.151.1.21:9200/venda/?pretty
curl -XPUT 10.151.1.21:9200/venda/?pretty
curl -XPUT 10.151.1.21:9200/venda/_mapping/venda?pretty --data-binary @venda/mapping.json

