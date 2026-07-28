from category import Category

class Product:
    # se indica que 'category' debe ser un objeto de la clase Category
    def __init__(self, name: str, category: Category) -> None:

        # Validación de nombre
        if not name or not name.strip():
            raise ValueError("El nombre no puede estar vacío")

        # Validación de categoría (Evita vacíos y tipos incorrectos)
        if not isinstance(category, Category):
            raise ValueError("La categoría debe ser un objeto válido de la clase Category")

        self.category: Category = category  
        self.name: str = name

error = "hola"

tecnologia = Category("Tecnología", "Dispositivos electrónicos y gadgets")
celular = Product("iPhone 15", error)

print(celular.category.name)