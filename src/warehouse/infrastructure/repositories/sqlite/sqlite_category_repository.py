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

    def search(self, column: str, value: any) -> tuple | None:
        cursor = self._connection.cursor()

        # Definir las columnas validas:
        valid_column = {
            "id": "id",
            "name": "name",
            "description": "description",
            "code": "code",
        }

        # Validación de segurdad(evitar Inyección SQL)
        if column not in valid_column:
            raise ValueError(f"La columna a buscar '{column}' no es válida.")

        #Obtención de los nombres según mapeados
        where_safe = valid_column[column]

        # SQL dinamico
        query = f"SELECT id, name, description, code FROM category WHERE {where_safe} = ?"

        try:
            cursor.execute(query, (value,))
            row = cursor.fetchone()
            if row is None:
                return None

        except sqlite3.Error as error:
            raise ValueError("Error al consultar la base de datos") from error

        return row


    def _reconstruct_category(self, result):

        # Separar el "result" en las distintas columnas:
        cat_id, cat_name, cat_description, cat_code = result

        # Construcción de la categoría:
        category = Category(name=cat_name, description=cat_description, code=cat_code)
        category._assign_id(cat_id)

        return category


    def find_by_id(self, category_id: int) -> Category | None:
        column = "id"
        result = self.search(column, category_id)

        #Si no hay resultado en la DB, se retorna None
        if result is None:
            return None

        category = self._reconstruct_category(result)
        return category

       

    def find_by_code(self, category_code: str) -> Category | None:

       column = "code"
       result = self.search(column, category_code)

       if result is None:
           return None

       category = self._reconstruct_category(result)
       return category


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
