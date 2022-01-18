"""from escpos.constants import GS, _CUT_PAPER, PAPER_FULL_CUT
from escpos.printer import Usb
import six



p = Usb(0x0519, 0x0001)
#p.text("Hello World OLA QU\n")
#p._raw(chr(29)+chr(86)+chr(00)+chr(48))
#print(chr(29)+chr(86)+chr(00)+chr(48))
#p.write(b'\x1D'+b'\x56')
#p._raw(GS + b'V' + six.int2byte(66) + b'\x00')
#PAPER_FULL_CUT
#CUT_PAPER = lambda m: GS + b'V' + b'\x00'
p.cut('PART')
print('\x1d'+'\x56'+'\x00')
#print(chr())
"""


from jinja2 import Template

from linemode import open_printer
from linemode.renderers import xml

import sqlite3
import pandas as pd



class PrintCola:
    con = sqlite3.connect('coladata.db')
    _instance = None
    pchek = False
    try:
        df = pd.read_sql_query("SELECT * from employees", con)
        if df > 1:
            i = df
        else:
            i = 0
    except:
        i = 0
        pass
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrintCola, cls).__new__(cls)
            cls._instance._load_config()

        return cls._instance

    def _load_config(self):
        pass

    def sql_table(con, entities, i):
        try:
            df = pd.read_sql_query("SELECT * from employees", con)
        except:

            cursorObj = con.cursor()
            cursorObj.execute(
                "CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")
            con.commit()
            df = pd.read_sql_query("SELECT * from employees", con)


        cursorObj = con.cursor()
        i =+ 1
        cursorObj.execute(
            'INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)',
            entities)

        con.commit()
        return i

    entities = (i+1, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')

    i = sql_table(con, entities, i)
    print(str(i))
    def sql_print(con, pcheck, i):
        cursorObj = con.cursor()

        cursorObj.execute('SELECT * FROM employees WHERE id==?', str(i))

        rows = cursorObj.fetchall()
        try:
            for row in rows:
                print(row)
            pcheck=True
        except:
            pcheck=False
        return pcheck
#        printer = open_printer('/dev/usb/lp0')
#        #jinja2 template
#        template = """
#        <document>
#          <line>
#          {{data}}
#          Prueba de impresión
#          </line>
#        </document>
#        """
#        # line mode printer document
#        document = Template(template).render()

#        # iterator of generic printer instructions
#        commands = xml.render(document)

#        # printer specific compiled representation
 #       program = printer.compile(commands)

#        printer.execute(program)
    def sql_delete(con, i):
        cursorObj = con.cursor()

        cursorObj.execute('DELETE FROM employees WHERE id == ?', str(i))

        con.commit()
        return i-1


    while pchek==False:
        pchek=sql_print(con, pchek, i)
    i=sql_delete(con, i)


