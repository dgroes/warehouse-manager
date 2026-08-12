class Category:
    # -> None es una indicación que dice: "Esta función no devuelve ningún valor con un return"
    def __init__(self, name: str, description:str, code) -> None:
        self.name: str = name
        self.description: str = description
        self.code: str = code # Será un código abreviado (Tecnología: tec, Instrumento: ins, Ropa: rop, Lectura: lec, etc)
        self._id = None


    @property
    def id(self) -> int | None:
        return self._id

    @property
    def name(self) -> str:
        # usar "_" es una convención de Python para indicarle a otros programadores que esa variable es privada o protegida
        return self._name

    @name.setter
    def name(self, value:str) -> None:

        # quitar los espacios al inicio y al final
        clean_name = value.strip() if value else ""

        if len(clean_name) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres válidos")
    
        self._name = clean_name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("La descripción no puede estar vacía")
        self._description = value.strip().capitalize()

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El código no puede estar vacío")
        self._code = value.strip().lower()

    def _assign_id(self, category_id: int) -> None:
        if self._id is not None:
            raise ValueError("La categoría ya tiene un ID asignado")

        self._id = category_id