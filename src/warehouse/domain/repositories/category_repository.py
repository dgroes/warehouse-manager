# PRODUCT_REPOSITORY ES EL CONTRATO 👈
from abc import ABC, abstractmethod

# from warehouse.domain import Category # <- Antes

# En este tipo de fichero es mejor que la arquitectura sea más explícita, 
# así se evita depender de lo que podría exponer desde domain/__init__.py
from warehouse.domain.category import Category  # <- ahora


class CategoryRepository(ABC):  # Hereda de ABC

    @abstractmethod  # Obliga a implementar este método
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod  # Obliga a implementar este método
    def find_by_id(self, category_id: int) -> Category | None:
        pass


