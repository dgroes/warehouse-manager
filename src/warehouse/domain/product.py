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
        self.active = True 

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

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value