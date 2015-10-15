__author__ = 'JSGold'
import psycopg2
from datetime import date

def export(tienda, desde, hasta):

    with open("precos - %s - %s - %s.txt" % (tienda, desde, hasta), "w") as f:

        f.write("\t".join(["Loja", "Material", "UM", "Data", "PreCo", "Moeda", "Tipo de CondiCao"]))
        f.write("\n")

        conn = psycopg2.connect("dbname='precios'")

        cur = conn.cursor()

        cur.execute(
            """select *
            from precio_dia
            where
                tienda = %(tienda)s and
                fecha >= %(fechaDesde)s and
                fecha <= %(fechaHasta)s
            order by tienda, material, unidadmedida, fecha""",
                {"tienda": tienda,
                 "fechaDesde": desde,
                 "fechaHasta": hasta})

        for row in cur:
            f.write("\t".join("%s"%x for x in row))
            f.write("\n")

export("B514",date(2015, 9, 5),date(2015, 10, 4))