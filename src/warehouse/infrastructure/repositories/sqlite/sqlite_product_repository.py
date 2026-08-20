import sqlite3
from warehouse.domain.product import Product
from warehouse.domain.category import Category
from warehouse.infrastructure.database.sqlite_connection import SQLiteConnection
from warehouse.infrastructure.services.random_barcode_generator import BarcodeGenerator
from warehouse.infrastructure.repositories.sqlite.sqlite_category_repository import (
    SQLiteCategoryRepository,
)


class SQLiteProductRepository:

    def __init__(
        self,
        connection,
        barcode_generator: BarcodeGenerator,
    ):
        self._connection = connection
        self._barcode_generator = barcode_generator

        # se inyecta la misma conexión al repositorio de categorías internamente
        self._category_repository = SQLiteCategoryRepository(self._connection)

    def save(self, product: Product) -> Product:
        cursor = self._connection.cursor()

        # asignar el Barcode

        max_intentos = 4

        for intento in range(max_intentos):
            barcode = self._barcode_generator.generate()

            try:
                cursor.execute(
                    """
                    INSERT INTO product (name, category_id, barcode,active)
                    VALUES(?, ?, ?, ?)
                    """,
                    (product.name, product.category.id, barcode, 1),
                )
                # obtener el ID
                product_id = cursor.lastrowid

                # Asignar el ID al objeto
                product._assign_id(product_id)

                # Asignar el Barcode al objeto
                product._assign_barcode(barcode)

                self._connection.commit()

                return product

            except sqlite3.IntegrityError as error:
                self._connection.rollback()
                mensaje = str(error)

                # Si el error es específicamente por duplicado en el barcode
                if "UNIQUE constraint failed: product.barcode" in mensaje:
                    # Si llegamos al último intento y sigue fallando, lanzamos la excepción
                    if intento == max_intentos - 1:
                        raise ValueError(
                            f"No se pudo generar un código de barras único tras {max_intentos} intentos."
                        ) from error
                    # Si aún quedan intentos, el 'continue' salta al siguiente ciclo del for
                    continue

                # Si es otra violación de integridad (ej. clave foránea o nombre duplicado), fallamos de inmediato
                raise ValueError(
                    "Error de integridad al guardar el producto"
                ) from error

    def update(self, product: Product) -> Product | None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE product SET name = ?, category_id = ? WHERE id = ?
                """,
                (product.name, product.category.id, product.id),
            )

            if cursor.rowcount == 0:
                raise ValueError(f"No existe ningún producto con el ID {product.id} para actualizar.")

            self._connection.commit()
            return product
        except sqlite3.Error as error:
            raise ValueError(f"Error en la base de datos al actualizar el producto con ID: {product.id}. [ERROR]: {error}") from error

    def search(self, column: str, value: any) -> Product | None:

        # Creación de la conexión
        cursor = self._connection.cursor()

        # Definir que columnas son las validas:
        valid_column = {
            "id": "id",
            "name": "name",
            "barcode": "barcode",
            "active": "active",
        }

        # Validación de seguridad estrica para evitar inyección SQL
        if column not in valid_column:
            raise ValueError(f"La columna a buscar '{column}' no es válida")

        # Obtención de los nombres seguros mapeados:
        where_safe = valid_column[column]

        # SQL Dinámico
        query = f"SELECT id, name, category_id, barcode, active FROM product WHERE {where_safe} = ?"

        try:
            cursor.execute(query, (value,))
            row = cursor.fetchone()
            if row is None:
                return None
        except sqlite3.Error as error:
            # Nota: IntegrityError es para fallos de constraints (UNIQUE, FK).
            # Para errores generales de lectura/ejecución se usa sqlite3.Error.
            raise ValueError("Error al consultar la base de datos") from error

        return row

    def disable(self, product: Product) -> Product | None:

        cursor = self._connection.cursor()


        try: 
            cursor.execute(
            """
            UPDATE product SET active = 0 WHERE id = ?
            """,
            (product.id)
        )
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el producto con el ID {product.id}.")
                
            self._connection.commit()
            return product
        except sqlite3.Error as error:
            raise ValueError(f"Error en al base de datos al desactivar el producto ID: {product.id}. [ERROR]: {error}") from error


    def enable(self, product: Product) -> Product | None:
        pass



    # Agregando "_" se indica que es un método interno del repository
    def _reconstruct_product(self, result):

        # Separa el "result" en las distintas columnas
        pro_id, pro_name, pro_category_id, pro_barcode, pro_active = result

        # Reconstrucción de la categoría
        category_class = self._category_repository.find_by_id(pro_category_id)

        # Construcción del producto
        product = Product(name=pro_name, category=category_class)
        product._assign_id(pro_id)
        product._assign_barcode(pro_barcode)

        # Tratado de active
        if pro_active == 0:
            product.disable()

        return product

    def find_by_id(self, product_id: int) -> Product | None:

        column = "id"
        result = self.search(column, product_id)

        # Si no hay resultado en la BD, se retorna None inmediatamente
        if result is None:
            return None

        # Construcción de producto
        product = self._reconstruct_product(result)
        return product

    def find_by_barcode(self, barcode: str) -> Product | None:

        column = "barcode"

        # Utilización de método "search" para buscar por barcode
        result = self.search(column, barcode)

        # Si no hya reslutado en la BD, se retorna None
        if result is None:
            return None

        # Construcción de producto
        product = self._reconstruct_product(result)

        return product

    
