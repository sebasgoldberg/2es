#/bin/bash

for i in "$@"
do
  /usr/bin/curl -XPUT localhost:9200/_bulk --data-binary "@$i" > /dev/null
done
