import sys
from pathlib import Path
from pprint import pprint

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

# C04: Imports
from warehouse.domain import Category
from warehouse.infrastructure.in_memory_product_repository import (
    InMemoryProductRepository,
)
from warehouse.infrastructure.services.simple_barcode_generator import (
    SimpleBarcodeGenerator,
)
from warehouse.application.product.create_product import CreateProduct

# Encuentra la raíz del proyecto (warehouse-manager) y añade 'src' a sys.path

# Crear la categoría primero
category_test = Category("Tecnología", "Productos de tecnología", "tec")

# Crear la infraestructura
barcode_generator = SimpleBarcodeGenerator()
repository = InMemoryProductRepository(barcode_generator)

# Crear caso de uso
create_product = CreateProduct(repository)

# Creación de producto
product_1 = create_product.execute(
    "iPhone 14 Pro Max",
    category_test
)

product_2 = create_product.execute(
    "Samsung S23",
    category_test
)

product_3 = create_product.execute(
    "MacBook Pro 16",
    category_test
)

product_2.disable()

product_4 = create_product.execute(
    "Onyx Boox Page 7",
    category_test
)

disabled_product = repository.disable("0000000003")

disabled_product_2 = repository.disable("9999999999")



pprint(vars(product_1))
pprint(vars(product_2))
pprint(vars(product_3))
pprint(vars(product_4))

print(f"\n{vars(disabled_product)}")

print(f"\n{disabled_product_2}")

product_2.enable()
print(f"\n {vars(product_2)}")


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