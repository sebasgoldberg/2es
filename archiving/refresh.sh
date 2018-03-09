#!/bin/bash
curl -H 'Content-Type: application/json' -XDELETE localhost:9200/archiving/?pretty
curl -H 'Content-Type: application/json' -XPUT localhost:9200/archiving/?pretty
#curl -H 'Content-Type: application/json' -XPUT localhost:9200/archiving/_mapping/usrtrx?pretty --data-binary @usrtrx/mapping.json

