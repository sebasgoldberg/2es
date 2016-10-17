#!/bin/bash
curl -XDELETE 10.151.1.21:9200/nomina/?pretty
curl -XPUT 10.151.1.21:9200/nomina/?pretty
curl -XPUT 10.151.1.21:9200/nomina/_mapping/nomina?pretty --data-binary @nomina/mapping.json

