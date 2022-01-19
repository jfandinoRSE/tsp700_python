from datetime import datetime

from jinja2 import Template

from linemode import open_printer
from linemode.renderers import xml

import sqlite3


def sql_check_tail(con):
    try:
        sql = 'SELECT * FROM venta'
        cursor = con.cursor()
        cursor.execute(sql)
        df = len(cursor.fetchall())
        if df >= 1:
            i = df
        else:
            i = 0
        return i, df
    except:
        i = 0
        df = 0
        return i, df


def sql_table(con, entities):
    try:
        sql = 'SELECT * FROM venta'
        cursor = con.cursor()
        cursor.execute(sql)
        df = len(cursor.fetchall())
    except:
        cursorObj = con.cursor()
        cursorObj.execute(
            "CREATE TABLE venta(id integer PRIMARY KEY, name text, salary real, department text, position text,"
            " hireDate text)")
        con.commit()

    cursorObj = con.cursor()

    cursorObj.execute(
        'INSERT INTO venta(id, name, last_name, amount, date_sell, box_office, sell_type, station, carrier_name )'
        ' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
        entities)

    con.commit()


def main_tail():
    con = sqlite3.connect('coladata.db')
    i, df = sql_check_tail(con)
    if df != 1:
        i = + 1
    entities = (i, 'Andree', 'perez', '10', 'Taquilla 2', datetime.now, 'debito', 'miranda', 'evelio')
    sql_table(con, entities)
    return i, con


def sql_print(con, pcheck):
    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM venta ORDER BY ROWID ASC LIMIT 1')

    rows = cursorObj.fetchall()
    try:
        # configurate port USB before use the printer
        printer = open_printer('star+lpt:///dev/usb/lp2')
        # jinja2 template
        template = """
        <document>
        <line>
            Datos de comprador
        </line>
            <line>
            {{rows}}
            </line>
        </document>
        """
        # line mode printer document
        document = Template(template).render(rows=str(rows))

        # iterator of generic printer instructions
        commands = xml.render(document)

        # printer specific compiled representation
        program = printer.compile(commands)

        printer.execute(program)

        pcheck = True
        return pcheck
    except:
        pcheck = False
        return pcheck


def sql_delete(con):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE FROM venta ORDER BY ROWID ASC LIMIT 1')

    con.commit()


def main_print():
    pchek = False
    con = sqlite3.connect('coladata.db')
    try:
        while not pchek:
            pchek = sql_print(con, pchek)
        sql_delete(con)

        if pchek:
            success = True
        return success
    except:
        success = False
        return success


def inf_client(data):
    if len(data) == 9:
        di1 = dict(Nombre=str(data[1]),
                   Apellido=str(data[2]),
                   Monto=str(data[3]),
                   Fecha=str(data[4]),
                   Taquilla=str(data[5]),
                   Tipo_de_venta=str(data[6]),
                   Estación=str(data[7]),
                   Operador=str(data[8])
                   )
    return di1


