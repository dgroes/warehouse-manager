from warehouse.domain.services.barcode_generator import BarcodeGenerator


class SimpleBarcodeGenerator(BarcodeGenerator):

    def generate(self, product_id: int) -> str:
        return str(product_id).zfill(10)