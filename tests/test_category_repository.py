# C11: Pytest en uso
import sys
from pathlib import Path

# Permitir importar desde src/
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

from warehouse.infrastructure.repositories.sqlite.sqlite_category_repository import (
    SQLiteCategoryRepository,
)
from warehouse.domain.category import Category
from warehouse.domain.exceptions import DuplicateCategoryCodeError
import pytest
import re


def test_find_category_by_id(connection):

    # Preparar (Arrange), Se inserta una categoría de prueba en la DB en memoria (que estará vacía al inicio)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )

    connection.commit()

    # Se pasa la conexión de la FIXTURE al repositorio
    repository = SQLiteCategoryRepository(connection)

    # Ejecutar (Act)
    category = repository.find_by_id(1)

    # Verificar (Assert)
    assert category is not None
    assert category.id == 1
    assert category.name == "Tecnología"
    assert category.code == "tec"


def test_find_category_by_id_fail(connection):

    repository = SQLiteCategoryRepository(connection)

    category = repository.find_by_id(1)

    assert category is None


def test_save_category(connection):

    repository = SQLiteCategoryRepository(connection)

    cat = Category("Tecnología", "Productos tech", "tec")

    category = repository.save(cat)

    assert category is not None
    assert category.id == 1
    assert category.name == "Tecnología"
    assert category.code == "tec"


def test_save_category_code_duplicate(connection):
    repository = SQLiteCategoryRepository(connection)

    first_cat = Category("Tecnología", "Productos tech", "tec")
    repository.save(first_cat)

    second_cat = Category("Instrumento", "Instrumentos Musicales", "tec")

    # Se verifica que se lance la excepción semántica de Dominio
    # re.escape() sirve para que el texto que se quiere comparar sea tratado literalmente, y no como una expresión regular.
    mensaje_esperado = "Ya existe una categoría con el código 'tec'."
    with pytest.raises(
        DuplicateCategoryCodeError, match=f"^{re.escape(mensaje_esperado)}$"
    ):
        repository.save(second_cat)


def test_find_category_by_code(connection):
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )

    connection.commit()

    repository = SQLiteCategoryRepository(connection)
    category = repository.find_by_code("tec")

    assert category is not None
    assert category.id == 1
    assert category.name == "Tecnología"
    assert category.code == "tec"


def test_find_category_by_code_fail(connection):

    repository = SQLiteCategoryRepository(connection)
    category = repository.find_by_code("ins")

    assert category is None


# By Name
def test_search_category(connection):
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO category (name, description, code) VALUES (?,?,?)",
        ("Tecnología", "Productos tech", "tec"),
    )

    connection.commit()

    repository = SQLiteCategoryRepository(connection)
    result = repository.search("name", "Tecnología")

    # Comprobar que 'result' sea un objeto de tipo tuple
    assert isinstance(result, tuple)
    assert result[0] == 1
    assert result[1] == "Tecnología"
    assert result[2] == "Productos tech"
    assert result[3] == "tec"


def test_search_category_not_found(connection):

    repository = SQLiteCategoryRepository(connection)

    result = repository.search("name", "No existe")

    assert result is None

def test_search_invalid_column(connection):
    repository = SQLiteCategoryRepository(connection)

    # Verificamos que al pasar una columna no permitida lance ValueError
    with pytest.raises(ValueError, match="La columna a buscar 'namess' no es válida."):
        repository.search("namess", "algo")


# pytest
#   │
#   ├── ejecuta fixture connection
#   │       │
#   │       ├── crea SQLite en memoria
#   │       ├── ejecuta schema.sql
#   │       └── entrega connection
#   │
#   ├── test_find_category_by_id(connection)
#   │       ├── INSERT de prueba
#   │       ├── Repository
#   │       ├── find_by_id()
#   │       └── assert
#   │
#   └── test_get_all_categories(connection)
#           └── BD nueva y vacía
