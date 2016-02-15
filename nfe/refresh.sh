#!/bin/bash
curl -XDELETE localhost:9200/nfe/?pretty
curl -XPUT localhost:9200/nfe/?pretty
curl -XPUT localhost:9200/nfe/_mapping/nfe?pretty --data-binary @nfe/mapping.json

