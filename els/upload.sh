#/bin/bash

for i in "$@"
do
  /usr/bin/curl -H 'Content-Type: application/json' -XPUT localhost:9200/_bulk --data-binary "@$i" 
done
