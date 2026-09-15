import sys
from pathlib import Path

# Permitir importar desde src/
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path / "src"))


from warehouse.infrastructure.services.random_barcode_generator import RandomBarcodeGenerator
from warehouse.application.product.create_product import CreateProduct
from warehouse.infrastructure.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository
from warehouse.infrastructure.repositories.in_memory.in_memory_category_repository import InMemoryCategoryRepository
from warehouse.domain.category import Category
from warehouse.domain.product import Product
import pytest


def test_create_product():

    # Preparar (Arrange)
    barcode = RandomBarcodeGenerator()
    product_repository = InMemoryProductRepository(barcode)
    category_repository = InMemoryCategoryRepository()
    use_case = CreateProduct(product_repository, category_repository)

    category = Category("Tecnología", "Productos tech", "tec")
    category_saved = category_repository.save(category)

    product = use_case.execute("iPhone Duo", category_saved.id)

    assert product is not None
    assert product.id == 1
    assert product.name == "iPhone Duo"
    assert product.category.code == "tec"
    assert len(product.barcode) == 10


""" def test_create_product_is_saved():
    # Preparar (Arrange)
    barcode = RandomBarcodeGenerator()
    repository = InMemoryProductRepository(barcode)
    use_case = CreateProduct(repository)

    category = Category("Tecnología", "Productos tech", "tec")

    product_saved = use_case.execute("iPhone Duo", category)

    find = repository.find_by_name(product_saved.name)

    assert find is not None
    assert find.name == "iPhone Duo"
    assert find.id == 1    
 """