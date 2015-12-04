#!/usr/bin/python
#encoding=utf8

import sys
import datetime
import json
from els.lang import Lang
from els.utils import ElasticFilesGenerator
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from retail.mapping import RetailMapping
from datetime import timedelta as TD

retail_mapping = RetailMapping()

L=Lang.get_instance()

INDEX = 'retail'
TYPE = 'retail'
FILE_NAME_PREFIX = 'retail/retail.delete'

es = Elasticsearch(['10.151.1.21',])
efg = ElasticFilesGenerator(INDEX, TYPE, FILE_NAME_PREFIX, preserve_path=True)

def read_index(index):
    
    res = scan(es, {
        "query" : {
            "filtered" : {
                "filter" : {
                    "bool" : {
                        "must_not" : {
                            "terms": { "loja" : [ "B503", "B514", "B555", "B612", "B634" ]
                                }
                            }
                        }
                     }
                 }
             }
         }, index=index)

    return res


def read():

    retail = read_index('retail')

    for register in retail:
        efg.delete(register['_id'])

read()

