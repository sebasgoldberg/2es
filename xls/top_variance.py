#!/usr/bin/python
from turtledemo.clock import hand

import psycopg2
from datetime import date
import math

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

    with open("Top %s desvio - %s - %s - %s - %s.xls" % (cantidad_top, tienda, desde, hasta, tipoCondicion),"w",encoding="utf-8") as f:
        print("\t".join(["material", "descricao", "UM", "media", "variacao", "indice variacao"]),file=f)
        for register in cur:
            cur_desc.execute(
                """select descripcion
                from materiales
                where material = %(material)s""",
                {'material':register[0]})
            descripcion=cur_desc.fetchone()[0].strip().encode("utf-8","ignore").decode()
            linea = [str(x).replace('.',',') for x in [register[0], descripcion, register[1], register[2], register[3], register[4]]]
            print(u"\t".join(linea),file=f)

top_variance("B503", date(2015, 9, 5), date(2015, 10, 10), 99999)
