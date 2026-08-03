from abc import ABC, abstractmethod
from warehouse.domain import Product

class ProductRepository(ABC): #Hereda de ABC

    @abstractmethod # Obliga a implementar este método
    def save(self, product: Product) -> None:
        pass

    # C07: Optional
    @abstractmethod # Obliga a implementar este método
    def find_by_barcode(self, barcode: str) -> Product | None:
        pass

    @abstractmethod
    def find_by_name(self, product: Product) -> None | None:
        pass

    @abstractmethod
    def disable(self, product: Product) -> None:
        pass