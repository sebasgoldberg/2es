#!/bin/bash
curl -H 'Content-Type: application/json' -XDELETE localhost:9200/usrtrx/?pretty
curl -H 'Content-Type: application/json' -XPUT localhost:9200/usrtrx/?pretty
curl -H 'Content-Type: application/json' -XPUT localhost:9200/usrtrx/_mapping/usrtrx?pretty --data-binary @usrtrx/mapping.json

