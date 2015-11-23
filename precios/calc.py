#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

"""
                            f1  f2  f3 ...
tienda, material, unidad:   p1  p2  p3
"""

import psycopg2
import sys
from datetime import timedelta as TD
from datetime import date
from math import log

conn = psycopg2.connect("dbname='precios'") 

prioridadesTipoCondicion = {}
prioridadesTipoCondicion["ZPRI"] = 10
prioridadesTipoCondicion["ZKA0"] = 20
prioridadesTipoCondicion["ZKPC"] = 30
prioridadesTipoCondicion["ZKP0"] = 40

TIPO_CONDICION = 0
MATERIAL = 1
MATERIAL_PADRE = 2
FECHA_DESDE = 3
FECHA_HASTA = 4
UNIDAD = 5
TIENDA = 6
PRECIO = 7
MONEDA = 8

precios={}

class PrecioPadreNoAplica(Exception):
    pass

def mayorPrioridadPrimerTipoCondicion(tc1, tc2):
    return prioridadesTipoCondicion[tc1] < prioridadesTipoCondicion[tc2]

def calc_fecha_hijo(row, fecha):

    material = row[MATERIAL]
    materialPadre = row[MATERIAL_PADRE]
    tienda = row[TIENDA]
    unidad = row[UNIDAD]
    tipoCondicion = row[TIPO_CONDICION]
    precio = row[PRECIO]
    moneda = row[MONEDA]

    try:

        tipoCondicionPadre, precioPadre, monedaPadre = precios[tienda][materialPadre][unidad][fecha]

        # En caso que el tipo de condición del hijo, tenga mayor prioridad que el padre,
        # no debería tomarse el precio del padre.
        if mayorPrioridadPrimerTipoCondicion(tipoCondicion, tipoCondicionPadre):
            raise PrecioPadreNoAplica

        precios[tienda][material][unidad][fecha] = (tipoCondicionPadre, precioPadre, monedaPadre)

    except KeyError:

        # En caso que todavía no exista el padre:
        raise PrecioPadreNoAplica

def calc_fecha(row, fecha):

    material = row[MATERIAL]
    materialPadre = row[MATERIAL_PADRE]

    if material != materialPadre:
        try:
            calc_fecha_hijo(row, fecha)
        except PrecioPadreNoAplica:
            pass

    tienda = row[TIENDA]
    unidad = row[UNIDAD]
    tipoCondicion = row[TIPO_CONDICION]
    precio = row[PRECIO]
    moneda = row[MONEDA]


    try:

        tipoCondicionExistente, precioExistente, monedaExistente = precios[tienda][material][unidad][fecha]

        if mayorPrioridadPrimerTipoCondicion(tipoCondicionExistente, tipoCondicion):
            return

        if precioExistente <= precio:
            return

    except KeyError:

        if tienda not in precios:
            precios[tienda] = {}
        if material not in precios[tienda]:
            precios[tienda][material] = {}
        if unidad not in precios[tienda][material]:
            precios[tienda][material][unidad] = {}

    precios[tienda][material][unidad][fecha] = (tipoCondicion, precio, moneda)

def calc(desde, hasta, iv_tienda=None):

    # Dos pasadas para tener los padres y luego poder calcular hijos
    for i in range(2):

        cur = conn.cursor()

        query = """select *
            from condicionesMateriales
            where
                validoDesde <= %(fechaHasta)s and
                validoHasta >= %(fechaDesde)s"""

        if iv_tienda is not None:
            query = query + """ and tienda = %(tienda)s """

        cur.execute(query,
                {"fechaDesde": desde,
                    "fechaHasta": hasta,
                    "tienda":iv_tienda})

        for row in cur:
            # Se obtiene la fecha desde que sea mayor.
            fi = max(desde, row[FECHA_DESDE])

            # Se obtiene la fecha hasta que sea menor
            ff = min(hasta, row[FECHA_HASTA])

            # Será guardado el precio para el periodo comprendido
            # entre las fechas fi y ff utilizando la información de
            # la condición en row, siempre y cuando no exista un
            # precio con mayor prioridad.
            fecha = fi
            while fecha <= ff:
                calc_fecha(row, fecha)
                fecha = fecha + TD(days=1)

    cur = conn.cursor()

    for tienda, materiales in precios.items():
        for material, unidades in materiales.items():
            for unidad, fechas in unidades.items():
                for fecha, (tipoCondicion, importe, moneda) in fechas.items():

                    fecha_anterior = fecha - TD(days=1)

                    rankvartot = 0
                    rankvarabs = 0

                    if fecha_anterior in fechas:
                        _ ,  importeAnterior, _ = fechas[fecha_anterior]
                        if importeAnterior <> 0 and importe <> 0:
                            variacion = importe - importeAnterior
                            indice = 1 + variacion / float(importeAnterior)
                            rankvartot = log(indice,2)
                            rankvarabs = abs(rankvartot)
                    
                    cur.execute(
                        """
                        select tienda
                        from precio_dia
                        where
                            tienda = %(tienda)s and
                            material = %(material)s and
                            unidadMedida = %(unidadMedida)s and
                            fecha = %(fecha)s
                            """,{
                            "tienda": tienda,
                            "material": material,
                            "unidadMedida": unidad,
                            "fecha": fecha,
                            })

                    rows = cur.fetchall()

                    if len(rows) == 0:
                        cur.execute(
                            """insert into precio_dia
                                (tienda, material, unidadMedida, fecha, tipoCondicion, precio, moneda, rankvartot, rankvarabs)
                                values
                                (%(tienda)s, %(material)s, %(unidadMedida)s, %(fecha)s, %(tipoCondicion)s, %(precio)s, %(moneda)s, %(rankvartot)s, %(rankvarabs)s)""",
                            {"tienda": tienda,
                                "material": material,
                                "unidadMedida": unidad,
                                "fecha": fecha,
                                "tipoCondicion": tipoCondicion,
                                "precio": importe,
                                "moneda": moneda,
                                "rankvarabs": rankvarabs,
                                "rankvartot": rankvartot})
                    else:
                        cur.execute(
                            """update precio_dia
                               set
                                tipoCondicion = %(tipoCondicion)s,
                                precio = %(precio)s,
                                moneda = %(moneda)s,
                                rankvartot = %(rankvartot)s,
                                rankvarabs = %(rankvarabs)s
                                where
                                    tienda = %(tienda)s and
                                    material = %(material)s and
                                    unidadMedida = %(unidadMedida)s and
                                    fecha = %(fecha)s
                            """,
                            {"tienda": tienda,
                                "material": material,
                                "unidadMedida": unidad,
                                "fecha": fecha,
                                "tipoCondicion": tipoCondicion,
                                "precio": importe,
                                "moneda": moneda,
                                "rankvarabs": rankvarabs,
                                "rankvartot": rankvartot})

                    conn.commit()

fecha_hasta = date(2015,11,23)
fecha_desde = fecha_hasta - TD(days=5)
fecha_desde = date(2015,07,01)

if len(sys.argv) > 1:
  for tienda in sys.argv[1:]:
    precios={}
    calc(fecha_desde, fecha_hasta, iv_tienda=tienda)
else:
    calc(fecha_desde, fecha_hasta)

