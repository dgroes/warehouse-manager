# C11: Pytest en uso
import sys
from pathlib import Path

# Permitir importar desde src/
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

from warehouse.infrastructure.repositories.sqlite.sqlite_product_repository import (
    SQLiteProductRepository,
)
from warehouse.infrastructure.repositories.sqlite.sqlite_category_repository import (
    SQLiteCategoryRepository,
)
from warehouse.domain.category import Category
from warehouse.domain.product import Product
from warehouse.infrastructure.services.random_barcode_generator import (
    RandomBarcodeGenerator,
)
import pytest
import re


def test_find_product_by_id(connection):
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )
    connection.commit()

    cursor.execute(
        "INSERT INTO product (name, category_id, barcode, active) VALUES (?, ?, ?, ?)",
        ("MOREFINE M7 R3-4300U", 1, "1227118753", 1),
    )

    connection.commit()

    barcode = RandomBarcodeGenerator()

    repository = SQLiteProductRepository(connection, barcode)

    product = repository.find_by_id(1)

    assert product is not None
    assert product.name == "MOREFINE M7 R3-4300U"
    assert product.barcode == "1227118753"
    assert product.category.id == 1
    assert product.category.code == "tec"


def test_find_product_by_id_fail(connection):

    barcode = RandomBarcodeGenerator()
    repository = SQLiteProductRepository(connection, barcode)
    product = repository.find_by_id(1)

    assert product is None


def test_save_product(connection):

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )
    connection.commit()

    repository_cat = SQLiteCategoryRepository(connection)

    category = repository_cat.find_by_id(1)

    barcode = RandomBarcodeGenerator()
    repository_pro = SQLiteProductRepository(connection, barcode)

    pro = Product("Flipper Zero", category)

    product = repository_pro.save(pro)

    assert product is not None
    assert product.name == "Flipper Zero"
    assert len(product.barcode) == 10
    assert product.category.code == "tec"
    assert product.active is True


def test_search_product(connection):
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )
    connection.commit()

    cursor.execute(
        "INSERT INTO product (name, category_id, barcode, active) VALUES (?, ?, ?, ?)",
        ("Retroid Pocket Flip 2", 1, "7427118004", 1),
    )
    connection.commit()

    barcode = RandomBarcodeGenerator()

    repository = SQLiteProductRepository(connection, barcode)
    result = repository.search("name", "Retroid Pocket Flip 2")

    assert isinstance(result, tuple)
    assert result[0] == 1
    assert result[1] == "Retroid Pocket Flip 2"
    assert result[2] == 1  # Id categoría


def test_search_product_not_found(connection):

    barcode = RandomBarcodeGenerator()
    respository = SQLiteProductRepository(connection, barcode)

    result = respository.search("name", "No existe")

    assert result is None


def test_search_invalid_column(connection):

    barcode = RandomBarcodeGenerator()
    respository = SQLiteProductRepository(connection, barcode)

    with pytest.raises(ValueError, match="La columna a buscar 'namess' no es válida."):
        respository.search("namess", "Behringer UM-02")


def test_disable_product(connection):

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )
    connection.commit()

    cursor.execute(
        "INSERT INTO product (name, category_id, barcode, active) VALUES (?, ?, ?, ?)",
        ("Accer Nitro 5", 1, "8402911093", 1),
    )
    connection.commit()

    barcode = RandomBarcodeGenerator()
    repository = SQLiteProductRepository(connection, barcode)

    pro = repository.find_by_id(1)
    product = repository.disable(pro)

    assert product.active is False


def test_disable_product(connection):

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )
    connection.commit()

    cursor.execute(
        "INSERT INTO product (name, category_id, barcode, active) VALUES (?, ?, ?, ?)",
        ("Accer Nitro 5", 1, "8402911093", 0),
    )
    connection.commit()

    barcode = RandomBarcodeGenerator()
    repository = SQLiteProductRepository(connection, barcode)

    pro = repository.find_by_id(1)
    product = repository.enable(pro)

    assert product.active is True


def test_update_product(connection):
    cursor = connection.cursor()
    
    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )
    connection.commit()

    cursor.execute(
        "INSERT INTO product (name, category_id, barcode, active) VALUES (?, ?, ?, ?)",
        ("Crucial: RAM Notebook DDR4 8GB", 1, "0389584716", 1),
    )
    connection.commit()

    barcode = RandomBarcodeGenerator()
    repository = SQLiteProductRepository(connection, barcode)


    pro_find = repository.find_by_id(1)    
    pro_find.name = "XPG: DDR4 8GB"

    pro_update = repository.update(pro_find)

    product = repository.find_by_id(pro_update.id)

    assert product is not None
    assert product.name == "XPG: DDR4 8GB"
    assert product.id == 1
    assert product.category.id == 1
    assert product.category.name == "Tecnología"
    assert product.barcode == "0389584716"

    
def test_update_product_not_found(connection):

    barcode = RandomBarcodeGenerator()
    repository = SQLiteProductRepository(connection, barcode)


    date_cat = Category("Tecnología", "Productos tech", "tec") 
    date_pro = Product("XPG: DDR4 8GB", date_cat)
    date_pro._assign_id(1)

    with pytest.raises(ValueError, match="No existe ningún producto con el ID 1 para actualizar"):
        repository.update(date_pro)


