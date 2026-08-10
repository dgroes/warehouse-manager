import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

# C04: Imports
from warehouse.domain import Product, Category
from warehouse.infrastructure.in_memory_product_repository import InMemoryProductRepository
from warehouse.infrastructure.services.simple_barcode_generator import SimpleBarcodeGenerator


# Encuentra la raíz del proyecto (warehouse-manager) y añade 'src' a sys.path

# Crear la categoría primero
category_test = Category("Tecnología", "Productos de tecnología", "tec")

# Crear productos
product_1 = Product("iPhone 14 Pro Max", category_test)
product_2 = Product("Samsung S23", category_test)
product_3 = Product("MacBook Pro 16", category_test)
product_4 = Product("Sony WH-1000XM5", category_test)
product_5 = Product("iPad Air M2", category_test)
product_6 = Product("PlayStation 5", category_test)
product_7 = Product("Logitech MX Master 3S", category_test)

""" product_1._assign_id(1)
product_1._assign_barcode("0000000001")

product_2._assign_id(2)
product_2._assign_barcode("0000000002")

product_3._assign_id(3)
product_3._assign_barcode("0000000003")

product_4._assign_id(4)
product_4._assign_barcode("0000000004")

product_5._assign_id(5)
product_5._assign_barcode("0000000005")

product_6._assign_id(6)
product_6._assign_barcode("0000000006")

product_7._assign_id(7)
product_7._assign_barcode("0000000007") """

barcode_generator = SimpleBarcodeGenerator()

repository = InMemoryProductRepository(barcode_generator)

repository.save(product_1)
repository.save(product_2)
repository.save(product_3)
repository.save(product_4)
repository.save(product_5)
repository.save(product_6)
repository.save(product_7)

"""  
Aquí el flujo sería:

Product
   ↓
repository.save()
   ↓
InMemoryProductRepository
   ↓
_products
"""

# Busqueda por nombre:
# product = repository.find_by_name("MacBook Pro 16")

# Busqueda por Barcode:
product = repository.find_by_barcode("0000000002")

if product is not None:
    print(f"{product.name} - {product.category.name} - ID[{product.id}] - BARCODE[{product.barcode}]")
else:
    print("[NOT FOUND] No se encontró el producto")


""" # Lista para almacenar datos
lista_productos = []

for p in [product_1, product_2]:
    lista_productos.append({
        "name": p.name,
        "category": p.category.name,
        "category_code": p.category.code,
    })

print(lista_productos) """