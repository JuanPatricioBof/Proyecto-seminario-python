# Proyecto EncuestAr - Seminario de python

### Grupo 38. Integrantes:

- Maia Paez
- Facundo Carbone
- Juan Patricio Bof
- Rodrigo Perez Pieroni
- x

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

Get-Command python       #verificar q pyhton se ejecute en esta carpeta

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

Los códigos de cada notebook deben ejecutarse en orden, porque algunas secciones dependen de los datos generados en otras.

---

### ✅ Para ver la página web ejecutamos en la terminar

`streamlit run EncuestAR.py`
