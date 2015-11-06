#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import psycopg2
import sys
import datetime
import json
import tz

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
        "tienda": register[TIENDA],
        "dia": datetime.datetime.strptime(register[DIA],"%d.%m.%Y").replace(tzinfo=tz.brst).astimezone(tz.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "organizacion_venta": register[ORGANIZACION_VENTA],
        "organizacion_venta_descripcion": register[ORGANIZACION_VENTA_DESCRIPCION],
        "material": register[MATERIAL],
        "material_descripcion": register[MATERIAL_DESCRIPCION],
        "seccion": register[SECCION],
        "venta_bruta": float(register[VENTA_BRUTA].replace('.','').replace(',','.')),
        "venta_liquida": float(register[VENTA_LIQUIDA].replace('.','').replace(',','.')),
        "cantidad": float(register[CANTIDAD].replace('.','').replace(',','.')),
        "costo": float(register[COSTO].replace('.','').replace(',','.')),
        "porcentaje_margen": float(register[PORCENTAJE_MARGEN].replace('.','').replace(',','.'))/100,
        "impuestos": float(register[IMPUESTOS].replace('.','').replace(',','.')),
        })

def read(filename):

    command_line = {
        "index": {
            "_index":"ventas",
            "_type":"venta",
            "_id":None
        }}


    CANT_REGS_FILE=50000
    nreg=0
    fsalida=None

    with open(filename, 'r') as f:
        for line in f:

            if (nreg % CANT_REGS_FILE) == 0:
                nfile=nreg/CANT_REGS_FILE
                if fsalida is not None:
                    fsalida.close()
                fsalida=open("venta.%s.json" % str(nfile),"w")

            line = line.strip()
            line = line.decode("utf8","replace")
            try:
                venta = parse(line)
                matid = "%(tienda)s%(material)s" % venta
                command_line['index']['_id'] = "%s%s" % (matid, str(venta['dia']).replace('-',''))
                venta.update({"matid": matid})

                json.dump(command_line,fsalida)
                fsalida.write('\n')
                json.dump(venta,fsalida)
                fsalida.write('\n')

                nreg = nreg + 1


            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)
        if fsalida is not None:
            fsalida.close()

for f in sys.argv:
    read(f)
