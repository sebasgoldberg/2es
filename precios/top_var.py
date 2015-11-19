#!/usr/bin/python
#encoding=utf8

import psycopg2
from datetime import date
from datetime import timedelta
import math
import json
from elasticsearch import Elasticsearch
import sys
import datetime
from els.lang import Lang
from bd.materiales import Materiales
from bd.secciones import Secciones
from els.utils import ElasticFilesGenerator

from venda import tz

#es = Elasticsearch('http://evoca:9200')

DESCRIPCION = 0
GRUPO_MERCADERIA = 1
DESCRIP_GRUPO_MERC = 2

L=Lang.get_instance()
materiales = Materiales()
secciones = Secciones()


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

        analisis[tienda][material][unidadMedida][L.media] = media
        analisis[tienda][material][unidadMedida][L.desvio] = desvio
        analisis[tienda][material][unidadMedida][L.indice_variacion] = indiceVariacion

    query = """
        select tienda, material, unidadMedida, fecha, precio, tipoCondicion, rankvartot, rankvarabs
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

    efg = ElasticFilesGenerator("precos", "venda", "precios-venta.%s" % iv_tienda)

    for reg in cur:

        tienda, material, unidadMedida, fecha, precio, tipoCondicionPrecioDia, rankvartot, rankvarabs = reg
        register = {
            L.loja: tienda.strip(),
            L.material: material,
            L.unidade_medida: unidadMedida.strip(),
            L.data: datetime.datetime(fecha.year,
                fecha.month,fecha.day,12).replace(tzinfo=tz.brst).astimezone(tz.utc).strftime("%Y-%m-%d %H:%M:%S"),
            L.preco: precio,
            L.tipo_condicao: tipoCondicionPrecioDia,
            L.rankvarabs: rankvarabs,
            L.rankvartot: rankvartot,
        }

        register[L.descricao_material] = materiales.get_descricao(material)
        register[L.secao] = materiales.get_seccion(register[L.material])
        register[L.descricao_secao] = secciones.get_descripcion(register[L.secao])

        try:
            register.update(analisis[tienda][material][unidadMedida])
        except KeyError:
            print "ERROR: Analisis material %s no encontrado" % material
            continue

        matid_com_um = "%s%s%s" % (register[L.loja],
            register[L.unidade_medida], register[L.material])
        register[L.matid_com_um] = matid_com_um

        matid = "%s%s" % (register[L.loja], register[L.material])
        register[L.matid] = matid

        efg.add(register, "%s%s" % (matid_com_um, str(register[L.data].split(' ')[0]).replace('-','')))


fecha_hasta = date(2015,11,12)
fecha_desde = fecha_hasta - timedelta(days=2)

tienda = None
if len(sys.argv) > 1:
  tienda = sys.argv[1]
top_variance(desde=fecha_desde, hasta=fecha_hasta, cantidad_top=99999999, toleranciaIndice=-1, iv_tienda=tienda)
