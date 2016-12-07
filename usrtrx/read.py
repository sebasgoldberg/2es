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

def parse(line):
    register = line.split('\t')
    if len(register) < 6:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
    if register[0] == "Ano":
        raise NoDataRecordException(u"El registro de cabecera no es un registro de datos")
    if register[0] == "*":
        raise NoDataRecordException(u"El registro de totales no es un registro de datos")
    return ({"usuario": register[USUARIO],
        "transaccion": register[TRANSACCION],
        "pasos": float(register[PASOS].replace('.','').replace(',','.')),
        "fecha": datetime.date(int(register[ANO]),int(register[PERIODO]),15),})


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
                efg.add(usrtrx)

            except NoDataRecordException as e:
                print(e)
            #except Exception:
                #print(line)

for f in sys.argv:
    read(f)
