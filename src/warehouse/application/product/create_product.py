from warehouse.domain.repositories.product_repository import ProductRepository
from warehouse.domain.category import Category
from warehouse.domain.services.barcode_generator import BarcodeGenerator 

# CreateProduct debería pedirle al repositorio que guarde el producto.
class CreateProduct:
    def __init__(
            self, 
            repository: ProductRepository,
            barcode_generator: BarcodeGenerator):
            self._repository = repository
            self._barcode_generator = barcode_generator

    def execute(
            self,
            name: str,
            category: Category
        ):
        pass

    