from abc import ABC, abstractmethod
from warehouse.domain.repositories.product_repository import ProductRepository
from warehouse.domain.product import Product
from warehouse.domain.services.barcode_generator import BarcodeGenerator

class InMemoryProductRepository(ProductRepository): #hereda de ABC

    # BarcodeGenerator se debería recibir por el constructor haciendo que "utilice" BarcodeGenerator y que no lo herede
    def __init__(self, barcode_generator: BarcodeGenerator):
        self._products = []
        self._next_id = 1
        self._barcode_generator = barcode_generator

    # Usar método obligatorio de ProductRepository
    def save(self, product: Product) -> None:
        product._assign_id(self._next_id)

        barcode = self._barcode_generator.generate(product.id)

        product._assign_barcode(barcode)
        
        self._products.append(product)
        self._next_id +=1


    # Usar método obligatorio de ProductRepository
    def find_by_barcode(self, barcode: str) -> Product | None:
        for product in self._products:
            if product.barcode == barcode:
                return product

        return None

    # Usar método obligatorio de ProductRepository
    def find_by_name(self, name: str) -> Product | None:
        for product in self._products:
            if product.name == name:
                return product

        # print("No se encontró el producto")
        return None

    def disable(self, product: Product) -> None:
        pass