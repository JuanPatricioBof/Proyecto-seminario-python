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
    
    Compara los años y trimestres registrados en los archivos JSON para detectar inconsistencias,
    asegurando que cada registro en hogares.json tenga su correspondiente en individuos.json y viceversa.

    Parameters
    ----------
    json_hogares : str or Path
        Ruta del archivo JSON que contiene los datos de hogares (formato: {año: [trimestres]})
    json_individuos : str or Path
        Ruta del archivo JSON que contiene los datos de individuos (formato: {año: [trimestres]})

    Returns
    -------
    list
        Lista de mensajes con los faltantes detectados. Cada mensaje sigue el formato:
        "En el archivo de [tipo], falta el trimestre: [X] del año: [Y]"
        Retorna lista vacía si no hay inconsistencias.
    """
    faltantes = []
    
    # Cargar los datos
    with open(json_hogares, 'r') as f:
        datos_hogares = json.load(f)
    with open(json_individuos, 'r') as f:
        datos_individuos = json.load(f)

    # Verificar hogares -> individuos
    for año, trimestres in datos_hogares.items():
        for trimestre in trimestres:
            if año not in datos_individuos or trimestre not in datos_individuos[año]:
                faltantes.append(f"En el archivo de individuos, falta el trimeste: {trimestre} del año: {año}")

    # Verificar individuos -> hogares
    for año, trimestres in datos_individuos.items():
        for trimestre in trimestres:
            if año not in datos_hogares or trimestre not in datos_hogares[año]:
                faltantes.append(f"En el archivo de individuos, falta el trimeste: {trimestre} del año: {año}")

    return faltantes