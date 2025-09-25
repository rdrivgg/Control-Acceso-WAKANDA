import barcode
from barcode.writer import ImageWriter
import uuid
import os

class BarcodeManager:
    def __init__(self):
        self.barcode_folder = "barcodes"
        if not os.path.exists(self.barcode_folder):
            os.makedirs(self.barcode_folder)
    
    def generar_codigo_barras(self, nombre, apellido):
        codigo_unico = f"{uuid.uuid4().hex[:10].upper()}"
        
        CODE128 = barcode.get_barcode_class('code128')
        codigo_barras = CODE128(codigo_unico, writer=ImageWriter())
        
        filename = f"{self.barcode_folder}/{codigo_unico}_{nombre}_{apellido}"
        codigo_barras.save(filename)
        
        return codigo_unico, f"{filename}.png"
    
    def validar_codigo_barras(self, barcode_data):
        try:
            barcode_data = barcode_data.strip()
            if len(barcode_data) == 10 and barcode_data.isalnum():
                return {
                    'codigo': barcode_data.upper(),
                    'valido': True
                }
            else:
                return {'valido': False, 'error': 'Código de barras no válido'}
        except Exception as e:
            return {'valido': False, 'error': f'Error al procesar código de barras: {str(e)}'}