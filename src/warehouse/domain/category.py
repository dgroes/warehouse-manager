class Category:
    # -> None es una indicación que dice: "Esta función no devuelve ningún valor con un return"
    def __init__(self, name: str, description:str) -> None:
        self.name: str = name
        self.description: str = description

    