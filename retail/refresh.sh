#!/bin/bash
curl -XDELETE 10.151.1.21:9200/retail/?pretty
curl -XPUT 10.151.1.21:9200/retail/?pretty
curl -XPUT 10.151.1.21:9200/retail/_mapping/retail?pretty --data-binary @retail/mapping.json

