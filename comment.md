# C01: PySide6 (Qt)
**PySide6** es **la biblioteca oficial de Python desarrollada por The Qt Company para utilizar el popular framework gráfico Qt** (específicamente la versión Qt6). Permite crear interfaces gráficas de usuario (GUI) y aplicaciones de escritorio multiplataforma para sistemas como Windows, macOS y Linux escribiendo código en Python
<br>

**Características principales**
- **Multiplataforma**: Diseñas el programa una sola vez y funciona en diferentes sistemas operativos sin cambiar el núcleo del código
- **Oficial y abierta**: Cuenta con el respaldo directo de los creadores de Qt y se distribuye bajo licencias flexibles (incluyendo LGPL), lo que la hace apta para software comercial
- **Basado en C++**: Por debajo aprovecha la velocidad y potencia de Qt en C++, pero expone una interfaz limpia y natural para los programadores de Python.
- **Sistema de Widgets**: Proporciona botones, menús, ventanas, cuadros de texto y herramientas avanzadas de diseño.
# C02: property
En Python, `property` **es un decorador que permite convertir un método de una clase en un atributo de solo lectura o gestionado**, facilitando el uso de getters, setters y la validación de datos sin cambiar la forma en que se accede a ellos.
- **Acceso limpio**: Permite llamar a un método usando la sintaxis de un punto normal (como `objeto.atributo`) sin escribir paréntesis al final.
- **Control total**: Ayuda a interceptar cuando alguien lee, cambia o borra el valor de una variable interna para aplicar reglas o filtros.
- **Mantenimiento seguro**: Si inicias usando un atributo público simple y luego necesitas agregar lógica (como revisar que un número no sea negativo), puedes usar @property sin romper el código externo que ya usaba ese atributo

