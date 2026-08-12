# PRODUCT_REPOSITORY ES EL CONTRATO 👈
from abc import ABC, abstractmethod

# from warehouse.domain import Product # <- Antes

# En este tipo de fichero es mejor que la arquitectura sea más explícita, 
# así se evita depender de lo que podría exponer desde domain/__init__.py
from warehouse.domain.product import Product  # <- ahora


class ProductRepository(ABC):  # Hereda de ABC

    @abstractmethod  # Obliga a implementar este método
    def save(self, product: Product) -> None:
        pass

    # C07: Optional
    @abstractmethod  # Obliga a implementar este método
    def find_by_barcode(self, barcode: str) -> Product | None:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Product | None:
        pass

    @abstractmethod
    def disable(self, barcode: str) -> Product | None:
        pass
