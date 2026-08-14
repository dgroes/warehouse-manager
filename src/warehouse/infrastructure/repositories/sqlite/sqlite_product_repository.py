import sqlite3
from warehouse.domain.product import Product
from warehouse.domain.category import Category
from warehouse.infrastructure.database.sqlite_connection import SQLiteConnection
from warehouse.infrastructure.services.random_barcode_generator import BarcodeGenerator


class SQLiteProductRepository:

    def __init__(
        self,
        connection,
        barcode_generator: BarcodeGenerator,
    ):
        self._connection = connection
        self._barcode_generator = barcode_generator

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

    def find_by_id(self, product_id: int) -> Product | None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, category_id, barcode, active FROM product WHERE id = ?
                """,
                (product_id,),  # <- se pasa como tupla
            )
            row_product = cursor.fetchone()

            if row_product is None:
                return None

            # Variable que almacena la tupla devuela por SQLite
            pro_id, name, cateogory_id, barcode, active = row_product

            # Crear el objeto Category en base al category_id

         
            cursor.execute(
                """
                    SELECT id, name, description, code FROM category WHERE id = ?
                    """,
                (cateogory_id,),
            )
            row_category = cursor.fetchone()
            if row_category is None:
                return None

            # Construcción de Objeto Category
            cat_id, name, description, code = row_category
            category = Category(name=name, code=code, description=description)
            category._assign_id(cat_id)

            # Construcción de objeto Product
            product = Product(name=name, category=Category.id)
            product._assign_barcode(barcode)
            product._assing_id(pro_id)
        

            return product
        except sqlite3.Error as error:
            # Nota: IntegrityError es para fallos de constraints (UNIQUE, FK).
            # Para errores generales de lectura/ejecución se usa sqlite3.Error.
            raise ValueError("Error al consultar la base de datos") from error
