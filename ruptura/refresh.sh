#!/bin/bash
curl -XDELETE 10.151.1.21:9200/ruptura/?pretty
curl -XPUT 10.151.1.21:9200/ruptura/?pretty
curl -XPUT 10.151.1.21:9200/ruptura/_mapping/ruptura?pretty --data-binary @ruptura/mapping.json

