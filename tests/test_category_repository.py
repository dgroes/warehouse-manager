# C11: Pytest en uso
import sys
from pathlib import Path

# Permitir importar desde src/
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

from warehouse.infrastructure.database.sqlite_connection import SQLiteConnection
from warehouse.infrastructure.repositories.sqlite.sqlite_category_repository import (
    SQLiteCategoryRepository
)


def test_find_category_by_id():

    # Preparar
    database_path = root_path / "data" / "warehouse.db"
    connection = SQLiteConnection(database_path)
    conn = connection.connect()

    repository = SQLiteCategoryRepository(conn)

    # Ejecutar
    category = repository.find_by_id(2)

    # Verificar
    assert category is not None
    assert category.id == 2
    assert category.name == "Tecnología"
    assert category.code == "tec"

    conn.close()