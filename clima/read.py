#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys

sys.path.append('./')
from els.utils import ElasticFilesGenerator

#Visão	Conceito	Item	Evaluação	Benchmark LATAM 2015
PAIS = 0
VISAO = 1
CONCEITO = 2
ITEM = 3
EVALUACAO = 4
BENCHMARK = 5
ANO = 6

class NoDataRecordException(Exception):
    pass

def get_float(value):
    if value == '':
        return None
    return float(value.replace('.','').replace(',','.'))

def parse(line):
    register = line.split('\t')
    if len(register) < 6:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
    return ({
        'pais': register[PAIS],
        'visao': register[VISAO],
        'conceito': register[CONCEITO],
        'item': register[ITEM],
        'evaluacao': get_float(register[EVALUACAO]),
        'benchmark': get_float(register[BENCHMARK]),
        'ano': int(register[ANO]),
        })

def read(filename):

    lineNum = 0
    efg = ElasticFilesGenerator("clima","clima","clima")

    with open(filename, 'r') as f:
        for line in f:
            lineNum = lineNum + 1
            if lineNum < 2:
                continue

            line = line.strip()
            try:
                clima = parse(line)
                efg.add(clima,'%(ano)s-%(pais)s-%(visao)s-%(conceito)s-%(item)s' % clima)

            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv[1:]:
    read(f)
