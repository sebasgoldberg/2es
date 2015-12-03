#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import psycopg2
import sys
import datetime
import json
from els.lang import Lang
from bd.materiales import Materiales
from bd.secciones import Secciones
from els.utils import ElasticFilesGenerator

L=Lang.get_instance()
materiales = Materiales()
secciones = Secciones()

#"";"";"";"";"";"";"";"Estoque";"Estoque UMB";"Quantidade de Estoque"
#"Loja";"Loja";"Dia";"Material";"Material";"Tipo Movimento";"";"BRL";"";""
#"B612";"B612 CESARIO ALVIM";"02.07.2015";"273874";"CREME DENT COLGATE TOTAL MINT 90G";"Z21";"Z21";"-3,85";"-1 UN";"-1,00"
TIENDA = 0
TIENDA_DESCRIPCION = 1
DIA = 2
MATERIAL = 3
MATERIAL_DESCRIPCION = 4
TIPO_MOVIMIENTO = 5
TIPO_MOVIMIENTO_DESCRIPCION = 6
IMPORTE = 7
CANTIDAD_Y_UN = 8
CANTIDAD = 9

class NoDataRecordException(Exception):
    pass

def parse(line):
    register = line.split(';')
    if len(register) < 10:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
        register[i] = register[i].strip('#')
        register[i] = register[i].strip('"')
    if register[0] == "" or register[DIA] == '':
        raise NoDataRecordException(u"El registro de cabecera no es un registro de datos")
    if register[0] == "Loja":
        raise NoDataRecordException(u"El registro de totales no es un registro de datos")
    cantidad, unidad_medida = register[CANTIDAD_Y_UN].split(' ')
    return ({
        L.loja: register[TIENDA],
        L.data: datetime.datetime.strptime(register[DIA],"%d.%m.%Y").replace(hour=12).strftime("%Y-%m-%d %H:%M:%S"),
        L.material: register[MATERIAL],
        L.descricao_material: register[MATERIAL_DESCRIPCION],
        L.tipo_movimento: register[TIPO_MOVIMIENTO],
        L.importe: float(register[IMPORTE].replace('.','').replace(',','.')),
        L.quantidade: float(cantidad.replace('.','').replace(',','.')),
        L.unidade_medida:unidad_medida, 
        })

INDEX = 'quebra'
TYPE = 'quebra'

def read(filename):

    efg = ElasticFilesGenerator(INDEX, TYPE, filename)

    with open(filename, 'r') as f:
        for line in f:

            line = line.strip()
            line = line.decode("utf8","replace")

            try:
                register = parse(line)
                register[L.secao] = materiales.get_seccion(register[L.material])
                register[L.descricao_secao] = secciones.get_descripcion(register[L.secao])
                matid = "%s%s" % (register[L.loja], register[L.material])
                register.update({L.matid: matid})

                efg.add(register, "%s%s%s" % (matid, register[L.tipo_movimento], str(register[L.data][0:10]).replace('-','')))


            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv[1:]:
    read(f)
