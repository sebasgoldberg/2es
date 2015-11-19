#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import psycopg2
import sys
import datetime
import json
import tz
from els.lang import Lang
from bd.materiales import Materiales
from bd.secciones import Secciones
from els.utils import ElasticFilesGenerator

L=Lang.get_instance()
materiales = Materiales()
secciones = Secciones()

#"";"";"";"";"";"";"";"Venda Bruta Atual";"Venda Líquida Atual";"Quantidade UMB Atual";"Custo Atual";"Margem Líquida Atual";"Impostos Totais"
#"Loja";"Dia";"Organização de Vendas";"Organização de Vendas";"Material";"Material";"[BI] Seçao";"BRL";"BRL";"";"BRL";"%";"BRL"
#"B503";"01.10.2015";"4002";"BR Bretas";"502";"CESTA BASICA MAXIMA 3";"CESTAS BASICA/NATALINA";"36";"26";"1";"35";"-35,3";"10"
TIENDA = 0
DIA = 1
ORGANIZACION_VENTA = 2
ORGANIZACION_VENTA_DESCRIPCION = 3
MATERIAL = 4
MATERIAL_DESCRIPCION = 5
SECCION = 6
VENTA_BRUTA = 7
VENTA_LIQUIDA = 8
CANTIDAD = 9
COSTO = 10
PORCENTAJE_MARGEN = 11
IMPUESTOS = 12

class NoDataRecordException(Exception):
    pass

def parse(line):
    register = line.split(';')
    if len(register) < 13:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
        register[i] = register[i].strip('#')
        register[i] = register[i].strip('"')
    if register[0] == "" or register[DIA] == '':
        raise NoDataRecordException(u"El registro de cabecera no es un registro de datos")
    if register[0] == "Loja":
        raise NoDataRecordException(u"El registro de totales no es un registro de datos")
    return ({
        L.loja: register[TIENDA],
        L.data: datetime.datetime.strptime(register[DIA],"%d.%m.%Y").replace(tzinfo=tz.brst).astimezone(tz.utc).strftime("%Y-%m-%d %H:%M:%S"),
        #"organizacion_register": register[ORGANIZACION_VENTA],
        #"organizacion_register_descripcion": register[ORGANIZACION_VENTA_DESCRIPCION],
        L.material: register[MATERIAL],
        L.descricao_material: register[MATERIAL_DESCRIPCION],
        L.secao: register[SECCION],
        L.venda_bruta: float(register[VENTA_BRUTA].replace('.','').replace(',','.')),
        L.venda_liquida: float(register[VENTA_LIQUIDA].replace('.','').replace(',','.')),
        L.quantidade: float(register[CANTIDAD].replace('.','').replace(',','.')),
        L.custo: float(register[COSTO].replace('.','').replace(',','.')),
        #"porcentaje_margen": float(register[PORCENTAJE_MARGEN].replace('.','').replace(',','.'))/100,
        #"impuestos": float(register[IMPUESTOS].replace('.','').replace(',','.')),
        })

INDEX = 'venda'
TYPE = 'venda'
FILE_NAME_PREFIX = 'venda'

def read(filename):

    efg = ElasticFilesGenerator(INDEX, TYPE, FILE_NAME_PREFIX)

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

                efg.add(register, "%s%s" % (matid, str(register[L.data]).replace('-','')))


            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv:
    read(f)
