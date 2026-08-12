import random
from warehouse.domain.services.barcode_generator import BarcodeGenerator


class RandomBarcodeGenerator(BarcodeGenerator):

    def generate(self) -> str:
        number = random.randint(1, 9999999999)

        # Si sale un número pequeño (ejemplo: 43) que se formatee con ceros
        barcode = f"{number:010}"
        # return "1234567890" #<- TEST
        
        return barcode