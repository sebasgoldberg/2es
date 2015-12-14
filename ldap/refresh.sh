#!/bin/bash
curl -XDELETE 10.151.1.21:9200/ldap/?pretty
curl -XPUT 10.151.1.21:9200/ldap/?pretty
curl -XPUT 10.151.1.21:9200/ldap/_mapping/ldap?pretty --data-binary @ldap/mapping.json

