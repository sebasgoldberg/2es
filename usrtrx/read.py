#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys

ANO = 0
PERIODO = 1
USUARIO = 2
TRANSACCION = 3
PASOS = 4
            
sys.path.append('./')
from els.utils import ElasticFilesGenerator

class NoDataRecordException(Exception):
    pass

class FixedWidthLineToShortException(Exception):
    pass

#2015 04 ZVCOSTA      RFC                                     |       177|         0
FIELDS_LENGTHS = (4, 2, 12, 40, 10, 10)
LENGTH_TO_IGNORE_BETW_FIELDS = 1

def from_fixed_width(line, lengths, ignore_between=0):

    if len(lengths) == 0:
        return []

    total_length = sum(lengths) + (len(lengths)-1)*ignore_between

    if len(line) < total_length:
        raise FixedWidthLineToShortException(u'Line to short.')

    idx_from = 0
    idx_to = lengths[0]
    fields = []
    fields.append(line[idx_from:idx_to])

    for i in lengths[1:]:
        idx_from = idx_to + ignore_between
        idx_to = idx_from + i
        fields.append(line[idx_from:idx_to])

    return fields


def parse(line):
    #register = line.split('\t')
    register = from_fixed_width(line, FIELDS_LENGTHS, LENGTH_TO_IGNORE_BETW_FIELDS)
    if len(register) < 6:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
    if register[0].lower() in  ["ano", 'gjah', '----']:
        raise NoDataRecordException(u"El registro de cabecera no es un registro de datos")
    if register[0] == "*":
        raise NoDataRecordException(u"El registro de totales no es un registro de datos")
    return ({"usuario": register[USUARIO],
        "transaccion": register[TRANSACCION],
        "pasos": float(register[PASOS].replace('.','').replace(',','.')),
        "fecha": datetime.datetime(int(register[ANO]),int(register[PERIODO]),15,12),})


def read(filename):

    lineNum = 0
    efg = ElasticFilesGenerator("usrtrx","usrtrx","usrtrx")

    with open(filename, 'r') as f:
        for line in f:
            lineNum = lineNum + 1

            line = line.strip()
            line = line.decode("utf8","replace")
            try:
                usrtrx = parse(line)
                usrtrx['fecha'] = str(usrtrx['fecha'])
                efg.add(usrtrx,'%(fecha)s-%(transaccion)s-%(usuario)s' % usrtrx)

            except FixedWidthLineToShortException as e:
                print('%s: %s' % (e, line) )
            except NoDataRecordException as e:
                print(e)
            #except Exception:
                #print(line)

for f in sys.argv[1:]:
    read(f)
