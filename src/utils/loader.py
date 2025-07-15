import streamlit as st
import pandas as pd
import json
import os
from src.utils.constants import PATHS

# -------------------------
# FUNCIONES CON CACHE
# -------------------------

@st.cache_data
def cargar_parcial_csv(path, usecols=None, filtro=None):
    """Lee un archivo CSV y lo retorna como DataFrame de pandas parcial.

    Args:
        path (str or Path): Ruta al archivo CSV
        usecols (list), optional): Columnas a guardar. Defaults to None.
        filtro (list(tuples), optional): Años y trimestres a filtrar. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.    
    """
    if not os.path.exists(path):
        st.warning(f"⚠️ El archivo {path} no existe.")
        return pd.DataFrame() # Vacío
    
    df = pd.read_csv(path, sep=";", decimal=",", low_memory=False, usecols=usecols)
    
    if filtro:
        df = df[df[["año", "trimestre"]].apply(tuple, axis=1).isin(filtro)]
    # Explicación de como funciona
    # df[["año", "trimestre"]] #Devuelve un DataFrame con solo esas 2 columnas.
    # .apply(tuple, axis=1) Convierte cada fila en una tupla.
    # .isin(filtros) Devuelve una serie booleana que dice si cada tupla está o no en la lista de filtros: [True, False, True, False]
    # df[ ... ] Aplica ese filtro y se queda solo con las filas True.

    return df


@st.cache_data
def cargar_json(path):
    """
    Lee un archivo json y lo retorna como un diccionario con los datos convertidos a int.
    Args:
        path (str or Path): Ruta al archivo json.
    Returns:
        diccionario: los años y trimestres del tipo int.
    """

    with open(path, 'r') as f:
        fechas = json.load(f)
    return {int(k): [int(tri) for tri in v] for k, v in fechas.items()}


def obtener_fechas_comunes(json_hogares, json_individuos):
    """
    Obtiene los años y trimestres que están presentes en ambos archivos JSON.

    Parameters
    ----------
    json_hogares : str or Path
        Ruta al archivo JSON de hogares (formato: {año: [trimestres]})
    json_individuos : str or Path
        Ruta al archivo JSON de individuos (formato: {año: [trimestres]})

    Returns
    -------
    list of tuples
        Lista de tuplas con los años y trimestres comunes en formato (año, trimestre)
    """
    # Cargar los datos
    try:
        with open(json_hogares, 'r') as f:
            hogares = {int(año): [int(t) for t in trimestres] 
                    for año, trimestres in json.load(f).items()}#Conversion a int
        
        with open(json_individuos, 'r') as f:
            individuos = {int(año): [int(t) for t in trimestres] 
                        for año, trimestres in json.load(f).items()}#Conversion a int

        # Encontrar coincidencias
        fechas_comunes = []
        
        # Buscar años comunes
        años_comunes = set(hogares.keys()) & set(individuos.keys())
        
        for año in años_comunes:
            # Buscar trimestres comunes para cada año
            trimestres_comunes = set(hogares[año]) & set(individuos[año])
            for trimestre in trimestres_comunes:
                fechas_comunes.append((año, trimestre))
        return fechas_comunes
    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado - {str(e)}")
       
    except json.JSONDecodeError as e:
        print(f"Error: Archivo JSON inválido - {str(e)}")
        
    except ValueError as e:
        print(f"Error: Valor incorrecto en los datos - {str(e)}")
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
    
    

def cargar_fechas_correspondencia_en_session(forzar_actualizacion=False):
    """Carga las fechas comunes en session_state"""
    if forzar_actualizacion or 'fechas_correspondencia' not in st.session_state:
        fechas = obtener_fechas_comunes(
            PATHS["hogar"]["json"], 
            PATHS["individual"]["json"]
        )
        st.session_state.fechas_correspondencia = fechas
        if not fechas:
            st.warning("No se encontraron fechas comunes entre los datasets")
            

def verificar_fechas_cargadas_en_session():
    if 'fechas_correspondencia' not in st.session_state:
        st.spinner("cargando correspondencia en session")
        cargar_fechas_correspondencia_en_session()    

