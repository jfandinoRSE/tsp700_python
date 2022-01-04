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

printer = open_printer('USB\VID_0483&PID_5720\11101800002')

# jinja2 template
template = """
<document>
  <line>
    MARICO EL QUE LO LEA
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