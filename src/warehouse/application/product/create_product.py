from warehouse.domain.repositories.product_repository import ProductRepository

# CreateProduct debería pedirle al repositorio que guarde el producto.
class CreateProduct:
    def __init__(self, repository: ProductRepository):
        self._repository = repository