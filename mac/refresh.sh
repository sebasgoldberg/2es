#!/bin/bash
curl -XDELETE 10.151.1.21:9200/mac/?pretty
curl -XPUT 10.151.1.21:9200/mac/?pretty
curl -XPUT 10.151.1.21:9200/mac/_mapping/mac?pretty --data-binary @mac/mapping.json

