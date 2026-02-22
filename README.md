# Manual del Gestor de Eventos DAM

Este proyecto consiste en una aplicación de escritorio diseñada para gestionar la organización de eventos (conciertos, bodas, cenas, etc.). Permite registrar datos, almacenarlos en una base de datos local y visualizar estadísticas mediante un panel de control.

---

## Guía de despliegue (Instalación desde ZIP)

Si has recibido este proyecto en un archivo comprimido, sigue estos pasos para ponerlo en marcha:

1. **Descomprimir el archivo**: Extrae el contenido del ZIP en una carpeta de tu ordenador.
2. **Preparar el entorno**: Es recomendable usar un entorno virtual de Python para no mezclar librerías.
   * Abre una terminal en la carpeta del proyecto.
   * Ejecuta: `python3 -m venv .venv`
   * Activa el entorno: `source .venv/bin/activate` (en Linux) 
3. **Instalar dependencias**: Instala las librerías necesarias con el comando:
   * `pip install -r requirements.txt`
4. **Ejecutar la aplicación**: Lanza el programa principal con:
   * `python3 src/main.py`

*Nota: Al arrancar por primera vez, el programa detectará si falta la base de datos y la creará automáticamente en la carpeta data.*


## Estructura del proyecto

El código está organizado de forma separada para que sea fácil de mantener y cumpla con los estándares de desarrollo:

* **src/**: Es la carpeta raíz del código fuente.
  * **main.py**: El punto de entrada del programa. Monta la ventana principal y carga los estilos CSS.
  * **conexionBD.py**: Contiene toda la lógica de la base de datos (guardar, leer, borrar).
  * **GUI/**: Carpeta con las ventanas secundarias (el formulario de datos y la ventana de estadísticas).
* **assets/**: Contiene el archivo `style.css` que define la estética de los botones, colores y tablas.
* **data/**: Carpeta destinada al almacenamiento del archivo `eventos.db`.
* **docs/**: Contiene la documentación técnica generada automáticamente por Sphinx.
* **tests/**: Archivos de prueba para verificar que el sistema de datos funciona correctamente.

---

## Cómo funciona el programa (Lógica interna)

### 1. El flujo de datos
Cuando se abre la aplicación, el archivo `main.py` solicita a `conexionBD.py` todos los eventos guardados. Estos datos se muestran en una tabla visual (**TreeView**). 

Si el usuario pulsa en **Añadir**, se abre la ventana del formulario. Al rellenar los campos y aceptar, los datos viajan desde la interfaz hasta la función `CRUD` de la base de datos, que se encarga de insertarlos permanentemente en SQLite.

### 2. La Base de Datos (CRUD)
Se utiliza **SQLite** por ser una solución ligera que no requiere un servidor externo. El sistema implementa las cuatro operaciones fundamentales:
* **C (Create)**: Inserción de nuevos eventos.
* **R (Read)**: Lectura de la lista para mostrarla en pantalla.
* **U (Update)**: Modificación de registros existentes.
* **D (Delete)**: Borrado definitivo de datos.

### 3. El Dashboard de Estadísticas
La ventana de resumen ejecuta consultas específicas para extraer métricas en tiempo real:
* Recuento total de eventos registrados.
* Porcentaje de eventos que requieren servicio de catering.
* Filtrado de eventos marcados con **Prioridad Alta**.
* Clasificación automática por tipo de evento.

### 4. Personalización Visual
Para evitar el aspecto genérico del sistema operativo, se ha integrado un motor de **estilos CSS**. Esto permite controlar visualmente elementos como los botones de "Eliminar" (en color rojo) o "Añadir" (en color azul), mejorando la experiencia del usuario.

---

## Tecnologías utilizadas

* **Lenguaje**: Python 3.
* **Interfaz Gráfica**: GTK 3.0 (vía PyGObject).
* **Base de Datos**: SQLite 3.
* **Documentación**: Sphinx.
* **Empaquetado**: Setuptools (generación de archivos Wheel y sdist).
