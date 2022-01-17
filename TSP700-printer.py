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

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrintCola, cls).__new__(cls)
            cls._instance._load_config()

        return cls._instance

    def _load_config(self):
        pass

    def sql_table(con, entities):
        df = pd.read_sql_query("SELECT * from coladata", con)

        if len(df) is None:
            cursorObj = con.cursor()

            cursorObj.execute(
                'INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)',
                entities)

            con.commit()

    entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')

    sql_table(con, entities)

    def print(self,data):
        printer = open_printer('/dev/usb/lp0')
        #jinja2 template
        template = """
        <document>
          <line>
          {{data}}
          Prueba de impresión 
          </line>
        </document>
        """
        # line mode printer document
        document = Template(template).render()

        # iterator of generic printer instructions
        commands = xml.render(document)

        # printer specific compiled representation
        program = printer.compile(commands)

        printer.execute(program)
