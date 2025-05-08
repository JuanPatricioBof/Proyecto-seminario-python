from utils.constants import DATA_OUT_PATH
import re

import json
from pathlib import Path

def obtener_periodos():
    """Obtiene el periodo más antiguo y más reciente desde el JSON de individuos
    
    Returns:
        tuple: ((año_más_antiguo, trimestre), (año_más_reciente, trimestre))
        None: Si no hay datos o el archivo no existe
    """
    json_path = DATA_OUT_PATH / "estructura_individual.json"  # Path fijo a individuos
    
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