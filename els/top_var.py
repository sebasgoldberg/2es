#!/usr/bin/python
#encoding=utf8

import psycopg2
from datetime import date
from datetime import timedelta
import math
import json
from elasticsearch import Elasticsearch

#es = Elasticsearch('http://evoca:9200')

def top_variance(desde=date.today()-timedelta(days=30),hasta=date.today(), cantidad_top=9999999, tipoCondicion=None, toleranciaIndice=2):

    with open("top%s-tol%s-precios-venta.json"%(cantidad_top, toleranciaIndice),"w") as f:

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

        query = query + """ group by tienda, material, unidadMedida
            order by porcentaje desc
            limit %(cantidad_top)s"""

        cur.execute(
            query,
            {
             'cantidad_top':cantidad_top,
             'tipoCondicion':tipoCondicion})

        cur_desc = conn.cursor()
        cur_hist = conn.cursor()

        for register in cur:

            analisisMaterial = {}
            tienda, material, unidadMedida, media, desvio, indiceVariacion = register
            if indiceVariacion <= toleranciaIndice:
                continue

            analisisMaterial.update({"tienda": tienda.strip()})
            analisisMaterial['material'] = material
            analisisMaterial['unidadMedida'] = unidadMedida.strip()
            analisisMaterial['media'] = media
            analisisMaterial['desvio'] = desvio
            analisisMaterial['indiceVariacion'] = indiceVariacion

            cur_desc.execute(
                """select descripcion
                from materiales
                where material = %(material)s""",
                {'material':material})
            analisisMaterial['descripcion'] = cur_desc.fetchone()[0].strip().encode("utf-8","ignore").decode()

            query = """
                select fecha, precio, tipoCondicion
                from precio_dia
                where
                    tienda = %(tienda)s and
                    material = %(material)s and
                    unidadMedida = %(unidadMedida)s and
                    fecha >= %(desde)s and
                    fecha <= %(hasta)s and
                    precio > 0
                """

            if tipoCondicion is not None:
                query = query + """ and tipoCondicion = %(tipoCondicion)s """

            query = query + """ order by fecha """

            cur_hist.execute(query,
                             {'tienda':tienda,
                              'desde':desde,
                              'hasta':hasta,
                              'material': material,
                              'unidadMedida': unidadMedida,
                              'tipoCondicion':tipoCondicion})

            for hist in cur_hist:
                fecha, precio, tipoCondicionPrecioDia = hist
                analisisMaterial.update({
                    "fecha": str(fecha),
                    "precio": precio,
                    "tipoCondicion": tipoCondicionPrecioDia,
                })

                matid = "%(tienda)s%(unidadMedida)s%(material)s" % analisisMaterial

                command_line['index']['_id'] = "%s%s" % (matid, str(analisisMaterial['fecha']).replace('-',''))
                analisisMaterial.update({"matid": matid})

                json.dump(command_line,f)
                f.write('\n')
                json.dump(analisisMaterial,f)
                f.write('\n')

                #res = es.index(index="precios", doc_type='venta', body=analisisMaterial)

top_variance(cantidad_top=500, toleranciaIndice=4)
