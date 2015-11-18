#!/usr/bin/python
import psycopg2
import sys
import datetime

def clear():
    conn = psycopg2.connect("dbname='precios'")

    cur = conn.cursor()

    cur.execute("delete from condicionesMateriales")

    cur.execute("delete from precio_dia")

    cur.execute("delete from materiales")

    conn.commit()



clear()
