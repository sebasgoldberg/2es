#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys
import ntpath

NOME_USUARIO = 0
ESTADO_ANTIVIRUS = 1
NOME_MAQUINA = 2
MAC_ADDRESS = 3
USUARIO_RED = 4


INDEX = 'mac'
TYPE = 'mac'
FILE_NAME_PREFIX = 'mac'

sys.path.append('./')
from els.utils import ElasticFilesGenerator

class NoDataRecordException(Exception):
    pass

def parse(line):
    register = line.split('\t')
    if len(register) < 5:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
    return ({"nome_usuario": register[NOME_USUARIO],
        "estado_antivirus": register[ESTADO_ANTIVIRUS],
        "nome_maquina": register[NOME_MAQUINA],
        "mac_address": register[MAC_ADDRESS],
        "usuario_red": register[USUARIO_RED], })


def read(filename):

    lineNum = 0
    efg = ElasticFilesGenerator(INDEX, TYPE, FILE_NAME_PREFIX)

    with open(filename, 'r') as f:
        for line in f:
            lineNum = lineNum + 1
            if lineNum <= 1:
                continue

            line = line.strip()
            line = line.decode("utf8","replace")
            try:
                register = parse(line)
                efg.add(register, register['mac_address'])

            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv[1:]:
    read(f)
