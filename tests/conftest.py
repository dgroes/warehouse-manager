# C14: Pytest conftest
import sqlite3
import pytest
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))

# Obtener el schema: src/warehouse/infrastructure/database/schema.sql
schema_path = root_path / "src" / "warehouse" / "infrastructure" / "database" / "schema.sql"


@pytest.fixture
def connection():
    # Conexión en memoria
    connection = sqlite3.connect(":memory:")

    # Leer el fichero SQL del schema
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Ejecución del schema para la creación de tablas
    connection.executescript(schema_sql)

    # Entregar la conexión lista para el test
    """ 
    La palabra clave yield en Python se utiliza para pausar una función y devolver un valor temporalmente, 
    permitiendo que la función continúe más tarde desde donde se quedó.
    En el contexto de las pruebas con Pytest, yield transforma una función en una "fixture con ciclo de vida". 
    Divide el código en dos fases: el antes y el después del test. 
    """
    yield connection

    # Cerrar la conexión al terminal el test
    connection.close()