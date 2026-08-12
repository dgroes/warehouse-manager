import sqlite3
from warehouse.domain.category import Category
from warehouse.infrastructure.database.sqlite_connection import SQLiteConnection


class SQLiteCategoryRepository:

    def __init__(self, connection):
        self._connection = connection

    def save(self, category: Category) -> Category:
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO category (name, description, code)
                VALUES (?, ?, ?)
                """,
                (category.name, category.description, category.code),
            )

            # lastrowid: "¿Cuál fue el ID que SQLite acaba de generar en el último INSERT?"
            category_id = cursor.lastrowid

            # `_assign_id()` sirve para asignarle el ID al objeto de Python el ID que se acaba de generar en la DB
            category._assign_id(category_id)

            self._connection.commit()

            return category

        # Para los errores
        except sqlite3.IntegrityError as error:

            # Gracias al rollback: "Deshaz cualquier cambio pendiente de esta transacción"
            self._connection.rollback()

            raise ValueError("No se pudo guardar la categoría") from error

    def find_by_id(self, category_id: int) -> Category | None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description, code FROM category WHERE id = ?
                """,
                (category_id,), # <- Se pasa como tupla
            )

            row = cursor.fetchone()

            if row is None:
                return None

            # se reconstruye el objeto Category desde la tupla devuelta por SQLite
            # Inserción según los parámetros de tu constructor Category
            cat_id, name, description, code = row
            category = Category(name=name, code=code, description=description)
            category._assign_id(cat_id)

            return category

        except sqlite3.Error as error:
            # Nota: IntegrityError es para fallos de constraints (UNIQUE, FK).
            # Para errores generales de lectura/ejecución se usa sqlite3.Error.
            raise ValueError("Error al consultar la base de datos") from error

    def find_by_code(self, category_code: str) -> Category | None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description, code FROM category WHERE code = ?
                """,
                (category_code,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            cat_id, name, description, code = row
            category = Category(name=name, code=code, description=description)
            category._assign_id(cat_id)

            return category

        except sqlite3.Error as error:
            raise ValueError("Erorr al consultar la base de datos") from error

# Que hace exactamente save():
# Category
#    │
#    │ id = None
#    ▼
# cursor.execute(INSERT)
#    │
#    ▼
# SQLite
#    │
#    ├── guarda name
#    ├── guarda description
#    ├── guarda code
#    └── genera id
#           │
#           ▼
#     cursor.lastrowid
#           │
#           ▼
# category._assign_id(...)
#           │
#           ▼
# Category
#    │
#    │ id = 1
#    ▼
# return category