**Partes principales de una propiedad**
- **Getter (`@property`)**: Se usa para obtener o leer el valor del atributo oculto.
- **Setter (`@nombre.setter`)**: Se usa para validar y asignar un nuevo valor al atributo.
- **Deleter (`@nombre.deleter`)**: Se usa si necesitas definir una acción especial al borrar el atributo
# C03: Strategy
El [patrón de diseño Strategy](https://refactoring.guru/es/design-patterns/strategy) ==es un patrón de comportamiento que define una familia de algoritmos, los encapsula en clases separadas y hace que sus objetos sean intercambiables en tiempo de ejecución==. Permite que el código principal (el cliente) cambie el comportamiento de un programa sin modificar su estructura interna.

**Componentes principales**
- **Contexto (Context):** Mantiene una referencia a un objeto de estrategia y le delega la ejecución de la tarea.
- **Interfaz de Estrategia (Strategy):** Define el contrato común o método que todas las estrategias concretas deben implementar.
- **Estrategias Concretas (ConcreteStrategy):** Clases separadas que implementan los diferentes algoritmos o variantes del comportamiento.

**Ventajas de usar Strategy**
- **Flexibilidad:** Permite cambiar el algoritmo de un objeto mientras la aplicación está corriendo.
- **Mantenimiento limpio:** Evita el uso excesivo de condicionales grandes (`if-else` o `switch`) dentro de las clases.
- **Escalabilidad:** Facilita añadir nuevas estrategias o algoritmos sin alterar el código que ya funciona. 
## Código de barras
El código de barras seguirá este patron (strategy), pero en un ejemplo, si en un principio se tiene esto:
```py
class BarcodeGenerator:

    def generate(self, type):
        if type == "EAN13":
            ...
        elif type == "QR":
            ...
        elif type == "CODE128":
            ...
```
Aquí se debería agregar los distintos tipos de códigos que podrá generar, si en un futuro se agrega uno nuevo, se debería modificar la clase. Lo ideal es tener lo siguiente:
```cs
BarcodeGenerator
        ▲
        │
 ┌──────┴─────────┐
 │                │
EAN13Generator   QRGenerator
                Code128Generator
```
Aquí cada clase sabe generar un único tipo. Por ejemplo:
```py
class EAN13Generator:
    def generate(self):
        ...
```
y luego se crea otra distinta:
```py
class QRGenerator:
    def generate(self):
        ...
```
Entonces, si en un futuro se aparece un código nuevo para agregar, no se modificarían las clases existentes, simplemente se agregaría otra:
```css
BarcodeGenerator
        ▲
        │
 ┌──────┴──────────────┐
 │                     │
EAN13Generator    QRGenerator
                  Code128Generator
                  PDF417Generator   ← nuevo
```
# C04: Imports (`__init__.py`)
Si está la ruta `domain` la cual tiene en su interior `category.py` y `product.py`, una buena practica es usar `__init__.py` para tener imports más limpios y profeesionales.
`__init__.py` sirve principalmente:
- **Convertir una carpeta en un paquete**: Le dice a Python que esa carpeta contiene módulos de código que pueden ser importados desde cualquier parte.
- **Funcionar como la "recepción" o "fachada" de la carpeta**: Te permite centralizar y exponer lo que hay dentro para que no tengas que escribir rutas tan largas al importar.

Dejar el fichero `__init__.py` vacío, las carpetas ya se consideran paquetes, pero se tendrá que seguir importando así: 
```py
from warehouse.domain.product import Product
from warehouse.domain.category import Category
```
Pero si ahora está el fichero `__init__.py` dentro de domain: `/home/dgroes/Documentos/Workspace/warehouse-manager/src/warehouse/domain/__init__.py` y dentro del fichero está lo siguiente:
```py
# Dentro de domain/__init__.py
from .product import Product
from .category import Category
```
Ahora, por ejemplo desde el fichero de pruebas (o cualquier otra parte del proyecto), se puede importar ambas clases en una sola línea limpia, sin necesidad de especificar el nombre de cada archivo:
```py
# En clases_test.py ahora puedes hacer esto:
from warehouse.domain import Product, Category
```
Internamente ocurre lo siguiente:
```bash
1. Encuentra el paquete warehouse
        ↓
2. Entra al paquete domain
        ↓
3. Ejecuta __init__.py
        ↓
4. __init__.py importa Product y Category
        ↓
5. Product queda disponible dentro de warehouse.domain
```
Asiendo que `__init__` fuera la **recepción** de un edificio:
```bash
warehouse.domain
        │
        ▼
 +---------------------+
 |     __init__.py     |
 +---------------------+
 |  Product            |
 |  Category           |
 +---------------------+
```
Cuando alguien llega al paquete, la recepción decide qué mostrar.
# C05: Repository (Patron)
Un **Repository** (Repositorio) no es una herammienta nativa de Python, sino un patrón de diseño de software. Sirve para separar las reglas del negocio (la clase `Product`) de la DB o la tecnología que se use para guardar la información.
<br>

Para entenderlo: un repositorio es una clase de Python cuyo único trabajo es hacer el trabajo sucio de BD (hacer el `INSERT`, `SELECT`, `UPDATE`, o escribir en un JSON) para que el resto del código no tenga que ver código SQL.
## ¿Para qué sirve? (El problema vs. La solución)
**El problema (Sin repositorio)**
Si se mete código de base de datos dentro de la lógica de negocio, el código se vuelve un caos difícil de probar:
```py
# application/create_product.py
import sqlite3

def crear_producto_servicio(name, category, barcode):
    # Lógica de negocio
    if not name: raise ValueError()
    
    # ❌ CÓDIGO SUCIO: Tu aplicación se amarra a SQLite obligatoriamente
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products VALUES (?, ?, ?)", (name, category, barcode))
    conn.commit()
```
Si se quiere hacer un test de esto, se está obligado a crear una base de datos real en el disco duro cada vez que se corra el test.
## La solución (Con repositorio)
Se crea una clase que actúa como una "**caja negra**" con métodos fáciles de leer, como `.save()`, `.find_by_id()`, etc.
```py
# infrastructure/repositories.py
import sqlite3

class SQLiteProductRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def save(self, product) -> None:
        # El código de base de datos se queda atrapado AQUÍ
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products VALUES (?, ?, ?)", 
            (product.name, product.category.name, product.barcode)
        )
        conn.commit()
        conn.close()
```
## Ejemplo del código
Ahora que se tiene un repositorio, el servicio o caso de uso (`CreateProduct`) se vuelve increíblemente limpio y fácil de leer. Ya no le importa SQL, solo le importa la lógica de negocio:
```py
# application/create_product.py
from warehouse.domain import Product

class CreateProduct:
    # 1. Le pasamos el repositorio que vamos a usar (Inyección de dependencias)
    def __init__(self, repository):
        self.repository = repository

    def execute(self, name: str, category, barcode: str):
        # 2. Creamos el objeto de dominio (tu clase Product con sus validaciones)
        nuevo_producto = Product(name, category, barcode)
        
        # 3. Le ordenamos al repositorio que lo guarde
        # A 'CreateProduct' no le importa SI se guarda en SQLite, Postgres o una lista.
        self.repository.save(nuevo_producto) 
```
## Si luego se quiere migrar de DB:
La respuesta correcta es `ProductRepository` (específicamente la implementación de infraestructura).
Si se pide cambiar SQLite por PostgreSQL, la clase `Product` de dominio no se toca, y la lógica `CreateProduct` tampoco se toca. Lo único que hace es crear un nuevo archivo:
```py
# infrastructure/postgres_product_repository.py
import psycopg2

class PostgresProductRepository:
    def save(self, product):
        # Aquí se mete el código específico de PostgreSQL
        # conexion = psycopg2.connect(...)
        # cursor.execute("INSERT INTO...")
        pass
```
Para conectar todo en el archivo de pruebas o de ejecución principal, solo se cambia la "pieza de lego" que se le pasas al servicio:
```py
# En las pruebas con SQLite:
repo_sqlite = SQLiteProductRepository("test.db")
servicio = CreateProduct(repo_sqlite)

# El día que se migre a Postgres, solo se cambia esta línea:
repo_postgres = PostgresProductRepository(connection_string)
servicio = CreateProduct(repo_postgres) # El servicio funciona EXACTAMENTE igual
```
El repositorio sirve para que el código sea **modular**. Separa el "Qué hace mi sistema" (crear productos) del "Cómo lo guarda" (en SQLite, Postgres o archivos de texto).
# C06: Clase Base Abstracta
En Python, `from abc import ABC, abstractmethod` es la herramienta oficial para crear Interfaces o Contratos.

`ABC` significa Abstract Base Class (Clase Base Abstracta)
<br>

Sirve exactamente para resolver el problema del Repositorio que se ve en "*C05: Repository (Patron)*". Ppermite definir qué debe hacer un repositorio, sin obligar a escribir el cómo lo hace.<br>
**¿Para qué sirve cada parte?**
1. `ABC`: Es una clase especial de la que debes heredar para decirle a Python: "*Ojo, esta clase es un molde abstracto, no permitas que nadie cree un objeto directamente de ella*".
2. `@abstractmethod`: Es un decorador que se pone encima de los métodos. Dice: "*Cualquiera que herede de esta clase está obligado a escribir su propia versión de este método; si no lo hace, el programa dará error*".<br>
## Ejemplo
Imaginemos que en el proyecto warehouse-manager se define el contrato general para todos los repositorios de productos. No tiene código SQL, solo define las reglas:
```py
# src/warehouse/domain/repositories.py
from abc import ABC, abstractmethod
from warehouse.domain.product import Product

class ProductRepository(ABC): # 1. Hereda de ABC
    
    @abstractmethod # 2. Obliga a implementar este método
    def save(self, product: Product) -> None:
        """Guarda un producto en el sistema de persistencia."""
        pass # No lleva código, es solo una definición

    @abstractmethod # 3. Obliga a implementar este método
    def find_by_barcode(self, barcode: str) -> Product:
        """Busca un producto por su código de barras."""
        pass
```

**¿Qué pasa ahora si intentas usarlo mal?**
Si en el ficherode pruebas se intenta  hacer esto:
```py
repo = ProductRepository()
# ❌ ERROR: Python no te dejará. Dirá: "TypeError: Can't instantiate abstract class..."
```

**Cómo se usa correctamente? (Cumpliendo el contrato)**
Los repositorios reales (los de infraestructura) heredan de esa clase abstracta y están **obligados** a escribir el código real de `save` y `find_by_barcode`:
```py
# src/warehouse/infrastructure/sqlite_repository.py
from warehouse.domain.repositories import ProductRepository

class SQLiteProductRepository(ProductRepository): # Hereda del contrato
    
    def save(self, product):
        # Python te obliga a escribir esto. Si lo olvidas, da error.
        print(f"Guardando {product.name} en SQLite con código SQL real...")

    def find_by_barcode(self, barcode):
        print("Buscando en SQLite...")
        # Código para buscar...
```

**¿Por qué es tan útil en Clean Architecture?**
Porque el caso de uso `CreateProduct` ya no depende de SQLite ni de PostgreSQL. Depende únicamente de la clase abstracta `ProductRepository`.
Se le dice a Python: "*A mí no me importa qué base de datos me pases, siempre y cuando sea un hijo de `ProductRepository` (es decir, que cumpla el contrato y tenga el método `.save()` disponible)*".