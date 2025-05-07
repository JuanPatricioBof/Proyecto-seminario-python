from utils.constants import DATA_PATH
import re

# Función para detectar los trimestres disponibles
def obtener_periodos():
    periodos = []

    # Carpeta donde están los datos
    for carpeta in DATA_PATH.iterdir():
        if carpeta.is_dir():
            match = re.search(r"(\d)(er|do|to)_Trim_(\d{4})", carpeta.name)
            if match:
                trimestre = int(match.group(1))
                año = int(match.group(3))
                periodos.append((año, trimestre))

    if not periodos:
        return None

    # Ordenar los periodos de menor a mayor
    periodos.sort()
    return periodos[0], periodos[-1]