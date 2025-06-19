"""Pagina 02. Funciones para cargar datos"""
import sys
sys.path.append("..") # Acceso a src
from src.utils.constants import DATA_OUT_PATH
import json


def obtener_periodos():
    """Obtiene el periodo más antiguo y más reciente desde el JSON de individuos
    
    Returns:
        tuple: ((año_más_antiguo, trimestre), (año_más_reciente, trimestre))
        None: Si no hay datos o el archivo no existe
    """
    json_path = DATA_OUT_PATH / "estructura_individuos.json"  # Path fijo a individuos
    
    try:
        with json_path.open('r', encoding='utf-8') as f:
            estructura = json.load(f)
            
        if not estructura:
            return None
            
        # Convertir años a enteros y ordenar
        años = sorted(int(año) for año in estructura.keys())
        
        año_antiguo = años[0]
        año_reciente = años[-1]
        
        # Obtener trimestres (el JSON ya los tiene ordenados descendentemente)
        trimestre_antiguo = int(estructura[str(año_antiguo)][-1])  # Último trimestre disponible
        trimestre_reciente = int(estructura[str(año_reciente)][0])  # Primer trimestre disponible
        
        return ((año_antiguo, trimestre_antiguo), (año_reciente, trimestre_reciente))
        
    except (FileNotFoundError, json.JSONDecodeError, IndexError, KeyError) as e:
        print(f"Error al leer periodos: {str(e)}")
        return None
def verificar_correspondencia(json_hogares, json_individuos):
    """
    Verifica la correspondencia entre archivos JSON de hogares e individuos de la EPH.
    
    Parameters
    ----------
    json_hogares : str or Path
        Ruta del archivo JSON de hogares (formato: {año: [trimestres]})
    json_individuos : str or Path
        Ruta del archivo JSON de individuos (formato: {año: [trimestres]})

    Returns
    -------
    list of tuples
        Lista de tuplas con los años y trimestres faltantes en formato (año, trimestre, tipo)
        donde tipo es 'hogares' o 'individuos' indicando dónde falta
    """
    faltantes = []
    
    # Cargar los datos
    with open(json_hogares, 'r') as f:
        datos_hogares = json.load(f)
    with open(json_individuos, 'r') as f:
        datos_individuos = json.load(f)

    # Verificar hogares -> individuos (faltantes en individuos)
    for año, trimestres in datos_hogares.items():
        año_int = int(año)  # Convertir a entero por si el JSON tiene años como strings
        for trimestre in trimestres:
            trimestre_int = int(trimestre)  # Convertir a entero
            if año not in datos_individuos or str(trimestre_int) not in datos_individuos[año]:
                faltantes.append((año_int, trimestre_int, 'individuos'))

    # Verificar individuos -> hogares (faltantes en hogares)
    for año, trimestres in datos_individuos.items():
        año_int = int(año)
        for trimestre in trimestres:
            trimestre_int = int(trimestre)
            if año not in datos_hogares or str(trimestre_int) not in datos_hogares[año]:
                faltantes.append((año_int, trimestre_int, 'hogares'))

    return faltantes