import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

from warehouse.domain.category import Category
from warehouse.domain.product import Product
from warehouse.infrastructure.services.random_barcode_generator import RandomBarcodeGenerator
from warehouse.infrastructure.database.sqlite_connection import SQLiteConnection
from warehouse.infrastructure.repositories.sqlite.sqlite_category_repository import (
    SQLiteCategoryRepository
)
from warehouse.infrastructure.repositories.sqlite.sqlite_product_repository import SQLiteProductRepository

# Ruta de la base de datos
database_path = root_path / "data" / "warehouse.db"


# Conexión
connection = SQLiteConnection(database_path)
conn = connection.connect()


# Repositorio
category_repository = SQLiteCategoryRepository(conn)

# Producto
barcode_generator = RandomBarcodeGenerator()




# Crear categoría
""" category = Category(
    "Jardinería",
    "Productos para jardinería",
    "jar",
)

try:
    saved_category = category_repository.save(category)

    print(
        f"{saved_category.id} - "
        f"{saved_category.name} - "
        f"{saved_category.description} - "
        f"{saved_category.code}"
    )

except ValueError as error:
    print(f"[ERROR] {error}") """

print("Categoría")
# Buscar categoría
category = category_repository.find_by_id(1)
print(category.name, category.id, category.code)

# Buscar por código
category_two = category_repository.find_by_code("tec")
print(category_two.name, category_two.id, category_two.code)




print("\n Producto")
category = category_repository.find_by_id(2)

product = Product(
    "iPhone 14 Pro Max",
    category,
)


barcode_generator = RandomBarcodeGenerator()

product_repository = SQLiteProductRepository(
    conn,
    barcode_generator,
)

saved_product = product_repository.save(product)


print(
    saved_product.id,
    saved_product.name,
    saved_product.category.id,
    saved_product.barcode,
    saved_product.active,
)


producto_por_id = product_repository.find_by_id(67)
print(producto_por_id)
