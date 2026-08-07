import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

# C04: Imports
from warehouse.domain import Product, Category


# Encuentra la raíz del proyecto (warehouse-manager) y añade 'src' a sys.path

# Crear la categoría primero
category_test = Category("Tecnología", "Productos de tecnología", "tec")

# Crear productos
product_1 = Product("iPhone 14 Pro Max", category_test)
product_2 = Product("Samsung S23", category_test)

# Lista para almacenar datos
lista_productos = []

for p in [product_1, product_2]:
    lista_productos.append({
        "name": p.name,
        "category": p.category.name,
        "category_code": p.category.code,
    })

print(lista_productos)