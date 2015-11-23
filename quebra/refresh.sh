#!/bin/bash
curl -XDELETE 10.151.1.21:9200/quebra/?pretty
curl -XPUT 10.151.1.21:9200/quebra/?pretty
curl -XPUT 10.151.1.21:9200/quebra/_mapping/quebra?pretty --data-binary @quebra/mapping.json

