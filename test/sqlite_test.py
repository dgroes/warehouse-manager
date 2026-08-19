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
category = category_repository.find_by_id(2)
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


## TEST DE producto desactivado:
cursor = conn.cursor()

# 2. Ejecutar la actualización especificando el ID 67
cursor.execute(
    """
    UPDATE product 
    SET active = 0 
    WHERE id = ?;
    """,
    (67,),
)

# 3. Guardar los cambios permanentemente en la base de datos
conn.commit()

print("\n[BD] Producto ID 67 desactivado correctamente.")

# 4. Probar la búsqueda mediante el repositorio para verificar que recupera active=False (0)
producto_por_id = product_repository.find_by_id(67)

if producto_por_id:
    print(
        f"Producto recuperado por Repositorio: "
        f"ID={producto_por_id.id} | "
        f"Nombre={producto_por_id.name} | "
        f"Activo={producto_por_id.active}"
    )
else:
    print("El producto con ID 67 no fue encontrado.")

 


producto_por_id = product_repository.find_by_id(67)
print(f"Producto buscado por ID: [{producto_por_id.name, producto_por_id.id, producto_por_id.category, producto_por_id.barcode, producto_por_id.active}]")

""" 
producto_por_barcode = product_repository.find_by_barcode("2227118753")
print("\n")
print(f"🔍 Producto buscado por BARCODE: [{producto_por_barcode.id, producto_por_barcode.category, producto_por_barcode.barcode, producto_por_barcode.active}]")

 """

print("\n")
def obtener_dato_dinamico(columna_a_buscar, columna_filtro, valor_filtro):
    # 1. Mapeo de columnas permitidas (tanto para SELECT como para el WHERE)
    columnas_validas = {
        "id": "id",
        "name": "name",
        "barcode": "barcode",
        "active": "active",
    }

    # 2. Validación de seguridad estricta para evitar inyección SQL
    if columna_a_buscar not in columnas_validas:
        raise ValueError(
            f"La columna a buscar '{columna_a_buscar}' no es válida."
        )

    if columna_filtro not in columnas_validas:
        raise ValueError(f"La columna de filtro '{columna_filtro}' no es válida.")

    # 3. Obtención de nombres seguros mapeados
    select_seguro = columnas_validas[columna_a_buscar]
    where_seguro = columnas_validas[columna_filtro]

    # 4. Construcción del SQL dinámico
    # Las columnas van por f-string (seguras por la whitelist). El valor va con '?'
    query = f"SELECT {select_seguro} FROM product WHERE {where_seguro} = ?"

    cursor = conn.cursor()
    try:
        cursor.execute(query, (valor_filtro,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    finally:
        cursor.close()  # Cerramos solo el cursor


# --- EJEMPLOS DE USO DINÁMICO ---

print("TEST de SQLite Totalmente Dinámico 😼")

# Caso 1: Buscar el 'barcode' filtrando por 'id'
barcode = obtener_dato_dinamico("barcode", "id", 77)
print(f"Barcode del ID 77: {barcode}")

# Caso 2: Buscar el 'name' filtrando por 'barcode'
nombre = obtener_dato_dinamico("name", "barcode", "6863277869")
print(f"Nombre del producto con ese barcode: {nombre}")

# Caso 3: Buscar el 'id' de un producto por su 'name'
producto_id = obtener_dato_dinamico("id", "name", "iPhone 14 Pro Max")
print(f"ID del iPhone: {producto_id}")


print("\n Producto por BARCODE:")
producto_por_barcode = product_repository.find_by_barcode("3446163192")
print (producto_por_barcode)
