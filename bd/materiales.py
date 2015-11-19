#!/usr/bin/python
#encoding=utf8

import psycopg2

DESCRIPCION = 0
GRUPO_MERCADERIA = 1

class Materiales:

    instance = None

    @staticmethod
    def get_instance():
        if Materiales.instance is None:
            Materiales.instance = Materiales()
        return Materiales.instance

    def __init__(self):

        conn = psycopg2.connect("dbname='precios'")

        cur = conn.cursor()

        cur.execute(
            """select material, descripcion, grupoMercaderia
            from materiales""")

        self.materiales = {}
        for reg in cur:
            material, descripcion, grupoMercaderia = reg
            self.materiales[material] = (descripcion, grupoMercaderia)

    def get_seccion(self, material):
        material = int(material)
        
        if material in self.materiales:
            return self.materiales[material][GRUPO_MERCADERIA][0:2]
        else:
            return 'NA'

    def get_descricao(self, material):
        material = int(material)
        
        if material in self.materiales:
            return self.materiales[material][DESCRIPCION].strip()
        else:
            return 'NA'
