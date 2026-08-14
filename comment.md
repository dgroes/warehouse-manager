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
# C07: Optional
En python si se busca un código de barras como lo hace `find_by_barcode` que no existe, lo normal es que el repositorio devuelva `None`. `Optional` sirve para avisarle de forma explícita a el editor de código y a otros dev que **el método puede devolver un objeto `Product` o un `None`**

Apartir de Python 3.10, se puede usar el operador `|` que es un ("o"), que es la forma más moderna y limpia de escribir `Optional`, además no hará falta de importar: `from typing import Optional`
```py
from abc import ABC, abstractmethod
from typing import Optional # Requerido si usas Python 3.9 o inferior
from warehouse.domain import Product

class ProductRepository(ABC):

    @abstractmethod
    def save(self, product: Product) -> None:
        pass

    # OPCIÓN A (Python 3.10+): Más limpia, usando el operador |
    @abstractmethod
    def find_by_barcode(self, barcode: str) -> Product | None:
        """Busca por código de barras. Devuelve el Product o None si no existe."""
        pass

    # OPCIÓN B (Python 3.9 o inferior): Usando la palabra Optional
    # @abstractmethod
    # def find_by_barcode(self, barcode: str) -> Optional[Product]:
    #     pass
```      
# C08: Inyección de dependencias
La inyección de dependencias significa pasarla a una clase los objetos que necesita para funcionar (sus dependencias) desde afuera, en lugar de que la calse los cree ella misma internamente.<br>
**Un ejemplo de la vida real**
Imagina que eres un cocinero y necesitas un horno para hacer pan:
- **Sin Inyección de Dependencias (Opción A)**: Para hacer pan, tú mismo construyes un horno eléctrico dentro de tu cocina. Si mañana quieres cambiarte a un horno de leña o a gas, tienes que romper la pared de tu cocina y reconstruirla.
- **Con Inyección de Dependencias (Opción B)**: Tú solo pides "un horno que cumpla con calentar a 200°C". Alguien te lo "inyecta" (te lo conecta) desde fuera. A ti no te importa si por dentro funciona con electricidad, gas o leña; tú solo metes la masa y horneas.

**Ahora dentro del código**:<br>
**Sin inyección**
```python
class CreateProduct:

    def __init__(self):
        # La clase "construye" su propio repositorio SQLite.
        # Está acoplada directamente a SQLite.
        self._repository = SQLiteProductRepository()
```
Aquí `CreateProduct` depende de SQLite, no hay forma de probar esta clase sin tocar una base de datos SQLite real.<br>
**Con inyección**
```python
class CreateProduct:

    def __init__(self, repository: ProductRepository):
        # La dependencia se la "inyectamos" desde fuera a través del constructor.
        self._repository = repository
```
Aquí `CreateProduct` solo dice: "Dame algo que respete el contrato  `ProductRepository`, no me importa qué sea ni cómo funcione por dentro".
## Ventajas
Esto tiene que ver directamente con **arquitectura limpia** que se está construyendo y da 3 beneficios concretos:
1. Flexibilidad de infraestructura: El día de mañana, en el punto de entrada del sistema (ejemplo: `main.py`) se puede hacer esto:
```py
# Si se usa SQLite:
repo = SQLiteProductRepository()
use_case = CreateProduct(repository=repo)

# Si se cambia a PostgreSQL, SOLO se cambia esta línea en main.py:
repo = PostgresProductRepository()
use_case = CreateProduct(repository=repo)
```
se puede ver que el archivo `create_product.py` no se toca en absoluto
2. Facilidad para hacer test: Para probar el caso de uso  `CreateProduct` no se necesita levantar toda una base de datos real. Se le "inmyecta" un repositorio falso en memoria (*FakeProductRepository*) que guarde los productos en una simple lista de Python:
```python
   fake_repo = FakeProductRepository()
   use_case = CreateProduct(repository=fake_repo)
   # ¡Tus tests corren en milisegundos y sin tocar el disco!
```
3. **Inversión de Control**: La capa de dominio/aplicación (`CreateProduct`) dicta las reglas (la interfaz `ProductRepository`), y las capas externas (infraestructura) se adaptan a ella.
# C09: Entorno Virutal
Es básicamente una **carpeta aislada** que contiene su propia copia de Python y sus librerías independientes del resto del sistema operativo.<br>
**La analogía de los contenedores**:
- **El Python del sistema (Sin venv)**: Es como instalar todas las herramientas de tu casa en una sola caja gigante compartida por todos en la familia. Si un proyecto necesita la herramienta `A` en versión 1.0 y otro necesita la versión 2.0, entran en conflicto y rompes el sistema.
- **El Entorno Virtual (Con venv)**: Es como darle a cada proyecto su propia caja de herramientas privada. Tu proyecto `warehouse-manager` tiene su propia carpeta `.venv` donde instalas `python-barcode`. Si mañana creas otro proyecto, tendrá su propio `.venv` sin interferir con este.

