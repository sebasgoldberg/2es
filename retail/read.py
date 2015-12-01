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
FILE_NAME_PREFIX = 'retail/retail'

es = Elasticsearch(['10.151.1.21',])
efg = ElasticFilesGenerator(INDEX, TYPE, FILE_NAME_PREFIX)

def retail_id(x):
    return "%s%s" % (x['_source'][L.matid], str(x['_source'][L.data][0:10]).replace('-',''))

def read_index(index, data_desde, data_ate):
    
    res = scan(es, {
        "query" : {
            "filtered" : {
                "filter" : {
                    "range" : {
                        "data" : {
                            "gte" : data_desde.strftime("%Y-%m-%d %H:%M:%S"),
                            "lte" : data_ate.strftime("%Y-%m-%d %H:%M:%S")
                            } } } } } }, index=index)

    res = sorted(res, key=retail_id)


def read(data_desde=datetime.date.today(), data_ate=None):

    if data_ate is None:
        data_ate = data_desde

    data_desde = datetime.datetime.combine(data_desde,datetime.datetime.min.time())
    data_ate = datetime.datetime.combine(data_ate,datetime.datetime.max.time())

    venda = read_index('venda', data_desde, data_ate)
    quebra = read_index('quebra', data_desde, data_ate)
    ruptura = read_index('ruptura', data_desde, data_ate)

    todos_los_registros_leidos = True
    ivenda, iquebra, iruptura = 0, 0, 0

    while not todos_los_registros_leidos:
        idvenda = retail_id(venda[ivenda])
        idquebra = retail_id(quebra[iquebra])
        idruptura = retail_id(ruptura[iruptura])

        if idvenda == idquebra:
            if idquebra == idruptura:
                register = venda[ivenda]['_source']
                register.update(quebra[iquebra]['_source'])
                register.update(ruptura[iruptura['_source'])
                efg.add(register, "%s%s" % (register[L.matid], str(register[L.data][0:10]).replace('-','')))
                ivenda = ivenda + 1
                iquebra = iquebra + 1
                iquebra = iquebra + 1
            elif idquebra < idruptura:

if len(sys.argv) == 1:
    read()
elif len(sys.argv) == 2:
    read(datetime.datetime.strptime(sys.argv[1],"%d.%m.%Y"))
elif len(sys.argv) == 3:
    read(datetime.datetime.strptime(sys.argv[1],"%d.%m.%Y"),
        datetime.datetime.strptime(sys.argv[2],"%d.%m.%Y"))
