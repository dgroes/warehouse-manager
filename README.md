
# Warehouse-Manager
## ¿Qué problema resuelve warehouse?
Sistema de gestión de inventario, ideal para la gestión de bodegas, registrando las salidas, entradas, etc.Muchas pequeñas empresas gestionan el inventario en papel o Excel, dificultando conocer el stock real y el historial de movimientos.
## ¿Quién lo usará?
Operarios de bodega y administradores, el cual poseerá una jerarquía de roles para mantener separado los permisos de cada tipo de usuario del sistema
## ¿Qué funcionalidades tendrá el MVP?
Las funcionales serán:
- Crear nuevo producto
- Actualización de stock (salida, entrada, merma)
- Gestión general de "bodegas"
- Por medio de perifericos externos impirmir códigos de barra de cada producto y lectura de códigos de barra o QR de productos para actualizar el inventario
- Visualización de un pequeño dashboard de lás métricas de los datos (esto no se si meterlo en la primera versión, pero cómo sabes que trabajé como BI, me gustaría que esto esté)
- Registro en una Base de Datos, manteniendo la data de manera integra y respaldada ante cualquier problema o migración futura
## ¿Qué funcionalidades quedan fuera del MVP?
La interfáz gráfica estaría fuera de la estructura principal, es decir PySide6 (Qt) quedaría fuera
## ¿Cuál es la visión de la versión 2?
Permitir que varios usuarios accedan simultáneamente desde distintos equipos mediante un navegador.