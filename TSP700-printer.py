from escpos.printer import Usb


""" Seiko Epson Corp. Receipt Printer (STAR TSP700) """
p = Usb(0x0519, 0x0001)
p.text("Hello World\n")
#p.image("logo.gif")
p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
p.cut()
