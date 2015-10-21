#!/usr/bin/python
#encoding=utf8

import psycopg2
from datetime import date
from datetime import timedelta
import math
import json
from elasticsearch import Elasticsearch
import sys

#es = Elasticsearch('http://evoca:9200')

def top_variance(desde=date.today()-timedelta(days=30),hasta=date.today(), cantidad_top=9999999, tipoCondicion=None, toleranciaIndice=2, iv_tienda=None):

    command_line = {
        "index": {
            "_index":"precios",
            "_type":"venta",
            "_id":None
        }}

    conn = psycopg2.connect("dbname='precios'")

    cur = conn.cursor()

    query = """select tienda, material, unidadMedida, avg(precio) as media,
            sqrt(abs(avg(precio*precio)- avg(precio)*avg(precio))) as varianza,
            CASE WHEN avg(precio) = 0 THEN 0 else sqrt(abs(avg(precio*precio)- avg(precio)*avg(precio))) * 100 / avg(precio) end as porcentaje
        from precio_dia
        where
            precio > 0"""

    if tipoCondicion is not None:
        query = query + """ and tipoCondicion = %(tipoCondicion)s """

    if iv_tienda is not None:
        query = query + """ and tienda = %(tienda)s """

    query = query + """ group by tienda, material, unidadMedida
        limit %(cantidad_top)s"""

    cur.execute(
        query,
        {
         'cantidad_top':cantidad_top,
         'tipoCondicion':tipoCondicion,
         'tienda': iv_tienda})

    analisis = {}

    for register in cur:

        tienda, material, unidadMedida, media, desvio, indiceVariacion = register

        if indiceVariacion <= toleranciaIndice:
            continue

        if tienda not in analisis:
            analisis[tienda] = {}
        if material not in analisis[tienda]:
            analisis[tienda][material] = {}
        if unidadMedida not in analisis[tienda][material]:
            analisis[tienda][material][unidadMedida] = {}

        analisis[tienda][material][unidadMedida]['media'] = media
        analisis[tienda][material][unidadMedida]['desvio'] = desvio
        analisis[tienda][material][unidadMedida]['indiceVariacion'] = indiceVariacion

    cur.execute(
        """select material, descripcion
        from materiales """)

    descripciones = {}
    for reg in cur:
        material, descripcion = reg
        descripciones[material] = descripcion


    query = """
        select tienda, material, unidadMedida, fecha, precio, tipoCondicion
        from precio_dia
        where
            fecha >= %(desde)s and
            fecha <= %(hasta)s and
            precio > 0
        """

    if tipoCondicion is not None:
        query = query + """ and tipoCondicion = %(tipoCondicion)s """

    if iv_tienda is not None:
        query = query + """ and tienda = %(tienda)s """

    cur.execute(query,
                     { 'desde':desde,
                      'hasta':hasta,
                      'tipoCondicion':tipoCondicion,
                      'tienda':iv_tienda})

    CANT_REGS_FILE=100000
    nreg=0
    f=None

    for reg in cur:

        if (nreg % CANT_REGS_FILE) == 0:
            nfile=nreg/CANT_REGS_FILE
            if f is not None:
                f.close()
            f=open("precios-venta.%s.%s.json" % (iv_tienda, str(nfile)),"w")

        tienda, material, unidadMedida, fecha, precio, tipoCondicionPrecioDia = reg
        analisisMaterial = {
            "tienda": tienda.strip(),
            "material": material,
            "unidadMedida": unidadMedida.strip(),
            "fecha": str(fecha),
            "precio": precio,
            "tipoCondicion": tipoCondicionPrecioDia,
        }

        try:
            analisisMaterial.update({
                "descripcion": descripciones[material].strip(),
                })
        except KeyError:
            print "ERROR: Descripcion material %s no encontrado" % material
            continue

        try:
            analisisMaterial.update(analisis[tienda][material][unidadMedida])
        except KeyError:
            print "ERROR: Analisis material %s no encontrado" % material
            continue

        matid = "%(tienda)s%(unidadMedida)s%(material)s" % analisisMaterial

        command_line['index']['_id'] = "%s%s" % (matid, str(analisisMaterial['fecha']).replace('-',''))
        analisisMaterial.update({"matid": matid})

        json.dump(command_line,f)
        f.write('\n')
        json.dump(analisisMaterial,f)
        f.write('\n')

        nreg = nreg + 1

tienda = None
if len(sys.argv) > 1:
  tienda = sys.argv[1]
top_variance(cantidad_top=99999999, toleranciaIndice=-1, iv_tienda=tienda)
