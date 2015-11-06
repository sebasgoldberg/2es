#/bin/bash

for i in "$@"
do
  curl -XPUT 10.151.1.21:9200/_bulk --data-binary "@$i" > /dev/null
done
