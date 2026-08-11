from warehouse.domain.repositories.product_repository import ProductRepository
from warehouse.domain.category import Category
from warehouse.domain.product import Product


# CreateProduct debería pedirle al repositorio que guarde el producto.
class CreateProduct:
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def execute(self, name: str, category: Category):
        product = Product(name, category)  # <- Crea el objeto de dominio

        # No guarda en la DB, sino que llama la abstracción `ProductRepository`
        self._repository.save(product)

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