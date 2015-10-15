#!/usr/bin/python
from turtledemo.clock import hand

import psycopg2
from datetime import date
import math
import json

def top_variance(tienda, desde, hasta, cantidad_top, tipoCondicion=None):

    conn = psycopg2.connect("dbname='precios'")

    cur = conn.cursor()

    query = """select material, unidadMedida, avg(precio) as media,
            sqrt(abs(avg(precio*precio)- avg(precio)*avg(precio))) as varianza,
            CASE WHEN avg(precio) = 0 THEN 0 else sqrt(abs(avg(precio*precio)- avg(precio)*avg(precio))) / avg(precio) end as porcentaje
        from precio_dia
        where
            tienda = %(tienda)s and
            fecha >= %(desde)s and
            fecha <= %(hasta)s and
            precio > 0"""

    if tipoCondicion is not None:
        query = query + """ and tipoCondicion = %(tipoCondicion)s """

    query = query + """ group by material, unidadMedida
        order by porcentaje desc
        limit %(cantidad_top)s"""

    cur.execute(
        query,
        {'tienda':tienda,
         'desde':desde,
         'hasta':hasta,
         'cantidad_top':cantidad_top,
         'tipoCondicion':tipoCondicion})

    cur_desc = conn.cursor()
    cur_hist = conn.cursor()

    analisis = {
        "tienda": tienda,
        "desde": str(desde),
        "hasta": str(hasta),
        "cantidad_top": cantidad_top,
        "tipoCondicion": tipoCondicion,
        "variacionPrecio": [],
    }

    for register in cur:

        analisisMaterial = {}
        material, unidadMedida, media, desvio, indiceVariacion = register
        analisisMaterial['material'] = material
        analisisMaterial['unidadMedida'] = unidadMedida
        analisisMaterial['media'] = media
        analisisMaterial['desvio'] = desvio
        analisisMaterial['indiceVariacion'] = indiceVariacion
        analisisMaterial['precios'] = []
        cur_desc.execute(
            """select descripcion
            from materiales
            where material = %(material)s""",
            {'material':register[0]})
        analisisMaterial['descripcion'] = cur_desc.fetchone()[0].strip().encode("utf-8","ignore").decode()

        query = """
            select fecha, precio
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
            fecha, precio = hist
            analisisMaterial['precios'].append({
                "fecha": str(fecha),
                "precio": precio
            })

        analisis['variacionPrecio'].append(analisisMaterial)


    with open("Top %s desvio - %s - %s - %s - %s.json" % (cantidad_top, tienda, desde, hasta, tipoCondicion),"w",encoding="utf-8") as f:
        json.dump(analisis,f,indent=4, sort_keys=True)

# top_variance("B612", date(2015, 9, 5), date(2015, 10, 4), 10)