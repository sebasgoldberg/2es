#!/bin/bash
curl -XDELETE 10.151.1.21:9200/trdir/?pretty
curl -XPUT 10.151.1.21:9200/trdir/?pretty
curl -XPUT 10.151.1.21:9200/trdir/_mapping/trdir?pretty --data-binary @trdir/mapping.json

