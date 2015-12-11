#!/bin/bash
curl -XDELETE 10.151.1.21:9200/wdecide/?pretty
curl -XPUT 10.151.1.21:9200/wdecide/?pretty
curl -XPUT 10.151.1.21:9200/wdecide/_mapping/wdecide?pretty --data-binary @wdecide/mapping.json

