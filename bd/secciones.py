#!/usr/bin/python
#encoding=utf8

import psycopg2

class Secciones:

    instance = None

    @staticmethod
    def get_instance():
        if Secciones.instance is None:
            Secciones.instance = Secciones()
        return Secciones.instance

    def __init__(self):

        conn = psycopg2.connect("dbname='precios'")

        cur = conn.cursor()

        cur.execute(
            """select seccion, descripcion
            from secciones""")

        self.secciones = {}
        for reg in cur:
            seccion, descripcion = reg
            if descripcion[:6] == 'SECAO ':
                self.secciones[seccion] = descripcion[6:]
            else:
                self.secciones[seccion] = descripcion

    def get_descripcion(self, seccion):
        
        if seccion in self.secciones:
            return self.secciones[seccion]
        return 'NA'
