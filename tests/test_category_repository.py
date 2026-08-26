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


def test_save_category(connection):

    repository = SQLiteCategoryRepository(connection)

    cat = Category("Tecnología", "Productos tech", "tec")

    category = repository.save(cat)

    assert category is not None
    assert category.id == 1
    assert category.name == "Tecnología"
    assert category.code == "tec"


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
