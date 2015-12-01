#!/usr/bin/python
#encoding=utf8

import sys
import datetime
import json
from els.lang import Lang
from els.utils import ElasticFilesGenerator
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

L=Lang.get_instance()

INDEX = 'retail'
TYPE = 'retail'
FILE_NAME_PREFIX = '../retail'

def read(data):

    es = Elasticsearch(['10.151.1.21',])
    efg = ElasticFilesGenerator(INDEX, TYPE, FILE_NAME_PREFIX)

    data_desde = datetime.datetime.combine(data,datetime.datetime.min.time())
    data_ate = datetime.datetime.combine(data,datetime.datetime.max.time())

    #res = es.search(index="venda", body={"query": {"match_all": {}}}, search_type='scan')

    res = scan(es, {"query": {"match_all": {}}}, index="venda")

    for i in res:
        print i['_id']
        print i['_source']

    """
    print("Got %d Hits:" % res['hits']['total'])

    for hit in res['hits']['hits']:
        register = hit['_source']
        #efg.add(register, "%s%s" % (register[L.matid], str(register[L.data][0:10]).replace('-','')))
        print register
    """

read(datetime.date(2015,11,25))