Al intentar hacer `python3 -m pip install "python-barcode[images]"` Unbutu (el sistema principal en el cual se está desarrollando el proyecto) lo bloqueó
## ¿Por qué Ubuntu te bloqueó? (PEP 668)
En versiones recientes de Ubuntu/Linux, el sistema operativo usa Python internamente para funciones críticas de la interfaz y herramientas del sistema.

Si se instalan paquetes globales con `pip install`, se corre el riesgo de sobrescribir o actualizar una librería que Ubuntu necesita para funcionar, pudiendo romper la terminal o la interfaz gráfica. Por eso, Linux ahora exige crear un entorno privado (`venv`) para cada proyecto de software que se desarrolle.
## ¿Qué contiene realmente la carpeta `.venv`?
Cuando se ejecuta `python3 -m venv .venv`, se crea una carpeta oculta en la raíz de el proyecto (el comando se debería ejecutar en la raíz)
- `.venv/bin/`: Contiene accesos directos al ejecutable de `python` y `pip`.
- `.venv/lib/python3.X/site-packages/`: Aquí es donde se descargan e instalan las librerías (como `python-barcode` o `Pillow`).

Al ejecutar source `.venv/bin/activate`, se le dice a la terminal: *"Durante esta sesión, cuando escriba `python` o `pip`, usa los ejecutables que están dentro de mi carpeta `.venv`, no los del sistema operativo*".
## ¿Por qué NUNCA se debe usar sudo pip?
**Se puede romper el sistema operativo**: Linux utiliza Python para componentes críticos del sistema (como el gestor de paquetes `apt`, el gestor de red o la interfaz gráfica). Si se usa `sudo pip`, se instalan paquetes con permisos de administrador sobreescribiendo archivos en `/usr/lib/python3`. Si pip actualiza o reemplaza una librería que Ubuntu necesita en una versión diferente, se puede dejar la terminal o el sistema inoperables.
## Creación del entorno y manejo
Dentro de la raíz del proyecto se debe ejecutar: `python3 -m venv .venv`, luego estará algo similar a esto:
```css
warehouse-manager/
├── .venv/
├── src/
├── test/
├── data/
└── ...
```
Ahora se debería activar `source .venv/bin/activate` luego de eso se puede comprobar con el comando: `which python`, luego de este segundo comando saldrá está línea:
```js
/home/dgroes/Documentos/Workspace/warehouse-manager/.venv/bin/python
```
La cual conforma que **el entorno virtual está activo**. <br>
Ahora sa se podrá instalar la librería sin tocar el Python local del sistema:
```bash
python -m pip install "python-barcode[images]"
```

Luego se podrá comprobar con esto:
```bash
python -m pip show python-barcode
```
Devolviendo algo como lo siguiente:
```BASH
@dgroes ➜ warehouse-manager git(main) python -m pip show python-barcode
Name: python-barcode
Version: 0.16.1
Summary: Create standard barcodes with Python. No external modules needed. (optional Pillow support included).
Home-page: 
Author: 
Author-email: Hugo Osvaldo Barrera et al <hugo@whynothugo.nl>
License: MIT
Location: /home/dgroes/Documentos/Workspace/warehouse-manager/.venv/lib/python3.14/site-packages
Requires: 
Required-by:
```
## Similar a Docker 🐋
Conceptualmente a una similitud con docker, pero son cosas diferenctes, para ambos casos, se pueden "*instalar cosas en un entorno controlado sin tocar el sofware interno*", pero en el **nivel de aislamiento** es diferente.<br>
### `venv` 
es lo que se hizo:
```js
Ubuntu
│
├── Python del sistema
│
└── warehouse-manager
    │
    └── .venv
        ├── Python
        ├── python-barcode
        └── Pillow
```
`venv` aísla principalmente **el entorno Python y sus paquetes**
Por ejemplo `pip install python-barcode` lo instala en `warehouse-manager/.venv/` y no en Python global, pero sigue usanso el **kernel, sistema operativo, drivers, USB, archivos, etc. de Ubuntu**.
### Docker
Docker lleva el aislamiento mucho más lejos:
```js
Ubuntu
│
└── Docker
    │
    └── Container
        ├── Python
        ├── dependencias
        ├── aplicación
        └── filesystem aislado
```
El contenedor tiene su propio entorno de ejecución, por ejemplo, se podría tener :
```ts
Container A
Python 3.12
Django 5
Pillow X
```
y además, tener simuláneamente:
```bash
Container B
Python 3.14
Django 4
Pillow Y
```
sin que las dependencias de uno interfieran directamente con las del otro.
### Uso
Ahora en el fichero `src/warehouse/infrastructure/services/barcode_render/code128_barcode_renderer.py` el en cual se debe hacer uso de la librería `barcode` basta con hacer un a importación normal:
```python
import barcode
from barcode.writer import ImageWriter
```
# C
# C
# C
# C
# C
# C
# C
# C
# C
# C
