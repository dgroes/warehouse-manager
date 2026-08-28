class DomainError(Exception):
    """Excepción base para el dominio."""
    pass

class DuplicateCategoryCodeError(DomainError):
    """Lanzada cuando se intenta guardar una categoría con un código que ya existe."""
    def __init__(self, code: str):
        # La función `super()` es la forma para decirle a una clase hija: "Llama al método de mi clase padre"
        # Esta clase hereda de `DomainError`, la cual hereda de la clase nativa "Exception"
        super().__init__(f"Ya existe una categoría con el código '{code}'.")