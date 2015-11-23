#!/bin/bash
curl -XDELETE 10.151.1.21:9200/windows_clients/?pretty
curl -XPUT 10.151.1.21:9200/windows_clients/?pretty
curl -XPUT 10.151.1.21:9200/windows_clients/_mapping/status?pretty --data-binary @mac/mapping.json

