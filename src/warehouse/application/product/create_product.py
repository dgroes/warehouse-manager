# C17: Casos de uso
from warehouse.domain.repositories.product_repository import ProductRepository
from warehouse.domain.repositories.category_repository import CategoryRepository
from warehouse.domain.category import Category
from warehouse.domain.product import Product


# CreateProduct debería pedirle al repositorio que guarde el producto.
class CreateProduct:
    def __init__(self, product_repository: ProductRepository, category_repository: CategoryRepository):
        self._product_repository = product_repository
        self._category_repository = category_repository

    def execute(self, name: str, category_id: int):

        category = self._category_repository.find_by_id(category_id)

        if category is None:
            raise ValueError(f"No se encontró la categoría con el id {category_id}")

        # Si existe, la ejecución continua
        product = Product(name, category) 

        self._product_repository.save(product)

        # Retornar el producto
        return product

# Flujo
# clases_test.py
#       │
#       │ execute("iPhone 14 Pro Max", category)
#       ▼
# CreateProduct
#       │
#       │ Product(...)
#       ▼
# Product
#       │
#       │ repository.save()
#       ▼
# InMemoryProductRepository
#       │
#       ├── ID = 1
#       ├── Barcode = 0000000001
#       └── _products.append()
#       │
#       ▼
# return product
#       │
#       ▼
# clases_test.py