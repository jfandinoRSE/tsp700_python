
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
        'INSERT INTO venta(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)',
        entities)

    con.commit()


def sql_print(con, pcheck):
    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM venta ORDER BY ROWID ASC LIMIT 1')

    rows = cursorObj.fetchall()
    try:
        for row in rows:
            print(row)
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


def main_tail():
    con = sqlite3.connect('coladata.db')
    i, df = sql_check_tail(con)
    if df != 1:
        i = + 1
    entities = (i, 'Andree', 800, 'IT', 'Tech', '2018-02-06')
    sql_table(con, entities)
    return i, con


def main_print():
    pchek = False
    i, con = main_tail()
    while not pchek:
        pchek = sql_print(con, pchek)
    sql_delete(con)

if __name__ == '__main__':
    main_print()

