import barcode
from barcode.writer import ImageWriter

# Elegir formato Code 128 (acepta letras y números)
formato = barcode.get_barcode_class('code128')
codigo = formato("PRODUCTO-2026", writer=ImageWriter())

# Guarda la imagen automáticamente como 'mi_codigo.png'
codigo.save("mi_codigo") 

