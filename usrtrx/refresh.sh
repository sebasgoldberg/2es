#!/bin/bash
curl -XDELETE 10.151.1.21:9200/usrtrx/?pretty
curl -XPUT 10.151.1.21:9200/usrtrx/?pretty
curl -XPUT 10.151.1.21:9200/usrtrx/_mapping/usrtrx?pretty --data-binary @usrtrx/mapping.json

