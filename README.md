# Proyecto EncuestAr - Seminario de python

### Grupo 38. Integrantes:

- Maia Paez
- Facundo Carbone
- Juan Patricio Bof
- Rodrigo Perez Pieroni
- Catalina Brochero

## Pasos para instalar y ejecutar el proyecto.

### Instalación de Python

Este proyecto requiere **Python 3.10 o superior**.  
Podés verificar tu versión instalada con:

```
python3 --version
```

Si necesitás instalar Python, podés hacerlo desde [python.org](https://www.python.org/downloads/).

---

### Clonar proyecto

Para tener el repositorio en nuestra computadora, desde la terminal posicionarse en un directorio y ejecutar los siguientes comandos:

```
git clone git@gitlab.catedras.linti.unlp.edu.ar:python-2025/proyectos/grupo38/code.git
cd repositorio
```

---

### Entorno virtual

Es una buena práctica crear un entorno virtual para correr el proyecto.

```
cd repositorio

python -m venv venv      #crear entorno virtual

.\venv\Scripts\activate      #activar entorno

Get-Command python       #verificar que pyhton se ejecute en esta carpeta

deactivate      #para desactivarlo
```

---

### 📦 Instalación de dependencias:

`pip install -r requirements.txt`

---

### 🛠️ Descargar los datos de trimestres:

Entrar al siguiente enlace: [Sitio de descarga de datasets](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos) , ingresar a Microdatos y documentos 2016-2024, Base
de microdatos y luego estarán por trimestre cada encuesta realizada.

Descargar los necesarios. Se recomienda realizar la descarga en formato TXT.

Luego mover los datos descargados, sin modificar, a la carpeta `data_eph` del proyecto.

---

### 🚀 Ejecutar los notebooks.ipynb

Desde VS hay que seleccionar el kernel del entorno virtual.

Hay dos notebooks, el que procesa los datos de hogares y el que procesa los datos de individuos.
Es importante, primero ejecutar la _sección A_ de ambos y luego la B. Ya que para la sección B tienen que estar generados los 2 dataset.

Los códigos de cada notebook deben ejecutarse en orden, porque algunas secciones dependen de los datos generados en otras.

---

### ✅ Para ver la página web ejecutamos en la terminal

`streamlit run EncuestAR.py`

### 📄 En EncuestAR.py

### 🟢 Página de bienvenida

La aplicación inicia con una pantalla de bienvenida.

### 📂 Página 2 – Carga de datos
Con los datos del trimestre colocados en la carpeta data_eph, se puede iniciar el procesamiento:

Presionar “Procesar dataset…” para generar los 4 archivos CSV y los 2 archivos JSON necesarios.

Si ya existen archivos procesados pero se han agregado nuevos archivos al directorio data_eph, se recomienda presionar “Forzar actualización del dataset” para regenerar todos los datos y asegurarse de que estén actualizados

### 🧭 Navegación
Una vez procesados los datos, se puede navegar entre las distintas páginas de análisis desde la barra lateral izquierda de Streamlit.