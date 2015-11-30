#!/usr/bin/python
#encoding=utf8

import sys
import datetime
import json
from els.lang import Lang
from els.utils import ElasticFilesGenerator
from elasticsearch import Elasticsearch

L=Lang.get_instance()

INDEX = 'retail'
TYPE = 'retail'
FILE_NAME_PREFIX = 'retail'

def read(data):

    es = Elasticsearch(['10.151.1.21',])
    efg = ElasticFilesGenerator(INDEX, TYPE, FILE_NAME_PREFIX)

    data_desde = datetime.datetime.combine(data,datetime.datetime.min.time())
    data_ate = datetime.datetime.combine(data,datetime.datetime.max.time())

    res = es.search(index="venda", body={
        "range" : {
            "data" : {
                "gte" : data_desde,
                "lte" : data_ate,
                "boost" : 2.0
                } } }) 

    for hit in res['hits']['hits']:
        register = hit['_source']
        efg.add(register, "%s%s" % (register[L.matid], str(register[L.data][0:10]).replace('-','')))

read(datetime.date(2015,11,25))
