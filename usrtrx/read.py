#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys
import json

ANO = 0
PERIODO = 1
USUARIO = 2
TRANSACCION = 3
PASOS = 4
            

class ElasticFilesGenerator:

    def __init__(self, iv_index, iv_type, iv_file_name_prefix):

        self.command_line = {
            "index": {
                "_index": iv_index,
                "_type": iv_type,
            }}

 
        self.CANT_REGS_FILE=50000
        self.nreg=0
        self.fsalida=None
        self.file_name_prefix = iv_file_name_prefix

    def __del__(self):
        if self.fsalida is not None:
            self.fsalida.close()
   
    def add(self, iv_object, iv_id=None):

        if (self.nreg % self.CANT_REGS_FILE) == 0:
            nfile = self.nreg / self.CANT_REGS_FILE
            if self.fsalida is not None:
                self.fsalida.close()
            self.fsalida = open("%s.%s.json" % (self.file_name_prefix, str(nfile)),"w")

        if iv_id is not None:
            command_line['index'].update({ '_id': iv_id })

        json.dump(self.command_line, self.fsalida)
        self.fsalida.write('\n')
        json.dump(iv_object, self.fsalida)
        self.fsalida.write('\n')

        self.nreg = self.nreg + 1


class NoDataRecordException(Exception):
    pass


def parse(line):
    register = line.split('|')
    if len(register) <= 3:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    register = register[1:-1]
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
            if lineNum <= 5:
                continue

            line = line.strip()
            line = line.decode("utf8","replace")
            try:
                usrtrx = parse(line)
                usrtrx['fecha'] = str(usrtrx['fecha'])
                efg.add(usrtrx)

            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv:
    read(f)
