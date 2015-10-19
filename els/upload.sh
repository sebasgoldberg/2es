#/bin/bash

for i in "$@"
do
  curl -XPUT localhost:9200/_bulk --data-binary "@$i" > /dev/null
done
