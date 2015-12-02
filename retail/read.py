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

    return sorted(res, key=retail_id)

def retail_id_from_model_data(model_data, index):

    if index < len(model_data):
        return retail_id(model_data[index])
    return None


def copy_independent_fields(register, source):

    if register[L.data] is not None:
        return
    
    register[L.data] = source[L.data]
    register[L.loja] = source[L.loja]
    register[L.secao] = source[L.secao]
    register[L.material] = source[L.material]
    register[L.matid] = source[L.matid]
    register[L.descricao_material] = source[L.descricao_material]
    register[L.descricao_secao] = source[L.descricao_secao]

def read(data_desde=datetime.date.today(), data_ate=None):

    if data_ate is None:
        data_ate = data_desde

    data_desde = datetime.datetime.combine(data_desde,datetime.datetime.min.time())
    data_ate = datetime.datetime.combine(data_ate,datetime.datetime.max.time())

    venda = read_index('venda', data_desde, data_ate)
    quebra = read_index('quebra', data_desde, data_ate)
    ruptura = read_index('ruptura', data_desde, data_ate)

    ivenda, iquebra, iruptura = 0, 0, 0

    register = retail_mapping.create_empty_register()
    idretail = None

    while True:
        ids = []

        idvenda = retail_id_from_model_data(venda, ivenda)
        idquebra = retail_id_from_model_data(quebra, iquebra)
        idruptura = retail_id_from_model_data(ruptura, iruptura)

        if idvenda is not None:
            ids.append(idvenda)
        if idquebra is not None:
            ids.append(idquebra)
        if idruptura is not None:
            ids.append(idruptura)

        if len(ids) == 0:
            if idretail is not None:
                efg.add(register, idretail)
            break

        minid = min(ids)

        if idretail is None:
            idretail = minid
        else:
            if idretail < minid:
                efg.add(register, idretail)
                idretail = None
                register = retail_mapping.create_empty_register()
                continue

        if idretail == idvenda:
            copy_independent_fields(register, venda[ivenda]['_source'])
            register[L.venda_bruta] = venda[ivenda]['_source'][L.venda_bruta]
            register[L.venda_liquida] = venda[ivenda]['_source'][L.venda_liquida]
            register[L.custo] = venda[ivenda]['_source'][L.custo]
            register[L.quantidade_vendida] = venda[ivenda]['_source'][L.quantidade]
            ivenda = ivenda + 1

        if idretail == idquebra:
            copy_independent_fields(register, quebra[iquebra]['_source'])
            register[L.importe_quebra] = ( register[L.importe_quebra] +
                quebra[iquebra]['_source'][L.importe] )
            iquebra = iquebra + 1

        if idretail == idruptura:
            copy_independent_fields(register, ruptura[iruptura]['_source'])
            register[L.ruptura] = ruptura[iruptura]['_source'][L.ruptura]
            register[L.perda] = ruptura[iruptura]['_source'][L.perda]
            iruptura = iruptura + 1

if len(sys.argv) == 1:
    read()
elif len(sys.argv) == 2:
    read(datetime.datetime.strptime(sys.argv[1],"%d.%m.%Y"))
elif len(sys.argv) == 3:
    data_desde = datetime.datetime.strptime(sys.argv[1],"%d.%m.%Y")
    data_ate = datetime.datetime.strptime(sys.argv[2],"%d.%m.%Y")
    for i in range((data_ate-data_desde).days+1):
        read(data_desde+TD(days=i))
