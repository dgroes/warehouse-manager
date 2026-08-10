from warehouse.domain.category import Category

class Product:
    # Aquí el "active" por defectó estará en True 👀, como el valor de active siempre será el mismo, lo mejor sería no exponerlo en el constructor
    def __init__(
                self, name: str, 
                category: Category 
                #active: bool = True
            ) -> None:
        # Al usar self.name y self.category (sin guion bajo), 
        # Python activa automáticamente los @setters definidos abajo
        self.name = name
        self.category = category
        self._active = True
        self._id = None
        self._barcode = None 

    # --- CONTROL DE NOMBRE ---
    @property
    def name(self) -> str:
        #"""Getter: Devuelve el nombre protegido"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        #"""Setter: Valida el nombre antes de guardarlo"""
        if not value or not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._name = value.strip() # Guarda en la variable interna protegida

    # --- CONTROL DE CATEGORÍA ---
    @property
    def category(self) -> Category:
        #"""Getter: Devuelve la categoría protegida"""
        return self._category

    @category.setter
    def category(self, value: Category) -> None:
        #"""Setter: Valida el tipo de categoría antes de guardarla"""
        if not isinstance(value, Category):
            raise ValueError("La categoría debe ser un objeto válido de la clase Category")
        self._category = value


    # Contro de is_active
    @property
    def active(self) -> bool:
        return self._active

    # El setter de "active" será mejor estar como un método, 
    # Así se evita que cualquier código pueda cambiar "active" arbitrariamente y obligamos a pasar por acciones explícitas
    """ 
    @active.setter
    def active(self, value: bool) -> None:
        self._active = value 
    """

    # Getters de ID y BARCODE
    @property
    def id(self) -> int | None:
        return self._id

    @property
    def barcode(self) -> str | None:
        return self._barcode


    # Asignación de ID de manera interna(SIN BD, uso para Test)
    def _assign_id(self, product_id: int) -> None:
        if self._id is not None:
            raise ValueError("El producto ya tiene un ID asignado")

        self._id = product_id

    def _assign_barcode(self, barcode: str) -> None:
        if self._barcode is not None:
            raise ValueError("El producto ya tiene un código de barras asignado")

        self._barcode = barcode

    # Método para desactivar
    def disable(self) -> None:
        self._active = False

    # Método para activar
    def enable(self) -> None:
        self._active = True