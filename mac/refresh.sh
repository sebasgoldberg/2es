#!/bin/bash
#curl -XDELETE localhost:9200/windows_clients/?pretty
#curl -XPUT localhost:9200/windows_clients/?pretty
curl -XPUT localhost:9200/windows_clients/_mapping/status?pretty --data-binary @mac/mapping.json

