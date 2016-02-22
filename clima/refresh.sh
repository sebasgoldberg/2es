#!/bin/bash
INDEX='clima'
curl -XDELETE localhost:9200/$INDEX/?pretty
curl -XPUT localhost:9200/$INDEX/?pretty
curl -XPUT localhost:9200/$INDEX/_mapping/$INDEX?pretty --data-binary @$INDEX/mapping.json

